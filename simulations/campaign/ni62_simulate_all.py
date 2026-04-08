"""
Ni-62 FWS Stack Simulations — All Five Options
================================================================
Spinful BdG Hamiltonian (Rashba nanowire model) extended with
site-dependent exchange field and pairing for each Ni-62 geometry.

GoS Layer: L3 (Physics / Computation)
TAS Methodology: Each option gets an honest PASS/FAIL with
diagnosed antitheses where applicable.

Adrian Domingo · GoS-Architect · March 2026
================================================================
"""

import numpy as np
from scipy import linalg
import json
import os

# ─── Pauli matrices ───────────────────────────────────────────
σ_0 = np.eye(2, dtype=complex)
σ_x = np.array([[0, 1], [1, 0]], dtype=complex)
σ_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
σ_z = np.array([[1, 0], [0, -1]], dtype=complex)

# Particle-hole (Nambu) space
τ_0 = np.eye(2, dtype=complex)
τ_x = np.array([[0, 1], [1, 0]], dtype=complex)
τ_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
τ_z = np.array([[1, 0], [0, -1]], dtype=complex)


def kron4(σ, τ):
    """4×4 Kronecker product: spin ⊗ particle-hole."""
    return np.kron(σ, τ)


def build_rashba_bdg(N, t, mu_arr, delta_s_arr, delta_t_arr, alpha_arr, h_ex_arr):
    """
    Build the real-space BdG Hamiltonian for an N-site Rashba nanowire.

    Basis per site: Ψ_i = (c_{i↑}, c_{i↓}, c†_{i↑}, c†_{i↓})

    The 4×4 on-site block is:
        [[H_N,      Δ_pair   ],
         [Δ_pair†, -H_N^T    ]]

    where H_N = -μ σ_0 + h σ_z  (2×2 normal Hamiltonian)
    and   Δ_pair = Δ_s (iσ_y)   (2×2 singlet pairing matrix)

    Parameters (arrays of length N or N-1):
        mu_arr[i]      : chemical potential at site i
        delta_s_arr[i] : singlet (s-wave) pairing at site i
        delta_t_arr[i] : triplet (p-wave) pairing on bond (i, i+1), length N-1
        alpha_arr[i]   : Rashba SOC on bond (i, i+1), length N-1
        h_ex_arr[i]    : exchange field at site i

    Returns:
        H_bdg : (4N × 4N) Hermitian matrix
    """
    dim = 4 * N
    H = np.zeros((dim, dim), dtype=complex)

    iσy = 1j * σ_y  # [[0, 1], [-1, 0]]

    for i in range(N):
        # Normal-state 2×2 block
        H_N = -mu_arr[i] * σ_0 + h_ex_arr[i] * σ_z
        # Singlet pairing 2×2
        Δ_pair = delta_s_arr[i] * iσy

        # Assemble 4×4 BdG on-site block
        blk = np.zeros((4, 4), dtype=complex)
        blk[0:2, 0:2] = H_N                    # electron block
        blk[2:4, 2:4] = -H_N.T                 # hole block (time-reversed)
        blk[0:2, 2:4] = Δ_pair                 # pairing
        blk[2:4, 0:2] = Δ_pair.conj().T        # pairing†

        s = 4 * i
        H[s:s+4, s:s+4] += blk

    for i in range(N - 1):
        # Normal hopping: -t σ_0
        T_N = -t * σ_0
        # Rashba SOC: iα σ_y (antisymmetric under Hermitian conjugate)
        T_N = T_N + 1j * alpha_arr[i] * σ_y

        # Triplet pairing on bond: Δ_t (iσ_y) — p-wave component
        Δ_hop = delta_t_arr[i] * iσy

        # Assemble 4×4 hopping block
        hop = np.zeros((4, 4), dtype=complex)
        hop[0:2, 0:2] = T_N                    # electron hopping
        hop[2:4, 2:4] = -T_N.T                 # hole hopping (time-reversed)
        hop[0:2, 2:4] = Δ_hop                  # triplet pairing on bond
        hop[2:4, 0:2] = Δ_hop.conj().T

        si = 4 * i
        sj = 4 * (i + 1)
        H[si:si+4, sj:sj+4] += hop
        H[sj:sj+4, si:si+4] += hop.conj().T

    # Verify Hermiticity
    herm_err = np.max(np.abs(H - H.conj().T))
    assert herm_err < 1e-10, f"BdG Hamiltonian not Hermitian (err={herm_err:.2e})"
    return H


