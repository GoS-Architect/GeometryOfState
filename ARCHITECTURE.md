# GEOMETRY OF STATE
## Systems Architecture v4.5

**A Layered Framework for Topological Quantum Matter**

Adrian Domingo · GoS-Architect · github.com/GoS-Architect · March 2026

---

### v4.5 CHANGELOG

- **FULL REPOSITORY AUDIT:** Complete inventory of all 101 unique files (49 Lean, 15 Python, 32 documents, 5 other). 22 duplicates identified and classified.
- **THEOREM COUNT CORRECTED:** 160 unique theorem names verified by automated deduplication across all project files. Previous counts (104, 144, 147, 155) were snapshots of subsets at different dates.
- **AXIOM ACCOUNTING COMPLETED:** 58 axiom declarations in canonical files, categorized into 5 types (HoTT infrastructure, real scaffolding, bridge axioms, physical postulates, type declarations). The "12 axioms" verbal estimate referred to bridge axioms only; the full count is documented.
- **SORRY ACCOUNTING UPDATED:** 10 sorry in canonical files (6 Float algebra in CLHoTT, 3 in retracted SingularityAsTypeError, 1 in TopologicalInvariant scaffolding). Zero sorry in any classification or topology theorem.
- **REPOSITORY REORGANIZATION PLANNED:** v4 directory structure defined. Active code separated from 34 archived Lean files, 5 Python copies, 8 document duplicates, and 12 superseded documents.
- **SOCRATIC PARTNER ARCHITECTURE ADDED:** Constitutional multi-agent verification framework documented as prompt profile.
- **GLASSBOX CONSTITUTIONAL XAI v2 FINAL** added to document map.

### v4 CHANGELOG (preserved)

- RETRACTION PROPAGATED: "Singularities are type errors" replaced with revised thesis from HiTT v0.2. Retraction history preserved. See §Core Thesis.
- Epistemic tags added to Stellarator/Chern-Simons connection and Ascending Ladder octonion row.
- BivectorDiscrimination.lean and SpinGroup.lean added to planned files.

### v3 CHANGELOG (preserved)

- Corrected BDI/D classification (simulation-confirmed). Added Ni-62 exchange and Bi SOC layers. Integrated 7-step simulation campaign results. Added stellarator/Chern-Simons connection.

---

## Overview

The Geometry of State (GoS) is a systems architecture connecting formal verification (Lean 4, Cubical Agda) through algebraic structures and topological classification to physical predictions, device design, and experimental certification.

The architecture is organized into six layers. Each layer imports from the layer below and exports to the layer above. No layer skips a level. The dependency direction is strictly upward.

---

## Layer Diagram

```
L6  GOVERNANCE — How do we reason about reasoning?
    Glassbox Constitutional XAI | Socratic Partner Architecture
    Epistemic tagging | Axiom accounting | Attribution transparency

L5  VERIFICATION — How do we know it's real?
    MZM Certification Architecture | Thermodynamic Bootstrap | TAS Dialectic
    Three-gate protocol: strain invariance + NV relaxometry + Clifford cert

L4  DEVICE — What do we build?
    FWS Engineering Spec (material stack, 7 layers including Ni-62 + Bi)
    Simulation Roadmap (7 stages, gated, kill conditions)

L3  PHYSICS — What does the math predict?
    15 simulation scripts | 7-step campaign | GP vortex dynamics | Taylor relaxation
    PGTC: κ=0.30 | BDI→D transition | Bott B=+1 | Defect localization 80-92%

L2  CLASSIFICATION — Which topological phase?
    AlgebraicLadder (16) KitaevCertification (35) EdgeModes (33)
    Bridge (9) FWS (22) RunGDescend (13)

L1  ALGEBRA — What are the structures?
    Clifford (12) CayleyDickson (3) Winding (defs) CLHoTT (7, frozen)

L0  FOUNDATIONS — What can we prove?
    Lean 4 v4.12.0, zero Mathlib | Cubical Agda (planned)
    Kernel is verifier | Path, S¹, π₁(S¹)≅ℤ axiomatized
```

