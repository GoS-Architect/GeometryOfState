# Geometry of State — Repository Structure (DRAFT)

**Status:** Working document — pending additional content from Adrian
**Date:** April 2026

---

## Root

```
GeometryOfState/
├── README.md                          # Public face — UPDATE: stack line v3.1 → v4.1
├── LICENSE                            # MIT
│
├── Kernel/                            # PROVED — the trust core
│   ├── Clifford/                      # Cl(p,q) over ℚ, Bott periodicity
│   ├── Bivector/                      # Spin group, discrimination theorem
│   ├── CayleyDickson/                 # Division algebra ladder, Adams obstruction
│   └── Kitaev/                        # Chain model, bulk-boundary, gap conditions
│
├── Classification/                    # AZ encoding, tenfold way (112+ theorems)
│   └── EmergentLightSpeed.lean        # SVT module — 5 rfl theorems, 0 sorry, 1 axiom
│
├── SVT/                               # Vacuum condensate — c as dependent term
│
├── FWS/                               # Materials architecture (v1 RETRACTED, v2 current)
│
├── Simulation/                        # BdG (1D PASS, 2D FAIL), Taylor relaxation (PASS)
│   ├── graphene_sw_lattice.py         # Corrected lattice generator
│   ├── run_all.py                     # Stage 1+2 runner
│   ├── step1_clean_baseline.py        # BDI baseline
│   ├── step3_spinful_bdg.py           # 4N×4N with Ni-62 + Bi
│   ├── step3b_finescan.py             # Parameter scan + Bott indices
│   ├── step4b_matched_bilayer.py      # 3D bilayer
│   ├── penrose_bdg_2d.py              # Original (superseded)
│   ├── penrose_phonon_2d.py           # Original (superseded)
│   ├── step4_bilayer_3d.py            # Mismatched bilayer (diagnostic failure)
│   └── SIMULATION_RESULTS.md          # Campaign summary — 7 steps, PGTC strongest result
│
├── Audit/                             # Automated epistemic tagging (in development)
│
├── Docs/
│   ├── canonical/                     # Current authoritative documents
│   │   ├── Glassbox_ConstitutionalXAI_v4.1.md
│   │   ├── Quantum_Stellarator_v0.1.md
│   │   ├── MZM_Vortex_Falsification_Narrative.md   # TAS cycle: 5 nulls → vortex pivot → Stellarator origin
│   │   ├── GoS_Thesis_for_Antithesis.md             # Structured target for adversarial review
│   │   ├── SpatialAZ_Concept_Paper.md               # BDI→D domain wall MZMs — active technical work
│   │   ├── GQAC_v0.0_Executive_Abstract.md         # CANONICAL — v4.1-aligned, SEEDS/biospheric
│   │   ├── Therapeutic_Modalities_Research_Plan.md  # Concept paper — potential publication
│   │   ├── CubicalAgda_Research_Strategy.md         # Live roadmap — 5 gaps, phased
│   │   ├── Omnivalence_Documentation_Map_v2.md      # MASTER INDEX — 25+ docs, 155 theorems (Mar 24)
│   │   ├── MZM_Certification_Architecture.docx      # Three-gate verification protocol
│   │   └── README.md                  # (symlink or copy of root README)
│   │
│   ├── archive/                       # Superseded — preserved, not deleted
│   │   ├── Glassbox_ConstitutionalXAI_v2.0.docx
│   │   ├── Glassbox_ConstitutionalXAI_v3.1.docx
│   │   ├── Global_Quantum_AI_Commons_v0.1.docx   # Archived — pre-v4.1, E8/sheaf version
│   │   ├── GQAC_v0.1_Draft.md                    # Archived — tight CERN-focused draft, pre-v4.1
│   │   ├── NQI_Systems_Architecture_v1.0.docx
│   │   ├── GoS_Project_Brief_Mar2026.md           # 104-theorem snapshot — superseded by current state
│   │   ├── FWS_Engineering_Spec.docx              # Needs Ni-62/Bi update
│   │   ├── FWS_Simulation_Roadmap.docx            # 7-stage gated program
│   │   ├── GoS_Quasiperiodic_Ratchet_Thesis_v3.docx  # Working thesis
│   │   └── theorem_inventory_v2.md                # 104 theorems — superseded
│   │
│   ├── audit/
│   │   ├── GoS_Cross_Document_Audit_v1.md         # STALE — audited v2.0/v3.1/NQI/Commons
│   │   ├── EmergentLightSpeed_Compilation.md       # Verification artifact — Apr 3, 2026
│   │   ├── SVT_Research_Landscape.md               # Literature context + architectural claim — Mar 30, 2026
│   │   ├── Jacobson_Detection_Analysis.md           # CRITICAL — SVT circularity + Majorana detection gap
│   │   ├── Quantum_Materials_Reference_v3.md        # Curated lit review mapped to L0–L5
│   │   └── AUDIT_STATUS.md                        # Flag: v2 needed against v4.1
│   │
│   └── preprint/
│       └── PGTC/                      # Pre-Geometric Topological Classification
│           └── (draft — awaiting arXiv endorsement)
│
├── Archive/                           # Superseded Lean files — preserved, not deleted
│
└── .github/                           # CI, workflows
```

