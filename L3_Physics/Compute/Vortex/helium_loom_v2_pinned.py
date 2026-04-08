"""
Helium Loom Simulator v2: PINNED SUBSTRATE
===========================================
Tests the claim: can a φ-spaced pinning lattice 
substitute for 3D topological protection?

Adds a Fibonacci-spaced pinning potential to the 
Gross-Pitaevskii evolution and re-runs the 
cohomological audit.
"""

import numpy as np
import json

# ============================================================
# SYSTEM PARAMETERS (same as v1)
# ============================================================
N = 64
L = 10.0
dt = 0.005
g = 1.0
mu = 1.0
N_STEPS = 2000
AUDIT_INTERVAL = 50

dx = L / N
x = np.linspace(-L/2, L/2, N, endpoint=False)
y = np.linspace(-L/2, L/2, N, endpoint=False)
X, Y = np.meshgrid(x, y, indexing='ij')

kx = 2 * np.pi * np.fft.fftfreq(N, d=dx)
ky = 2 * np.pi * np.fft.fftfreq(N, d=dx)
KX, KY = np.meshgrid(kx, ky, indexing='ij')
K2 = KX**2 + KY**2

# ============================================================
# GOLDEN RATIO PINNING LATTICE
# ============================================================
PHI = (1 + np.sqrt(5)) / 2  # Golden ratio

def fibonacci_radii(n_sites, base_radius=0.5):
    """
    Generate pinning site radii using Fibonacci scaling.
    r_n = base * φ^n gives maximally anti-resonant spacing.
    """
    radii = [base_radius * PHI**n for n in range(n_sites)]
    return radii

def golden_angle_positions(n_sites, base_radius=0.5):
    """
    Place pinning sites using golden angle (137.5°) separation.
    This gives the most uniform angular distribution.
    Combined with Fibonacci radii for full quasicrystalline placement.
    """
    golden_angle = 2 * np.pi / PHI**2  # ≈ 137.5° in radians
    positions = []
    for n in range(n_sites):
        r = base_radius * (1 + n * 0.3)  # Gradual radial expansion
        theta = n * golden_angle
        positions.append((r * np.cos(theta), r * np.sin(theta)))
    return positions

def create_pinning_potential(X, Y, pin_depth, pin_width, arrangement='fibonacci'):
    """
    Create a 2D pinning potential from positioned Gaussian wells.
    
    V_pin(x,y) = -depth * Σ exp(-|r - r_i|² / (2 * width²))
    
    Three arrangements tested:
    - 'fibonacci': golden-angle positions (quasicrystalline)
    - 'triangular': periodic triangular lattice (crystalline)
    - 'none': no pinning (control)
    """
    V = np.zeros_like(X)
    
    if arrangement == 'none':
        return V, []
    
    if arrangement == 'fibonacci':
        # Place 3 primary pinning sites at the vortex core positions
        # (where the Milnor polynomial has its zeros)
        # Plus secondary sites in golden-angle pattern
        
        # The trefoil imprint places 3 vortices near the origin
        # We need to pin near where they form
        n_primary = 3
        n_secondary = 9
        
        # Primary sites: 3-fold symmetric, matching trefoil
        primary = []
        for k in range(n_primary):
            angle = 2 * np.pi * k / 3 + np.pi/6  # 120° spacing
            r = 0.8  # Match the initial vortex core radius
            primary.append((r * np.cos(angle), r * np.sin(angle)))
        
        # Secondary sites: golden angle spiral around the primary
        secondary = golden_angle_positions(n_secondary, base_radius=1.5)
        
        positions = primary + secondary
        
    elif arrangement == 'triangular':
        # Regular triangular lattice for comparison
        spacing = 1.5
        positions = []
        for i in range(-3, 4):
            for j in range(-3, 4):
                px = i * spacing + (j % 2) * spacing / 2
                py = j * spacing * np.sqrt(3) / 2
                if px**2 + py**2 < (L/3)**2:
                    positions.append((px, py))
    
    for (px, py) in positions:
        V += -pin_depth * np.exp(-((X - px)**2 + (Y - py)**2) / (2 * pin_width**2))
    
    return V, positions

# ============================================================
# MILNOR TREFOIL PHASE (same as v1)
# ============================================================
def milnor_trefoil_phase(X, Y):
    z = (X + 1j * Y)
    w = np.conj(z) * 0.5
    f = z**3 - w**2
    return np.angle(f)

def initialize_wavefunction(X, Y):
    r = np.sqrt(X**2 + Y**2)
    rho = mu * np.exp(-0.5 * (r / (L/3))**4)
    theta = milnor_trefoil_phase(X, Y)
    psi = np.sqrt(rho) * np.exp(1j * theta)
    return psi

# ============================================================
# GP EVOLUTION WITH PINNING
# ============================================================
def gpe_step_pinned(psi, V_pin, dt):
    """Split-step with pinning potential included."""
    rho = np.abs(psi)**2
    V_total = g * rho - mu + V_pin  # Pinning added to potential
    psi = psi * np.exp(-1j * V_total * dt / 2)
    
    psi_k = np.fft.fft2(psi)
    psi_k = psi_k * np.exp(-1j * K2 * dt / 2)
    psi = np.fft.ifft2(psi_k)
    
    rho = np.abs(psi)**2
    V_total = g * rho - mu + V_pin
    psi = psi * np.exp(-1j * V_total * dt / 2)
    
    return psi

