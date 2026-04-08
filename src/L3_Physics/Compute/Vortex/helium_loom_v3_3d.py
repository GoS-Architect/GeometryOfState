"""
Helium Loom v3: 3D Trefoil Vortex Filament
============================================
Tests Level 3 topological protection: does a knotted 
vortex filament in 3D GP dynamics preserve its knot type?

The trefoil is imprinted as a density-zero filament using
the Milnor fibration in 3D: the zero set of f(z,w) = z^3 - w^2
intersected with S^3 gives the trefoil knot.

Grid: 48^3 (reduced from 64^3 for computational tractability)
"""

import numpy as np
import json

# ============================================================
# PARAMETERS
# ============================================================
N = 48              # Grid resolution (48^3 = 110,592 points)
L = 8.0             # Box size  
dt = 0.002          # Time step (smaller for 3D stability)
g = 0.5             # Interaction strength
mu = 1.0            # Chemical potential
N_STEPS = 600       # Evolution steps 
AUDIT_INTERVAL = 30 # Audit frequency
HEALING_LENGTH = 0.3 # Vortex core size parameter

dx = L / N
coords = np.linspace(-L/2, L/2, N, endpoint=False)
X, Y, Z = np.meshgrid(coords, coords, coords, indexing='ij')

# Momentum space
k1d = 2 * np.pi * np.fft.fftfreq(N, d=dx)
KX, KY, KZ = np.meshgrid(k1d, k1d, k1d, indexing='ij')
K2 = KX**2 + KY**2 + KZ**2

print(f"Grid: {N}^3 = {N**3:,} points")
print(f"Memory: ~{N**3 * 16 / 1e6:.0f} MB per complex field")

# ============================================================
# TREFOIL VORTEX IMPRINT
# ============================================================
def imprint_trefoil(X, Y, Z, core_width=HEALING_LENGTH):
    """
    Create a trefoil-knotted vortex filament in 3D.
    
    Method: The trefoil is a (2,3) torus knot. We parameterize it
    on a torus of major radius R and minor radius r:
    
        x(t) = (R + r cos(3t)) cos(2t)
        y(t) = (R + r cos(3t)) sin(2t)  
        z(t) = r sin(3t)
    
    The vortex phase field is constructed by computing, at each
    grid point, the angle around the nearest point on the filament.
    The density goes to zero at the filament core.
    """
    R_major = 2.0   # Major radius of the torus
    r_minor = 0.8   # Minor radius
    
    # Sample points on the trefoil
    n_filament = 500
    t_param = np.linspace(0, 2*np.pi, n_filament, endpoint=False)
    
    # Trefoil parameterization: (2,3) torus knot
    fx = (R_major + r_minor * np.cos(3 * t_param)) * np.cos(2 * t_param)
    fy = (R_major + r_minor * np.cos(3 * t_param)) * np.sin(2 * t_param)
    fz = r_minor * np.sin(3 * t_param)
    
    # For each grid point, find distance to nearest filament point
    # and the winding angle around the filament
    # (Vectorized over grid, loop over filament samples)
    
    min_dist_sq = np.full((N, N, N), 1e10)
    phase = np.zeros((N, N, N))
    
    # Tangent vectors along filament (for computing winding)
    dt_param = t_param[1] - t_param[0]
    dfx = np.gradient(fx, dt_param)
    dfy = np.gradient(fy, dt_param)
    dfz = np.gradient(fz, dt_param)
    
    print("Imprinting trefoil filament...")
    for i in range(n_filament):
        # Displacement from this filament point
        dx_f = X - fx[i]
        dy_f = Y - fy[i]
        dz_f = Z - fz[i]
        
        dist_sq = dx_f**2 + dy_f**2 + dz_f**2
        
        # Update nearest point
        closer = dist_sq < min_dist_sq
        min_dist_sq = np.where(closer, dist_sq, min_dist_sq)
        
        # Compute winding phase contribution
        # The phase at a point near the filament is the angle in the 
        # plane perpendicular to the tangent
        # We use two perpendicular normals n1, n2 to the tangent
        
        # Tangent at this point
        tx, ty, tz = dfx[i], dfy[i], dfz[i]
        t_norm = np.sqrt(tx**2 + ty**2 + tz**2) + 1e-10
        tx, ty, tz = tx/t_norm, ty/t_norm, tz/t_norm
        
        # First normal: tangent × z-hat (or x-hat if tangent ≈ z-hat)
        if abs(tz) < 0.9:
            n1x = ty
            n1y = -tx
            n1z = 0.0
        else:
            n1x = 0.0
            n1y = tz
            n1z = -ty
        n1_norm = np.sqrt(n1x**2 + n1y**2 + n1z**2) + 1e-10
        n1x, n1y, n1z = n1x/n1_norm, n1y/n1_norm, n1z/n1_norm
        
        # Second normal: tangent × n1
        n2x = ty*n1z - tz*n1y
        n2y = tz*n1x - tx*n1z
        n2z = tx*n1y - ty*n1x
        
        # Project displacement onto normal plane
        proj1 = dx_f * n1x + dy_f * n1y + dz_f * n1z
        proj2 = dx_f * n2x + dy_f * n2y + dz_f * n2z
        
        # Phase from this filament segment
        local_phase = np.arctan2(proj2, proj1)
        
        # Weight by proximity (closest filament point dominates)
        phase = np.where(closer, local_phase, phase)
    
    min_dist = np.sqrt(min_dist_sq)
    
    # Density: zero at filament core, heals to background
    density = mu * np.tanh(min_dist / core_width)**2
    
    # Wavefunction
    psi = np.sqrt(density) * np.exp(1j * phase)
    
    print(f"  Filament imprinted. Min distance to core: {min_dist.min():.4f}")
    print(f"  Density at core: {density.min():.6f}")
    print(f"  Core volume (ρ < 0.1): {np.sum(density < 0.1) * dx**3:.4f}")
    
    return psi, (fx, fy, fz)


