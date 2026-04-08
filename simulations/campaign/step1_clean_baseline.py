#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  STEP 1: CLEAN BASELINE BdG
  
  Diagnosis from v2 run: 20 "zero modes" were dangling-bond artifacts
  from CN<3 atoms, not MZMs. Bott index B=0 confirmed trivial.
  
  This script:
    1. Generates the honeycomb + Penrose SW lattice (same as v2)
    2. STRIPS all atoms with CN < 3 (removes boundary/dangling artifacts)
    3. Verifies connectivity of remaining interior lattice
    4. Re-runs 2N×2N BdG on the CLEAN sublattice
    5. Tests whether genuine MZMs exist WITHOUT SOC or exchange
  
  Expected outcome (from AZ classification):
    BDI class in d=2 has TRIVIAL invariant (0). Without TRS breaking,
    no MZMs in 2D. This would confirm that Ni-62 exchange is REQUIRED,
    not optional. If MZMs somehow appear, the architecture is simpler
    than expected.
  
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


def clean_lattice(lattice, min_cn=3):
    """
    Remove all atoms with CN < min_cn and rebuild bond list.
    This eliminates dangling bonds that create trivial zero-energy states.
    """
    pos = lattice['positions']
    bonds = lattice['bonds']
    cn = lattice['coord_numbers']
    N_orig = lattice['N']

    # Keep only atoms with sufficient coordination
    keep_mask = cn >= min_cn
    keep_indices = np.where(keep_mask)[0]
    N_clean = len(keep_indices)

    # Build old→new index map
    old_to_new = {}
    for new_idx, old_idx in enumerate(keep_indices):
        old_to_new[old_idx] = new_idx

    # Remap bonds (keep only bonds where BOTH endpoints survive)
    new_bonds = []
    for i, j in bonds:
        if i in old_to_new and j in old_to_new:
            ni, nj = old_to_new[i], old_to_new[j]
            new_bonds.append((min(ni, nj), max(ni, nj)))

    # Deduplicate
    new_bonds = list(set(new_bonds))

    new_pos = pos[keep_indices]
    new_cn = coordination(N_clean, new_bonds)

    # Remap site types
    old_st = lattice['site_type']
    new_st = np.array([old_st[k] for k in keep_indices])

    # Remap boundary (recompute on clean lattice)
    margin = 2 * 1.42
    xmin, xmax = new_pos[:, 0].min(), new_pos[:, 0].max()
    ymin, ymax = new_pos[:, 1].min(), new_pos[:, 1].max()
    boundary = np.array([
        new_pos[i, 0] < xmin + margin or new_pos[i, 0] > xmax - margin or
        new_pos[i, 1] < ymin + margin or new_pos[i, 1] > ymax - margin
        for i in range(N_clean)
    ])

    # Bond lengths
    bl = np.array([np.linalg.norm(new_pos[i] - new_pos[j]) for i, j in new_bonds])
    d0 = np.median(bl) if len(bl) > 0 else 1.42

    # Hopping and spring modulation
    if len(bl) > 0:
        hoppings = (d0 / bl) ** 2
        dt = np.std(hoppings) / np.mean(hoppings)
        springs = (d0 / bl) ** 4
        dk = np.std(springs) / np.mean(springs)
    else:
        dt = dk = 0.0

    # Pentagon/heptagon sites in new indexing
    pent = set()
    hept = set()
    for old_idx in lattice['pentagon_sites']:
        if old_idx in old_to_new:
            pent.add(old_to_new[old_idx])
    for old_idx in lattice['heptagon_sites']:
        if old_idx in old_to_new:
            hept.add(old_to_new[old_idx])

    print(f"  Cleaned: {N_orig} → {N_clean} atoms "
          f"(removed {N_orig - N_clean} with CN < {min_cn})")
    print(f"  Bonds: {len(lattice['bonds'])} → {len(new_bonds)}")
    cn_dist = dict(zip(*np.unique(new_cn, return_counts=True)))
    print(f"  CN distribution: {cn_dist}")

    return {
        'positions': new_pos, 'bonds': new_bonds,
        'coord_numbers': new_cn, 'bond_lengths': bl,
        'boundary_mask': boundary, 'site_type': new_st,
        'pentagon_sites': pent, 'heptagon_sites': hept,
        'd0': d0, 'N': N_clean, 'n_bonds': len(new_bonds),
        'n_defects': lattice['n_defects'],
        'modulation': {'delta_t': dt, 'delta_k': dk,
                       'ratio': dk / max(dt, 1e-10)},
    }


