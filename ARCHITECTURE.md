# GEOMETRY OF STATE — Systems Architecture

**A Layered Framework for Topological Quantum Matter**

Adrian Domingo · GoS-Architect · March 2026

---

## Overview

The Geometry of State (GoS) is a systems architecture connecting formal
verification (Lean 4, Cubical Agda) through algebraic structures and
topological classification to physical predictions, device design, and
experimental certification.

The architecture is organized into six layers. Each layer imports from
the layer below and exports to the layer above. No layer skips a level.
The dependency direction is strictly upward.

---

## Layer Diagram

```
╔═══════════════════════════════════════════════════════════════╗
║  L5  VERIFICATION                                            ║
║  How do we know it's real?                                   ║
║  ┌─────────────────────┐  ┌────────────────────────────────┐ ║
║  │ MZM Certification   │  │ Thermodynamic Bootstrap        │ ║
║  │ Architecture        │  │ TAS Dialectic, Red/Blue Team   │ ║
║  └─────────────────────┘  └────────────────────────────────┘ ║
╠═══════════════════════════════════════════════════════════════╣
║  L4  DEVICE                                                  ║
║  What do we build?                                           ║
║  ┌─────────────────────┐  ┌────────────────────────────────┐ ║
║  │ FWS Engineering     │  │ Simulation Roadmap             │ ║
║  │ Spec (material      │  │ 7 stages, gated, kill          │ ║
║  │ stack, fabrication)  │  │ conditions at each gate        │ ║
║  └─────────────────────┘  └────────────────────────────────┘ ║
╠═══════════════════════════════════════════════════════════════╣
║  L3  PHYSICS                                                 ║
║  What does the math predict?                                 ║
║  ┌──────────────────┐  ┌──────────────┐  ┌───────────────┐  ║
║  │ Thesis (PGTC,    │  │ ratchet_     │  │ penrose_      │  ║
║  │ ratchet, MZMs,   │  │ full.py      │  │ bdg_2d.py     │  ║
║  │ ascending ladder) │  │ 1D: PASS     │  │ 2D: FAIL*     │  ║
║  └──────────────────┘  └──────────────┘  └───────────────┘  ║
╠═══════════════════════════════════════════════════════════════╣
║  L2  CLASSIFICATION                                          ║
║  Which topological phase?                                    ║
║  ┌────────────────┐ ┌──────────┐ ┌──────┐ ┌──────┐ ┌─────┐ ║
║  │ Algebraic      │ │ Kitaev   │ │ Edge │ │Bridge│ │ FWS │ ║
║  │ Ladder (13thm) │ │ Chain    │ │ Modes│ │(9thm)│ │(22) │ ║
║  │ AZ, Bott, ∀N   │ │ (35thm) │ │ (33) │ │      │ │     │ ║
║  └────────────────┘ └──────────┘ └──────┘ └──────┘ └─────┘ ║
╠═══════════════════════════════════════════════════════════════╣
║  L1  ALGEBRA                                                 ║
║  What are the structures?                                    ║
║  ┌────────────────┐ ┌──────────────┐ ┌───────┐ ┌─────────┐ ║
║  │ Clifford.lean  │ │ CayleyDick-  │ │Winding│ │ CLHoTT  │ ║
║  │ Cl(2,0),Cl(3,0)│ │ son.lean     │ │ .lean │ │ (frozen)│ ║
║  │ 12 theorems    │ │ 𝕆, 3 theorems│ │ defs  │ │ 7, 6sorry║
║  └────────────────┘ └──────────────┘ └───────┘ └─────────┘ ║
╠═══════════════════════════════════════════════════════════════╣
║  L0  FOUNDATIONS                                             ║
║  What can we prove?                                          ║
║  ┌─────────────────────┐  ┌────────────────────────────────┐ ║
║  │ Lean 4 v4.12.0      │  │ Cubical Agda (planned)         │ ║
║  │ Zero Mathlib deps   │  │ π₁(S¹)≅ℤ proved, univalence   │ ║
║  │ Kernel is verifier   │  │ Winding number with content    │ ║
║  └─────────────────────┘  └────────────────────────────────┘ ║
╚═══════════════════════════════════════════════════════════════╝
```

*Stage 1 FAIL diagnosis: wrong lattice (Penrose vertices, not graphene
with Penrose-seeded defects). Modulation 59% vs physical 10%. TAS
antithesis, not termination.

---

## Dependency Rules

1. **L1 imports nothing** except Lean core. Zero Mathlib.
2. **L2 imports L1 only.** Classification builds on algebra.
3. **L3 imports L2 numerically.** Python reads the same structures.
4. **L4 imports L3 predictions.** Device spec references computed results.
5. **L5 imports all layers.** Verification must access every level.
6. **No layer skips a level.** L4 does not directly reference L1.

---

## Theorem Census

| Layer | Files | Theorems | Sorry | Proof techniques |
|-------|-------|----------|-------|------------------|
| L1 Algebra | 4 | 22 | 6 | rfl, decide, sorry(Float) |
| L2 Classification | 5 | 112 | 0 | rfl, native_decide, decide, omega, induction |
| Archive | 5 | 13 | 1 | rfl, intro+exact |
| **Total** | **14** | **147** | **7** | |

