# Geometry of State — Repository Organization (v3 Snapshot)

**Date:** March 25, 2026
**Total files in project:** 58 (.lean) + 1 (.agda) + 2 (.md) + 1 (.pdf)
**Purpose:** Classify every file before v4 reorganization

---

## v3 Canonical Set (15 Lean + 1 Agda + 2 build)

These are the active, authoritative files matching ARCHITECTURE_v3/v4.

### L0 — Foundations

| File | Thm | Ax | Sorry | Notes |
|------|-----|-----|-------|-------|
| logickernel.lean | 1 | 1 | 0 | Custom "Univalence" (actually winding injectivity). **v4 action: rename axiom.** |
| FirstFile.agda | — | — | — | Cubical Agda start. Horizon. |

### L1 — Algebra

| File | Thm | Ax | Sorry | Notes |
|------|-----|-----|-------|-------|
| Clifford.lean | 12 | 0 | 0 | Cl(2,0), Cl(3,0). Strongest L1 file. |
| CayleyDickson.lean | 3 | 0 | 0 | Octonion non-associativity. |
| Winding.lean | 0 | 0 | 0 | Definitions only (Cl(1,0)→Cl(2,0) ladder, winding computation). |
| CLHoTT.lean | 7 | 0 | 6 | **FROZEN.** All sorry are Float algebra. Path to close: ℤ/ℚ coefficients. |

### L2 — Classification

| File | Thm | Ax | Sorry | Notes |
|------|-----|-----|-------|-------|
| AlgebraicLadder.lean | 16 | 0 | 0 | AZ tenfold way, Bott periodicity. |
| KitaevCertification.lean | 35 | 0 | 0 | Full §12–§14. Phase boundary, BBC N=2..5, general ∀N≥2. |
| EdgeModes.lean | 33 | 0 | 0 | Station Q certification. BBC, edge localization. |
| Bridge.lean | 9 | 21 | 0 | HoTT axioms + Bridge Axioms A–G. Protection theorems. Best-documented file. |
| FWS.lean | 22 | 0 | 0 | FWS device classification. Penrose curvature, AZ symmetries. |

### Archive (thesis + special purpose)

| File | Thm | Ax | Sorry | Notes |
|------|-----|-----|-------|-------|
| SingularityAsTypeError.lean | 17 | 21 | 3 | **⚠ Contains retracted ConservationOfInformation + proved ladder ∅→𝟙→𝟚→ℕ→ℤ→S¹.** Larger project version (543 lines). **v4 action: archive with retraction header.** |
| TopologicalInvariant.lean | 1 | 15 | 1 | Real' scaffolding. `gapless_invariant_undefined`. |
| GeometryOfState_verified3.lean | 8 | 0 | 0 | Verification pillars. |
| TrivialPhaseCheck.lean | 2 | 0 | 0 | Quick check. |

### Build

| File | Role |
|------|------|
| lakefile.lean | Build configuration |
| Main.lean | Entry point |

### v3 Canonical Totals

| Metric | Count |
|--------|-------|
| **Theorems** | **166** |
| **Axiom declarations** | **58** |
| **Sorry** | **10** (6 Float in CLHoTT, 3 in SingularityAsTypeError, 1 in TopologicalInvariant) |
| **Lean files** | **14** |
| **Zero sorry in classification/topology** | **✓** |

**Note:** ARCHITECTURE_v3 reported 155 theorems / 7 sorry. The increase comes from the project version of SingularityAsTypeError.lean (17 theorems vs 1 in the earlier snapshot, 3 sorry vs 0). The canonical count depends on which version of that file is authoritative. If the smaller uploaded version is canonical: 150 theorems, 7 sorry. If the full project version: 166 theorems, 10 sorry.

---

## Byte-Identical Duplicates (archive — same content, different name)

These are confirmed identical by md5sum. Keep the canonical name, archive the duplicate.

| Keep (canonical) | Archive (identical) |
|-----------------|---------------------|
| Bridge.lean | TopologicalBridge_v2.lean |
| Clifford.lean | GeometryOfState_v2.lean |
| FWS.lean | FractonicWeylSemimetal.lean |
| GeometryOfState_verified3.lean | GeometryOfState_verified.lean |
| Winding.lean | CliffordFoundation.lean |
| GeometryOfState_The_Majorana_Zero_Mode.lean | KitaevBridge.lean |
| GoS_KitaevChain.lean | The_Type-Safety_Chain.lean |
| GeometryOfState_Pseudoscalar_Squares.lean | GoS_Spacetime.lean |

---

## Version History (archive — superseded by canonical files)

### GeometryOfState Monolith Family

The original monolith was refactored into Clifford.lean + KitaevCertification.lean + EdgeModes.lean + Bridge.lean + FWS.lean etc. All these are earlier versions:

| File | Size | Thm | Relationship |
|------|------|-----|-------------|
| GeometryOfState.lean | 40K | 6 | Original monolith v1 |
| GeometryOfState__1_.lean | 40K | 6 | Identical to above |
| GeometryOfState_v1.lean | 40K | 6 | Identical to above |
| GeometryOfState.lean copy | 39K | — | Near-identical copy |
| GeometryOfState__4_.lean | 42K | 6 | Slightly later version |
| GeometryOfState-v1.lean | 7K | 6 | Early small version |
| GeometryOfState_unified.lean | 7K | — | Identical to -v1 |
| GeometryOfState-v3.lean | 29K | 6 | Mid-evolution version |
| GeometryOfState-Stage-1-5.lean | 6K | 1 | Partial extract |

### TopologicalBridge Family

Evolved into Bridge.lean (canonical). All are earlier iterations:

