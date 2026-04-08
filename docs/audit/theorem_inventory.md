# THE GEOMETRY OF STATE — THEOREM INVENTORY
## Reorganized March 2026

---

## Summary

| Category | Files | Theorems | Sorry | Axioms |
|----------|-------|----------|-------|--------|
| GoS/Algebra | 3 | 15 | 0 | 0 |
| GoS/Kitaev | 3 | 77 | 0 | 21 |
| GoS/Classification | 2 | 35 | 0 | 0 |
| GoS/Category | 1 | 7 | 6 | 0 |
| **Active total** | **9** | **134** | **6** | **21** |
| Archive | 5 | 13 | 1 | 25 |
| **Grand total** | **14** | **147** | **7** | **46** |

All 7 sorry are Float arithmetic (6 in CLHoTT.lean, 1 in TopologicalInvariant.lean).
Zero sorry in any finite verification theorem.

---

## GoS/Algebra/Clifford.lean (was: GeometryOfState.lean)
### 12 theorems, 0 sorry, 0 axioms — 1004 lines

| # | Theorem | Proof | What it proves |
|---|---------|-------|----------------|
| 1 | `gapless_blocks_inversion` | intro+exact | **THE CORE THESIS.** Gapless → no proof term exists. |
| 2 | `left_edge_mode` | rfl | A(1) is free in 3-site topological chain. |
| 3 | `right_edge_mode` | rfl | B(3) is free in 3-site topological chain. |
| 4 | `bulk_is_coupled` | rfl | Bulk mode B(1) is NOT free. |
| 5 | `trivial_no_left_edge` | rfl | Trivial phase: no left edge mode. |
| 6 | `trivial_no_right_edge` | rfl | Trivial phase: no right edge mode. |
| 7 | `topological_ne_unprotected` | decide | Protection levels distinct (1/3). |
| 8 | `topological_ne_energetic` | decide | Protection levels distinct (2/3). |
| 9 | `energetic_ne_unprotected` | decide | Protection levels distinct (3/3). |
| 10 | `stellarator_is_topological` | rfl | Stellarator = topologically protected. |
| 11 | `tokamak_is_unprotected` | rfl | Tokamak = unprotected. |
| 12 | `confinement_types_differ` | decide | Stellarator ≠ tokamak in protection class. |

---

## GoS/Algebra/CayleyDickson.lean (unchanged)
### 3 theorems, 0 sorry, 0 axioms — 244 lines

| # | Theorem | Proof | What it proves |
|---|---------|-------|----------------|
| 13 | `octonion_non_associative` | decide | (e₁e₂)e₄ ≠ e₁(e₂e₄). |
| 14 | `associator_nonzero` | decide | [e₁,e₂,e₄] ≠ 0. |
| 15 | `non_associativity_inevitable` | contradiction | ¬ ∀ xyz, associator = 0. |

---

## GoS/Algebra/Winding.lean (was: CliffordWindingNumber.lean)
### 0 theorems — 494 lines

Definitions only: Cl(1,0), Cl(2,0) structures, rotor operations, winding number computation. No theorems, no sorry. Infrastructure for Clifford.lean and Chain.lean.

---

## GoS/Kitaev/Chain.lean (was: KitaevCertification.lean)
### 35 theorems, 0 sorry, 0 axioms — 366 lines

### Phase Boundary (7)

| # | Theorem | Proof | What it proves |
|---|---------|-------|----------------|
| 16 | `topo_is_gapped` | native_decide | μ=0: gap open everywhere. |
| 17 | `triv_is_gapped` | native_decide | μ=3: gap open (trivial phase). |
| 18 | `bdry_is_boundary` | native_decide | μ=2: gap closes. Phase boundary. |
| 19 | `near_bdry_still_gapped` | native_decide | μ=1.99: still gapped. |
| 20 | `topo_classified` | native_decide | μ=0 → topological. |
| 21 | `triv_classified` | native_decide | μ=3 → trivial. |
| 22 | `bdry_classified` | native_decide | μ=2 → boundary. |

### Bulk-Boundary Correspondence (23)

| # | Theorem | Proof | What it proves |
|---|---------|-------|----------------|
| 23–34 | `bbc_N2_*` through `bbc_N5_*` | native_decide | Edge modes at N=2,3,4,5. |
| 35–38 | `trivial_N3_*`, `trivial_N5_*` | native_decide | No edge modes in trivial phase. |
| 39–42 | `migration_2_to_3` through `migration_5_to_6` | native_decide | Edge migrates as chain grows. |
| 43–46 | `edges_N2` through `edges_N5` | native_decide | Combined edge check per N. |