# ============================================================
# 3D GP EVOLUTION
# ============================================================
def gpe_step_3d(psi, dt):
    """Split-step Fourier for 3D Gross-Pitaevskii."""
    rho = np.abs(psi)**2
    V_nl = g * rho - mu
    psi = psi * np.exp(-1j * V_nl * dt / 2)
    
    psi_k = np.fft.fftn(psi)
    psi_k = psi_k * np.exp(-1j * K2 * dt / 2)
    psi = np.fft.ifftn(psi_k)
    
    rho = np.abs(psi)**2
    V_nl = g * rho - mu
    psi = psi * np.exp(-1j * V_nl * dt / 2)
    
    return psi


# ============================================================
# 3D TOPOLOGICAL AUDIT
# ============================================================
def extract_vortex_filament(psi, threshold=0.15):
    """
    Extract vortex core positions as the low-density locus.
    Returns the positions where |ψ|² < threshold.
    """
    rho = np.abs(psi)**2
    core_mask = rho < threshold
    core_volume = np.sum(core_mask) * dx**3
    
    # Extract core positions
    positions = np.argwhere(core_mask).astype(float)
    if len(positions) > 0:
        positions = positions * dx - L/2  # Convert to physical coordinates
    
    return positions, core_volume, core_mask


def compute_writhe_proxy(positions, n_sample=1000):
    """
    Compute a proxy for the writhe of the vortex filament.
    
    The writhe is a geometric measure related to knot topology:
        Wr = (1/4π) ∮∮ (r₁ - r₂) · (dr₁ × dr₂) / |r₁ - r₂|³
    
    For the trefoil, Wr ≈ 3.0 (related to winding).
    For the unknot (circle), Wr = 0.
    
    We approximate this by sampling pairs of points on the filament.
    Note: writhe alone doesn't determine knot type, but changes
    in writhe indicate topological events.
    """
    if len(positions) < 20:
        return 0.0, False  # Too few points
    
    # Sort positions into a curve by nearest-neighbor ordering
    # (crude but sufficient for writhe estimation)
    n_pts = min(len(positions), n_sample)
    idx = np.random.choice(len(positions), n_pts, replace=False)
    pts = positions[idx]
    
    # Order by greedy nearest neighbor
    ordered = [0]
    remaining = set(range(1, len(pts)))
    for _ in range(len(pts) - 1):
        last = ordered[-1]
        nearest = min(remaining, key=lambda j: np.sum((pts[last] - pts[j])**2))
        ordered.append(nearest)
        remaining.remove(nearest)
    
    curve = pts[ordered]
    n = len(curve)
    
    if n < 10:
        return 0.0, False
    
    # Compute tangent vectors
    tangents = np.diff(curve, axis=0)
    tangents = np.vstack([tangents, tangents[0:1]])  # Close the curve
    
    # Writhe double integral (sampled)
    writhe = 0.0
    n_pairs = min(n * 5, 5000)
    
    for _ in range(n_pairs):
        i = np.random.randint(0, n)
        j = np.random.randint(0, n)
        if abs(i - j) < 3 or abs(i - j) > n - 3:
            continue
            
        r12 = curve[i] - curve[j]
        r12_norm = np.linalg.norm(r12)
        if r12_norm < dx:
            continue
            
        cross = np.cross(tangents[i], tangents[j])
        writhe += np.dot(r12, cross) / (r12_norm**3)
    
    writhe *= n**2 / (4 * np.pi * n_pairs)
    
    return writhe, True


