# Geometry of State — Repository Audit

**Auditor:** Claude (Anthropic, Opus 4.6)
**Date:** March 24, 2026
**Files reviewed:** 14 Lean files, ARCHITECTURE.md, ARCHITECTURE_v3.pdf, 5 concept papers
**Method:** `grep` across all `.lean` files + manual review of every axiom, sorry, and theorem

---

## 1. Hard Numbers (14 uploaded files)

| Metric | Count |
|--------|-------|
| Theorems (`theorem` keyword) | **150** |
| Axiom declarations (`axiom` keyword) | **46** |
| Sorry in proofs (actual, not comments) | **7** |
| Definitions (`def` / `noncomputable def`) | ~289 |
| Structures (`structure` keyword) | ~66 |
| Total lines of Lean | 5,824 |

**Note:** ARCHITECTURE_v3.pdf reports 155 theorems across 15 files. This audit covers 14 uploaded files containing 150 theorems. The discrepancy (5 theorems, 1 file) likely reflects recent work not yet uploaded.

---

## 2. File-by-File Breakdown

### L1 — Algebra (4 files, 22 theorems, 6 sorry)

| File | Lines | Theorems | Axioms | Sorry | Proof methods |
|------|-------|----------|--------|-------|---------------|
| Clifford.lean | 1,004 | 12 | 0 | 0 | rfl, decide |
| CayleyDickson.lean | 244 | 3 | 0 | 0 | rfl |
| Winding.lean | 494 | 0 | 0 | 0 | (definitions only) |
| CLHoTT.lean | 477 | 7 | 0 | 6 | sorry (Float), rfl |

CLHoTT.lean is **frozen**. All 6 sorry are Float algebraic identities (neg_neg, mul_comm, mul_one, etc.) — true in ℝ, unprovable for IEEE 754 Float without Mathlib ring tactic. Each sorry is individually documented with the specific lemma it needs. Path to closure: replace Float with ℤ/ℚ coefficients.

### L2 — Classification (5 files, 112+ theorems, 0 sorry)

| File | Lines | Theorems | Axioms | Sorry | Proof methods |
|------|-------|----------|--------|-------|---------------|
| AlgebraicLadder.lean | 463 | 16 | 0 | 0 | rfl, decide, omega |
| KitaevChain.lean | 366 | 35 | 0 | 0 | rfl, native_decide, induction |
| EdgeModes.lean | 561 | 33 | 0 | 0 | rfl, native_decide, induction |
| Bridge.lean | 947 | 9 | 21 | 0 | Classical.byContradiction, congrArg |
| FWS.lean | 582 | 22 | 0 | 0 | rfl, decide, omega |

**Zero sorry in any classification or topology theorem.** This is the strongest layer.

### Foundations & Special Files (5 files, 13 theorems, 1 sorry)

| File | Lines | Theorems | Axioms | Sorry | Role |
|------|-------|----------|--------|-------|------|
| LogicKernel.lean | 31 | 1 | 1 | 0 | Univalence axiom + Safe_Harbor_Exists |
| SingularityAsTypeError.lean | 218 | 1 | 9 | 0 | Core thesis (singularity_is_type_error) |
| TopologicalInvariant.lean | 151 | 1 | 15 | 1 | Winding number via dependent types |
| GeometryOfState_verified3.lean | 223 | 8 | 0 | 0 | Verification pillars |
| TrivialPhaseCheck.lean | 63 | 2 | 0 | 0 | Quick check proofs |

---

## 3. Axiom Accounting (CRITICAL)

### The headline number problem

Adrian has stated "12 axioms" in conversation. The actual `axiom` keyword count is **46**. This is not dishonest — the categories are genuinely different — but the discrepancy must be addressed proactively. Anyone running `grep -c axiom *.lean` will see 46.

### Categorical breakdown

**Category A — HoTT Infrastructure (8 declarations, 3 unique concepts)**

Axioms that are theorems in Cubical Agda but must be postulated in Lean 4's CIC. Well-understood, consistent with MLTT+UA. Would be eliminated by the planned Cubical Agda port.

| Axiom | File(s) | Note |
|-------|---------|------|
| Path : {α : Type} → α → α → Type | Bridge.lean | Proof-relevant identity |
| Path.refl | Bridge.lean | Reflexivity |
| S1 : Type | Bridge.lean, SingularityAsTypeError.lean | Circle HIT (duplicated) |
| S1.base : S1 | Bridge.lean, SingularityAsTypeError.lean | Base point (duplicated) |
| S1.loop | Bridge.lean, SingularityAsTypeError.lean | Loop path (duplicated) |
| pi1_S1 : LoopSpace S1 S1.base ≃ Int | Bridge.lean | π₁(S¹) ≅ ℤ |
| Univalence (A B : State) | LogicKernel.lean | Custom: same winding → same state |

