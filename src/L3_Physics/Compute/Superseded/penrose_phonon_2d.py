#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  STAGE 2: 2D Phonon Transport on Penrose-Tiled Lattice
  Fractonic Weyl Semimetal — Simulation Roadmap
  
  Geometry of State (GoS) Framework
  Adrian — GoS-Architect | github.com/GoS-Architect
  March 2026
═══════════════════════════════════════════════════════════════════════════════

PURPOSE:
  Compute phonon spectrum and thermal transport on the same 2D Penrose lattice
  used in Stage 1. Validate the PGTC (Phonon Glass Topological Crystal) self-
  protection principle: the same quasiperiodic geometry that hosts MZMs also
  suppresses phonon transport.

KEY COMPARISON (from thesis):
  1D result: κ_QP/κ_ord ≈ 0.84–0.86 (14–16% reduction)
  2D prediction: κ_QP/κ_ord < 0.5 (strong suppression)
  
  Electron modulation: δt/t₀ = 9.7%  (Harrison d⁻² scaling)
  Phonon modulation:   δk/k₀ = 19.3% (spring constant d⁻⁴ scaling)

PASS/FAIL CRITERIA:
  PASS: κ_QP/κ_ord < 0.5, ξ_phonon < ξ_MZM by ≥ 2×
  FAIL: κ_QP/κ_ord > 0.8 (no improvement over 1D)

