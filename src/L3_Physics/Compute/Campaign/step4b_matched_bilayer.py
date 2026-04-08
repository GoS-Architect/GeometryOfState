#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  STEP 4b: MATCHED BILAYER — Both Layers Defected
  
  Fix from Step 4: mismatched layers → coupling hybridizes nothing useful.
  Fix: duplicate the SAME defected lattice as both layers.
  
  Now interlayer coupling mixes equivalent Dirac states, enabling
  Weyl node formation from matched band structures.
  
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
from step3_spinful_bdg import extract_interior

A_CC = 1.42
D_INTER = 3.35


def build_matched_bilayer(Nx=15, Ny=15, n_penrose=3,
                           defect_frac=0.04, min_sep=4.0):
    """Both layers: same defected lattice, vertically stacked."""
    print("  Generating single defected layer...")
    raw = generate_lattice(Nx=Nx, Ny=Ny, n_penrose=n_penrose,
                            defect_frac=defect_frac, min_sep=min_sep,
                            do_relax=False)
    lat = extract_interior(raw, margin_factor=4.0)
    N1 = lat['N']
    pos1 = lat['positions']
    bonds1 = lat['bonds']
    bl1 = lat['bond_lengths']

    # Layer 1: z=0, Layer 2: z=D_INTER (identical copy)
    pos_l1 = np.column_stack([pos1, np.zeros(N1)])
    pos_l2 = np.column_stack([pos1, np.full(N1, D_INTER)])
    pos_all = np.vstack([pos_l1, pos_l2])
    N = 2 * N1

    # Intralayer bonds (same topology in both layers)
    bonds_l1 = list(bonds1)
    bonds_l2 = [(i + N1, j + N1) for i, j in bonds1]

    # Interlayer: each atom connects to its mirror (same x,y, different z)
    inter_bonds = [(i, i + N1) for i in range(N1)]
    inter_bl = np.full(N1, D_INTER)

    all_bonds = bonds_l1 + bonds_l2 + inter_bonds
    all_bl = np.concatenate([bl1, bl1, inter_bl])

    # 0=intra L1, 1=intra L2, 2=interlayer
    bond_type = np.array([0]*len(bonds1) + [1]*len(bonds1) + [2]*N1)

    cn = np.zeros(N, dtype=int)
    for i, j in all_bonds:
        cn[i] += 1; cn[j] += 1

    # Defect mask: same pattern in both layers
    defect_mask = np.zeros(N, dtype=bool)
    for d in lat.get('defect_neighborhood', set()):
        if d < N1:
            defect_mask[d] = True
            defect_mask[d + N1] = True

    m2 = 2 * A_CC
    xmn, xmx = pos1[:, 0].min(), pos1[:, 0].max()
    ymn, ymx = pos1[:, 1].min(), pos1[:, 1].max()
    boundary = np.zeros(N, dtype=bool)
    for i in range(N):
        x, y = pos_all[i, 0], pos_all[i, 1]
        if x < xmn + m2 or x > xmx - m2 or y < ymn + m2 or y > ymx - m2:
            boundary[i] = True

    d0 = np.median(bl1) if len(bl1) > 0 else A_CC

    print(f"    Matched bilayer: {N} atoms ({N1}×2), "
          f"{len(all_bonds)} bonds ({len(bonds1)} intra×2 + {N1} inter)")

    return {
        'positions': pos_all, 'bonds': all_bonds,
        'bond_lengths': all_bl, 'bond_type': bond_type,
        'coord_numbers': cn, 'boundary_mask': boundary,
        'defect_mask': defect_mask,
        'd0': d0, 'N': N, 'N1': N1,
        'n_interlayer': N1,
        'n_defects': lat.get('n_defects', 0),
    }