**Warning:** LogicKernel.lean's `Univalence` is **not** the standard univalence axiom (A ≃ B → A =_U B). It's an injectivity condition: same winding number implies same State. The name may invite confusion. Recommend renaming to `winding_determines_state` or similar.

**Category B — Real Number Scaffolding (15 declarations)**

Building a minimal real number system because of zero Mathlib dependencies. These would **vanish entirely** with a Mathlib import of `Mathlib.Analysis.SpecificLimits.Basic` or similar.

| Axioms | File | Content |
|--------|------|---------|
| Real', Real'.zero, Real'.one, Real'.pi | TopologicalInvariant.lean | Real number type + constants |
| Real'.add, .sub, .mul, .neg, .div | TopologicalInvariant.lean | Arithmetic operations |
| IsNonzero, IsNonzero.one | TopologicalInvariant.lean | Nonzero predicate |
| BrillouinZone, deriv_k, integral_BZ | TopologicalInvariant.lean | Domain + calculus |
| exact_quantization | TopologicalInvariant.lean | Gap → integer (the bridge) |

**Category C — Bridge Axioms (7 axioms, the actual trust boundary)**

These are the claims with real mathematical content that could in principle be false. Each is documented in Bridge.lean with its domain, trust level, and closure strategy.

| Label | Name | Domain | What it claims |
|-------|------|--------|----------------|
| A | normalization_defines_loop | Point-set topology | Gapped Hamiltonian defines a loop on S¹ |
| B | exact_winding_is_degree | Differential topology | Real-valued winding integral = topological degree |
| C | sensor_rounding_stable | Numerical analysis | Float Riemann sum within 0.5 of true integral |
| D | sensor_equals_degree | Composition | Discrete sensor output = topological degree |
| E | intermediate_singularity | Homotopy + IVT | Different invariants ⟹ singularity on any path between |
| F | knot_change_requires_singularity | 3D differential topology | Knot type change requires reconnection |
| G | helicity_change_requires_reconnection | MHD theory | Helicity change requires magnetic reconnection |

**Category D — Physical Postulates (9 declarations)**

Physics claims stated as axioms. Mixed epistemic status.

| Axiom | File | Status |
|-------|------|--------|
| ConservationOfInformation | SingularityAsTypeError.lean | Foundational claim (no state equals Empty) |
| Topological_Lock | SingularityAsTypeError.lean | Gap prevents volume collapse |
| MagneticHelicity, MagneticEnergy | SingularityAsTypeError.lean | Functions on AlbertAlgebra (signatures only) |
| Taylor_Relaxation | SingularityAsTypeError.lean | **Concludes `True` — structurally vacuous** |
| Grand_Syntactic_Immunity | SingularityAsTypeError.lean | **Apex theorem stated as axiom, not proved** |
| IsKnotProtected | Bridge.lean | Protection law for filaments |
| IsHelicityProtected | Bridge.lean | Protection law for magnetic configurations |

**Category E — Type/Structure Declarations (7 declarations)**

Types postulated rather than constructed. Standard practice for axiomatized domains.

| Axiom | File |
|-------|------|
| Filament : Type | Bridge.lean |
| KnotType : Type | Bridge.lean |
| filament_knot_type : Filament → KnotType | Bridge.lean |
| MagneticConfig : Type | Bridge.lean |
| magnetic_helicity : MagneticConfig → Float | Bridge.lean |
| real_winding_integral | Bridge.lean |

### Summary table

| Category | Count | Would be eliminated by | Epistemic status |
|----------|-------|------------------------|------------------|
| A. HoTT Infrastructure | 8 | Cubical Agda port | POSTULATED (theorems elsewhere) |
| B. Real Number Scaffolding | 15 | Mathlib import | SCAFFOLDING |
| C. Bridge Axioms | 7 | Individual proofs (closure strategy exists) | TRUST BOUNDARY |
| D. Physical Postulates | 9 | Physics arguments / simulation evidence | MIXED |
| E. Type Declarations | 7 | Domain formalization | STRUCTURAL |
| **Total** | **46** | | |

**Recommended public statement:** "46 axiom declarations: 8 HoTT infrastructure (theorems in Cubical Agda), 15 real-number scaffolding (eliminated by Mathlib), 7 bridge axioms (documented trust boundary with closure strategy), 16 physical/structural postulates."

---

## 4. Sorry Accounting