---

## Open Questions

1. **~~Which GQAC is canonical?~~ RESOLVED:** GQAC v0.0 (executive abstract) is canonical — v4.1-aligned with SEEDS, compound tags, biospheric alignment. The tight v0.1 draft and longer Commons v0.1 are both archived (pre-v4.1).
2. **NQI location:** Archive only, or does it need a canonical successor?
3. **Theorem count — PARTIALLY RESOLVED:** Documentation map v2 (Mar 24) gives **155 theorems, 15 files, 46 axiom declarations, 7 sorry**. README says 152. Stellarator says 144. Both are stale. If work has continued since Mar 24, actual count may be higher. **Must audit against live repo.**
4. **Stellarator ↔ GQAC overlap:** Stellarator §2.3 (sustainable energy/plasma) and GQAC both reference stellarator cooperation protocols. Relationship needs explicit mapping.
5. **Stellarator references v3.1 in stack:** Needs update to v4.1. Also needs alignment with v4.1's biospheric ground truth — the Stellarator's "serve or extract" framing in v4.1 §2.1 applies directly to fusion energy claims.
6. **Lean file placement:**
   - `SpinGroup.lean` — blocked on import fix from GitHub recovery snapshot
   - `BivectorDiscrimination.lean` — highest impact next step, depends on SpinGroup
   - `EdgeModeBivector.lean` — critical path, needs type-level bridge
   - `CLHoTT.lean` — quarantined sorry debt (Pillars VII–VIII)