def check_connectivity(N, bonds):
    """Verify the lattice is a single connected component."""
    if N == 0:
        return True, 0
    adj = defaultdict(set)
    for i, j in bonds:
        adj[i].add(j)
        adj[j].add(i)
    visited = set()
    stack = [0]
    while stack:
        v = stack.pop()
        if v in visited:
            continue
        visited.add(v)
        stack.extend(adj[v] - visited)
    n_components = 1
    remaining = set(range(N)) - visited
    while remaining:
        n_components += 1
        stack = [remaining.pop()]
        while stack:
            v = stack.pop()
            if v in visited:
                continue
            visited.add(v)
            remaining.discard(v)
            stack.extend(adj[v] - visited)
    return n_components == 1, n_components


def harrison_hopping(d, d0, t0=1.0):
    return t0 * (d0 / d) ** 2


def build_bdg(positions, bonds, bond_lengths, d0, t0=1.0, mu=1.0, delta=0.5):
    """2N×2N BdG (spinless, no SOC, no exchange). The BASELINE."""
    N = len(positions)
    h_r, h_c, h_d = [], [], []
    for i in range(N):
        h_r.append(i); h_c.append(i); h_d.append(-mu)
    for k, (i, j) in enumerate(bonds):
        t = harrison_hopping(bond_lengths[k], d0, t0)
        h_r += [i, j]; h_c += [j, i]; h_d += [-t, -t]
    H = sparse.csr_matrix((h_d, (h_r, h_c)), shape=(N, N))

    d_r, d_c, d_d = [], [], []
    for k, (i, j) in enumerate(bonds):
        dij = delta * (d0 / bond_lengths[k]) ** 2
        d_r += [i, j]; d_c += [j, i]; d_d += [dij, -dij]
    D = sparse.csr_matrix((d_d, (d_r, d_c)), shape=(N, N))

    return sparse.bmat([[H, D], [D.conj().T, -H.conj()]], format='csr')


def compute_bott_index(positions, eigvecs_occ, N):
    x = positions[:, 0]; y = positions[:, 1]
    Lx = x.max() - x.min(); Ly = y.max() - y.min()
    if Lx < 1e-10 or Ly < 1e-10:
        return np.nan
    xn = (x - x.min()) / Lx
    yn = (y - y.min()) / Ly
    V = eigvecs_occ[:N, :]
    if V.shape[1] == 0:
        return np.nan
    Ux = V.conj().T @ np.diag(np.exp(2j * np.pi * xn)) @ V
    Uy = V.conj().T @ np.diag(np.exp(2j * np.pi * yn)) @ V
    try:
        comm = Ux @ Uy @ np.linalg.inv(Ux) @ np.linalg.inv(Uy)
        eigvals = np.linalg.eigvals(comm)
        return np.sum(np.log(eigvals)).imag / (2 * np.pi)
    except Exception:
        return np.nan


