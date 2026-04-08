# Quantum Materials Review — GoS-Targeted Reference (v3)

*Content retained only where it feeds a specific GoS architecture layer (L0–L5).*
*Sources: General quantum materials review, MZM Certification Architecture,*
*Microsoft Majorana 1 research brief, ATMS Quantum Materials 2026.*

---

## Feeds L0 (Foundations): Formal Verification and Type-Theoretic Foundations

### Lean 4 as Deductive Infrastructure

Formal verification using machine-checked mathematical logic has been a staple of cryptography, aerospace, and safety-critical software. It is now being adapted for theoretical quantum materials science. Lean 4 functions as both an interactive proof assistant and a functional programming language, enabling formalization of complex mathematical theories while preventing human error in dense topological proofs.

Recent work demonstrates Lean 4's efficacy in formalizing nonlinear dynamics: convergence of Hebbian learning in deterministic Hopfield networks has been proved, and ergodicity of stochastic Boltzmann machines established by formalizing the Perron-Frobenius theorem.

**Application to topological hardware**: BdG Hamiltonians governing candidate superconducting devices are transcribed into formalized type theory. Researchers then construct machine-verified proofs that a specific material configuration, under defined parameter regimes (SOC strength, magnetic field), possesses a non-zero topological invariant (e.g., a nontrivial ℤ₂ index). This pre-verifies MZM existence before the expense of synthesis, isolating true topological phases from trivial mimics purely through mathematical logic.

**GoS connection**: Your L0 is Lean 4 v4.12.0 with zero Mathlib dependencies. The kernel is the verifier. The application described here — formalizing BdG Hamiltonians as type-theoretic objects and proving topological invariants — is exactly what your L1→L2 pipeline does. The gap condition as a dependent type (IsGappedAt), the winding number as a derived integer, and the edge mode theorems verified by rfl are instances of this methodology. The ATMS framing makes explicit what your architecture already implements: formal deductive verification is not optional for topological quantum hardware, it is a non-negotiable engineering necessity because inductive observation cannot prove global topological properties.

### Homotopy Type Theory (HoTT)

HoTT establishes a connection between Martin-Löf dependent type theory and algebraic topology. Within HoTT:

- Logical types are interpreted as topological spaces
- Terms are interpreted as points within those spaces
- Mathematical equality is interpreted as a continuous path (homotopy) between points
- The **Univalence Axiom** codifies that equivalent mathematical structures are identical

This natively topological representation of logic makes HoTT the natural foundational language for expressing properties of materials where physical behavior is dictated by continuous deformations and invariant topological structures.

**GoS connection**: Your L0 includes Cubical Agda (planned), where π₁(S¹) ≅ ℤ is proved and the winding number carries computational content. Cubical Agda implements a computational version of HoTT where univalence is a theorem rather than an axiom. The HoTT interpretation — types as spaces, equality as paths — is the formal content underlying your core claim that "singularities are type errors": the phase transition is a point where the path (homotopy) between gapped Hamiltonians becomes undefined.

### Linear Homotopy Type Theory (LHoTT)

HoTT alone cannot encode the resource constraints of quantum mechanics (no-cloning). LHoTT extends HoTT with "dependent linear" homotopy data types, whose categorical semantics reside in parameterized stable homotopy theory. LHoTT natively comprehends topological error-protection, quantum coherence limits, and projective quantum measurements.

By encoding non-Abelian braiding of anyonic quasiparticles (SU(2)-monodromies) as homotopy data types, LHoTT enables exact compilation and verifiable certification of topological quantum gates. It simultaneously proves the physical operation principles of hardware (braiding an anyon along a specific path produces a specific unitary rotation) while certifying the algorithmic correctness of quantum logic circuits above the hardware.

**GoS connection**: LHoTT is the formal language that could unify your L2 (classification of topological phases) with your L5 (certification of quantum gates). Your current architecture uses Lean 4 (not LHoTT) for classification and Clifford algebra certification. LHoTT represents a potential future L0 extension where the braiding operations themselves become type-theoretic objects with machine-checked correctness proofs. The CLHoTT.lean file (frozen, 7 theorems, 6 sorry) is an early step in this direction.