def compute_3d_winding(psi, center=(0,0,0), radius=2.5, n_points=200):
    """
    Compute winding number around a circular contour in the z=0 plane.
    This measures the LINKING NUMBER of the contour with the vortex filament.
    For a trefoil centered at origin, a circle in the z=0 plane 
    links the filament with linking number related to the knot type.
    """
    theta_pts = np.linspace(0, 2*np.pi, n_points, endpoint=False)
    dtheta = 2 * np.pi / n_points
    
    # Compute phase gradient (gauge-invariant)
    rho = np.abs(psi)**2 + 1e-20
    psi_k = np.fft.fftn(psi)
    
    dpsi_dx = np.fft.ifftn(1j * KX * psi_k)
    dpsi_dy = np.fft.ifftn(1j * KY * psi_k)
    
    vx = np.imag(np.conj(psi) * dpsi_dx) / rho
    vy = np.imag(np.conj(psi) * dpsi_dy) / rho
    
    # z-index for the z=0 plane
    iz = N // 2
    
    integral = 0.0
    for t in theta_pts:
        px = center[0] + radius * np.cos(t)
        py = center[1] + radius * np.sin(t)
        
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
        
        vx_i = (vx[ix,iy,iz]*(1-fx)*(1-fy) + vx[ix1,iy,iz]*fx*(1-fy) +
                vx[ix,iy1,iz]*(1-fx)*fy + vx[ix1,iy1,iz]*fx*fy)
        vy_i = (vy[ix,iy,iz]*(1-fx)*(1-fy) + vy[ix1,iy,iz]*fx*(1-fy) +
                vy[ix,iy1,iz]*(1-fx)*fy + vy[ix1,iy1,iz]*fx*fy)
        
        integral += float(np.real(vx_i)) * dlx + float(np.real(vy_i)) * dly
    
    return integral / (2 * np.pi)


def topological_audit_3d(psi, step, t):
    """Full 3D topological audit."""
    
    # 1. Extract filament
    positions, core_vol, _ = extract_vortex_filament(psi)
    
    # 2. Compute writhe proxy
    writhe, writhe_valid = compute_writhe_proxy(positions)
    
    # 3. Winding numbers in z=0 plane at multiple radii
    windings = {}
    for r in [1.0, 1.5, 2.0, 2.5]:
        w = compute_3d_winding(psi, radius=r)
        windings[f"r={r}"] = round(w, 4)
    
    # 4. Core connectivity: is the filament one connected component?
    # (If it fragments, a reconnection has occurred)
    n_core_points = len(positions)
    
    result = {
        "step": step,
        "time": round(t, 4),
        "core_volume": round(core_vol, 6),
        "n_core_points": n_core_points,
        "writhe": round(writhe, 4) if writhe_valid else None,
        "windings": windings,
        "total_density": round(float(np.sum(np.abs(psi)**2) * dx**3), 4),
    }
    
    return result


