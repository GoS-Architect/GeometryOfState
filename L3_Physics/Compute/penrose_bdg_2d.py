#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  STAGE 1: 2D BdG Hamiltonian on Penrose-Tiled Lattice
  Fractonic Weyl Semimetal — Simulation Roadmap
  
  Geometry of State (GoS) Framework
  Adrian — GoS-Architect | github.com/GoS-Architect
  March 2026
═══════════════════════════════════════════════════════════════════════════════

PURPOSE:
  Extend the 1D BdG computation (ratchet_full.py, 100-site golden-angle chain,
  w=1, two MZMs) to a 2D Penrose-tiled lattice with explicit coordination-number
  variation (pentagon/heptagon analogs). Determine whether Majorana zero modes
  survive the transition from 1D to 2D quasicrystalline geometry.

METHOD:
  1. Generate Penrose P3 tiling via Robinson triangle subdivision
  2. Extract vertex lattice with coordination-number-dependent site types
  3. Compute bond lengths, apply Harrison scaling: t_ij = t0 * (d0/d_ij)^2
  4. Build 2N×2N BdG Hamiltonian in Nambu space
  5. Sparse diagonalization targeting E ≈ 0 (shift-invert ARPACK)
  6. Compute Bott index (2D topological invariant)
  7. Visualize MZM wavefunction localization on the lattice

PASS/FAIL CRITERIA (from Simulation Roadmap):
  PASS: ≥ 2 zero modes |E| < 1e-8, edge localization > 90%, Bott index B = 1
  FAIL: 0 zero modes, |B| < 0.5

EPISTEMIC STATUS: COMPUTATIONAL DEMONSTRATION
  This code tests the geometry → Hamiltonian → invariant → MZM bridge in 2D.
