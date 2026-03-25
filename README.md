# Geometry of State

**A formally verified framework for topological quantum materials.**

160 unique theorems. Zero Mathlib dependencies. Zero sorry in any classification or topology theorem.

Built through transparent human-AI collaboration (Gemini + Claude) in three months, starting from zero formal verification experience. The compiler is the credential.

---

## What This Is

Geometry of State (GoS) connects formal verification (Lean 4) through algebraic structures and topological classification to physical predictions and device design. The core observation: at a topological phase transition, the gap condition `IsGappedAt` becomes undischargeable as a proof obligation. The winding number function is uncallable at the type level — not because the computation crashes, but because the system has crossed into a regime where the topological classification changes.

The framework is organized into layers. Each layer imports from the layer below. No layer skips a level.

```
L5  VERIFICATION     How do we know it's real?
L4  DEVICE           What do we build?
L3  PHYSICS          What does the math predict?
L2  CLASSIFICATION   Which topological phase?
L1  ALGEBRA          What are the structures?
L0  FOUNDATIONS      What can we prove?
```

---

## Hard Numbers

| Metric | Count |
|--------|-------|
| Unique theorems (deduplicated across all files) | **160** |
| Canonical Lean files | 15 |
| Axiom declarations | 58 (see breakdown below) |
| Sorry | 10 (6 Float algebra, 3 retracted file, 1 scaffolding) |
| Sorry in classification or topology | **0** |
| Python simulation scripts | 15 |
| Lines of Lean | ~13,000 |
| Lines of Python | ~8,100 |
| Mathlib dependencies | **0** |

### Axiom Breakdown

Not all 58 axioms are equal. They fall into five categories:

| Category | Count | Status |
|----------|-------|--------|
| HoTT infrastructure (theorems in Cubical Agda, postulated in Lean 4) | 8 | Eliminated by Agda port |
| Real number scaffolding (building ℝ without Mathlib) | 15 | Eliminated by Mathlib import |
| Bridge axioms (the actual trust boundary, each documented) | 7 | Closure strategy exists |
| Physical/structural postulates | 21 | Mixed (1 retracted) |
| Type declarations | 7 | Structural |

The 7 bridge axioms are documented in `Bridge.lean` with domain, trust level, and closure strategy for each.

---

## Retraction Notice

The original core thesis — "singularities are type errors" — was **retracted** in March 2026 after the Lean kernel surfaced a formal inconsistency. The foundational axiom `ConservationOfInformation` stated that no state type could equal `Empty`, but `Empty = Empty` holds by `rfl`. The compiler rejected the thesis about type errors via a type error.

The retraction is documented in `ARCHITECTURE_v4.md` and `ARCHITECTURE_v3_to_v4_changes.md`. The revised thesis (singularities as topos phase transitions) is explicitly tagged **SPECULATIVE**. The retracted file `SingularityAsTypeError.lean` is preserved in `src/Archive/` as methodology documentation.

This retraction is the strongest evidence that the project's epistemic methodology works. The system designed to catch errors caught the biggest error in the project — its own foundational axiom — and the process handled it cleanly.

---

## Canonical Files

### L0 — Foundations

| File | Theorems | Notes |
|------|----------|-------|
| `LogicKernel.lean` | 1 | Winding-number identity axiom |

### L1 — Algebra

| File | Theorems | Sorry | Notes |
|------|----------|-------|-------|
| `Clifford.lean` | 12 | 0 | Cl(2,0), Cl(3,0), geometric product, gap condition |
| `CayleyDickson.lean` | 3 | 0 | Octonion non-associativity |
| `Winding.lean` | 0 | 0 | Cl(1,0)→Cl(2,0) ladder, winding computation (definitions) |
| `CLHoTT.lean` | 7 | 6 | Frozen. All sorry are Float algebra (neg_neg, mul_comm, etc.) |

### L2 — Classification

| File | Theorems | Sorry | Notes |
|------|----------|-------|-------|
| `AlgebraicLadder.lean` | 16 | 0 | AZ tenfold way, Bott periodicity |
| `KitaevCertification.lean` | 35 | 0 | Phase boundary, BBC N=2..5, general ∀N≥2 |
| `EdgeModes.lean` | 33 | 0 | Station Q certification, edge localization |
| `Bridge.lean` | 9 | 0 | HoTT axioms, Bridge Axioms A–G, protection theorems |
| `FWS.lean` | 22 | 0 | FWS device classification, Penrose curvature, AZ symmetries |
| `RunGDescend.lean` | 13 | 0 | Algebraic ladder ℝ→ℂ→ℍ→𝕆, Bott periodicity |

