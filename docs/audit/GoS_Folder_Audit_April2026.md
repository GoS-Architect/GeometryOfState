# GoS Glassbox — Folder Structure Audit

**Date:** April 7, 2026
**Scope:** All files and folders in `GoS_Glassbox_April-2026/`
**Method:** Full directory tree mapping, content hashing, naming analysis, thematic classification

---

## 1. Summary

The folder contains 188 files across 25 subdirectories and 15 loose root-level files. The work spans Lean 4 formalization, Agda, Python simulations, React dashboards, LaTeX papers, and Word/Markdown documentation for the Geometry of State (GoS) research program.

The main issues are: three near-duplicate Lean project folders, typos baked into folder names, loose root files that belong inside existing folders, significant version sprawl without a clear "canonical" marker, and a mismatch between the proposed v5 repo structure (which you already wrote) and the current layout.

---

## 2. Typos in Folder Names

Seven folder names contain misspellings or inconsistencies:

| Current Name | Issue | Suggested Fix |
|---|---|---|
| `RacthetHamiltonian` | "Racthet" → "Ratchet" | `RatchetHamiltonian` |
| `GoS-Retaction-v2` | "Retaction" → "Retraction" | `GoS-Retraction-v2` |
| `KiteavCertification` | "Kiteav" → "Kitaev" | `KitaevCertification` |
| `HeliumLoom-TaylorRelaxationi` | trailing "i" | `HeliumLoom-TaylorRelaxation` |
| `Edgemide-Bivector-Lean` | "Edgemide" → "EdgeMode" | `EdgeMode-Bivector-Lean` |
| `SpingroupBiVector` | "Spingroup" (missing capital G, inconsistent casing) | `SpinGroup-Bivector` |
| `QuantumStellerator-Research` | "Stellerator" → "Stellarator" | `QuantumStellarator-Research` |

Additionally, the naming **separators** are inconsistent: some folders use hyphens (`GoS-Blueprint`), some use CamelCase (`CliffordFoundation`), some use spaces (`PGTC Documents`), and some mix underscores with hyphens. Pick one convention and apply it everywhere.

---

## 3. Duplicate Lean Files

Three folders contain the same trio of Lean files — `BivectorDiscrimination.lean`, `EdgeModeBivector.lean`, `SpinGroup.lean` — but with **different content** (all hashes differ):

| Folder | Likely Role |
|---|---|
| `BivectorDiscrimination/` | Has `lakefile.lean` + `CHANGELOG`. Looks like the primary project. |
| `Edgemide-Bivector-Lean/` | 3 files only, no build config. Possibly an earlier snapshot. |
| `SpingroupBiVector/` | Has `lakefile.lean` but no docs. Possibly a fork/variant. |

**Recommendation:** Determine which is canonical, archive the others into a clearly marked `_archive/` folder (or delete them). Three divergent copies with the same filenames is a merge hazard.

---

## 4. Loose Root Files

15 files sit at the top level with no folder. Most have a natural home:

