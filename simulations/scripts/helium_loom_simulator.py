"""
Helium Loom Simulator
=====================
Gross-Pitaevskii equation on a 2D grid with trefoil phase imprint
via the Milnor polynomial f(u,v) = u^3 - v^2.

The wavefunction is represented in GA rotor form:
    ψ = √ρ · exp(-B/2)
where B is a bivector encoding the phase (rotation in the e12 plane).

In 2D, this reduces to ψ = √ρ · exp(-iθ/2) where θ is the phase angle,
but we track it as a bivector magnitude, not as a complex number.

The cohomological audit computes the winding number:
    W = (1/2π) ∮ v · dl
around closed contours, where v = (ℏ/m) ∇θ is the superfluid velocity.
"""

import numpy as np
import json
import os

# ============================================================
# SYSTEM PARAMETERS
# ============================================================
N = 64              # Grid resolution
L = 10.0            # Box size
dt = 0.005          # Time step (reduced for stability)
g = 1.0             # Non-linear interaction strength
mu = 1.0            # Chemical potential / background density
N_STEPS = 2000      # Total evolution steps
AUDIT_INTERVAL = 50 # Steps between cohomological audits

dx = L / N
x = np.linspace(-L/2, L/2, N, endpoint=False)
y = np.linspace(-L/2, L/2, N, endpoint=False)
X, Y = np.meshgrid(x, y, indexing='ij')

# Momentum space grid for split-step FFT
kx = 2 * np.pi * np.fft.fftfreq(N, d=dx)
ky = 2 * np.pi * np.fft.fftfreq(N, d=dx)
KX, KY = np.meshgrid(kx, ky, indexing='ij')
K2 = KX**2 + KY**2

# ============================================================
# MILNOR POLYNOMIAL TREFOIL PHASE IMPRINT
# ============================================================
def milnor_trefoil_phase(X, Y):
    """
    The Milnor fibration of f(u,v) = u^3 - v^2 gives the trefoil knot
    as the link of the singularity at the origin.
    
    Map (x,y) -> (u,v) in C^2 via u = x + iy normalized to S^3,
    then compute arg(f) = arg(u^3 - v^2).
    
    For a 2D slice, we use:
        u = (x + iy) / r_norm
        v = secondary coordinate constructed from the radial direction
    
    The phase θ = arg(u^3 - v^2) winds 3 times as we go around
    the trefoil, giving winding number related to the knot topology.
    """
    r = np.sqrt(X**2 + Y**2) + 1e-10
    
    # Complex coordinate
    z = (X + 1j * Y)
    
    # Milnor map: f(z, w) = z^3 - w^2
    # For a 2D section, set w = conjugate(z) * scale to get
    # a non-degenerate phase field
    w = np.conj(z) * 0.5
    
    f = z**3 - w**2
    
    # The phase of f gives the Milnor fiber
    theta = np.angle(f)
    
    return theta


def initialize_wavefunction(X, Y):
    """
    Initialize ψ = √ρ · exp(-B/2) where B is the Milnor trefoil phase.
    
    In GA terms:
        ρ = scalar grade (density)
        B = bivector grade (phase as rotation in e12 plane)
        
    The rotor R = exp(-B/2) acts on vectors by v -> R v R†
    For the scalar wavefunction, this reduces to phase multiplication.
    """
    # Background density with smooth envelope
    r = np.sqrt(X**2 + Y**2)
    rho = mu * np.exp(-0.5 * (r / (L/3))**4)  # Super-Gaussian envelope
    
    # Trefoil phase from Milnor polynomial
    theta = milnor_trefoil_phase(X, Y)
    
    # GA rotor form: ψ = √ρ · exp(-iθ/2) 
    # where i = e12 bivector, not abstract √(-1)
    # In component form for computation:
    psi = np.sqrt(rho) * np.exp(1j * theta)
    
    return psi


# ============================================================
# GROSS-PITAEVSKII EVOLUTION (Split-Step Fourier)
# ============================================================
def gpe_step(psi, dt):
    """
    Split-step Fourier method for:
        iℏ ∂ψ/∂t = (-ℏ²/2m ∇² + g|ψ|² - μ) ψ
        
    In natural units (ℏ = m = 1):
        i ∂ψ/∂t = (-1/2 ∇² + g|ψ|² - μ) ψ
    """
    # Half-step nonlinear
    rho = np.abs(psi)**2
    V_nl = g * rho - mu
    psi = psi * np.exp(-1j * V_nl * dt / 2)
    
    # Full-step kinetic (in Fourier space)
    psi_k = np.fft.fft2(psi)
    psi_k = psi_k * np.exp(-1j * K2 * dt / 2)
    psi = np.fft.ifft2(psi_k)
    
    # Half-step nonlinear
    rho = np.abs(psi)**2
    V_nl = g * rho - mu
    psi = psi * np.exp(-1j * V_nl * dt / 2)
    
    return psi