### Archive

| File | Theorems | Notes |
|------|----------|-------|
| `SingularityAsTypeError.lean` | 17 | ⚠ Contains retracted axiom. Preserved as methodology. |
| `TopologicalInvariant.lean` | 1 | Real' scaffolding. `gapless_invariant_undefined`. |
| `GeometryOfState_verified3.lean` | 8 | Verification pillars |
| `TrivialPhaseCheck.lean` | 2 | Quick check proofs |

---

## Simulation Campaign (L3)

Seven computational steps, each gated with pass/fail criteria.

| Step | Script | Result | Key Finding |
|------|--------|--------|-------------|
| Lattice | `graphene_sw_lattice.py` | **PASS** | Corrected honeycomb + Penrose SW, CN={2,3,4}, δt≈9.7% |
| PGTC | `run_all.py` | **PASS** | κ=0.30 (70% phonon suppression), 12 localized modes |
| Baseline | `step1_clean_baseline.py` | **PASS** | BDI trivial in d=2 confirmed. Exchange required. |
| Exchange | `step3_spinful_bdg.py` | **PASS** | Gap closes h_ex≈0.6. BDI→D transition confirmed. |
| Fine scan | `step3b_finescan.py` | **PASS** | Bott index B=+1 (h_ex=0), B=-1 (h_ex=1.1) |
| 3D bilayer | `step4_bilayer_3d.py` | PARTIAL | First 3D attempt |
| Matched | `step4b_matched_bilayer.py` | PARTIAL | Defect localization 80-92% |

Additional simulations: 3D Gross-Pitaevskii vortex dynamics (`helium_loom_*.py`, `gp3d_*.py`), Taylor relaxation (`stellarator_taylor_relaxation.py`).

Failure history preserved: v1 lattice used Penrose vertices directly (CN={3..10}, δt=59%, 0 MZMs, all gates FAIL). Diagnosis and correction documented.

---

## Epistemic Tags

Every claim in this project carries an explicit status:

| Tag | Meaning | Criterion |
|-----|---------|-----------|
| **PROVED** | Lean kernel verified | `lake build` succeeds, zero sorry in proof |
| **DEMONSTRATED** | Quantified computation | Python simulation with reproducible results |
| **CONJECTURED** | Reasoned, kill condition defined | Falsifiable claim with explicit failure criteria |
| **SPECULATIVE** | Exploratory | Direction, not commitment |
| **RETRACTED** | Withdrawn with documented reason | Formal inconsistency or physical incorrectness |

---

## Methodology

**Glassbox:** Every reasoning step is auditable. Epistemic tags on all claims. Axiom accounting on all proofs. Attribution transparency (which AI contributed what).

**TAS Protocol:** Thesis → Antithesis → Synthesis. Every significant claim survives structured adversarial examination. The antithesis can come from a different AI system, a compiler, or a simulation. The core thesis retraction is the protocol's most significant test case — the thesis survived months of discursive review but not compilation.

**Kill Conditions:** Defined before results, not after. If a conjectured claim fails its kill condition, it is retracted, not revised.

---

## Building

```bash
# Lean 4 (L1 + L2)
lake build

# Python simulations (L3)
python3 run_all.py                  # PGTC main pipeline
python3 step1_clean_baseline.py     # BDI baseline
python3 step3_spinful_bdg.py        # Ni-62 exchange BdG
python3 step3b_finescan.py          # Parameter scan + Bott indices
python3 step4b_matched_bilayer.py   # 3D matched bilayer
```

Requires Lean 4 v4.12.0. Python requires NumPy and SciPy.

---

## Author

Adrian Domingo · GoS-Architect · Chicago
Visual systems architect, 20 years across regulated industries. Self-taught formal verification researcher. Neurodivergent. AI as cognitive partner has been genuinely transformative — not as a crutch, but as an externalizer of reasoning.

Built with Claude (Anthropic) and Gemini (Google).

---

*The compiler is the credential. The retraction is the proof of honesty.*
