"""
Stellarator Force-Free Field & Taylor Relaxation
==================================================
Demonstrates the CORE of Taylor's theorem:
  Under resistive diffusion, energy decays FASTER than helicity.

Uses pure resistive MHD (∂B/∂t = η∇²B) which is:
  1. Numerically stable
  2. Analytically tractable (eigenmode analysis)
  3. Sufficient to demonstrate the helicity/energy separation

The force-free ABC flow has known eigenmodes, so we can
verify the simulation against exact results.
"""

import numpy as np
import json

N = 48
L = 2 * np.pi
dx = L / N

coords = np.linspace(0, L, N, endpoint=False)
X, Y, Z = np.meshgrid(coords, coords, coords, indexing='ij')

k1d = np.fft.fftfreq(N, d=dx) * 2 * np.pi
KX, KY, KZ = np.meshgrid(k1d, k1d, k1d, indexing='ij')
K2 = KX**2 + KY**2 + KZ**2
K2_safe = K2.copy()
K2_safe[0, 0, 0] = 1.0

print(f"Grid: {N}^3 = {N**3:,} points")

# ============================================================
# MAGNETIC FIELD CONFIGURATIONS
# ============================================================
def abc_flow(X, Y, Z, A=1.0, B=1.0, C=1.0):
    """Exact Beltrami field: ∇ × B = B (λ = 1)"""
    Bx = A * np.sin(Z) + C * np.cos(Y)
    By = B * np.sin(X) + A * np.cos(Z)
    Bz = C * np.sin(Y) + B * np.cos(X)
    return Bx, By, Bz

def perturbed_field(X, Y, Z, noise_level=0.5):
    """ABC + noise: simulates injection of disordered flux"""
    Bx, By, Bz = abc_flow(X, Y, Z)
    np.random.seed(42)
    Bx += noise_level * np.random.randn(N, N, N)
    By += noise_level * np.random.randn(N, N, N)
    Bz += noise_level * np.random.randn(N, N, N)
    # Enforce ∇·B = 0
    Bx_k = np.fft.fftn(Bx)
    By_k = np.fft.fftn(By)
    Bz_k = np.fft.fftn(Bz)
    div_k = KX * Bx_k + KY * By_k + KZ * Bz_k
    Bx_k -= KX * div_k / K2_safe
    By_k -= KY * div_k / K2_safe
    Bz_k -= KZ * div_k / K2_safe
    Bx_k[0,0,0] = 0; By_k[0,0,0] = 0; Bz_k[0,0,0] = 0
    return np.real(np.fft.ifftn(Bx_k)), np.real(np.fft.ifftn(By_k)), np.real(np.fft.ifftn(Bz_k))

def high_k_perturbation(X, Y, Z, noise_level=0.3):
    """ABC + high-k noise: small-scale structure that Taylor relaxation eliminates"""
    Bx, By, Bz = abc_flow(X, Y, Z)
    np.random.seed(123)
    # Only add noise at high k (small scales)
    noise_x = np.fft.fftn(noise_level * np.random.randn(N, N, N))
    noise_y = np.fft.fftn(noise_level * np.random.randn(N, N, N))
    noise_z = np.fft.fftn(noise_level * np.random.randn(N, N, N))
    K_mag = np.sqrt(K2)
    high_k_mask = (K_mag > 3.0).astype(float)
    noise_x *= high_k_mask; noise_y *= high_k_mask; noise_z *= high_k_mask
    Bx += np.real(np.fft.ifftn(noise_x))
    By += np.real(np.fft.ifftn(noise_y))
    Bz += np.real(np.fft.ifftn(noise_z))
    # Enforce ∇·B = 0
    Bx_k = np.fft.fftn(Bx)
    By_k = np.fft.fftn(By)
    Bz_k = np.fft.fftn(Bz)
    div_k = KX * Bx_k + KY * By_k + KZ * Bz_k
    Bx_k -= KX * div_k / K2_safe
    By_k -= KY * div_k / K2_safe
    Bz_k -= KZ * div_k / K2_safe
    Bx_k[0,0,0] = 0; By_k[0,0,0] = 0; Bz_k[0,0,0] = 0
    return np.real(np.fft.ifftn(Bx_k)), np.real(np.fft.ifftn(By_k)), np.real(np.fft.ifftn(Bz_k))

# ============================================================
# DIAGNOSTICS
# ============================================================
def compute_A(Bx, By, Bz):
    """Vector potential in Coulomb gauge"""
    Bx_k = np.fft.fftn(Bx); By_k = np.fft.fftn(By); Bz_k = np.fft.fftn(Bz)
    cross_x = KY * Bz_k - KZ * By_k
    cross_y = KZ * Bx_k - KX * Bz_k
    cross_z = KX * By_k - KY * Bx_k
    Ax_k = -1j * cross_x / K2_safe
    Ay_k = -1j * cross_y / K2_safe
    Az_k = -1j * cross_z / K2_safe
    Ax_k[0,0,0]=0; Ay_k[0,0,0]=0; Az_k[0,0,0]=0
    return (np.real(np.fft.ifftn(Ax_k)), np.real(np.fft.ifftn(Ay_k)), 
            np.real(np.fft.ifftn(Az_k)))

