#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════
  FWS Simulation Runner — Stages 1 & 2
  Execute both critical-path simulations and produce combined report.
═══════════════════════════════════════════════════════════════════════════════
"""
import sys
import os
import json
import time

# Add simulation directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from penrose_bdg_2d import run_stage1
from penrose_phonon_2d import run_stage2

def main():
    print("╔" + "═" * 68 + "╗")
    print("║  FRACTONIC WEYL SEMIMETAL — SIMULATION PROGRAM                     ║")
    print("║  Stages 1 & 2: Critical Path Simulations                          ║")
    print("║  GoS-Architect | March 2026                                        ║")
    print("╚" + "═" * 68 + "╝")
    
    t_total = time.time()
    
    # ── STAGE 1: 2D BdG ──
    print("\n\n" + "▓" * 70)
    print("  RUNNING STAGE 1: 2D BdG on Penrose Patch")
    print("▓" * 70)
    
    s1 = run_stage1(
        output_dir="stage1_results",
        n_subdivisions=5,
        t0=1.0,
        mu=1.0,
        delta=0.5,
        n_eig=20,
    )
    
    # ── STAGE 2: Phonon Transport ──
    print("\n\n" + "▓" * 70)
    print("  RUNNING STAGE 2: 2D Phonon Transport on Penrose Patch")
    print("▓" * 70)
    
    s2 = run_stage2(
        output_dir="stage2_results",
        n_subdivisions=5,
        k0=1.0,
        t0=1.0,
    )
    
    # ── COMBINED REPORT ──
    t_total = time.time() - t_total
    
    print("\n\n" + "═" * 70)
    print("  COMBINED GATE REPORT")
    print("═" * 70)
    
    print(f"\n  Total runtime: {t_total:.1f}s")
    print(f"\n  STAGE 1 — 2D BdG (MZM survival in 2D):")
    print(f"    Vertices:          {s1['n_vertices']}")
    print(f"    Zero modes found:  {s1['n_zero_modes']}")
    if s1['n_zero_modes'] > 0:
        print(f"    Zero mode energies: {s1['zero_mode_energies']}")
        print(f"    Edge weights:       {s1['zero_mode_edge_weights']}")
    print(f"    Bott index:        {s1.get('bott_index', 'N/A')}")
    
    g1 = s1['gate_assessment']
    print(f"    Gate: {'✓ PASS' if g1['zero_modes_pass'] and g1['edge_localization_pass'] else '✗ FAIL'}")
    
    print(f"\n  STAGE 2 — Phonon Transport (PGTC validation):")
    print(f"    κ_QP/κ_ordered:    {s2['kappa_ratio_mean']:.4f}")
    print(f"    Min ξ/L (phonon):  {s2['min_xi_over_L_qp']:.4f}")
    print(f"    Modulation ratio:  {s2['modulation']['ratio']:.2f}× (phonon/electron)")
    
    g2 = s2['gate_assessment']
    if g2['kappa_ratio_pass']:
        print(f"    Gate: ✓ PASS (strong phonon suppression)")
    elif g2['kappa_ratio_partial']:
        print(f"    Gate: ~ PARTIAL (modest suppression)")
    else:
        print(f"    Gate: ✗ FAIL (no significant suppression)")
    
    # Combined
    combined = {
        'stage1': s1,
        'stage2': s2,
        'total_runtime': t_total,
    }
    
    with open("combined_report.json", 'w') as f:
        json.dump(combined, f, indent=2, default=str)
    
    print(f"\n  Combined report: combined_report.json")
    print(f"  Stage 1 plots:   stage1_results/")
    print(f"  Stage 2 plots:   stage2_results/")
    
    print("\n" + "═" * 70)
    print("  SIMULATION PROGRAM COMPLETE")
    print("═" * 70)
    
    return combined

if __name__ == "__main__":
    main()
