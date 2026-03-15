# The Geometry of State

A Lean 4 framework deriving topological invariants from Clifford algebra. Connects the Kitaev chain (condensed matter) to Taylor relaxation (fusion plasma confinement) through a shared Cl(3,0) bivector structure.

**Bulk-boundary correspondence proved for all chain lengths by structural induction. Phase boundaries formalized as type errors — the winding number requires `IsGapped`, which becomes undischargeable at the phase boundary.**

Two Lean files. Zero dependencies beyond Lean 4. 46+ machine-checked results. Zero `sorry` on finite structures.

```
lake build
```

## Contents

- `GeometryOfState.lean` — §1–§11. Clifford algebras Cl(2,0) and Cl(3,0), Kitaev Hamiltonian, winding numbers, Majorana edge modes, gap condition, MHD Taylor relaxation, stellarator/tokamak classification.
- `KitaevCertification.lean` — §12–§15. Parameterized phase boundary certification, inductive bulk-boundary correspondence (N=2–5, migration N=2–6), and **general ∀N ≥ 2 theorems** proved by structural induction. **34 results, 0 sorry, 0 axioms.**
- `TopologicalBridge.lean` — Axiom chain from HoTT (π₁(S¹) = ℤ) through the gap condition to topological protection. Extends to 3D knot protection and MHD helicity conservation.
- `Simulations/` — Python scripts providing numerical evidence for the physics inputs.

## The ∀N Theorems (§14)

The main results in `KitaevCertification.lean`:

```lean
theorem left_edge_always_free : ∀ (N : Nat), N ≥ 2 →
    isUnpaired leftEdge (topoChain N) = true

theorem right_edge_always_free : ∀ (N : Nat), N ≥ 2 →
    isUnpaired (rightEdge N) (topoChain N) = true
```

These are not case checks. The left-edge proof proceeds by showing A(1) cannot appear in any extension bond (cross-constructor elimination + `omega`), then inducting over chain length via `isUnpaired_append_single`. The right-edge proof uses a strengthened auxiliary (`rightEdge_not_in_chain_general`: B(m+2) ∉ topoChain(n+2) for all n ≤ m), instantiated at n = m.

## Proved Theorems

### KitaevCertification.lean — 34 results, 0 sorry, 0 axioms

**§12 — Phase boundary certification (7 theorems)**

| Theorem | Proof | What it says |
|---|---|---|
| `topo_is_gapped` | `native_decide` | Topological point (μ=0) has nonzero gap |
| `triv_is_gapped` | `native_decide` | Trivial point (μ=3) has nonzero gap |
| `bdry_is_boundary` | `native_decide` | Boundary point (μ=2) has zero gap |
| `near_bdry_still_gapped` | `native_decide` | Near-boundary (μ=1.99) remains gapped |
| `topo_classified` | `native_decide` | μ=0 classified as `.topological` |
| `triv_classified` | `native_decide` | μ=3 classified as `.trivial` |
| `bdry_classified` | `native_decide` | μ=2 classified as `.boundary` |

**§13 — Inductive bulk-boundary correspondence (23 theorems)**

Edge modes verified at N=2,3,4,5. Trivial chains verified to have no free edges. Migration predicate (`migrationHolds`) verified for N=2 through 6 — growing the chain by one site correctly migrates the right edge mode.

**§14 — General theorems (2 theorems + 3 lemmas, structural induction)**

| Theorem | Proof | What it says |
|---|---|---|
| `list_any_append` | structural induction | `List.any` distributes over `++` |
| `isUnpaired_append_single` | simp | Distributes over single-bond append |
| `leftEdge_not_in_new_bond` | constructor + omega | A(1) ∉ any extension bond |
| `left_edge_always_free` | structural induction | ∀ N ≥ 2, A(1) is free |
| `right_edge_always_free` | structural induction | ∀ N ≥ 2, B(N) is free |

### GeometryOfState.lean — 12 theorems