def build_matched_bdg(lat, t0=1.0, mu=1.0, delta=0.3,
                       h_ex=0.0, lambda_R=0.2, t_perp=0.12,
                       pairing='p-wave'):
    """4N×4N spinful BdG for matched bilayer."""
    pos = lat['positions']
    bonds = lat['bonds']
    bl = lat['bond_lengths']
    bond_type = lat['bond_type']
    d0 = lat['d0']
    N = lat['N']
    defect_sites = set(np.where(lat['defect_mask'])[0])

    size = 2 * N
    rows, cols, vals = [], [], []

    for k, (i, j) in enumerate(bonds):
        bt = bond_type[k]
        if bt <= 1:  # Intralayer
            t = t0 * (d0 / bl[k]) ** 2
            for s in [0, N]:
                rows += [i+s, j+s]; cols += [j+s, i+s]; vals += [-t, -t]
            # Rashba (2D bond direction)
            dr = pos[j, :2] - pos[i, :2]
            d2d = np.linalg.norm(dr)
            if d2d > 1e-10:
                dx, dy = dr[0]/d2d, dr[1]/d2d
                v_ud = 1j * lambda_R * (dy - 1j*dx)
                v_du = 1j * lambda_R * (dy + 1j*dx)
                rows += [i, i+N]; cols += [j+N, j]; vals += [v_ud, v_du]
                rows += [j, j+N]; cols += [i+N, i]
                vals += [np.conj(v_du), np.conj(v_ud)]
        else:  # Interlayer
            for s in [0, N]:
                rows += [i+s, j+s]; cols += [j+s, i+s]
                vals += [-t_perp, -t_perp]

    for i in range(N):
        for s in [0, N]:
            rows.append(i+s); cols.append(i+s); vals.append(-mu)

    if h_ex != 0:
        for i in range(N):
            h_i = h_ex if i in defect_sites else 0.0
            if h_i != 0:
                rows += [i, i+N]; cols += [i, i+N]; vals += [h_i, -h_i]

    H_n = sparse.csr_matrix((vals, (rows, cols)), shape=(size, size), dtype=complex)
    assert np.max(np.abs(H_n - H_n.conj().T)) < 1e-12

    # Pairing
    dr, dc, dv = [], [], []
    for k, (i, j) in enumerate(bonds):
        bt = bond_type[k]
        if pairing == 'p-wave' and bt <= 1:
            dij = delta * (d0 / bl[k]) ** 2
            dr += [i, j, i+N, j+N]
            dc += [j+N, i+N, j, i]
            dv += [dij, -dij, -dij, dij]
    # Small on-site stabilizer
    for i in range(N):
        dr += [i, i+N]; dc += [i+N, i]; dv += [delta*0.05, -delta*0.05]

    D = sparse.csr_matrix((dv, (dr, dc)), shape=(size, size), dtype=complex)

    H_BdG = sparse.bmat([[H_n, D], [D.conj().T, -H_n.conj()]], format='csr')
    assert np.max(np.abs(H_BdG - H_BdG.conj().T)) < 1e-12
    return H_BdG


def bott_3d(pos, evecs_occ, N):
    V = evecs_occ[:N, :]
    results = {}
    for c1i, c2i, label in [(0,1,'xy'), (0,2,'xz'), (1,2,'yz')]:
        c1 = pos[:, c1i]; c2 = pos[:, c2i]
        L1 = c1.max()-c1.min(); L2 = c2.max()-c2.min()
        if L1 < 1e-10 or L2 < 1e-10:
            results[label] = np.nan; continue
        c1n = (c1-c1.min())/L1; c2n = (c2-c2.min())/L2
        U1 = V.conj().T @ np.diag(np.exp(2j*np.pi*c1n)) @ V
        U2 = V.conj().T @ np.diag(np.exp(2j*np.pi*c2n)) @ V
        try:
            comm = U1 @ U2 @ np.linalg.inv(U1) @ np.linalg.inv(U2)
            ev = np.linalg.eigvals(comm)
            results[label] = float(np.sum(np.log(ev)).imag / (2*np.pi))
        except:
            results[label] = np.nan
    return results


