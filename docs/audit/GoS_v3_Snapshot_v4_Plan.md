# Geometry of State — Repository Organization v3 → v4

**Date:** March 25, 2026
**Author:** Adrian Domingo, with audit by Claude (Anthropic, Opus 4.6)

---

## Project Totals (as of March 25, 2026)

| Metric | Count |
|--------|-------|
| Unique theorems (Lean, deduplicated) | **160** |
| Unique Lean files | 49 |
| Unique Python files | 15 |
| Unique documents | 30 |
| Total unique files | 99 |
| Duplicate/copy files | 22 |
| Python lines of code | 8,107 |
| Sorry (across all canonical Lean) | 10 |
| Core thesis status | **RETRACTED** (v4, March 2026) |

---

## v4 Directory Structure

```
GoS/
│
├── lakefile.lean
├── Main.lean
├── README.md
│
├── src/
│   ├── L0_Foundations/
│   │   └── LogicKernel.lean
│   │
│   ├── L1_Algebra/
│   │   ├── Clifford.lean
│   │   ├── CayleyDickson.lean
│   │   ├── Winding.lean
│   │   └── CLHoTT.lean                    # frozen, 6 sorry (Float)
│   │
│   ├── L2_Classification/
│   │   ├── AlgebraicLadder.lean
│   │   ├── KitaevCertification.lean
│   │   ├── EdgeModes.lean
│   │   ├── Bridge.lean
│   │   ├── FWS.lean
│   │   └── RunGDescend.lean
│   │
│   └── Archive/
│       ├── SingularityAsTypeError.lean     # RETRACTED axiom — preserved as methodology
│       ├── TopologicalInvariant.lean       # Real' scaffolding, 1 sorry
│       ├── GeometryOfState_verified3.lean
│       └── TrivialPhaseCheck.lean
│
├── simulations/
│   ├── campaign/                           # 7-step FWS simulation campaign
│   │   ├── graphene_sw_lattice.py          # Corrected honeycomb + Penrose SW
│   │   ├── run_all.py                      # PGTC main pipeline (Stage 2)
│   │   ├── step1_clean_baseline.py         # BDI baseline d=2
│   │   ├── step3_spinful_bdg.py            # Ni-62 exchange + Bi SOC BdG
│   │   ├── step3b_finescan.py              # Fine parameter scan, Bott index
│   │   ├── step4_bilayer_3d.py             # 2D→3D bilayer (first attempt)
│   │   └── step4b_matched_bilayer.py       # Matched bilayer (both defected)
│   │
│   ├── vortex/                             # GP vortex dynamics
│   │   ├── helium_loom_simulator.py        # 2D GP trefoil imprint
│   │   ├── helium_loom_v2_pinned.py        # Fibonacci pinning test
│   │   ├── helium_loom_v3_3d.py            # 3D trefoil filament
│   │   ├── gp3d_readwrite.py               # 3D READ/WRITE cycle
│   │   └── gp3d_solver.py                  # JAX-accelerated GP solver
│   │
│   ├── mhd/
│   │   └── stellarator_taylor_relaxation.py
│   │
│   └── superseded/                         # v1 (preserved as failure record)
│       ├── penrose_bdg_2d.py               # v1 lattice — FAIL
│       └── penrose_phonon_2d.py            # v1 phonon — superseded
│
├── agda/
│   └── FirstFile.agda
│
├── docs/
│   ├── architecture/
│   │   ├── ARCHITECTURE_v4.md
│   │   ├── ARCHITECTURE_v3_to_v4_changes.md
│   │   ├── ARCHITECTURE_v3.pdf
│   │   ├── GoS_AUDIT_v3_1.md
│   │   ├── GoS_COMPLETE_AUDIT.md
│   │   └── AUDIT_v2.md                    # (from this session)
│   │
│   ├── thesis/
│   │   ├── GeometryOfState_Thesis_WhitePaper.docx
│   │   ├── TheGeometryOfState_SystemsArchitecture.docx
│   │   ├── HiTT_Architectural_Draft_v0_1.docx
│   │   ├── HiTT_Architectural_Draft_v0_2.docx   # contains retraction
│   │   └── Glassbox_ConstitutionalXAI_v2.docx
│   │
│   ├── physics/
│   │   ├── GoS_Quasiperiodic_Ratchet_Thesis_v3.docx
│   │   ├── Topological_Invariants_as_Dependent_Types.docx
│   │   ├── topological_boundary_coherence_outline.docx
│   │   ├── The_Thermodynamic_Bootstrap_Case_Study.docx
│   │   └── MZM_Certification_Architecture.docx
│   │
│   ├── device/
│   │   ├── FWS_Engineering_Spec_v2.docx
│   │   └── FWS_Simulation_Roadmap.docx
│   │
│   ├── proposals/
│   │   ├── GoS_Research_Proposal_Updated.md
│   │   ├── GoS_Technical_Briefing.docx
│   │   ├── StationQ_Collaboration_Proposal.docx
│   │   ├── GoS_Systems_Architecture_Blueprint_2026-2050.docx
│   │   └── GoS_Year1_Plan_2026.docx
│   │
│   └── industry/
│       ├── Digital_Triplet_Architecture_Preprint.docx
│       ├── FVDT_Industry5_Paper_Draft.docx
│       ├── fvdt_paper.docx
│       └── QM_Foundation_NotebookLM_Architecture.docx
│
└── archive/
    ├── lean_monolith/                      # GeometryOfState.lean evolution
    │   ├── GeometryOfState.lean            # 40K original monolith
    │   ├── GeometryOfState-v1.lean         # 7K early version
    │   ├── GeometryOfState-v3.lean         # 29K mid version
    │   ├── GeometryOfState__4_.lean        # 42K later version
    │   └── GeometryOfState-Stage-1-5.lean  # 6K partial extract
    │
    ├── lean_bridge_versions/
    │   ├── TopologicalBridge_v1.lean
    │   ├── TopologicalBridgeFixed.lean
    │   └── TopologicalBridgeComplete.lean
    │
    ├── lean_kitaev_versions/
    │   ├── Chain.lean                      # Near-identical to KitaevCertification
    │   ├── KitaevChain.lean                # Smaller earlier version
    │   ├── StationQ.lean                   # Same theorems as EdgeModes
    │   └── StationQ_Phase1_Phase2.lean     # Earlier StationQ
    │
    ├── lean_mathlib_experiments/
    │   ├── TopologicalComputation.lean     # Imports Mathlib, 30 axioms
    │   ├── TopologicalLock3D.lean          # Imports Mathlib, 14 axioms
    │   ├── MHDTopology.lean                # Imports Mathlib, 20 axioms
    │   └── PinnedPseudoKnot.lean           # Imports Mathlib, 4 axioms
    │
    ├── lean_small_files/
    │   ├── AdrianDomingo_GeometryOfState_Logic.lean  # RETRACTED axiom
    │   ├── CliffordFoundation3D.lean       # Defs only, covered in Clifford.lean
    │   ├── WindingNumber.lean              # 20 thm, 5 sorry — review for v4 inclusion
    │   ├── GeometryOfState_KitaevBridge.lean
    │   ├── GeometryOfState_Logic_CL-HoTT.lean
    │   ├── GeometryOfState_Pseudoscalar_Squares.lean
    │   ├── GeometryOfState_The_Majorana_Zero_Mode.lean
    │   ├── GoS_KitaevChain.lean
    │   ├── KitaevChain_Digital_Triplet.lean
    │   ├── TheGeometryOfState_Verifiable_Quantum_Theory.lean
    │   └── The_Type-Safety_Chain.lean
    │
    ├── lean_fix_patches/
    │   ├── section14_fix_final.lean
    │   ├── section14_3_fix.lean
    │   ├── two_replacements_final.lean
    │   └── nat_beq_fix.lean
    │
    ├── lean_duplicates/                    # Byte-identical, different names
    │   ├── TopologicalBridge_v2.lean       # = Bridge.lean
    │   ├── GeometryOfState_v2.lean         # = Clifford.lean
    │   ├── FractonicWeylSemimetal.lean     # = FWS.lean
    │   ├── GeometryOfState_verified.lean   # = GeometryOfState_verified3.lean
    │   ├── CliffordFoundation.lean         # = Winding.lean
    │   ├── GeometryOfState__1_.lean        # = GeometryOfState.lean
    │   ├── GeometryOfState_v1.lean         # = GeometryOfState.lean
    │   ├── GeometryOfState_unified.lean    # = GeometryOfState-v1.lean
    │   ├── KitaevBridge.lean               # = GeometryOfState_The_Majorana_Zero_Mode.lean
    │   ├── GoS_Spacetime.lean              # = GeometryOfState_Pseudoscalar_Squares.lean
    │   ├── GeometryOfState.lean copy
    │   ├── KitaevCertification.lean copy
    │   └── PinnedPseudoKnot.lean copy
    │
    ├── python_copies/
    │   ├── run_all_copy.py
    │   ├── step3_spinful_bdg_copy.py
    │   ├── step3_spinful_bdg_copy_2.py
    │   ├── step3b_finescan_copy.py
    │   └── graphene_sw_lattice_copy.py
    │
    ├── doc_duplicates/
    │   ├── GeometryOfState_ResearchProposal_1.docx
    │   ├── GeometryOfState_ResearchProposal_copy.docx
    │   ├── GoS_Quasiperiodic_Ratchet_Thesis_v2_copy.docx
    │   ├── GoS_Quasiperiodic_Ratchet_Thesis_v3_copy.docx
    │   ├── MZM_Certification_Architecture_copy.docx
    │   ├── The_Thermodynamic_Bootstrap_Case_Study_copy.docx
    │   ├── Topological_Invariants_as_Dependent_Types_copy.docx
    │   └── GoS_Year1_Plan_2026__1_.docx
    │
    └── doc_superseded/
        ├── GoS_Quasiperiodic_Ratchet_Thesis.docx      # v1
        ├── GoS_Quasiperiodic_Ratchet_Thesis_v2.docx   # v2
        ├── FWS_Engineering_Spec.docx                   # v1
        ├── GeometryOfState_ResearchProposal.docx       # superseded by Updated.md
        ├── GoS_Research_Proposal.docx                  # superseded by Updated.md
        ├── GeometryOfState.txt
        └── GeometryOfState-Stage.txt
```