| # | File | Line | What it needs | Category |
|---|------|------|---------------|----------|
| 1 | CLHoTT.lean | 286 | -(-r.b) = r.b (Float neg_neg) | Float algebra |
| 2 | CLHoTT.lean | 295 | -(0.0 : Float) = 0.0 | Float/IEEE 754 |
| 3 | CLHoTT.lean | 305 | Float ring laws (commutativity, neg distributes) | Float algebra |
| 4 | CLHoTT.lean | 313 | Float.one_mul, Float.zero_mul, Float.sub_zero | Float algebra |
| 5 | CLHoTT.lean | 321 | Float.mul_one, Float.mul_zero, Float.sub_zero | Float algebra |
| 6 | CLHoTT.lean | 330 | Float ring laws (associativity, distributivity) | Float algebra |
| 7 | TopologicalInvariant.lean | 110 | 2π ≠ 0 (requires Real' axiom enrichment) | Real scaffolding |

**All sorry are quarantined in two files. Zero sorry in any classification, topology, or bridge theorem.** Path to closure: replace Float with ℤ/ℚ coefficients (CLHoTT), enrich Real' axioms (TopologicalInvariant).

---

## 5. Strongest Results

These theorems carry the most weight. All are zero-sorry and depend only on definitions + documented axioms.

| Theorem | File | Depends on | What it proves |
|---------|------|------------|----------------|
| singularity_blocks_construction | Bridge.lean | Definitions only | Gapless parameter blocks invariant computation |
| singularity_excludes_point | Bridge.lean | Definitions only | IsSingularity = ¬IsGapped (tautological but clean) |
| topological_protection | Bridge.lean | Axiom E | No singularity on path ⟹ invariant conserved |
| information_conservation | Bridge.lean | Axioms D + E | Parity conserved along gapped paths (calc proof) |
| knot_topological_protection | Bridge.lean | Axiom F | Knot type conserved without reconnection |
| helicity_topological_protection | Bridge.lean | Axiom G | Helicity conserved without reconnection |
| gapless_invariant_undefined | TopologicalInvariant.lean | Real' scaffolding | Cannot call topological_invariant at gapless point |
| left_edge_always_free / right_edge_always_free | KitaevChain.lean | None | Edge modes exist ∀N≥2 (structural induction) |
| bott_period_8_AI | AlgebraicLadder.lean | None | Bott periodicity for class AI |
| confinement_types_differ | Clifford.lean | None | Stellarator ≠ tokamak topological protection |

---

## 6. Known Weaknesses

| Issue | File | Impact |
|-------|------|--------|
| `Univalence` naming | LogicKernel.lean | Name suggests standard UA; actual content is winding-number injectivity |
| `Taylor_Relaxation` concludes `True` | SingularityAsTypeError.lean | Axiom asserts nothing; structurally vacuous |
| `Grand_Syntactic_Immunity` is axiom, not theorem | SingularityAsTypeError.lean | The "apex theorem" is assumed, not derived |
| `singularity_is_type_error` is `Iff.rfl` | SingularityAsTypeError.lean | Definitionally true; content is in definitions, not proof |
| Duplicated S1 axioms | Bridge.lean + SingularityAsTypeError.lean | Same axioms declared twice in different files |
| Float-based proofs | CLHoTT.lean, some defs elsewhere | Runtime demonstrations, not formal type-level verification |

---

## 7. Cross-Document Number Reconciliation

| Document | Theorems | Axioms | Sorry | Files |
|----------|----------|--------|-------|-------|
| This audit (14 files) | 150 | 46 | 7 | 14 |
| ARCHITECTURE_v3.pdf | 155 | not stated | 7 | 15 |
| TBC Concept Paper | 147 | not stated | 7 | — |
| PGTC Concept Paper | 112 (classification only) | — | 0 (classification) | — |
| TBC Claude Review | 144 | — | — | — |
| Anthropic Memo (current) | 104 | — | 7 | 11 |
| Adrian verbal (this session) | ~146 | ~12 | ~6 | — |

**Recommended canonical numbers (based on this audit):** 150 theorems, 46 axiom declarations (7 at trust boundary), 7 sorry (all Float/scaffolding), 14 files, 5,824 lines. Update all documents to match, with the axiom categorical breakdown.

---

## 8. Recommendations

1. **Push the unpushed files.** ARCHITECTURE_v3 references 155 theorems across 15 files. Get the repo to match the architecture document.

2. **Rename LogicKernel.lean's `Univalence`.** Call it `winding_determines_state` or `topological_identity`. The current name invites a fight you don't want.

3. **Fix or remove `Taylor_Relaxation`.** An axiom that concludes `True` is worse than not having it. Either give it real content or delete it.

4. **Consolidate S1 axioms.** S1, S1.base, S1.loop appear in both Bridge.lean and SingularityAsTypeError.lean. Create a shared foundations file or acknowledge the duplication.

5. **Reframe `Grand_Syntactic_Immunity`.** Currently an axiom claiming the apex theorem. Either prove it from existing components or explicitly tag it CONJECTURED and explain what would be needed to prove it.

6. **Update the Anthropic memo.** Current version says 104 theorems. Actual count is 150. Update to reflect current state.

7. **Add this audit to the repository.** As AUDIT.md or similar. Bridge.lean already has an excellent self-audit section. The rest of the repo should match that standard.

---

*Audit performed by Claude (Anthropic, Opus 4.6) on March 24, 2026. Based on 14 Lean files uploaded by Adrian Domingo, plus 9 supporting documents.*