| File | Thm | Notes |
|------|-----|-------|
| TopologicalBridge_v1.lean | 7 | Earlier version (v1) |
| TopologicalBridgeFixed.lean | 7 | Fix iteration |
| TopologicalBridgeComplete.lean | 9 | Near-final (same theorem count as Bridge.lean but different hash) |

### Kitaev/StationQ Overlaps

Same theorem content packaged differently during development:

| File | Thm | Overlap |
|------|-----|---------|
| Chain.lean | 35 | Same headers as KitaevCertification.lean, different hash |
| KitaevChain.lean | 1 | Smaller earlier version |
| StationQ.lean | 33 | Same theorem names as EdgeModes.lean |
| StationQ_Phase1_Phase2.lean | 26 | Earlier StationQ version |
| KitaevCertification.lean copy | 35 | Literal copy |
| PinnedPseudoKnot.lean copy | 2 | Literal copy |

---

## Unique Content Not Yet in Canonical Set

These files contain theorems not found in any canonical file. Decision needed: include in v4 canonical, or archive.

| File | Thm | Ax | Sorry | Content | Imports Mathlib? | Recommendation |
|------|-----|-----|-------|---------|-----------------|----------------|
| **RunGDescend.lean** | **13** | 0 | 0 | Algebraic ladder ℝ→ℂ→ℍ→𝕆, AZ, Bott. Zero sorry. | No | **Include in v4** — clean, unique, 0 sorry |
| **WindingNumber.lean** | **20** | 0 | **5** | Phase boundary, winding by region, BBC. | No | **Review** — 5 sorry need accounting |
| **TopologicalComputation.lean** | 5 | **30** | 0 | Knot-based read/write state machine. | Yes | Archive — heavy axiom count, Mathlib-dependent |
| **TopologicalLock3D.lean** | 3 | **14** | 0 | 3D knotted vortex protection. | Yes | Archive — Mathlib-dependent, content in Bridge.lean axioms |
| **MHDTopology.lean** | 1 | **20** | 0 | Superfluid-to-MHD correspondence. | Yes | Archive — Mathlib-dependent, content in Bridge.lean axioms |
| **PinnedPseudoKnot.lean** | 2 | **4** | 0 | 2D pinning as energetic protection. | Yes | Archive — Mathlib-dependent |
| **CliffordFoundation3D.lean** | 0 | 0 | 0 | Cl(3,0) extension, definitions only. | No | Archive — no theorems, defs covered in Clifford.lean |

---

## Small/Special Files

| File | Content | Recommendation |
|------|---------|----------------|
| AdrianDomingo_GeometryOfState_Logic.lean | Early Gemini-era logic. **Contains retracted ConservationOfInformation.** | Archive with retraction notice |
| GeometryOfState_KitaevBridge.lean | 1 theorem, identical to GeometryOfState_The_Majorana_Zero_Mode.lean | Archive |
| GeometryOfState_Logic_CL-HoTT.lean | 0 theorems, small logic fragment | Archive |
| KitaevChain_Digital_Triplet.lean | 1 theorem, small | Archive |
| GoS_KitaevChain.lean | 1 theorem, identical to The_Type-Safety_Chain.lean | Archive |
| TheGeometryOfState_Verifiable_Quantum_Theory.lean | 1 theorem | Archive |
| section14_fix_final.lean | Fix patch for §14 | Archive |
| section14_3_fix.lean | Fix patch | Archive |
| two_replacements_final.lean | Fix patch | Archive |
| nat_beq_fix.lean | Fix patch | Archive |

---

## Documentation Files

| File | Status |
|------|--------|
| ARCHITECTURE_v4.md | Current architecture (retraction propagated) |
| ARCHITECTURE_v3_to_v4_changes.md | Change log |
| ARCHITECTURE_v3.pdf | Previous architecture (pre-retraction) |

---

## Proposed v4 Directory Structure

```
GoS/
├── src/                          # Canonical Lean files
│   ├── L0_Foundations/
│   │   └── LogicKernel.lean      # renamed axiom
│   ├── L1_Algebra/
│   │   ├── Clifford.lean
│   │   ├── CayleyDickson.lean
│   │   ├── Winding.lean
│   │   └── CLHoTT.lean           # frozen
│   ├── L2_Classification/
│   │   ├── AlgebraicLadder.lean
│   │   ├── KitaevCertification.lean
│   │   ├── EdgeModes.lean
│   │   ├── Bridge.lean
│   │   ├── FWS.lean
│   │   └── RunGDescend.lean      # new in v4
│   └── Archive/
│       ├── SingularityAsTypeError.lean  # retraction header added
│       ├── TopologicalInvariant.lean
│       ├── GeometryOfState_verified3.lean
│       └── TrivialPhaseCheck.lean
├── archive/                      # Version history (preserved, not active)
│   ├── monolith/                 # GeometryOfState.lean evolution
│   ├── bridge_versions/          # TopologicalBridge iterations
│   ├── kitaev_versions/          # Chain/StationQ iterations
│   ├── mathlib_experiments/      # TopologicalComputation, Lock3D, MHD, etc.
│   ├── fix_patches/              # section14_fix, nat_beq_fix, etc.
│   └── duplicates/               # Byte-identical renamed files
├── agda/
│   └── FirstFile.agda
├── docs/
│   ├── ARCHITECTURE_v4.md
│   ├── ARCHITECTURE_v3_to_v4_changes.md
│   ├── AUDIT_v2.md
│   └── ARCHITECTURE_v3.pdf
├── lakefile.lean
└── Main.lean
```

---

*Organization prepared by Claude (Anthropic, Opus 4.6), March 25, 2026.*