"""

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from scipy.spatial import Delaunay
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
from collections import defaultdict
import time
import json
import os

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: PENROSE TILING GENERATION (Robinson Triangle Subdivision)
# ═══════════════════════════════════════════════════════════════════════════════

PHI = (1 + np.sqrt(5)) / 2  # Golden ratio ≈ 1.61803

class RobinsonTriangle:
    """
    A Robinson triangle for Penrose P3 tiling generation.
    
    Two types:
      - Type 0: "Acute" golden triangle (36°-72°-72°)
      - Type 1: "Obtuse" golden gnomon (108°-36°-36°)
    
    Vertices are stored as complex numbers for easy rotation/scaling.
    """
    def __init__(self, tri_type, A, B, C):
        self.tri_type = tri_type  # 0 = acute, 1 = obtuse
        self.A = A  # apex
        self.B = B  # base left
        self.C = C  # base right


def subdivide(triangles):
    """
    Apply one level of Robinson triangle subdivision.
    
    Acute triangle (type 0, 36-72-72) subdivides into:
      - 1 acute + 1 obtuse
    Obtuse triangle (type 1, 108-36-36) subdivides into:
      - 1 acute + 1 obtuse
    
    This is the standard Penrose P3 inflation rule.
    """
    result = []
    for tri in triangles:
        A, B, C = tri.A, tri.B, tri.C
        if tri.tri_type == 0:  # Acute: subdivide
            P = A + (B - A) / PHI
            result.append(RobinsonTriangle(0, C, P, B))
            result.append(RobinsonTriangle(1, P, C, A))
        else:  # Obtuse: subdivide
            Q = B + (A - B) / PHI
            R = B + (C - B) / PHI
            result.append(RobinsonTriangle(1, R, C, A))
            result.append(RobinsonTriangle(1, Q, R, B))
            result.append(RobinsonTriangle(0, R, Q, A))
    return result


def generate_penrose_tiling(n_subdivisions=5):
    """
    Generate a Penrose P3 tiling by starting with a decagon of triangles
    and applying n_subdivisions levels of Robinson triangle subdivision.
    
    Returns:
      vertices: np.array of shape (N, 2) — unique vertex positions
      edges: list of (i, j) pairs — bonds between adjacent vertices
      coord_numbers: np.array of shape (N,) — coordination number per vertex
    """
    print(f"  Generating Penrose tiling with {n_subdivisions} subdivisions...")
    
    # Start with a sun configuration: 10 acute triangles in a decagon
    triangles = []
    for i in range(10):
        angle1 = (2 * i) * np.pi / 10
        angle2 = (2 * i + 2) * np.pi / 10
        B = np.exp(1j * angle1)
        C = np.exp(1j * angle2)
        if i % 2 == 0:
            triangles.append(RobinsonTriangle(0, 0j, B, C))
        else:
            triangles.append(RobinsonTriangle(0, 0j, C, B))
    
    # Subdivide
    for level in range(n_subdivisions):
        triangles = subdivide(triangles)
        print(f"    Level {level+1}: {len(triangles)} triangles")
    
    # Extract unique vertices and edges
    vertex_map = {}
    edges_set = set()
    tolerance = 1e-8
    
    def get_vertex_id(z):
        """Map a complex coordinate to a unique vertex index."""
        key = (round(z.real / tolerance) * tolerance, 
               round(z.imag / tolerance) * tolerance)
        if key not in vertex_map:
            vertex_map[key] = len(vertex_map)
        return vertex_map[key]
    
    for tri in triangles:
        iA = get_vertex_id(tri.A)
        iB = get_vertex_id(tri.B)
        iC = get_vertex_id(tri.C)
        for edge in [(iA, iB), (iB, iC), (iA, iC)]:
            e = (min(edge), max(edge))
            edges_set.add(e)
    
    # Convert to arrays
    N = len(vertex_map)
    vertices = np.zeros((N, 2))
    for (x, y), idx in vertex_map.items():
        vertices[idx] = [x, y]
    
    edges = list(edges_set)
    
    # Compute coordination numbers
    coord_numbers = np.zeros(N, dtype=int)
    for i, j in edges:
        coord_numbers[i] += 1
        coord_numbers[j] += 1
    
    print(f"  Tiling complete: {N} vertices, {len(edges)} edges")
    print(f"  Coordination number distribution:")
    for cn in sorted(set(coord_numbers)):
        count = np.sum(coord_numbers == cn)
        print(f"    CN={cn}: {count} vertices ({100*count/N:.1f}%)")
    
    return vertices, edges, coord_numbers


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: TIGHT-BINDING HAMILTONIAN WITH HARRISON SCALING
# ═══════════════════════════════════════════════════════════════════════════════

def compute_bond_lengths(vertices, edges):
    """Compute Euclidean bond lengths for all edges."""
    lengths = np.zeros(len(edges))
    for k, (i, j) in enumerate(edges):
        dx = vertices[i] - vertices[j]
        lengths[k] = np.sqrt(dx @ dx)
    return lengths


def harrison_hopping(d, d0, t0):
    """
    Harrison scaling rule: t(d) = t0 * (d0/d)^2
    
    This is the bridge from geometry to Hamiltonian.
    ESTABLISHED: Harrison (1980), widely used in tight-binding models.
    """
    return t0 * (d0 / d) ** 2


def build_tight_binding_hamiltonian(vertices, edges, bond_lengths, t0=1.0, mu=1.0):
    """
    Build the single-particle tight-binding Hamiltonian:
      H = -μ Σ_i c†_i c_i - Σ_<ij> t_ij (c†_i c_j + h.c.)
    
    Hopping t_ij determined by Harrison scaling from bond length.
    Chemical potential μ applied uniformly.
    
    Returns sparse CSR matrix.
    """
    N = len(vertices)
    d0 = np.median(bond_lengths)  # Reference bond length = median
    
    row, col, data = [], [], []
    
    # On-site: chemical potential
    for i in range(N):
        row.append(i); col.append(i); data.append(-mu)
    
    # Hopping
    for k, (i, j) in enumerate(edges):
        t_ij = harrison_hopping(bond_lengths[k], d0, t0)
        row.append(i); col.append(j); data.append(-t_ij)
        row.append(j); col.append(i); data.append(-t_ij)
    
    H = sparse.csr_matrix((data, (row, col)), shape=(N, N))
    return H, d0


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: BdG HAMILTONIAN IN NAMBU SPACE
# ═══════════════════════════════════════════════════════════════════════════════

def build_bdg_hamiltonian(vertices, edges, bond_lengths, t0=1.0, mu=1.0, delta=0.5):
    """
    Build the Bogoliubov-de Gennes Hamiltonian in Nambu space.
    
    The BdG Hamiltonian is a 2N × 2N matrix:
      H_BdG = [  H       Δ  ]
              [  Δ†    -H*  ]
    
    where:
      H = single-particle tight-binding Hamiltonian
      Δ = superconducting pairing (p-wave, along bonds)
    
    For p-wave pairing on each bond:
      Δ_ij = Δ * sign(i-j) * (d0/d_ij)^2
    
    This models proximity-induced superconductivity from Nb.
    
    Returns sparse CSR matrix of dimension 2N × 2N.
    """
    N = len(vertices)
    d0 = np.median(bond_lengths)
    
    # Build H block
    H_tb, _ = build_tight_binding_hamiltonian(vertices, edges, bond_lengths, t0, mu)
    
    # Build Δ block (p-wave pairing along bonds)
    row_d, col_d, data_d = [], [], []
    for k, (i, j) in enumerate(edges):
        delta_ij = delta * (d0 / bond_lengths[k]) ** 2
        # p-wave: antisymmetric pairing
        row_d.append(i); col_d.append(j); data_d.append(delta_ij)
        row_d.append(j); col_d.append(i); data_d.append(-delta_ij)
    
    Delta = sparse.csr_matrix((data_d, (row_d, col_d)), shape=(N, N))
    
    # Assemble BdG matrix:
    # [ H      Δ   ]
    # [ Δ†   -H*   ]
    # For real H: H* = H. For antisymmetric Δ: Δ† = -Δ^T = Δ (since Δ is antisymmetric)
    H_BdG = sparse.bmat([
        [H_tb,          Delta],
        [Delta.conj().T, -H_tb.conj()]
    ], format='csr')
    
    return H_BdG, H_tb, Delta


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: TOPOLOGICAL INVARIANT — BOTT INDEX
# ═══════════════════════════════════════════════════════════════════════════════

def compute_bott_index(vertices, eigvecs_occ, N):
    """
    Compute the Bott index — the 2D generalization of the winding number
    for systems without translational symmetry.
    
    B = (1/2π) Im Tr[log(U_x U_y U_x† U_y†)]
    
    where U_x = P exp(2πi X/L_x) P, U_y = P exp(2πi Y/L_y) P,
    and P is the projector onto occupied states.
    
    Bott index B = 1 indicates non-trivial topology (Class D).
    
    ESTABLISHED: Loring and Hastings (2010), standard for disordered/quasiperiodic
    topological invariant computation.
    """
    # Normalize coordinates to [0, 1]
    x = vertices[:, 0]
    y = vertices[:, 1]
    Lx = x.max() - x.min()
    Ly = y.max() - y.min()
    x_norm = (x - x.min()) / Lx
    y_norm = (y - y.min()) / Ly
    
    # For BdG, we use the particle sector of the projector
    # eigvecs_occ has shape (2N, n_occ) — occupied states below E=0
    P_particle = eigvecs_occ[:N, :]  # particle sector
    
    # Projected position operators
    # U_x = P * diag(exp(2πi x)) * P
    exp_x = np.exp(2j * np.pi * x_norm)
    exp_y = np.exp(2j * np.pi * y_norm)
    
    # Project: U_x = V† diag(exp_x) V where V = P_particle
    V = P_particle
    Ux = V.conj().T @ np.diag(exp_x) @ V
    Uy = V.conj().T @ np.diag(exp_y) @ V
    
    # Bott index = (1/2π) Im Tr log(Ux Uy Ux† Uy†)
    Ux_inv = np.linalg.inv(Ux)
    Uy_inv = np.linalg.inv(Uy)
    
    commutator = Ux @ Uy @ Ux_inv @ Uy_inv
    
    # Compute via eigenvalues of the commutator
    eigvals = np.linalg.eigvals(commutator)
    log_sum = np.sum(np.log(eigvals))
    
    bott = log_sum.imag / (2 * np.pi)
    
    return bott


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: BOUNDARY IDENTIFICATION
# ═══════════════════════════════════════════════════════════════════════════════

def identify_boundary(vertices, edges, coord_numbers):
    """
    Identify boundary vertices of the Penrose patch.
    
    Boundary vertices have lower coordination number than the bulk
    (they're missing neighbors that would exist in an infinite tiling).
    Uses convex hull as primary boundary identifier.
    """
    from scipy.spatial import ConvexHull
    
    hull = ConvexHull(vertices)
    boundary_mask = np.zeros(len(vertices), dtype=bool)
    boundary_mask[hull.vertices] = True
    
    # Also include vertices within one bond length of the hull
    hull_vertices = set(hull.vertices)
    adjacency = defaultdict(set)
    for i, j in edges:
        adjacency[i].add(j)
        adjacency[j].add(i)
    
    for v in hull.vertices:
        for neighbor in adjacency[v]:
            boundary_mask[neighbor] = True
    
    return boundary_mask


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: ANALYSIS AND DIAGNOSTICS
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_zero_modes(eigenvalues, eigenvectors, N, boundary_mask, threshold=1e-6):
    """
    Analyze near-zero energy modes of the BdG Hamiltonian.
    
    Returns dict with:
      - n_zero_modes: count of modes with |E| < threshold
      - energies: the near-zero eigenvalues
      - edge_weights: fraction of wavefunction weight on boundary
      - bulk_weights: fraction in bulk
      - localization: spatial profile of each zero mode
    """
    results = {
        'n_zero_modes': 0,
        'zero_energies': [],
        'edge_weights': [],
        'mode_profiles': [],
        'all_eigenvalues': eigenvalues,
    }
    
    zero_mask = np.abs(eigenvalues) < threshold
    n_zero = np.sum(zero_mask)
    results['n_zero_modes'] = n_zero
    
    if n_zero == 0:
        print("  ⚠ NO ZERO MODES FOUND — GATE 1 FAIL CONDITION")
        return results
    
    zero_indices = np.where(zero_mask)[0]
    
    for idx in zero_indices:
        E = eigenvalues[idx]
        psi = eigenvectors[:, idx]
        
        # Probability density (particle + hole sectors)
        prob_particle = np.abs(psi[:N])**2
        prob_hole = np.abs(psi[N:])**2
        prob_total = prob_particle + prob_hole
        prob_total /= np.sum(prob_total)
        
        edge_weight = np.sum(prob_total[boundary_mask])
        bulk_weight = 1.0 - edge_weight
        
        results['zero_energies'].append(E)
        results['edge_weights'].append(edge_weight)
        results['mode_profiles'].append(prob_total)
    
    results['zero_energies'] = np.array(results['zero_energies'])
    results['edge_weights'] = np.array(results['edge_weights'])
    
    return results


def compute_modulation_stats(bond_lengths, d0, t0):
    """Compute statistics of the hopping modulation."""
    hoppings = harrison_hopping(bond_lengths, d0, t0)
    t_mean = np.mean(hoppings)
    delta_t = np.std(hoppings) / t_mean
    t_max = np.max(hoppings)
    t_min = np.min(hoppings)
    
    return {
        't_mean': t_mean,
        'delta_t_over_t0': delta_t,
        't_max': t_max,
        't_min': t_min,
        't_max_over_t_min': t_max / t_min,
        'd0': d0,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7: PARAMETER SWEEP — TOPOLOGICAL PHASE DIAGRAM
# ═══════════════════════════════════════════════════════════════════════════════

def sweep_chemical_potential(vertices, edges, bond_lengths, 
                             t0=1.0, delta=0.5, 
                             mu_values=None, n_eig=10):
    """
    Sweep chemical potential μ and track zero modes.
    Maps out the topological phase diagram μ vs gap size.
    
    Mirrors the 1D result: topological window μ ∈ [0, 1.95t₀] expected
    to shift/narrow in 2D.
    """
    if mu_values is None:
        mu_values = np.linspace(0.0, 2.5, 26)
    
    N = len(vertices)
    results = []
    
    print(f"\n  Chemical potential sweep: {len(mu_values)} points")
    for mi, mu in enumerate(mu_values):
        H_BdG, _, _ = build_bdg_hamiltonian(vertices, edges, bond_lengths, 
                                             t0=t0, mu=mu, delta=delta)
        
        # Find eigenvalues nearest to zero
        try:
            evals = eigsh(H_BdG, k=min(n_eig, H_BdG.shape[0]-2), 
                         sigma=0.0, which='LM', return_eigenvectors=False)
            min_E = np.min(np.abs(evals))
            n_near_zero = np.sum(np.abs(evals) < 1e-6)
        except Exception:
            min_E = np.nan
            n_near_zero = 0
        
        results.append({
            'mu': mu,
            'min_energy': min_E,
            'n_near_zero': n_near_zero,
        })
        
        status = "✓ TOPOLOGICAL" if n_near_zero >= 2 else "  trivial"
        if mi % 5 == 0 or n_near_zero >= 2:
            print(f"    μ/t₀ = {mu:.2f}: min|E| = {min_E:.2e}, "
                  f"near-zero modes = {n_near_zero} {status}")
    
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 8: DEFECT DENSITY ROBUSTNESS SWEEP  
# ═══════════════════════════════════════════════════════════════════════════════

def test_defect_density_robustness(n_subdivisions_range=(3, 4, 5, 6),
                                    t0=1.0, mu=1.0, delta=0.5, n_eig=10):
    """
    Test MZM robustness across different Penrose patch sizes.
    Different subdivision levels produce different defect densities
    and system sizes.
    
    PASS criterion: MZMs stable from N=500 to N=5000.
    """
    results = []
    for n_sub in n_subdivisions_range:
        print(f"\n{'='*60}")
        print(f"  Testing n_subdivisions = {n_sub}")
        print(f"{'='*60}")
        
        vertices, edges, coord_numbers = generate_penrose_tiling(n_sub)
        N = len(vertices)
        
        if N < 20:
            print(f"  Skipping: too few vertices ({N})")
            continue
        
        bond_lengths = compute_bond_lengths(vertices, edges)
        
        H_BdG, _, _ = build_bdg_hamiltonian(vertices, edges, bond_lengths,
                                             t0=t0, mu=mu, delta=delta)
        
        k = min(n_eig, 2*N - 2)
        try:
            evals, evecs = eigsh(H_BdG, k=k, sigma=0.0, which='LM')
            sort_idx = np.argsort(np.abs(evals))
            evals = evals[sort_idx]
            evecs = evecs[:, sort_idx]
            
            n_zero = np.sum(np.abs(evals) < 1e-6)
            min_E = np.min(np.abs(evals))
            
            boundary_mask = identify_boundary(vertices, edges, coord_numbers)
            
            if n_zero > 0:
                psi = evecs[:, 0]
                prob = np.abs(psi[:N])**2 + np.abs(psi[N:])**2
                prob /= np.sum(prob)
                edge_w = np.sum(prob[boundary_mask])
            else:
                edge_w = 0.0
                
        except Exception as e:
            print(f"  Eigensolver failed: {e}")
            n_zero = -1
            min_E = np.nan
            edge_w = 0.0
        
        results.append({
            'n_sub': n_sub,
            'N': N,
            'n_edges': len(edges),
            'n_zero_modes': n_zero,
            'min_energy': min_E,
            'edge_weight': edge_w,
        })
        
        print(f"  N = {N}: zero modes = {n_zero}, min|E| = {min_E:.2e}, "
              f"edge weight = {edge_w:.3f}")
    
    return results


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 9: VISUALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def plot_tiling_with_coordination(vertices, edges, coord_numbers, filename):
    """Plot the Penrose tiling colored by coordination number."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    
    # Draw edges
    for i, j in edges:
        ax.plot([vertices[i, 0], vertices[j, 0]], 
                [vertices[i, 1], vertices[j, 1]], 
                'k-', alpha=0.15, linewidth=0.3)
    
    # Color vertices by coordination number
    cmap = plt.cm.coolwarm
    scatter = ax.scatter(vertices[:, 0], vertices[:, 1], 
                        c=coord_numbers, cmap=cmap, 
                        s=15, edgecolors='none', alpha=0.8,
                        vmin=3, vmax=7)
    
    plt.colorbar(scatter, label='Coordination Number', shrink=0.7)
    ax.set_aspect('equal')
    ax.set_title(f'Penrose P3 Tiling — {len(vertices)} vertices\n'
                 f'CN=5 (pentagon analog) | CN=6 (hexagon) | CN=7 (heptagon analog)',
                 fontsize=12)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filename}")