All 7 sorry are Float arithmetic in CLHoTT.lean (6) and
TopologicalInvariant.lean (1, archived). Zero sorry in any
finite verification theorem. Zero sorry in any classification theorem.

---

## Document Map

Each document lives at the layer where its content operates.

| Document | Layer | Role |
|----------|-------|------|
| Quasiperiodic Ratchet Thesis | L3 | Theory: PGTC, ratchet, MZMs, ascending ladder |
| Topological Invariants as Dependent Types | L3 | Formal paper: IsGapped → ℤ, phase transition as type error |
| FWS Engineering Spec | L4 | Material stack: Si-28, C-12, Penrose graphene, Nb, He-3/4 |
| FWS Simulation Roadmap | L4 | 7-stage gated verification pipeline |
| MZM Certification Architecture | L5 | Strain-differential + NV relaxometry + Clifford certification |
| Thermodynamic Bootstrap | L5 | Sustainability argument, TAS dialectic, red/blue team protocol |

---

## Computation Map

| Script | Layer | Status | Key Result |
|--------|-------|--------|------------|
| ratchet_full.py | L3 | **PASS** | 1D: w=1, 2 MZMs, 99.7% edge, κ ratio 0.86 |
| penrose_bdg_2d.py | L3 | **FAIL** | 2D Stage 1: δt/t₀=59%, wrong lattice type |
| penrose_phonon_2d.py | L3 | **PARTIAL** | 2D Stage 2: κ=0.92, localization onset |
| run_all.py | L3 | Runner | Executes stages 1+2 |

---

## The Core Claim

**Singularities are type errors.**

At a topological phase boundary, the gap condition `IsGappedAt` becomes
undischargeable. The function computing the winding number is uncallable
at the type level. The phase transition is not a divergence — it is the
absence of a proof term.

This claim is:
- **Proved** in L1 (`gapless_blocks_inversion`, Clifford.lean §3)
- **Generalized** in L1 (`singularity_blocks_computation`, CLHoTT.lean §6)
- **Classified** in L2 (AZ tenfold way, AlgebraicLadder.lean)
- **Computed** in L3 (BdG diagonalization, ratchet_full.py)
- **Applied** in L4 (FWS device architecture)
- **Certified** in L5 (three-gate MZM certification protocol)

Each layer adds content. No layer repeats.

---

## The Ascending Ladder

The division algebra ladder ℝ → ℂ → ℍ → 𝕆 is reinterpreted as
ascending: each step trades a constraint for a capability.

| Step | Constraint Released | Capability Gained |
|------|-------------------|------------------|
| ℝ → ℂ | Ordering | Rotation (π₁(S¹)≅ℤ, phase, topology) |
| ℂ → ℍ | Commutativity | Spin (non-abelian structure, chirality) |
| ℍ → 𝕆 | Associativity | Gauge (exceptional Lie groups, E₈) |

The MZM at the 5/7 boundary is not a mode living at a breakdown. It is
the witness of emergence — the object that appears when the system
ascends to a rung where fermion parity becomes classifiable.

Formalized in `L2_Classification/AlgebraicLadder.lean` with `rfl` proofs.

---

## TAS Methodology

The project follows the Thesis–Antithesis–Synthesis dialectic:

- **Thesis:** Simulation produces a result (1D chain → MZMs)
- **Antithesis:** Type checker or 2D computation rejects (Stage 1 FAIL)
- **Synthesis:** Hidden assumption surfaced, corrected, re-run

The v1→v2→v3 thesis evolution is itself a TAS loop:
- v1: construction identified, gap unnamed
- v2: gap characterized as type error, time section removed
- v3: gap filled computationally (1D), PGTC discovered, Stage 1 antithesis

Each version is more honest than the last because the epistemic tags
force explicit accountability.

---

## Epistemic Discipline

Every claim in every document is tagged:

| Tag | Meaning | Example |
|-----|---------|---------|
| **PROVED** | Machine-checked, zero sorry | `left_edge_always_free` ∀N≥2 |
| **DEMONSTRATED** | Computationally verified | BdG: w=1, 2 MZMs in 1D |
| **CONJECTURED** | Falsifiable, formalization-ready | 5/7 → AI→D class transition |
| **SPECULATIVE** | Logically coherent, not yet testable | Experimental realization |

---

## Open Problems (Ordered by Priority)

1. **Corrected 2D lattice:** Graphene + Penrose-seeded SW defects (δt≈10%), re-run Stage 1
2. **AZ classification:** Formally show 5/7 boundary maps to AI→D (L2)
3. **Cubical Agda:** π₁(S¹)≅ℤ proved, winding number with computational content (L0)
4. **Float sorry:** Refactor CLHoTT.lean to ℤ/ℚ coefficients or move to Agda (L1)
5. **2D phonon glass:** Dynamical matrix on corrected lattice (L3)
6. **Thesis v4:** Incorporate ascending ladder, TAS framing, honest Stage 1 result (L3)

---

## Building

```bash
# Lean 4 (L1 + L2)
lake build

# Python computations (L3)
cd L3_Physics/Compute
python3 ratchet_full.py      # 1D BdG + phonon glass
python3 run_all.py           # 2D stages 1+2
```

Requires Lean 4 v4.12.0. Python requires NumPy and SciPy.

---

Geometry of State · GoS-Architect · github.com/GoS-Architect
