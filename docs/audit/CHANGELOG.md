# Changelog

## March 17, 2026 — Systems Architecture Reorganization

- Reorganized flat file structure into layered architecture (L0–L5)
- Created ARCHITECTURE.md with layer diagram, dependency rules, document map
- Added AlgebraicLadder.lean: ascending ladder, AZ tenfold, Bott periodicity (13 theorems, 0 sorry)
- Fixed EdgeModes.lean: Float.min, list_any_append, leftEdge_not_in_new_bond
- Added ratchet_full.py: 1D BdG + phonon glass computation (PASS: w=1, 2 MZMs)
- Created Agda/ directory with scope definition for Cubical Agda work
- Archived legacy files (01–05 series) to Archive/
- Updated lakefile for L1/L2 source directories

## March 14, 2026 — KitaevCertification + StationQ

- Added KitaevCertification.lean (35 theorems): phase boundary, bulk-boundary, ∀N
- Added StationQ.lean (33 theorems): inductive edge modes
- Universal edge theorems: left_edge_always_free, right_edge_always_free

## March 12, 2026 — TopologicalBridge + FWS

- Added TopologicalBridge.lean (9 theorems): pipeline, conservation laws
- Added FractonicWeylSemimetal.lean (22 theorems): curvature, AZ, PGTC
- Added CayleyDickson.lean (3 theorems): octonion non-associativity

## March 8, 2026 — GeometryOfState v2

- Cl(2,0) and Cl(3,0) with 12 theorems, zero sorry
- Gap condition as dependent type (IsGappedAt)
- gapless_blocks_inversion: the core thesis
- MHD / fusion connection via shared bivector structure

## January 2026 — Initial Development

- 01_LogicKernel through 05_GeometryOfState_verified3
- First proofs: i²=-1, singularity as type error, Univalence axiom usage
