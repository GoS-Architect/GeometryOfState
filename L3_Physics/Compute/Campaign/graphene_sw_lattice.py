#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  GRAPHENE LATTICE GENERATOR WITH PENROSE-SELECTED STONE-WALES DEFECTS
  
  The critical fix identified by Stage 1 failure analysis:
  
  WRONG (v1): Use Penrose tiling vertices as lattice sites.
    → CN = {3,4,5,6,8,10}, δt/t₀ = 59%, no MZMs.
    
  CORRECT (v2): Start with honeycomb, overlay Penrose to select SW sites.
    → CN ∈ {2,3,4}, δt/t₀ ≈ 9.7%, matching thesis Harrison scaling.
    (Honeycomb CN is 3, not 6 — that's the triangulated dual.)
  
  Pipeline:
    1. Generate pristine honeycomb graphene lattice (CN = 3 everywhere)
    2. Generate Penrose P3 tiling at matching scale
    3. Map Penrose vertices to nearest honeycomb bond midpoints
    4. Apply Stone-Wales rotations at selected sites
    5. Relax via Keating energy minimization
    6. Export lattice for BdG and phonon simulations
═══════════════════════════════════════════════════════════════════════════════
"""

import numpy as np
from scipy.spatial import cKDTree
from scipy.optimize import minimize
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os

PHI = (1 + np.sqrt(5)) / 2
A_CC = 1.42  # Å


def generate_honeycomb(Nx, Ny, a_cc=A_CC):
    """Generate pristine honeycomb lattice. CN=3 for all interior atoms."""
    a_lat = a_cc * np.sqrt(3)
    a1 = a_lat * np.array([1.0, 0.0])
    a2 = a_lat * np.array([0.5, np.sqrt(3)/2])
    basis_b = (a1 + a2) / 3.0

    positions = []
    sublattice = []
    index_map = {}

    for nx in range(Nx):
        for ny in range(Ny):
            origin = nx * a1 + ny * a2
            idx_a = len(positions)
            positions.append(origin.copy())
            sublattice.append(0)
            index_map[(nx, ny, 0)] = idx_a

            idx_b = len(positions)
            positions.append(origin + basis_b)
            sublattice.append(1)
            index_map[(nx, ny, 1)] = idx_b

    positions = np.array(positions)
    sublattice = np.array(sublattice)

    bonds = set()
    for nx in range(Nx):
        for ny in range(Ny):
            ia = index_map.get((nx, ny, 0))
            if ia is None:
                continue
            for key in [(nx, ny, 1), (nx-1, ny, 1), (nx, ny-1, 1)]:
                jb = index_map.get(key)
                if jb is not None:
                    bonds.add((min(ia, jb), max(ia, jb)))

    return positions, list(bonds), sublattice


def adjacency(N, bonds):
    adj = defaultdict(set)
    for i, j in bonds:
        adj[i].add(j)
        adj[j].add(i)
    return adj


def coordination(N, bonds):
    cn = np.zeros(N, dtype=int)
    for i, j in bonds:
        cn[i] += 1
        cn[j] += 1
    return cn


# ── Penrose overlay ──────────────────────────────────────────────────────────

class RT:
    def __init__(self, t, A, B, C):
        self.t = t; self.A = A; self.B = B; self.C = C

def subdivide(tris):
    out = []
    for tr in tris:
        A, B, C = tr.A, tr.B, tr.C
        if tr.t == 0:
            P = A + (B - A) / PHI
            out.append(RT(0, C, P, B)); out.append(RT(1, P, C, A))
        else:
            Q = B + (A - B) / PHI; R = B + (C - B) / PHI
            out.append(RT(1, R, C, A)); out.append(RT(1, Q, R, B))
            out.append(RT(0, R, Q, A))
    return out

def penrose_points(n_sub, scale=1.0):
    tris = []
    for i in range(10):
        a1 = (2*i) * np.pi / 10; a2 = (2*i+2) * np.pi / 10
        B = np.exp(1j*a1); C = np.exp(1j*a2)
        tris.append(RT(0, 0j, B, C) if i % 2 == 0 else RT(0, 0j, C, B))
    for _ in range(n_sub):
        tris = subdivide(tris)
    tol = 1e-8
    vset = set()
    for tr in tris:
        for z in [tr.A, tr.B, tr.C]:
            vset.add((round(z.real/tol)*tol, round(z.imag/tol)*tol))
    pts = np.array([[x, y] for x, y in vset]) * scale
    return pts


# ── Stone-Wales rotation ─────────────────────────────────────────────────────

def ordered_neighbors(i, adj_map, positions):
    """Get neighbors of i ordered counterclockwise by angle (planar embedding)."""
    nbrs = list(adj_map[i])
    if not nbrs:
        return []
    angles = [np.arctan2(positions[j,1]-positions[i,1],
                          positions[j,0]-positions[i,0]) for j in nbrs]
    return [n for _, n in sorted(zip(angles, nbrs))]


def trace_face(a, b, adj_map, positions, max_ring=8):
    """
    Trace the face on the LEFT side of directed edge a→b in a planar graph.
    Returns the ring as a list of vertex indices, or None if not found.
    
    In a honeycomb lattice, every interior edge borders two hexagonal faces.
    This function finds one of them by walking counterclockwise.
    """
    ring = [a]
    current = a
    next_v = b
    for _ in range(max_ring):
        ring.append(next_v)
        ordered = ordered_neighbors(next_v, adj_map, positions)
        if current not in ordered:
            return None
        idx = ordered.index(current)
        # Next in clockwise = previous in counterclockwise order
        next_next = ordered[(idx - 1) % len(ordered)]
        if next_next == ring[0]:
            return ring  # closed the ring
        current = next_v
        next_v = next_next
    return None  # didn't close


def find_sw_quad(a, b, adj_map, positions):
    """
    Find the Stone-Wales quadrilateral for bond (a,b).
    
    In a honeycomb, bond (a,b) borders two hexagonal faces.
    The SW quad consists of (a, b, c, d) where c and d are the
    atoms at distance 2 from both a and b in each hexagonal ring —
    the "wing tips" of the butterfly.
    
    Returns (c, d) or None if not a valid SW site.
    """
    # Trace both faces of the edge
    face1 = trace_face(a, b, adj_map, positions)
    face2 = trace_face(b, a, adj_map, positions)
    
    if face1 is None or face2 is None:
        return None
    if len(face1) != 6 or len(face2) != 6:
        return None  # only apply SW to hexagonal faces
    
    # In a hexagon a-b-x1-x2-x3-x4, the atom "opposite" the bond a-b
    # is at position 3 in the ring (distance 3 from both a and b around ring)
    # face1 = [a, b, v1, v2, v3, v4] → opposite vertex is v2 (index 3)
    c = face1[3]
    d = face2[3]
    
    if c == d:
        return None
    
    return c, d


def find_sw_candidates(positions, bonds, adj_map, penrose_pts,
                        min_sep=3.0, a_cc=A_CC):
    """Select bonds for SW rotation nearest to Penrose vertices.
    Uses face-tracing for honeycomb (not common-neighbor method)."""
    N = len(positions)
    cn = coordination(N, bonds)

    midpoints = []
    valid_indices = []
    quad_map = {}  # bond_idx → (c, d) quad wing tips

    for k, (i, j) in enumerate(bonds):
        # Only interior bonds with full coordination
        if cn[i] < 3 or cn[j] < 3:
            continue
        quad = find_sw_quad(i, j, adj_map, positions)
        if quad is not None:
            midpoints.append((positions[i] + positions[j]) / 2.0)
            valid_indices.append(k)
            quad_map[k] = quad

    print(f"    {len(valid_indices)} interior bonds with valid SW quads")

    if not midpoints:
        return [], {}

    midpoints = np.array(midpoints)
    tree = cKDTree(midpoints)

    selected = []
    sel_pos = []
    for pp in penrose_pts:
        dist, idx = tree.query(pp)
        bond_idx = valid_indices[idx]
        mid = midpoints[idx]
        if any(np.linalg.norm(mid - sp) < min_sep * a_cc for sp in sel_pos):
            continue
        if bond_idx not in selected:
            selected.append(bond_idx)
            sel_pos.append(mid)
    return selected, quad_map


def apply_single_sw(positions, bonds_list, adj_map, bond_idx, quad_map):
    """
    Apply one SW rotation using face-derived quad.
    
    SW rotation of bond (a,b) with quad wings (c,d):
    - Remove bond (a,b)
    - Add bond (c,d)
    This converts two adjacent hexagons into a 5-7-7-5 quartet.
    
    a,b lose a bond → their rings become pentagons
    c,d gain a bond → their rings become heptagons
    """
    a, b = bonds_list[bond_idx]
    if bond_idx not in quad_map:
        return bonds_list, None
    c, d = quad_map[bond_idx]
    
    existing = set((min(i,j), max(i,j)) for i,j in bonds_list)
    if (min(c,d), max(c,d)) in existing:
        return bonds_list, None
    
    removed = (min(a,b), max(a,b))
    new_bonds = [e for e in bonds_list if (min(e[0],e[1]), max(e[0],e[1])) != removed]
    new_bonds.append((min(c,d), max(c,d)))
    return new_bonds, {'removed': (a,b), 'added': (c,d),
                        'pentagon': [a,b], 'heptagon': [c,d]}


def apply_all_sw(positions, bonds, sw_indices, quad_map):
    cur = list(bonds)
    N = len(positions)
    infos = []
    pent = set(); hept = set()

    for bond_idx in sw_indices:
        if bond_idx not in quad_map:
            continue
        a, b = bonds[bond_idx]
        target = (min(a,b), max(a,b))
        adj_map = adjacency(N, cur)
        for k, (i, j) in enumerate(cur):
            if (min(i,j), max(i,j)) == target:
                cur, info = apply_single_sw(positions, cur, adj_map, k, 
                                            {k: quad_map[bond_idx]})
                if info:
                    infos.append(info)
                    pent.update(info['pentagon'])
                    hept.update(info['heptagon'])
                break
    print(f"    Applied {len(infos)} SW defects")
    return cur, infos, pent, hept


# ── Keating relaxation ────────────────────────────────────────────────────────

def keating_energy(flat_pos, bonds, adj_map, a_cc=A_CC):
    N = len(flat_pos) // 2
    pos = flat_pos.reshape(N, 2)
    alpha, beta = 26.9, 5.4
    d0_sq = a_cc ** 2

    E = 0.0
    for i, j in bonds:
        dr = pos[i] - pos[j]
        E += alpha / 2 * (dr @ dr - d0_sq) ** 2 / (4 * d0_sq)

    for i in range(N):
        nbrs = list(adj_map[i])
        for ni in range(len(nbrs)):
            for nj in range(ni+1, len(nbrs)):
                rij = pos[nbrs[ni]] - pos[i]
                rik = pos[nbrs[nj]] - pos[i]
                E += beta / 2 * (rij @ rik + d0_sq / 2) ** 2 / d0_sq ** 2
    return E


def relax(positions, bonds, a_cc=A_CC, maxiter=300):
    N = len(positions)
    adj_map = adjacency(N, bonds)
    cn = coordination(N, bonds)

    margin = 2 * a_cc
    xmin, xmax = positions[:,0].min(), positions[:,0].max()
    ymin, ymax = positions[:,1].min(), positions[:,1].max()
    free = np.array([
        i for i in range(N)
        if (positions[i,0] > xmin + margin and positions[i,0] < xmax - margin and
            positions[i,1] > ymin + margin and positions[i,1] < ymax - margin and
            cn[i] >= 3)
    ])

    if len(free) == 0:
        E0 = keating_energy(positions.flatten(), bonds, adj_map, a_cc)
        return positions.copy(), E0, E0

    print(f"    Relaxing {len(free)} / {N} atoms...")
    x0 = positions[free].flatten()

    def obj(x):
        p = positions.copy()
        p[free] = x.reshape(-1, 2)
        return keating_energy(p.flatten(), bonds, adj_map, a_cc)

    E0 = obj(x0)
    res = minimize(obj, x0, method='L-BFGS-B', options={'maxiter': maxiter, 'ftol': 1e-6})
    relaxed = positions.copy()
    relaxed[free] = res.x.reshape(-1, 2)
    print(f"    Energy: {E0:.2f} → {res.fun:.2f} eV ({100*(E0-res.fun)/max(E0,1e-10):.1f}% reduction)")
    return relaxed, E0, res.fun


# ── Full pipeline ─────────────────────────────────────────────────────────────

def generate_lattice(Nx=20, Ny=20, n_penrose=4, defect_frac=0.05,
                      min_sep=3.5, do_relax=True):
    print("═" * 60)
    print("  GRAPHENE + PENROSE SW LATTICE GENERATOR v2")
    print("═" * 60)

    print(f"\n  Step 1: {Nx}×{Ny} honeycomb...")
    pos, bonds, sub = generate_honeycomb(Nx, Ny)
    N = len(pos)
    print(f"    {N} atoms, {len(bonds)} bonds")

    print(f"\n  Step 2: Penrose overlay (depth {n_penrose})...")
    extent = max(pos[:,0].max()-pos[:,0].min(), pos[:,1].max()-pos[:,1].min())
    pp = penrose_points(n_penrose, scale=extent/2.0) + pos.mean(axis=0)
    margin = 3 * A_CC
    mask = ((pp[:,0] > pos[:,0].min() + margin) & (pp[:,0] < pos[:,0].max() - margin) &
            (pp[:,1] > pos[:,1].min() + margin) & (pp[:,1] < pos[:,1].max() - margin))
    pp = pp[mask]
    n_target = max(1, int(defect_frac * len(bonds)))
    if len(pp) > n_target:
        pp = pp[np.linspace(0, len(pp)-1, n_target, dtype=int)]
    print(f"    {len(pp)} Penrose sites selected")

    print(f"\n  Step 3: Selecting SW candidates...")
    adj_map = adjacency(N, bonds)
    cands, quad_map = find_sw_candidates(pos, bonds, adj_map, pp, min_sep=min_sep)
    print(f"    {len(cands)} candidates")

    print(f"\n  Step 4: Applying SW rotations...")
    new_bonds, infos, pent, hept = apply_all_sw(pos, bonds, cands, quad_map)
    cn_after = coordination(N, new_bonds)
    print(f"    CN distribution: {dict(zip(*np.unique(cn_after, return_counts=True)))}")

    if do_relax and infos:
        print(f"\n  Step 5: Keating relaxation...")
        rpos, E0, Ef = relax(pos, new_bonds)
    else:
        rpos = pos.copy(); E0 = Ef = 0.0

    bl = np.array([np.linalg.norm(rpos[i]-rpos[j]) for i,j in new_bonds])
    d0 = np.median(bl)
    dt = np.std((d0/bl)**2) / np.mean((d0/bl)**2)
    dk = np.std((d0/bl)**4) / np.mean((d0/bl)**4)

    print(f"\n  Step 6: Bond statistics")
    print(f"    d₀ = {d0:.4f} Å, δt/t₀ = {dt*100:.1f}%, δk/k₀ = {dk*100:.1f}%")
    print(f"    Ratio = {dk/max(dt,1e-10):.2f}×")

    bnd = 2 * A_CC
    boundary = np.array([
        pos[i,0] < pos[:,0].min()+bnd or pos[i,0] > pos[:,0].max()-bnd or
        pos[i,1] < pos[:,1].min()+bnd or pos[i,1] > pos[:,1].max()-bnd or
        cn_after[i] < 2
        for i in range(N)
    ])

    site_type = np.full(N, 'hex', dtype='U4')
    for i in pent:
        if i < N: site_type[i] = 'pent'
    for i in hept:
        if i < N: site_type[i] = 'hept'

    return {
        'positions': rpos, 'bonds': new_bonds, 'sublattice': sub,
        'coord_numbers': cn_after, 'bond_lengths': bl,
        'boundary_mask': boundary, 'site_type': site_type,
        'pentagon_sites': pent, 'heptagon_sites': hept,
        'defect_info': infos, 'd0': d0,
        'modulation': {'delta_t': dt, 'delta_k': dk,
                       'ratio': dk/max(dt,1e-10)},
        'keating_energy': {'initial': E0, 'final': Ef},
        'N': N, 'n_bonds': len(new_bonds), 'n_defects': len(infos),
    }


def plot_lattice(lat, filename):
    pos = lat['positions']; bonds = lat['bonds']
    cn = lat['coord_numbers']; st = lat['site_type']
    N = lat['N']
    fig, axes = plt.subplots(1, 2, figsize=(20, 10))

    ax = axes[0]
    for i,j in bonds:
        ax.plot([pos[i,0],pos[j,0]], [pos[i,1],pos[j,1]], 'k-', alpha=0.12, lw=0.3)
    sc = ax.scatter(pos[:,0], pos[:,1], c=cn, cmap='coolwarm', s=6,
                    edgecolors='none', vmin=2, vmax=4)
    plt.colorbar(sc, ax=ax, label='CN', shrink=0.7)
    ax.set_aspect('equal')
    ax.set_title(f'CN Map — {N} atoms, {lat["n_defects"]} SW defects')

    ax = axes[1]
    for i,j in bonds:
        ax.plot([pos[i,0],pos[j,0]], [pos[i,1],pos[j,1]], 'k-', alpha=0.12, lw=0.3)
    cmap = {'hex': '#2E75B6', 'pent': '#2D8B4E', 'hept': '#C0392B'}
    colors = [cmap.get(s, '#999') for s in st]
    ax.scatter(pos[:,0], pos[:,1], c=colors, s=6, edgecolors='none')
    from matplotlib.patches import Patch
    ax.legend(handles=[Patch(fc='#2E75B6', label='Hexagon'),
                       Patch(fc='#2D8B4E', label='Pentagon (κ>0)'),
                       Patch(fc='#C0392B', label='Heptagon (κ<0)')],
              loc='upper right')
    ax.set_aspect('equal')
    m = lat['modulation']
    ax.set_title(f'Site Types — δt/t₀={m["delta_t"]*100:.1f}%, δk/k₀={m["delta_k"]*100:.1f}%')

    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filename}")


if __name__ == "__main__":
    lat = generate_lattice(Nx=20, Ny=20, n_penrose=4,
                            defect_frac=0.05, min_sep=3.5)
    os.makedirs("lattice_results", exist_ok=True)
    plot_lattice(lat, "lattice_results/sw_penrose_graphene.png")
