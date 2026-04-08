# PGTC PREPRINT — DRAFTING BRIEF

**For: New Claude conversation**
**From: Adrian Domingo**
**Date: March 20, 2026**

---

## Task

Help me draft an arXiv preprint (cond-mat.mes-hall or cond-mat.mtrl-sci). Lead with the physics. Keep it focused, honest, and citable. I have a potential arXiv endorser at University of Wisconsin (engineering physics background).

---

## The result

**Title concept:** Something like "Phonon Glass Topological Crystal via Quasiperiodic Stone-Wales Defects in Graphene"

**Core claim:** A honeycomb graphene lattice with Penrose-selected Stone-Wales (5-7-7-5) defects simultaneously supports a topological electronic phase and suppresses phonon transport. The mechanism: electron hopping scales as d⁻² (Harrison scaling), phonon spring constants scale as d⁻⁴ (Keating scaling). The same geometric modulation produces 2× stronger effective disorder for phonons than electrons.

**2D simulation (main result, corrected lattice, N=800, 30 defects):**
- κ_QP / κ_ordered = 0.30 (70% phonon suppression)
- 12 localized phonon modes in quasiperiodic vs 0 in ordered
- Spectral gap ratio: 58.8×
- Phonon modulation / electron modulation ratio: 5.0
- All gate conditions PASS

**1D ratchet (supporting result, N=100):**
- Winding number w = -1 (topological)
- 2 Majorana zero modes, 99.7% edge-localized
- κ ratio = 0.86 in 1D (weaker effect, expected for 1D)
- Phase boundary at μ ≈ 2.0 (gap closes)
- Robustness: topological phase survives δt up to ~0.49

**AZ classification (verified):**
- BDI is trivial in d=2 (simulation confirmed, step1_clean_baseline.py)
- Breaking TRS via exchange field moves BDI → D
- Class D in d=2 has ℤ invariant (Bott index)
- Gap closes at h_ex ≈ 0.6 (step3_spinful_bdg.py)

---

## Failure history (include in paper — shows methodology)

- **v1 lattice FAILED:** Used Penrose tile vertices directly as lattice sites. Produced coordination numbers {3..10}, unphysical 59% hopping modulation. Result: 0 zero modes, Bott index = 0, all gates fail.
- **Diagnosis:** Wrong lattice type. Penrose tiling should seed defect locations, not replace the graphene lattice.
- **v1 Rashba error:** Non-Hermitian Rashba matrix (error 0.35) produced 4 spurious MZMs. Fixed: corrected conjugation.
- **v1 bilayer:** Mismatched layers (pristine L2) caused Layer 2 to dominate. Fixed: matched defect layers.
- **v2 corrected:** Honeycomb graphene + face-traced Stone-Wales defects. ~12% modulation (physical). Passes all gates.

---

## Scripts producing the results

| Script | Result file | What it computes |
|--------|------------|-----------------|
| ratchet_full.py | ratchet_full_results.json | 1D BdG + phonon transport |
| run_all.py (v2) | stage2_summary.json (v2) | 2D PGTC (main result) |
| graphene_sw_lattice.py | — | Corrected lattice generator |
| step1_clean_baseline.py | stage1_summary.json | BDI baseline (trivial d=2) |
| step3_spinful_bdg.py | — | Ni-62 exchange transition |
| step3b_finescan.py | — | Bott index parameter scan |

Failed results preserved: stage1_summary.json, combined_report.json

---

## Formal verification (mention, don't center)

Lean 4 formalization exists for the underlying algebraic structures (github.com/GoS-Architect). Relevant theorems:
- Phonon scaling steeper than electron scaling (proved)
- PGTC amplification factor = 2 (proved)
- Bott periodicity for class D (proved)
- AZ classification table (encoded and verified)
- 144 unique theorems, 0 sorry in classification layer

Reference the repo in the paper but don't require readers to know Lean.

---

## What the paper needs

1. **Abstract** — the result in 150 words
2. **Introduction** — phonon glass + topological crystal as dual objectives, cite PGEC literature (Slack, Nolas, skutterudites), cite tenfold way (Kitaev 2009, Ryu et al 2010)
3. **Model** — honeycomb lattice, SW defect construction, BdG Hamiltonian, Harrison/Keating scaling
4. **Results** — 1D ratchet, 2D PGTC, phase diagram, kappa ratios
5. **Failure analysis** — v1 failure, diagnosis, correction (this IS the methodology section)
6. **Discussion** — connection to AZ classification, what remains to be demonstrated (genuine MZMs at defect sites need larger lattice), formal verification as future direction
7. **Conclusion**

---

## Constraints

- I'm an independent researcher, no institutional affiliation
- First arXiv submission — need endorsement
- No Mathlib dependencies in the Lean code (zero-dependency architecture)
- Timeline pressure: severance runway ends ~June 2026
- Lead with physics, not AI methodology — the AI story opens scrutiny that distracts from the result
