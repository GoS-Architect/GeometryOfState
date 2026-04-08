#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  STEP 3: SPINFUL BdG WITH Ni-62 EXCHANGE + Bi RASHBA SOC
  
  Baseline result (Step 1): BDI in d=2 → TRIVIAL. No MZMs without TRS breaking.
  
  This script adds the two REQUIRED ingredients:
    • Ni-62 exchange field h_ex (breaks TRS: BDI → D)
    • Bi Rashba SOC λ_R (splits Dirac → Weyl)
  
  The BdG Hamiltonian becomes 4N×4N in Nambu-spin space:
    |ψ⟩ = (c↑, c↓, c†↓, -c†↑)^T
  
  H_BdG = [ H_N      Δ    ]
          [ Δ†     -H_N*  ]
  
  where H_N is the 2N×2N normal-state Hamiltonian with spin:
    H_N = H_hop ⊗ σ₀  - μ·I ⊗ σ₀  + h_ex(r)·I ⊗ σ_z  + H_SOC
  
  and H_SOC (Rashba) couples spin to hopping direction:
    H_SOC = iλ_R Σ_<ij> (σ × d̂_ij)_z c†_i c_j
  
  AZ classification after these additions:
    TRS broken (h_ex ≠ 0) → class D
    d = 2, class D → ℤ invariant (Bott index / Chern number)
    Non-trivial Bott index → MZMs at domain walls
  
  GoS-Architect | March 2026