---

## v4 Canonical Lean File Census

| Layer | File | Thm | Ax | Sorry | Status |
|-------|------|-----|-----|-------|--------|
| L0 | LogicKernel.lean | 1 | 1 | 0 | ⚠ Rename axiom |
| L1 | Clifford.lean | 12 | 0 | 0 | ✓ |
| L1 | CayleyDickson.lean | 3 | 0 | 0 | ✓ |
| L1 | Winding.lean | 0 | 0 | 0 | ✓ (defs) |
| L1 | CLHoTT.lean | 7 | 0 | 6 | Frozen (Float) |
| L2 | AlgebraicLadder.lean | 16 | 0 | 0 | ✓ |
| L2 | KitaevCertification.lean | 35 | 0 | 0 | ✓ |
| L2 | EdgeModes.lean | 33 | 0 | 0 | ✓ |
| L2 | Bridge.lean | 9 | 21 | 0 | ✓ (axioms documented) |
| L2 | FWS.lean | 22 | 0 | 0 | ✓ |
| L2 | RunGDescend.lean | 13 | 0 | 0 | ✓ (new in v4) |
| Arc | SingularityAsTypeError.lean | 17 | 21 | 3 | ⚠ RETRACTED axiom |
| Arc | TopologicalInvariant.lean | 1 | 15 | 1 | Scaffolding |
| Arc | GeometryOfState_verified3.lean | 8 | 0 | 0 | ✓ |
| Arc | TrivialPhaseCheck.lean | 2 | 0 | 0 | ✓ |
| **TOTAL** | **15 files** | **179** | **58** | **10** | |