| Theorem | Proof | What it says |
|---|---|---|
| `gapless_blocks_inversion` | 3 lines | If the gap is closed, no proof of `IsGappedAt` exists, so the invariant cannot be computed |
| `left_edge_mode` | `rfl` | Majorana A(1) is free in the 3-site topological chain |
| `right_edge_mode` | `rfl` | Majorana B(3) is free in the 3-site topological chain |
| `bulk_is_coupled` | `rfl` | Majorana B(1) is coupled (not an edge mode) |
| `trivial_no_left_edge` | `rfl` | No left edge mode in the trivial phase |
| `trivial_no_right_edge` | `rfl` | No right edge mode in the trivial phase |
| `topological_ne_unprotected` | `decide` | Protection levels are distinct |
| `topological_ne_energetic` | `decide` | Protection levels are distinct |
| `energetic_ne_unprotected` | `decide` | Protection levels are distinct |
| `stellarator_is_topological` | `rfl` | Stellarator confinement maps to topological protection |
| `tokamak_is_unprotected` | `rfl` | Tokamak confinement maps to unprotected |
| `confinement_types_differ` | `decide` | The two confinement geometries produce different protection levels |

### TopologicalBridge.lean — 9 theorems

| Theorem | Status | Depends on |
|---|---|---|
| `singularity_blocks_construction` | Proved | Nothing (pure logic) |
| `singularity_excludes_point` | Proved | Nothing (pure logic) |
| `mzm_matches_topology` | Proved | Axiom D |
| `full_pipeline` | Proved | Axiom D |
| `full_pipeline_to_qubit` | Proved | Axiom D |
| `topological_protection` | Proved | Axiom E |
| `information_conservation` | Proved | Axioms D + E |
| `knot_topological_protection` | Proved | Axiom F |
| `helicity_topological_protection` | Proved | Axiom G |

## Axiom Accounting

`KitaevCertification.lean`: **0 axioms, 0 sorry, 34 machine-checked results.**

`GeometryOfState.lean`: 0 sorry on finite/decidable structures. 2 sorry marked ANALYSIS (require real-number arguments not yet formalized). Physics inputs stated in comments, not as Lean axioms.

`TopologicalBridge.lean`: 7 axioms (A–G), each in a different mathematical domain. Two theorems depend on no axioms at all.

## Scope and Limitations

The Clifford algebras are explicit Float structures (Cl(2,0) and Cl(3,0)), not Mathlib's abstract `CliffordAlgebra`. The winding number computation is numerical. Phase classification uses Float thresholds.

The ∀N bulk-boundary theorems (§14) are genuine structural inductions over bond graphs — these are proofs, not case checks. Connecting the Float-level Hamiltonian classification to Mathlib's real analysis and abstract algebra is an open direction.

## Derivation Chain

```
Cl(2,0) → bivector e₁₂ → e₁₂² = -1 (computed, not assumed)
        → rotors on S¹
        → Kitaev H(k) as Cl(2,0) vector
        → winding number W (computed: W=1 topological, W=0 trivial)
        → edge modes verified by rfl (§6) and ∀N induction (§14)

Cl(3,0) → 3D rotors (quaternions)
        → codim-2 singularities are curves → can knot
        → knot type is discrete invariant
        → magnetic bivector B ∈ Λ²
        → resistive decay exp(-ηk²t)
        → Taylor relaxation → Beltrami equilibrium
```

## Simulations

Numerical evidence for the physics inputs. Independent of the Lean proofs.

- `stellarator_taylor_relaxation.py` — 48³ grid, ABC Beltrami fields. Perturbed ABC at η=0.005: energy decays 4.4× faster than helicity. Pure Beltrami control: ratio = 1.0×. Lower resistivity (η=0.001): 17.3× ratio.
- `gp3d_solver.py` — 3D Gross-Pitaevskii solver. Biot-Savart trefoil initialization, imaginary-time relaxation, real-time evolution.
- `gp3d_readwrite.py` — Read/write topological cycle: relax, read, splice, verify.

All seven simulation runs confirmed the Lean predictions: every failure corresponded to a violated precondition, every success to a satisfied one.

## Building

Requires [Lean 4](https://leanprover.github.io/lean4/doc/setup.html). No Mathlib dependency.

```bash
git clone https://github.com/GoS-Architect/topological-invariants-dependent-types.git
cd topological-invariants-dependent-types
lake build
```

## License

MIT

## Author

Adrian Domingo