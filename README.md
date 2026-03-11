# The Geometry of State

A formally verified framework deriving topological invariants from Clifford algebra, connecting condensed matter physics to fusion plasma confinement.

**One file. Zero dependencies. Seven theorems verified by the Lean 4 kernel.**

```
lake build
```

## What This Proves

The file `GeometryOfState.lean` builds a chain from the Clifford algebra Cl(n,0) to Majorana zero-mode edge states, with every step either computed by the type checker or proved without `sorry`.

### Derivation Chain

```
Cl(2,0)  →  bivector e₁₂  →  e₁₂² = -1 (derived, not assumed)
         →  rotors R = cos(θ/2) + sin(θ/2)·e₁₂
         →  Kitaev Hamiltonian H(k) as Cl(2,0) vector
         →  winding number W ∈ ℤ (computed: W=1 topological, W=0 trivial)
         →  W=1 ⟹ edge modes at A(1), B(3) (rfl proof)
         →  W=0 ⟹ no edge modes (rfl proof)

Cl(3,0)  →  3D rotors on S³  →  sandwich product RvR† (no rotation matrices)
         →  magnetic bivector B ∈ Λ²
         →  resistive decay exp(-ηk²t) → energy decays faster than helicity
         →  Taylor relaxation → Beltrami equilibrium
         →  stellarator (3D) = topological protection
         →  tokamak (2D symmetry) = unprotected
```

### Verified Theorems

| Theorem | Statement | Proof |
|---|---|---|
| `gapless_blocks_inversion` | If the spectral gap is closed, the topological invariant cannot be computed | 3-line proof, no sorry |
| `left_edge_mode` | Majorana A(1) is a zero-energy mode in the 3-site topological Kitaev chain | `rfl` |
| `right_edge_mode` | Majorana B(3) is a zero-energy mode in the 3-site topological Kitaev chain | `rfl` |
| `bulk_is_coupled` | Majorana B(1) is NOT a zero-energy mode (it's coupled to the bulk) | `rfl` |
| `trivial_no_left_edge` | No left edge mode in the trivial phase | `rfl` |
| `trivial_no_right_edge` | No right edge mode in the trivial phase | `rfl` |

The `rfl` proofs mean the Lean 4 kernel evaluates the function and confirms the result. No axioms, no trust — the compiler is the verifier.

### Computed Verifications (via `#eval`)

- `e₁₂² = -1` in Cl(2,0) — the "imaginary unit" is a consequence of the algebra
- `e₁₂² = -1`, `e₁₂₃² = -1`, associativity in Cl(3,0)
- Winding number: W = 1 (topological), W = 0 (trivial), W = -1 (negative pairing)
- 3D rotation via sandwich product matches expected results
- Selective dissipation: low-k modes persist while high-k modes decay

## Architecture

```
§1   Cl(2,0) algebra — geometric product, bivector emerges
§2   Rotors — even subalgebra, composition, angle extraction
§3   Gap condition — bivector inversion requires proof of |B|² ≠ 0
§4   Kitaev Hamiltonian — Cl(2,0) vector field over Brillouin zone
§5   Winding number — integer derived from rotor phase accumulation
§6   Majorana edge modes — bulk-boundary correspondence, rfl proofs
§7   Cl(3,0) — full 8D algebra, 64-term product, verified identities
§8   3D rotors — quaternionic structure, sandwich product
§9   Protection hierarchy — unprotected / energetic / topological
§10  MHD fusion — magnetic bivector, Taylor relaxation, stellarator vs tokamak
```

## Axiom Accounting

**Zero inconsistent axioms.** The `ConservationOfInformation` axiom from earlier versions (which was provably false — `Empty = Empty` by `rfl`) has been removed.

**Zero `sorry`.** Every theorem is fully proved.

**Physics input** (stated in comments, not as Lean axioms):
- Gross-Pitaevskii evolution preserves density > 0 below reconnection energy
- Resistive MHD gives spectral decay exp(-ηk²t)
- Beltrami field is minimum-energy state at fixed helicity (Taylor 1974)

These are empirical facts about PDEs. They belong to the simulation layer, not the proof layer.

## The Key Insight

The spectral gap in the Kitaev chain is not just a number — it is a **proof obligation**. The function `safeBivectorInv` requires a witness `_hGap : IsGappedAt h1 h2` to be called. At the topological phase transition, this witness does not exist. The invariant becomes **uncomputable** — not because of a runtime error, but because the proof term is absent.

The singularity is a type error. This is proven in `gapless_blocks_inversion`.

## Building

Requires [Lean 4](https://leanprover.github.io/lean4/doc/setup.html) (v4.12.0 or compatible).

```bash
git clone https://github.com/GoS-Architect/GeometryOfState.git
cd GeometryOfState
lake build
```

All proofs compile. The `#eval` blocks print verification results.

To run as an executable:

```bash
lake exe geometry_of_state
```

## Related Simulations

The `simulations/` directory contains Python scripts that numerically validate the framework's predictions:

- `stellarator_taylor_relaxation.py` — Demonstrates selective dissipation (energy decays ~2.5× faster than helicity) on ABC Beltrami fields
- `gp3d_solver.py` — 3D Gross-Pitaevskii solver with Biot-Savart trefoil initialization
- `gp3d_readwrite.py` — Complete read/write cycle: relax → read → splice → verify

These simulations are independent of the Lean proofs. The Lean file proves the logical structure; the simulations provide numerical evidence.

## Author

Adrian Domingo

## License

MIT