### Infrastructure (5)

| # | Theorem | Proof | What it proves |
|---|---------|-------|----------------|
| 47 | `nat_beq_false_of_ne` | omega | BEq reflects ≠ on Nat. |
| 48 | `list_any_append` | simp | List.any distributes over ++. |
| 49 | `isUnpaired_append_single` | simp | isUnpaired distributes over append. |
| 50 | **`left_edge_always_free`** | omega+induction | **∀ N ≥ 2: A(1) is free.** |
| 51 | **`right_edge_always_free`** | omega+induction | **∀ N ≥ 2: B(N) is free.** |

---

## GoS/Kitaev/EdgeModes.lean (was: StationQ.lean)
### 33 theorems, 0 sorry, 0 axioms — 554 lines

Archived but valid. Contains the inductive bulk-boundary correspondence with full verification up to N=50. Overlaps with Chain.lean §13–§14 but uses a different implementation strategy.

---

## GoS/Kitaev/Bridge.lean (was: TopologicalBridge.lean)
### 9 theorems, 0 sorry, 21 bridge axioms — 947 lines

| # | Theorem | Proof | What it proves |
|---|---------|-------|----------------|
| 52 | `mzm_matches_topology` | congrArg | Sensor verdict = topological classification. |
| 53 | `singularity_blocks_construction` | intro+exact | Gapless → no invariant computable. |
| 54 | `singularity_excludes_point` | exact | IsSingularity IS ¬IsGapped. |
| 55 | `full_pipeline` | exact axiom | Hardware integer = topological invariant. |
| 56 | `full_pipeline_to_qubit` | congrArg | Pipeline through to ℤ₂ parity. |
| 57 | `topological_protection` | byContradiction | Invariant conserved along gapped paths. |
| 58 | `information_conservation` | calc chain | MZM parity conserved. |
| 59 | `knot_topological_protection` | byContradiction | 3D knot type conserved. |
| 60 | `helicity_topological_protection` | byContradiction | MHD helicity conserved. |

---

## GoS/Classification/AlgebraicLadder.lean (was: RunGDescend.lean)
### 13 theorems, 0 sorry, 0 axioms — ~460 lines

**NEW — built March 2026. Contains ascending ladder reframe.**

| # | Theorem | Proof | What it proves |
|---|---------|-------|----------------|
| 61 | `ascent_releases_one` | cases+decide | Each rung releases exactly one constraint. |
| 62 | `rotation_requires_ordering` | rfl | ℝ→ℂ: ordering traded for rotation. |
| 63 | `spin_requires_commutativity` | rfl | ℂ→ℍ: commutativity traded for spin. |
| 64 | `gauge_requires_associativity` | rfl | ℍ→𝕆: associativity traded for gauge. |
| 65 | `kitaev_is_Z2` | rfl | Class D in d=1 → ℤ/2 invariant. |
| 66 | `kitaev_has_PH` | rfl | Kitaev chain has particle-hole symmetry. |
| 67 | `kitaev_no_TR` | rfl | Kitaev chain: no time-reversal. |
| 68 | `winding_zero_trivial` | rfl | w=0 → even fermion parity. |
| 69 | `winding_one_topological` | rfl | w=1 → odd fermion parity. |
| 70 | `kitaev_edge_is_topological` | decide | Trivial-to-D wall supports boundary mode. |
| 71 | `bdi_d_changes` | decide | BDI→D changes invariant type. |
| 72 | `bott_period_8_AI` | rfl | Real AZ classes have period 8. |
| 73 | `if_conjecture_then_MZM` | decide | IF 5/7→AI→D, THEN wall is topological. |

---

## GoS/Classification/FWS.lean (was: FractonicWeylSemimetal.lean)
### 22 theorems, 0 sorry, 0 axioms — 582 lines