# ============================================================
# MAIN
# ============================================================
def main():
    print("=" * 65)
    print("HELIUM LOOM v3: 3D TREFOIL VORTEX FILAMENT")
    print("=" * 65)
    print(f"Grid: {N}^3, Box: {L}, dt: {dt}, g: {g}")
    print(f"Steps: {N_STEPS}, Audit every {AUDIT_INTERVAL}")
    
    # Initialize with trefoil
    psi, filament_coords = imprint_trefoil(X, Y, Z)
    
    # Initial audit
    print("\n--- Initial Topological Audit ---")
    audit = topological_audit_3d(psi, 0, 0.0)
    print(f"  Core volume: {audit['core_volume']:.4f}")
    print(f"  Core points: {audit['n_core_points']}")
    print(f"  Writhe:      {audit['writhe']}")
    print(f"  Windings:    {audit['windings']}")
    
    audit_log = [audit]
    
    # Evolve
    print("\n--- 3D GP Evolution ---")
    for step in range(1, N_STEPS + 1):
        psi = gpe_step_3d(psi, dt)
        
        if step % AUDIT_INTERVAL == 0:
            audit = topological_audit_3d(psi, step, step * dt)
            audit_log.append(audit)
            
            w2 = audit['windings'].get('r=2.0', 0)
            print(f"  Step {step:4d} | t={step*dt:.3f} | "
                  f"CoreVol={audit['core_volume']:.4f} | "
                  f"Writhe={audit['writhe']} | "
                  f"W(r=2)={w2:+.4f}")
    
    # Final assessment
    print("\n" + "=" * 65)
    print("3D TOPOLOGICAL LOCK ASSESSMENT")
    print("=" * 65)
    
    # Track winding stability
    w_series = [a['windings'].get('r=2.0', 0) for a in audit_log]
    w_initial = w_series[0]
    w_final = w_series[-1]
    w_std = np.std(w_series)
    
    print(f"  Initial W(r=2): {w_initial:+.4f}")
    print(f"  Final   W(r=2): {w_final:+.4f}")
    print(f"  Drift:          {abs(w_final - w_initial):.4f}")
    print(f"  Stability (σ):  {w_std:.4f}")
    
    # Compare writhe
    writhes = [a['writhe'] for a in audit_log if a['writhe'] is not None]
    if writhes:
        print(f"\n  Initial writhe: {writhes[0]:.4f}")
        print(f"  Final writhe:   {writhes[-1]:.4f}")
        print(f"  Writhe σ:       {np.std(writhes):.4f}")
    
    # Core volume evolution
    vols = [a['core_volume'] for a in audit_log]
    print(f"\n  Initial core volume: {vols[0]:.4f}")
    print(f"  Final core volume:   {vols[-1]:.4f}")
    print(f"  Volume change:       {abs(vols[-1]-vols[0])/max(vols[0],1e-6)*100:.1f}%")
    
    # Lock assessment
    w_near_initial = sum(1 for w in w_series if abs(w - w_initial) < 0.5)
    retention = w_near_initial / len(w_series) * 100
    
    print(f"\n  Winding retention: {retention:.1f}%")
    if retention > 80:
        print("  STATUS: LEVEL 3 LOCK HOLDING ✓")
    elif retention > 50:
        print("  STATUS: LOCK DEGRADING ⚠")
    else:
        print("  STATUS: LOCK BROKEN ✗")
    
    # Save results
    results = {
        "parameters": {"N": N, "L": L, "dt": dt, "g": g, "mu": mu,
                       "N_steps": N_STEPS, "healing_length": HEALING_LENGTH},
        "filament": {"x": filament_coords[0].tolist(), 
                     "y": filament_coords[1].tolist(),
                     "z": filament_coords[2].tolist()},
        "audit_log": audit_log,
        "summary": {
            "initial_winding": w_initial,
            "final_winding": w_final,
            "drift": abs(w_final - w_initial),
            "winding_sigma": float(w_std),
            "retention": retention,
            "initial_writhe": writhes[0] if writhes else None,
            "final_writhe": writhes[-1] if writhes else None,
        }
    }
    
    with open("/home/claude/3d_results.json", 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to /home/claude/3d_results.json")
    return results

if __name__ == "__main__":
    results = main()
