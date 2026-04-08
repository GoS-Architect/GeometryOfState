# Cubical Agda — Homotopy Type Theory Layer

## Scope

This directory will contain Cubical Agda formalizations for the homotopy-theoretic
content that Lean 4 currently axiomatizes. The goal is to **prove** rather than
**postulate** the topological foundations.

## Targets

| Result | Lean 4 Status | Agda Goal |
|--------|--------------|-----------|
| π₁(S¹) ≅ ℤ | Axiom | **Proved** via universal cover |
| Univalence | Axiom | **Built-in** (Cubical) |
| Winding number | Axiom (`exact_quantization`) | **Computed** as function S¹ → ℤ |
| Loop space structure | Postulated | **Constructed** as HIT |
| Degree of map S¹ → S¹ | Assumed integer | **Proved** integer-valued |

## Why Two Proof Assistants

**Lean 4** handles everything algebraic and decidable:
- Clifford algebra multiplication tables (`rfl`)
- Finite chain edge modes (`native_decide`)
- AZ classification (`decide`)
- Bott periodicity (`rfl`)

**Cubical Agda** handles everything homotopy-theoretic:
- Winding number quantization (requires universal cover)
- Topological invariance under continuous deformation
- Path-based identity (Univalence with computational content)

The bridge between them is the type signatures. Both express:
`IsGapped H → ℤ`

Lean proves the algebraic content. Agda proves the topological content.
The numerical layer (Python) provides the physical bridge for both.

## Dependencies

- [Agda](https://github.com/agda/agda) with `--cubical` flag
- [cubical](https://github.com/agda/cubical) library

## Status

Not yet started. This README defines the scope.