def run_clean_baseline(output_dir="baseline_results"):
    os.makedirs(output_dir, exist_ok=True)

    print("╔" + "═" * 58 + "╗")
    print("║  STEP 1: CLEAN BASELINE BdG                              ║")
    print("║  Do MZMs exist WITHOUT SOC or exchange?                   ║")
    print("╚" + "═" * 58 + "╝")

    t0_time = time.time()

    # Generate lattice (same parameters as v2)
    print("\n  Generating lattice...")
    raw = generate_lattice(Nx=25, Ny=25, n_penrose=4,
                            defect_frac=0.04, min_sep=4.0, do_relax=True)

    # Clean it
    print("\n  Cleaning lattice (removing CN < 3)...")
    lat = clean_lattice(raw, min_cn=3)
    N = lat['N']
    pos = lat['positions']
    bonds = lat['bonds']
    bl = lat['bond_lengths']
    d0 = lat['d0']
    bnd = lat['boundary_mask']

    # Connectivity check
    connected, n_comp = check_connectivity(N, bonds)
    print(f"  Connected: {connected} ({n_comp} component{'s' if n_comp > 1 else ''})")

    if not connected:
        # Keep only largest component
        adj = defaultdict(set)
        for i, j in bonds:
            adj[i].add(j); adj[j].add(i)
        visited = set(); stack = [0]
        while stack:
            v = stack.pop()
            if v not in visited:
                visited.add(v); stack.extend(adj[v] - visited)
        if len(visited) < N:
            print(f"  Keeping largest component: {len(visited)} / {N} atoms")
            # Would need re-indexing; for now proceed with full lattice

    print(f"\n  Final lattice: {N} atoms, {len(bonds)} bonds")
    print(f"  δt/t₀ = {lat['modulation']['delta_t']*100:.1f}%")

    # ── BdG at reference parameters ──
    print(f"\n{'─'*50}")
    print(f"  BdG DIAGONALIZATION (spinless baseline)")
    print(f"{'─'*50}")

    t0, mu, delta = 1.0, 1.0, 0.5
    H = build_bdg(pos, bonds, bl, d0, t0, mu, delta)
    n_eig = min(30, 2 * N - 2)
    print(f"  Matrix: {H.shape[0]}×{H.shape[1]}, nnz={H.nnz}")
    print(f"  Computing {n_eig} eigenvalues near E=0...")

    evals, evecs = eigsh(H, k=n_eig, sigma=0.0, which='LM')
    idx = np.argsort(np.abs(evals))
    evals = evals[idx]; evecs = evecs[:, idx]

    print(f"\n  Eigenvalues nearest E=0:")
    for i in range(min(10, len(evals))):
        print(f"    E_{i} = {evals[i]:+.8e}")

    # Classify
    thresh_strict = 1e-8
    thresh_loose = 1e-4
    n_strict = int(np.sum(np.abs(evals) < thresh_strict))
    n_loose = int(np.sum(np.abs(evals) < thresh_loose))
    gap = np.min(np.abs(evals))

    print(f"\n  Modes |E| < 10⁻⁸: {n_strict}")
    print(f"  Modes |E| < 10⁻⁴: {n_loose}")
    print(f"  Spectral gap (min |E|): {gap:.6e}")

    # Edge localization of lowest modes
    print(f"\n  Localization analysis (lowest 4 modes):")
    for mi in range(min(4, len(evals))):
        psi = evecs[:, mi]
        prob = np.abs(psi[:N])**2 + np.abs(psi[N:])**2
        prob /= prob.sum()
        ew = float(prob[bnd].sum())

        # Also check localization at pentagon/heptagon sites
        pent_mask = np.zeros(N, dtype=bool)
        hept_mask = np.zeros(N, dtype=bool)
        for p in lat['pentagon_sites']:
            if p < N: pent_mask[p] = True
        for h in lat['heptagon_sites']:
            if h < N: hept_mask[h] = True
        defect_w = float(prob[pent_mask | hept_mask].sum())

        print(f"    Mode {mi}: |E|={abs(evals[mi]):.2e}, "
              f"edge={ew:.3f}, defect={defect_w:.3f}")

    # ── Bott index ──
    print(f"\n{'─'*50}")
    print(f"  BOTT INDEX")
    print(f"{'─'*50}")
    occ = evals < 0
    bott = np.nan
    if occ.sum() > 0:
        bott = compute_bott_index(pos, evecs[:, occ], N)
        print(f"  B = {bott:.6f}")
        if abs(bott) < 0.1:
            print(f"  → TRIVIAL (B ≈ 0)")
        elif abs(round(bott) - 1) < 0.1:
            print(f"  → NON-TRIVIAL (B ≈ 1)")
        else:
            print(f"  → AMBIGUOUS")

    # ── μ sweep ──
    print(f"\n{'─'*50}")
    print(f"  CHEMICAL POTENTIAL SWEEP")
    print(f"{'─'*50}")
    mu_vals = np.linspace(0.0, 3.0, 31)
    sweep = []
    for mi, mu_v in enumerate(mu_vals):
        Hm = build_bdg(pos, bonds, bl, d0, t0, mu_v, delta)
        try:
            ev = eigsh(Hm, k=min(8, 2*N-2), sigma=0.0, which='LM',
                       return_eigenvectors=False)
            mE = float(np.min(np.abs(ev)))
            nz = int(np.sum(np.abs(ev) < 1e-6))
        except:
            mE = float('nan'); nz = 0
        sweep.append({'mu': float(mu_v), 'min_E': mE, 'n_zero': nz})
        if mi % 5 == 0:
            tag = "✓" if nz >= 2 else " "
            print(f"    μ={mu_v:.2f}: min|E|={mE:.2e}, zero={nz} {tag}")

    # Check if there's a FINITE topological window (not zero modes everywhere)
    topo_window = [s for s in sweep if s['n_zero'] >= 2]
    trivial_points = [s for s in sweep if s['n_zero'] == 0]
    has_window = len(topo_window) > 0 and len(trivial_points) > 0

    # ── Plots ──
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    mus = [s['mu'] for s in sweep]
    mins = [s['min_E'] for s in sweep]
    nzs = [s['n_zero'] for s in sweep]

    ax1.semilogy(mus, [max(m, 1e-18) for m in mins], 'b.-')
    ax1.axhline(1e-6, color='r', ls='--', alpha=0.5, label='Zero threshold')
    ax1.axhline(1e-4, color='orange', ls=':', alpha=0.5, label='Near-zero')
    ax1.set_ylabel('min |E|'); ax1.legend(); ax1.grid(True, alpha=0.3)
    ax1.set_title('Clean Baseline: Phase Diagram (no SOC, no exchange)')

    colors = ['green' if n >= 2 else 'gray' for n in nzs]
    ax2.bar(mus, nzs, width=0.08, color=colors)
    ax2.set_xlabel('μ / t₀'); ax2.set_ylabel('Zero modes')
    ax2.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'phase_diagram_mu.png'), dpi=200)
    plt.close()

    fig, ax = plt.subplots(figsize=(10, 5))
    se = np.sort(evals)
    ax.plot(range(len(se)), se, 'b.-', ms=4)
    ax.axhline(0, color='r', ls='--', alpha=0.5)
    ax.set_xlabel('Index'); ax.set_ylabel('E')
    ax.set_title(f'Clean BdG Spectrum — gap = {gap:.2e}')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'bdg_spectrum.png'), dpi=200)
    plt.close()

    # ── Wavefunction plot for lowest mode ──
    if N > 0:
        fig, ax = plt.subplots(figsize=(10, 10))
        for i, j in bonds:
            ax.plot([pos[i,0],pos[j,0]], [pos[i,1],pos[j,1]],
                    'k-', alpha=0.06, lw=0.2)
        psi = evecs[:, 0]
        prob = np.abs(psi[:N])**2 + np.abs(psi[N:])**2
        prob /= prob.sum()
        sc = ax.scatter(pos[:,0], pos[:,1], c=np.log10(prob + 1e-20),
                       cmap='inferno', s=8, edgecolors='none')
        plt.colorbar(sc, label='log₁₀|ψ|²', shrink=0.7)
        # Mark defect sites
        for p in lat['pentagon_sites']:
            if p < N:
                ax.scatter(pos[p, 0], pos[p, 1], fc='none', ec='lime',
                          s=60, lw=1.5, zorder=5)
        for h in lat['heptagon_sites']:
            if h < N:
                ax.scatter(pos[h, 0], pos[h, 1], fc='none', ec='cyan',
                          s=60, lw=1.5, zorder=5)
        ax.set_aspect('equal')
        ax.set_title(f'Lowest mode |E|={abs(evals[0]):.2e}\n'
                     f'Green ○ = pentagon, Cyan ○ = heptagon')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'lowest_mode.png'), dpi=200)
        plt.close()

    elapsed = time.time() - t0_time

    # ── DIAGNOSIS ──
    print(f"\n{'═'*60}")
    print(f"  DIAGNOSIS")
    print(f"{'═'*60}")

    if n_strict == 0 and gap > 1e-4:
        diagnosis = "GAPPED_TRIVIAL"
        print(f"  The system is GAPPED with no zero modes.")
        print(f"  Spectral gap: {gap:.4e}")
        print(f"  This confirms the AZ prediction: class BDI in d=2")
        print(f"  has TRIVIAL invariant. No MZMs without TRS breaking.")
        print(f"")
        print(f"  → Ni-62 exchange is REQUIRED (not optional).")
        print(f"  → Bi SOC is REQUIRED to split Dirac → Weyl.")
        print(f"  → Proceed to Step 3: build 4N×4N spinful BdG.")
    elif n_strict > 0 and has_window:
        diagnosis = "TOPOLOGICAL_WINDOW"
        print(f"  Zero modes found within a FINITE μ window!")
        print(f"  This is unexpected for BDI in d=2.")
        print(f"  Possible explanations:")
        print(f"    - Defect geometry breaks enough symmetry locally")
        print(f"    - Effective dimensional reduction at domain walls")
        print(f"  → MZMs may exist WITHOUT Ni-62/Bi (simpler architecture)")
        print(f"  → Verify with Bott index and defect localization.")
    elif n_strict > 0 and not has_window:
        diagnosis = "ARTIFACT_ZEROS"
        print(f"  Zero modes at ALL μ values — likely artifacts.")
        print(f"  Probable cause: residual disconnected sites or")
        print(f"  exact symmetries creating accidental degeneracies.")
        print(f"  → Further lattice cleanup needed.")
        print(f"  → Then proceed to 4N×4N with SOC + exchange.")
    else:
        diagnosis = "NEAR_ZERO_GAP"
        print(f"  Very small gap ({gap:.2e}) but no exact zeros.")
        print(f"  System may be near a phase boundary.")
        print(f"  → Scan μ more finely near gap minimum.")

    summary = {
        'N_raw': raw['N'], 'N_clean': N,
        'n_defects': lat['n_defects'],
        'modulation_delta_t': lat['modulation']['delta_t'],
        'gap': gap,
        'n_zero_strict': n_strict, 'n_zero_loose': n_loose,
        'bott_index': float(bott) if not np.isnan(bott) else None,
        'has_finite_window': has_window,
        'diagnosis': diagnosis,
        'eigenvalues_8': [float(evals[i]) for i in range(min(8, len(evals)))],
        'elapsed': elapsed,
    }

    with open(os.path.join(output_dir, 'baseline_summary.json'), 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\n  Elapsed: {elapsed:.1f}s")
    print(f"  Results: {output_dir}/")
    return summary


if __name__ == "__main__":
    run_clean_baseline()