| File | Suggested Destination |
|---|---|
| `GQAC_v0_1.md`, `GQAC-v0_2.docx` | → `Glassbox-4_1-GQAC-v_0/` |
| `GoS_Quasiperiodic_Ratchet_Thesis.docx` | → `RatchetHamiltonian/` (alongside v2 and v3) |
| `HiTT_Architectural_Draft_v0_25.docx` | → `GoS-Retraction-v1/` (alongside v0.1 and v0.2) |
| `MZM_Certification_Architecture.docx` | → `KitaevCertification/` or `MZM-Vortex-ER-EPR-FWS/` |
| `NQI_Systems_Architecture_v1.docx` | → `Glassbox-NQI-QRoadtrip/` |
| `GoS-5ResearchProposals.docx` | → `GoS-Arch-v4-Roadmap/` or a new `GoS-Meta/` folder |
| `GoS-TQC-Fusion.docx` | → `MZM-Vortex-ER-EPR-FWS/` (topological quantum computing fusion) |
| `Clifford-10FoldWay-MZM.md` | → `CliffordFoundation/` |
| `EmergentGravity-MZMDetection-TQC.md` | → `MZM-Vortex-ER-EPR-FWS/` |
| `QuantumMaterialsExploration.md` | → `QuantumMaterials/` or `QuantumMaterials-Ni62/` |
| `SVT-Sonifacation.md` | Unique topic — keep at root or create a new folder |
| `GoS-13Problems.md` | Meta/roadmap doc — `GoS-Arch-v4-Roadmap/` or root (if it's a top-level index) |
| `Beta_Testing_Reality.pdf` | Unclear fit — keep at root or move to a `Publications/` folder |
| `Quantum Parks Infrastructure Research.pdf` | Same — `Publications/` or root |

---

## 5. Version Sprawl

At least 35 files carry version suffixes (_v1, _v2, _v3, etc.) and in many cases multiple versions live side by side with no indication of which is current. The worst cases:

- **Ratchet Thesis:** `GoS_Quasiperiodic_Ratchet_Thesis.docx` (root) + `_v2.docx` and `_v3.docx` (in `RatchetHamiltonian/`). Three versions across two locations.
- **HiTT Architectural Draft:** `v0.1` and `v0.2` in `GoS-Retraction-v1/`, plus `v0_25` at root. Three versions across two locations.
- **Quantum Materials GoS Reference:** `v1`, `v2`, `v3` all in the same folder.
- **FWS Materials Architecture:** `v2` and `v3` in the same folder.
- **Glassbox Constitutional XAI:** `v3` and `v3.1` in the same folder.
- **Repository Audit/Organization:** audit v1 and v2, organization v3, structure v5 — spread across three different folders.

**Recommendation:** For each versioned chain, either (a) keep only the latest and move older versions to `_archive/`, or (b) adopt a convention like `CURRENT_<name>.docx` for the canonical version.

---

## 6. Thematic Overlap Between Folders

Several folders cover closely related territory and could potentially be consolidated:

**Bivector/SpinGroup cluster** (3 folders):
`BivectorDiscrimination/`, `Edgemide-Bivector-Lean/`, `SpingroupBiVector/` — all contain the same three Lean files at different stages. Consolidate into one.

**GoS Architecture/Meta cluster** (4+ locations):
`GoS-Arch-v4-Roadmap/`, `GoS-v4-AuditableReasoning/`, `GoS-Blueprint/`, `PGTC Documents/`, plus loose root files like `GoS-13Problems.md` and `GoS-5ResearchProposals.docx`. These all deal with project-level planning, architecture specs, and audits.

**Topological Bridge** (2 folders):
`TopologicalBridge-v2/` and `TopologicalBridgeRefined/` — both contain `.lean` files for the same conceptual bridge. Could be one folder with clear versioning.

**Retraction** (2 folders):
`GoS-Retraction-v1/` and `GoS-Retaction-v2/` — clear version sequence but the typo in v2 obscures the relationship.

---

## 7. Misplaced or Surprising Files

A few files seem out of place in their current folders:

- `CLHoTT-CayleyDickson-AGDA/GeometryOfState_ResearchProposal.docx` and `GeometryOfState_Thesis_WhitePaper.docx` — these are docs, not Agda/Lean code. They'd fit better in a docs or meta folder.
- `CliffordFoundation/linkedin_gimbal_lock.md` — a social media post draft sitting in a Lean project folder.
- `GoS-v4-AuditableReasoning/Adrian_Domingo_Professional_Profile.docx` — personal/professional doc in a technical audit folder.
- `GoS-v4-AuditableReasoning/Journal_Entry_March_2026_PRIVATE.docx` and `Personal_Journal_March_2026_PRIVATE.docx` — private journal entries in a shared project folder. Consider moving these somewhere private.
- `GoS-v4-AuditableReasoning/Gemini_Handoff_Brief.md` — agent handoff doc, not an audit artifact.
- `CleanSetupGoogleDrive/` — workspace setup guides, not GoS research content.

---

## 8. Existing Structure Proposals

You already have **three** prior attempts at reorganization in this repo:

1. `GoS_Repo_Organization_v3.md` (March 25, 2026)
2. `GoS_Repository_Audit_v2.md` (March 24, 2026)
3. `GoS_Repository_Structure_v5.md` (March 2026)

The v5 structure proposal is the most mature — it cleanly separates `src/` (verified code), `docs/` (documentation), and `agents/` (Socratic Partner constitutions). **None of these proposals have been executed.** The current folder structure doesn't reflect any of them.

---

## 9. Recommended Next Steps

1. **Fix the typos** — rename the 7 misspelled folders. This is quick and unambiguous.
2. **Pick a naming convention** — I'd suggest `PascalCase-With-Hyphens` since most folders already lean that way. Eliminate spaces (`PGTC Documents`).
3. **Consolidate the Bivector trio** — pick one canonical folder, archive the other two.
4. **File the loose root documents** — move the 15 root files into their natural folders per Section 4.
5. **Resolve version chains** — for each document that exists in 2-3 versions, decide what's canonical.
6. **Separate private/personal files** — journal entries and professional profiles should live outside the research repo.
7. **Consider executing your v5 structure** — you've already designed a clean `src/docs/agents` split. The main barrier is just doing the move.

---

*Generated by Claude · April 7, 2026*
