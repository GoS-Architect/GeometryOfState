"""
3D GP Solver: Complete READ/WRITE Topological Cycle
=====================================================
Four-phase protocol:

  Phase 0: RELAX   — Imaginary time → GP ground state in trefoil sector
  Phase 1: READ    — Real-time evolution, no perturbation → verify lock holds
  Phase 2: WRITE   — Apply V_splice at geometric crossing → trigger reconnection
  Phase 3: VERIFY  — Real-time after splice → verify new topology persists

The splice potential V_splice is a localized Gaussian pulse at one of
the trefoil's three self-crossing points in projection. It pushes the
two filament strands together, forcing the bivector fields into
anti-parallel annihilation at the X-point.

Success criteria:
  Phase 1: Core volume stable, writhe stable → READ works
  Phase 2: Core volume spikes, writhe changes → WRITE fires
  Phase 3: Core volume re-stabilizes at new value → new state locks

Backend: JAX (@jit, GPU) with NumPy fallback (CPU, reduced resolution)
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional
import json, time, os

try:
    import jax
    import jax.numpy as jnp
    from jax import jit
    HAS_JAX = True
    xp = jnp
    print(f"JAX backend: {jax.devices()[0].device_kind}")
except ImportError:
    HAS_JAX = False
    xp = np
    print("NumPy fallback (CPU)")


# ============================================================
# CONFIGURATION
# ============================================================
@dataclass
class Config:
    # Grid — 128³ on GPU, 48³ on CPU
    N: int = 128 if HAS_JAX else 48
    L: float = 10.0

    # Physics
    g: float = 0.5
    mu: float = 1.0
    healing_length: float = 0.5
    core_width: float = 0.4

    # Trefoil geometry
    R_major: float = 3.0
    r_minor: float = 1.2

    # Phase durations (steps)
    n_relax: int = 1500 if HAS_JAX else 500
    n_read: int = 2000 if HAS_JAX else 600
    n_write: int = 200 if HAS_JAX else 80     # Splice pulse duration
    n_verify: int = 2000 if HAS_JAX else 600

    # Time steps
    dt_imag: float = 0.005
    dt_real: float = 0.001 if HAS_JAX else 0.002

    # Splice parameters
    splice_amplitude: float = 50.0    # Potential depth at X-point
    splice_width: float = 0.8         # Gaussian width of splice pulse
    splice_ramp_steps: int = 30       # Steps to ramp on/off (avoid shock)

    # Audit
    audit_interval: int = 50 if HAS_JAX else 25

    @property
    def dx(self): return self.L / self.N


# ============================================================
# GRID
# ============================================================
def setup_grid(cfg):
    c = np.linspace(-cfg.L/2, cfg.L/2, cfg.N, endpoint=False)
    X, Y, Z = np.meshgrid(c, c, c, indexing='ij')
    k = 2 * np.pi * np.fft.fftfreq(cfg.N, d=cfg.dx)
    KX, KY, KZ = np.meshgrid(k, k, k, indexing='ij')
    K2 = KX**2 + KY**2 + KZ**2
    if HAS_JAX:
        return tuple(jnp.array(a) for a in (X,Y,Z)), jnp.array(K2)
    return (X, Y, Z), K2


# ============================================================
# TREFOIL INITIALIZATION (Biot-Savart)
# ============================================================
def trefoil_curve(n_pts, R, r):
    t = np.linspace(0, 2*np.pi, n_pts, endpoint=False)
    x = (R + r*np.cos(3*t)) * np.cos(2*t)
    y = (R + r*np.cos(3*t)) * np.sin(2*t)
    z = r * np.sin(3*t)
    dx = np.gradient(x, t); dy = np.gradient(y, t); dz = np.gradient(z, t)
    mag = np.sqrt(dx**2+dy**2+dz**2)
    return (x,y,z), (dx/mag, dy/mag, dz/mag), t


def find_crossings(curve_pos, n_pts=500):
    """
    Find approximate self-crossing points of the trefoil in the z=0 projection.
    These are the locations where two filament strands pass near each other.
    A splice potential placed at one of these points will force reconnection.
    """
    fx, fy, fz = curve_pos
    crossings = []

    for i in range(n_pts):
        for j in range(i + n_pts//6, min(i + 5*n_pts//6, n_pts)):
            # Distance in projection (x,y only)
            dxy = np.sqrt((fx[i]-fx[j])**2 + (fy[i]-fy[j])**2)
            # Separation in z
            dz = abs(fz[i] - fz[j])
            if dxy < 0.5 and dz > 0.1:  # Close in xy, separated in z
                mid_x = (fx[i]+fx[j])/2
                mid_y = (fy[i]+fy[j])/2
                mid_z = (fz[i]+fz[j])/2
                crossings.append((mid_x, mid_y, mid_z, dxy, dz, i, j))

    # Cluster nearby crossings and take centroids
    if not crossings:
        return []

    crossings.sort(key=lambda c: (c[0], c[1]))
    clusters = []
    used = set()
    for ci, c in enumerate(crossings):
        if ci in used: continue
        cluster = [c]
        for cj, c2 in enumerate(crossings):
            if cj <= ci or cj in used: continue
            if (c[0]-c2[0])**2 + (c[1]-c2[1])**2 < 1.0:
                cluster.append(c2)
                used.add(cj)
        used.add(ci)
        cx = np.mean([cc[0] for cc in cluster])
        cy = np.mean([cc[1] for cc in cluster])
        cz = np.mean([cc[2] for cc in cluster])
        clusters.append((cx, cy, cz))

    return clusters[:3]  # Trefoil has 3 crossings


def init_biot_savart(cfg, grids):
    (X,Y,Z), K2 = grids
    Xn, Yn, Zn = (np.array(a) if HAS_JAX else a for a in (X,Y,Z))

    n_fil = 500
    pos, tan, _ = trefoil_curve(n_fil, cfg.R_major, cfg.r_minor)
    fx,fy,fz = pos; tx,ty,tz = tan

    # Find crossing points for later splice
    crossings = find_crossings(pos, n_fil)
    print(f"  Trefoil crossings found: {len(crossings)}")
    for i, (cx,cy,cz) in enumerate(crossings):
        print(f"    Crossing {i}: ({cx:.2f}, {cy:.2f}, {cz:.2f})")

    # Phase field from nearest-filament winding
    print("  Computing phase field from Biot-Savart...")
    min_dist = np.full_like(Xn, 1e10)
    phase = np.zeros_like(Xn)

    for i in range(n_fil):
        dx = Xn-fx[i]; dy = Yn-fy[i]; dz = Zn-fz[i]
        dist = np.sqrt(dx**2+dy**2+dz**2)
        closer = dist < min_dist

        if abs(tz[i]) < 0.9:
            n1x,n1y,n1z = ty[i],-tx[i],0.0
        else:
            n1x,n1y,n1z = 0.0,tz[i],-ty[i]
        nm = np.sqrt(n1x**2+n1y**2+n1z**2)+1e-10
        n1x/=nm; n1y/=nm; n1z/=nm

        n2x = ty[i]*n1z-tz[i]*n1y
        n2y = tz[i]*n1x-tx[i]*n1z
        n2z = tx[i]*n1y-ty[i]*n1x

        p1 = dx*n1x+dy*n1y+dz*n1z
        p2 = dx*n2x+dy*n2y+dz*n2z

        min_dist = np.where(closer, dist, min_dist)
        phase = np.where(closer, np.arctan2(p2, p1), phase)

    rho = cfg.mu * np.tanh(min_dist/cfg.core_width)**2
    r_edge = np.sqrt(Xn**2+Yn**2+Zn**2)
    rho *= np.exp(-0.5*(r_edge/(cfg.L/3))**4)

    psi = np.sqrt(np.maximum(rho, 0)) * np.exp(1j*phase)
    if HAS_JAX: psi = jnp.array(psi)

    print(f"  Core volume: {np.sum(rho < 0.1*cfg.mu)*cfg.dx**3:.1f}")
    return psi, crossings


# ============================================================
# SPLICE POTENTIAL
# ============================================================
def make_splice_potential(cfg, grids, crossing_point, amplitude, width):
    """
    V_splice(r) = -A * exp(-|r - r_cross|² / (2σ²))

    A localized attractive well at the crossing point.
    This pulls both filament strands toward the crossing,
    forcing the anti-parallel bivector fields into collision.

    The amplitude must exceed the core energy to trigger
    reconnection (i.e., to discharge h_energy > E_reconnect).
    """
    (X,Y,Z), _ = grids
    if HAS_JAX:
        Xn,Yn,Zn = np.array(X),np.array(Y),np.array(Z)
    else:
        Xn,Yn,Zn = X,Y,Z

    cx, cy, cz = crossing_point
    r2 = (Xn-cx)**2 + (Yn-cy)**2 + (Zn-cz)**2
    V = -amplitude * np.exp(-r2 / (2*width**2))

    if HAS_JAX: V = jnp.array(V)
    return V


# ============================================================
# GP KERNELS
# ============================================================
def make_step_real(K2, dt, g, mu):
    prop = xp.exp(-1j * K2 * dt / 2)
    def step(psi, V_ext=None):
        rho = xp.abs(psi)**2
        V = g*rho - mu
        if V_ext is not None: V = V + V_ext
        psi = psi * xp.exp(-1j*V*dt/2)
        if HAS_JAX:
            psi = jnp.fft.ifftn(jnp.fft.fftn(psi)*prop)
        else:
            psi = np.fft.ifftn(np.fft.fftn(psi)*prop)
        rho = xp.abs(psi)**2
        V = g*rho - mu
        if V_ext is not None: V = V + V_ext
        return psi * xp.exp(-1j*V*dt/2)
    return step

def make_step_imag(K2, dt, g, mu):
    prop = xp.exp(-K2 * dt / 2)
    def step(psi, target_N):
        rho = xp.abs(psi)**2
        V = g*rho - mu
        psi = psi * xp.exp(-V*dt/2)
        if HAS_JAX:
            psi = jnp.fft.ifftn(jnp.fft.fftn(psi)*prop)
        else:
            psi = np.fft.ifftn(np.fft.fftn(psi)*prop)
        rho = xp.abs(psi)**2
        V = g*rho - mu
        psi = psi * xp.exp(-V*dt/2)
        cur = xp.sum(xp.abs(psi)**2)
        return psi * xp.sqrt(target_N / (cur + 1e-30))
    return step


# ============================================================
# DIAGNOSTICS
# ============================================================
def audit(psi, cfg, K2_np, label=""):
    psi_np = np.array(psi) if HAS_JAX else psi
    rho = np.abs(psi_np)**2

    # Core volume
    core_mask = rho < 0.15 * cfg.mu
    core_vol = np.sum(core_mask) * cfg.dx**3
    n_core = int(np.sum(core_mask))

    # Energy
    pk = np.fft.fftn(psi_np)
    E_kin = 0.5*np.sum(K2_np*np.abs(pk)**2)/cfg.N**3 * cfg.dx**3
    E_int = 0.5*cfg.g*np.sum(rho**2)*cfg.dx**3
    E_pot = -cfg.mu*np.sum(rho)*cfg.dx**3
    E = float(E_kin + E_int + E_pot)

    # Density at known crossing points (monitor reconnection)
    ix0, iy0, iz0 = cfg.N//2, cfg.N//2, cfg.N//2
    rho_center = float(rho[ix0, iy0, iz0])

    # Writhe (subsampled for speed)
    positions = np.argwhere(core_mask).astype(float) * cfg.dx - cfg.L/2
    writhe = 0.0
    writhe_valid = False
    if len(positions) > 50:
        n = min(len(positions), 800)
        idx = np.random.choice(len(positions), n, replace=False)
        pts = positions[idx]
        ordered = [0]; remaining = set(range(1,n))
        for _ in range(min(n-1, 500)):
            if not remaining: break
            last = ordered[-1]
            nearest = min(remaining, key=lambda j: np.sum((pts[last]-pts[j])**2))
            ordered.append(nearest); remaining.remove(nearest)
        curve = pts[ordered[:min(len(ordered),500)]]
        if len(curve) > 20:
            tangents = np.diff(curve, axis=0)
            tangents = np.vstack([tangents, tangents[:1]])
            nc = len(curve)
            w = 0.0; np_pairs = min(nc*3, 3000)
            for _ in range(np_pairs):
                i,j = np.random.randint(0,nc), np.random.randint(0,nc)
                if abs(i-j)<3 or abs(i-j)>nc-3: continue
                r12 = curve[i]-curve[j]; rn = np.linalg.norm(r12)
                if rn < 0.3: continue
                w += np.dot(r12, np.cross(tangents[i],tangents[j]))/rn**3
            writhe = w * nc**2 / (4*np.pi*np_pairs)
            writhe_valid = True

    return {
        "energy": round(E, 4),
        "core_volume": round(core_vol, 2),
        "n_core": n_core,
        "writhe": round(writhe, 2) if writhe_valid else None,
        "rho_center": round(rho_center, 6),
    }


# ============================================================
# MAIN: FOUR-PHASE PROTOCOL
# ============================================================
def run():
    cfg = Config()

    print("="*65)
    print("3D GP: COMPLETE READ/WRITE TOPOLOGICAL CYCLE")
    print("="*65)
    print(f"Grid: {cfg.N}³  Backend: {'JAX' if HAS_JAX else 'NumPy'}")
    pph = cfg.healing_length / cfg.dx
    print(f"Resolution: {pph:.1f} pts/ξ {'✓' if pph>=3 else '⚠ (need ≥5)'}")

    grids = setup_grid(cfg)
    (X,Y,Z), K2 = grids
    K2_np = np.array(K2) if HAS_JAX else K2

    # ── Initialize ──
    print("\n── Initialization: Biot-Savart Trefoil ──")
    psi, crossings = init_biot_savart(cfg, grids)
    N_particles = float(xp.sum(xp.abs(psi)**2))

    log = []
    def record(phase, step, t, extra=None):
        a = audit(psi, cfg, K2_np)
        a.update({"phase": phase, "step": step, "time": round(t,4)})
        if extra: a.update(extra)
        log.append(a)
        return a

    # ── Phase 0: RELAX ──
    print(f"\n── Phase 0: IMAGINARY TIME RELAXATION ({cfg.n_relax} steps) ──")
    imag = make_step_imag(K2, cfg.dt_imag, cfg.g, cfg.mu)
    a0 = record("relax", 0, 0)
    print(f"  Initial E={a0['energy']:.1f} CoreVol={a0['core_volume']:.1f}")

    for s in range(1, cfg.n_relax+1):
        psi = imag(psi, N_particles)
        if s % cfg.audit_interval == 0:
            a = record("relax", s, s*cfg.dt_imag)
            if s % (cfg.audit_interval*4) == 0:
                print(f"  Step {s:5d} E={a['energy']:.1f} CoreVol={a['core_volume']:.1f}")

    a_relaxed = record("relax", cfg.n_relax, cfg.n_relax*cfg.dt_imag)
    print(f"  Relaxed E={a_relaxed['energy']:.1f} CoreVol={a_relaxed['core_volume']:.1f}")

    # ── Phase 1: READ (stability hold) ──
    print(f"\n── Phase 1: READ STABILITY ({cfg.n_read} steps) ──")
    real = make_step_real(K2, cfg.dt_real, cfg.g, cfg.mu)
    t_offset = 0.0

    read_entries = []
    for s in range(1, cfg.n_read+1):
        psi = real(psi)
        if s % cfg.audit_interval == 0:
            a = record("read", s, t_offset + s*cfg.dt_real)
            read_entries.append(a)
            if s % (cfg.audit_interval*4) == 0:
                w_str = f"Wr={a['writhe']:.1f}" if a['writhe'] is not None else "Wr=N/A"
                print(f"  Step {s:5d} E={a['energy']:.2f} CoreVol={a['core_volume']:.1f} {w_str}")

    t_offset += cfg.n_read * cfg.dt_real

    # Read assessment
    vols_read = [e['core_volume'] for e in read_entries]
    vol_drift_read = abs(vols_read[-1]-vols_read[0]) / (vols_read[0]+1e-10) * 100
    print(f"  READ drift: CoreVol {vols_read[0]:.1f}→{vols_read[-1]:.1f} ({vol_drift_read:.1f}%)")

    # ── Phase 2: WRITE (splice) ──
    print(f"\n── Phase 2: WRITE — TOPOLOGICAL SPLICE ({cfg.n_write} steps) ──")

    if crossings:
        splice_point = crossings[0]  # Use first crossing
        print(f"  Target crossing: ({splice_point[0]:.2f}, {splice_point[1]:.2f}, {splice_point[2]:.2f})")
    else:
        # Fallback: aim at a likely crossing region
        splice_point = (cfg.R_major * 0.5, 0.0, 0.0)
        print(f"  No crossings found, targeting ({splice_point[0]:.1f}, {splice_point[1]:.1f}, {splice_point[2]:.1f})")

    V_splice_full = make_splice_potential(cfg, grids, splice_point,
                                           cfg.splice_amplitude, cfg.splice_width)

    write_entries = []
    for s in range(1, cfg.n_write+1):
        # Smooth ramp: on for first ramp_steps, full in middle, off for last ramp_steps
        if s <= cfg.splice_ramp_steps:
            ramp = s / cfg.splice_ramp_steps
        elif s >= cfg.n_write - cfg.splice_ramp_steps:
            ramp = (cfg.n_write - s) / cfg.splice_ramp_steps
        else:
            ramp = 1.0

        V_current = V_splice_full * ramp
        psi = real(psi, V_current)

        if s % (cfg.audit_interval // 2) == 0:
            a = record("write", s, t_offset + s*cfg.dt_real,
                       {"splice_ramp": round(ramp, 3)})
            write_entries.append(a)
            w_str = f"Wr={a['writhe']:.1f}" if a['writhe'] is not None else "Wr=N/A"
            print(f"  Step {s:4d} ramp={ramp:.2f} E={a['energy']:.2f} "
                  f"CoreVol={a['core_volume']:.1f} ρ(0)={a['rho_center']:.4f} {w_str}")

    t_offset += cfg.n_write * cfg.dt_real

    # ── Phase 3: VERIFY (post-splice stability) ──
    print(f"\n── Phase 3: VERIFY POST-SPLICE ({cfg.n_verify} steps) ──")

    verify_entries = []
    for s in range(1, cfg.n_verify+1):
        psi = real(psi)
        if s % cfg.audit_interval == 0:
            a = record("verify", s, t_offset + s*cfg.dt_real)
            verify_entries.append(a)
            if s % (cfg.audit_interval*4) == 0:
                w_str = f"Wr={a['writhe']:.1f}" if a['writhe'] is not None else "Wr=N/A"
                print(f"  Step {s:5d} E={a['energy']:.2f} CoreVol={a['core_volume']:.1f} {w_str}")

    # ── ASSESSMENT ──
    print("\n" + "="*65)
    print("COMPLETE READ/WRITE CYCLE ASSESSMENT")
    print("="*65)

    # READ assessment
    print("\n  ── READ (Phase 1) ──")
    vr = [e['core_volume'] for e in read_entries]
    print(f"  Core volume: {vr[0]:.1f} → {vr[-1]:.1f} "
          f"(drift: {abs(vr[-1]-vr[0])/(vr[0]+1e-10)*100:.1f}%)")
    wr_read = [e['writhe'] for e in read_entries if e['writhe'] is not None]
    if wr_read:
        print(f"  Writhe: {wr_read[0]:.1f} → {wr_read[-1]:.1f} (σ={np.std(wr_read):.1f})")
    er = [e['energy'] for e in read_entries]
    print(f"  Energy: {er[0]:.2f} → {er[-1]:.2f}")

    read_stable = abs(vr[-1]-vr[0])/(vr[0]+1e-10) < 0.1
    print(f"  STATUS: {'LOCK HOLDING ✓' if read_stable else 'LOCK DEGRADING ⚠'}")

    # WRITE assessment
    print("\n  ── WRITE (Phase 2) ──")
    vw = [e['core_volume'] for e in write_entries]
    ew = [e['energy'] for e in write_entries]
    print(f"  Core volume: {vw[0]:.1f} → {vw[-1]:.1f}")
    print(f"  Energy: {ew[0]:.2f} → {ew[-1]:.2f} "
          f"(injected: {ew[-1]-ew[0]:.2f})")
    wr_write = [e['writhe'] for e in write_entries if e['writhe'] is not None]
    if wr_write:
        print(f"  Writhe: {wr_write[0]:.1f} → {wr_write[-1]:.1f}")

    write_fired = abs(ew[-1]-ew[0]) > 1.0 or abs(vw[-1]-vw[0])/(vw[0]+1e-10) > 0.05
    print(f"  STATUS: {'SPLICE FIRED ✓' if write_fired else 'SPLICE DID NOT FIRE ⚠'}")

    # VERIFY assessment
    print("\n  ── VERIFY (Phase 3) ──")
    vv = [e['core_volume'] for e in verify_entries]
    ev = [e['energy'] for e in verify_entries]
    print(f"  Core volume: {vv[0]:.1f} → {vv[-1]:.1f} "
          f"(drift: {abs(vv[-1]-vv[0])/(vv[0]+1e-10)*100:.1f}%)")
    print(f"  Energy: {ev[0]:.2f} → {ev[-1]:.2f}")
    wr_verify = [e['writhe'] for e in verify_entries if e['writhe'] is not None]
    if wr_verify:
        print(f"  Writhe: {wr_verify[0]:.1f} → {wr_verify[-1]:.1f} (σ={np.std(wr_verify):.1f})")

    verify_stable = len(vv) > 2 and abs(vv[-1]-vv[1])/(vv[1]+1e-10) < 0.15
    print(f"  STATUS: {'NEW STATE LOCKED ✓' if verify_stable else 'POST-SPLICE UNSTABLE ⚠'}")

    # Overall
    print("\n  ── OVERALL ──")
    if read_stable and write_fired and verify_stable:
        print("  ✓ COMPLETE READ/WRITE CYCLE SUCCESSFUL")
    elif read_stable and write_fired:
        print("  ⚠ READ + WRITE work, post-splice stability needs higher resolution")
    elif read_stable:
        print("  ⚠ READ works, WRITE needs stronger pulse or better targeting")
    else:
        print("  ✗ Insufficient resolution for definitive result")

    # Compare pre-splice vs post-splice topology
    if wr_read and wr_verify:
        print(f"\n  Pre-splice writhe  (mean): {np.mean(wr_read):+.1f}")
        print(f"  Post-splice writhe (mean): {np.mean(wr_verify):+.1f}")
        delta_w = abs(np.mean(wr_verify) - np.mean(wr_read))
        if delta_w > 2:
            print(f"  TOPOLOGY CHANGE DETECTED (ΔWr = {delta_w:.1f})")
        else:
            print(f"  No clear topology change (ΔWr = {delta_w:.1f})")

    # Save
    results = {
        "config": {k:v for k,v in cfg.__dict__.items()},
        "backend": "JAX" if HAS_JAX else "NumPy",
        "crossings": crossings,
        "splice_point": list(splice_point),
        "log": log,
        "assessment": {
            "read_stable": read_stable,
            "write_fired": write_fired,
            "verify_stable": verify_stable,
        }
    }

    with open("../rw_cycle_results.json", "w") as f:
        json.dump(results, f, indent=2, default=float)

    print(f"\nSaved to {os.path.abspath('../rw_cycle_results.json')}")
    return results


if __name__ == "__main__":
    t0 = time.time()
    run()
    print(f"\nTotal time: {time.time()-t0:.1f}s")