# ============================================================
# COHOMOLOGICAL AUDIT (same as v1)
# ============================================================
def compute_phase_gradient(psi):
    rho = np.abs(psi)**2 + 1e-20
    psi_k = np.fft.fft2(psi)
    dpsi_dx = np.fft.ifft2(1j * KX * psi_k)
    dpsi_dy = np.fft.ifft2(1j * KY * psi_k)
    vx = np.imag(np.conj(psi) * dpsi_dx) / rho
    vy = np.imag(np.conj(psi) * dpsi_dy) / rho
    return vx, vy

def winding_number_contour(vx, vy, cx, cy, radius, n_points=200):
    theta_pts = np.linspace(0, 2*np.pi, n_points, endpoint=False)
    dtheta = 2 * np.pi / n_points
    integral = 0.0
    for t in theta_pts:
        px = cx + radius * np.cos(t)
        py = cy + radius * np.sin(t)
        dlx = -radius * np.sin(t) * dtheta
        dly =  radius * np.cos(t) * dtheta
        ix_f = (px + L/2) / dx
        iy_f = (py + L/2) / dx
        ix = int(ix_f) % N
        iy = int(iy_f) % N
        ix1 = (ix + 1) % N
        iy1 = (iy + 1) % N
        fx = ix_f - int(ix_f)
        fy = iy_f - int(iy_f)
        vx_interp = (vx[ix,iy]*(1-fx)*(1-fy) + vx[ix1,iy]*fx*(1-fy) +
                      vx[ix,iy1]*(1-fx)*fy + vx[ix1,iy1]*fx*fy)
        vy_interp = (vy[ix,iy]*(1-fx)*(1-fy) + vy[ix1,iy]*fx*(1-fy) +
                      vy[ix,iy1]*(1-fx)*fy + vy[ix1,iy1]*fx*fy)
        integral += vx_interp * dlx + vy_interp * dly
    return integral / (2 * np.pi)

def audit_winding(psi):
    vx, vy = compute_phase_gradient(psi)
    radii = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
    return {f"r={r:.1f}": round(winding_number_contour(vx, vy, 0, 0, r), 4) for r in radii}

# ============================================================
# COMPARATIVE EXPERIMENT
# ============================================================
def run_experiment(arrangement, pin_depth, pin_width=0.3):
    """Run GP evolution with specified pinning and return winding time series."""
    
    V_pin, pin_positions = create_pinning_potential(X, Y, pin_depth, pin_width, arrangement)
    psi = initialize_wavefunction(X, Y)
    
    results = {
        "arrangement": arrangement,
        "pin_depth": pin_depth,
        "pin_width": pin_width,
        "n_pin_sites": len(pin_positions),
        "time": [],
        "w_r05": [], "w_r10": [], "w_r15": [], 
        "w_r20": [], "w_r25": [], "w_r30": [],
    }
    
    # Initial audit
    w = audit_winding(psi)
    results["time"].append(0.0)
    for key in ["r=0.5","r=1.0","r=1.5","r=2.0","r=2.5","r=3.0"]:
        short = "w_" + key.replace("=","").replace(".","")
        results[short].append(w[key])
    
    for step in range(1, N_STEPS + 1):
        psi = gpe_step_pinned(psi, V_pin, dt)
        
        if step % AUDIT_INTERVAL == 0:
            w = audit_winding(psi)
            results["time"].append(round(step * dt, 4))
            for key in ["r=0.5","r=1.0","r=1.5","r=2.0","r=2.5","r=3.0"]:
                short = "w_" + key.replace("=","").replace(".","")
                results[short].append(w[key])
    
    return results

def main():
    print("=" * 65)
    print("HELIUM LOOM v2: PINNING LATTICE COMPARATIVE EXPERIMENT")
    print("=" * 65)
    
    experiments = [
        ("none",       0.0,  "CONTROL: No pinning"),
        ("fibonacci",  5.0,  "Fibonacci φ-lattice, depth=5"),
        ("fibonacci", 20.0,  "Fibonacci φ-lattice, depth=20"),
        ("fibonacci", 50.0,  "Fibonacci φ-lattice, depth=50"),
        ("triangular", 20.0, "Triangular periodic, depth=20"),
    ]
    
    all_results = []
    
    for arrangement, depth, label in experiments:
        print(f"\n--- {label} ---")
        res = run_experiment(arrangement, depth)
        
        w_init = res["w_r10"][0]
        w_final = res["w_r10"][-1]
        drift = abs(w_final - w_init)
        
        # Check if winding stayed near 3 throughout
        w_series = res["w_r10"]
        near_3_count = sum(1 for w in w_series if abs(w - 3.0) < 0.5)
        total = len(w_series)
        retention = near_3_count / total * 100
        
        print(f"  W(r=1) initial: {w_init:+.4f}")
        print(f"  W(r=1) final:   {w_final:+.4f}")
        print(f"  Drift:          {drift:.4f}")
        print(f"  W≈3 retention:  {retention:.1f}% ({near_3_count}/{total} audits)")
        
        if retention > 90:
            print(f"  STATUS: LOCK HOLDING ✓")
        elif retention > 50:
            print(f"  STATUS: LOCK DEGRADING ⚠")
        else:
            print(f"  STATUS: LOCK BROKEN ✗")
        
        res["label"] = label
        res["retention"] = retention
        res["drift"] = drift
        all_results.append(res)
    
    # Summary
    print("\n" + "=" * 65)
    print("COMPARATIVE SUMMARY")
    print("=" * 65)
    print(f"{'Experiment':<40} {'Retention':>10} {'Drift':>8}")
    print("-" * 60)
    for res in all_results:
        print(f"{res['label']:<40} {res['retention']:>9.1f}% {res['drift']:>8.4f}")
    
    # Save
    with open("/home/claude/pinning_results.json", 'w') as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\nResults saved to /home/claude/pinning_results.json")
    return all_results

if __name__ == "__main__":
    main()