def helicity(Bx, By, Bz):
    Ax, Ay, Az = compute_A(Bx, By, Bz)
    return float(np.sum(Ax*Bx + Ay*By + Az*Bz) * dx**3)

def energy(Bx, By, Bz):
    return float(0.5 * np.sum(Bx**2 + By**2 + Bz**2) * dx**3)

def ff_error(Bx, By, Bz, lam=1.0):
    Bx_k = np.fft.fftn(Bx); By_k = np.fft.fftn(By); Bz_k = np.fft.fftn(Bz)
    cx = np.real(np.fft.ifftn(1j*(KY*Bz_k - KZ*By_k)))
    cy = np.real(np.fft.ifftn(1j*(KZ*Bx_k - KX*Bz_k)))
    cz = np.real(np.fft.ifftn(1j*(KX*By_k - KY*Bx_k)))
    err = np.sqrt(np.mean((cx-lam*Bx)**2 + (cy-lam*By)**2 + (cz-lam*Bz)**2))
    B_rms = np.sqrt(np.mean(Bx**2 + By**2 + Bz**2))
    return float(err / (B_rms + 1e-10))

def current_helicity(Bx, By, Bz):
    Bx_k = np.fft.fftn(Bx); By_k = np.fft.fftn(By); Bz_k = np.fft.fftn(Bz)
    Jx = np.real(np.fft.ifftn(1j*(KY*Bz_k - KZ*By_k)))
    Jy = np.real(np.fft.ifftn(1j*(KZ*Bx_k - KX*Bz_k)))
    Jz = np.real(np.fft.ifftn(1j*(KX*By_k - KY*Bx_k)))
    return float(np.sum(Jx*Bx + Jy*By + Jz*Bz) * dx**3)

# ============================================================
# RESISTIVE DIFFUSION: ∂B/∂t = η∇²B
# ============================================================
def resistive_step(Bx, By, Bz, eta, dt):
    """
    Pure resistive diffusion in Fourier space.
    Each mode decays as exp(-η k² t).
    
    CRUCIALLY: modes at different k decay at different rates.
    High-k modes (small-scale structure, energy) decay fast.
    Low-k modes (large-scale structure, helicity) decay slow.
    
    This is the MECHANISM of Taylor relaxation:
    the k-dependence of resistive decay separates
    energy dissipation (fast) from helicity decay (slow).
    """
    decay = np.exp(-eta * K2 * dt)
    
    Bx_k = np.fft.fftn(Bx) * decay
    By_k = np.fft.fftn(By) * decay
    Bz_k = np.fft.fftn(Bz) * decay
    
    return np.real(np.fft.ifftn(Bx_k)), np.real(np.fft.ifftn(By_k)), np.real(np.fft.ifftn(Bz_k))