---

## Feeds L1 (Algebra): Clifford Structure, Berry Phase, Division Algebras

### The Clifford Algebra–Majorana Isomorphism

Majorana operators satisfy:

    γᵢγⱼ = −γⱼγᵢ  (i ≠ j),    γᵢ² = 1

These are precisely the defining relations of the real Clifford algebra Cl(n,0). This isn't analogy — it's isomorphism. The consequences:

- A pair of spatially separated MZMs encodes a nonlocal fermion c = (γ₁ + iγ₂)/2 defining two degenerate parity states — the qubit.
- The energy splitting between parity states decays as e^(−L/ξ), where L is wire length and ξ is localization length. This exponential suppression is the formal basis of topological protection.
- The gap condition (IsGappedAt in your Lean code) corresponds to the invertibility of a bivector in the Clifford algebra. When the gap closes, the bivector is non-invertible — the proof obligation is undischargeable.

**GoS connection**: Your L1 encodes Cl(2,0) and Cl(3,0) multiplication tables derived from three rules (signature, anticommutativity, associativity), the gap condition as a dependent type, and the winding number as a derived integer from rotor phase accumulation over the BZ. Six edge mode theorems are verified by rfl for the 3-site Kitaev chain. The certification architecture extends this: strain perturbation is formalized as a Cl(2,0) rotor transformation (the sandwich product in Rotor3D.rotate), and ABS vs. MZM distinction becomes whether a state satisfies bivector invariance under that rotor action.

### Quantum Geometric Algebra (QGA)

In the QGA framework, quantum mechanical states are manipulated without imaginary numbers or matrix representations. A qubit is defined by the co-occurrence of orthonormal state vectors. The geometric product applied to two orthogonal vectors creates a bivector that acts as a spinor — a rotational operator in quantum state space. A critical property: applying the spinor twice yields complete inversion (S² = −1), acting as the square root of a logical NOT.

The geometric product is inherently anticommutative (ab = −ba) and homologous to the tensor product in standard Hilbert spaces, allowing natural algebraic representation of multi-qubit registers and entanglement structures (ebits, Bell states). Quantum operations — particularly the reversible phase rotations central to topological computing — are executed using vector addition and geometric products, dramatically more streamlined than complex matrix representations.

**GoS connection**: This algebraic simplicity is why your L1 Clifford formalization in Lean 4 works at all. The Cl(2,0) multiplication table you've formalized is exactly the QGA framework for a single-qubit register. The geometric product encodes gate operations, the sandwich product encodes frame rotations (your Rotor3D.rotate), and the bivector invertibility encodes the gap condition. QGA makes the Lean 4 formalization of quantum gates tractable by bypassing the computational overhead of complex matrices — you're proving properties of algebraic operations, not diagonalizing matrices.

### Berry Phase and Curvature

The Berry phase is a geometric phase acquired by an electron's wave function moving adiabatically in parameter space. The Berry connection acts as an effective vector potential; its curl, the Berry curvature, acts as an effective magnetic field in momentum space:

- Berry curvature modifies semiclassical electron dynamics by adding an anomalous velocity transverse to applied forces — the microscopic origin of AHE, SHE, QAHE.
- Integrals of Berry curvature over closed manifolds yield Chern numbers (integer-valued, robust).
- Weyl nodes are monopoles/antimonopoles of Berry curvature — point sources of quantized flux.

**GoS connection**: The winding number in Winding.lean is the 1D instance. The Berry phase integral over a closed BZ path gives w ∈ ℤ classifying the Kitaev chain. This invariant is computable from the Hamiltonian's eigenstates and is what your type-theoretic framework makes uncallable at phase boundaries.

### Spin-Orbit Coupling as Algebraic Structure