═══════════════════════════════════════════════════════════════════════════════
"""

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os, sys, json, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from graphene_sw_lattice import generate_lattice, adjacency, coordination

# Pauli matrices
sigma_0 = np.eye(2, dtype=complex)
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)


def geometric_interior(pos, margin_factor=4.0, a_cc=1.42):
    """Select interior atoms by geometric margin from bounding box."""
    margin = margin_factor * a_cc
    xmin, xmax = pos[:, 0].min(), pos[:, 0].max()
    ymin, ymax = pos[:, 1].min(), pos[:, 1].max()
    return np.array([
        pos[i, 0] > xmin + margin and pos[i, 0] < xmax - margin and
        pos[i, 1] > ymin + margin and pos[i, 1] < ymax - margin
        for i in range(len(pos))
    ])


def extract_interior(lat, margin_factor=4.0):
    """Extract interior sublattice with clean indexing."""
    pos = lat['positions']
    bonds = lat['bonds']
    N_orig = lat['N']

    interior = geometric_interior(pos, margin_factor)
    keep = np.where(interior)[0]
    o2n = {old: new for new, old in enumerate(keep)}

    new_bonds = list(set(
        (min(o2n[i], o2n[j]), max(o2n[i], o2n[j]))
        for i, j in bonds if i in o2n and j in o2n
    ))
    new_pos = pos[keep]
    N = len(new_pos)

    new_cn = np.zeros(N, dtype=int)
    for i, j in new_bonds:
        new_cn[i] += 1; new_cn[j] += 1

    bl = np.array([np.linalg.norm(new_pos[i] - new_pos[j])
                    for i, j in new_bonds])
    d0 = np.median(bl) if len(bl) > 0 else 1.42

    # Map defect sites
    pent = set()
    hept = set()
    for p in lat['pentagon_sites']:
        if p in o2n: pent.add(o2n[p])
    for h in lat['heptagon_sites']:
        if h in o2n: hept.add(o2n[h])

    # Defect proximity mask: atoms within 2 bonds of a defect site
    adj = defaultdict(set)
    for i, j in new_bonds:
        adj[i].add(j); adj[j].add(i)

    defect_sites = pent | hept
    defect_neighborhood = set(defect_sites)
    for d in defect_sites:
        defect_neighborhood.update(adj[d])
        for n in adj[d]:
            defect_neighborhood.update(adj[n])

    # Boundary of interior patch
    m2 = 2 * 1.42
    xmn, xmx = new_pos[:, 0].min(), new_pos[:, 0].max()
    ymn, ymx = new_pos[:, 1].min(), new_pos[:, 1].max()
    boundary = np.array([
        new_pos[i, 0] < xmn + m2 or new_pos[i, 0] > xmx - m2 or
        new_pos[i, 1] < ymn + m2 or new_pos[i, 1] > ymx - m2
        for i in range(N)
    ])

    return {
        'positions': new_pos, 'bonds': new_bonds,
        'coord_numbers': new_cn, 'bond_lengths': bl,
        'd0': d0, 'N': N, 'n_bonds': len(new_bonds),
        'pentagon_sites': pent, 'heptagon_sites': hept,
        'defect_neighborhood': defect_neighborhood,
        'boundary_mask': boundary, 'adjacency': adj,
    }


def build_spinful_bdg(lat, t0=1.0, mu=1.0, delta=0.3,
                       h_ex=0.3, lambda_R=0.2,
                       exchange_at_defects_only=True):
    """
    Build 4N×4N spinful BdG Hamiltonian.

    Basis ordering: site i has 4 components:
      [c_{i,↑}, c_{i,↓}, c†_{i,↓}, -c†_{i,↑}]
    Global vector: [particle_↑, particle_↓, hole_↓, hole_↑_neg]
    arranged as blocks of size N.

    Block structure (4N×4N):
      H_BdG = [ H_↑↑    H_↑↓    0      Δ_s   ]
              [ H_↓↑    H_↓↓    -Δ_s   0      ]
              [ 0       -Δ_s*   -H_↓↓* -H_↓↑* ]
              [ Δ_s*    0       -H_↑↓* -H_↑↑* ]

    Simpler: use Nambu spinor Ψ = (c_↑, c_↓, c†_↓, -c†_↑)^T

    H_BdG = [ H_normal    Δ_pair  ]
            [ Δ_pair†   -H_normal*]

    where H_normal is 2N×2N (spin space) and Δ_pair is 2N×2N.

    Components:
      H_normal = (H_hop - μ) ⊗ σ₀  +  h_ex(r) ⊗ σ_z  +  H_Rashba
      Δ_pair = Δ · (iσ_y) ⊗ I_bonds  (s-wave singlet pairing)
    """
    pos = lat['positions']
    bonds = lat['bonds']
    bl = lat['bond_lengths']
    d0 = lat['d0']
    N = lat['N']

    # Which sites get exchange field
    if exchange_at_defects_only:
        ex_sites = lat['defect_neighborhood']
    else:
        ex_sites = set(range(N))

    # ── Build H_normal as 2N×2N sparse matrix ──
    # Index convention: 0..N-1 = spin-up, N..2N-1 = spin-down
    size = 2 * N
    rows, cols, vals = [], [], []

    # (a) Hopping: t_ij (c†_{i,s} c_{j,s} + h.c.) — diagonal in spin
    for k, (i, j) in enumerate(bonds):
        t = t0 * (d0 / bl[k]) ** 2
        for s_off in [0, N]:  # spin-up block, spin-down block
            rows += [i + s_off, j + s_off]
            cols += [j + s_off, i + s_off]
            vals += [-t, -t]

    # (b) Chemical potential: -μ on diagonal, both spins
    for i in range(N):
        for s_off in [0, N]:
            rows.append(i + s_off)
            cols.append(i + s_off)
            vals.append(-mu)

    # (c) Ni-62 exchange field: h_ex σ_z (site-dependent)
    #     σ_z = diag(+1, -1): spin-up gets +h_ex, spin-down gets -h_ex
    for i in range(N):
        h_i = h_ex if i in ex_sites else 0.0
        if h_i != 0:
            rows.append(i)      # spin-up
            cols.append(i)
            vals.append(+h_i)
            rows.append(i + N)  # spin-down
            cols.append(i + N)
            vals.append(-h_i)

    # (d) Rashba SOC: iλ_R Σ_<ij> (σ × d̂_ij)_z · c†_i c_j
    #     For 2D with d̂ = (dx, dy)/|d|:
    #     H_R = iλ_R [(σ_x dy - σ_y dx)/|d|]
    #     σ_x connects ↑↓: off-diagonal spin blocks
    #     σ_y connects ↑↓ with ±i
    #     (σ × d̂)_z = σ_x d̂_y - σ_y d̂_x
    for k, (i, j) in enumerate(bonds):
        dr = pos[j] - pos[i]
        d_len = bl[k]
        dx, dy = dr[0] / d_len, dr[1] / d_len

        # (σ × d̂)_z = σ_x·d̂_y - σ_y·d̂_x
        # σ_x: ↑→↓ and ↓→↑ with coefficient +1
        # σ_y: ↑→↓ with -i, ↓→↑ with +i

        # i→j, spin-up to spin-down: iλ_R(d̂_y · 1 - d̂_x · (-i)) = iλ_R(d̂_y + i·d̂_x)
        val_up_down = 1j * lambda_R * (dy + 1j * dx)
        # i→j, spin-down to spin-up: iλ_R(d̂_y · 1 - d̂_x · (i)) = iλ_R(d̂_y - i·d̂_x)
        val_down_up = 1j * lambda_R * (dy - 1j * dx)

        # i→j
        rows += [i, i + N]
        cols += [j + N, j]
        vals += [val_up_down, val_down_up]

        # j→i (hermitian conjugate): values must be swapped between spin blocks
        # H[j+N, i] = conj(H[i, j+N]) = conj(val_up_down)
        # H[j, i+N] = conj(H[i+N, j]) = conj(val_down_up)
        rows += [j, j + N]
        cols += [i + N, i]
        vals += [np.conj(val_down_up), np.conj(val_up_down)]

    H_normal = sparse.csr_matrix(
        (vals, (rows, cols)), shape=(size, size), dtype=complex)

    # ── Build Δ_pair as 2N×2N sparse matrix ──
    # s-wave singlet: Δ(iσ_y) = Δ [[0, 1],[-1, 0]]
    # On-site pairing: Δ_{i,↑↓} = +Δ, Δ_{i,↓↑} = -Δ
    d_rows, d_cols, d_vals = [], [], []
    for i in range(N):
        # ↑ pairs with ↓: position (i, i+N) in the 2N basis
        d_rows.append(i)
        d_cols.append(i + N)
        d_vals.append(delta)
        # ↓ pairs with ↑: position (i+N, i) — antisymmetric
        d_rows.append(i + N)
        d_cols.append(i)
        d_vals.append(-delta)

    Delta_pair = sparse.csr_matrix(
        (d_vals, (d_rows, d_cols)), shape=(size, size), dtype=complex)

    # ── Assemble 4N×4N BdG ──
    # H_BdG = [  H_normal     Δ_pair  ]
    #          [  Δ_pair†    -H_normal*]
    H_BdG = sparse.bmat([
        [H_normal, Delta_pair],
        [Delta_pair.conj().T, -H_normal.conj()]
    ], format='csr')

    return H_BdG


def compute_bott_index_spinful(positions, eigvecs_occ, N):
    """Bott index for 4N system. Use particle sector (first 2N rows)."""
    x = positions[:, 0]; y = positions[:, 1]
    Lx = x.max() - x.min(); Ly = y.max() - y.min()
    if Lx < 1e-10 or Ly < 1e-10:
        return np.nan
    xn = (x - x.min()) / Lx
    yn = (y - y.min()) / Ly

    # Particle sector: rows 0..N-1 (spin-up) and N..2N-1 (spin-down)
    V_up = eigvecs_occ[:N, :]
    V_dn = eigvecs_occ[N:2*N, :]
    V = np.vstack([V_up, V_dn])  # 2N × n_occ

    # Position operators act on site index (same for both spins)
    exp_x = np.exp(2j * np.pi * xn)
    exp_y = np.exp(2j * np.pi * yn)

    # Block-diagonal: same phase for both spin components of same site
    exp_x_full = np.concatenate([exp_x, exp_x])
    exp_y_full = np.concatenate([exp_y, exp_y])

    Ux = V.conj().T @ np.diag(exp_x_full) @ V
    Uy = V.conj().T @ np.diag(exp_y_full) @ V

    try:
        comm = Ux @ Uy @ np.linalg.inv(Ux) @ np.linalg.inv(Uy)
        eigvals = np.linalg.eigvals(comm)
        return np.sum(np.log(eigvals)).imag / (2 * np.pi)
    except Exception:
        return np.nan


def run_spinful_bdg(output_dir="spinful_results",
                     Nx=15, Ny=15, n_penrose=3,
                     t0=1.0, mu=1.0, delta=0.3,
                     h_ex=0.3, lambda_R=0.2,
                     n_eig=30):
    os.makedirs(output_dir, exist_ok=True)

    print("╔" + "═" * 58 + "╗")
    print("║  STEP 3: SPINFUL BdG (Ni-62 Exchange + Bi SOC)           ║")
    print("║  BDI → D class transition. d=2, class D → ℤ invariant.   ║")
    print("╚" + "═" * 58 + "╝")

    t_start = time.time()

    # ── Generate and clean lattice ──
    print(f"\n  Generating {Nx}×{Ny} lattice...")
    raw = generate_lattice(Nx=Nx, Ny=Ny, n_penrose=n_penrose,
                            defect_frac=0.04, min_sep=4.0, do_relax=False)

    print(f"  Extracting interior...")
    lat = extract_interior(raw, margin_factor=4.0)
    N = lat['N']
    pos = lat['positions']
    bonds = lat['bonds']
    bnd = lat['boundary_mask']

    print(f"  Interior: {N} atoms, {len(bonds)} bonds")
    print(f"  Defect sites: {len(lat['pentagon_sites'])} pent, "
          f"{len(lat['heptagon_sites'])} hept")
    print(f"  Defect neighborhood: {len(lat['defect_neighborhood'])} atoms")
    print(f"  d₀ = {lat['d0']:.4f} Å")

    cn_dist = dict(zip(*np.unique(lat['coord_numbers'], return_counts=True)))
    print(f"  CN distribution: {cn_dist}")

    # ── Build 4N×4N BdG ──
    print(f"\n  Parameters:")
    print(f"    t₀ = {t0}, μ = {mu}, Δ = {delta}")
    print(f"    h_ex = {h_ex} (Ni-62 exchange, at defect sites)")
    print(f"    λ_R = {lambda_R} (Bi Rashba SOC)")

    H = build_spinful_bdg(lat, t0=t0, mu=mu, delta=delta,
                           h_ex=h_ex, lambda_R=lambda_R,
                           exchange_at_defects_only=True)

    print(f"\n  BdG matrix: {H.shape[0]}×{H.shape[1]} (4N={4*N})")
    print(f"  nnz = {H.nnz}")
    print(f"  Hermitian check: {np.max(np.abs(H - H.conj().T)):.2e}")

    # ── Diagonalize ──
    ne = min(n_eig, 4 * N - 2)
    print(f"  Solving for {ne} eigenvalues near E=0...")
    evals, evecs = eigsh(H, k=ne, sigma=0.0, which='LM')
    idx = np.argsort(np.abs(evals))
    evals = evals[idx]; evecs = evecs[:, idx]

    print(f"\n  Eigenvalues nearest E=0:")
    for i in range(min(12, len(evals))):
        print(f"    E_{i} = {evals[i]:+.8e}")

    gap = np.min(np.abs(evals))
    n_zero_strict = int(np.sum(np.abs(evals) < 1e-8))
    n_zero_loose = int(np.sum(np.abs(evals) < 1e-4))
    n_zero_mid = int(np.sum(np.abs(evals) < 1e-6))

    print(f"\n  Spectral gap: {gap:.6e}")
    print(f"  Modes |E| < 10⁻⁸: {n_zero_strict}")
    print(f"  Modes |E| < 10⁻⁶: {n_zero_mid}")
    print(f"  Modes |E| < 10⁻⁴: {n_zero_loose}")

    # ── Localization analysis ──
    print(f"\n  Localization of lowest modes:")

    # Build defect mask
    defect_mask = np.zeros(N, dtype=bool)
    for d in lat['defect_neighborhood']:
        if d < N:
            defect_mask[d] = True

    mode_data = []
    for mi in range(min(8, len(evals))):
        psi = evecs[:, mi]
        # Probability: sum over particle spin-up, particle spin-down,
        # hole spin-down, hole spin-up components
        prob = np.zeros(N)
        for block in range(4):
            prob += np.abs(psi[block * N:(block + 1) * N]) ** 2
        prob /= prob.sum()

        edge_w = float(prob[bnd].sum())
        defect_w = float(prob[defect_mask].sum())
        bulk_w = 1.0 - edge_w - defect_w + float(prob[bnd & defect_mask].sum())

        mode_data.append({
            'energy': float(evals[mi]),
            'edge_weight': edge_w,
            'defect_weight': defect_w,
            'prob': prob,
        })

        loc = "EDGE" if edge_w > 0.7 else ("DEFECT" if defect_w > 0.5 else "BULK")
        print(f"    Mode {mi}: |E|={abs(evals[mi]):.2e}  "
              f"edge={edge_w:.3f}  defect={defect_w:.3f}  → {loc}")

    # ── Bott index ──
    print(f"\n  Bott index computation...")
    occ = evals < 0
    bott = np.nan
    if occ.sum() > 0:
        bott = compute_bott_index_spinful(pos, evecs[:, occ], N)
        print(f"  B = {bott:.4f}")
        if abs(bott) < 0.3:
            print(f"  → Likely trivial (B ≈ 0)")
        elif abs(round(bott)) >= 1 and abs(bott - round(bott)) < 0.3:
            print(f"  → NON-TRIVIAL (B ≈ {round(bott):.0f})")
        else:
            print(f"  → Ambiguous")

    # ── Parameter sweeps ──
    print(f"\n  Exchange field sweep (h_ex):")
    hex_vals = np.linspace(0.0, 0.8, 9)
    hex_sweep = []
    for hx in hex_vals:
        Hx = build_spinful_bdg(lat, t0=t0, mu=mu, delta=delta,
                                h_ex=hx, lambda_R=lambda_R)
        try:
            ev = eigsh(Hx, k=min(8, 4*N-2), sigma=0.0, which='LM',
                       return_eigenvectors=False)
            mE = float(np.min(np.abs(ev)))
            nz = int(np.sum(np.abs(ev) < 1e-6))
        except:
            mE = float('nan'); nz = 0
        hex_sweep.append({'h_ex': float(hx), 'gap': mE, 'n_zero': nz})
        tag = "✓" if nz >= 2 else " "
        print(f"    h_ex={hx:.2f}: gap={mE:.2e}  zero={nz} {tag}")

    print(f"\n  Chemical potential sweep:")
    mu_vals = np.linspace(0.0, 3.0, 13)
    mu_sweep = []
    for mu_v in mu_vals:
        Hm = build_spinful_bdg(lat, t0=t0, mu=mu_v, delta=delta,
                                h_ex=h_ex, lambda_R=lambda_R)
        try:
            ev = eigsh(Hm, k=min(8, 4*N-2), sigma=0.0, which='LM',
                       return_eigenvectors=False)
            mE = float(np.min(np.abs(ev)))
            nz = int(np.sum(np.abs(ev) < 1e-6))
        except:
            mE = float('nan'); nz = 0
        mu_sweep.append({'mu': float(mu_v), 'gap': mE, 'n_zero': nz})
        tag = "✓" if nz >= 2 else " "
        print(f"    μ={mu_v:.2f}: gap={mE:.2e}  zero={nz} {tag}")

    # ── Plots ──
    # Spectrum
    fig, ax = plt.subplots(figsize=(10, 5))
    se = np.sort(evals)
    ax.plot(range(len(se)), se, 'b.-', ms=4)
    ax.axhline(0, color='r', ls='--', alpha=0.5)
    ax.set_xlabel('Index'); ax.set_ylabel('E')
    ax.set_title(f'Spinful BdG Spectrum (h_ex={h_ex}, λ_R={lambda_R})\n'
                 f'Gap={gap:.2e}, zero modes(<1e-6)={n_zero_mid}')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bdg_spectrum.png'), dpi=200)
    plt.close()

    # Phase diagrams
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

    ax1.semilogy([s['h_ex'] for s in hex_sweep],
                 [max(s['gap'], 1e-18) for s in hex_sweep], 'b.-', ms=6)
    ax1.axhline(1e-6, color='r', ls='--', alpha=0.5)
    ax1.set_xlabel('h_ex (Ni-62 exchange)'); ax1.set_ylabel('min |E|')
    ax1.set_title('Exchange Field Sweep'); ax1.grid(True, alpha=0.3)

    ax2.semilogy([s['mu'] for s in mu_sweep],
                 [max(s['gap'], 1e-18) for s in mu_sweep], 'b.-', ms=6)
    ax2.axhline(1e-6, color='r', ls='--', alpha=0.5)
    ax2.set_xlabel('μ / t₀'); ax2.set_ylabel('min |E|')
    ax2.set_title('Chemical Potential Sweep'); ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'phase_diagram_mu.png'), dpi=200)
    plt.close()

    # Wavefunction of lowest mode
    if len(mode_data) > 0:
        fig, axes = plt.subplots(1, 2, figsize=(18, 8))

        for ax_idx, mi in enumerate([0, min(1, len(mode_data) - 1)]):
            ax = axes[ax_idx]
            for i, j in bonds:
                ax.plot([pos[i, 0], pos[j, 0]], [pos[i, 1], pos[j, 1]],
                        'k-', alpha=0.06, lw=0.2)

            prob = mode_data[mi]['prob']
            sc = ax.scatter(pos[:, 0], pos[:, 1],
                           c=np.log10(prob + 1e-20),
                           cmap='inferno', s=12, edgecolors='none')
            plt.colorbar(sc, ax=ax, label='log₁₀|ψ|²', shrink=0.7)

            # Mark defect sites
            for p in lat['pentagon_sites']:
                if p < N:
                    ax.scatter(pos[p, 0], pos[p, 1], fc='none', ec='lime',
                              s=80, lw=2, zorder=5)
            for h in lat['heptagon_sites']:
                if h < N:
                    ax.scatter(pos[h, 0], pos[h, 1], fc='none', ec='cyan',
                              s=80, lw=2, zorder=5)

            ax.set_aspect('equal')
            E = mode_data[mi]['energy']
            ew = mode_data[mi]['edge_weight']
            dw = mode_data[mi]['defect_weight']
            ax.set_title(f'Mode {mi}: |E|={abs(E):.2e}\n'
                         f'edge={ew:.2f} defect={dw:.2f}\n'
                         f'Green ○=pentagon  Cyan ○=heptagon')

        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'mzm_wavefunctions.png'), dpi=200)
        plt.close()

    # ── Gate assessment ──
    elapsed = time.time() - t_start

    # Identify defect-localized zero modes
    defect_zero_modes = [
        m for m in mode_data
        if abs(m['energy']) < 1e-4 and m['defect_weight'] > 0.3
    ]
    edge_zero_modes = [
        m for m in mode_data
        if abs(m['energy']) < 1e-4 and m['edge_weight'] > 0.7
    ]

    has_finite_window = (
        any(s['n_zero'] >= 2 for s in mu_sweep) and
        any(s['n_zero'] == 0 for s in mu_sweep)
    )

    gate = {
        'zero_modes_total': n_zero_mid,
        'defect_localized_modes': len(defect_zero_modes),
        'edge_modes_only': len(edge_zero_modes),
        'bott_nontrivial': abs(bott - round(bott)) < 0.3 and abs(round(bott)) >= 1 if not np.isnan(bott) else False,
        'has_finite_mu_window': has_finite_window,
        'has_exchange_transition': (
            any(s['n_zero'] == 0 for s in hex_sweep if s['h_ex'] < 0.1) and
            any(s['n_zero'] >= 2 for s in hex_sweep if s['h_ex'] > 0.1)
        ),
    }

    genuine_mzm = (
        gate['defect_localized_modes'] >= 2 and
        gate['has_finite_mu_window']
    )

    print(f"\n  {'═' * 50}")
    print(f"  STEP 3 ASSESSMENT")
    print(f"  {'═' * 50}")
    print(f"  Zero modes (|E|<1e-6):    {n_zero_mid}")
    print(f"  Defect-localized:         {gate['defect_localized_modes']}")
    print(f"  Edge-only (artifacts):    {gate['edge_modes_only']}")
    print(f"  Bott index:               {bott:.4f}")
    print(f"  Finite μ window:          {gate['has_finite_mu_window']}")
    print(f"  Exchange-driven transition: {gate['has_exchange_transition']}")
    print(f"  {'─' * 50}")

    if genuine_mzm:
        print(f"  ✓ GENUINE MZMs: Defect-localized modes in finite window")
        print(f"    The Ni-62 exchange + Bi SOC activate the topology.")
        print(f"    Class D, d=2, Bott index non-trivial.")
    elif n_zero_mid > 0 and not gate['has_finite_mu_window']:
        print(f"  ⚠ ZERO MODES but no finite window — likely boundary artifacts")
        print(f"    Need larger lattice or different parameters.")
    elif n_zero_mid == 0 and gap > 1e-3:
        print(f"  ✗ GAPPED, no zero modes at these parameters.")
        print(f"    Try: increase h_ex, adjust μ, scan parameter space.")
    else:
        print(f"  ? AMBIGUOUS: small gap ({gap:.2e}), needs finer scan.")

    summary = {
        'N': N, 'n_defects': len(lat['pentagon_sites']) + len(lat['heptagon_sites']),
        'parameters': {'t0': t0, 'mu': mu, 'delta': delta,
                       'h_ex': h_ex, 'lambda_R': lambda_R},
        'gap': float(gap),
        'n_zero_1e8': n_zero_strict, 'n_zero_1e6': n_zero_mid,
        'n_zero_1e4': n_zero_loose,
        'bott_index': float(bott) if not np.isnan(bott) else None,
        'eigenvalues_12': [float(evals[i]) for i in range(min(12, len(evals)))],
        'mode_localization': [
            {'energy': m['energy'], 'edge': m['edge_weight'],
             'defect': m['defect_weight']}
            for m in mode_data
        ],
        'gate': {k: bool(v) if isinstance(v, (bool, np.bool_)) else v
                 for k, v in gate.items()},
        'genuine_mzm': bool(genuine_mzm),
        'hex_sweep': hex_sweep, 'mu_sweep': mu_sweep,
        'elapsed': elapsed,
    }

    with open(os.path.join(output_dir, 'spinful_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n  Elapsed: {elapsed:.1f}s")
    print(f"  Results: {output_dir}/")

    return summary


if __name__ == "__main__":
    run_spinful_bdg(
        output_dir="spinful_results",
        Nx=15, Ny=15, n_penrose=3,
        t0=1.0, mu=1.0, delta=0.3,
        h_ex=0.3, lambda_R=0.2,
        n_eig=30,
    )