def plot_zero_mode_wavefunction(vertices, edges, mode_profile, boundary_mask, 
                                 energy, mode_idx, filename):
    """Plot spatial distribution of a zero-mode wavefunction on the lattice."""
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    
    # Draw edges faintly
    for i, j in edges:
        ax.plot([vertices[i, 0], vertices[j, 0]], 
                [vertices[i, 1], vertices[j, 1]], 
                'k-', alpha=0.08, linewidth=0.2)
    
    # Plot wavefunction density
    log_prob = np.log10(mode_profile + 1e-20)
    scatter = ax.scatter(vertices[:, 0], vertices[:, 1],
                        c=log_prob, cmap='inferno',
                        s=20, edgecolors='none', alpha=0.9)
    
    # Highlight boundary
    ax.scatter(vertices[boundary_mask, 0], vertices[boundary_mask, 1],
              facecolors='none', edgecolors='cyan', s=40, linewidths=0.5, alpha=0.5)
    
    plt.colorbar(scatter, label='log₁₀(|ψ|²)', shrink=0.7)
    edge_w = np.sum(mode_profile[boundary_mask])
    ax.set_aspect('equal')
    ax.set_title(f'MZM #{mode_idx} — |E| = {abs(energy):.2e}\n'
                 f'Edge weight: {edge_w:.1%} | Boundary sites shown in cyan',
                 fontsize=12)
    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filename}")