SOC is the interaction between electron spin and orbital angular momentum, fundamentally relativistic (Dirac equation). Strength scales as ~Z⁴ (hydrogenic) or ~Z³ (screened valence). SOC entangles spin and momentum degrees of freedom, is the essential ingredient for most topological phases, and in the Clifford algebra language mixes the spin and spatial generators. In InAs nanowires (Majorana 1 substrate), strong Rashba SOC from structural inversion asymmetry, combined with Zeeman splitting and proximity superconductivity, drives the topological phase transition.

### The Division Algebra Ladder

ℝ → ℂ → ℍ → 𝕆, each step trading a constraint for a capability:

- **ℝ → ℂ (ordering → rotation)**: Winding number π₁(S¹) ≅ ℤ requires the complex phase. Mathematical content of your Cubical Agda proof.
- **ℂ → ℍ (commutativity → spin)**: Kramers degeneracy (T² = −1 for spin-1/2) is quaternionic — the Z₂ invariant for TIs lives here.
- **ℍ → 𝕆 (associativity → gauge)**: Cayley-Dickson construction in CayleyDickson.lean produces octonions. Connection to exceptional Lie groups (E₈).

---

## Feeds L2 (Classification): The Tenfold Way, Interactions, and Beyond

### The Altland-Zirnbauer Classification (Complete Table)

Free-fermion topological phases are classified by three discrete anti-unitary symmetries. Because T and C are anti-unitary, their squares evaluate to +1, −1, or 0 (absent). This yields exactly ten AZ symmetry classes:

    AZ Class    T    C    S    Invariant(1D)  Invariant(2D)  Invariant(3D)
    ─────────────────────────────────────────────────────────────────────
    A           0    0    0         0              ℤ              0
    AIII        0    0    1         ℤ              0              ℤ
    AI         +1    0    0         0              0              0
    BDI        +1   +1    1         ℤ              0              0
    D           0   +1    0         ℤ₂             ℤ              0
    DIII       −1   +1    1         ℤ₂             ℤ₂             ℤ
    AII        −1    0    0         0              ℤ₂             ℤ₂
    CII        −1   −1    1         2ℤ             0              ℤ₂
    C           0   −1    0         0              ℤ              0
    CI         +1   −1    1         0              0              ℤ

The classification repeats with period 2 (complex classes A, AIII) and period 8 (real classes) — Bott periodicity. K-theory and nonlinear sigma models provide the mathematical tools. The bulk-boundary correspondence guarantees that a non-trivial bulk invariant necessitates protected gapless boundary states.

**Extensions beyond the tenfold way:**
- **Topological Crystalline Insulators/Superconductors (TCIs/TCSs)**: Spatial symmetries (reflection, inversion, point-group) protect additional phases characterized by mirror Chern numbers or mirror ℤ₂ invariants.
- **Gapless topological materials**: Nodal line semimetals, Weyl semimetals — invariants defined on surfaces enclosing gapless points in the BZ.

**GoS connection**: Your AlgebraicLadder.lean (13 theorems) formalizes this classification. The Bott periodicity is the same as the Clifford algebra sequence Cl(n,0). Your Kitaev chain sits in class BDI (1D, invariant ℤ = winding number). The BdG generalization to class D (breaking T with Ni-62 exchange) changes the 1D invariant from ℤ to ℤ₂. The full table is the object your L2 must eventually encode completely.

### Classification Collapse Under Interactions

The free-fermion tenfold way fails when many-body interactions dominate. Strong electron-electron interactions can cause classification "collapse": states that are topologically distinct and protected in the non-interacting limit can be adiabatically deformed into each other via interaction pathways, destroying their protection.

**The critical example for GoS**: In 1D, class BDI collapses from ℤ to ℤ₈ under strong interactions. This means the Kitaev chain winding number w is only protected modulo 8 when interactions are present. Chains with w = 8 can be smoothly deformed to w = 0 (trivial) by turning on interactions. For w = 1 (your ratchet_full.py result), the protection survives — but this collapse constrains what invariants remain meaningful in realistic, interacting devices.