7. **v4.1 format:** Currently markdown. Does it need a .docx canonical version?
8. **Stellarator sorry count:** States 6 sorry in CLHoTT.lean. Cross-check against repo.
9. **PGTC preprint:** Lives in Docs/preprint/ but Stellarator Ch.5 contains the core PGTC results. Relationship: preprint is the extractable submission; Stellarator is the architectural context.
10. **EmergentLightSpeed.lean location:** Confirmed in `L2_Classification/`, not `SVT/`. The SVT/ folder may be redundant or intended for something else.
11. **svt_vacuum_exists is trivially satisfiable:** Needs `DivisionAlgebraGrounded` predicate. Identified as 1-2 week task.
12. **Chern-Simons H₁ cycle:** CS(A) appears in both Kodama state and tenfold-way classification — open feedback loop. Most important unresolved structural gap per the compilation doc.
13. **PosRat/Float bridge:** EmergentLightSpeed uses PosRat; Kitaev simulations use Float. Two arithmetic universes, no formal bridge.
14. **Zero-Mathlib two-track strategy:** SVT landscape doc identifies two compilation paths — zero-dep (replace `norm_num` with `native_decide`) vs L2-Classification track (import Mathlib.Tactic). Recommendation: iterate in L2 track, migrate to zero-dep once stable. This is the concrete instantiation of the zero-Mathlib architectural tension.
15. **SVT circularity (Jacobson analysis):** Jacobson presupposes Lorentzian causal structure → SVT claims c is emergent → circularity if combined in a single-stage derivation. The Stellarator §7.5-7.6 inherits this. §9.4 question 5 acknowledges it. The EmergentLightSpeed compilation doesn't resolve it — the metamathematical claim (SVT is more constrained) holds independently, but the physical claim is bounded.
16. **Majorana detection gap:** No matched-filter equivalent exists for topological phases. Every device is unique. Das Sarma argues all experimental Majorana signatures to date can be explained by disorder. This is the adversarial context for PGTC — the preprint needs to position itself relative to this landscape.
17. **Therapeutic modalities paper:** Independent publication target (FAccT, NeurIPS Safety, JMIR Mental Health, arXiv cs.AI+cs.CY). Has a 4-phase research plan. Phase 1 (literature review) and Phase 2 (metric operationalization) are prerequisites. Currently at CONJECTURED — needs face validity from clinical psychology. Separate submission pathway from PGTC.
18. **Additional content:** Adrian has more material to integrate — structure TBD.
19. **Lean file inventory — THREE DIFFERENT INVENTORIES:**
    - README: GeometryOfState.lean, TopologicalBridge.lean, AZ_Classification/, EmergentLightSpeed.lean, CLHoTT.lean
    - Antithesis doc: KitaevChain.lean, TopologicalLock3D.lean, TopologicalComputation.lean, PinnedPseudoKnot.lean, MHDTopology.lean
    - Spatial AZ paper: AlgebraicLadder.lean, KitaevChain.lean, EdgeModes.lean, BridgeTheorems.lean, FWSClassification.lean
    - Planned files: SpinGroup.lean, BivectorDiscrimination.lean, EdgeModeBivector.lean, SpatialAZ.lean, DomainWallMZM.lean
    **Must reconcile against actual repo before finalizing folder structure.**
20. **Documents referenced but not yet seen:** ARCHITECTURE.md v4, Repository Audit v2, Auditable Reasoning Memo v2, bivector_invariance_concept_v3, PGTC_2D_Simulation_Concept, Topological_Boundary_Coherence_Concept, Cubical_Agda_Winding_Number_Concept, HiTT v0.1/v0.2, Ni62_FWS_physics_analysis, PGTC_DRAFTING_BRIEF, TBC outline, Table of Contents Draft, compass artifact, 3 philosophical companions. Full inventory needs all of these placed.

---

## Dependency Order (Rung Rule applied to repo tasks)

### Must happen first
- [ ] Fix `SpinGroup.lean` import (unblocks everything below)
- [ ] Update README stack line: v3.1 → v4.1

### Then
- [ ] `BivectorDiscrimination.lean` — move bivector commutativity CONJECTURED → PROVED
- [ ] Flag audit as stale, scope v2 audit
- [ ] Reconcile theorem count (144 vs 152) across Stellarator/README/v4.1

### Then
- [ ] `EdgeModeBivector.lean` — type-level bridge
- [ ] Cross-document audit v2 against v4.1 + Stellarator v0.1
- [ ] PGTC preprint submission (gated on endorsement)
- [ ] Update Stellarator stack reference v3.1 → v4.1

### Deferred
- [ ] Resolve zero-Mathlib vs. tactic dependency tension
- [ ] Strengthen `svt_vacuum_exists` with `DivisionAlgebraGrounded` predicate
- [ ] Close Chern-Simons H₁ cycle (Kodama ↔ tenfold-way feedback loop)
- [ ] Document PosRat/Float bridge (L3→L2)
- [ ] Therapeutic modalities paper: Phase 1 literature review, Phase 2 metric operationalization
- [ ] NQI update to v4.1 compatibility

### Cubical Agda Track (parallel to Lean 4 work)
- [ ] Phase 0: Install Cubical Agda, complete HoTT Game (1-2 weeks)
- [ ] Phase 1: π₁(S¹) ≅ ℤ in own file, DaggerCategory.agda, close CLHoTT sorry equivalents (2-4 weeks)
- [ ] Phase 2: Cohesive modalities — shape/flat/sharp, TopologicallyProtected (4-8 weeks)
- [ ] Phase 3: Kitaev chain in HoTT — winding number as dependent type over IsGapped (4-8 weeks)
- [ ] Phase 4: TBC theorem — Volovik functor, univalence application (4-8 weeks)
