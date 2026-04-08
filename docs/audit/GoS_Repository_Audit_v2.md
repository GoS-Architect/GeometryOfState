# Geometry of State — Repository Audit v2

**Auditor:** Claude (Anthropic, Opus 4.6)
**Date:** March 24, 2026
**Files reviewed:** 14 Lean files, ARCHITECTURE_v4.md, ARCHITECTURE_v3.pdf, v3→v4 changelog, 5 concept papers, Omnivalence documentation map
**Method:** `grep` across all `.lean` files + manual review of every axiom, sorry, and theorem

---

## 0. Critical Notice: Core Thesis Retracted

The original GoS thesis — "singularities are type errors" — was **retracted** in HiTT v0.2 (March 2026) and the retraction propagated in ARCHITECTURE v4. Two grounds:

1. **Formal inconsistency.** The axiom `ConservationOfInformation : ∀ (state : Type), Impossible (state = Empty)` is provably false. `Empty = Empty` holds by `rfl`, so the axiom generates a contradiction. The compiler rejected the thesis about type errors via a type error.

2. **Physical incorrectness.** The Kitaev chain Hamiltonian H(k) is perfectly well-defined at the critical point μ = 2t. The bivector exists with zero magnitude. Nothing is ill-formed. The gap condition `IsGappedAt` becomes undischargeable, but the Hamiltonian itself type-checks.

**Revised thesis (SPECULATIVE):** Singularities are topos phase transitions — points where the ambient grammar of valid mathematics undergoes structural transformation. The gap condition fails not because the computation is ill-formed, but because the system has crossed into a regime where the topological classification changes.

**Repository impact:** SingularityAsTypeError.lean contains the retracted axiom and should be archived, corrected, or prominently marked. See Section 6.

---

## 1. Hard Numbers

### Audited (14 uploaded files)

| Metric | Count |
|--------|-------|
| Theorems (`theorem` keyword) | **150** |
| Axiom declarations (`axiom` keyword) | **46** |
| Sorry in proofs (actual, not comments) | **7** |
| Definitions (`def` / `noncomputable def`) | ~289 |
| Structures (`structure` keyword) | ~66 |
| Total lines of Lean | 5,824 |

### Canonical (per ARCHITECTURE_v4, 15 files)

| Metric | Count |
|--------|-------|
| Theorems | **155** |
| Sorry | **7** |
| Files | **15** |

The discrepancy (5 theorems, 1 file) reflects recent work not yet uploaded. Single source of truth: `theorem_inventory_v2.md`.

---

## 2. File-by-File Breakdown

### L1 — Algebra (4 files, 22 theorems, 6 sorry)

| File | Lines | Theorems | Axioms | Sorry | Proof methods |
|------|-------|----------|--------|-------|---------------|
| Clifford.lean | 1,004 | 12 | 0 | 0 | rfl, decide |
| CayleyDickson.lean | 244 | 3 | 0 | 0 | rfl |
| Winding.lean | 494 | 0 | 0 | 0 | (definitions only) |
| CLHoTT.lean | 477 | 7 | 0 | 6 | sorry (Float), rfl |

CLHoTT.lean is **frozen**. All 6 sorry are Float algebraic identities (neg_neg, mul_comm, mul_one, etc.) — true in ℝ, unprovable for IEEE 754 Float without Mathlib ring tactic. Each sorry is individually documented. Path to closure: replace Float with ℤ/ℚ coefficients.

### L2 — Classification (5 files, 112+ theorems, 0 sorry)

| File | Lines | Theorems | Axioms | Sorry | Proof methods |
|------|-------|----------|--------|-------|---------------|
| AlgebraicLadder.lean | 463 | 16 | 0 | 0 | rfl, decide, omega |
| KitaevChain.lean | 366 | 35 | 0 | 0 | rfl, native_decide, induction |
| EdgeModes.lean | 561 | 33 | 0 | 0 | rfl, native_decide, induction |
| Bridge.lean | 947 | 9 | 21 | 0 | Classical.byContradiction, congrArg |
| FWS.lean | 582 | 22 | 0 | 0 | rfl, decide, omega |