# ============================================================
# COHOMOLOGICAL AUDIT: Winding Number Computation
# ============================================================
def compute_phase_gradient(psi):
    """
    Compute the superfluid velocity v = (ℏ/m) ∇θ
    where θ = arg(ψ), using the gauge-invariant formula:
    
        v_x = Im(ψ* ∂ψ/∂x) / |ψ|²
        v_y = Im(ψ* ∂ψ/∂y) / |ψ|²
    
    This avoids branch cut issues in direct phase differentiation.
    """
    rho = np.abs(psi)**2 + 1e-20  # regularize
    
    # Spectral derivatives
    psi_k = np.fft.fft2(psi)
    dpsi_dx = np.fft.ifft2(1j * KX * psi_k)
    dpsi_dy = np.fft.ifft2(1j * KY * psi_k)
    
    vx = np.imag(np.conj(psi) * dpsi_dx) / rho
    vy = np.imag(np.conj(psi) * dpsi_dy) / rho
    
    return vx, vy


def winding_number_contour(vx, vy, cx, cy, radius, n_points=200):
    """
    Compute winding number along a circular contour:
        W = (1/2π) ∮ v · dl
    
    This is the cohomological audit: the integral of the 
    superfluid velocity 1-form over a closed 1-cycle.
    
    In GA language: integrate the bivector field's boundary 
    over a closed contour to extract the scalar topological charge.
    """
    theta_pts = np.linspace(0, 2*np.pi, n_points, endpoint=False)
    dtheta = 2 * np.pi / n_points
    
    integral = 0.0
    for t in theta_pts:
        # Point on contour
        px = cx + radius * np.cos(t)
        py = cy + radius * np.sin(t)
        
        # Tangent vector (dl)
        dlx = -radius * np.sin(t) * dtheta
        dly =  radius * np.cos(t) * dtheta
        
        # Interpolate velocity at this point
        # Map to grid indices
        ix_f = (px + L/2) / dx
        iy_f = (py + L/2) / dx
        
        ix = int(ix_f) % N
        iy = int(iy_f) % N
        ix1 = (ix + 1) % N
        iy1 = (iy + 1) % N
        
        fx = ix_f - int(ix_f)
        fy = iy_f - int(iy_f)
        
        # Bilinear interpolation
        vx_interp = (vx[ix, iy] * (1-fx)*(1-fy) + 
                      vx[ix1, iy] * fx*(1-fy) +
                      vx[ix, iy1] * (1-fx)*fy + 
                      vx[ix1, iy1] * fx*fy)
        vy_interp = (vy[ix, iy] * (1-fx)*(1-fy) + 
                      vy[ix1, iy] * fx*(1-fy) +
                      vy[ix, iy1] * (1-fx)*fy + 
                      vy[ix1, iy1] * fx*fy)
        
        integral += vx_interp * dlx + vy_interp * dly
    
    return integral / (2 * np.pi)


def full_cohomological_audit(psi):
    """
    Compute winding numbers on multiple contours at different radii.
    
    The topological lock is verified if:
    1. All contours enclosing the origin give the same integer W
    2. The value persists over time evolution
    3. Non-integer values indicate vortex cores crossing the contour
    """
    vx, vy = compute_phase_gradient(psi)
    
    radii = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    windings = {}
    
    for r in radii:
        w = winding_number_contour(vx, vy, 0, 0, r)
        windings[f"r={r:.1f}"] = round(w, 4)
    
    # Also compute total vorticity via discrete curl
    # ω = ∂v_y/∂x - ∂v_x/∂y (the "bivector shear")
    vx_k = np.fft.fft2(vx)
    vy_k = np.fft.fft2(vy)
    
    dvydx = np.real(np.fft.ifft2(1j * KX * vy_k))
    dvxdy = np.real(np.fft.ifft2(1j * KY * vx_k))
    
    vorticity = dvydx - dvxdy
    total_circulation = np.sum(vorticity) * dx * dx / (2 * np.pi)
    
    windings["total_circulation"] = round(float(total_circulation), 4)
    
    return windings, vorticity


