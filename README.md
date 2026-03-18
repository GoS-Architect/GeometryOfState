# Geometry of State

A Lean 4 framework deriving topological invariants from Clifford algebra.

**147 theorems · 7 sorry (all Float) · Zero Mathlib dependencies**

Connects the Kitaev chain (topological superconductivity) to Taylor
relaxation (fusion plasma confinement) through a shared Cl(2,0)/Cl(3,0)
bivector structure. Extends to the Altland-Zirnbauer tenfold classification,
Phonon Glass Topological Crystal self-protection, and a Fractonic Weyl
Semimetal device architecture.

## Architecture

See [ARCHITECTURE.md](ARCHITECTURE.md) for the full layered systems design.

```
L5  Verification    ← MZM certification, red/blue team, TAS
L4  Device          ← FWS engineering spec, simulation roadmap
L3  Physics         ← thesis, BdG computation, phonon glass
L2  Classification  ← AZ tenfold, Bott, edge modes, ascending ladder
L1  Algebra         ← Cl(2,0), Cl(3,0), octonions, gap condition
L0  Foundations     ← Lean 4 kernel, Cubical Agda (planned)
```

## Core Claim

Singularities are type errors. At a phase boundary, `IsGappedAt` fails,
the winding number is untypeable, and the topological invariant cannot be
constructed. The phase transition is the absence of a proof term.

## Building

```bash
lake build
```

Requires [Lean 4](https://leanprover.github.io/lean4/doc/setup.html) v4.12.0.

## Author

Adrian Domingo · [github.com/GoS-Architect](https://github.com/GoS-Architect)

MIT License