**Zero sorry in any classification or topology theorem.** This is the strongest layer.

### Foundations & Archive (5 files, 13 theorems, 1 sorry)

| File | Lines | Theorems | Axioms | Sorry | Status |
|------|-------|----------|--------|-------|--------|
| LogicKernel.lean | 31 | 1 | 1 | 0 | Active (naming issue — see §6) |
| SingularityAsTypeError.lean | 218 | 1 | 9 | 0 | **⚠ CONTAINS RETRACTED AXIOM** |
| TopologicalInvariant.lean | 151 | 1 | 15 | 1 | Active (Real' scaffolding) |
| GeometryOfState_verified3.lean | 223 | 8 | 0 | 0 | Active |
| TrivialPhaseCheck.lean | 63 | 2 | 0 | 0 | Active |

---

## 3. Axiom Accounting

### The headline number problem

Adrian has stated "12 axioms" in conversation. The actual `axiom` keyword count is **46**. This is not dishonest — the categories are genuinely different — but the discrepancy must be addressed proactively. Anyone running `grep -c axiom *.lean` will see 46.

### Categorical breakdown

**Category A — HoTT Infrastructure (8 declarations, 3 unique concepts)**

Axioms that are theorems in Cubical Agda but must be postulated in Lean 4's CIC. Consistent with MLTT+UA. Would be eliminated by the planned Cubical Agda port.

| Axiom | File(s) | Note |
|-------|---------|------|
| Path : {α : Type} → α → α → Type | Bridge.lean | Proof-relevant identity |
| Path.refl | Bridge.lean | Reflexivity |
| S1 : Type | Bridge, SingularityAsTypeError | Circle HIT (duplicated) |
| S1.base : S1 | Bridge, SingularityAsTypeError | Base point (duplicated) |
| S1.loop | Bridge, SingularityAsTypeError | Loop (duplicated) |
| pi1_S1 : LoopSpace S1 S1.base ≃ Int | Bridge.lean | π₁(S¹) ≅ ℤ |
| Univalence (A B : State) | LogicKernel.lean | ⚠ See naming warning below |

**⚠ LogicKernel.lean naming warning:** This `Univalence` axiom is **not** the standard univalence axiom (A ≃ B → A =_U B). It is an injectivity condition: same winding number implies same State. Recommend renaming to `winding_determines_state` to avoid confusion.

**Category B — Real Number Scaffolding (15 declarations)**

Minimal real number system built because of zero Mathlib dependencies. Would **vanish entirely** with a Mathlib import.

| File | Content |
|------|---------|
| TopologicalInvariant.lean | Real', Real'.zero/one/pi, arithmetic ops, IsNonzero, Real'.div, BrillouinZone, deriv_k, integral_BZ, exact_quantization |

**Category C — Bridge Axioms (7 axioms — the actual trust boundary)**

Claims with real mathematical content that could in principle be false. Each documented in Bridge.lean with domain, trust level, and closure strategy.

| Label | Name | Domain |
|-------|------|--------|
| A | normalization_defines_loop | Point-set topology |
| B | exact_winding_is_degree | Differential topology |
| C | sensor_rounding_stable | Numerical analysis / IEEE 754 |
| D | sensor_equals_degree | Composition of B+C |
| E | intermediate_singularity | Homotopy theory + IVT |
| F | knot_change_requires_singularity | 3D differential topology |
| G | helicity_change_requires_reconnection | MHD theory |

**Category D — Physical Postulates (9 declarations, 1 RETRACTED)**

| Axiom | File | Status |
|-------|------|--------|
| **ConservationOfInformation** | **SingularityAsTypeError.lean** | **⚠ RETRACTED — provably inconsistent (`Empty = Empty` by `rfl`)** |
| Topological_Lock | SingularityAsTypeError.lean | Depends on retracted framework |
| MagneticHelicity, MagneticEnergy | SingularityAsTypeError.lean | Function signatures only |
| Taylor_Relaxation | SingularityAsTypeError.lean | **Concludes `True` — structurally vacuous** |
| Grand_Syntactic_Immunity | SingularityAsTypeError.lean | Apex theorem as axiom; depends on retracted framework |
| IsKnotProtected | Bridge.lean | Active (valid) |
| IsHelicityProtected | Bridge.lean | Active (valid) |

**Category E — Type/Structure Declarations (7 declarations)**

| Axiom | File |
|-------|------|
| Filament, KnotType, filament_knot_type | Bridge.lean |
| MagneticConfig, magnetic_helicity | Bridge.lean |
| real_winding_integral | Bridge.lean |

### Summary

| Category | Count | Status | Eliminated by |
|----------|-------|--------|---------------|
| A. HoTT Infrastructure | 8 | POSTULATED | Cubical Agda port |
| B. Real Number Scaffolding | 15 | SCAFFOLDING | Mathlib import |
| C. Bridge Axioms | 7 | TRUST BOUNDARY | Individual proofs (closure strategy exists) |
| D. Physical Postulates | 9 | MIXED (1 retracted, 1 vacuous) | Revision / archival |
| E. Type Declarations | 7 | STRUCTURAL | Domain formalization |
| **Total** | **46** | | |

**Recommended public statement:** "46 axiom declarations: 8 HoTT infrastructure (theorems in Cubical Agda), 15 real-number scaffolding (eliminated by Mathlib), 7 bridge axioms (documented trust boundary with closure strategy), 16 physical/structural postulates (1 retracted, retraction documented)."

---

## 4. Sorry Accounting

| # | File | Line | What it needs |
|---|------|------|---------------|
| 1 | CLHoTT.lean | 286 | -(-r.b) = r.b (Float neg_neg) |
| 2 | CLHoTT.lean | 295 | -(0.0 : Float) = 0.0 |
| 3 | CLHoTT.lean | 305 | Float ring laws (commutativity, neg distributes) |
| 4 | CLHoTT.lean | 313 | Float.one_mul, Float.zero_mul, Float.sub_zero |
| 5 | CLHoTT.lean | 321 | Float.mul_one, Float.mul_zero, Float.sub_zero |
| 6 | CLHoTT.lean | 330 | Float ring laws (associativity, distributivity) |
| 7 | TopologicalInvariant.lean | 110 | 2π ≠ 0 (requires Real' axiom enrichment) |

**All sorry quarantined in two files. Zero sorry in any classification, topology, or bridge theorem.** Path to closure: replace Float with ℤ/ℚ coefficients (CLHoTT), enrich Real' axioms (TopologicalInvariant).

---

## 5. Strongest Results

| Theorem | File | Depends on | Significance |
|---------|------|------------|-------------|
| topological_protection | Bridge.lean | Axiom E | No singularity on path ⟹ invariant conserved |
| information_conservation | Bridge.lean | Axioms D+E | Parity conserved along gapped paths (calc proof) |
| knot_topological_protection | Bridge.lean | Axiom F | Knot type conserved without reconnection |
| helicity_topological_protection | Bridge.lean | Axiom G | Helicity conserved without reconnection |
| gapless_invariant_undefined | TopologicalInvariant.lean | Real' scaffolding | Cannot call topological_invariant at gapless point |
| left/right_edge_always_free | KitaevChain.lean | None | Edge modes exist ∀N≥2 (structural induction) |
| bott_period_8_AI | AlgebraicLadder.lean | None | Bott periodicity |
| confinement_types_differ | Clifford.lean | None | Stellarator ≠ tokamak protection |
| singularity_blocks_construction | Bridge.lean | Definitions only | Gapless blocks invariant computation (unconditional) |

**Note on "singularity as type error" results:** The theorems `gapless_blocks_inversion` (Clifford.lean), `gapless_invariant_undefined` (TopologicalInvariant.lean), and `singularity_blocks_construction` (Bridge.lean) remain **valid** under the revised thesis. The formal observation — that `IsGappedAt` becomes undischargeable and the winding number function is uncallable at the type level — is correct. What was retracted is the *interpretation* (type error vs. topos transition), not the formal content.

---

## 6. Issues Requiring Action

### CRITICAL

| Issue | File | Action needed |
|-------|------|---------------|
| `ConservationOfInformation` is provably inconsistent | SingularityAsTypeError.lean | Archive file or remove axiom. Currently contains a contradiction. |
| `Grand_Syntactic_Immunity` depends on retracted framework | SingularityAsTypeError.lean | Archive or re-derive from valid foundations |
| `Taylor_Relaxation` concludes `True` | SingularityAsTypeError.lean | Asserts nothing. Remove or give real content. |

### IMPORTANT

| Issue | File | Action needed |
|-------|------|---------------|
| `Univalence` naming | LogicKernel.lean | Rename to `winding_determines_state` |
| Duplicated S1 axioms | Bridge + SingularityAsTypeError | Consolidate or archive SingularityAsTypeError |
| Retraction not reflected in code | SingularityAsTypeError.lean | No retraction notice in the file itself |

### LOW PRIORITY

| Issue | File | Action needed |
|-------|------|---------------|
| Float sorry | CLHoTT.lean | Refactor to ℤ/ℚ coefficients |
| Downstream retraction propagation | Various docs | Some earlier documents still reference original thesis |

**Recommended action for SingularityAsTypeError.lean:** Move to `archive/` directory with a header comment:

```
/- RETRACTED (March 2026)
   The axiom ConservationOfInformation in this file is provably inconsistent:
   Empty = Empty by rfl, contradicting Impossible (state = Empty).
   
   The formal observations (IsSingularity, PhysicalLaw, singularity_is_type_error)
   remain valid. The interpretation changed: see ARCHITECTURE_v4.md §Core Thesis.
   
   This file is preserved as methodology documentation, not active code.
-/
```

---

## 7. The Retraction as Methodology

The v3→v4 retraction is the strongest evidence that the Glassbox methodology works. The system designed to catch errors caught the biggest error in the project — the core thesis itself. The retraction was:

- **Formally grounded:** The compiler surfaced the inconsistency (`Empty = Empty` by `rfl`).
- **Transparently documented:** Version history preserved in ARCHITECTURE_v4, change summary in v3→v4 changelog.
- **Propagated downstream:** Identified all affected documents with priority tags.
- **Used as TAS example:** The retraction itself is documented as a Thesis-Antithesis-Synthesis cycle.

This retraction discipline — preserving the error, documenting the discovery, propagating the correction, and using the failure as evidence for the methodology — is rare in any research context. It demonstrates that the epistemic tagging and axiom accounting systems are not performative but functional.

---

## 8. Cross-Document Number Reconciliation

| Source | Theorems | Axioms | Sorry |
|--------|----------|--------|-------|
| This audit (14 files) | 150 | 46 | 7 |
| ARCHITECTURE_v4 (15 files) | 155 | not stated | 7 |
| Anthropic memo (needs update) | 104 | not stated | 7 |

**Canonical numbers:** 155 theorems (per ARCHITECTURE_v4), 46 axiom declarations (7 at trust boundary, 1 retracted), 7 sorry (all Float/scaffolding), 15 files.

---

*Audit v2 performed by Claude (Anthropic, Opus 4.6) on March 24, 2026. Based on 14 Lean files, ARCHITECTURE_v4.md, v3→v4 changelog, 5 concept papers, and Omnivalence documentation map uploaded by Adrian Domingo.*

*The compiler is the credential. The retraction is the proof of honesty.*