EPISTEMIC STATUS: COMPUTATIONAL DEMONSTRATION
"""

import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigsh
from scipy.linalg import eigh
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import json
import time

# Import the Penrose tiling generator from Stage 1
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from penrose_bdg_2d import (generate_penrose_tiling, compute_bond_lengths, 
                             harrison_hopping, PHI)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: PHONON DYNAMICAL MATRIX
# ═══════════════════════════════════════════════════════════════════════════════

def spring_constant(d, d0, k0):
    """
    Spring constant scaling: k(d) = k₀ × (d₀/d)⁴
    
    This is the STEEPER scaling compared to Harrison hopping (d⁻²).
    For the same geometric modulation, phonons feel 2× the effective
    disorder that electrons do. This asymmetry is the PGTC mechanism.
    
    ESTABLISHED: Bond-stretching force constants scale as d⁻⁴ in 
    Keating-type models (Keating 1966, widely used in semiconductor physics).
    """
    return k0 * (d0 / d) ** 4


def build_dynamical_matrix_scalar(vertices, edges, bond_lengths, k0=1.0):
    """
    Build the scalar (1D displacement) dynamical matrix.
    
    D_ii = Σ_j k_ij  (diagonal: sum of spring constants to neighbors)
    D_ij = -k_ij     (off-diagonal: negative spring constant)
    
    This is the phonon analog of the tight-binding Hamiltonian.
    Eigenvalues ω² give phonon frequencies; eigenvectors give mode shapes.
    
    Returns:
      D_qp: dynamical matrix for quasiperiodic lattice
      D_ord: dynamical matrix for comparison ordered lattice (uniform springs)
      d0: reference bond length
    """
    N = len(vertices)
    d0 = np.median(bond_lengths)
    
    # Quasiperiodic dynamical matrix
    row, col, data = [], [], []
    diagonal = np.zeros(N)
    
    for idx, (i, j) in enumerate(edges):
        k_ij = spring_constant(bond_lengths[idx], d0, k0)
        row.append(i); col.append(j); data.append(-k_ij)
        row.append(j); col.append(i); data.append(-k_ij)
        diagonal[i] += k_ij
        diagonal[j] += k_ij
    
    for i in range(N):
        row.append(i); col.append(i); data.append(diagonal[i])
    
    D_qp = sparse.csr_matrix((data, (row, col)), shape=(N, N))
    
    # Ordered comparison: uniform spring constant k₀
    row_o, col_o, data_o = [], [], []
    diagonal_o = np.zeros(N)
    
    for idx, (i, j) in enumerate(edges):
        row_o.append(i); col_o.append(j); data_o.append(-k0)
        row_o.append(j); col_o.append(i); data_o.append(-k0)
        diagonal_o[i] += k0
        diagonal_o[j] += k0
    
    for i in range(N):
        row_o.append(i); col_o.append(i); data_o.append(diagonal_o[i])
    
    D_ord = sparse.csr_matrix((data_o, (row_o, col_o)), shape=(N, N))
    
    return D_qp, D_ord, d0


def build_dynamical_matrix_2d(vertices, edges, bond_lengths, k0=1.0):
    """
    Build the full 2D vector dynamical matrix (2N × 2N).
    
    Each atom has x and y displacements. The force on atom i due to 
    displacement of atom j depends on the bond direction.
    
    D^(αβ)_ij = -k_ij * n^α_ij * n^β_ij  (off-diagonal)
    D^(αβ)_ii = Σ_j k_ij * n^α_ij * n^β_ij  (diagonal)
    
    where n_ij is the unit vector along bond i→j, and α,β ∈ {x,y}.
    """
    N = len(vertices)
    d0 = np.median(bond_lengths)
    size = 2 * N
    
    row, col, data = [], [], []
    diagonal = np.zeros((N, 2, 2))
    
    for idx, (i, j) in enumerate(edges):
        k_ij = spring_constant(bond_lengths[idx], d0, k0)
        
        # Bond direction unit vector
        dr = vertices[j] - vertices[i]
        d_len = bond_lengths[idx]
        n = dr / d_len
        
        # Dyadic product n ⊗ n
        for a in range(2):
            for b in range(2):
                val = -k_ij * n[a] * n[b]
                # i→j block
                row.append(2*i + a); col.append(2*j + b); data.append(val)
                # j→i block (symmetric)
                row.append(2*j + a); col.append(2*i + b); data.append(val)
                # Diagonal accumulation
                diagonal[i, a, b] += k_ij * n[a] * n[b]
                diagonal[j, a, b] += k_ij * n[a] * n[b]
    
    # Add diagonal blocks
    for i in range(N):
        for a in range(2):
            for b in range(2):
                row.append(2*i + a); col.append(2*i + b)
                data.append(diagonal[i, a, b])
    
    D_qp = sparse.csr_matrix((data, (row, col)), shape=(size, size))
    
    # Ordered comparison
    row_o, col_o, data_o = [], [], []
    diagonal_o = np.zeros((N, 2, 2))
    
    for idx, (i, j) in enumerate(edges):
        dr = vertices[j] - vertices[i]
        d_len = bond_lengths[idx]
        n = dr / d_len
        
        for a in range(2):
            for b in range(2):
                val = -k0 * n[a] * n[b]
                row_o.append(2*i + a); col_o.append(2*j + b); data_o.append(val)
                row_o.append(2*j + a); col_o.append(2*i + b); data_o.append(val)
                diagonal_o[i, a, b] += k0 * n[a] * n[b]
                diagonal_o[j, a, b] += k0 * n[a] * n[b]
    
    for i in range(N):
        for a in range(2):
            for b in range(2):
                row_o.append(2*i + a); col_o.append(2*i + b)
                data_o.append(diagonal_o[i, a, b])
    
    D_ord = sparse.csr_matrix((data_o, (row_o, col_o)), shape=(size, size))
    
    return D_qp, D_ord, d0


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: PHONON ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def compute_phonon_spectrum(D, label=""):
    """
    Diagonalize the dynamical matrix to get phonon frequencies and modes.
    
    ω² = eigenvalues of D (should be ≥ 0 for stable lattice)
    """
    D_dense = D.toarray()
    eigenvalues, eigenvectors = eigh(D_dense)
    
    # Clean up tiny negative eigenvalues (numerical noise)
    eigenvalues = np.maximum(eigenvalues, 0)
    frequencies = np.sqrt(eigenvalues)
    
    n_zero = np.sum(eigenvalues < 1e-10)
    print(f"  {label}: {len(eigenvalues)} modes, "
          f"{n_zero} zero modes (acoustic/rigid), "
          f"ω_max = {frequencies[-1]:.4f}")
    
    return frequencies, eigenvectors


def compute_participation_ratio(eigenvectors, N):
    """
    Compute the inverse participation ratio (IPR) for each mode.
    
    IPR = 1 / (N × Σ_i |ψ_i|⁴)
    
    IPR ≈ 1 → fully extended (plane wave)
    IPR ≈ 1/N → fully localized (single site)
    
    This is the primary diagnostic for phonon localization.
    """
    prob = np.abs(eigenvectors) ** 2
    # Normalize each mode
    norms = np.sum(prob, axis=0)
    prob = prob / norms[np.newaxis, :]
    
    ipr = 1.0 / (N * np.sum(prob ** 2, axis=0))
    
    return ipr


def compute_localization_length(eigenvectors, vertices, N):
    """
    Compute the localization length ξ for each mode.
    
    ξ² = Σ_i |ψ_i|² × |r_i - r_cm|²
    
    where r_cm = Σ_i |ψ_i|² r_i is the center of mass of the mode.
    
    ξ/L → 0: localized
    ξ/L → 1/√12 ≈ 0.29: uniformly distributed
    """
    # For scalar modes, vertices positions are direct
    # For 2D vector modes, we need to handle the 2N case
    if eigenvectors.shape[0] == N:
        pos = vertices
    else:
        # 2N vector case: combine x,y components per atom
        prob_atoms = np.zeros((N, eigenvectors.shape[1]))
        for i in range(N):
            prob_atoms[i] = np.abs(eigenvectors[2*i])**2 + np.abs(eigenvectors[2*i+1])**2
        prob = prob_atoms
        pos = vertices
        norms = np.sum(prob, axis=0)
        prob = prob / norms[np.newaxis, :]
        
        xi = np.zeros(eigenvectors.shape[1])
        for m in range(eigenvectors.shape[1]):
            r_cm = np.sum(prob[:, m:m+1] * pos, axis=0)
            dr = pos - r_cm[np.newaxis, :]
            xi[m] = np.sqrt(np.sum(prob[:, m] * np.sum(dr**2, axis=1)))
        
        return xi
    
    prob = np.abs(eigenvectors) ** 2
    norms = np.sum(prob, axis=0)
    prob = prob / norms[np.newaxis, :]
    
    xi = np.zeros(eigenvectors.shape[1])
    for m in range(eigenvectors.shape[1]):
        r_cm = np.sum(prob[:, m:m+1] * pos, axis=0)
        dr = pos - r_cm[np.newaxis, :]
        xi[m] = np.sqrt(np.sum(prob[:, m] * np.sum(dr**2, axis=1)))
    
    return xi


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: THERMAL CONDUCTIVITY (Allen-Feldman Method)
# ═══════════════════════════════════════════════════════════════════════════════

def allen_feldman_thermal_conductivity(frequencies, eigenvectors, D, T, 
                                        broadening=0.02):
    """
    Compute thermal conductivity using the Allen-Feldman method.
    
    κ = (1/V) Σ_n C(ω_n, T) × D_n
    
    where C(ω,T) is the mode heat capacity and D_n is the mode diffusivity:
      D_n = (π/ω_n²) Σ_{m≠n} |S_nm|² δ(ω_n - ω_m)
      S_nm = <n|∂D/∂r|m> (heat current matrix element)
    
    The Allen-Feldman method is designed for disordered/amorphous systems
    where the Boltzmann transport equation breaks down — exactly our case.
    
    ESTABLISHED: Allen and Feldman (1993), standard for amorphous thermal
    conductivity.
    """
    N_modes = len(frequencies)
    kB = 1.0  # Working in natural units
    
    # Mode heat capacities (quantum, Bose-Einstein)
    C = np.zeros(N_modes)
    for n in range(N_modes):
        if frequencies[n] > 1e-10:
            x = frequencies[n] / (kB * T)
            if x < 500:  # Avoid overflow
                ex = np.exp(x)
                C[n] = kB * x**2 * ex / (ex - 1)**2
    
    # Mode diffusivities via Lorentzian-broadened Allen-Feldman formula
    # For computational efficiency, we use the off-diagonal elements of D
    # in the eigenmode basis
    
    # S_nm = Σ_i e_n(i) × D_ij × e_m(j) for i≠j → this is just the 
    # off-diagonal of D in the eigenbasis
    D_dense = D.toarray()
    D_eigen = eigenvectors.T @ D_dense @ eigenvectors
    
    # Mode diffusivities
    diff = np.zeros(N_modes)
    for n in range(N_modes):
        if frequencies[n] < 1e-10:
            continue
        for m in range(N_modes):
            if m == n or frequencies[m] < 1e-10:
                continue
            # Lorentzian delta function
            dw = frequencies[n] - frequencies[m]
            lorentz = broadening / (np.pi * (dw**2 + broadening**2))
            diff[n] += np.abs(D_eigen[n, m])**2 * lorentz
        diff[n] *= np.pi / (frequencies[n]**2) if frequencies[n] > 1e-10 else 0
    
    # Total thermal conductivity (in arbitrary units — ratio is what matters)
    kappa = np.sum(C * diff)
    
    return kappa, C, diff


def simple_thermal_conductivity_proxy(frequencies, eigenvectors, N, T_values):
    """
    Simplified thermal conductivity proxy based on mode participation.
    
    κ_proxy(T) = Σ_n C(ω_n, T) × PR_n × v²_n
    
    where PR_n is the participation ratio (proxy for diffusivity)
    and v_n ∝ ω_n (group velocity proxy for acoustic-like modes).
    
    This is faster than full Allen-Feldman and captures the essential
    physics: localized modes don't transport heat.
    """
    ipr = compute_participation_ratio(eigenvectors, N)
    kB = 1.0
    
    kappa_vs_T = []
    for T in T_values:
        kappa = 0.0
        for n in range(len(frequencies)):
            if frequencies[n] < 1e-10:
                continue
            # Bose-Einstein heat capacity
            x = frequencies[n] / (kB * T)
            if x < 500:
                ex = np.exp(x)
                C_n = kB * x**2 * ex / (ex - 1)**2
            else:
                C_n = 0.0
            # Transport weight: participation × group velocity proxy
            v_proxy = frequencies[n]  # ∝ ω for acoustic modes
            kappa += C_n * ipr[n] * v_proxy**2
        kappa_vs_T.append(kappa)
    
    return np.array(kappa_vs_T)


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: SPRING CONSTANT MODULATION ANALYSIS
# ═══════════════════════════════════════════════════════════════════════════════

def analyze_modulation(bond_lengths, d0, k0=1.0, t0=1.0):
    """
    Compare electron vs phonon modulation from the same geometry.
    
    This quantifies the PGTC differential localization mechanism.
    """
    # Electron hopping modulation
    t_vals = harrison_hopping(bond_lengths, d0, t0)
    t_mean = np.mean(t_vals)
    delta_t = np.std(t_vals) / t_mean
    
    # Phonon spring constant modulation  
    k_vals = spring_constant(bond_lengths, d0, k0)
    k_mean = np.mean(k_vals)
    delta_k = np.std(k_vals) / k_mean
    
    return {
        'electron_modulation': delta_t,
        'phonon_modulation': delta_k,
        'ratio': delta_k / delta_t,
        't_mean': t_mean, 't_std': np.std(t_vals),
        'k_mean': k_mean, 'k_std': np.std(k_vals),
        'bond_length_std': np.std(bond_lengths) / d0,
    }


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: VISUALIZATION
# ═══════════════════════════════════════════════════════════════════════════════

def plot_phonon_dos(freq_qp, freq_ord, filename):
    """Plot phonon density of states: quasiperiodic vs ordered."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bins = np.linspace(0, max(freq_qp.max(), freq_ord.max()) * 1.05, 100)
    
    ax.hist(freq_qp, bins=bins, alpha=0.6, density=True, 
            label='Quasiperiodic (Penrose)', color='red')
    ax.hist(freq_ord, bins=bins, alpha=0.6, density=True,
            label='Ordered (uniform k)', color='blue')
    
    ax.set_xlabel('Frequency ω')
    ax.set_ylabel('Density of States g(ω)')
    ax.set_title('Phonon DOS: Quasiperiodic vs Ordered')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filename}")