---

## Project Census (v4.5 — Audited March 25, 2026)

### Hard Numbers

| Metric | Count | Source |
|--------|-------|--------|
| Unique theorem names | **160** | `grep` + `sort -u` across all 49 Lean files |
| Canonical Lean files | 15 | See §Canonical File Map |
| Axiom declarations (canonical) | 58 | See §Axiom Accounting |
| Sorry (canonical) | 10 | See §Sorry Accounting |
| Sorry in classification/topology | **0** | |
| Unique Python scripts | 15 | See §Simulation Campaign |
| Unique documents | 32 | See §Document Map |
| Total unique project files | 101 | |
| Duplicate/copy files (to archive) | 22 | See §Archive Inventory |
| Lines of Lean (all unique) | ~13,000 | |
| Lines of Python (all unique) | 8,107 | |
| Mathlib dependencies | **0** | |

### Previous Counts (reconciliation)

| Source | Theorems | Date | Explanation |
|--------|----------|------|-------------|
| ARCHITECTURE v3 | 155 | March 2026 | Snapshot of 15 files, raw grep |
| Anthropic memo v1 | 104 | March 2026 | Earlier snapshot, 11 files |
| TBC Review | 144 | March 2026 | Reviewer's count at review time |
| **This audit** | **160** | **March 25, 2026** | **Deduplicated across all 49 unique Lean files** |

The 160 count is definitive. It reflects unique theorem names — no theorem counted twice even if it appears in multiple files.

---

## Theorem Census by Layer

| Layer | Files | Theorems | Sorry | Key proof methods |
|-------|-------|----------|-------|-------------------|
| L0 Foundations | 1 | 1 | 0 | apply + rfl |
| L1 Algebra | 4 | 22 | 6 | rfl, decide, sorry(Float) |
| L2 Classification | 6 | 128 | 0 | rfl, native_decide, omega, induction, Classical.byContradiction |
| Archive | 4 | 28 | 4 | rfl, intro+exact, sorry |
| **TOTAL** | **15** | **179 raw / 160 unique** | **10** | **Zero sorry in classification or topology** |

---

## Axiom Accounting

### Why 58, not 12

The project has referred to "12 axioms" informally. The actual `axiom` keyword count across canonical files is **58**. The discrepancy is not dishonest — the categories are genuinely different — but must be addressed explicitly.

### Category A — HoTT Infrastructure (8 declarations)

Theorems in Cubical Agda, postulated in Lean 4. Consistent with MLTT+UA. Eliminated by the planned Cubical Agda port.

- `Path`, `Path.refl` — proof-relevant identity type (Bridge.lean)
- `S1`, `S1.base`, `S1.loop` — circle HIT (Bridge.lean, SingularityAsTypeError.lean — duplicated)
- `pi1_S1` — π₁(S¹) ≅ ℤ (Bridge.lean)
- `Univalence` — **⚠ NAMING ISSUE:** Actually winding-number injectivity, not standard UA (LogicKernel.lean). Rename pending.

### Category B — Real Number Scaffolding (15 declarations)

Building a minimal ℝ because of zero Mathlib dependencies. Would vanish with `import Mathlib.Analysis`.

- `Real'`, arithmetic operations, `IsNonzero`, `BrillouinZone`, `deriv_k`, `integral_BZ`, `exact_quantization` (TopologicalInvariant.lean)

### Category C — Bridge Axioms (7 declarations — the trust boundary)

Each documented in Bridge.lean with domain, trust level, and closure strategy.

| Label | Name | Domain |
|-------|------|--------|
| A | `normalization_defines_loop` | Point-set topology |
| B | `exact_winding_is_degree` | Differential topology |
| C | `sensor_rounding_stable` | Numerical analysis / IEEE 754 |
| D | `sensor_equals_degree` | Composition of B+C |
| E | `intermediate_singularity` | Homotopy theory + IVT |
| F | `knot_change_requires_singularity` | 3D differential topology |
| G | `helicity_change_requires_reconnection` | MHD theory |