**Symmetry-Protected Topological (SPT) phases**: Classified using group supercohomology theory and cobordism theory. These go beyond free-fermion K-theory.

**Many-Body Real Space Invariants (RSIs)**: Generalize Topological Quantum Chemistry (TQC) to the interacting regime. RSIs are defined as eigenvalues of discrete symmetry operators on open boundaries, with spatial cutoffs around Wyckoff positions ensuring independence from boundary conditions. In the thermodynamic limit, many-body RSIs become quantized coefficients of Wen-Zee terms in the governing TQFT. This identifies strongly correlated topological phases with no single-particle analogue.

**GoS connection**: Your current L2 is free-fermion (112 theorems, zero sorry). The interaction-driven collapse is an open problem for the framework — if you formalize class BDI with invariant ℤ, you should be aware that the physical system only respects ℤ₈ when correlations are strong. For the Kitaev chain at w = 1, this doesn't change the conclusion, but it matters for higher-winding-number phases and for any future extension to strongly correlated systems. The RSI framework is a potential target for L2 extension beyond free fermions.

### Bulk-Boundary Correspondence

A non-trivial bulk invariant guarantees protected boundary states:

- Bulk w = 1 in Kitaev chain → two MZMs at endpoints
- Bulk Z₂ in 3D TIs → spin-momentum locked Dirac cone surface states
- Bulk Chern number n → n chiral edge modes

Boundary states cannot be removed by perturbations preserving symmetry class and bulk gap. This is why the type-theoretic formulation works: as long as IsGappedAt holds, the invariant is well-defined and edge modes guaranteed. Gap closes → invariant undefined → proof term absent → phase transition = type error.

### Topological Invariants in Disordered, Finite Systems

In idealized models, the transition is sharp. In real devices with disorder, finite size, and inhomogeneous potentials, the transition becomes a crossover and the invariant's applicability is contested.

**GoS connection**: Microsoft's TGP attempts to measure transport quantities reflecting the bulk invariant but has been challenged (Legg, Basel, 2025) for significant false-positive rate. Your parametrized gap certification (IsGappedAt over parameter ranges) addresses this directly. A formally verified connection between scattering matrix invariant and bulk classification would settle the debate.

### Material-Specific Classification

**Topological Insulators**: Class AII. Bi₂Se₃, Bi₂Te₃. MnBi₂Te₄ (AFM TI) shows symmetry-breaking-driven class transitions.

**Dirac/Weyl semimetals**: Four-fold/two-fold degenerate crossings. Berry curvature monopoles. Fermi arcs. TaAs family. Your FWS device targets Weyl physics.

**The Kitaev Chain**: Class D or BDI, ℤ invariant in 1D. Parameters: t, Δ, μ. Topological when |μ| < 2t with Δ ≠ 0. Your L2 has 35 theorems; ratchet_full.py diagonalizes the BdG at specific parameters — the L2→L3 bridge.

---

## Feeds L3 (Physics): BdG, MZMs, Phase Transitions, Floquet Engineering

### BdG Formalism and Topological Superconductivity

The BdG Hamiltonian describes quasiparticle excitations above the superconducting ground state. Built-in particle-hole symmetry automatically places superconductors in AZ classes supporting topological phases.

Pairing symmetry determines topological class:
- s-wave (conventional) → class CI or C
- p-wave (Kitaev chain) → class D or DIII, supports MZMs
- d-wave (cuprates) → nodal, different topological structure

**GoS connection**: ratchet_full.py computes w = 1, confirming two MZMs with 99.7% edge localization in 1D. The ni62_simulate_all.py extends this with spinful BdG, site-dependent exchange and SOC across five Ni-62 geometries.

### Majorana Zero Modes: Physics and Verification

MZMs are quasiparticle excitations that are their own antiparticles (γ = γ†):

- Zero energy (pinned by particle-hole symmetry)
- Spatially localized at boundaries/defects
- Non-Abelian braiding statistics
- Exponential protection: splitting decays as e^(−L/ξ)