def plot_participation_ratios(freq_qp, ipr_qp, freq_ord, ipr_ord, filename):
    """Plot participation ratios vs frequency."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.scatter(freq_ord, ipr_ord, s=5, alpha=0.4, c='blue', label='Ordered')
    ax.scatter(freq_qp, ipr_qp, s=5, alpha=0.4, c='red', label='Quasiperiodic')
    
    ax.axhline(y=1.0, color='k', linestyle='--', alpha=0.3, label='Fully extended')
    ax.axhline(y=0.1, color='gray', linestyle=':', alpha=0.3)
    
    ax.set_xlabel('Frequency ω')
    ax.set_ylabel('Participation Ratio (IPR)')
    ax.set_title('Mode Localization: Quasiperiodic vs Ordered\n'
                 'Lower IPR = more localized')
    ax.set_ylim(0, 1.2)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filename}")


def plot_localization_lengths(freq_qp, xi_qp, freq_ord, xi_ord, L, filename):
    """Plot localization lengths vs frequency."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    ax.scatter(freq_ord, xi_ord / L, s=5, alpha=0.4, c='blue', label='Ordered')
    ax.scatter(freq_qp, xi_qp / L, s=5, alpha=0.4, c='red', label='Quasiperiodic')
    
    ax.axhline(y=0.29, color='k', linestyle='--', alpha=0.3, 
               label='Uniform distribution (1/√12)')
    ax.axhline(y=0.05, color='green', linestyle=':', alpha=0.5, 
               label='Pass threshold (ξ/L < 0.05)')
    
    ax.set_xlabel('Frequency ω')
    ax.set_ylabel('ξ / L (Localization length / System size)')
    ax.set_title('Phonon Localization Length')
    ax.set_ylim(0, 0.5)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filename}")