def analyze_bdg(H, N, label, defect_sites=None):
    """
    Diagonalize BdG Hamiltonian and extract diagnostics.

    Returns dict with:
        - energies (sorted)
        - gap (smallest |E| among all eigenvalues)
        - near_zero_modes (number of eigenvalues with |E| < gap_threshold)
        - mzm_localization (edge weight of near-zero modes)
        - topological (bool: are there robust zero modes?)
    """
    evals, evecs = linalg.eigh(H)

    # Sort by absolute energy
    idx_sorted = np.argsort(np.abs(evals))
    evals_sorted = evals[idx_sorted]

    # Gap: smallest positive eigenvalue above a numerical threshold
    pos_evals = evals[evals > 1e-10]
    gap = float(np.min(pos_evals)) if len(pos_evals) > 0 else 0.0

    # Near-zero modes: |E| < 0.05 * t (energy unit)
    gap_threshold = 0.05
    near_zero_mask = np.abs(evals) < gap_threshold
    n_zero_modes = int(np.sum(near_zero_mask))

    # Localization analysis for near-zero modes
    edge_weight = 0.0
    defect_weight = 0.0
    bulk_weight = 0.0
    n_edge_sites = max(N // 10, 2)

    if n_zero_modes > 0:
        zero_vecs = evecs[:, near_zero_mask]
        # Probability density per site (sum over spin and particle-hole)
        prob = np.zeros(N)
        for site in range(N):
            s = 4 * site
            prob[site] = np.sum(np.abs(zero_vecs[s:s+4, :])**2)
        prob /= (np.sum(prob) + 1e-30)

        # Edge weight
        edge_weight = float(np.sum(prob[:n_edge_sites]) + np.sum(prob[-n_edge_sites:]))

        # Defect weight
        if defect_sites is not None and len(defect_sites) > 0:
            defect_weight = float(np.sum(prob[defect_sites]))
            # Bulk = everything not edge and not defect
            bulk_mask = np.ones(N, dtype=bool)
            bulk_mask[:n_edge_sites] = False
            bulk_mask[-n_edge_sites:] = False
            bulk_mask[defect_sites] = False
            bulk_weight = float(np.sum(prob[bulk_mask]))
        else:
            bulk_weight = float(np.sum(prob[n_edge_sites:-n_edge_sites]))
    else:
        prob = np.zeros(N)

    # Topological criterion: ≥2 near-zero modes with high edge or defect localization
    localization = max(edge_weight, defect_weight)
    is_topological = (n_zero_modes >= 2) and (localization > 0.5)

    return {
        "label": label,
        "N_sites": N,
        "gap": round(gap, 6),
        "n_zero_modes": n_zero_modes,
        "edge_weight": round(edge_weight, 4),
        "defect_weight": round(defect_weight, 4),
        "bulk_weight": round(bulk_weight, 4),
        "localization_max": round(localization, 4),
        "is_topological": is_topological,
        "lowest_10_energies": [round(float(e), 6) for e in evals_sorted[:10]],
        "site_probability": prob.tolist(),
    }


# ─── Physical Parameters ──────────────────────────────────────
N = 100          # Chain length
t = 1.0          # Hopping (energy unit)
mu_0 = 0.5       # Chemical potential
Delta_s = 0.3    # Singlet pairing from Nb proximity
alpha_R = 0.5    # Rashba SOC
h_ex_Ni = 0.6    # Exchange field from Ni-62
# Topological condition: h > sqrt(mu^2 + Delta^2) = sqrt(0.34) ≈ 0.583
# h_ex_Ni = 0.6 is just above threshold.

# Defect sites: central region modeling a 5/7 SW defect
defect_center = N // 2
defect_half_width = 5
defect_sites = list(range(defect_center - defect_half_width,
                          defect_center + defect_half_width + 1))
defect_set = set(defect_sites)


# ─── CONTROL: No Ni-62 (Original Kitaev-like, no exchange) ───
def run_control():
    mu = np.full(N, mu_0)
    delta_s = np.full(N, Delta_s)
    delta_t = np.zeros(N - 1)
    alpha = np.full(N - 1, alpha_R)
    h_ex = np.zeros(N)

    H = build_rashba_bdg(N, t, mu, delta_s, delta_t, alpha, h_ex)
    result = analyze_bdg(H, N, "CONTROL: No Ni-62 (h_ex=0)")
    result["option"] = "Control"
    result["status"] = "TRIVIAL" if not result["is_topological"] else "TOPOLOGICAL"
    result["diagnosis"] = (
        "No time-reversal breaking. System is in class BDI. "
        "Without exchange field, the Rashba nanowire is in the trivial phase "
        f"(need h > {np.sqrt(mu_0**2 + Delta_s**2):.3f}, have h=0). "
        "This is the expected baseline: no MZMs without T-breaking."
    )
    return result


# ─── OPTION A: Uniform exchange layer ─────────────────────────
def run_option_a():
    mu = np.full(N, mu_0)
    # Pair-breaking: continuous Ni film drastically reduces Δ_eff
    # ξ_F ~ 1-2 nm in Ni. For a ~2 nm Ni layer, Δ_eff drops to ~10% of Δ_Nb
    delta_eff = Delta_s * 0.10  # 90% suppression from pair-breaking
    delta_s = np.full(N, delta_eff)
    delta_t = np.zeros(N - 1)
    alpha = np.full(N - 1, alpha_R * 1.3)  # Enhanced SOC from Ni proximity
    h_ex = np.full(N, h_ex_Ni)

    H = build_rashba_bdg(N, t, mu, delta_s, delta_t, alpha, h_ex)
    result = analyze_bdg(H, N, "OPTION A: Uniform exchange layer (Ni-62 between graphene & Nb)")
    result["option"] = "A"
    result["Delta_eff"] = round(float(delta_eff), 4)
    h_threshold = np.sqrt(mu_0**2 + delta_eff**2)
    result["h_threshold"] = round(float(h_threshold), 4)

    if result["is_topological"]:
        result["status"] = "PASS"
        result["diagnosis"] = (
            f"Topological phase achieved. h_ex={h_ex_Ni} > threshold={h_threshold:.3f}. "
            f"But gap is very small ({result['gap']:.4f}) due to pair-breaking "
            f"(Δ_eff={delta_eff:.3f} vs Δ_Nb={Delta_s}). "
            "ANTITHESIS: Gap too small for realistic certification. "
            "Thermal fluctuations at any nonzero T would close this gap. "
            "The 90% Δ suppression from a continuous Ni film makes this "
            "technically topological but practically uncertifiable."
        )
    else:
        result["status"] = "FAIL"
        result["diagnosis"] = (
            f"Pair-breaking from continuous Ni film suppresses Δ_eff to {delta_eff:.3f}. "
            f"While h_ex={h_ex_Ni} > threshold={h_threshold:.3f} (class D topology "
            "is mathematically allowed), the induced gap is too small to support "
            "well-separated zero modes. "
            "ANTITHESIS: Continuous ferromagnetic film kills superconducting "
            "proximity before topology can emerge. This is the central tension "
            "in Option A — exchange and pairing compete destructively."
        )
    return result


# ─── OPTION B: Ni-62 substrate under graphene ─────────────────
def run_option_b():
    mu = np.full(N, mu_0)
    # SC proximity from Nb above is NOT blocked (Ni is below, Nb is above)
    # But the Dirac cone is destroyed by strong Ni-C hybridization
    # Model: full Δ from Nb, but μ shifted ~2 eV (=2.0 in our units) and
    # band structure fundamentally altered. We model this as large μ shift.
    mu_shifted = mu_0 + 2.0  # Dirac cone shifted far from Fermi level
    mu = np.full(N, mu_shifted)
    delta_s = np.full(N, Delta_s)
    delta_t = np.zeros(N - 1)
    alpha = np.full(N - 1, alpha_R * 1.5)  # Giant enhanced SOC from Ni substrate
    h_ex = np.full(N, h_ex_Ni)

    H = build_rashba_bdg(N, t, mu, delta_s, delta_t, alpha, h_ex)
    result = analyze_bdg(H, N, "OPTION B: Ni-62(111) substrate under graphene")
    result["option"] = "B"
    result["mu_shifted"] = round(float(mu_shifted), 4)
    h_threshold = np.sqrt(mu_shifted**2 + Delta_s**2)
    result["h_threshold"] = round(float(h_threshold), 4)

    result["status"] = "FAIL"
    result["diagnosis"] = (
        f"Ni(111) substrate shifts graphene π-band ~2 eV below E_F via "
        f"C p_z–Ni 3d hybridization. Effective μ={mu_shifted:.1f} puts system "
        f"far from the topological regime (threshold h > {h_threshold:.2f}, "
        f"have h={h_ex_Ni}). "
        "ANTITHESIS: The 1.2% lattice match between Ni(111) and graphene "
        "enables perfect epitaxy but DESTROYS the Dirac cone. The very "
        "property that makes Ni an excellent graphene substrate (strong "
        "hybridization) is what kills the topological physics. "
        "This is not a parameter tuning problem — it is structural. "
        "Even with enhanced SOC (~1.5×), the system is deep in the trivial phase."
    )
    return result


# ─── OPTION C: Patterned Ni-62 at defect sites ────────────────
def run_option_c():
    mu = np.full(N, mu_0)
    delta_s = np.full(N, Delta_s)
    delta_t = np.zeros(N - 1)

    # SOC: baseline everywhere, enhanced at defect sites
    alpha = np.full(N - 1, alpha_R)
    for i in range(N - 1):
        if i in defect_set or (i + 1) in defect_set:
            alpha[i] = alpha_R * 1.3  # Enhanced by Ni proximity at defects

    # Exchange: zero in bulk, h_ex at defect sites
    h_ex = np.zeros(N)
    h_ex[defect_sites] = h_ex_Ni

    H = build_rashba_bdg(N, t, mu, delta_s, delta_t, alpha, h_ex)
    result = analyze_bdg(H, N,
                         "OPTION C: Ni-62 nano-islands at 5/7 defect sites",
                         defect_sites=np.array(defect_sites))
    result["option"] = "C"
    result["defect_sites"] = defect_sites
    result["defect_width"] = 2 * defect_half_width + 1
    h_threshold = np.sqrt(mu_0**2 + Delta_s**2)
    result["h_threshold"] = round(float(h_threshold), 4)

    if result["is_topological"]:
        result["status"] = "PASS"
        result["diagnosis"] = (
            f"Topological domain wall achieved. Exchange h={h_ex_Ni} applied "
            f"only at defect sites (sites {defect_sites[0]}-{defect_sites[-1]}). "
            f"Bulk: trivial (h=0 < threshold {h_threshold:.3f}). "
            f"Defect region: topological (h={h_ex_Ni} > {h_threshold:.3f}). "
            f"MZMs localize at domain walls between trivial/topological regions. "
            f"Defect localization: {result['defect_weight']:.1%}. "
            f"Gap: {result['gap']:.4f}. "
            "Full Δ preserved everywhere (no continuous Ni film blocking proximity). "
            "This is the architecture-aligned result: Penrose-seeded defects "
            "host the local topological phase, MZMs appear at defect boundaries."
        )
    else:
        result["status"] = "PARTIAL"
        result["diagnosis"] = (
            f"Exchange field applied at defect sites, but topological domain "
            f"may be too narrow ({2*defect_half_width+1} sites) to support "
            "well-separated MZMs. The two domain walls are close together, "
            "causing hybridization of the MZMs and energy splitting away from "
            "zero. ANTITHESIS: defect region may need to be wider, or exchange "
            "field stronger, for robust zero modes. "
            f"Defect localization: {result['defect_weight']:.1%}, "
            f"Gap: {result['gap']:.4f}."
        )
    return result


# ─── OPTION D: Ni-62/Nb bilayer triplet generator ─────────────
def run_option_d():
    mu = np.full(N, mu_0)
    # No exchange at the graphene level (Ni is above Nb, not touching graphene)
    h_ex = np.zeros(N)
    alpha = np.full(N - 1, alpha_R)

    # The Ni-62/Nb interface converts singlet to triplet.
    # Model: reduced singlet + induced triplet pairing at all sites
    delta_s = np.full(N, Delta_s * 0.5)  # Partial singlet survives
    # Triplet pairing (p-wave, on bonds) — conversion efficiency ~20-30%
    delta_t = np.full(N - 1, Delta_s * 0.25)

    H = build_rashba_bdg(N, t, mu, delta_s, delta_t, alpha, h_ex)
    result = analyze_bdg(H, N, "OPTION D: Ni-62/Nb bilayer triplet generator")
    result["option"] = "D"
    result["delta_s_eff"] = round(float(Delta_s * 0.5), 4)
    result["delta_t_eff"] = round(float(Delta_s * 0.25), 4)

    if result["is_topological"]:
        result["status"] = "PASS"
        result["diagnosis"] = (
            "Triplet pairing from Ni-62/Nb interface induces effective p-wave "
            f"component (Δ_t={Delta_s*0.25:.3f}). With residual singlet "
            f"(Δ_s={Delta_s*0.5:.3f}), the system may enter a topological phase "
            "even without explicit T-breaking at the graphene level. "
            "NOTE: This result depends sensitively on the triplet conversion "
            "efficiency, which is hard to control experimentally."
        )
    else:
        result["status"] = "FAIL"
        result["diagnosis"] = (
            "Without exchange field at the graphene level (h_ex=0), the system "
            "lacks time-reversal symmetry breaking. Triplet pairing alone "
            f"(Δ_t={Delta_s*0.25:.3f}) is present but without a Zeeman-like "
            "term to select a spin channel, the system remains in a "
            "time-reversal invariant class (DIII) where the invariant is Z₂. "
            "The p-wave component is too weak relative to the residual singlet "
            "to drive a topological transition. "
            "ANTITHESIS: Triplet conversion without local T-breaking is "
            "architecturally indirect — it doesn't create the domain-wall "
            "geometry your 5/7 defect picture requires. The MZMs, if they "
            "appeared, would be at the chain ends, not at defect boundaries."
        )
    return result


# ─── OPTION E: Hybrid — Ni-62 at defects + Nb above ───────────
def run_option_e():
    mu = np.full(N, mu_0)

    # Singlet pairing: full everywhere
    delta_s = np.full(N, Delta_s)

    # Exchange: only at defect sites
    h_ex = np.zeros(N)
    h_ex[defect_sites] = h_ex_Ni

    # SOC: enhanced at defect sites
    alpha = np.full(N - 1, alpha_R)
    for i in range(N - 1):
        if i in defect_set or (i + 1) in defect_set:
            alpha[i] = alpha_R * 1.3

    # Triplet pairing: induced at boundaries of Ni-62 islands
    # (magnetization inhomogeneity enables singlet→triplet conversion)
    delta_t = np.zeros(N - 1)
    defect_boundary = set()
    for s in defect_sites:
        if s - 1 >= 0 and s - 1 not in defect_set:
            defect_boundary.add(s - 1)
        if s + 1 < N and s + 1 not in defect_set:
            defect_boundary.add(s)
    for b in defect_boundary:
        if b < N - 1:
            delta_t[b] = Delta_s * 0.15  # Small triplet component at boundaries

    H = build_rashba_bdg(N, t, mu, delta_s, delta_t, alpha, h_ex)
    result = analyze_bdg(H, N,
                         "OPTION E: Hybrid — Ni-62 at defects + triplet at boundaries",
                         defect_sites=np.array(defect_sites))
    result["option"] = "E"
    result["defect_sites"] = defect_sites
    result["n_boundary_bonds"] = len(defect_boundary)
    h_threshold = np.sqrt(mu_0**2 + Delta_s**2)
    result["h_threshold"] = round(float(h_threshold), 4)

    if result["is_topological"]:
        result["status"] = "PASS"
        result["diagnosis"] = (
            f"Hybrid configuration: exchange h={h_ex_Ni} at defects, full Δ "
            f"everywhere, triplet component at {len(defect_boundary)} boundary bonds. "
            f"Defect region is topological (class D), bulk is trivial (class BDI). "
            f"MZMs localize at domain walls. "
            f"Defect localization: {result['defect_weight']:.1%}. "
            f"Edge localization: {result['edge_weight']:.1%}. "
            f"Gap: {result['gap']:.4f}. "
            "The triplet component at boundaries may slightly enhance the "
            "topological gap at the domain wall, though the effect is small. "
            "This is Option C with an additional physical mechanism at the "
            "domain walls — architecturally equivalent but with richer physics."
        )
    else:
        result["status"] = "PARTIAL"
        result["diagnosis"] = (
            f"Similar to Option C: defect region too narrow for fully separated "
            f"MZMs, or exchange/SOC balance needs tuning. "
            f"Defect localization: {result['defect_weight']:.1%}. "
            f"Gap: {result['gap']:.4f}. "
            "The triplet boundary component adds complexity without qualitatively "
            "changing the result relative to Option C."
        )
    return result


# ─── PARAMETER SWEEP: Defect width scan for Option C ──────────
def sweep_defect_width():
    """Scan defect region width to find minimum for robust MZMs."""
    results = []
    for half_w in range(2, 30):
        dsites = list(range(N//2 - half_w, N//2 + half_w + 1))
        dset = set(dsites)
        width = 2 * half_w + 1

        mu = np.full(N, mu_0)
        delta_s = np.full(N, Delta_s)
        delta_t = np.zeros(N - 1)
        alpha = np.full(N - 1, alpha_R)
        for i in range(N - 1):
            if i in dset or (i + 1) in dset:
                alpha[i] = alpha_R * 1.3
        h_ex = np.zeros(N)
        for s in dsites:
            h_ex[s] = h_ex_Ni

        H = build_rashba_bdg(N, t, mu, delta_s, delta_t, alpha, h_ex)
        r = analyze_bdg(H, N, f"C_sweep_w{width}", defect_sites=np.array(dsites))
        results.append({
            "width": width,
            "gap": r["gap"],
            "n_zero_modes": r["n_zero_modes"],
            "defect_weight": r["defect_weight"],
            "edge_weight": r["edge_weight"],
            "is_topological": r["is_topological"],
            "lowest_energy": r["lowest_10_energies"][0] if r["lowest_10_energies"] else None,
        })
    return results


# ─── PARAMETER SWEEP: Exchange strength scan for Option C ─────
def sweep_exchange_strength():
    """Scan h_ex from 0 to 1.5 for fixed defect width."""
    results = []
    for h_val in np.linspace(0.0, 1.5, 31):
        mu = np.full(N, mu_0)
        delta_s = np.full(N, Delta_s)
        delta_t = np.zeros(N - 1)
        alpha = np.full(N - 1, alpha_R)
        for i in range(N - 1):
            if i in defect_set or (i + 1) in defect_set:
                alpha[i] = alpha_R * 1.3
        h_ex = np.zeros(N)
        h_ex[defect_sites] = h_val

        H = build_rashba_bdg(N, t, mu, delta_s, delta_t, alpha, h_ex)
        r = analyze_bdg(H, N, f"C_sweep_h{h_val:.2f}", defect_sites=np.array(defect_sites))
        results.append({
            "h_ex": round(float(h_val), 3),
            "gap": r["gap"],
            "n_zero_modes": r["n_zero_modes"],
            "defect_weight": r["defect_weight"],
            "is_topological": r["is_topological"],
            "lowest_energy": r["lowest_10_energies"][0] if r["lowest_10_energies"] else None,
        })
    return results


# ─── MAIN ─────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 70)
    print("  Ni-62 FWS Stack Simulations — All Five Options")
    print("  GoS L3 · Spinful BdG · TAS Methodology")
    print("=" * 70)

    all_results = {}

    # Control
    print("\n[CONTROL] Running baseline (no Ni-62)...")
    ctrl = run_control()
    all_results["control"] = ctrl
    print(f"  Status: {ctrl['status']}")
    print(f"  Zero modes: {ctrl['n_zero_modes']}, Gap: {ctrl['gap']:.4f}")

    # Option A
    print("\n[OPTION A] Uniform exchange layer...")
    a = run_option_a()
    all_results["option_a"] = a
    print(f"  Status: {a['status']}")
    print(f"  Δ_eff: {a.get('Delta_eff', '?')}, Gap: {a['gap']:.4f}")
    print(f"  Zero modes: {a['n_zero_modes']}, Edge weight: {a['edge_weight']:.1%}")

    # Option B
    print("\n[OPTION B] Ni-62 substrate...")
    b = run_option_b()
    all_results["option_b"] = b
    print(f"  Status: {b['status']}")
    print(f"  μ_shifted: {b.get('mu_shifted', '?')}, Gap: {b['gap']:.4f}")

    # Option C
    print("\n[OPTION C] Patterned at defect sites...")
    c = run_option_c()
    all_results["option_c"] = c
    print(f"  Status: {c['status']}")
    print(f"  Zero modes: {c['n_zero_modes']}, Gap: {c['gap']:.4f}")
    print(f"  Defect weight: {c['defect_weight']:.1%}, Edge: {c['edge_weight']:.1%}")

    # Option D
    print("\n[OPTION D] Triplet generator...")
    d = run_option_d()
    all_results["option_d"] = d
    print(f"  Status: {d['status']}")
    print(f"  Δ_s: {d.get('delta_s_eff', '?')}, Δ_t: {d.get('delta_t_eff', '?')}")
    print(f"  Zero modes: {d['n_zero_modes']}, Gap: {d['gap']:.4f}")

    # Option E
    print("\n[OPTION E] Hybrid (C + triplet at boundaries)...")
    e = run_option_e()
    all_results["option_e"] = e
    print(f"  Status: {e['status']}")
    print(f"  Zero modes: {e['n_zero_modes']}, Gap: {e['gap']:.4f}")
    print(f"  Defect weight: {e['defect_weight']:.1%}, Edge: {e['edge_weight']:.1%}")

    # Parameter sweeps for Option C
    print("\n[SWEEP] Defect width scan (Option C)...")
    width_sweep = sweep_defect_width()
    all_results["sweep_defect_width"] = width_sweep
    topological_widths = [r for r in width_sweep if r["is_topological"]]
    if topological_widths:
        min_w = topological_widths[0]["width"]
        print(f"  Minimum topological defect width: {min_w} sites")
    else:
        print("  No topological phase found in width sweep (5 to 59 sites)")

    print("\n[SWEEP] Exchange strength scan (Option C)...")
    h_sweep = sweep_exchange_strength()
    all_results["sweep_exchange_strength"] = h_sweep
    topo_h = [r for r in h_sweep if r["is_topological"]]
    if topo_h:
        min_h = topo_h[0]["h_ex"]
        print(f"  Minimum topological exchange field: {min_h}")
    else:
        print("  No topological phase found in exchange sweep")

    # ─── Summary Table ─────────────────────────────────────────
    print("\n" + "=" * 70)
    print("  SUMMARY TABLE")
    print("=" * 70)
    header = f"{'Option':<12} {'Status':<10} {'#ZM':<5} {'Gap':<8} {'Edge%':<8} {'Defect%':<9} {'Topo?'}"
    print(header)
    print("-" * 70)
    for key in ["control", "option_a", "option_b", "option_c", "option_d", "option_e"]:
        r = all_results[key]
        label = r.get("option", "Ctrl")
        print(f"{label:<12} {r['status']:<10} {r['n_zero_modes']:<5} "
              f"{r['gap']:<8.4f} {r['edge_weight']:<8.1%} "
              f"{r['defect_weight']:<9.1%} {'YES' if r['is_topological'] else 'NO'}")

    # ─── Full Diagnostics ──────────────────────────────────────
    print("\n" + "=" * 70)
    print("  DIAGNOSTICS (per option)")
    print("=" * 70)
    for key in ["control", "option_a", "option_b", "option_c", "option_d", "option_e"]:
        r = all_results[key]
        print(f"\n--- {r['label']} ---")
        print(f"  {r['diagnosis']}")

    # ─── Save JSON report ──────────────────────────────────────
    # Strip site_probability arrays to keep JSON manageable
    report = {}
    for key, val in all_results.items():
        if isinstance(val, dict):
            report[key] = {k: v for k, v in val.items() if k != "site_probability"}
        elif isinstance(val, list):
            report[key] = val
        else:
            report[key] = val

    report["parameters"] = {
        "N": N, "t": t, "mu_0": mu_0, "Delta_s": Delta_s,
        "alpha_R": alpha_R, "h_ex_Ni": h_ex_Ni,
        "defect_center": defect_center,
        "defect_half_width": defect_half_width,
        "topological_threshold": round(float(np.sqrt(mu_0**2 + Delta_s**2)), 4),
    }
    report["methodology"] = "TAS: Each option simulated, failures diagnosed as antitheses"
    report["model"] = "Spinful BdG, Rashba nanowire, site-dependent exchange and SOC"

    os.makedirs("/home/claude/output", exist_ok=True)
    with open("/home/claude/output/ni62_simulation_report.json", "w") as f:
        json.dump(report, f, indent=2, default=str)

    print(f"\n[SAVED] Full report → ni62_simulation_report.json")

    # ─── Generate plots ────────────────────────────────────────
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, axes = plt.subplots(3, 2, figsize=(14, 16))
        fig.suptitle("Ni-62 FWS Stack: All Options — BdG Spectrum & MZM Localization",
                      fontsize=14, fontweight="bold", y=0.98)

        option_keys = ["control", "option_a", "option_b", "option_c", "option_d", "option_e"]
        option_labels = ["CONTROL (no Ni-62)", "A: Uniform Exchange",
                         "B: Ni-62 Substrate", "C: Patterned at Defects",
                         "D: Triplet Generator", "E: Hybrid (C + Triplet)"]
        colors = ["#666666", "#e74c3c", "#e74c3c", "#27ae60", "#3498db", "#27ae60"]

        # Recompute site probabilities for plotting (we stripped them from report)
        site_probs = {}
        for key in option_keys:
            r = all_results[key]
            if "site_probability" in r:
                site_probs[key] = r["site_probability"]
            else:
                site_probs[key] = np.zeros(N)

        for idx, (key, label, color) in enumerate(zip(option_keys, option_labels, colors)):
            ax = axes[idx // 2, idx % 2]
            r = all_results[key]
            prob = np.array(site_probs[key])

            # Plot site probability
            ax.bar(range(N), prob, width=1.0, color=color, alpha=0.7)

            # Mark defect region
            if key in ["option_c", "option_e"]:
                ax.axvspan(defect_sites[0] - 0.5, defect_sites[-1] + 0.5,
                          alpha=0.15, color="orange", label="Ni-62 defect region")

            status = r.get("status", "?")
            status_color = {"PASS": "green", "FAIL": "red", "PARTIAL": "orange",
                           "TRIVIAL": "gray", "TOPOLOGICAL": "green"}.get(status, "black")

            ax.set_title(f"{label}\n[{status}] gap={r['gap']:.4f}, "
                        f"#ZM={r['n_zero_modes']}", fontsize=10,
                        color=status_color)
            ax.set_xlabel("Site index")
            ax.set_ylabel("|ψ|² (zero-mode probability)")
            ax.set_xlim(-1, N)
            if key in ["option_c", "option_e"]:
                ax.legend(fontsize=8, loc="upper right")

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig("/home/claude/output/ni62_all_options_localization.png", dpi=150)
        print("[SAVED] Localization plot → ni62_all_options_localization.png")

        # ─── Spectrum plot: lowest eigenvalues ─────────────────
        fig2, axes2 = plt.subplots(3, 2, figsize=(14, 16))
        fig2.suptitle("Ni-62 FWS Stack: Low-Energy BdG Spectra",
                       fontsize=14, fontweight="bold", y=0.98)

        for idx, (key, label, color) in enumerate(zip(option_keys, option_labels, colors)):
            ax = axes2[idx // 2, idx % 2]
            r = all_results[key]
            energies = r["lowest_10_energies"]

            ax.barh(range(len(energies)), energies, color=color, alpha=0.8)
            ax.axvline(0, color="black", linewidth=0.5, linestyle="--")
            ax.set_xlabel("Energy (units of t)")
            ax.set_ylabel("Eigenvalue index")
            ax.set_title(f"{label} — Lowest 10 eigenvalues", fontsize=10)

        plt.tight_layout(rect=[0, 0, 1, 0.96])
        plt.savefig("/home/claude/output/ni62_all_options_spectra.png", dpi=150)
        print("[SAVED] Spectra plot → ni62_all_options_spectra.png")

        # ─── Sweep plots ──────────────────────────────────────
        fig3, (ax_w, ax_h) = plt.subplots(1, 2, figsize=(14, 5))
        fig3.suptitle("Option C Parameter Sweeps", fontsize=13, fontweight="bold")

        # Width sweep
        widths = [r["width"] for r in width_sweep]
        gaps = [r["gap"] for r in width_sweep]
        dw = [r["defect_weight"] for r in width_sweep]
        topo_mask = [r["is_topological"] for r in width_sweep]

        ax_w.plot(widths, gaps, "o-", color="#27ae60", markersize=4, label="Gap")
        ax_w2 = ax_w.twinx()
        ax_w2.plot(widths, dw, "s-", color="#3498db", markersize=4, label="Defect weight")
        for i, topo in enumerate(topo_mask):
            if topo:
                ax_w.axvspan(widths[i]-0.5, widths[i]+0.5, alpha=0.08, color="green")
        ax_w.set_xlabel("Defect region width (sites)")
        ax_w.set_ylabel("Gap (t)", color="#27ae60")
        ax_w2.set_ylabel("Defect weight", color="#3498db")
        ax_w.set_title("Defect Width Sweep")

        # Exchange sweep
        hs = [r["h_ex"] for r in h_sweep]
        gaps_h = [r["gap"] for r in h_sweep]
        dw_h = [r["defect_weight"] for r in h_sweep]
        topo_h_mask = [r["is_topological"] for r in h_sweep]
        h_thresh = np.sqrt(mu_0**2 + Delta_s**2)

        ax_h.plot(hs, gaps_h, "o-", color="#27ae60", markersize=4, label="Gap")
        ax_h2 = ax_h.twinx()
        ax_h2.plot(hs, dw_h, "s-", color="#3498db", markersize=4, label="Defect weight")
        ax_h.axvline(h_thresh, color="red", linestyle="--", alpha=0.7,
                     label=f"Threshold h={h_thresh:.3f}")
        for i, topo in enumerate(topo_h_mask):
            if topo:
                ax_h.axvspan(hs[i]-0.025, hs[i]+0.025, alpha=0.08, color="green")
        ax_h.set_xlabel("Exchange field h_ex (t)")
        ax_h.set_ylabel("Gap (t)", color="#27ae60")
        ax_h2.set_ylabel("Defect weight", color="#3498db")
        ax_h.set_title("Exchange Strength Sweep")
        ax_h.legend(fontsize=8, loc="upper left")

        plt.tight_layout()
        plt.savefig("/home/claude/output/ni62_option_c_sweeps.png", dpi=150)
        print("[SAVED] Sweep plots → ni62_option_c_sweeps.png")

    except Exception as ex:
        print(f"[WARN] Plot generation failed: {ex}")

    print("\n" + "=" * 70)
    print("  SIMULATION COMPLETE")
    print("=" * 70)