### Category D — Physical Postulates (21 declarations)

| Axiom | File | Status |
|-------|------|--------|
| `ConservationOfInformation` | SingularityAsTypeError.lean | **⚠ RETRACTED** — provably inconsistent |
| `Topological_Lock` | SingularityAsTypeError.lean | Depends on retracted framework |
| `Taylor_Relaxation` | SingularityAsTypeError.lean | **⚠ Concludes `True` — structurally vacuous** |
| `Grand_Syntactic_Immunity` | SingularityAsTypeError.lean | Apex theorem as axiom, not proved |
| (17 additional type/structure declarations) | SingularityAsTypeError.lean, Bridge.lean | Various: S¹ variants, Filament, KnotType, MagneticConfig, etc. |

### Category E — Type Declarations (7 declarations)

Types postulated rather than constructed: `Filament`, `KnotType`, `filament_knot_type`, `MagneticConfig`, `magnetic_helicity`, `IsKnotProtected`, `IsHelicityProtected` (Bridge.lean).

---

## Sorry Accounting

| # | File | What it needs | Category |
|---|------|---------------|----------|
| 1–6 | CLHoTT.lean (lines 286–330) | Float algebra: neg_neg, mul_comm, mul_one, etc. | Float (frozen) |
| 7 | TopologicalInvariant.lean (line 110) | 2π ≠ 0 | Real scaffolding |
| 8–10 | SingularityAsTypeError.lean (lines 353, 500, 503) | Full Hamiltonian theory; MZM-gap connection | Retracted file |

**Path to closure:** CLHoTT → refactor to ℤ/ℚ coefficients. TopologicalInvariant → enrich Real' axioms. SingularityAsTypeError → file is archived; sorry are moot unless ladder theorems are extracted to a clean file.

---

## The Core Thesis (Revised in v4 — Retraction Propagated)

### The Original Thesis [RETRACTED]

**[RETRACTED]** The original GoS thesis held that singularities are type errors — points where a topological program fails to type-check. This framing was presented as the core claim in ARCHITECTURE v1–v3 and motivated the project's initial development.

The retraction is grounded in two findings documented in HiTT v0.2:

1. **Formal inconsistency.** The axiom `ConservationOfInformation`, stated as `∀ (state : Type), Impossible (state = Empty)`, is provably inconsistent. `Empty = Empty` holds by `rfl`, so the axiom generates a contradiction. The compiler rejected the thesis about type errors via a type error.

2. **Physical incorrectness.** The Kitaev chain Hamiltonian H(k) is perfectly well-defined at the critical point μ = 2t. The bivector exists; it has zero magnitude. Nothing is ill-formed. The gap condition `IsGappedAt` becomes undischargeable — but the Hamiltonian itself type-checks.

### The Revised Thesis

Singularities are phase transitions in the topos itself — points where the ambient grammar of valid mathematics undergoes a structural transformation. At a topological phase boundary, the gap condition `IsGappedAt` becomes undischargeable — not because the computation is ill-formed, but because the system has crossed into a regime where the topological classification changes. The phase transition is the absence of a proof term *in the original topos*. In the new topos, a different proof term exists.

**[SPECULATIVE]** The topos-theoretic formulation — that each Altland-Zirnbauer symmetry class defines a distinct topos with its own internal logic — is architecturally motivated but has no formal expression. No specific ∞-topos has been exhibited for any symmetry class.

### What Survived the Retraction