def plot_thermal_conductivity(T_values, kappa_qp, kappa_ord, filename):
    """Plot thermal conductivity vs temperature."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    ax1.loglog(T_values, kappa_qp, 'r-', linewidth=2, label='Quasiperiodic')
    ax1.loglog(T_values, kappa_ord, 'b-', linewidth=2, label='Ordered')
    ax1.set_xlabel('Temperature T')
    ax1.set_ylabel('κ (thermal conductivity proxy)')
    ax1.set_title('Thermal Conductivity')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ratio = kappa_qp / np.maximum(kappa_ord, 1e-20)
    ax2.semilogx(T_values, ratio, 'k-', linewidth=2)
    ax2.axhline(y=0.5, color='green', linestyle='--', alpha=0.5, label='Pass threshold')
    ax2.axhline(y=0.8, color='red', linestyle='--', alpha=0.5, label='Fail threshold')
    ax2.axhline(y=0.85, color='orange', linestyle=':', alpha=0.5, label='1D result (thesis)')
    ax2.set_xlabel('Temperature T')
    ax2.set_ylabel('κ_QP / κ_ordered')
    ax2.set_title('Thermal Conductivity Ratio')
    ax2.set_ylim(0, 1.2)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filename}")


def plot_modulation_comparison(mod_stats, filename):
    """Visualize electron vs phonon modulation asymmetry."""
    fig, ax = plt.subplots(figsize=(8, 5))
    
    labels = ['Electron\n(hopping t, d⁻²)', 'Phonon\n(spring k, d⁻⁴)']
    values = [mod_stats['electron_modulation'] * 100, 
              mod_stats['phonon_modulation'] * 100]
    colors = ['#2E75B6', '#C0392B']
    
    bars = ax.bar(labels, values, color=colors, width=0.5, edgecolor='black')
    
    ax.axhline(y=100, color='gray', linestyle='--', alpha=0.3, 
               label='Aubry-André localization threshold')
    
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                f'{val:.1f}%', ha='center', va='bottom', fontweight='bold')
    
    ax.set_ylabel('Modulation δ/mean (%)')
    ax.set_title('PGTC Mechanism: Differential Localization\n'
                 f'Phonon modulation is {mod_stats["ratio"]:.1f}× electron modulation')
    ax.set_ylim(0, max(values) * 1.3)
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig(filename, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filename}")


# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

def run_stage2(output_dir="stage2_results", n_subdivisions=5, k0=1.0, t0=1.0):
    """
    Execute the full Stage 2 phonon transport simulation.
    
    Uses the SCALAR dynamical matrix for speed (captures essential physics).
    Full 2D vector analysis available via build_dynamical_matrix_2d.
    """
    os.makedirs(output_dir, exist_ok=True)
    
    print("═" * 70)
    print("  STAGE 2: 2D Phonon Transport on Penrose Patch")
    print("  Fractonic Weyl Semimetal — PGTC Validation")
    print("═" * 70)
    
    t_start = time.time()
    
    # ── Step 1: Generate lattice (same as Stage 1) ──
    print(f"\n{'─'*50}")
    print("  STEP 1: Penrose Tiling Generation")
    print(f"{'─'*50}")
    vertices, edges, coord_numbers = generate_penrose_tiling(n_subdivisions)
    N = len(vertices)
    bond_lengths = compute_bond_lengths(vertices, edges)
    d0 = np.median(bond_lengths)
    
    # System size
    L = np.sqrt((vertices[:, 0].max() - vertices[:, 0].min())**2 + 
                (vertices[:, 1].max() - vertices[:, 1].min())**2)
    
    # ── Step 2: Modulation analysis ──
    print(f"\n{'─'*50}")
    print("  STEP 2: Modulation Analysis (PGTC Mechanism)")
    print(f"{'─'*50}")
    mod_stats = analyze_modulation(bond_lengths, d0, k0, t0)
    
    print(f"  Electron hopping modulation:  δt/t₀ = {mod_stats['electron_modulation']:.4f} "
          f"({mod_stats['electron_modulation']*100:.1f}%)")
    print(f"  Phonon spring modulation:     δk/k₀ = {mod_stats['phonon_modulation']:.4f} "
          f"({mod_stats['phonon_modulation']*100:.1f}%)")
    print(f"  Phonon/Electron ratio:        {mod_stats['ratio']:.2f}×")
    print(f"  (Thesis 1D values: 9.7% / 19.3% = 2.0×)")
    
    plot_modulation_comparison(mod_stats, 
                               os.path.join(output_dir, "modulation_comparison.png"))
    
    # ── Step 3: Build dynamical matrices ──
    print(f"\n{'─'*50}")
    print("  STEP 3: Dynamical Matrix Construction")
    print(f"{'─'*50}")
    
    D_qp, D_ord, _ = build_dynamical_matrix_scalar(vertices, edges, bond_lengths, k0)
    print(f"  Scalar dynamical matrix: {N}×{N}")
    print(f"  QP matrix nnz: {D_qp.nnz}")
    
    # ── Step 4: Diagonalize ──
    print(f"\n{'─'*50}")
    print("  STEP 4: Phonon Spectrum Computation")
    print(f"{'─'*50}")
    
    freq_qp, evec_qp = compute_phonon_spectrum(D_qp, "Quasiperiodic")
    freq_ord, evec_ord = compute_phonon_spectrum(D_ord, "Ordered")
    
    # ── Step 5: Participation ratios ──
    print(f"\n{'─'*50}")
    print("  STEP 5: Mode Localization Analysis")
    print(f"{'─'*50}")
    
    ipr_qp = compute_participation_ratio(evec_qp, N)
    ipr_ord = compute_participation_ratio(evec_ord, N)
    
    # Exclude zero modes from statistics
    nonzero_qp = freq_qp > 1e-6
    nonzero_ord = freq_ord > 1e-6
    
    mean_ipr_qp = np.mean(ipr_qp[nonzero_qp])
    mean_ipr_ord = np.mean(ipr_ord[nonzero_ord])
    min_ipr_qp = np.min(ipr_qp[nonzero_qp])
    min_ipr_ord = np.min(ipr_ord[nonzero_ord])
    
    print(f"  Mean IPR — Quasiperiodic: {mean_ipr_qp:.4f}, Ordered: {mean_ipr_ord:.4f}")
    print(f"  Min IPR  — Quasiperiodic: {min_ipr_qp:.4f}, Ordered: {min_ipr_ord:.4f}")
    print(f"  IPR ratio (QP/Ord): {mean_ipr_qp/mean_ipr_ord:.3f}")
    
    # Localization lengths
    xi_qp = compute_localization_length(evec_qp, vertices, N)
    xi_ord = compute_localization_length(evec_ord, vertices, N)
    
    min_xi_qp = np.min(xi_qp[nonzero_qp])
    min_xi_ord = np.min(xi_ord[nonzero_ord])
    
    print(f"\n  Min ξ/L — Quasiperiodic: {min_xi_qp/L:.4f}, Ordered: {min_xi_ord/L:.4f}")
    
    # Count strongly localized modes (ξ/L < 0.05)
    n_localized_qp = np.sum((xi_qp[nonzero_qp] / L) < 0.05)
    n_localized_ord = np.sum((xi_ord[nonzero_ord] / L) < 0.05)
    print(f"  Strongly localized modes (ξ/L < 0.05):")
    print(f"    Quasiperiodic: {n_localized_qp} / {np.sum(nonzero_qp)}")
    print(f"    Ordered:       {n_localized_ord} / {np.sum(nonzero_ord)}")
    
    # ── Step 6: Thermal conductivity ──
    print(f"\n{'─'*50}")
    print("  STEP 6: Thermal Conductivity Computation")
    print(f"{'─'*50}")
    
    T_values = np.logspace(-1, 1, 30)
    
    kappa_qp = simple_thermal_conductivity_proxy(freq_qp, evec_qp, N, T_values)
    kappa_ord = simple_thermal_conductivity_proxy(freq_ord, evec_ord, N, T_values)
    
    kappa_ratio = kappa_qp / np.maximum(kappa_ord, 1e-20)
    mean_ratio = np.mean(kappa_ratio[(T_values > 0.3) & (T_values < 5.0)])
    
    print(f"\n  Thermal conductivity ratio κ_QP / κ_ordered:")
    for T_sample in [0.5, 1.0, 5.0]:
        idx = np.argmin(np.abs(T_values - T_sample))
        print(f"    T = {T_sample:.1f}: κ_QP/κ_ord = {kappa_ratio[idx]:.4f}")
    print(f"  Mean ratio (T ∈ [0.3, 5.0]): {mean_ratio:.4f}")
    print(f"  Compare thesis 1D: 0.84–0.86")
    
    # ── Step 7: Spectral gaps analysis ──
    print(f"\n{'─'*50}")
    print("  STEP 7: Spectral Gap Analysis")
    print(f"{'─'*50}")
    
    # Check for hierarchical gaps in the phonon spectrum
    freq_sorted_qp = np.sort(freq_qp[freq_qp > 1e-6])
    freq_sorted_ord = np.sort(freq_ord[freq_ord > 1e-6])
    
    gaps_qp = np.diff(freq_sorted_qp)
    gaps_ord = np.diff(freq_sorted_ord)
    
    mean_gap_qp = np.mean(gaps_qp)
    max_gap_qp = np.max(gaps_qp)
    mean_gap_ord = np.mean(gaps_ord)
    max_gap_ord = np.max(gaps_ord)
    
    print(f"  Mean spectral gap — QP: {mean_gap_qp:.6f}, Ord: {mean_gap_ord:.6f}")
    print(f"  Max spectral gap  — QP: {max_gap_qp:.6f}, Ord: {max_gap_ord:.6f}")
    print(f"  Gap ratio (max QP / max Ord): {max_gap_qp/max_gap_ord:.2f}")
    
    # ── Step 8: Generate plots ──
    print(f"\n{'─'*50}")
    print("  STEP 8: Visualization")
    print(f"{'─'*50}")
    
    plot_phonon_dos(freq_qp, freq_ord, 
                    os.path.join(output_dir, "phonon_dos.png"))
    plot_participation_ratios(freq_qp, ipr_qp, freq_ord, ipr_ord,
                              os.path.join(output_dir, "participation_ratios.png"))
    plot_localization_lengths(freq_qp, xi_qp, freq_ord, xi_ord, L,
                              os.path.join(output_dir, "localization_lengths.png"))
    plot_thermal_conductivity(T_values, kappa_qp, kappa_ord,
                              os.path.join(output_dir, "thermal_conductivity.png"))
    
    # ── Summary ──
    t_elapsed = time.time() - t_start
    
    summary = {
        'n_vertices': N,
        'n_edges': len(edges),
        'system_size_L': float(L),
        'modulation': mod_stats,
        'mean_ipr_ratio': float(mean_ipr_qp / mean_ipr_ord),
        'min_xi_over_L_qp': float(min_xi_qp / L),
        'min_xi_over_L_ord': float(min_xi_ord / L),
        'n_localized_modes_qp': int(n_localized_qp),
        'n_localized_modes_ord': int(n_localized_ord),
        'kappa_ratio_mean': float(mean_ratio),
        'kappa_ratios': {
            'T=0.5': float(kappa_ratio[np.argmin(np.abs(T_values - 0.5))]),
            'T=1.0': float(kappa_ratio[np.argmin(np.abs(T_values - 1.0))]),
            'T=5.0': float(kappa_ratio[np.argmin(np.abs(T_values - 5.0))]),
        },
        'spectral_gap_ratio': float(max_gap_qp / max_gap_ord),
        'gate_assessment': {
            'kappa_ratio_pass': float(mean_ratio) < 0.5,
            'kappa_ratio_partial': float(mean_ratio) < 0.8,
            'localization_pass': float(min_xi_qp / L) < 0.05,
            'spectral_gaps_visible': float(max_gap_qp / max_gap_ord) > 2.0,
        },
        'elapsed_seconds': t_elapsed,
    }
    
    print(f"\n{'═'*70}")
    print(f"  STAGE 2 COMPLETE — Elapsed: {t_elapsed:.1f}s")
    print(f"{'═'*70}")
    
    kp = summary['gate_assessment']['kappa_ratio_pass']
    kpart = summary['gate_assessment']['kappa_ratio_partial']
    lp = summary['gate_assessment']['localization_pass']
    
    print(f"\n  ┌─────────────────────────────────────────────────┐")
    print(f"  │             STAGE 2 GATE ASSESSMENT              │")
    print(f"  ├─────────────────────────────────────────────────┤")
    print(f"  │  κ_QP/κ_ord < 0.5:      {'✓ PASS' if kp else '✗ FAIL':>10}          │")
    print(f"  │  κ_QP/κ_ord < 0.8:      {'✓ PASS' if kpart else '✗ FAIL':>10}          │")
    print(f"  │  min ξ/L < 0.05:        {'✓ PASS' if lp else '✗ FAIL':>10}          │")
    print(f"  ├─────────────────────────────────────────────────┤")
    if kp:
        print(f"  │  OVERALL: ✓ GATE PASSED (strong suppression)   │")
    elif kpart:
        print(f"  │  OVERALL: ~ PARTIAL PASS (modest suppression)   │")
    else:
        print(f"  │  OVERALL: ✗ GATE FAILED (no improvement)        │")
    print(f"  └─────────────────────────────────────────────────┘")
    
    with open(os.path.join(output_dir, "stage2_summary.json"), 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\n  Summary saved to {output_dir}/stage2_summary.json")
    
    return summary


# ═══════════════════════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    summary = run_stage2(
        output_dir="stage2_results",
        n_subdivisions=5,
        k0=1.0,
        t0=1.0,
    )
