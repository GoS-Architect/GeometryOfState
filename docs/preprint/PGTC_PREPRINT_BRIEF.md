# PGTC PREPRINT BRIEF

**For: New Claude conversation**
**From: Adrian Domingo (GoS-Architect)**
**Date: March 20, 2026**

---

## What I need

Help drafting an arXiv preprint on the Phonon Glass Topological Crystal (PGTC) result from the Geometry of State project. This is my highest-priority deliverable — I need a citable artifact in the scientific record.

---

## Who I am

Self-taught formal verification researcher, background in visual systems design (20+ years). No physics or CS degree. Built the Geometry of State framework using Claude and Gemini as thought partners, Lean 4 as the proof assistant. Started my first Lean theorem January 19, 2026. Currently have 144 unique zero-dependency theorems, 7 sorry (none in classification layer). Unemployed with severance runway ending ~June 2026.

---

## The PGTC result

**Origin:** The phonon glass / topological crystal concept and the quasiperiodic ratchet mechanism were developed in collaboration with Gemini (Google) in February 2026, as part of a broader "Digital Triplet" architecture. The key insight from that work: 5-7-7-5 Stone-Wales defects in a Penrose nanoribbon act as geometric rotors that violently scatter thermal phonons (collapsing phonon mean free path) while the interior electronic topology remains protected — an "electron crystal / phonon glass." The PGTC preprint extracts and validates this specific mechanism through simulation.

**Core claim:** A quasiperiodic lattice geometry (honeycomb graphene with Penrose-selected Stone-Wales defects) simultaneously supports a topological electronic phase and suppresses phonon transport. The same geometry does both jobs because electron hopping scales as d⁻² (Harrison) while phonon spring constants scale as d⁻⁴ (Keating) — the same geometric modulation hits phonons 2× harder than electrons.

**Key numbers (2D simulation, corrected lattice, N=800):**
- κ_QP / κ_ordered = 0.30 (70% phonon suppression)
- 12 localized phonon modes in quasiperiodic lattice vs 0 in ordered
- Spectral gap ratio: 58.8×
- All gate conditions PASS

**Key numbers (1D ratchet, N=100):**
- Winding number w = -1 (|w|=1, topological)
- 2 Majorana zero modes, 99.7% edge-localized
- κ ratio = 0.86 in 1D (weaker effect, as expected)
- Phase boundary at μ ≈ 2.0

**Critical failure history (must be included):**
- v1 lattice FAILED: used Penrose vertices directly instead of graphene + Penrose-seeded SW defects. Modulation was 59% (unphysical). Zero MZMs, Bott index = 0.
- Diagnosis: wrong lattice type, not wrong physics.
- Corrected lattice: honeycomb with face-traced Stone-Wales defects, ~12% modulation (physical).
- v2 passes all gates.

---

## Simulation scripts and results

- `ratchet_full.py` → `ratchet_full_results.json` (1D topology + phonon)
- `run_all.py` v2 → `stage2_summary.json` v2 (2D PGTC, the main result)
- `graphene_sw_lattice.py` (corrected lattice generator)
- `step1_clean_baseline.py` → BDI trivial in d=2 confirmed
- Failed results preserved: `stage1_summary.json`, `combined_report.json`

---

## Formal verification connection

The PGTC mechanism is formalized in `FWS.lean`:
- `phonon_scaling_steeper` — proves d⁻⁴ < d⁻² (phonons feel geometric modulation more)
- `pgtc_amplification_factor` — proves phonon modulation = 2× electron modulation
- `deficit_equals_excess` — net curvature deficit = excess pentagons (by list induction)
- `bott_periodicity_class_D` — classification repeats with period 8

The AZ classification (BDI trivial in 2D, D has ℤ after exchange) is formalized in `AlgebraicLadder.lean` and `FWS.lean`.

---

## What the preprint should be

- **Focused on the PGTC physics result**, not the full GoS architecture
- **Target audience:** condensed matter physicists working on topological materials, phonon engineering, or thermoelectrics
- **Honest about what's computed vs proved vs conjectured**
- **Includes the failure history** as methodology (TAS dialectic)
- **References the Lean formalization** but doesn't require readers to understand it
- **Citable and searchable** on arXiv (cond-mat.mes-hall or cond-mat.mtrl-sci)

---

## Methodological origin

The PGTC result didn't emerge from a traditional research program. It came out of a trajectory that started with hard sci-fi world-building ("Quantum Fiction") and progressively formalized into real material science.

**The sequence:**

1. **Quantum Fiction** — Adrian was building a physics engine for a sci-fi game/novel. Wanted the physics to be accurate, not handwaved. Coined the genre "Quantum Fiction."

2. **Digital Triplet** — Developed with Gemini. Extended the Digital Twin concept (physical + digital) with a third logical verification layer. The triplet structure: something claims to be true → something independently checks it → the discrepancy produces new knowledge. This is the same pattern as Constitutional AI.

3. **ATMS (Animate Topological Material Science)** — The concept that topological materials aren't static objects but engineered systems with active verification loops. Likely an extension of the tenfold way (Altland-Zirnbauer classification) into an engineering framework — taking the 10 symmetry classes from a classification scheme into a design language.

4. **TAS (Thesis-Antithesis-Synthesis)** — The triplet pattern applied as explicit methodology. Simulation produces a result (thesis), the type checker or computation rejects it (antithesis), the hidden assumption is surfaced and corrected (synthesis). Every version of the architecture is more honest than the last.

5. **Deductive Engineering** — The unifying concept: engineering that works from verified principles downward (formalize, compile, check) rather than inductively from experimental data upward (observe, generalize, hope). Auditable reasoning at every step.

The fiction-to-formalism trajectory is the origin story. The triplet/TAS/deductive engineering methodology is what survived the transition. The PGTC result is the first concrete, publishable output of that methodology.

**AI collaboration model:** Gemini as concept partner (Digital Triplet, PGTC mechanism, material architecture). Claude as formalization partner (Lean 4 proofs, simulation analysis, epistemic auditing). Lean 4 as independent arbiter (compiler doesn't care who wrote it). This transparent three-tool methodology is itself a triplet.

---

github.com/GoS-Architect
144 unique zero-dep theorems | 7 sorry | Zero Mathlib dependencies
Full audit completed March 19, 2026 (by Claude, Opus 4.6)