**Note on theorem count:** The 15 canonical files contain 179 theorems by `grep`. However, some theorem names overlap between files (e.g., `topo_is_gapped` appears in both KitaevCertification and EdgeModes). The **160 unique theorem names** across the entire 49-file project remains the deduplicated count. The canonical-set-only unique count is:

| Metric | Count |
|--------|-------|
| Theorems in canonical files (raw grep) | 179 |
| Unique theorem names (whole project) | **160** |
| Axiom declarations (canonical) | 58 |
| Sorry (canonical) | 10 |
| Zero sorry in classification/topology | ✓ |

---

## v4 Simulation File Map

### Campaign (L3 — DEMONSTRATED)

| Script | Lines | Result | Status |
|--------|-------|--------|--------|
| graphene_sw_lattice.py | 472 | Corrected honeycomb + Penrose SW | **PASS** |
| run_all.py | 502 | κ=0.30, 70% suppression, 12 modes | **PASS** |
| step1_clean_baseline.py | 459 | BDI trivial d=2, Bott=0 | **PASS** |
| step3_spinful_bdg.py | 617 | Gap closes h_ex≈0.6, BDI→D | **PASS** |
| step3b_finescan.py | 490 | B=+1 at h_ex=0, B=-1 at h_ex=1.1 | **PASS** |
| step4_bilayer_3d.py | 764 | First 3D attempt | **PARTIAL** |
| step4b_matched_bilayer.py | 483 | Defect loc 80-92% | **PARTIAL** |

### Vortex Dynamics

