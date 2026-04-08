# Geometry of State — Repository Structure v5 (Proposed)

**Author:** Adrian Domingo · GoS-Architect
**Date:** March 2026
**Purpose:** Update repo folder structure to properly separate three distinct components: verified code, project documentation, and Socratic Partner agent infrastructure. Current repo mixes these; this proposal cleans it up.

---

## Design Principles

The repo serves three audiences with three different needs, and the folder structure should reflect that cleanly.

**The compiler** reads the Lean and Agda files. It needs a clean import graph with no circular dependencies, strict layer ordering, and zero ambiguity about what is active code vs. archived code. The compiler doesn't care about documentation.

**The reader** (collaborator, reviewer, endorser, hiring manager) reads the documentation. They need to find the right document fast, understand the project state, and trace any claim back to its evidence. They don't need to read Lean.

**The agents** (Socratic Partner constitutions) are operational infrastructure that drives the verification ecology described in Glassbox v2 §6–7. They are not documentation (they do things) and not proof code (they don't compile to theorems). They are the governance layer — L6 in the architecture — and they need their own home.

---

## Proposed Structure

```
GeometryOfState/
│
├── README.md                          # Project overview, build instructions, quick start
├── lakefile.lean                      # Lean 4 build configuration
├── lean-toolchain                     # Lean version pin (v4.12.0)
│
├── src/                               # ═══ VERIFIED CODE (L0–L2) ═══
│   │                                  # Everything here compiles. No sorry in L2.
│   │
│   ├── L1_Algebra/                    # Layer 1: Algebraic structures
│   │   ├── Clifford.lean             # Cl(2,0), Cl(3,0), 12 theorems, 0 sorry
│   │   ├── CayleyDickson.lean        # Octonions, 3 theorems, 0 sorry
│   │   ├── Winding.lean              # Definitions (no theorems)
│   │   └── CLHoTT.lean              # FROZEN: 7 theorems, 6 sorry (Float)
│   │
│   ├── L2_Classification/            # Layer 2: Topological classification
│   │   ├── AlgebraicLadder.lean      # AZ tenfold way, Bott periodicity, 16 theorems
│   │   ├── KitaevChain.lean          # Kitaev chain, winding number, 35 theorems
│   │   ├── EdgeModes.lean            # Edge mode existence ∀N≥2, 33 theorems
│   │   ├── Bridge.lean               # Protection theorems, 9 theorems, 7 bridge axioms
│   │   └── FWS.lean                  # Device classification, 30 theorems
│   │
│   ├── L1_Planned/                    # Planned L1 files (not yet compiling)
│   │   ├── SpinGroup.lean            # Spin(2,0), Pin(2,0) — 1–2 weeks
│   │   ├── BivectorDiscrimination.lean # Core discrimination theorem — days
│   │   └── EdgeModeBivector.lean     # L1↔L2 bridge — 4–8 weeks
│   │
│   └── Foundations/                   # L0 support files
│       ├── LogicKernel.lean          # ⚠ Rename Univalence → winding_determines_state
│       ├── TopologicalInvariant.lean # Real' scaffolding, 1 sorry
│       ├── GeometryOfState_verified3.lean # Legacy verified file, 8 theorems
│       └── TrivialPhaseCheck.lean    # 2 theorems
│
├── simulations/                       # ═══ COMPUTATIONAL PHYSICS (L3) ═══
│   │                                  # Python/NumPy/SciPy. Results are DEMONSTRATED.
│   │
│   ├── ratchet_full.py               # 1D BdG + phonon transport — PASS
│   ├── graphene_sw_lattice.py        # Corrected v2 honeycomb + SW generator
│   ├── run_all.py                    # 2D PGTC main pipeline — PASS
│   ├── step1_clean_baseline.py       # BDI baseline in d=2 — CONFIRMED
│   ├── step3_spinful_bdg.py          # Ni-62 exchange BDI→D — TRANSITION
│   ├── step3b_finescan.py            # Bott index parameter scan — B=+1
│   ├── step4b_matched_bilayer.py     # 3D bilayer — PARTIAL
│   │
│   ├── results/                       # Simulation output (JSON, CSV)
│   │   ├── stage2_summary.json       # v2 corrected lattice results
│   │   ├── ratchet_full_results.json # 1D results
│   │   └── SIMULATION_RESULTS.md     # Campaign summary with pass/fail tables
│   │
│   └── failed/                        # ═══ PRESERVED FAILURES ═══
│       ├── stage1_summary.json       # v1 Penrose-vertex lattice (FAILED)
│       ├── combined_report.json      # v1 full pipeline (ALL GATES FAIL)
│       └── penrose_bdg_2d.py         # v1 script (SUPERSEDED)
│
├── agda/                              # ═══ CUBICAL AGDA (L0, planned) ═══
│   ├── Circle.agda                   # S¹ HIT, encode-decode, π₁(S¹)≅ℤ
│   ├── Winding.agda                  # windingNumber : ΩS¹ → ℤ (computable)
│   ├── KitaevWinding.agda            # BdG → loop on S¹ → winding number
│   └── Bridge.agda                   # Cross-verify with Lean 4 classification
│
├── agents/                            # ═══ SOCRATIC PARTNER INFRASTRUCTURE (L6) ═══
│   │                                  # NOT documentation. Operational governance layer.
│   │                                  # Drives TAS protocol, epistemic tagging, retraction.
│   │
│   ├── README.md                     # How the verification ecology works
│   ├── CONSTITUTIONS.md              # All 13 constitutions with epistemic commitments
│   │
│   ├── constitutions/                 # Individual agent definitions
│   │   ├── noether.md                # Abstraction auditor: structural reasons > results
│   │   ├── grothendieck.md           # Foundational refactorer: right abstraction level
│   │   ├── weyl.md                   # Gauge consistency checker: local ↔ global
│   │   ├── atiyah.md                 # Cross-domain correspondence detector
│   │   ├── voevodsky.md              # Formal verification gatekeeper (interfaces w/ Lean)
│   │   ├── dirac.md                  # Physical grounding enforcer
│   │   ├── kitaev.md                 # Robustness certifier: topological protection
│   │   ├── schrodinger.md            # Interdisciplinary provocateur
│   │   ├── albert_cartan.md          # Taxonomist: classify first, study second
│   │   ├── cayley_dickson.md         # Trade-off auditor: what you sacrifice, what you gain
│   │   ├── bott.md                   # Pattern recurrence detector: period 8
│   │   ├── hestenes.md              # Explanation translator: geometry > formalism
│   │   └── england.md               # Thermodynamic grounding: energy gradients
│   │
│   ├── protocols/                     # Verification ecology procedures
│   │   ├── tas_protocol.md           # Thesis-Antithesis-Synthesis cycle specification
│   │   ├── retraction_protocol.md    # Multi-agent retraction (cross-constitutional)
│   │   ├── tag_generation.md         # How agent pairs generate epistemic tags
│   │   └── red_screen_protocol.md    # Kill condition specification and enforcement
│   │
│   └── pairs/                         # Cross-constitutional verification pairs
│       ├── voevodsky_dirac.md        # Verified AND grounded
│       ├── noether_grothendieck.md   # Explained AND correctly framed
│       ├── kitaev_weyl.md            # Robust AND locally consistent
│       ├── atiyah_bott.md            # Convergent AND recurrent
│       ├── cayley_dickson_albert.md  # Trade-offs explicit AND classification complete
│       └── hestenes_schrodinger.md   # Transparent AND provocative
│
├── docs/                              # ═══ PROJECT DOCUMENTATION ═══
│   │                                  # For humans. Not compiled. Not operational.
│   │
│   ├── architecture/                  # Architecture documents
│   │   ├── ARCHITECTURE_v4.md        # CURRENT: Systems architecture
│   │   ├── ARCHITECTURE_v3_to_v4_changes.md # Retraction audit trail
│   │   └── GoS_Repository_Audit_v2.md # Hard audit: 46 axioms, 155 theorems
│   │
│   ├── thesis/                        # Thesis documents (versioned)
│   │   ├── GeometryOfState_Thesis_WhitePaper.docx
│   │   ├── TheGeometryOfState_SystemsArchitecture.docx
│   │   ├── HiTT_Architectural_Draft_v0_1.docx  # ⚠ Contains retracted thesis
│   │   ├── HiTT_Architectural_Draft_v0_2.docx  # Revised thesis
│   │   └── GoS_Quasiperiodic_Ratchet_Thesis.docx
│   │
│   ├── concept_papers/                # Technical concept papers (5)
│   │   ├── bivector_invariance_concept_v3.docx
│   │   ├── PGTC_2D_Simulation_Concept.md
│   │   ├── AZ_Class_Transition_Concept.md
│   │   ├── Topological_Boundary_Coherence_Concept.md
│   │   └── Cubical_Agda_Winding_Number_Concept.md
│   │
│   ├── device/                        # Device engineering documents
│   │   ├── FWS_Engineering_Spec_v2.docx
│   │   └── Ni62_FWS_physics_analysis.md
│   │
│   ├── methodology/                   # Glassbox methodology documents
│   │   ├── Glassbox_ConstitutionalXAI_v2.docx
│   │   ├── Auditable_Reasoning_Memo_v2.docx
│   │   └── Prophets_Programmers_Rosetta_Stones.md
│   │
│   ├── literature/                    # Literature reviews
│   │   ├── quantum_materials_GoS_reference_v3.md
│   │   ├── quantum_materials_GoS_reference_v2.md
│   │   ├── quantum_materials_GoS_reference.md
│   │   └── quantum_materials_review_filtered.md
│   │
│   ├── preprint/                      # arXiv preprint materials
│   │   └── PGTC_DRAFTING_BRIEF.md
│   │
│   ├── inventories/                   # Single-source-of-truth files
│   │   ├── theorem_inventory_v2.md   # 155 theorems catalogued
│   │   └── PROJECT_BRIEF.md          # Complete state for new sessions
│   │
│   └── novelty/                       # Novelty and prior art analysis
│       └── singularity_type_error_novelty_report.md
│
├── book/                              # ═══ THE OMNIVALENCE POSTULATE (book project) ═══
│   │                                  # Separated from GoS documentation.
│   │                                  # Book draws on GoS but is its own project.
│   │
│   ├── Table_of_Contents_Draft.md
│   ├── Omnivalence_Documentation_Map_v2.md
│   ├── Omnivalence_Philosophical_Notebook.md
│   ├── compass_research_report.md    # External academic sources
│   └── chapters/                      # Chapter drafts (when written)
│       └── .gitkeep
│
├── archive/                           # ═══ RETRACTED / SUPERSEDED CODE ═══
│   │                                  # Preserved for methodology documentation.
│   │                                  # Not active. Not imported by anything.
│   │
│   └── SingularityAsTypeError.lean   # ⚠ RETRACTED: ConservationOfInformation inconsistent
│                                      #   Contains: Empty = Empty by rfl contradiction
│                                      #   Formal observations (IsSingularity, etc.) remain valid
│                                      #   Interpretation changed: see ARCHITECTURE_v4.md
│
└── artifacts/                         # ═══ INTERACTIVE / VISUAL ARTIFACTS ═══
    └── topology_of_everything.jsx    # Socratic instruction manual (React)
```

---

## Key Decisions and Rationale

### Why `agents/` is separate from `docs/`

The Socratic Partner constitutions are not descriptions — they are specifications. Each constitution defines an epistemic commitment that determines how that agent evaluates claims. The verification ecology (Glassbox v2 §7) specifies how agent pairs interact to generate epistemic tags, execute retractions, and run the TAS protocol. This is operational infrastructure: when you run a TAS cycle, you are executing the agents/protocols. When you read a document, you are reading docs/.

The practical difference: if you change a constitution (say, tightening the Voevodsky agent's acceptance threshold), that changes how future claims get evaluated. If you change a document (say, updating the theorem count), that changes what humans read. Different audiences, different change semantics, different folders.

### Why `book/` is separate from `docs/`

The Omnivalence Postulate is a book project that draws on the GoS research but is not the GoS research itself. The book makes claims that go beyond anything in the repository (the postulate statement, the type error cascade, the ISR resolution). Keeping it separate prevents confusion between what is proved/demonstrated in GoS and what is argued in the book.

### Why `archive/` exists

The Glassbox methodology requires that retracted content be preserved, not deleted. SingularityAsTypeError.lean contains a provably inconsistent axiom (ConservationOfInformation), but the formal observations in that file (IsSingularity, PhysicalLaw, the "singularity blocks construction" pattern) remain valid. Archiving preserves the methodology evidence while preventing the inconsistent axiom from being imported by active code.

The archive header should read:
```lean
/- RETRACTED (March 2026)
   The axiom ConservationOfInformation in this file is provably inconsistent:
   Empty = Empty by rfl, contradicting Impossible (state = Empty).
   
   Formal observations (IsSingularity, PhysicalLaw) remain valid.
   Interpretation changed: see docs/architecture/ARCHITECTURE_v4.md §Core Thesis.
   
   This file is preserved as methodology documentation, not active code.
-/
```

### Why `simulations/failed/` exists

Same principle as archive/. The v1 Penrose-vertex lattice failure is methodology evidence. The PGTC preprint includes the failure history as a methodology section. Deleting failed results would violate the Red Screen Protocol.

---

## Layer → Folder Mapping

| Layer | Folder(s) | Content Type |
|-------|-----------|-------------|
| L0 Foundations | `src/Foundations/`, `agda/` | Lean kernel, Cubical Agda |
| L1 Algebra | `src/L1_Algebra/`, `src/L1_Planned/` | Clifford algebras, CLHoTT |
| L2 Classification | `src/L2_Classification/` | AZ, Kitaev, edge modes, FWS |
| L3 Physics | `simulations/` | Python BdG, phonon transport |
| L4 Device | `docs/device/` | FWS spec, Ni-62 analysis |
| L5 Verification | `docs/concept_papers/bivector*` | Certification architecture |
| L6 Governance | `agents/`, `docs/methodology/` | Constitutions, protocols, Glassbox |

---

## Migration Checklist

Moving from current flat structure to this tree:

| Action | Files Affected | Risk |
|--------|---------------|------|
| Move .lean files into `src/L1_Algebra/` and `src/L2_Classification/` | 14 files | LOW — update lakefile.lean imports |
| Move SingularityAsTypeError.lean to `archive/` | 1 file | LOW — nothing imports it (confirmed by Audit v2) |
| Create `agents/` tree from Glassbox v2 §6 | New files | NONE — net new content |
| Create `book/` tree | New files | NONE — net new content |
| Move simulation scripts to `simulations/` | ~8 files | LOW — update any relative paths |
| Move all .docx/.md docs to `docs/` subtree | ~20 files | NONE — docs don't import anything |
| Update lakefile.lean for new source paths | 1 file | MEDIUM — must recompile and verify all 155 theorems still pass |
| Update ARCHITECTURE_v4.md file map references | 1 file | LOW — path changes only |

---

## What This Doesn't Cover

This proposal addresses folder structure only. It does not address:

- **Agent implementation**: Whether the Socratic Partners are implemented as LLM prompts, as Lean metaprograms, as CI/CD pipeline stages, or as something else entirely. The `agents/` folder contains their specifications (constitutions + protocols). Implementation is a separate decision.
- **CI/CD**: Whether `lake build` runs automatically on push, whether simulation results are cached, whether the TAS protocol is automated. These are infrastructure decisions that depend on the agent implementation choice.
- **Mathlib migration**: If/when the repo adds Mathlib as a dependency (eliminating 15 Real' scaffolding axioms), the `src/Foundations/TopologicalInvariant.lean` file would be substantially refactored. The folder structure accommodates this without change.
- **PhysLean contribution**: The TBC concept paper targets PhysLean upstream. If accepted, some `src/` content would migrate to a PhysLean PR while remaining in GoS as a dependency. The folder structure accommodates this.

---

*Geometry of State · GoS-Architect · github.com/GoS-Architect*

*The compiler is the credential. The retraction is the proof of honesty.*