# ============================================================
# ENERGY SPECTRUM ANALYSIS
# ============================================================
def compute_energy_spectrum(psi):
    """
    Decompose kinetic energy into:
    - Compressible (scalar/acoustic part - "Sharp" modality)
    - Incompressible (vortical/bivector part - "Flat" modality)
    
    This separation corresponds to the HoTT modality mapping:
        Sharp (♯): irrotational flow → scalar grade
        Flat (♭): rotational flow → bivector grade
    """
    rho = np.abs(psi)**2 + 1e-20
    sqrt_rho = np.sqrt(rho)
    
    vx, vy = compute_phase_gradient(psi)
    
    # Momentum density
    jx = rho * vx
    jy = rho * vy
    
    # Helmholtz decomposition via FFT
    jx_k = np.fft.fft2(jx)
    jy_k = np.fft.fft2(jy)
    
    # Compressible (irrotational) part: ∇φ where ∇²φ = ∇·j
    div_j_k = 1j * KX * jx_k + 1j * KY * jy_k
    K2_reg = K2.copy()
    K2_reg[0, 0] = 1.0  # Avoid division by zero
    phi_k = div_j_k / K2_reg
    phi_k[0, 0] = 0
    
    jx_comp_k = 1j * KX * phi_k
    jy_comp_k = 1j * KY * phi_k
    
    # Incompressible (solenoidal) part
    jx_inc_k = jx_k - jx_comp_k
    jy_inc_k = jy_k - jy_comp_k
    
    # Energy spectra (radially averaged)
    E_comp = 0.5 * (np.abs(jx_comp_k)**2 + np.abs(jy_comp_k)**2) / (N**2 * rho.mean())
    E_inc = 0.5 * (np.abs(jx_inc_k)**2 + np.abs(jy_inc_k)**2) / (N**2 * rho.mean())
    
    # Radial binning
    k_mag = np.sqrt(K2)
    k_bins = np.arange(0.5, N//2, 1.0) * (2*np.pi/L)
    
    spec_comp = np.zeros(len(k_bins))
    spec_inc = np.zeros(len(k_bins))
    
    for i, kb in enumerate(k_bins):
        mask = (k_mag >= kb - np.pi/L) & (k_mag < kb + np.pi/L)
        if mask.any():
            spec_comp[i] = E_comp[mask].sum()
            spec_inc[i] = E_inc[mask].sum()
    
    return k_bins, spec_comp, spec_inc


# ============================================================
# KSS BOUND CHECK
# ============================================================
def estimate_viscosity_entropy_ratio(psi, vorticity):
    """
    Estimate η/s from the simulation.
    
    The KSS bound states η/s ≥ ℏ/(4πk_B).
    In natural units: η/s ≥ 1/(4π).
    
    We estimate:
    - η from the decay rate of velocity correlations (Kubo formula proxy)
    - s from the entanglement entropy proxy (von Neumann entropy of 
      the coarse-grained density matrix)
    
    This is an ORDER OF MAGNITUDE estimate, not a precision measurement.
    The real measurement requires the GTI hardware.
    """
    rho = np.abs(psi)**2
    rho_norm = rho / rho.sum()
    
    # Entropy estimate: S = -Σ ρ ln ρ (configuration space entropy)
    s_density = -rho_norm * np.log(rho_norm + 1e-30)
    s_total = s_density.sum()
    
    # Viscosity estimate: η ~ <ω²> / (characteristic rate)
    omega_sq = np.mean(vorticity**2)
    char_rate = np.sqrt(mu)  # characteristic frequency scale
    eta_estimate = omega_sq / (char_rate + 1e-10)
    
    ratio = eta_estimate / (s_total + 1e-10)
    kss_bound = 1.0 / (4 * np.pi)
    
    return {
        "eta_estimate": float(eta_estimate),
        "s_estimate": float(s_total),
        "eta_over_s": float(ratio),
        "kss_bound": float(kss_bound),
        "saturates_bound": bool(abs(ratio - kss_bound) / kss_bound < 0.5)
    }


# ============================================================
# MAIN SIMULATION LOOP
# ============================================================
def run_simulation():
    print("=" * 60)
    print("HELIUM LOOM SIMULATOR")
    print("Gross-Pitaevskii + Milnor Trefoil + Cohomological Audit")
    print("=" * 60)
    print(f"\nGrid: {N}x{N}, Box: {L}, dt: {dt}, g: {g}, μ: {mu}")
    print(f"Steps: {N_STEPS}, Audit interval: {AUDIT_INTERVAL}")
    
    # Initialize
    psi = initialize_wavefunction(X, Y)
    
    # Storage for time series
    audit_log = []
    density_snapshots = []
    phase_snapshots = []
    vorticity_snapshots = []
    spectrum_data = []
    
    # Initial audit
    print("\n--- Initial Cohomological Audit ---")
    windings, vorticity = full_cohomological_audit(psi)
    kss = estimate_viscosity_entropy_ratio(psi, vorticity)
    print(f"Winding numbers: {windings}")
    print(f"KSS estimate: η/s = {kss['eta_over_s']:.6f} (bound: {kss['kss_bound']:.6f})")
    
    audit_log.append({
        "step": 0,
        "time": 0.0,
        "windings": windings,
        "kss": kss,
        "total_density": float(np.sum(np.abs(psi)**2) * dx * dx),
        "max_density": float(np.max(np.abs(psi)**2))
    })
    
    # Save initial snapshot
    density_snapshots.append(np.abs(psi)**2)
    phase_snapshots.append(np.angle(psi))
    vorticity_snapshots.append(vorticity)
    
    # Evolution
    print("\n--- Evolution ---")
    for step in range(1, N_STEPS + 1):
        psi = gpe_step(psi, dt)
        
        if step % AUDIT_INTERVAL == 0:
            windings, vorticity = full_cohomological_audit(psi)
            kss = estimate_viscosity_entropy_ratio(psi, vorticity)
            
            total_N = float(np.sum(np.abs(psi)**2) * dx * dx)
            
            audit_entry = {
                "step": step,
                "time": round(step * dt, 4),
                "windings": windings,
                "kss": kss,
                "total_density": total_N,
                "max_density": float(np.max(np.abs(psi)**2))
            }
            audit_log.append(audit_entry)
            
            # Check topological lock
            w_origin = windings.get("r=1.0", 0)
            
            if step % (AUDIT_INTERVAL * 5) == 0:
                print(f"  Step {step:5d} | t={step*dt:7.3f} | "
                      f"W(r=1)={w_origin:+8.4f} | "
                      f"N={total_N:.4f} | "
                      f"η/s={kss['eta_over_s']:.6f}")
                
                density_snapshots.append(np.abs(psi)**2)
                phase_snapshots.append(np.angle(psi))
                vorticity_snapshots.append(vorticity)
    
    # Final audit
    print("\n--- Final Cohomological Audit ---")
    windings_final, vorticity_final = full_cohomological_audit(psi)
    kss_final = estimate_viscosity_entropy_ratio(psi, vorticity_final)
    print(f"Winding numbers: {windings_final}")
    print(f"KSS estimate: η/s = {kss_final['eta_over_s']:.6f}")
    
    # Energy spectrum
    k_bins, spec_comp, spec_inc = compute_energy_spectrum(psi)
    
    # Topological lock assessment
    print("\n" + "=" * 60)
    print("TOPOLOGICAL LOCK ASSESSMENT")
    print("=" * 60)
    
    initial_w = audit_log[0]["windings"].get("r=1.0", 0)
    final_w = windings_final.get("r=1.0", 0)
    w_drift = abs(final_w - initial_w)
    
    print(f"  Initial winding (r=1): {initial_w:+.4f}")
    print(f"  Final winding   (r=1): {final_w:+.4f}")
    print(f"  Drift: {w_drift:.4f}")
    
    if w_drift < 0.1:
        print("  STATUS: TOPOLOGICAL LOCK HOLDING")
    elif w_drift < 0.5:
        print("  STATUS: TOPOLOGICAL LOCK DEGRADING")
    else:
        print("  STATUS: TOPOLOGICAL LOCK BROKEN")
    
    # Reconnection resistance check
    w_values = [entry["windings"].get("r=1.0", 0) for entry in audit_log]
    w_std = np.std(w_values)
    print(f"\n  Winding number stability (σ): {w_std:.6f}")
    if w_std < 0.05:
        print("  RECONNECTION RESISTANCE: STRONG")
    elif w_std < 0.2:
        print("  RECONNECTION RESISTANCE: MODERATE")
    else:
        print("  RECONNECTION RESISTANCE: WEAK")
    
    # Save results
    results = {
        "parameters": {
            "N": N, "L": L, "dt": dt, "g": g, "mu": mu,
            "N_steps": N_STEPS, "audit_interval": AUDIT_INTERVAL
        },
        "audit_log": audit_log,
        "final_assessment": {
            "initial_winding": initial_w,
            "final_winding": final_w,
            "winding_drift": w_drift,
            "winding_stability_sigma": float(w_std),
            "kss_ratio": kss_final["eta_over_s"],
            "kss_bound": kss_final["kss_bound"]
        },
        "energy_spectrum": {
            "k_bins": k_bins.tolist(),
            "compressible": spec_comp.tolist(),
            "incompressible": spec_inc.tolist()
        },
        "winding_time_series": w_values,
        "density_snapshots": [d.tolist() for d in density_snapshots],
        "phase_snapshots": [p.tolist() for p in phase_snapshots],
        "vorticity_snapshots": [v.tolist() for v in vorticity_snapshots]
    }
    
    return results


if __name__ == "__main__":
    results = run_simulation()
    
    output_path = "/home/claude/loom_results.json"
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to {output_path}")