**The Majorana vs. Andreev crisis**: At least three trivial state classes mimic MZMs:

1. **Andreev bound states** from disorder-induced quantum dots
2. **Yu-Shiba-Rusinov states** from magnetic impurities
3. **Quasi-Majorana states** — partially separated ABS mimicking nonlocality

The 2021 Nature retraction of quantized Majorana conductance claims demonstrated that the field's evidentiary framework is insufficient. The crisis is epistemological: inductive observation (measuring a conductance peak) is mathematically insufficient to prove a global topological property. This is the deepest motivation for your formal verification approach.

**The distinguishing property is spatial decay**: Genuine MZM pair components are exponentially localized at opposite wire ends (nonlocal). ABS components spatially overlap (local). Machine-checked proof of conditions ensuring exponential smallness of overlap provides a verification standard.

### Intrinsic Topological Superconductors: Beyond Engineered Heterostructures

The fragility of engineered nanowire heterostructures has driven a strategic pivot toward crystalline materials with intrinsic topological superconductivity:

**Iron-based superconductors (FeSCs)**: LiFeAs and FeTe₁₋ₓSeₓ are premier candidates. Strongly correlated systems with Hund's coupling and multi-orbital physics, natively hosting topological Dirac surface states within their superconducting gaps. Because the topological state is a bulk property of the crystal rather than an interface artifact, they offer higher operational temperatures and greater stability. The verification problem persists — distinguishing MZM from impurity-site ABS still requires multi-modal, non-local protocols.

**UTe₂**: Verified as intrinsic TSC via Andreev STM (spin-aligned pairs, topological surface state), though Majoranas appear in inseparable pairs.

**Microsoft Majorana 1** (InAs/Al): H-shaped nanowire qubits, ~1% parity measurement error, TGP under challenge, Nature paper disclaims topological determination. Device roadmap: single-qubit → two-qubit braiding → eight-qubit logical improvement → qubit array with lattice surgery.

### Quantum Phase Transitions as Singularities

QPTs at T = 0, driven by non-thermal parameters. At the QCP: ground state energy non-analytic, ξ and ξ_τ diverge, gap vanishes, scale-invariant behavior. Universality: near QCPs, properties depend on dimensionality and symmetries, not microscopic details.

**GoS connection**: "Singularities are type errors." Gap closes → winding number undefined (IsGappedAt undischargeable) → computation blocked at type level. The QPT is the absence of a proof term.

### Floquet Engineering and Prethermalization

Floquet engineering applies periodic drives (high-frequency laser pulses) to dynamically modify the effective Hamiltonian H_eff. Periodic modulation can induce topological phase transitions, creating Floquet topological insulators or superconductors from topologically trivial equilibrium materials.

**The many-body heating problem**: Periodically driven, interacting quantum systems absorb energy from the drive and eventually heat to a featureless infinite-temperature state, destroying coherence, entanglement, and topological protection.

**Prethermalization**: If the driving frequency is much higher than the system's local energy scales, energy absorption is exponentially suppressed (multi-photon processes have low probability). Before eventual thermalization, the system enters a long-lived prethermal plateau where it behaves as if governed by the engineered H_eff. Experiments on 78-qubit superconducting processors have confirmed prethermal phases with stable, coherent oscillatory entanglement dynamics.

**GoS connection**: Floquet engineering is a potential future extension for your L4 (device). A Floquet drive could dynamically tune the topological phase at defect boundaries rather than relying solely on static Ni-62 exchange. The prethermalization timescale sets a fundamental limit: quantum algorithms must complete within the prethermal lifetime. For your current architecture (static material stack + strain perturbation), Floquet is not directly operational, but it represents a path toward dynamically programmable topological domains — converting the fixed Penrose-seeded defect pattern into a reconfigurable topological circuit.

---

## Feeds L4 (Device): Material Design for the FWS Stack

### SOC and Heavy Element Selection