def analyze_modes(evals, evecs, N, N1, defect_mask, boundary_mask, n=8):
    out = []
    for mi in range(min(n, len(evals))):
        psi = evecs[:, mi]
        prob = np.zeros(N)
        for b in range(4):
            prob += np.abs(psi[b*N:(b+1)*N])**2
        prob /= prob.sum()
        out.append({
            'E': float(evals[mi]), 'absE': float(abs(evals[mi])),
            'L1': float(prob[:N1].sum()), 'L2': float(prob[N1:].sum()),
            'defect': float(prob[defect_mask].sum()),
            'edge': float(prob[boundary_mask].sum()),
            'prob': prob,
        })
    return out


def main():
    os.makedirs("matched_bilayer_results", exist_ok=True)
    out = "matched_bilayer_results"

    print("╔" + "═"*58 + "╗")
    print("║  STEP 4b: MATCHED BILAYER (both layers defected)          ║")
    print("║  Interlayer coupling between resonant Dirac states        ║")
    print("╚" + "═"*58 + "╝")
    t0_time = time.time()

    lat = build_matched_bilayer(Nx=15, Ny=15, n_penrose=3)
    N = lat['N']; N1 = lat['N1']; pos = lat['positions']

    # ═══════════════════════════════════════════════════
    # SCAN 1: t_perp sweep — THE key test
    # ═══════════════════════════════════════════════════
    print(f"\n{'═'*55}")
    print(f"  SCAN 1: t_perp sweep (matched layers)")
    print(f"{'═'*55}")

    tperp_vals = np.concatenate([np.linspace(0, 0.05, 6),
                                  np.linspace(0.06, 0.5, 23)])
    tperp_scan = []

    for tp in tperp_vals:
        H = build_matched_bdg(lat, t0=1.0, mu=1.0, delta=0.3,
                               h_ex=0.0, lambda_R=0.2, t_perp=tp)
        ne = min(16, 4*N-2)
        ev, evec = eigsh(H, k=ne, sigma=0.0, which='LM')
        idx = np.argsort(np.abs(ev)); ev = ev[idx]; evec = evec[:, idx]

        gap = float(np.min(np.abs(ev)))
        modes = analyze_modes(ev, evec, N, N1, lat['defect_mask'],
                              lat['boundary_mask'], n=2)

        occ = ev < 0
        bott = {'xy': np.nan, 'xz': np.nan, 'yz': np.nan}
        if 0 < occ.sum() < len(ev):
            bott = bott_3d(pos, evec[:, occ], N)

        tperp_scan.append({
            't_perp': float(tp), 'gap': gap,
            'bott_xy': bott['xy'], 'bott_xz': bott['xz'], 'bott_yz': bott['yz'],
            'defect': modes[0]['defect'], 'L1': modes[0]['L1'],
        })

        if tp < 0.02 or abs(tp-0.1) < 0.02 or abs(tp-0.2) < 0.02 or \
           abs(tp-0.3) < 0.02 or abs(tp-0.4) < 0.02 or gap < 0.005:
            bxy = f"{bott['xy']:+.3f}" if not np.isnan(bott['xy']) else "  nan"
            bxz = f"{bott['xz']:+.3f}" if not np.isnan(bott['xz']) else "  nan"
            print(f"    t⊥={tp:.3f}: gap={gap:.4e}  B_xy={bxy}  B_xz={bxz}  "
                  f"def={modes[0]['defect']:.2f}  L1={modes[0]['L1']:.2f}")

    # ═══════════════════════════════════════════════════
    # SCAN 2: h_ex sweep at t_perp = 0.12
    # ═══════════════════════════════════════════════════
    print(f"\n{'═'*55}")
    print(f"  SCAN 2: h_ex sweep (matched bilayer, t_perp=0.12)")
    print(f"{'═'*55}")

    hex_vals = np.linspace(0, 1.5, 31)
    hex_scan = []

    for hx in hex_vals:
        H = build_matched_bdg(lat, t0=1.0, mu=1.0, delta=0.3,
                               h_ex=hx, lambda_R=0.2, t_perp=0.12)
        ne = min(12, 4*N-2)
        ev = eigsh(H, k=ne, sigma=0.0, which='LM', return_eigenvectors=False)
        gap = float(np.min(np.abs(ev)))
        hex_scan.append({'h_ex': float(hx), 'gap': gap})
        if hx < 0.03 or gap < 0.003 or abs(hx-0.5) < 0.03 or abs(hx-1.0) < 0.03:
            print(f"    h_ex={hx:.2f}: gap={gap:.4e}")

    # ═══════════════════════════════════════════════════
    # SCAN 3: (t_perp, h_ex) 2D phase map
    # ═══════════════════════════════════════════════════
    print(f"\n{'═'*55}")
    print(f"  SCAN 3: (t_perp, h_ex) phase diagram")
    print(f"{'═'*55}")

    tp_grid = np.linspace(0, 0.4, 11)
    hx_grid = np.linspace(0, 1.2, 13)
    phase_map = np.zeros((len(tp_grid), len(hx_grid)))

    for ti, tp in enumerate(tp_grid):
        for hi, hx in enumerate(hx_grid):
            H = build_matched_bdg(lat, t0=1.0, mu=1.0, delta=0.3,
                                   h_ex=hx, lambda_R=0.2, t_perp=tp)
            ev = eigsh(H, k=min(6, 4*N-2), sigma=0.0, which='LM',
                       return_eigenvectors=False)
            phase_map[ti, hi] = float(np.min(np.abs(ev)))
        print(f"    t_perp={tp:.2f}: min gap={phase_map[ti,:].min():.4e}")

    # ═══════════════════════════════════════════════════
    # DETAILED: reference point
    # ═══════════════════════════════════════════════════
    print(f"\n{'═'*55}")
    print(f"  DETAILED: t_perp=0.12, h_ex=0, p-wave")
    print(f"{'═'*55}")

    H = build_matched_bdg(lat, t0=1.0, mu=1.0, delta=0.3,
                           h_ex=0.0, lambda_R=0.2, t_perp=0.12)
    ne = min(30, 4*N-2)
    ev, evec = eigsh(H, k=ne, sigma=0.0, which='LM')
    idx = np.argsort(np.abs(ev)); ev = ev[idx]; evec = evec[:, idx]

    gap_3d = float(np.min(np.abs(ev)))
    nz = int(np.sum(np.abs(ev) < 1e-4))
    print(f"  Eigenvalues:")
    for i in range(min(12, len(ev))):
        print(f"    E_{i} = {ev[i]:+.8e}")
    print(f"  Gap: {gap_3d:.6e}, near-zero(<1e-4): {nz}")

    modes = analyze_modes(ev, evec, N, N1, lat['defect_mask'],
                          lat['boundary_mask'], n=8)
    print(f"\n  Mode decomposition:")
    for mi, m in enumerate(modes):
        loc = "DEF" if m['defect'] > 0.5 else ("EDGE" if m['edge'] > 0.7 else "BULK")
        print(f"    {mi}: |E|={m['absE']:.2e}  L1={m['L1']:.2f}/L2={m['L2']:.2f}  "
              f"def={m['defect']:.2f}  → {loc}")

    occ = ev < 0
    bott = {'xy': np.nan, 'xz': np.nan, 'yz': np.nan}
    if 0 < occ.sum() < len(ev):
        bott = bott_3d(pos, evec[:, occ], N)
        print(f"\n  Bott indices: B_xy={bott['xy']:+.4f}  "
              f"B_xz={bott['xz']:+.4f}  B_yz={bott['yz']:+.4f}")

    # 2D reference (t_perp=0)
    H0 = build_matched_bdg(lat, t0=1.0, mu=1.0, delta=0.3,
                            h_ex=0.0, lambda_R=0.2, t_perp=0.0)
    ev0 = eigsh(H0, k=min(8, 4*N-2), sigma=0.0, which='LM',
                return_eigenvectors=False)
    gap_2d = float(np.min(np.abs(ev0)))
    ratio = gap_3d / max(gap_2d, 1e-16)

    print(f"\n  2D gap (t_perp=0): {gap_2d:.6e}")
    print(f"  3D gap (t_perp=0.12): {gap_3d:.6e}")
    print(f"  Ratio: {ratio:.2f}×")

    # ═══════════════════════════════════════════════════
    # PLOTS
    # ═══════════════════════════════════════════════════

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    ax = axes[0,0]
    ax.semilogy([r['t_perp'] for r in tperp_scan],
                [max(r['gap'], 1e-16) for r in tperp_scan], 'b.-', ms=5)
    ax.axhline(gap_2d, color='r', ls=':', alpha=0.5, label=f'2D gap ({gap_2d:.2e})')
    ax.set_xlabel('t_perp'); ax.set_ylabel('Gap')
    ax.set_title('Gap vs Interlayer Coupling (Matched)')
    ax.legend(); ax.grid(True, alpha=0.3)

    ax = axes[0,1]
    bxy = [r['bott_xy'] for r in tperp_scan]
    bxz = [r['bott_xz'] for r in tperp_scan]
    ax.plot([r['t_perp'] for r in tperp_scan], bxy, 'r.-', ms=5, label='B_xy')
    ax.plot([r['t_perp'] for r in tperp_scan], bxz, 'b.-', ms=5, label='B_xz')
    ax.axhline(0, color='gray', ls='--', alpha=0.3)
    ax.axhline(1, color='green', ls='--', alpha=0.3, label='B=±1')
    ax.axhline(-1, color='green', ls='--', alpha=0.3)
    ax.set_xlabel('t_perp'); ax.set_ylabel('Bott index')
    ax.set_title('Topological Invariants vs Coupling')
    ax.legend(); ax.grid(True, alpha=0.3)

    ax = axes[1,0]
    ax.semilogy([r['h_ex'] for r in hex_scan],
                [max(r['gap'], 1e-16) for r in hex_scan], 'b.-', ms=4)
    ax.set_xlabel('h_ex'); ax.set_ylabel('Gap')
    ax.set_title('Exchange Sweep (matched bilayer)')
    ax.grid(True, alpha=0.3)

    ax = axes[1,1]
    im = ax.pcolormesh(hx_grid, tp_grid, np.log10(phase_map + 1e-16),
                        cmap='RdBu_r', shading='auto')
    plt.colorbar(im, ax=ax, label='log₁₀(gap)')
    ax.set_xlabel('h_ex'); ax.set_ylabel('t_perp')
    ax.set_title('(t_perp, h_ex) Phase Diagram')

    plt.tight_layout()
    plt.savefig(os.path.join(out, 'matched_bilayer_scans.png'), dpi=200)
    plt.close()

    # Spectrum + wavefunction
    fig, axes = plt.subplots(1, 2, figsize=(16, 7))
    ax = axes[0]
    se = np.sort(ev)
    ax.plot(range(len(se)), se, 'b.-', ms=4)
    ax.axhline(0, color='r', ls='--', alpha=0.5)
    ax.set_xlabel('Index'); ax.set_ylabel('E')
    ax.set_title(f'Matched Bilayer Spectrum\ngap={gap_3d:.4e}')
    ax.grid(True, alpha=0.3)

    ax = axes[1]
    if modes:
        prob = modes[0]['prob']
        sc = ax.scatter(pos[:N1, 0], pos[:N1, 1],
                       c=np.log10(prob[:N1] + 1e-20),
                       cmap='inferno', s=10, ec='none', marker='o')
        ax.scatter(pos[N1:, 0], pos[N1:, 1],
                  c=np.log10(prob[N1:] + 1e-20),
                  cmap='inferno', s=10, ec='none', marker='s', alpha=0.5)
        plt.colorbar(sc, ax=ax, label='log₁₀|ψ|²', shrink=0.7)
        di = np.where(lat['defect_mask'][:N1])[0]
        if len(di) > 0:
            ax.scatter(pos[di, 0], pos[di, 1], fc='none', ec='lime', s=60, lw=1.5)
        ax.set_aspect('equal')
        ax.set_title(f'Lowest mode: L1={modes[0]["L1"]:.2f} '
                     f'def={modes[0]["defect"]:.2f}')
    plt.tight_layout()
    plt.savefig(os.path.join(out, 'matched_bilayer_spectrum.png'), dpi=200)
    plt.close()

    elapsed = time.time() - t0_time

    # ═══════════════════════════════════════════════════
    # VERDICT
    # ═══════════════════════════════════════════════════
    gap_opened = ratio > 2
    has_3d_topo = any(abs(v) > 0.5 for v in bott.values() if not np.isnan(v))
    defect_loc = modes[0]['defect'] > 0.3 if modes else False
    layer_balanced = 0.3 < modes[0]['L1'] < 0.7 if modes else False

    print(f"\n{'═'*55}")
    print(f"  MATCHED BILAYER VERDICT")
    print(f"{'═'*55}")
    print(f"  Gap 2D: {gap_2d:.4e}  →  3D: {gap_3d:.4e}  (×{ratio:.2f})")
    print(f"  Bott: B_xy={bott['xy']:+.3f}  B_xz={bott['xz']:+.3f}")
    print(f"  Defect localized: {defect_loc}")
    print(f"  Layer balanced: {layer_balanced}")
    print(f"  Gap opened: {gap_opened}")
    print(f"  3D topology: {has_3d_topo}")

    if gap_opened and has_3d_topo and defect_loc:
        print(f"\n  ✓ STELLARATOR TRANSITION ACHIEVED")
        print(f"    3D matched geometry stabilizes topology at defect sites.")
    elif gap_opened and defect_loc:
        print(f"\n  ~ Gap opened + defect localized, Bott needs larger system")
    elif gap_opened:
        print(f"\n  ~ Gap opened but modes not yet defect-localized")
    elif has_3d_topo:
        print(f"\n  ~ Topology detected but gap not enhanced")
    else:
        print(f"\n  Assessment: checking h_ex transition structure...")
        # Check if h_ex creates clear transition in matched bilayer
        hex_gaps = [r['gap'] for r in hex_scan]
        min_hgap = min(hex_gaps)
        if min_hgap < 1e-3:
            print(f"    h_ex transition: gap minimum {min_hgap:.4e}")
            print(f"    Topological transition accessible via exchange tuning")
        else:
            print(f"    h_ex transition: gap minimum {min_hgap:.4e} (not sharp)")

    print(f"\n  Elapsed: {elapsed:.1f}s")

    summary = {
        'N': N, 'N1': N1, 'gap_2d': gap_2d, 'gap_3d': gap_3d,
        'ratio': ratio, 'bott': bott,
        'gap_opened': bool(gap_opened), 'has_3d_topo': bool(has_3d_topo),
        'defect_loc': bool(defect_loc), 'layer_balanced': bool(layer_balanced),
        'tperp_scan': tperp_scan, 'hex_scan': hex_scan,
        'modes': [{k: v for k, v in m.items() if k != 'prob'} for m in modes],
        'elapsed': elapsed,
    }
    with open(os.path.join(out, 'summary.json'), 'w') as f:
        json.dump(summary, f, indent=2,
                  default=lambda x: float(x) if isinstance(x, (np.floating, np.integer))
                  else bool(x) if isinstance(x, np.bool_) else str(x))

    return summary


if __name__ == "__main__":
    main()