The formal observations remain valid under the revised thesis:
- `gapless_blocks_inversion` (Clifford.lean) — gap closing blocks algebraic inversion. **PROVED.**
- `gapless_invariant_undefined` (TopologicalInvariant.lean) — cannot call topological_invariant at gapless point. **PROVED** (modulo Real' scaffolding).
- `singularity_blocks_construction` (Bridge.lean) — gapless parameter blocks invariant computation. **PROVED** (unconditional).
- AZ tenfold way classifies what changes across the transition. **PROVED** (128 theorems, 0 sorry).

### Retraction Record

| Version | Thesis | Status | Reason |
|---------|--------|--------|--------|
| v1–v3 | Singularities are type errors | **RETRACTED** | Formal inconsistency + physical incorrectness |
| v4–v4.5 | Singularities are topos phase transitions | **SPECULATIVE** | Architecturally motivated; no formal topos exhibited |

---

## FWS Material Stack

| Layer | Material | Role | Status |
|-------|----------|------|--------|
| 1 | Si-28 wafer (99.995%) | Nuclear spin silence, structural base | ESTABLISHED |
| 2 | C-12 diamond (99.99%) | Spin silence, lattice-compatible buffer | ESTABLISHED |
| 2.5 | Ni-62 thin film (I=0) | Exchange field: breaks TRS (BDI→D) | REQUIRED (sim) |
| 3 | Penrose graphene ZGNR | Quasicrystalline curvature field + SW defects | MOTIVATED |
| 3.5 | Bismuth proximity | Rashba SOC: Dirac → Weyl splitting | REQUIRED (theory) |
| 4 | Niobium (Tc=9.3K) | Proximity-induced superconductivity | ESTABLISHED |
| 5 | He-3/He-4 mixture | Hamiltonian tuning | SPECULATIVE |

All three isotopes (Si-28, C-12, Ni-62) have nuclear spin I=0. Proved in Lean: `full_stack_spin_silent` (rfl).

---

## Simulation Campaign (L3)

### FWS Pipeline (7 steps)

| Step | Script | Lines | Result | Key Finding |
|------|--------|-------|--------|-------------|
| Lattice | graphene_sw_lattice.py | 472 | **PASS** | Corrected honeycomb + Penrose SW, CN={2,3,4}, δt≈9.7% |
| PGTC | run_all.py | 502 | **PASS** | κ=0.30 (70% suppression), 12 localized modes, gap ratio 58.8× |
| Baseline | step1_clean_baseline.py | 459 | **PASS** | BDI trivial in d=2. Exchange required. |
| Exchange | step3_spinful_bdg.py | 617 | **PASS** | Gap closes h_ex≈0.6. BDI→D confirmed. Hermitian-exact. |
| Fine scan | step3b_finescan.py | 490 | **PASS** | Bott B=+1 (h_ex=0), B=-1 (h_ex=1.1). Quantized. |
| 3D bilayer | step4_bilayer_3d.py | 764 | PARTIAL | First 3D attempt. |
| Matched | step4b_matched_bilayer.py | 483 | PARTIAL | Defect localization 80-92%. Gap locked by Δ. |

### Vortex Dynamics

| Script | Lines | Content | Status |
|--------|-------|---------|--------|
| helium_loom_simulator.py | 503 | 2D GP trefoil, winding audit | DEMONSTRATED |
| helium_loom_v2_pinned.py | 294 | Fibonacci pinning test | DEMONSTRATED |
| helium_loom_v3_3d.py | 443 | 3D trefoil filament | DEMONSTRATED |
| gp3d_readwrite.py | 544 | 3D READ/WRITE topological cycle | DEMONSTRATED |
| gp3d_solver.py | 633 | JAX-accelerated GP solver | Infrastructure |

### MHD

| Script | Lines | Content | Status |
|--------|-------|---------|--------|
| stellarator_taylor_relaxation.py | 301 | Energy decays faster than helicity | DEMONSTRATED |

### Superseded (preserved as failure record)

| Script | Lines | Failure |
|--------|-------|---------|
| penrose_bdg_2d.py | 823 | v1 lattice: Penrose vertices as sites. CN={3..10}, δt=59%, 0 MZMs. |
| penrose_phonon_2d.py | 779 | v1 phonon on wrong lattice. |

### Critical Fix History

- v1 lattice FAILED (Penrose vertices, CN={3..10}, dt=59%). Fixed: honeycomb + face-traced SW.
- Rashba Hermiticity error (0.35) produced 4 spurious MZMs. Fixed: corrected conjugation.
- Mismatched bilayer FAILED (pristine L2 dominated). Fixed: matched layers.

---

## Canonical File Map

### L0 — Foundations

| File | Thm | Ax | Sorry | Notes |
|------|-----|-----|-------|-------|
| LogicKernel.lean | 1 | 1 | 0 | Winding-number identity. ⚠ Rename `Univalence` pending. |

### L1 — Algebra

| File | Thm | Ax | Sorry | Notes |
|------|-----|-----|-------|-------|
| Clifford.lean | 12 | 0 | 0 | Cl(2,0), Cl(3,0). Gap condition, protection hierarchy. |
| CayleyDickson.lean | 3 | 0 | 0 | Octonion non-associativity. |
| Winding.lean | 0 | 0 | 0 | Cl(1,0)→Cl(2,0) ladder. Definitions only. |
| CLHoTT.lean | 7 | 0 | 6 | **Frozen.** Float algebra sorry. Path to close: ℤ/ℚ. |

### L2 — Classification

| File | Thm | Ax | Sorry | Notes |
|------|-----|-----|-------|-------|
| AlgebraicLadder.lean | 16 | 0 | 0 | AZ tenfold way, Bott periodicity. |
| KitaevCertification.lean | 35 | 0 | 0 | §12–§14. Phase boundary, BBC ∀N≥2. |
| EdgeModes.lean | 33 | 0 | 0 | Station Q certification, edge localization. |
| Bridge.lean | 9 | 21 | 0 | HoTT + Bridge Axioms A–G. Best-documented file. |
| FWS.lean | 22 | 0 | 0 | Device classification, Penrose curvature, AZ symmetries. |
| RunGDescend.lean | 13 | 0 | 0 | Algebraic ladder ℝ→ℂ→ℍ→𝕆. **New in v4.5.** |

### Archive

| File | Thm | Ax | Sorry | Notes |
|------|-----|-----|-------|-------|
| SingularityAsTypeError.lean | 17 | 21 | 3 | ⚠ RETRACTED axiom. Preserved as methodology. |
| TopologicalInvariant.lean | 1 | 15 | 1 | Real' scaffolding. `gapless_invariant_undefined`. |
| GeometryOfState_verified3.lean | 8 | 0 | 0 | Verification pillars. |
| TrivialPhaseCheck.lean | 2 | 0 | 0 | Quick check proofs. |

---

## Altland-Zirnbauer Tenfold Way

| Class | T | C | S | Inv(1D) | Inv(2D) | Inv(3D) | Notes |
|-------|---|---|---|---------|---------|---------|-------|
| A | 0 | 0 | 0 | 0 | ℤ | 0 | |
| AIII | 0 | 0 | 1 | ℤ | 0 | ℤ | |
| AI | +1 | 0 | 0 | 0 | 0 | 0 | Bulk graphene |
| **BDI** | +1 | +1 | 1 | **ℤ** | **0** | 0 | Kitaev chain (with T). **2D TRIVIAL.** |
| **D** | 0 | +1 | 0 | ℤ₂ | **ℤ** | 0 | After Ni-62 exchange. **TARGET.** |
| DIII | -1 | +1 | 1 | ℤ₂ | ℤ₂ | ℤ | |
| AII | -1 | 0 | 0 | 0 | ℤ₂ | ℤ₂ | TIs: Bi₂Se₃ |
| CII | -1 | -1 | 1 | 2ℤ | 0 | ℤ₂ | |
| C | 0 | -1 | 0 | 0 | ℤ | 0 | |
| CI | +1 | -1 | 1 | 0 | 0 | ℤ | |

BDI 1D: ℤ (winding number, w=1). 2D: 0 (TRIVIAL — simulation confirmed). Breaking TRS via Ni-62 → D row: 2D has ℤ (Bott index). Under interactions, BDI ℤ → ℤ₈; w=1 survives.

---

## The Ascending Ladder

| Step | Constraint Released | Capability Gained | Status |
|------|-------------------|-------------------|--------|
| ℝ → ℂ | Ordering | Rotation (π₁(S¹)=ℤ, phase, topology) | **PROVED** (L1–L2) |
| ℂ → ℍ | Commutativity | Spin (non-abelian structure, chirality) | **PROVED** (Cl(3,0)); quaternion junction **SPECULATIVE** |
| ℍ → 𝕆 | Associativity | Gauge (exceptional Lie groups, E₈) | **SPECULATIVE** — Clifford algebras are associative; octonions are not. |

**[SPECULATIVE]** Cayley-Dickson and Clifford ladders agree at ℝ, ℂ, ℍ but diverge at 𝕆. This tension is the most important structural question in the framework.

---

## The Stellarator Connection [SPECULATIVE]

Taylor relaxation in 3D plasmas conserves magnetic helicity K = ∫ A·B dV — the abelian Chern-Simons functional. The plasma relaxes to minimum energy consistent with this topological constraint.

Lean theorems (knot type and helicity conservation without reconnection) formalize the same mathematics applied to magnetic field lines. **[PROVED]**

The FWS-to-stellarator structural analogy and the identification of the Kodama ground state with the Chern-Simons functional remain **[SPECULATIVE]**.

---

## Socratic Partner Architecture (NEW in v4.5)

The Glassbox methodology is operationalized through a constitutional multi-agent verification system. Claims are interrogated from structurally different epistemic positions. Agreement across constitutions is evidence of robustness; disagreement surfaces tensions for human resolution.

### Constitutional Agents

| Agent | Epistemic Commitment | Activates for |
|-------|---------------------|---------------|
| **Noether** | Structural reasons > specific results | Conservation laws, symmetries, generalizations |
| **Grothendieck** | Wrong foundations make problems hard | Elaborate machinery, paradigm-level questions |
| **Weyl** | Global symmetry must hold locally | Invariance claims, robustness under perturbation |
| **Atiyah** | Cross-domain coincidence IS the theorem | TBC instantiations, unexpected convergences |
| **Voevodsky (Lean)** | Machine-verified or not proved | Any PROVED claim. Axiom auditing. |
| **Voevodsky (Agda)** | Existence requires construction | HoTT claims, path computation, bridge axioms |
| **Dirac** | Physical necessity guides math | Physical significance of abstract results |
| **Kitaev** | Topology protects information | Robustness, AZ classification, protection claims |

### Operating Principles

- Tensions are features, not bugs. Disagreement is surfaced, not flattened.
- The compiler outranks everyone. On PROVED claims, Voevodsky has final authority.
- The human outranks the system. Direction and value decisions are the architect's.
- Kill conditions before results. Define falsification criteria before assessing truth.
- Retraction is strength. A documented retraction demonstrates the system works.

Full specification: `Socratic_Partner_Prompt_Profile.md`.

---

## TAS Methodology

**Thesis:** Simulation produces a result (1D chain → MZMs, 2D PGTC → κ=0.30).

**Antithesis:** Type checker or computation rejects. Examples: Stage 1 FAIL (wrong lattice). Rashba non-Hermitian (spurious MZMs). Mismatched bilayer (Layer 2 dominates). Core thesis retraction (`Empty = Empty` by `rfl`).

**Synthesis:** Hidden assumption surfaced, corrected, re-run. Each failure localized exactly what was wrong. The singularity thesis retraction is itself a TAS cycle: the architecture applied to its own foundations and self-corrected.

---

## Established Findings

| Finding | Evidence | Implication |
|---------|----------|-------------|
| PGTC self-protection | κ_QP/κ_ord = 0.30 in 2D | Same geometry protects topology + suppresses phonons |
| AZ classification holds | BDI trivial d=2, D has ℤ | Tenfold way predictions confirmed computationally |
| Exchange transition | Gap closes h_ex ~ 0.55 | Ni-62 drives BDI → D topological transition |
| p-wave Bott B=1 | Integer-quantized at h_ex=0 | Defected lattice intrinsically topological with p-wave |
| Defect localization | 80–92% at SW sites | Physics concentrates at 5/7 domain walls |

## Not Yet Demonstrated

| Gap | What's needed |
|-----|---------------|
| Genuine MZMs at defect sites | Larger lattice (1000+ sites, periodic boundaries) |
| Weyl nodes in normal state | Larger system or periodic Penrose approximant |
| 3D topological enhancement | Bilayer Bott indices trivial at current size |
| Fracton phase signatures | Roadmap Stage 6 (ED/DMRG) |

---

## Document Map (v4.5)

### Architecture & Audits

| Document | Layer | Role |
|----------|-------|------|
| ARCHITECTURE_v4.5.md | L0–L6 | **This document.** Single source of truth for project state. |
| ARCHITECTURE_v3_to_v4_changes.md | Meta | Retraction change log |
| GoS_COMPLETE_AUDIT.md | All | Previous audit |
| AUDIT_v2.md | All | Claude audit (March 25, 2026) — retraction-aware |

### Thesis & Methodology

| Document | Layer | Role |
|----------|-------|------|
| Glassbox_ConstitutionalXAI_v2_Final.docx | L6 | Epistemic tagging, Socratic Partners, Red Screen Protocol |
| Socratic_Partner_Prompt_Profile.md | L6 | Constitutional agent specification (prompt architecture) |
| HiTT_Architectural_Draft_v0_2.docx | L0–L3 | Revised thesis, CLHoTT kernel, retraction record |
| GeometryOfState_Thesis_WhitePaper.docx | L1–L5 | Original thesis document |

### Physics & Device

| Document | Layer | Role |
|----------|-------|------|
| GoS_Quasiperiodic_Ratchet_Thesis_v3.docx | L3 | PGTC, ratchet, ascending ladder |
| Topological_Invariants_as_Dependent_Types.docx | L2–L3 | IsGapped → ℤ, phase transition formalization |
| topological_boundary_coherence_outline.docx | L2–L5 | TBC theorem, three instantiations |
| The_Thermodynamic_Bootstrap_Case_Study.docx | L5 | Verification methodology |
| MZM_Certification_Architecture.docx | L5 | Three-gate protocol |
| FWS_Engineering_Spec_v2.docx | L4 | Material stack (Ni-62, Bi) |
| FWS_Simulation_Roadmap.docx | L4 | 7-stage gated pipeline |

### Strategy & Proposals

| Document | Layer | Role |
|----------|-------|------|
| GoS_Research_Proposal_Updated.md | Meta | Research proposal (current) |
| GoS_Technical_Briefing.docx | Meta | Technical briefing |
| StationQ_Collaboration_Proposal.docx | Meta | Microsoft collaboration proposal |
| GoS_Systems_Architecture_Blueprint_2026-2050.docx | Meta | Long-range architecture |
| GoS_Year1_Plan_2026.docx | Meta | Year 1 operational plan |

### Industry

| Document | Layer | Role |
|----------|-------|------|
| Digital_Triplet_Architecture_Preprint.docx | L4–L5 | Digital triplet concept |
| FVDT_Industry5_Paper_Draft.docx | L4–L5 | Industry 5.0 paper |
| fvdt_paper.docx | L4–L5 | FVDT paper |
| QM_Foundation_NotebookLM_Architecture.docx | Meta | NotebookLM integration |

---

## Dependency Rules

1. L1 imports nothing except Lean core. Zero Mathlib.
2. L2 imports L1 only. Classification builds on algebra.
3. L3 imports L2 numerically. Python reads the same structures.
4. L4 imports L3 predictions. Device spec references computed results.
5. L5 imports all layers. Verification must access every level.
6. L6 operates on the reasoning process itself. Meta-layer.
7. No layer skips a level. L4 does not directly reference L1.

---

## Open Problems (Priority Order)

| # | Problem | Layer | Status |
|---|---------|-------|--------|
| 1 | arXiv preprint on PGTC result | L3 | READY NOW |
| 2 | BivectorDiscrimination.lean — prove core theorem | L1 | READY NOW |
| 3 | Repository reorganization (this document) | Meta | IN PROGRESS |
| 4 | Larger lattice (1000+ sites, periodic) for MZM resolution | L3 | Next simulation |
| 5 | DFT validation of Harrison scaling at SW defects | L3/L4 | HPC required |
| 6 | 3D normal-state Weyl node search | L3 | HPC required |
| 7 | AZ: formally show 5/7 boundary maps AI→D | L2 | Partially done |
| 8 | Cubical Agda: winding number with computational content | L0 | Planned |
| 9 | Float sorry: refactor CLHoTT.lean to ℤ/ℚ | L1 | Low priority |

---

## Horizon Extensions

| Extension | Layer | Status | What it adds |
|-----------|-------|--------|-------------|
| Linear HoTT (LHoTT) | L0 | FUTURE | No-cloning, braiding as homotopy types |
| QGA = Cl(2,0) | L1 | CONNECTED | Qubit as bivector |
| Interaction collapse | L2 | KNOWN LIMIT | ℤ → ℤ₈ under interactions. w=1 survives. |
| Many-Body RSIs | L2 | FUTURE | Beyond free fermions |
| Floquet engineering | L3/L4 | FUTURE | Dynamic topology via periodic drives |
| Intrinsic TSC (FeSCs) | L4 | ALTERNATIVE | LiFeAs, FeTeSe |
| TDA (persistent homology) | L5 | SPECULATIVE | Fourth verification channel |
| Stellarator/Chern-Simons | L4/L5 | SPECULATIVE | Taylor relaxation = Kodama ground state |
| Bivector Discrimination | L1/L5 | PLANNED | MZM/ABS discrimination via Clifford invariance |

---

## Known Limitations

- **Classification collapse under interactions.** BDI ℤ → ℤ₈. w=1 survives. Higher winding numbers need interaction analysis.
- **Free-fermion only.** L2 handles non-interacting electrons.
- **Static architecture.** Fixed material stack. Floquet extension would make defects reconfigurable.
- **Finite lattice size.** 264–528 sites. ξ ~ 100 sites. MZM splitting may exceed topological gap.
- **Normal state gapped.** Gap 0.011, not semimetallic. Weyl nodes not observed.
- **Cayley-Dickson/Clifford divergence.** Agree at ℝ, ℂ, ℍ; diverge at 𝕆. Framework cannot handle octonion level.
- **Retracted thesis residue.** Earlier documents may reference "singularities as type errors." Update or mark [RETRACTED] as encountered.
- **Axiom count optics.** 58 axiom declarations looks large without the categorical breakdown. Always present with categories.

---

## Building

```bash
# Lean 4 (L1 + L2)
lake build

# Python simulations (L3)
python3 graphene_sw_lattice.py      # Generate corrected lattice
python3 run_all.py                  # PGTC main pipeline
python3 step1_clean_baseline.py     # BDI baseline
python3 step3_spinful_bdg.py        # Ni-62 exchange BdG
python3 step3b_finescan.py          # Parameter scan + Bott indices
python3 step4b_matched_bilayer.py   # 3D matched bilayer
```

Requires Lean 4 v4.12.0. Python requires NumPy and SciPy.

---

## Archive Inventory

The repository contains 22 duplicate/copy files and 34 archived Lean files representing version history. Full classification in `GoS_v3_Snapshot_v4_Plan.md`. These are preserved for methodology documentation and are not active code.

---

*Geometry of State · GoS-Architect · github.com/GoS-Architect*

*The compiler is the credential. The retraction is the proof of honesty.*