SOC ~Z⁴. Your FWS stack includes Nb (Z = 41) for superconductivity with SOC. In InAs/Al (Microsoft), strong Rashba SOC from structural inversion asymmetry at the interface, combined with Zeeman splitting and proximity-induced superconductivity, drives the topological transition. Your graphene/Nb system uses different SOC sources (intrinsic + proximity + defect-induced at Stone-Wales boundaries).

### Strain Engineering (Dual Role)

Strain in L4 (FWS design): Penrose-seeded SW defects create quasiperiodic strain/hopping modulation. Stage 1 failure: δt/t₀ = 59% vs. physical ~10% (wrong lattice diagnosis).

Strain in L5 (certification): Piezoelectric AFM applies controlled strain; Bir-Pikus coupling modifies μ and SOC. Formalized as Cl(2,0) rotor transformation.

### Heterostructure Engineering

Your FWS stack (Si-28 / C-12 Penrose graphene / Nb / He-3/4) is a heterostructure. Graphene-Nb interface: proximity-induced superconductivity creates effective p-wave pairing. Microsoft's InAs/Al uses epitaxial growth for a "hard" induced gap. Interface quality determines gap cleanliness.

**Ni-62 integration (from simulations)**: Patterned Ni-62 nano-islands at 5/7 defect sites provide local exchange splitting (~6 meV), breaking time-reversal symmetry at defects while preserving bulk Dirac physics. Ni-62 simulation results: minimum topological defect width ≥51 sites. This constrains Penrose tiling geometry for the corrected 2D lattice.

### Defect Engineering

Si-28 and C-12 isotopic purity eliminates nuclear spin disorder (I = 0 for both). Ni-62 extends this (I = 0, highest nuclear binding energy per nucleon). Stone-Wales 5/7 defects are intentional topological defects in service of topology, not random impurities.

---

## Feeds L5 (Verification): The Certification Problem

### The Verification Crisis

The Majorana verification crisis is epistemological: inductive observation cannot prove global topological properties. ABS mimicry makes standard transport measurements insufficient. The 2021 Nature retraction, the TGP false-positive challenge, and the Nature paper's explicit disclaimer ("measurements do not determine whether detected states are topological") all confirm that the field needs deductive verification.

DARPA's US2QC/QBI program frames verification as the program's primary function.

### Verification Needs Across the GoS Stack

**L1**: Clifford algebra → Majorana operators → exponential localization chain must be machine-checked.
**L2**: Topological invariant well-defined for finite, disordered systems. Parametrized gap certification.
**L2/L3**: MZM vs. ABS: exponential nonlocality vs. local overlap. Imposter taxonomy.
**L3**: Measurement-based braiding = adiabatic braiding (Clifford group, formalizable).
**L4/L5**: Error propagation: given measured rates, does architecture deliver fault-tolerance threshold?

### Topological Data Analysis as Verification Modality

TDA via persistent homology measures multiscale connectivity of datasets to extract robust global topological features. Applied to momentum-space or real-space point cloud data from a material:

- A filtration (Vietoris-Rips complex) is applied as a length-scale parameter increases
- Topological features are born and die: connected components (β₀), loops (β₁), voids (β₂)
- Lifespans are recorded as persistence diagrams or barcodes
- Persistence images (normalized vector representations) feed directly into ML classifiers

**Why TDA matters for verification**: Persistent homology detects phase transitions where conventional local order parameters fail. In topological transitions, local symmetries aren't broken — Ginzburg-Landau theory is useless. But TDA applied to lattice spin models, skyrmion systems, and amorphous materials reveals hidden order invisible to Fourier analysis or local probes.

By counting persistent topological features across macroscopic datasets, TDA bypasses the interpretational ambiguities of isolated local measurements like ZBCPs. It provides an objective, mathematically rigorous methodology to verify emergence of true topological phases from empirical data.

