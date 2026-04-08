#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  FWS Simulation Runner v2 — Corrected Lattice
  
  Uses honeycomb graphene + Penrose-selected Stone-Wales defects
  instead of raw Penrose tiling vertices.
  
  Fix: CN ∈ {2,3,4} (honeycomb) instead of CN ∈ {3,4,5,6,8,10} (Penrose)
═══════════════════════════════════════════════════════════════════════════════
"""

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from scipy.linalg import eigh
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, sys, json, time

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer): return int(obj)
        if isinstance(obj, np.floating): return float(obj)
        if isinstance(obj, np.ndarray): return obj.tolist()
        if isinstance(obj, np.bool_): return bool(obj)
        if isinstance(obj, (set, frozenset)): return list(obj)
        return super().default(obj)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graphene_sw_lattice import generate_lattice, plot_lattice


# ═══════════════════════════════════════════════════════════════════════════
# BdG HAMILTONIAN (adapted from penrose_bdg_2d.py to accept external lattice)
# ═══════════════════════════════════════════════════════════════════════════

def harrison_hopping(d, d0, t0=1.0):
    return t0 * (d0 / d) ** 2

def build_bdg(positions, bonds, bond_lengths, d0, t0=1.0, mu=1.0, delta=0.5):
    """Build 2N×2N BdG Hamiltonian with Harrison-scaled hopping + p-wave pairing."""
    N = len(positions)
    # H block
    h_row, h_col, h_data = [], [], []
    for i in range(N):
        h_row.append(i); h_col.append(i); h_data.append(-mu)
    for k, (i, j) in enumerate(bonds):
        t = harrison_hopping(bond_lengths[k], d0, t0)
        h_row += [i, j]; h_col += [j, i]; h_data += [-t, -t]
    H = sparse.csr_matrix((h_data, (h_row, h_col)), shape=(N, N))

    # Delta block (p-wave)
    d_row, d_col, d_data = [], [], []
    for k, (i, j) in enumerate(bonds):
        dij = delta * (d0 / bond_lengths[k]) ** 2
        d_row += [i, j]; d_col += [j, i]; d_data += [dij, -dij]
    D = sparse.csr_matrix((d_data, (d_row, d_col)), shape=(N, N))

    H_BdG = sparse.bmat([[H, D], [D.conj().T, -H.conj()]], format='csr')
    return H_BdG


def compute_bott_index(positions, eigvecs_occ, N):
    """Bott index B — 2D topological invariant for disordered systems."""
    x = positions[:, 0]; y = positions[:, 1]
    Lx = x.max() - x.min(); Ly = y.max() - y.min()
    xn = (x - x.min()) / max(Lx, 1e-10)
    yn = (y - y.min()) / max(Ly, 1e-10)
    V = eigvecs_occ[:N, :]
    Ux = V.conj().T @ np.diag(np.exp(2j*np.pi*xn)) @ V
    Uy = V.conj().T @ np.diag(np.exp(2j*np.pi*yn)) @ V
    try:
        comm = Ux @ Uy @ np.linalg.inv(Ux) @ np.linalg.inv(Uy)
        eigvals = np.linalg.eigvals(comm)
        return np.sum(np.log(eigvals)).imag / (2 * np.pi)
    except Exception:
        return np.nan


# ═══════════════════════════════════════════════════════════════════════════
# PHONON ANALYSIS (adapted from penrose_phonon_2d.py)
# ═══════════════════════════════════════════════════════════════════════════

def spring_constant(d, d0, k0=1.0):
    return k0 * (d0 / d) ** 4

def build_dynamical_matrix(positions, bonds, bond_lengths, d0, k0=1.0, ordered=False):
    """Scalar dynamical matrix. If ordered=True, use uniform k₀."""
    N = len(positions)
    row, col, data = [], [], []
    diag = np.zeros(N)
    for idx, (i, j) in enumerate(bonds):
        k = k0 if ordered else spring_constant(bond_lengths[idx], d0, k0)
        row += [i, j]; col += [j, i]; data += [-k, -k]
        diag[i] += k; diag[j] += k
    for i in range(N):
        row.append(i); col.append(i); data.append(diag[i])
    return sparse.csr_matrix((data, (row, col)), shape=(N, N))

def participation_ratio(evecs, N):
    p = np.abs(evecs)**2
    p = p / np.maximum(p.sum(axis=0, keepdims=True), 1e-30)
    return 1.0 / (N * np.sum(p**2, axis=0))

def localization_length(evecs, positions, N):
    p = np.abs(evecs)**2
    p = p / np.maximum(p.sum(axis=0, keepdims=True), 1e-30)
    xi = np.zeros(evecs.shape[1])
    for m in range(evecs.shape[1]):
        rcm = (p[:, m:m+1] * positions).sum(axis=0)
        dr = positions - rcm
        xi[m] = np.sqrt((p[:, m] * (dr**2).sum(axis=1)).sum())
    return xi

def thermal_conductivity_proxy(freq, evecs, N, T_vals):
    ipr = participation_ratio(evecs, N)
    kappa = []
    for T in T_vals:
        k = 0.0
        for n in range(len(freq)):
            if freq[n] < 1e-10: continue
            x = freq[n] / T
            if x < 500:
                ex = np.exp(x)
                C = x**2 * ex / (ex - 1)**2
            else:
                C = 0.0
            k += C * ipr[n] * freq[n]**2
        kappa.append(k)
    return np.array(kappa)


# ═══════════════════════════════════════════════════════════════════════════
# STAGE 1: BdG on corrected lattice
# ═══════════════════════════════════════════════════════════════════════════

def run_stage1(lattice, output_dir, t0=1.0, mu=1.0, delta=0.5, n_eig=20):
    os.makedirs(output_dir, exist_ok=True)
    pos = lattice['positions']; bonds = lattice['bonds']
    bl = lattice['bond_lengths']; d0 = lattice['d0']
    N = lattice['N']; bnd = lattice['boundary_mask']

    print(f"\n{'═'*60}")
    print(f"  STAGE 1 v2: BdG on Honeycomb + SW Lattice")
    print(f"{'═'*60}")
    print(f"  {N} atoms, {len(bonds)} bonds, {lattice['n_defects']} SW defects")
    print(f"  δt/t₀ = {lattice['modulation']['delta_t']*100:.1f}%")

    H = build_bdg(pos, bonds, bl, d0, t0, mu, delta)
    print(f"  BdG matrix: {H.shape[0]}×{H.shape[1]}, nnz={H.nnz}")

    k = min(n_eig, 2*N - 2)
    print(f"  Solving for {k} eigenvalues near E=0...")
    evals, evecs = eigsh(H, k=k, sigma=0.0, which='LM')
    idx = np.argsort(np.abs(evals))
    evals = evals[idx]; evecs = evecs[:, idx]

    print(f"  Nearest eigenvalues to E=0:")
    for i in range(min(8, len(evals))):
        print(f"    E_{i} = {evals[i]:+.6e}")

    # Zero mode analysis
    thresh = 1e-6
    n_zero = int(np.sum(np.abs(evals) < thresh))
    edge_weights = []
    profiles = []
    if n_zero > 0:
        for zi in range(n_zero):
            psi = evecs[:, zi]
            prob = np.abs(psi[:N])**2 + np.abs(psi[N:])**2
            prob /= prob.sum()
            ew = prob[bnd].sum()
            edge_weights.append(float(ew))
            profiles.append(prob)

    # Also check with looser threshold
    n_near = int(np.sum(np.abs(evals) < 1e-3))
    print(f"  Modes with |E| < 10⁻⁶: {n_zero}")
    print(f"  Modes with |E| < 10⁻³: {n_near}")

    # Bott index
    occ = evals < 0
    bott = np.nan
    if occ.sum() > 0:
        try:
            bott = compute_bott_index(pos, evecs[:, occ], N)
            print(f"  Bott index B = {bott:.4f}")
        except Exception as e:
            print(f"  Bott index failed: {e}")

    # μ sweep
    print(f"\n  Chemical potential sweep...")
    mu_vals = np.linspace(0.0, 2.5, 26)
    sweep = []
    for mi, mu_v in enumerate(mu_vals):
        Hm = build_bdg(pos, bonds, bl, d0, t0, mu_v, delta)
        try:
            ev = eigsh(Hm, k=min(8, 2*N-2), sigma=0.0, which='LM',
                       return_eigenvectors=False)
            mE = np.min(np.abs(ev))
            nz = int(np.sum(np.abs(ev) < 1e-6))
        except:
            mE = np.nan; nz = 0
        sweep.append({'mu': float(mu_v), 'min_E': float(mE), 'n_zero': nz})
        if mi % 5 == 0:
            tag = "✓ TOPO" if nz >= 2 else ""
            print(f"    μ={mu_v:.2f}: min|E|={mE:.2e}, zero modes={nz} {tag}")

    # Plots
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.semilogy([s['mu'] for s in sweep], [s['min_E'] for s in sweep], 'b.-')
    ax.axhline(1e-6, color='r', ls='--', alpha=0.5, label='Zero-mode threshold')
    ax.set_xlabel('μ / t₀'); ax.set_ylabel('min |E|')
    ax.set_title('Phase Diagram — μ sweep (Honeycomb + SW)')
    ax.legend(); ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'phase_diagram_mu.png'), dpi=200)
    plt.close()

    fig, ax = plt.subplots(figsize=(10, 5))
    se = np.sort(evals)
    ax.plot(range(len(se)), se, 'b.-', ms=4)
    ax.axhline(0, color='r', ls='--', alpha=0.5)
    ax.set_xlabel('Index'); ax.set_ylabel('E')
    ax.set_title(f'BdG Spectrum — {n_zero} modes |E|<10⁻⁶, {n_near} modes |E|<10⁻³')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bdg_spectrum.png'), dpi=200)
    plt.close()

    if profiles:
        fig, ax = plt.subplots(figsize=(10, 10))
        for i,j in bonds:
            ax.plot([pos[i,0],pos[j,0]], [pos[i,1],pos[j,1]], 'k-', alpha=0.06, lw=0.2)
        sc = ax.scatter(pos[:,0], pos[:,1], c=np.log10(profiles[0]+1e-20),
                       cmap='inferno', s=8, edgecolors='none')
        plt.colorbar(sc, label='log₁₀|ψ|²', shrink=0.7)
        ax.scatter(pos[bnd,0], pos[bnd,1], fc='none', ec='cyan', s=15, lw=0.3, alpha=0.3)
        ax.set_aspect('equal')
        ax.set_title(f'MZM #0 — |E|={abs(evals[0]):.2e}, edge weight={edge_weights[0]:.1%}')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'mzm_wavefunction_0.png'), dpi=200)
        plt.close()

    gate = {
        'zero_modes_pass': n_zero >= 2,
        'edge_loc_pass': any(w > 0.9 for w in edge_weights) if edge_weights else False,
        'bott_pass': abs(round(bott) - 1) < 0.1 if not np.isnan(bott) else False,
        'near_zero_modes': n_near,
    }

    summary = {
        'N': N, 'n_bonds': len(bonds), 'n_defects': lattice['n_defects'],
        'modulation_delta_t': lattice['modulation']['delta_t'],
        'n_zero_modes': n_zero, 'n_near_zero_1e3': n_near,
        'zero_energies': [float(evals[i]) for i in range(min(n_zero, 8))],
        'edge_weights': edge_weights,
        'bott_index': float(bott) if not np.isnan(bott) else None,
        'eigenvalues_near_zero': [float(evals[i]) for i in range(min(8, len(evals)))],
        'gate': gate,
    }

    zp = gate['zero_modes_pass']; ep = gate['edge_loc_pass']; bp = gate['bott_pass']
    overall = zp and ep

    print(f"\n  ┌──────────────────────────────────────────┐")
    print(f"  │        STAGE 1 v2 GATE ASSESSMENT         │")
    print(f"  ├──────────────────────────────────────────┤")
    print(f"  │  Zero modes ≥ 2:    {'✓ PASS' if zp else '✗ FAIL':>10}           │")
    print(f"  │  Edge loc > 90%:    {'✓ PASS' if ep else '✗ FAIL':>10}           │")
    print(f"  │  Bott index B=1:    {'✓ PASS' if bp else '? DEFER':>10}           │")
    print(f"  │  Near-zero (<1e-3): {n_near:>10}           │")
    print(f"  ├──────────────────────────────────────────┤")
    print(f"  │  OVERALL:  {'✓ GATE PASSED' if overall else '✗ GATE FAILED':>14}            │")
    print(f"  └──────────────────────────────────────────┘")

    with open(os.path.join(output_dir, 'stage1_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2, cls=NpEncoder)
    return summary


# ═══════════════════════════════════════════════════════════════════════════
# STAGE 2: Phonon transport on corrected lattice
# ═══════════════════════════════════════════════════════════════════════════

def run_stage2(lattice, output_dir, k0=1.0):
    os.makedirs(output_dir, exist_ok=True)
    pos = lattice['positions']; bonds = lattice['bonds']
    bl = lattice['bond_lengths']; d0 = lattice['d0']
    N = lattice['N']

    print(f"\n{'═'*60}")
    print(f"  STAGE 2 v2: Phonon Transport on Honeycomb + SW Lattice")
    print(f"{'═'*60}")
    print(f"  δk/k₀ = {lattice['modulation']['delta_k']*100:.1f}%")

    D_qp = build_dynamical_matrix(pos, bonds, bl, d0, k0, ordered=False)
    D_ord = build_dynamical_matrix(pos, bonds, bl, d0, k0, ordered=True)

    print(f"  Diagonalizing ({N}×{N})...")
    ev_qp, evec_qp = eigh(D_qp.toarray())
    ev_ord, evec_ord = eigh(D_ord.toarray())
    ev_qp = np.maximum(ev_qp, 0); ev_ord = np.maximum(ev_ord, 0)
    f_qp = np.sqrt(ev_qp); f_ord = np.sqrt(ev_ord)

    nz_qp = f_qp > 1e-6; nz_ord = f_ord > 1e-6

    ipr_qp = participation_ratio(evec_qp, N)
    ipr_ord = participation_ratio(evec_ord, N)
    print(f"  Mean IPR — QP: {ipr_qp[nz_qp].mean():.4f}, Ord: {ipr_ord[nz_ord].mean():.4f}")

    L = np.sqrt(pos[:,0].max()-pos[:,0].min()**2 + pos[:,1].max()-pos[:,1].min()**2)
    xi_qp = localization_length(evec_qp, pos, N)
    xi_ord = localization_length(evec_ord, pos, N)
    print(f"  Min ξ/L — QP: {xi_qp[nz_qp].min()/L:.4f}, Ord: {xi_ord[nz_ord].min()/L:.4f}")

    n_loc_qp = int((xi_qp[nz_qp]/L < 0.05).sum())
    n_loc_ord = int((xi_ord[nz_ord]/L < 0.05).sum())
    print(f"  Strongly localized (ξ/L<0.05) — QP: {n_loc_qp}, Ord: {n_loc_ord}")

    T_vals = np.logspace(-1, 1, 30)
    kap_qp = thermal_conductivity_proxy(f_qp, evec_qp, N, T_vals)
    kap_ord = thermal_conductivity_proxy(f_ord, evec_ord, N, T_vals)
    ratio = kap_qp / np.maximum(kap_ord, 1e-20)
    mid = (T_vals > 0.3) & (T_vals < 5.0)
    mean_ratio = float(ratio[mid].mean()) if mid.any() else float(ratio.mean())

    for Ts in [0.5, 1.0, 5.0]:
        idx = np.argmin(np.abs(T_vals - Ts))
        print(f"    T={Ts:.1f}: κ_QP/κ_ord = {ratio[idx]:.4f}")
    print(f"  Mean ratio (0.3<T<5): {mean_ratio:.4f}")

    # Spectral gaps
    fs_qp = np.sort(f_qp[nz_qp]); fs_ord = np.sort(f_ord[nz_ord])
    max_gap_qp = np.max(np.diff(fs_qp)) if len(fs_qp) > 1 else 0
    max_gap_ord = np.max(np.diff(fs_ord)) if len(fs_ord) > 1 else 1e-10
    gap_ratio = max_gap_qp / max(max_gap_ord, 1e-10)
    print(f"  Spectral gap ratio: {gap_ratio:.2f}×")

    # ── Plots ──
    fig, ax = plt.subplots(figsize=(10, 6))
    bins = np.linspace(0, max(f_qp.max(), f_ord.max())*1.05, 100)
    ax.hist(f_qp, bins=bins, alpha=0.6, density=True, label='Quasiperiodic', color='red')
    ax.hist(f_ord, bins=bins, alpha=0.6, density=True, label='Ordered', color='blue')
    ax.set_xlabel('ω'); ax.set_ylabel('g(ω)'); ax.legend(); ax.grid(True, alpha=0.3)
    ax.set_title('Phonon DOS')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'phonon_dos.png'), dpi=200); plt.close()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(f_ord, ipr_ord, s=4, alpha=0.3, c='blue', label='Ordered')
    ax.scatter(f_qp, ipr_qp, s=4, alpha=0.3, c='red', label='Quasiperiodic')
    ax.set_xlabel('ω'); ax.set_ylabel('IPR'); ax.legend(); ax.grid(True, alpha=0.3)
    ax.set_title('Participation Ratios'); ax.set_ylim(0, 1.2)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'participation_ratios.png'), dpi=200); plt.close()

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(f_ord, xi_ord/L, s=4, alpha=0.3, c='blue', label='Ordered')
    ax.scatter(f_qp, xi_qp/L, s=4, alpha=0.3, c='red', label='Quasiperiodic')
    ax.axhline(0.05, color='green', ls=':', alpha=0.5, label='Pass threshold')
    ax.set_xlabel('ω'); ax.set_ylabel('ξ/L'); ax.legend(); ax.grid(True, alpha=0.3)
    ax.set_title('Localization Lengths'); ax.set_ylim(0, 0.5)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'localization_lengths.png'), dpi=200); plt.close()

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(14, 6))
    a1.loglog(T_vals, kap_qp, 'r-', lw=2, label='QP')
    a1.loglog(T_vals, kap_ord, 'b-', lw=2, label='Ordered')
    a1.set_xlabel('T'); a1.set_ylabel('κ'); a1.legend(); a1.grid(True, alpha=0.3)
    a1.set_title('Thermal Conductivity')
    a2.semilogx(T_vals, ratio, 'k-', lw=2)
    a2.axhline(0.5, color='green', ls='--', alpha=0.5, label='Pass')
    a2.axhline(0.8, color='red', ls='--', alpha=0.5, label='Fail')
    a2.axhline(0.85, color='orange', ls=':', alpha=0.5, label='1D thesis')
    a2.set_xlabel('T'); a2.set_ylabel('κ_QP/κ_ord'); a2.legend()
    a2.set_title('Conductivity Ratio'); a2.set_ylim(0, 1.3); a2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'thermal_conductivity.png'), dpi=200); plt.close()

    # Modulation comparison
    dt = lattice['modulation']['delta_t']; dk = lattice['modulation']['delta_k']
    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(['Electron\n(t ∝ d⁻²)', 'Phonon\n(k ∝ d⁻⁴)'],
                  [dt*100, dk*100], color=['#2E75B6', '#C0392B'], width=0.5, ec='black')
    for b, v in zip(bars, [dt*100, dk*100]):
        ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.3, f'{v:.1f}%',
                ha='center', fontweight='bold')
    ax.set_ylabel('Modulation %')
    ax.set_title(f'PGTC: Phonon mod = {dk/max(dt,1e-10):.1f}× electron mod')
    ax.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'modulation_comparison.png'), dpi=200); plt.close()

    gate = {
        'kappa_pass': mean_ratio < 0.5,
        'kappa_partial': mean_ratio < 0.8,
        'localization_pass': float(xi_qp[nz_qp].min()/L) < 0.05,
        'gap_structure': gap_ratio > 2.0,
    }

    summary = {
        'N': N, 'n_defects': lattice['n_defects'],
        'modulation': lattice['modulation'],
        'mean_ipr_ratio': float(ipr_qp[nz_qp].mean() / max(ipr_ord[nz_ord].mean(), 1e-10)),
        'min_xi_L_qp': float(xi_qp[nz_qp].min()/L),
        'n_localized_qp': n_loc_qp, 'n_localized_ord': n_loc_ord,
        'kappa_ratio_mean': mean_ratio,
        'gap_ratio': float(gap_ratio),
        'gate': gate,
    }

    kp = gate['kappa_pass']; kpart = gate['kappa_partial']; lp = gate['localization_pass']
    print(f"\n  ┌──────────────────────────────────────────┐")
    print(f"  │        STAGE 2 v2 GATE ASSESSMENT         │")
    print(f"  ├──────────────────────────────────────────┤")
    print(f"  │  κ_QP/κ_ord < 0.5:  {'✓ PASS' if kp else '✗ FAIL':>10}           │")
    print(f"  │  κ_QP/κ_ord < 0.8:  {'✓ PASS' if kpart else '✗ FAIL':>10}           │")
    print(f"  │  min ξ/L < 0.05:    {'✓ PASS' if lp else '✗ FAIL':>10}           │")
    print(f"  ├──────────────────────────────────────────┤")
    if kp:
        tag = "✓ PASSED (strong)"
    elif kpart:
        tag = "~ PARTIAL"
    else:
        tag = "✗ FAILED"
    print(f"  │  OVERALL:     {tag:>20}      │")
    print(f"  └──────────────────────────────────────────┘")

    with open(os.path.join(output_dir, 'stage2_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2, cls=NpEncoder)
    return summary


# ═══════════════════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════════════════

def main():
    print("╔" + "═"*58 + "╗")
    print("║  FWS SIMULATION v2 — CORRECTED LATTICE GENERATOR         ║")
    print("║  Honeycomb + Penrose-Selected Stone-Wales Defects         ║")
    print("╚" + "═"*58 + "╝")

    t0 = time.time()

    # Generate the corrected lattice
    lattice = generate_lattice(
        Nx=20, Ny=20,
        n_penrose=4,
        defect_frac=0.05,
        min_sep=3.5,
        do_relax=True,
    )

    os.makedirs("stage1_results", exist_ok=True)
    os.makedirs("stage2_results", exist_ok=True)
    plot_lattice(lattice, "stage1_results/penrose_tiling_coordination.png")

    # Stage 1: BdG
    s1 = run_stage1(lattice, "stage1_results", t0=1.0, mu=1.0, delta=0.5, n_eig=20)

    # Stage 2: Phonons
    s2 = run_stage2(lattice, "stage2_results", k0=1.0)

    elapsed = time.time() - t0

    print(f"\n{'═'*60}")
    print(f"  COMBINED REPORT v2 — {elapsed:.1f}s")
    print(f"{'═'*60}")
    print(f"  Lattice: {lattice['N']} atoms, {lattice['n_defects']} SW defects")
    print(f"  δt/t₀ = {lattice['modulation']['delta_t']*100:.1f}% "
          f"(thesis: 9.7%)")
    print(f"  δk/k₀ = {lattice['modulation']['delta_k']*100:.1f}% "
          f"(thesis: 19.3%)")
    print(f"\n  Stage 1: {s1['n_zero_modes']} zero modes, "
          f"Bott={s1.get('bott_index','N/A')}")
    print(f"           Near-zero (<1e-3): {s1['n_near_zero_1e3']}")
    print(f"           {'✓ PASS' if s1['gate']['zero_modes_pass'] else '✗ FAIL'}")
    print(f"\n  Stage 2: κ ratio = {s2['kappa_ratio_mean']:.4f}")
    g2 = s2['gate']
    if g2['kappa_pass']:
        print(f"           ✓ PASS (strong suppression)")
    elif g2['kappa_partial']:
        print(f"           ~ PARTIAL (modest)")
    else:
        print(f"           ✗ FAIL")

    combined = {'stage1': s1, 'stage2': s2, 'lattice_info': {
        'N': lattice['N'], 'n_defects': lattice['n_defects'],
        'modulation': lattice['modulation']}, 'elapsed': elapsed}
    with open('combined_report.json', 'w') as f:
        json.dump(combined, f, indent=2, cls=NpEncoder)

    print(f"\n  Reports: combined_report.json, stage[12]_results/")


if __name__ == "__main__":
    main()
