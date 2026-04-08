# Bridging Clifford algebras, the tenfold way, and Majorana modes in Cubical Agda

**The formal verification of topological condensed matter physics in Homotopy Type Theory is a genuinely frontier research program with no direct precedent.** No one has formalized the Kitaev chain, BdG Hamiltonians, Majorana zero modes, or the Altland-Zirnbauer classification in any proof assistant. Yet a clear pathway exists: the Sati-Schreiber program at CQTS (NYU Abu Dhabi) has demonstrated that HoTT naturally encodes topological quantum gates via transport in dependent types, and Cubical Agda already contains the synthetic homotopy theory infrastructure — cohomology, Eilenberg-MacLane spaces, higher homotopy groups — needed as a foundation. The five gaps identified below range from immediately actionable (installing Cubical Agda and studying the π₁(S¹) proof) to genuinely novel (constructing a "Volovik functor" connecting Green's function topology to KR-theory). This report maps each gap's existing formalization, missing pieces, key references, active researchers, and concrete next steps.

---

## GAP 1: The π₁(S¹) ≅ ℤ proof and Cubical Agda on Apple Silicon

### Toolchain as of early 2026

The latest stable Agda release is **version 2.8.0**, a significant release that ships as a self-contained single binary (no separate data files). The matching cubical library is **v0.9**, and these two must be used together — version coupling is strict. The development branch is 2.9.0, requiring GHC 9.2.8–9.12.2.

For an Apple Silicon Mac Mini, the recommended installation path is **GHCup + Cabal**: install GHCup first, then `cabal install Agda`. This compiles from source and takes considerable time and memory, but produces the latest version. On macOS, the ICU library path may need explicit specification (`--extra-lib-dirs` and `--extra-include-dirs` for `/usr/local/opt/icu4c/`). Homebrew (`brew install agda`) is faster but may lag behind releases. A third option — `pip install agda` — provides binary wheels including `macosx_11_0_arm64` but currently lags at v2.7.0.1. GitHub release binaries are not Apple-notarized and require `xattr -d com.apple.quarantine` to run.

The VS Code extension **agda-mode-vscode** (by banacorn) is actively maintained and supports Agda Language Server connections. Known issues on macOS include incorrect architecture detection for ALS binaries (issue #192) and keybinding conflicts with system shortcuts. Recent CI updates address Agda 2.8.0 output format changes.

| Component | Version | Installation |
|-----------|---------|-------------|
| Agda | **2.8.0** | `cabal install Agda` via GHCup |
| Cubical library | **v0.9** | `git clone` + `git checkout v0.9` |
| VS Code plugin | Latest | Marketplace: `banacorn.agda-mode` |
| GHC requirement | 8.8.4–9.12.2 | Via GHCup |

### Where the encode-decode proof lives

The encode-decode proof of **π₁(S¹) ≅ ℤ** resides in `Cubical.HITs.S1` (file `Cubical/HITs/S1.agda`). The key definitions are `helix : S¹ → Type` (the universal cover), `encode`/`decode` maps, `winding : ΩS¹ → ℤ`, and the culminating path `ΩS¹≡ℤ : ΩS¹ ≡ ℤ`. The companion file `Cubical.Papers.Synthetic` re-exports these definitions with commentary matching the CPP 2020 paper by Mörtberg and Pujet.

The recommended study path through the library is: `Cubical.Foundations.Prelude` (paths, transport, hcomp) → `Cubical.Foundations.Isomorphism` (Iso, isoToPath) → `Cubical.Foundations.Univalence` (ua, Glue types) → `Cubical.Data.Int` (integers, `sucPathℤ`) → `Cubical.HITs.S1` (the proof itself).

### Ljungström-Mörtberg π₄(S³) formalization

This work **won the Distinguished Paper Award at LICS 2023** ("Formalizing π₄(S³) ≅ ℤ/2ℤ and Computing a Brunerie Number in Cubical Agda," June 2023, DOI: 10.1109/LICS56636.2023.10175833). An extended journal version appeared in *Mathematical Structures in Computer Science* (2024/2025, arXiv: 2302.00151). The formalization introduces extensive new machinery: **simplified Brunerie numbers** (one normalizes to −2 in seconds, giving a computer-assisted proof), Eilenberg-MacLane spaces and cohomology groups with cup products, the Mayer-Vietoris sequence, Hopf invariant, James construction, Blakers-Massey theorem, and Gysin sequence. Ljungström has continued producing distinguished work — LICS 2025 (Distinguished Paper + Kleene Award with David Wärn) and ITP 2025.

The companion files in the cubical library are `Cubical/Papers/Pi4S3.agda` and `Cubical/Papers/Pi4S3-JournalVersion.agda`, with implementation details in `Cubical/Homotopy/Group/Pi4S3/`.

### The HoTT Game and Escardó's notes

The HoTT Game (thehottgameguide.readthedocs.io) **requires cubical library v0.3 and Agda 2.6.2** — it does not work with the latest versions and has not been updated. It remains playable in-browser via Agdapad, and its first quest line (proving π₁(S¹) = ℤ from scratch) is excellent pedagogy, but the version incompatibility is a significant limitation.

Escardó's "Introduction to Univalent Foundations of Mathematics with Agda" was **last updated November 17, 2025** and remains actively maintained. It uses standard Agda (not cubical) with univalence postulated rather than computed. It serves as an excellent pedagogical gateway — learn the concepts here, then transition to Cubical Agda for computational content. The modular version lives in `source/MGS/` of the TypeTopology repository.

### Practical recommendations for GAP 1

Install Agda 2.8.0 via Cabal on the Mac Mini. Clone the cubical library at v0.9. Begin with Escardó's notes for conceptual foundations, then work through the `Cubical.HITs.S1` module directly. The HoTT Game is useful for intuition but requires a separate Agda 2.6.2 installation. Study the π₄(S³) paper files to understand the cohomology infrastructure that will be needed for later gaps.

---

## GAP 2: Dagger categories via path types — a completely open field

### Category theory in Cubical Agda and the 1Lab

The `Cubical/Categories/` directory in the cubical library contains categories, functors, natural transformations, adjunctions, limits, displayed categories, abelian and additive categories, free categories, and the category of elements. Recent additions (2024–2025) include reworked displayed category reasoning and free category improvements. However, the library lacks explicit univalent categories as a standalone development.

The **1Lab** (1lab.dev) fills this gap comprehensively. It is described in Agda's official documentation as "much better documented than the agda/cubical library and hence more accessible to newcomers." Its category theory is described by its maintainers as constituting "a vast majority" of the library's mathematics. It formalizes **univalent categories** via identity systems following Ahrens-Kapulkin-Shulman exactly (`is-category C = is-identity-system (Isomorphism C) (λ a → id-iso C)`), the **Rezk completion** with its universal property, displayed categories and displayed univalence, monoidal categories, bicategories, monads, Kleisli categories, the Yoneda lemma, congruences, and regular categories. For this project, the 1Lab is the strongest existing foundation for univalent category theory in Cubical Agda.

### No dagger categories formalized anywhere

After exhaustive search, the finding is unambiguous: **no formalization of dagger categories exists in any proof assistant as of April 2026**. This spans Cubical Agda (both agda/cubical and 1Lab), Lean 4/Mathlib, Coq UniMath, the Coq HoTT library, agda-categories (Hu-Carette), and Isabelle. The gap extends to dagger compact categories, dagger Frobenius algebras, and the entire Abramsky-Coecke categorical quantum mechanics framework.

The closest computational tools are DisCoPy (Python library for categorical quantum mechanics with string diagrams), Quantomatic (automated diagram reasoning), and homotopy.io (Jamie Vicary's higher-dimensional diagrammatic reasoning tool) — none of which are formal verifications.

### The †-saturation concept in HoTT

Mike Shulman introduced the concept of **†-saturated categories** in a 2013 n-Category Café post: just as univalent categories identify paths between objects with isomorphisms, †-saturated categories identify paths with *unitary* isomorphisms (isomorphisms f where f† = f⁻¹). This is the natural HoTT formulation of dagger categories and has **never been formalized**. It represents a genuinely novel contribution waiting to be made.

### Key references

**Ahrens-Kapulkin-Shulman**, "Univalent categories and the Rezk completion," *Mathematical Structures in Computer Science* 25(5), 2015, pp. 1010–1039 (arXiv: 1303.0584). Originally formalized in Coq UniMath; the concepts are now also formalized in the 1Lab. Recent extensions include van der Weide's enriched univalent categories (FSCD 2024) and double category univalence principles (CSL 2025).

**Heunen-Vicary**, *Categories for Quantum Theory: An Introduction*, Oxford Graduate Texts in Mathematics 28, 2019. Defines dagger categories as categories with an involutive identity-on-objects contravariant endofunctor. Covers dagger biproducts, dagger equalizers, dagger compact closure, and dagger Frobenius structures. Active follow-up work by **Di Meglio and Heunen** (2024–2025) on axiomatizing finite-dimensional Hilbert spaces categorically has not been formalized.

### What's missing and what to do

The formalization of dagger categories in Cubical Agda represents a **completely open and publishable contribution**. The recommended approach: build on the 1Lab's univalent category infrastructure, define the dagger structure as an identity-on-objects contravariant endofunctor, then prove †-saturation (the dagger analogue of univalence). Use Heunen-Vicary as the axiom source. This is likely the most immediately achievable of the five gaps.

---

## GAP 3: Cohesive modalities ʃ ⊣ ♭ ⊣ ♯ — native support meets cubical friction

### The flat modality is now mainline Agda

There is no longer a separate "agda-flat" fork. **The ♭ modality is built into Agda** via the `--cohesion` flag (with `--flat-split` for pattern matching on crisp arguments), maintained as part of mainline Agda by Andrea Vezzosi and the core development team. The `@♭` attribute provides crisp variables: `♭ A` can be defined as an inductive type with constructor `con : (@♭ x : A) → ♭ A`. This is available in Agda 2.6.x through 2.8.0 and documented in the 2.9.0 development docs.

However, **only ♭ is native** — neither ♯ (sharp) nor ʃ (shape) are built-in. A critical limitation exists: in Cubical Agda, functions matching on `@♭` arguments trigger the `UnsupportedIndexedMatch` warning, and code may not compute properly (open issue agda/agda#6238). This tension between `--cohesion` and `--cubical` is the primary technical obstacle.

The **agda-unimath** library has the most developed formalization of modal type theory using these features: `modal-type-theory.flat-modality` (♭), `modal-type-theory.sharp-modality` (♯ postulated as a right adjoint), and `modal-type-theory.flat-sharp-adjunction` (proving ♭(♯A) ≃ ♭A).

### What Wellen and Myers have formalized

**Felix Cherubini** (née Wellen) defended his thesis "Formalizing Cartan Geometry in Modal Homotopy Type Theory" at KIT in 2017 (arXiv: 1806.05966). The formalization in the DCHoTT-Agda repository (github.com/felixwellen/DCHoTT-Agda, checks with Agda 2.6.2.2) covers the **infinitesimal shape modality ℑ** — a single monadic modality of differential cohesion. Key results: formal disk bundles over groups are trivial, formal disk bundles over V-manifolds are locally trivial, and all F-fiber bundles are associated to Aut(F) principal bundles. Crucially, this uses only one modality out of six needed for full differential cohesion, and it is monadic (so it doesn't require the judgmental machinery of ♭).

**David Jaz Myers** published "Good Fibrations through the Modal Prism" (*Higher Structures* 6(1), 2022) and "Modal Fracture of Higher Groups" (*Differential Geometry and its Applications*, 2024). His PhD thesis "Symmetry, Geometry, Modality" (Johns Hopkins, 2022) develops extensive modal HoTT theory. With Hassan, he formalized **Higher Schreier Theory in Cubical Agda** (*Journal of Symbolic Logic*, 2024) — one of the few actual Cubical Agda formalizations of cohesive/modal constructions. His repository `DavidJaz/Cohesion` contains further cohesion formalizations.

**Myers-Riley "Commuting Cohesions"** (arXiv: 2301.13780, presented at HoTT 2023) extends spatial type theory to handle multiple commuting cohesive structures simultaneously — enabling types to carry both topological and simplicial structure, or differential and equivariant structure. This is critical for the full Sati-Schreiber program but remains unformalized.

### The no-go theorem and the hybrid approach

**Shulman proved that ♭ cannot be axiomatized as an internal operation Type → Type** (Section 4 of the real-cohesion paper, *MSCS* 28(6), 2018). The flat modality inherently requires crisp/judgmental support — it restricts the context. This means pure axiomatic postulation without `--cohesion` cannot properly handle ♭.

The currently viable approach is **hybrid**: ♭ uses native `--cohesion`, ♯ is postulated as a right adjoint to ♭ (as in agda-unimath), and ʃ is postulated as a monadic modality à la Rijke-Shulman-Spitters (*LMCS* 16(1), 2020). The Cubical Agda library already has `Cubical/Modalities/Modality.agda` providing a general framework for monadic modalities. The tradeoff: postulated modalities lack computation rules (transport gets stuck), while the native ♭ has cubical compatibility issues.

### Emerging proof assistants

Two experimental systems deserve attention. **Narya** (github.com/mikeshulman/narya), Shulman's proof assistant for Higher Observational Type Theory, is designed for eventual multimodal support but does not yet implement cohesive modalities. **mitten** (Stassen-Gratzer-Birkedal, TYPES 2022) implements Multimodal Type Theory with preordered mode theories — the most direct implementation of Licata-Shulman adjoint logic — but cannot yet handle the full 2-categorical mode theory needed for cohesive HoTT.

### Recommendations for GAP 3

Use Agda 2.8.0 with `--cohesion --flat-split` for ♭, postulate ♯ following agda-unimath's `modal-type-theory` module, and axiomatize ʃ as a monadic modality using the cubical library's modality framework. Accept that ♭ + cubical interaction will produce warnings and limited computation. For the shape modality specifically, study `Cubical/Modalities/Modality.agda` and the Rijke-Shulman-Spitters theory. Monitor Narya's development for a future cleaner approach. The `--cohesion` + cubical friction is the single biggest technical risk in this research program.

---

## GAP 4: The Kitaev chain and topological condensed matter in HoTT — terra incognita

### No condensed matter formalized in any proof assistant

After broad searching, the result is definitive: **no formalization of any standard condensed matter physics concept exists in any proof assistant**. No Kitaev chain, no BdG Hamiltonian, no Majorana zero modes, no SSH model, no quantum Hall Hamiltonian, no topological band theory — nothing. The gap is total.

### The Sati-Schreiber program is the closest existing work

The Center for Quantum and Topological Systems (CQTS) at NYU Abu Dhabi, led by **Hisham Sati** and **Urs Schreiber**, represents essentially the **only active effort** at the triple intersection of HoTT formalization, topological phases, and K-theory classification. Their program has pivoted significantly toward condensed matter since ~2022:

- **"Topological Quantum Gates in Homotopy Type Theory"** (Myers-Sati-Schreiber, *Communications in Mathematical Physics* 405:172, 2024, arXiv: 2303.02382) — the breakthrough paper. Topological quantum gates are formalized as transport in parameterized dependent types into Eilenberg-MacLane spaces. Explicitly discusses Majorana/Ising anyons and Fibonacci anyons. **Certifiable in Cubical Agda**, with ongoing formalization at CQTS by research assistant Zyad Yasser.
- **"Anyonic topological order in TED K-theory"** (Sati-Schreiber, *Reviews in Mathematical Physics* 35(03):2350001, 2023) — classifies su(2)-anyonic topological order in interacting 2D semi-metals using twisted equivariant differential K-theory.
- **"Fragile Topological Phases and Topological Order of 2D Crystalline Chern Insulators"** (Schreiber, arXiv: 2512.24709, December 2025) — classifies crystalline Chern insulators via equivariant 2-Cohomotopy.
- **"Orientations of Orbi-K-Theory measuring Topological Phases and Brane Charges"** (arXiv: 2511.12720, November 2025) — connects orbifold K-theory to topological phase measurement.

The program's code formalization status: Shulman formalized core cohesive HoTT axioms in Coq (Rocq code at `LocalTopos.v`). The topological quantum gates construction is being formalized in Cubical Agda at CQTS. The bulk of the program — TED K-theory, anyonic classification, cohomotopy classification of crystalline phases — remains paper mathematics, described as "written in the pseudocode formerly known as mathematics."

### The Altland-Zirnbauer tenfold classification has no formal verification

The mathematical backbone connecting the AZ classification to homotopy theory is well understood: the 10 symmetry classes correspond to 10 classical compact symmetric spaces, and Kitaev's "periodic table" maps symmetry class × dimension to K-theory groups via **Bott periodicity in real and complex K-theory** (Kitaev 2009). Freed-Moore's "Twisted Equivariant Matter" (2013) provides the rigorous framework using KR-theory. **None of this has been formalized.** The obstacles are fundamental: topological K-theory, Bott periodicity, and KR-theory have not been formalized in any proof assistant.

The **Freed-Hopkins classification** ("Reflection positivity and invertible topological phases," *Geometry & Topology* 25, 2021, pp. 1165–1330, arXiv: 1604.06527) uses stable homotopy theory (Thom bordism spectra, Anderson duality) to classify symmetry-protected topological phases. The mathematics is far beyond current proof assistant capabilities — bordism theory, spectral sequences, and equivariant stable homotopy theory have no formalizations.

### First steps toward K-theory in HoTT

At HoTT/UF 2025, **Reid Barton** (Carnegie Mellon) presented "first steps towards construction of topological K-theory" in HoTT — using simplicial sets and an "interval" type axiom. This is **very early-stage** work but represents the first direct attempt to build the K-theory bridge in HoTT. Lean's Mathlib contains some algebraic K-theory infrastructure (exact sequences, group completions) but no K-theory spectrum, no Bott periodicity, and no KR-theory.

The existing Cubical Agda infrastructure most relevant to this gap includes: synthetic cohomology (Eilenberg-MacLane spaces, cohomology groups, cup products — formalized by Lamiaux-Ljungström-Mörtberg, CPP 2023 Distinguished Paper), the Hopf fibration (`Cubical/Homotopy/Hopf.agda`), and sphere joins. These provide the homotopy-theoretic substrate but not the K-theoretic superstructure.

### Recommendations for GAP 4

This gap requires a two-track strategy. **Track 1 (immediate)**: Study the CQTS topological quantum gates formalization closely. Their encoding of anyon braiding as transport in dependent types is the nearest existing model for encoding topological physics in Cubical Agda. Contact Zyad Yasser at CQTS for current code status. **Track 2 (medium-term)**: The Kitaev chain specifically requires formalizing: (a) a BdG Hamiltonian as a Hermitian operator on a finite-dimensional Hilbert space with particle-hole symmetry, (b) the topological invariant (winding number) as a map to ℤ, (c) the bulk-boundary correspondence relating this invariant to Majorana zero modes. The winding number computation could potentially reuse the existing π₁(S¹) machinery — the loop space characterization is structurally similar. The Clifford algebra structure underlying the AZ classification connects directly to the algebraic infrastructure needed.

---

## GAP 5: The Volovik functor and bulk-boundary correspondence — toward a categorical framework

### No "Volovik functor" exists in the literature

Volovik's topological classification of gapless systems uses Green's function topology in momentum-frequency space, assigning homotopy invariants (winding numbers, Chern numbers) to different universality classes. His monograph *The Universe in a Helium Droplet* (Oxford UP, 2003) and review "Topology of quantum vacuum" (arXiv: 1111.4627, 2012) develop this physically but **never organize it as a functor between categories**. Constructing such a functor — mapping a category of Hamiltonians with symmetry data to a category of K-theory classes — would be a genuinely novel mathematical contribution.

### Bulk-boundary correspondence has rigorous K-theoretic proofs

The most rigorous mathematical treatment is **Alldridge-Max-Zirnbauer** (*Communications in Mathematical Physics*, 2019), who proved bulk-boundary correspondence across all 10 AZ symmetry classes using real C*-algebras: a bulk-to-boundary short exact sequence connects bulk and boundary K-theory, and the connecting map in KR-theory maps bulk classes to boundary classes. Other rigorous treatments include Prodan-Schulz-Baldes (*Bulk and Boundary Invariants for Complex Topological Insulators*, Springer, 2016), Bourne-Kellendonk-Rennie (Kasparov theory approach, 2017), and Mathai-Thiang (T-duality approach, 2015–2018). **None have been formalized in proof assistants.**

On the categorical side, **Kong and Zheng** showed that the boundary-bulk relation is functorial — the Drinfeld center construction mapping boundary to bulk topological order can be made functorial in monoidal categories describing 1+1D topological orders.

### Functors in topological phase classification

The field has extensively used functorial structures without always naming them as such:

- **Johnson-Freyd** (*Communications in Mathematical Physics* 393, 2022) axiomatizes topological orders as anomalous fully-extended TQFTs using monoidal Karoubi-complete n-categories. The Cobordism Hypothesis provides a functorial equivalence between gapped topological phases and fully extended TQFTs.
- **Gaiotto-Johnson-Freyd** (arXiv: 1905.09566, updated April 2025) develops condensations in higher categories — the higher Karoubi envelope construction.
- **Inamura** (*JHEP* 2021, 204) classifies SPT phases with fusion category symmetries via fiber functors: SPT phases correspond to equivalence classes of quintuples where fiber functors S → Vec are the classifying data.
- **Freed-Hopkins** classify invertible/SPT phases as maps between Thom bordism spectra and Anderson duals — an explicitly functorial construction.

However, **explicit functors mapping between different classification schemes** (Volovik's Green's function classification → K-theory classification → cobordism classification) have never been systematically constructed as a commutative diagram.

### Univalence and physical equivalences

The **Hole Argument** in general relativity provides the clearest existing connection between univalence and physics: Ladyman and Presnell (*Foundations of Physics*, 2020) showed that the univalence axiom naturally resolves the Hole Argument because diffeomorphism-related spacetime models are literally equal in HoTT. Schreiber's program uses univalence to ensure all constructions respect gauge equivalence automatically. **No work connecting univalence to condensed matter equivalences** (e.g., identifying topologically equivalent Hamiltonians) has been published. This connection — using univalence to formalize when two gapped Hamiltonians represent "the same" topological phase — is conceptually natural but unexplored.

### Recommendations for GAP 5

The "Volovik functor" construction requires defining: (a) a source category (gapped/gapless Hamiltonians with symmetry data and continuous deformations as morphisms), (b) a target category (K-theory groups or homotopy types), and (c) the functor itself (assigning topological invariants and proving functoriality). The existing encode-decode machinery in Cubical Agda for π₁(S¹) provides a structural template — the winding number of a loop in BdG Hamiltonian space is computed by exactly the same homotopy-theoretic mechanism. Start by formalizing the simplest case: the winding number classification of 1D class BDI (the Kitaev chain's symmetry class).

---

## Cross-cutting: researchers, institutions, and the distance to formalization

### Active researchers spanning multiple gaps

**Urs Schreiber** (CQTS, NYU Abu Dhabi) is the central figure connecting cohesive HoTT (GAP 3), topological phases (GAP 4), and K-theoretic classification (GAP 5). His 2025 papers on crystalline Chern insulators and orbifold K-theory represent the frontier. **Hisham Sati** (CQTS director) co-architects the TED K-theory program. **David Jaz Myers** (formerly Topos Institute, now at CQTS) bridges modal HoTT formalization (GAP 3) and topological quantum gates (GAP 4) — his "Topological Quantum Gates in HoTT" paper is the single most relevant existing work for this project. **Mike Shulman** (University of San Diego) created real-cohesive HoTT and is developing Narya, an experimental proof assistant designed for multimodal type theories. **Felix Cherubini** (University of Augsburg, organizer of HoTT/UF 2025 and 2026) produced the only existing Agda formalization of differential cohesion.

On the topological phases side, **Theo Johnson-Freyd** (Perimeter Institute) leads higher-categorical classification of topological orders. **Daniel Freed** (Harvard) and **Michael Hopkins** provide the bordism-theoretic classification framework. **Liang Kong** and **Hao Zheng** (SUSTech, Shenzhen) develop the functorial boundary-bulk relation. **Ralph Kaufmann** (Purdue) and **Varghese Mathai** (Adelaide) work on KR-theory approaches to topological insulators.

**CQTS at NYU Abu Dhabi is the only institution actively working at the triple intersection** of HoTT formalization, topological physics, and K-theory classification. Their GitHub organization (github.com/CQTS) contains Cubical Agda coursework and projects.

### Key conferences and workshops (2025–2026)

- **"QFT and Topological Phases via Homotopy Theory and Operator Algebras"** — CMSA Harvard + MPIM Bonn twinned workshop, **June 30 – July 11, 2025**. Lecturers include Michael Hopkins and Alexei Kitaev. Explores Kitaev's conjecture that invertible phases are classified by an Ω-spectrum.
- **HoTT/UF 2026** — Aarhus, Denmark, **June 1–2, 2026**. Organizers: Felix Cherubini, Axel Ljungström, Daniel Gratzer, Loïc Pujet.
- **"Homotopy Theory, K-theory, and Topological Data Analysis"** — Western University (Ontario), **June 8–12, 2026**.
- **"Higher Differential Geometry"** — Greifswald, **May 4–6, 2026**. Schreiber speaking.
- **"Quantum Information and Quantum Matter 2026"** — NYU Abu Dhabi, **May 20–23, 2026**. Schreiber speaking.
- **"A Panorama of Quantum Topology"** — BIRS Banff, **July 19–24, 2026**.
- **TYPES 2026** — Paris (INRIA). Abstracts due January 12, 2026.

### The distance map

The table below estimates the formalization distance from current state to project goals:

| Component | Current state | Gap size | Estimated effort |
|-----------|--------------|----------|-----------------|
| π₁(S¹) ≅ ℤ in Cubical Agda | **Complete** (Cubical.HITs.S1) | None | Ready to use |
| Synthetic cohomology, cup products | **Complete** (Lamiaux-Ljungström-Mörtberg) | None | Ready to use |
| Univalent categories | **Complete** in 1Lab | None | Ready to use |
| Dagger categories | **Nothing exists anywhere** | Large | ~6–12 months |
| ♭ modality | **Native** in Agda --cohesion | Cubical friction | Workaround needed |
| ♯ modality | **Postulated** in agda-unimath | Partial | Usable now |
| ʃ (shape) modality | **Axiomatizable** as monadic modality | Moderate | ~3–6 months |
| Full differential cohesion (6 modalities) | **1 of 6 formalized** (Cherubini) | Very large | ~3–5 years |
| K-theory spectrum in HoTT | **Early steps** (Barton, HoTT/UF 2025) | Very large | ~2–4 years |
| KR-theory + Bott periodicity | **Nothing** | Enormous | ~3–5 years after K-theory |
| Kitaev chain in HoTT | **Nothing** | Novel | ~1–2 years (simplified model) |
| AZ tenfold classification | **Nothing formalized** | Enormous | Requires KR-theory |
| Topological quantum gates | **Partially formalized** at CQTS | Moderate | Ongoing |
| Volovik functor | **Not constructed mathematically** | Novel | ~1–2 years (mathematical), then formalization |
| Bulk-boundary in HoTT | **Nothing** | Very large | Requires K-theory stack |

### The most promising path forward

Rather than attempting to formalize classical K-theory bottom-up (which could take a decade), this project should follow the **Sati-Schreiber shortcut**: use cohesive HoTT to synthetically construct topological phase classifications directly from the physics, leveraging Cohomotopy and equivariant cohomology. Their 2025 papers on crystalline Chern insulators demonstrate this strategy works mathematically. The immediate roadmap:

1. **Now**: Master the π₁(S¹) proof and cohomology infrastructure in Cubical Agda (GAP 1).
2. **Months 1–6**: Formalize dagger categories in the 1Lab framework, establishing †-saturation as the HoTT-native formulation (GAP 2). This is the most publishable near-term contribution.
3. **Months 3–9**: Set up the hybrid cohesive modality stack (♭ native + ♯ postulated + ʃ axiomatized) and verify basic cohesive constructions (GAP 3).
4. **Months 6–18**: Formalize the Kitaev chain as a simplified BdG Hamiltonian with a winding number invariant, reusing the ΩS¹ ≅ ℤ machinery for the topological invariant (GAP 4). Contact CQTS for collaboration.
5. **Months 12–24**: Construct the Volovik functor mathematically for the 1D BDI class, then formalize (GAP 5).

The critical insight is that the winding number classifying the Kitaev chain's topological phase is *the same mathematical object* as the winding number in π₁(S¹) ≅ ℤ — both are elements of the fundamental group of U(1). Cubical Agda already has this. The project's unique contribution is building the bridge from this existing infrastructure to the physics.