**GoS connection**: TDA could serve as a fourth verification channel alongside your three-gate protocol (strain invariance, NV relaxometry, Clifford certification). While your three gates operate on transport and magnetic data, TDA operates on the global topology of the dataset itself. A persistence barcode showing a stable β₁ feature (loop) in the BdG spectrum across the strain sweep would provide independent topological evidence. This is speculative but well-grounded — the mathematical machinery exists and has been demonstrated for classical phase transitions. Extending it to superconducting topological transitions is an open research direction.

### The Three-Gate Certification Protocol

**Gate 1 — Topological gap certification**: IsGappedAt satisfiable across strain sweep → compute W; W ≠ 0 → topological.

**Gate 2 — Strain invariance**: ZBCP variance < Δ_topo/10 across strain sweep. Larger shift → REJECT. Formalized as Cl(2,0) rotor invariance (sandwich product).

**Gate 3 — NV-transport consistency**: T₁ minimum (NV) agrees with ZBCP disappearance (transport) within resolution. Disagreement → artifact → REJECT.

Rejection iterates; exhaustion of parameter space = definitive negative = falsifiability concrete.

### Gate Physics

**Gate 1**: Gap Δ protects MZMs. In InAs/Al, Δ > 30 µeV. Computing gap from parameters and checking IsGappedAt is formally decidable.

**Gate 2**: Bir-Pikus Hamiltonian couples strain to μ and SOC. Piezoelectric AFM applies controlled strain. True MZMs don't move; ABS shift. Three modes: ramp, dwell, oscillatory. Rotor invariance = algebraic criterion for topological protection.

**Gate 3**: NV centers (10 nm from wire), electrically decoupled. T₁ relaxometry measures magnetic noise from quasiparticle excitations. Gap closing → noise increases → T₁ drops. Agreement between NV and transport phase boundaries = same transition, not artifacts.

### General Probes

- **ARPES**: Band structure, surface states, gap symmetry.
- **STM/STS**: Local DOS, ZBCPs, edge mode localization. Andreev STM verified UTe₂.
- **Transport**: Quantized conductances, chiral anomaly, quantum oscillations. Local + nonlocal matrices distinguish MZM nonlocality. SSAR (spin-selective Andreev reflection).
- **Josephson**: 4π periodicity from MZMs vs. 2π conventional.

### Entanglement as Diagnostic

- **Area law**: Gapped ground states → boundary-area scaling of entanglement entropy. Signature of the gapped phase where IsGappedAt holds.
- **Topological entanglement entropy**: Universal negative constant for topologically ordered systems.
- **Critical systems**: Logarithmic corrections with CFT coefficients at phase boundaries (type errors).

---

## What's Not Here (and Why)

Cut from the original quantum materials review:
- Core QM pedagogy, band theory basics, electron configuration / periodic trends (beyond SOC)
- Heavy fermion phenomenology (beyond unconventional SC), QSLs in detail (beyond non-Abelian anyons)
- Coherence engineering (beyond entanglement scaling), statistical mechanics basics
- AI/ML discovery methods, spintronics, quantum sensing applications, energy conversion
- Hyperon-inspired appendix

Cut from the ATMS document:
- **Introduction** (padded grand claims about "permanent paradigm shifts" and "redefining" fields)
- **Section 5.3 (ATMS / "animate materials")** — speculative. The "nervous system" and "metabolism" metaphors for AI-controlled Floquet driving are conceptually interesting but not grounded in demonstrated physics. Prethermalization physics is retained; the "living material" framing is cut.
- **Section 6 in its entirety (Digital Triplet / Industry 5.0)** — industrial engineering framework for cyber-physical systems. The Lean 4 verification gate concept (proposed new action must pass formal proof before physical actuation) is architecturally sound but belongs to a different project scope. Multi-agent orchestration, ecosystemic governance, Industry 5.0 alignment — none of this feeds GoS L0–L5.
- **Section 7 (Synthesis)** — recap paragraphs restating earlier content.
- **AI in materials discovery** (Section 6.1) — GNoME, MatterGen, MACE are useful tools but your project is theorem-proving and simulation, not ML screening. Already covered and cut in v2.