| Script | Lines | Content | Status |
|--------|-------|---------|--------|
| helium_loom_simulator.py | 503 | 2D GP trefoil, winding audit | **DEMONSTRATED** |
| helium_loom_v2_pinned.py | 294 | Fibonacci pinning test | **DEMONSTRATED** |
| helium_loom_v3_3d.py | 443 | 3D trefoil filament | **DEMONSTRATED** |
| gp3d_readwrite.py | 544 | READ/WRITE topological cycle | **DEMONSTRATED** |
| gp3d_solver.py | 633 | JAX GP solver | Infrastructure |

### MHD

| Script | Lines | Content | Status |
|--------|-------|---------|--------|
| stellarator_taylor_relaxation.py | 301 | Energy decays faster than helicity | **DEMONSTRATED** |

### Superseded (v1 failure record)

| Script | Lines | Failure |
|--------|-------|---------|
| penrose_bdg_2d.py | 823 | Wrong lattice, CN={3..10}, 0 MZMs |
| penrose_phonon_2d.py | 779 | v1 phonon on wrong lattice |

---

## v4 Document Map

### Current (active)

| Document | Category | Layer |
|----------|----------|-------|
| ARCHITECTURE_v4.md | Architecture | L0-L5 |
| ARCHITECTURE_v3_to_v4_changes.md | Architecture | Meta |
| GoS_COMPLETE_AUDIT.md | Audit | All |
| Glassbox_ConstitutionalXAI_v2.docx | Thesis | L6 |
| HiTT_Architectural_Draft_v0_2.docx | Thesis | L0-L3 |
| GoS_Quasiperiodic_Ratchet_Thesis_v3.docx | Physics | L3 |
| FWS_Engineering_Spec_v2.docx | Device | L4 |
| FWS_Simulation_Roadmap.docx | Device | L4 |
| MZM_Certification_Architecture.docx | Verification | L5 |
| Topological_Invariants_as_Dependent_Types.docx | Physics | L2-L3 |
| topological_boundary_coherence_outline.docx | Physics | L2-L5 |
| The_Thermodynamic_Bootstrap_Case_Study.docx | Physics | L5 |
| GoS_Research_Proposal_Updated.md | Strategy | Meta |
| GoS_Technical_Briefing.docx | Strategy | Meta |
| StationQ_Collaboration_Proposal.docx | Strategy | Meta |
| GoS_Systems_Architecture_Blueprint_2026-2050.docx | Strategy | Meta |
| GoS_Year1_Plan_2026.docx | Strategy | Meta |
| Digital_Triplet_Architecture_Preprint.docx | Industry | L4-L5 |
| FVDT_Industry5_Paper_Draft.docx | Industry | L4-L5 |
| fvdt_paper.docx | Industry | L4-L5 |
| QM_Foundation_NotebookLM_Architecture.docx | Industry | Meta |

### Historical (archive)

| Document | Superseded by |
|----------|---------------|
| ARCHITECTURE_v3.pdf | ARCHITECTURE_v4.md |
| GoS_AUDIT_v3_1.md | GoS_COMPLETE_AUDIT.md |
| HiTT_Architectural_Draft_v0_1.docx | v0_2 |
| GeometryOfState_Thesis_WhitePaper.docx | ARCHITECTURE_v4 + thesis docs |
| TheGeometryOfState_SystemsArchitecture.docx | ARCHITECTURE_v4 |
| GoS_Quasiperiodic_Ratchet_Thesis.docx (v1) | v3 |
| GoS_Quasiperiodic_Ratchet_Thesis_v2.docx | v3 |
| FWS_Engineering_Spec.docx (v1) | v2 |
| GeometryOfState_ResearchProposal.docx | Updated.md |
| GoS_Research_Proposal.docx | Updated.md |
| GeometryOfState.txt | Monolith era |
| GeometryOfState-Stage.txt | Monolith era |

---

## Actions for v4 Transition

### Critical (do before sharing repo)

- [ ] Move duplicates to archive/ (22 files)
- [ ] Add retraction header to SingularityAsTypeError.lean
- [ ] Rename LogicKernel `Univalence` → `winding_determines_state`
- [ ] Add AUDIT_v2.md to docs/
- [ ] Create README.md with canonical file list and hard numbers

### Important (do before Anthropic contact)

- [ ] Organize into directory structure above
- [ ] Review WindingNumber.lean (20 thm, 5 sorry) for possible v4 inclusion
- [ ] Remove or fix Taylor_Relaxation (concludes True)
- [ ] Update all documents to say 160 theorems

### Low priority

- [ ] Refactor CLHoTT.lean Float sorry → ℤ/ℚ
- [ ] Consolidate duplicate S1 axioms across files
- [ ] Propagate retraction to remaining downstream docs

---

*The compiler is the credential. The retraction is the proof of honesty.*
