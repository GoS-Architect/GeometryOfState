# The Geometry of State

A Lean 4 framework deriving topological invariants from Clifford algebra. Connects the Kitaev chain (condensed matter) to Taylor relaxation (fusion plasma confinement) through a shared Cl(3,0) bivector structure.

Two files. Zero dependencies beyond Lean 4. Twelve proved theorems. Zero `sorry`.

```
lake build
```

## Contents

- `GeometryOfState.lean` — Clifford algebras Cl(2,0) and Cl(3,0), Kitaev Hamiltonian, winding numbers, Majorana edge modes, MHD Taylor relaxation, stellarator/tokamak classification. All proofs by `rfl` or `decide`.
- `TopologicalBridge.lean` — Axiom chain from HoTT (pi_1(S^1) = Z) through the gap condition to topological protection and information conservation. Extends to 3D knot protection and MHD helicity conservation. All proved theorems in term mode, no tactic imports.
- `Simulations/` — Python scripts providing numerical evidence for the physics inputs.

## Proved Theorems

### GeometryOfState.lean

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

### TopologicalBridge.lean

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

The TopologicalBridge has 7 axioms (A-G), each in a different mathematical domain. The dependency graph and closure strategy are documented in the file. Two theorems (`singularity_blocks_construction`, `singularity_excludes_point`) depend on no axioms at all.

GeometryOfState has zero axioms and zero `sorry`. Physics inputs (PDE behavior, simulation results) are stated in comments, not as Lean axioms.

## Derivation Chain

```
Cl(2,0) -> bivector e12 -> e12^2 = -1 (computed, not assumed)
        -> rotors on S^1
        -> Kitaev H(k) as Cl(2,0) vector
        -> winding number W (computed: W=1 topological, W=0 trivial)
        -> edge modes verified by rfl

Cl(3,0) -> 3D rotors (quaternions)
        -> codim-2 singularities are curves -> can knot
        -> knot type is discrete invariant
        -> magnetic bivector B in Lambda^2
        -> resistive decay exp(-eta k^2 t)
        -> Taylor relaxation -> Beltrami equilibrium
```

## Simulations

Numerical evidence for the physics inputs. These are independent of the Lean proofs.

- `stellarator_taylor_relaxation.py` — 48^3 grid, ABC Beltrami fields. Perturbed ABC at eta=0.005: energy decays 4.4x faster than helicity. Pure Beltrami control: ratio = 1.0x. Lower resistivity (eta=0.001): 17.3x ratio.
- `gp3d_solver.py` — 3D Gross-Pitaevskii solver. Biot-Savart trefoil initialization, imaginary-time relaxation, real-time evolution.
- `gp3d_readwrite.py` — Read/write topological cycle: relax, read, splice, verify.

## Building

Requires [Lean 4](https://leanprover.github.io/lean4/doc/setup.html).

```bash
git clone https://github.com/GoS-Architect/GeometryOfState.git
cd GeometryOfState
lake build
```

## License

MIT

## Author

Adrian Domingo