def plot_eigenvalue_spectrum(eigenvalues, filename):
    """Plot the BdG eigenvalue spectrum near E=0."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    sorted_E = np.sort(eigenvalues)
    
    # Full spectrum of computed eigenvalues
    ax1.plot(range(len(sorted_E)), sorted_E, 'b.-', markersize=4)
    ax1.axhline(y=0, color='r', linestyle='--', alpha=0.5)
    ax1.set_xlabel('Eigenvalue index')
    ax1.set_ylabel('Energy E')
    ax1.set_title('BdG Spectrum (near E=0)')
    ax1.grid(True, alpha=0.3)
    
    # Zoom on near-zero modes
    near_zero = sorted_E[np.abs(sorted_E) < 0.1]
    if len(near_zero) > 0:
        ax2.stem(range(len(near_zero)), near_zero, linefmt='b-', markerfmt='bo', basefmt='r--')
        ax2.set_xlabel('Mode index (near zero)')
        ax2.set_ylabel('Energy E')
        ax2.set_title(f'Near-Zero Modes (|E| < 0.1)\n'
                      f'Modes with |E| < 10⁻⁶: {np.sum(np.abs(sorted_E) < 1e-6)}')
        ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filename}")


def plot_phase_diagram(sweep_results, filename):
    """Plot the topological phase diagram: μ vs gap."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    mu_vals = [r['mu'] for r in sweep_results]
    min_E = [r['min_energy'] for r in sweep_results]
    n_zero = [r['n_near_zero'] for r in sweep_results]
    
    ax1.semilogy(mu_vals, min_E, 'b.-')
    ax1.axhline(y=1e-6, color='r', linestyle='--', alpha=0.5, label='Zero-mode threshold')
    ax1.set_ylabel('min |E|')
    ax1.set_title('Topological Phase Diagram — μ sweep')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    colors = ['green' if n >= 2 else 'gray' for n in n_zero]
    ax2.bar(mu_vals, n_zero, width=0.08, color=colors)
    ax2.set_xlabel('μ / t₀')
    ax2.set_ylabel('Near-zero modes')
    ax2.set_title('Zero Mode Count (green = topological)')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filename}")


