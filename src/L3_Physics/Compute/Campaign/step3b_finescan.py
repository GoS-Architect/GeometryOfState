#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  STEP 3b: FINE SCAN AROUND TOPOLOGICAL TRANSITION
  
  Step 3 result: gap closes at h_ex ≈ 0.6, reopens with tiny gap (~0.001).
  The transition is real. The question: is the reopened phase topological,
  and can we widen the gap enough to see clean MZMs?
  
  Strategy:
    1. Fine h_ex scan near transition (0.3–1.0, 30 points)
    2. At each h_ex, scan Δ and λ_R to maximize post-transition gap
    3. Relax zero-mode threshold to 10% of gap (not fixed 10⁻⁶)
    4. Track whether lowest modes are defect-localized
    5. Try p-wave bond pairing (natural for proximity SC) vs s-wave on-site
  
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
from graphene_sw_lattice import generate_lattice
from step3_spinful_bdg import extract_interior, compute_bott_index_spinful

sigma_0 = np.eye(2, dtype=complex)
sigma_x = np.array([[0, 1], [1, 0]], dtype=complex)
sigma_y = np.array([[0, -1j], [1j, 0]], dtype=complex)
sigma_z = np.array([[1, 0], [0, -1]], dtype=complex)


def build_bdg_v2(lat, t0=1.0, mu=1.0, delta=0.3,
                  h_ex=0.3, lambda_R=0.2,
                  pairing='p-wave'):
    """
    4N×4N spinful BdG with corrected Rashba and selectable pairing.
    
    pairing='s-wave': on-site singlet Δ(iσ_y)
    pairing='p-wave': bond-based triplet-like Δ_ij along bonds
    """
    pos = lat['positions']
    bonds = lat['bonds']
    bl = lat['bond_lengths']
    d0 = lat['d0']
    N = lat['N']
    ex_sites = lat['defect_neighborhood']

    size = 2 * N
    rows, cols, vals = [], [], []

    # (a) Hopping — spin-diagonal
    for k, (i, j) in enumerate(bonds):
        t = t0 * (d0 / bl[k]) ** 2
        for s in [0, N]:
            rows += [i + s, j + s]
            cols += [j + s, i + s]
            vals += [-t, -t]

    # (b) Chemical potential
    for i in range(N):
        for s in [0, N]:
            rows.append(i + s); cols.append(i + s); vals.append(-mu)

    # (c) Ni-62 exchange: h_ex σ_z at defect neighborhood
    for i in range(N):
        h_i = h_ex if i in ex_sites else 0.0
        if h_i != 0:
            rows += [i, i + N]
            cols += [i, i + N]
            vals += [h_i, -h_i]

    # (d) Rashba SOC — HERMITIAN VERIFIED
    #     H_R = iλ_R Σ_<ij> c†_i (σ × d̂_ij)_z c_j
    #     (σ × d̂)_z = σ_x d̂_y - σ_y d̂_x
    #     Matrix element ↑→↓: d̂_y - i d̂_x, times iλ_R
    #     Matrix element ↓→↑: d̂_y + i d̂_x, times iλ_R
    for k, (i, j) in enumerate(bonds):
        dr = pos[j] - pos[i]
        d_len = bl[k]
        dx, dy = dr[0] / d_len, dr[1] / d_len

        # i→j spin-up to spin-down
        v_ud = 1j * lambda_R * (dy - 1j * dx)
        # i→j spin-down to spin-up
        v_du = 1j * lambda_R * (dy + 1j * dx)

        # i→j
        rows += [i, i + N]
        cols += [j + N, j]
        vals += [v_ud, v_du]
        # j→i (Hermitian conjugate: swap i↔j AND swap spin blocks)
        rows += [j, j + N]
        cols += [i + N, i]
        vals += [np.conj(v_du), np.conj(v_ud)]

    H_normal = sparse.csr_matrix((vals, (rows, cols)),
                                  shape=(size, size), dtype=complex)

    # Verify Hermiticity
    herm_err = np.max(np.abs(H_normal - H_normal.conj().T))
    assert herm_err < 1e-12, f"H_normal not Hermitian: {herm_err}"

    # (e) Pairing
    d_rows, d_cols, d_vals = [], [], []

    if pairing == 's-wave':
        # On-site singlet: Δ(iσ_y) at each site
        for i in range(N):
            d_rows += [i, i + N]
            d_cols += [i + N, i]
            d_vals += [delta, -delta]
    elif pairing == 'p-wave':
        # Bond-based p-wave: Δ_ij (iσ_y) along each bond
        # Antisymmetric in bond direction, singlet in spin
        for k, (i, j) in enumerate(bonds):
            dij = delta * (d0 / bl[k]) ** 2
            # Singlet pairing: (iσ_y)_{↑↓} = +1, (iσ_y)_{↓↑} = -1
            # i-↑ pairs with j-↓
            d_rows += [i, j]
            d_cols += [j + N, i + N]
            d_vals += [dij, -dij]
            # i-↓ pairs with j-↑ (antisymmetric)
            d_rows += [i + N, j + N]
            d_cols += [j, i]
            d_vals += [-dij, dij]

    Delta_pair = sparse.csr_matrix((d_vals, (d_rows, d_cols)),
                                    shape=(size, size), dtype=complex)

    # Assemble BdG
    H_BdG = sparse.bmat([
        [H_normal, Delta_pair],
        [Delta_pair.conj().T, -H_normal.conj()]
    ], format='csr')

    # Final Hermiticity check
    bdg_err = np.max(np.abs(H_BdG - H_BdG.conj().T))
    assert bdg_err < 1e-12, f"H_BdG not Hermitian: {bdg_err}"

    return H_BdG