# ============================================================
# SPECTRAL HELICITY/ENERGY ANALYSIS
# ============================================================
def spectral_analysis(Bx, By, Bz):
    """
    Compute the helicity and energy spectra as functions of k.
    
    For a Beltrami field with ∇×B = λB, the helicity spectrum
    H(k) peaks at k = λ and the energy spectrum E(k) = k·H(k).
    
    Under resistive decay:
      H(k,t) = H(k,0) · exp(-2ηk²t)
      E(k,t) = E(k,0) · exp(-2ηk²t)
    
    The total helicity decays as ~ exp(-2ηk_min²t)
    The total energy decays as ~ exp(-2η<k²>t) where <k²> > k_min²
    
    Hence energy decays faster — this IS Taylor relaxation.
    """
    Bx_k = np.fft.fftn(Bx); By_k = np.fft.fftn(By); Bz_k = np.fft.fftn(Bz)
    Ax_k, Ay_k, Az_k = [np.zeros_like(Bx_k) for _ in range(3)]
    
    cross_x = KY * Bz_k - KZ * By_k
    cross_y = KZ * Bx_k - KX * Bz_k
    cross_z = KX * By_k - KY * Bx_k
    Ax_k = -1j * cross_x / K2_safe
    Ay_k = -1j * cross_y / K2_safe
    Az_k = -1j * cross_z / K2_safe
    
    # Spectral energy density: E(k) = (1/2)|B̂(k)|²
    E_spec = 0.5 * (np.abs(Bx_k)**2 + np.abs(By_k)**2 + np.abs(Bz_k)**2) / N**6
    # Spectral helicity density: H(k) = Re(Â*(k) · B̂(k))
    H_spec = np.real(np.conj(Ax_k)*Bx_k + np.conj(Ay_k)*By_k + np.conj(Az_k)*Bz_k) / N**6
    
    K_mag = np.sqrt(K2)
    k_bins = np.arange(0.5, N//2) * (2*np.pi/L)
    dk = 2*np.pi/L
    
    E_shell = np.zeros(len(k_bins))
    H_shell = np.zeros(len(k_bins))
    for i, kb in enumerate(k_bins):
        mask = (K_mag >= kb - dk/2) & (K_mag < kb + dk/2)
        if mask.any():
            E_shell[i] = E_spec[mask].sum()
            H_shell[i] = H_spec[mask].sum()
    
    return k_bins.tolist(), E_shell.tolist(), H_shell.tolist()


# ============================================================
# MAIN
# ============================================================
def run_diffusion(init_func, label, eta, n_steps=800, dt=0.005):
    Bx, By, Bz = init_func(X, Y, Z)
    
    H0 = helicity(Bx, By, Bz)
    E0 = energy(Bx, By, Bz)
    ff0 = ff_error(Bx, By, Bz)
    
    rec = {"label": label, "eta": eta, 
           "t": [0.0], "H": [H0], "E": [E0], "ff": [ff0],
           "H_norm": [1.0], "E_norm": [1.0]}
    
    print(f"\n  {label}")
    print(f"    H₀ = {H0:.2f}, E₀ = {E0:.2f}, FF₀ = {ff0:.4f}")
    
    for step in range(1, n_steps + 1):
        Bx, By, Bz = resistive_step(Bx, By, Bz, eta, dt)
        
        if step % 40 == 0:
            H = helicity(Bx, By, Bz)
            E = energy(Bx, By, Bz)
            ff = ff_error(Bx, By, Bz)
            
            rec["t"].append(round(step*dt, 4))
            rec["H"].append(H)
            rec["E"].append(E)
            rec["ff"].append(ff)
            rec["H_norm"].append(H / (H0 + 1e-30))
            rec["E_norm"].append(E / (E0 + 1e-30))
            
            if step % 200 == 0:
                print(f"    t={step*dt:.2f} | H/H₀={H/(H0+1e-30):.6f} | "
                      f"E/E₀={E/(E0+1e-30):.6f} | FF={ff:.4f}")
    
    # Final spectrum
    k_bins, E_spec, H_spec = spectral_analysis(Bx, By, Bz)
    rec["final_spectrum_k"] = k_bins
    rec["final_spectrum_E"] = E_spec
    rec["final_spectrum_H"] = H_spec
    
    # Initial spectrum
    Bx0, By0, Bz0 = init_func(X, Y, Z)
    _, E_spec0, H_spec0 = spectral_analysis(Bx0, By0, Bz0)
    rec["initial_spectrum_E"] = E_spec0
    rec["initial_spectrum_H"] = H_spec0
    
    rec["H_final_pct"] = (rec["H"][-1] / (H0 + 1e-30) - 1) * 100
    rec["E_final_pct"] = (rec["E"][-1] / (E0 + 1e-30) - 1) * 100
    
    return rec

def main():
    print("=" * 65)
    print("TAYLOR RELAXATION: HELICITY vs ENERGY UNDER RESISTIVE DECAY")
    print("=" * 65)
    
    results = []
    
    # 1: Pure ABC at different η
    print("\n--- Pure ABC Flow (Exact Beltrami) ---")
    for eta in [1e-3, 5e-3, 1e-2]:
        r = run_diffusion(abc_flow, f"ABC η={eta}", eta)
        results.append(r)
    
    # 2: Perturbed ABC (Taylor relaxation)
    print("\n--- Perturbed ABC (Taylor Relaxation) ---")
    for eta in [1e-3, 5e-3, 1e-2]:
        r = run_diffusion(perturbed_field, f"Perturbed η={eta}", eta)
        results.append(r)
    
    # 3: High-k perturbation (small-scale noise)
    print("\n--- High-k Perturbation (Small-Scale Noise) ---")
    for eta in [1e-3, 5e-3, 1e-2]:
        r = run_diffusion(high_k_perturbation, f"High-k η={eta}", eta)
        results.append(r)
    
    # Summary
    print("\n" + "=" * 65)
    print("SUMMARY: SELECTIVE DISSIPATION")
    print("=" * 65)
    print(f"{'Experiment':<30} {'H retained':>12} {'E retained':>12} {'Ratio':>8}")
    print("-" * 65)
    for r in results:
        H_ret = r["H_norm"][-1] * 100
        E_ret = r["E_norm"][-1] * 100
        ratio = (100 - E_ret) / (100 - H_ret + 1e-10)
        print(f"{r['label']:<30} {H_ret:>11.3f}% {E_ret:>11.3f}% {ratio:>7.1f}x")
    
    print("\n--- KEY RESULT ---")
    print("If energy dissipation >> helicity dissipation,")
    print("then Taylor relaxation is operating:")
    print("the system sheds energy while preserving topology.")
    
    with open("/home/claude/taylor_results.json", 'w') as f:
        json.dump(results, f, indent=2, default=float)
    
    print(f"\nSaved to /home/claude/taylor_results.json")
    return results

if __name__ == "__main__":
    main()