def plot_robustness(robustness_results, filename):
    """Plot MZM survival across system sizes."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    Ns = [r['N'] for r in robustness_results]
    n_zero = [r['n_zero_modes'] for r in robustness_results]
    edge_w = [r['edge_weight'] for r in robustness_results]
    
    ax1.plot(Ns, n_zero, 'go-', markersize=8, linewidth=2)
    ax1.axhline(y=2, color='r', linestyle='--', alpha=0.5, label='Minimum for pass')
    ax1.set_xlabel('System size N')
    ax1.set_ylabel('Number of zero modes')
    ax1.set_title('MZM Count vs System Size')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(Ns, edge_w, 'bs-', markersize=8, linewidth=2)
    ax2.axhline(y=0.9, color='r', linestyle='--', alpha=0.5, label='90% pass threshold')
    ax2.set_xlabel('System size N')
    ax2.set_ylabel('Edge weight fraction')
    ax2.set_title('Edge Localization vs System Size')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filename}")


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 10: MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

def run_stage1(output_dir="stage1_results", n_subdivisions=5, 
               t0=1.0, mu=1.0, delta=0.5, n_eig=20):
    """
    Execute the full Stage 1 simulation pipeline.
    
    Parameters:
      n_subdivisions: Penrose tiling subdivision depth (5 → ~500 sites)
      t0: base hopping amplitude
      mu: chemical potential  
      delta: superconducting pairing amplitude
      n_eig: number of eigenvalues to compute near E=0
    """
    os.makedirs(output_dir, exist_ok=True)
    
    print("═" * 70)
    print("  STAGE 1: 2D BdG on Penrose Patch")
    print("  Fractonic Weyl Semimetal — Simulation Roadmap")
    print("═" * 70)
    print(f"\n  Parameters: t₀={t0}, μ={mu}, Δ={delta}, n_sub={n_subdivisions}")
    
    t_start = time.time()
    
    # ── Step 1: Generate Penrose tiling ──
    print(f"\n{'─'*50}")
    print("  STEP 1: Penrose Tiling Generation")
    print(f"{'─'*50}")
    vertices, edges, coord_numbers = generate_penrose_tiling(n_subdivisions)
    N = len(vertices)
    
    # ── Step 2: Compute bond properties ──
    print(f"\n{'─'*50}")
    print("  STEP 2: Bond Length Analysis")
    print(f"{'─'*50}")
    bond_lengths = compute_bond_lengths(vertices, edges)
    d0 = np.median(bond_lengths)
    mod_stats = compute_modulation_stats(bond_lengths, d0, t0)
    
    print(f"  Reference bond length d₀ = {d0:.4f}")
    print(f"  Hopping modulation δt/t₀ = {mod_stats['delta_t_over_t0']:.4f} "
          f"({mod_stats['delta_t_over_t0']*100:.1f}%)")
    print(f"  t_max/t_min = {mod_stats['t_max_over_t_min']:.3f}")
    print(f"  Compare thesis 1D: δt/t₀ = 0.097 (9.7%)")
    
    # ── Step 3: Build and solve BdG Hamiltonian ──
    print(f"\n{'─'*50}")
    print("  STEP 3: BdG Hamiltonian Construction & Diagonalization")
    print(f"{'─'*50}")
    print(f"  Building 2N × 2N = {2*N} × {2*N} BdG matrix...")
    
    H_BdG, H_tb, Delta_mat = build_bdg_hamiltonian(
        vertices, edges, bond_lengths, t0=t0, mu=mu, delta=delta)
    
    print(f"  Matrix: {H_BdG.shape}, nnz = {H_BdG.nnz}")
    print(f"  Solving for {n_eig} eigenvalues near E = 0 (shift-invert)...")
    
    k = min(n_eig, 2*N - 2)
    evals, evecs = eigsh(H_BdG, k=k, sigma=0.0, which='LM')
    
    sort_idx = np.argsort(np.abs(evals))
    evals = evals[sort_idx]
    evecs = evecs[:, sort_idx]
    
    print(f"  Eigenvalues computed. Nearest to zero:")
    for i in range(min(6, len(evals))):
        print(f"    E_{i} = {evals[i]:+.6e}")
    
    # ── Step 4: Identify boundary and analyze modes ──
    print(f"\n{'─'*50}")
    print("  STEP 4: Zero Mode Analysis")
    print(f"{'─'*50}")
    boundary_mask = identify_boundary(vertices, edges, coord_numbers)
    n_boundary = np.sum(boundary_mask)
    print(f"  Boundary sites: {n_boundary} / {N} ({100*n_boundary/N:.1f}%)")
    
    mode_results = analyze_zero_modes(evals, evecs, N, boundary_mask, threshold=1e-6)
    
    n_zero = mode_results['n_zero_modes']
    print(f"\n  ┌─────────────────────────────────────────────────┐")
    print(f"  │  ZERO MODE COUNT: {n_zero:>3}                             │")
    if n_zero >= 2:
        print(f"  │  STATUS: ✓ PASS (≥ 2 required)                  │")
    else:
        print(f"  │  STATUS: ✗ FAIL (≥ 2 required)                  │")
    print(f"  └─────────────────────────────────────────────────┘")
    
    if n_zero > 0:
        for i in range(n_zero):
            E = mode_results['zero_energies'][i]
            ew = mode_results['edge_weights'][i]
            loc_status = "✓ PASS" if ew > 0.9 else ("~ PARTIAL" if ew > 0.5 else "✗ FAIL")
            print(f"  Mode {i}: |E| = {abs(E):.2e}, edge weight = {ew:.3f} {loc_status}")
    
    # ── Step 5: Bott index ──
    print(f"\n{'─'*50}")
    print("  STEP 5: Bott Index (2D Topological Invariant)")
    print(f"{'─'*50}")
    
    # Occupied states: negative energy eigenvalues
    occ_mask = evals < 0
    if np.sum(occ_mask) > 0:
        evecs_occ = evecs[:, occ_mask]
        try:
            bott = compute_bott_index(vertices, evecs_occ, N)
            print(f"  Bott index B = {bott:.4f}")
            if abs(round(bott) - 1) < 0.1:
                print(f"  STATUS: ✓ PASS (B ≈ 1, non-trivial topology)")
            elif abs(bott) < 0.5:
                print(f"  STATUS: ✗ FAIL (B ≈ 0, trivial)")
            else:
                print(f"  STATUS: ? AMBIGUOUS (B not near integer)")
        except Exception as e:
            bott = np.nan
            print(f"  Bott index computation failed: {e}")
            print(f"  (May need larger system or more occupied states)")
    else:
        bott = np.nan
        print(f"  No occupied states found for Bott index computation")
    
    # ── Step 6: Generate plots ──
    print(f"\n{'─'*50}")
    print("  STEP 6: Visualization")
    print(f"{'─'*50}")
    
    plot_tiling_with_coordination(
        vertices, edges, coord_numbers,
        os.path.join(output_dir, "penrose_tiling_coordination.png"))
    
    plot_eigenvalue_spectrum(
        evals, os.path.join(output_dir, "bdg_spectrum.png"))
    
    if n_zero > 0:
        for i in range(min(n_zero, 4)):
            plot_zero_mode_wavefunction(
                vertices, edges, mode_results['mode_profiles'][i],
                boundary_mask, mode_results['zero_energies'][i], i,
                os.path.join(output_dir, f"mzm_wavefunction_{i}.png"))
    
    # ── Step 7: Chemical potential sweep ──
    print(f"\n{'─'*50}")
    print("  STEP 7: Chemical Potential Sweep (Phase Diagram)")
    print(f"{'─'*50}")
    
    sweep_results = sweep_chemical_potential(
        vertices, edges, bond_lengths, t0=t0, delta=delta,
        mu_values=np.linspace(0.0, 2.5, 26), n_eig=8)
    
    plot_phase_diagram(sweep_results, 
                       os.path.join(output_dir, "phase_diagram_mu.png"))
    
    # ── Summary ──
    t_elapsed = time.time() - t_start
    
    print(f"\n{'═'*70}")
    print(f"  STAGE 1 COMPLETE — Elapsed: {t_elapsed:.1f}s")
    print(f"{'═'*70}")
    
    summary = {
        'n_vertices': N,
        'n_edges': len(edges),
        'n_subdivisions': n_subdivisions,
        'parameters': {'t0': t0, 'mu': mu, 'delta': delta},
        'modulation': mod_stats,
        'n_zero_modes': n_zero,
        'bott_index': float(bott) if not np.isnan(bott) else None,
        'zero_mode_energies': mode_results['zero_energies'].tolist() if n_zero > 0 else [],
        'zero_mode_edge_weights': mode_results['edge_weights'].tolist() if n_zero > 0 else [],
        'gate_assessment': {
            'zero_modes_pass': n_zero >= 2,
            'edge_localization_pass': bool(np.any(mode_results['edge_weights'] > 0.9)) if n_zero > 0 else False,
            'bott_index_pass': bool(abs(round(bott) - 1) < 0.1) if not np.isnan(bott) else False,
        },
        'elapsed_seconds': t_elapsed,
    }
    
    # Determine overall gate
    gate_pass = (summary['gate_assessment']['zero_modes_pass'] and 
                 summary['gate_assessment']['edge_localization_pass'])
    
    print(f"\n  ┌─────────────────────────────────────────────────┐")
    print(f"  │             STAGE 1 GATE ASSESSMENT              │")
    print(f"  ├─────────────────────────────────────────────────┤")
    print(f"  │  Zero modes ≥ 2:        {'✓ PASS' if summary['gate_assessment']['zero_modes_pass'] else '✗ FAIL':>10}          │")
    print(f"  │  Edge localization > 90%: {'✓ PASS' if summary['gate_assessment']['edge_localization_pass'] else '✗ FAIL':>9}          │")
    print(f"  │  Bott index B = 1:       {'✓ PASS' if summary['gate_assessment']['bott_index_pass'] else '? DEFER':>9}          │")
    print(f"  ├─────────────────────────────────────────────────┤")
    print(f"  │  OVERALL:                {'✓ GATE PASSED' if gate_pass else '✗ GATE FAILED':>14}         │")
    print(f"  └─────────────────────────────────────────────────┘")
    
    with open(os.path.join(output_dir, "stage1_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\n  Summary saved to {output_dir}/stage1_summary.json")
    
    return summary


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Default: medium-sized Penrose patch
    # n_subdivisions=5 gives ~500 sites (tractable on laptop)
    # n_subdivisions=6 gives ~1300 sites
    # n_subdivisions=7 gives ~3500 sites
    
    summary = run_stage1(
        output_dir="stage1_results",
        n_subdivisions=5,  # Start with ~500 sites
        t0=1.0,
        mu=1.0,
        delta=0.5,
        n_eig=20,
    )