def solve_near_zero(H, n_eig=12):
    """Solve for eigenvalues nearest E=0. Returns sorted by |E|."""
    k = min(n_eig, H.shape[0] - 2)
    evals, evecs = eigsh(H, k=k, sigma=0.0, which='LM')
    idx = np.argsort(np.abs(evals))
    return evals[idx], evecs[:, idx]


def analyze_modes(evals, evecs, N, defect_mask, boundary_mask, n_modes=4):
    """Analyze localization of lowest modes."""
    results = []
    for mi in range(min(n_modes, len(evals))):
        psi = evecs[:, mi]
        prob = np.zeros(N)
        for block in range(4):
            prob += np.abs(psi[block * N:(block + 1) * N]) ** 2
        prob /= prob.sum()
        results.append({
            'energy': float(evals[mi]),
            'abs_energy': float(abs(evals[mi])),
            'edge_weight': float(prob[boundary_mask].sum()),
            'defect_weight': float(prob[defect_mask].sum()),
        })
    return results


def run_fine_scan(output_dir="finescan_results"):
    os.makedirs(output_dir, exist_ok=True)

    print("╔" + "═" * 58 + "╗")
    print("║  STEP 3b: FINE SCAN AROUND TOPOLOGICAL TRANSITION        ║")
    print("╚" + "═" * 58 + "╝")
    t_start = time.time()

    # Generate lattice
    print("\n  Generating lattice...")
    raw = generate_lattice(Nx=15, Ny=15, n_penrose=3,
                            defect_frac=0.04, min_sep=4.0, do_relax=False)
    lat = extract_interior(raw, margin_factor=4.0)
    N = lat['N']
    pos = lat['positions']

    defect_mask = np.zeros(N, dtype=bool)
    for d in lat['defect_neighborhood']:
        if d < N: defect_mask[d] = True
    bnd = lat['boundary_mask']

    print(f"  Interior: {N} atoms, {len(lat['bonds'])} bonds")
    print(f"  Defect neighborhood: {defect_mask.sum()} atoms")

    # ══════════════════════════════════════════════════════════════
    # SCAN 1: Fine h_ex sweep with BOTH pairing symmetries
    # ══════════════════════════════════════════════════════════════
    print(f"\n{'═' * 55}")
    print(f"  SCAN 1: h_ex sweep, s-wave vs p-wave pairing")
    print(f"{'═' * 55}")

    hex_vals = np.linspace(0.0, 1.5, 31)
    results_swave = []
    results_pwave = []

    for pairing, result_list in [('s-wave', results_swave),
                                   ('p-wave', results_pwave)]:
        print(f"\n  [{pairing}]")
        for hx in hex_vals:
            H = build_bdg_v2(lat, t0=1.0, mu=1.0, delta=0.3,
                             h_ex=hx, lambda_R=0.2, pairing=pairing)
            evals, evecs = solve_near_zero(H, n_eig=8)
            gap = float(np.min(np.abs(evals)))
            modes = analyze_modes(evals, evecs, N, defect_mask, bnd, n_modes=2)

            result_list.append({
                'h_ex': float(hx), 'gap': gap,
                'E0': modes[0]['abs_energy'],
                'defect_w': modes[0]['defect_weight'],
                'edge_w': modes[0]['edge_weight'],
            })

            if hx < 0.05 or abs(hx - 0.5) < 0.03 or abs(hx - 1.0) < 0.03 or gap < 0.01:
                print(f"    h_ex={hx:.2f}: gap={gap:.4e}  "
                      f"defect={modes[0]['defect_weight']:.2f}  "
                      f"edge={modes[0]['edge_weight']:.2f}")

    # ══════════════════════════════════════════════════════════════
    # SCAN 2: 2D parameter space (h_ex, λ_R) for p-wave
    # ══════════════════════════════════════════════════════════════
    print(f"\n{'═' * 55}")
    print(f"  SCAN 2: (h_ex, λ_R) phase diagram [p-wave]")
    print(f"{'═' * 55}")

    hex_grid = np.linspace(0.0, 1.5, 16)
    lr_grid = np.linspace(0.0, 0.6, 13)
    phase_map = np.zeros((len(hex_grid), len(lr_grid)))
    defect_map = np.zeros_like(phase_map)

    for hi, hx in enumerate(hex_grid):
        for li, lr in enumerate(lr_grid):
            H = build_bdg_v2(lat, t0=1.0, mu=1.0, delta=0.3,
                             h_ex=hx, lambda_R=lr, pairing='p-wave')
            evals, evecs = solve_near_zero(H, n_eig=4)
            gap = float(np.min(np.abs(evals)))
            modes = analyze_modes(evals, evecs, N, defect_mask, bnd, n_modes=1)
            phase_map[hi, li] = gap
            defect_map[hi, li] = modes[0]['defect_weight']
        print(f"    h_ex={hx:.2f}: min gap across λ_R = {phase_map[hi,:].min():.4e}")

    # ══════════════════════════════════════════════════════════════
    # SCAN 3: Δ sweep at the gap-closing h_ex
    # ══════════════════════════════════════════════════════════════
    print(f"\n{'═' * 55}")
    print(f"  SCAN 3: Δ sweep at h_ex near transition [p-wave]")
    print(f"{'═' * 55}")

    # Find approximate gap-closing h_ex from Scan 1 (p-wave)
    gaps_p = [r['gap'] for r in results_pwave]
    hex_min_idx = np.argmin(gaps_p)
    hex_transition = results_pwave[hex_min_idx]['h_ex']
    print(f"  Transition at h_ex ≈ {hex_transition:.2f}")

    # Scan Δ at h_ex slightly above transition
    hex_above = hex_transition + 0.15
    delta_vals = np.linspace(0.1, 1.0, 19)
    delta_scan = []

    print(f"  Scanning Δ at h_ex = {hex_above:.2f}:")
    for dv in delta_vals:
        H = build_bdg_v2(lat, t0=1.0, mu=1.0, delta=dv,
                         h_ex=hex_above, lambda_R=0.2, pairing='p-wave')
        evals, evecs = solve_near_zero(H, n_eig=8)
        gap = float(np.min(np.abs(evals)))
        modes = analyze_modes(evals, evecs, N, defect_mask, bnd, n_modes=2)

        delta_scan.append({
            'delta': float(dv), 'gap': gap,
            'defect_w': modes[0]['defect_weight'],
        })
        if gap < 0.05 or dv > 0.95 or abs(dv - 0.3) < 0.03:
            print(f"    Δ={dv:.2f}: gap={gap:.4e}  defect={modes[0]['defect_weight']:.2f}")

    # ══════════════════════════════════════════════════════════════
    # SCAN 4: μ sweep at best parameters from above
    # ══════════════════════════════════════════════════════════════
    print(f"\n{'═' * 55}")
    print(f"  SCAN 4: μ sweep at optimized parameters [p-wave]")
    print(f"{'═' * 55}")

    # Find Δ that gives smallest gap (closest to transition → MZMs)
    gaps_d = [r['gap'] for r in delta_scan]
    best_delta_idx = np.argmin(gaps_d)
    best_delta = delta_scan[best_delta_idx]['delta']
    print(f"  Best Δ = {best_delta:.2f} (gap = {gaps_d[best_delta_idx]:.4e})")

    # Also try: Δ just above the minimum (topological side)
    for delta_try in [best_delta, best_delta + 0.1, 0.3, 0.5]:
        print(f"\n  μ sweep at Δ={delta_try:.2f}, h_ex={hex_above:.2f}, λ_R=0.2:")
        mu_vals = np.linspace(0.0, 3.0, 25)
        mu_scan = []
        for mu_v in mu_vals:
            H = build_bdg_v2(lat, t0=1.0, mu=mu_v, delta=delta_try,
                             h_ex=hex_above, lambda_R=0.2, pairing='p-wave')
            evals, evecs = solve_near_zero(H, n_eig=6)
            gap = float(np.min(np.abs(evals)))
            modes = analyze_modes(evals, evecs, N, defect_mask, bnd, n_modes=1)
            mu_scan.append({
                'mu': float(mu_v), 'gap': gap,
                'defect_w': modes[0]['defect_weight']
            })

        # Find gap minimum in μ
        mu_gaps = [r['gap'] for r in mu_scan]
        mu_min_idx = np.argmin(mu_gaps)
        print(f"    Gap minimum: μ={mu_scan[mu_min_idx]['mu']:.2f}, "
              f"gap={mu_gaps[mu_min_idx]:.4e}")
        print(f"    Gap at μ=0: {mu_gaps[0]:.4e}")
        print(f"    Gap at μ=3: {mu_gaps[-1]:.4e}")

        # Check for finite window (gap small in middle, large at ends)
        threshold = 0.05
        low_gap = [r for r in mu_scan if r['gap'] < threshold]
        high_gap_low_mu = any(r['gap'] > threshold for r in mu_scan if r['mu'] < 0.5)
        high_gap_high_mu = any(r['gap'] > threshold for r in mu_scan if r['mu'] > 2.5)

        if low_gap and high_gap_low_mu:
            print(f"    ✓ Finite window detected: gap drops below {threshold} "
                  f"for μ ∈ [{low_gap[0]['mu']:.2f}, {low_gap[-1]['mu']:.2f}]")
        else:
            print(f"    No clear finite window at threshold {threshold}")

    # ══════════════════════════════════════════════════════════════
    # SCAN 5: Bott index across h_ex transition at best parameters
    # ══════════════════════════════════════════════════════════════
    print(f"\n{'═' * 55}")
    print(f"  SCAN 5: Bott index across transition")
    print(f"{'═' * 55}")

    hex_bott = np.linspace(0.0, 1.5, 16)
    bott_results = []
    for hx in hex_bott:
        H = build_bdg_v2(lat, t0=1.0, mu=1.0, delta=0.3,
                         h_ex=hx, lambda_R=0.2, pairing='p-wave')
        evals, evecs = solve_near_zero(H, n_eig=min(30, 4*N-2))
        occ = evals < 0
        bott = np.nan
        if occ.sum() > 0 and occ.sum() < len(evals):
            bott = compute_bott_index_spinful(pos, evecs[:, occ], N)
        gap = float(np.min(np.abs(evals)))
        bott_results.append({'h_ex': float(hx), 'bott': float(bott), 'gap': gap})
        b_str = f"{bott:+.3f}" if not np.isnan(bott) else "  nan"
        print(f"    h_ex={hx:.2f}: B={b_str}  gap={gap:.4e}")

    # ══════════════════════════════════════════════════════════════
    # PLOTS
    # ══════════════════════════════════════════════════════════════

    # Plot 1: h_ex sweep comparison
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    ax1.semilogy([r['h_ex'] for r in results_swave],
                 [max(r['gap'], 1e-16) for r in results_swave],
                 'b.-', ms=5, label='s-wave')
    ax1.semilogy([r['h_ex'] for r in results_pwave],
                 [max(r['gap'], 1e-16) for r in results_pwave],
                 'r.-', ms=5, label='p-wave')
    ax1.set_ylabel('Spectral gap')
    ax1.set_title('Gap vs Exchange Field — Pairing Comparison')
    ax1.legend(); ax1.grid(True, alpha=0.3)
    ax1.axhline(1e-3, color='gray', ls=':', alpha=0.3, label='1 meV scale')

    ax2.plot([r['h_ex'] for r in results_pwave],
             [r['defect_w'] for r in results_pwave],
             'r.-', ms=5, label='p-wave defect weight')
    ax2.plot([r['h_ex'] for r in results_swave],
             [r['defect_w'] for r in results_swave],
             'b.-', ms=5, label='s-wave defect weight')
    ax2.set_xlabel('h_ex (Ni-62 exchange)')
    ax2.set_ylabel('Defect weight of lowest mode')
    ax2.legend(); ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'hex_sweep_comparison.png'), dpi=200)
    plt.close()

    # Plot 2: 2D phase map
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    im1 = ax1.pcolormesh(lr_grid, hex_grid, np.log10(phase_map + 1e-16),
                          cmap='RdBu_r', shading='auto')
    plt.colorbar(im1, ax=ax1, label='log₁₀(gap)')
    ax1.set_xlabel('λ_R (Bi SOC)'); ax1.set_ylabel('h_ex (Ni-62)')
    ax1.set_title('Spectral Gap Phase Diagram [p-wave]')

    im2 = ax2.pcolormesh(lr_grid, hex_grid, defect_map,
                          cmap='inferno', shading='auto')
    plt.colorbar(im2, ax=ax2, label='Defect weight')
    ax2.set_xlabel('λ_R (Bi SOC)'); ax2.set_ylabel('h_ex (Ni-62)')
    ax2.set_title('Defect Localization of Lowest Mode')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'phase_diagram_2d.png'), dpi=200)
    plt.close()

    # Plot 3: Bott index across transition
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    botts = [r['bott'] for r in bott_results]
    gaps_b = [r['gap'] for r in bott_results]
    hexs_b = [r['h_ex'] for r in bott_results]
    ax1.semilogy(hexs_b, [max(g, 1e-16) for g in gaps_b], 'b.-', ms=6)
    ax1.set_ylabel('Gap'); ax1.set_title('Gap and Bott Index vs Exchange')
    ax1.grid(True, alpha=0.3)
    ax2.plot(hexs_b, botts, 'ro-', ms=6)
    ax2.axhline(0, color='gray', ls='--', alpha=0.3)
    ax2.axhline(1, color='green', ls='--', alpha=0.3, label='B=1 (topological)')
    ax2.axhline(-1, color='green', ls='--', alpha=0.3)
    ax2.set_xlabel('h_ex'); ax2.set_ylabel('Bott index B')
    ax2.legend(); ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bott_transition.png'), dpi=200)
    plt.close()

    elapsed = time.time() - t_start

    # ══════════════════════════════════════════════════════════════
    # SUMMARY
    # ══════════════════════════════════════════════════════════════
    # Find gap minimum for each pairing
    min_gap_s = min(r['gap'] for r in results_swave)
    min_gap_p = min(r['gap'] for r in results_pwave)
    hex_min_s = results_swave[np.argmin([r['gap'] for r in results_swave])]['h_ex']
    hex_min_p = results_pwave[np.argmin([r['gap'] for r in results_pwave])]['h_ex']

    # Bott index change
    bott_before = [r['bott'] for r in bott_results if r['h_ex'] < hex_min_p - 0.1]
    bott_after = [r['bott'] for r in bott_results if r['h_ex'] > hex_min_p + 0.1]
    bott_change = False
    if bott_before and bott_after:
        b_before = np.nanmean(bott_before)
        b_after = np.nanmean(bott_after)
        bott_change = abs(b_after - b_before) > 0.3

    print(f"\n{'═' * 55}")
    print(f"  FINE SCAN SUMMARY")
    print(f"{'═' * 55}")
    print(f"  s-wave: gap minimum = {min_gap_s:.4e} at h_ex = {hex_min_s:.2f}")
    print(f"  p-wave: gap minimum = {min_gap_p:.4e} at h_ex = {hex_min_p:.2f}")
    print(f"  Bott index change across transition: {bott_change}")
    if bott_before and bott_after:
        print(f"    Before: B ≈ {np.nanmean(bott_before):.3f}")
        print(f"    After:  B ≈ {np.nanmean(bott_after):.3f}")

    if min_gap_p < 1e-3 or min_gap_s < 1e-3:
        print(f"\n  ✓ Gap closing confirmed (< 1 meV)")
        if bott_change:
            print(f"  ✓ Bott index changes across transition")
            print(f"    → TOPOLOGICAL PHASE TRANSITION DETECTED")
        else:
            print(f"  ? Bott index does not clearly change")
            print(f"    → Transition is real but may need larger system")
            print(f"      for clean Bott index quantization")
    else:
        print(f"\n  Gap minimum > 1 meV: no sharp transition at these parameters")

    print(f"\n  Elapsed: {elapsed:.1f}s")

    summary = {
        'N': N, 'n_defects': len(lat['pentagon_sites']) + len(lat['heptagon_sites']),
        'swave_min_gap': min_gap_s, 'swave_hex_min': hex_min_s,
        'pwave_min_gap': min_gap_p, 'pwave_hex_min': hex_min_p,
        'bott_change': bott_change,
        'bott_before': float(np.nanmean(bott_before)) if bott_before else None,
        'bott_after': float(np.nanmean(bott_after)) if bott_after else None,
        'hex_sweep_swave': results_swave,
        'hex_sweep_pwave': results_pwave,
        'bott_sweep': bott_results,
        'elapsed': elapsed,
    }

    with open(os.path.join(output_dir, 'finescan_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    return summary


if __name__ == "__main__":
    run_fine_scan()