| # | Theorem | Proof | What it proves |
|---|---------|-------|----------------|
| 74 | `pentagon_positive_curvature` | rfl | Pentagon → positive Gaussian curvature. |
| 75 | `heptagon_negative_curvature` | rfl | Heptagon → negative Gaussian curvature. |
| 76 | `pentagon_deficit_positive` | rfl | Pentagon angular deficit > 0. |
| 77 | `heptagon_deficit_negative` | rfl | Heptagon angular deficit < 0. |
| 78 | `stone_wales_pair_zero_net_deficit` | rfl | SW pair: net curvature = 0. |
| 79 | `deficit_equals_excess` | rfl | Balanced defect pattern: Σ deficit = 0. |
| 80 | `class_D_symmetries` | rfl | Class D: PH yes, TR no, chiral no. |
| 81 | `class_AI_symmetries` | rfl | Class AI: TR yes (T²=+1). |
| 82 | `kitaev_chain_Z2` | rfl | Class D d=1 → ℤ/2. |
| 83 | `class_D_2d_Z` | rfl | Class D d=2 → ℤ. |
| 84 | `class_AI_1d_trivial` | rfl | Class AI d=1 → trivial. |
| 85 | `bott_periodicity_class_D` | rfl | Bott period 8 for class D. |
| 86 | `class_D_clock_position` | rfl | D at position 2 on Bott clock. |
| 87 | `class_AI_clock_position` | rfl | AI at position 0. |
| 88 | `AI_to_D_clifford_steps` | rfl | AI→D = 2 Clifford steps. |
| 89 | `sw_conserves_vertices` | rfl | SW defect conserves atom count. |
| 90 | `sw_net_curvature_zero` | rfl | SW defect: zero net curvature. |
| 91 | `phonon_scaling_steeper` | decide | k∝d⁻⁴ steeper than t∝d⁻². |
| 92 | `pgtc_amplification_factor` | rfl | Phonon modulation = 2× electron. |
| 93 | `fws_device_has_Z_invariant` | rfl | Full FWS stack → ℤ invariant in 2D. |
| 94 | `boundary_hosts_topology` | decide | Conditional: boundary → MZM. |
| 95 | `penrose_2d_invariant` | decide | Conditional: 2D patch → invariant. |

---

## GoS/Category/CLHoTT.lean (unchanged)
### 7 theorems, 6 sorry, 0 axioms — 477 lines

**FROZEN** — blocked on Float ring lemmas. Fix path: ℤ/ℚ coefficients or Cubical Agda.

| # | Theorem | Proof | What it proves |
|---|---------|-------|----------------|
| 96 | `rev_involution` | sorry (Float) | Dagger is involution. |
| 97 | `rev_identity` | sorry (Float) | Identity is self-adjoint. |
| 98 | `rev_compose` | sorry (Float) | Dagger reverses composition. |
| 99 | `identity_compose` | sorry (Float) | Left identity. |
| 100 | `compose_identity` | sorry (Float) | Right identity. |
| 101 | `compose_assoc` | sorry (Float) | Associativity. |
| 102 | `singularity_blocks_computation` | intro+exact | **PROVED.** General categorical singularity. |

---

## Archive/ — 5 files, 13 theorems, 1 sorry, 25 axioms

Legacy files from January–February 2026. Superseded by active core. Preserved for history.

| File | Theorems | Notes |
|------|----------|-------|
| LogicKernel.lean | 1 | First theorem (Safe_Harbor_Exists) |
| TrivialPhaseCheck.lean | 2 | verify_pillar_one, verify_pillar_two |
| SingularityAsTypeError.lean | 1 | singularity_is_type_error |
| TopologicalInvariant.lean | 1 | gapless_invariant_undefined (1 sorry: 2π≠0) |
| GeometryOfState_verified3.lean | 8 | Early Pillars I–VIII exploration |

---

## Compute/ — Numerical Layer

| File | Status | Key Result |
|------|--------|------------|
| ratchet_full.py | **PASS** | 1D: w=1, 2 MZMs, 99.7% edge, κ ratio 0.86 |
| penrose_bdg_2d.py | **FAIL** | 2D Stage 1: δt/t₀=59%, wrong lattice |
| penrose_phonon_2d.py | **PARTIAL** | 2D Stage 2: κ=0.92, localization onset |
| run_all.py | Runner | Executes stages 1+2 |

---

## Proof Technique Distribution

| Technique | Count | Used in |
|-----------|-------|---------|
| rfl | ~50 | Algebra, Classification, FWS |
| native_decide | ~35 | Chain, EdgeModes |
| decide | ~15 | Algebra, Classification, AlgebraicLadder |
| intro+exact | ~5 | Core singularity theorems |
| omega+induction | 2 | Universal edge theorems |
| byContradiction | 3 | Protection theorems (Bridge) |
| sorry (Float) | 7 | CLHoTT only |
