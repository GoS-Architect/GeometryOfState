# Geometric presuppositions and detection thresholds in emergent gravity and topological quantum matter

**Jacobson's celebrated 1995 derivation of the Einstein field equations from thermodynamics does not derive gravity from thermodynamics alone—it derives gravitational *dynamics* from thermodynamics applied atop a pre-existing Lorentzian geometry.** The derivation presupposes a differentiable manifold, a full metric with Lorentzian signature, and causal structure. No subsequent program (Padmanabhan, Verlinde, Chirco-Haggard-Riello-Rovelli) has succeeded in deriving geometry itself from thermodynamic or information-theoretic principles. In the parallel domain of topological quantum matter, the detection problem is inverted: the theoretical predictions exist but lack the specificity needed for matched-filter-style detection. The Majorana zero mode controversy—culminating in a 2021 Nature retraction and ongoing disputes over Microsoft's topological gap protocol—reveals that condensed matter physics has no equivalent to the **5σ** detection standard used in gravitational wave astronomy, and the fundamental obstacle is that every device is unique, eliminating the universality that makes LIGO's template matching possible.

---

## THREAD 1: What Jacobson's derivation actually assumes and derives

### The full inventory of geometric presuppositions

Ted Jacobson's 1995 derivation (Physical Review Letters 75, 1260) applies the Clausius relation δQ = TdS locally to Rindler horizons to obtain the Einstein field equations. The logical structure is precise and its inputs are identifiable at each step.

**Presupposed geometric structure.** The derivation begins with a **4-dimensional differentiable manifold equipped with a Lorentzian metric** g_μν of signature (−,+,+,+). This is the starting arena, not an output. From this metric follow all the geometric objects the derivation uses: light cones, null surfaces, null geodesics, causal horizons, the Levi-Civita connection, and the Riemann curvature tensor. The Lorentzian signature is essential—it enables the distinction between timelike and spacelike, and hence the existence of null surfaces that serve as local Rindler horizons.

**Riemann Normal Coordinates and the unimodular condition.** Jacobson invokes the equivalence principle to view a small neighborhood of each spacetime point as approximately flat. In Riemann Normal Coordinates (RNC), the metric satisfies g_μν(p) = η_μν at the origin, with Christoffel symbols vanishing there. The metric determinant satisfies **√(−g) = 1 + O(x²)**, meaning area and volume elements are flat to leading order. This "unimodular condition" ensures that the area element dA on 2-surface cross-sections of the null congruence can be treated as the flat-space area element, with curvature corrections entering only at subleading order. The condition cannot be significantly weakened within Jacobson's framework—it is automatic in RNC and reflects the physical requirement that the integration region is small compared to the curvature scale. Alternative coordinate systems (Gaussian null coordinates, as used by Parikh and Svesko in 2018) replace this condition with analogous smallness conditions, but the essential physics remains.

**Three thermodynamic inputs.** Beyond the geometric framework, Jacobson assumes three physical relations as inputs:

- **The Unruh temperature** T = ℏκ/(2π), assigning a temperature to the local Rindler horizon proportional to the acceleration κ. This is an explicit input, relying on quantum field theory on curved spacetime and the Bisognano-Wichmann theorem. Jacobson states: "We shall thus take the temperature of the system to be the Unruh temperature."

- **The Bekenstein-Hawking area-entropy relation** dS = η dA, where η is a proportionality constant later identified as 1/(4ℓ_P²). This is assumed, not derived. Jacobson motivates it via entanglement entropy arguments but explicitly treats it as an input. Changing this assumption (e.g., to entropy densities polynomial in the Ricci scalar) yields different field equations.

- **The Clausius relation** δQ = TdS, demanded to hold for all local Rindler horizons through every spacetime point. This is the bridge principle connecting thermodynamics to geometry.

### The derivation step by step and what it produces

The logical chain proceeds as follows. At each point, Jacobson constructs a local Rindler horizon—a null surface with vanishing expansion and shear (the "local equilibrium condition," always achievable by construction). The energy flux δQ through this horizon is expressed as an integral of T_ab χ^a dΣ^b, where χ^a is the approximate boost Killing vector. The entropy change dS = η δA is computed using the area variation, which the **Raychaudhuri equation** relates to the Ricci tensor: in the equilibrium limit, the expansion θ satisfies θ = −λ R_ab k^a k^b, where k^a is the null generator.

Equating δQ = TdS then yields T_ab k^a k^b = (ℏη/2π) R_ab k^a k^b for all null vectors k^a. Since this holds for all null k^a, algebraic reasoning gives R_ab + f g_ab = (2π/ℏη) T_ab for some undetermined scalar function f. A **separate assumption**—local energy-momentum conservation ∇^a T_ab = 0—combined with the contracted Bianchi identity then fixes f = −R/2 + Λ, yielding the full Einstein equations G_ab + Λg_ab = 8πG T_ab with G = 1/(4ℏη).

**What is derived is the dynamical content**: the specific tensor relationship governing how matter curves spacetime. What is **not** derived includes the manifold structure, the metric, its signature, the causal structure, the Raychaudhuri equation (a geometric identity), the Unruh effect, or the area-entropy proportionality. The result is precisely: **(Lorentzian geometry) + (QFT on curved spacetime) + (area-entropy) + (Clausius relation) + (energy conservation) → Einstein dynamics.**

A notable technical finding from Alonso-Serrano and Liška (2021): the thermodynamic derivation naturally produces **unimodular gravity** (traceless field equations), not full general relativity. The null-null projection constrains only 9 of 10 independent components. The trace equation—and hence the cosmological constant as an integration constant—emerges only when energy-momentum conservation is separately imposed. This suggests the minimal output is closer to Weyl transverse gravity than to standard GR.

### Why conformal structure alone is insufficient

A conformal structure (light cones without a scale) determines causal ordering and null geodesics as unparameterized curves. But it does **not** determine areas of surfaces, the Unruh temperature (which involves proper acceleration, hence a length scale), energy flux (which requires specific integration measures), or the Ricci tensor in its standard form. The derivation requires the **full metric**—conformal structure plus a volume element. Malament's theorem shows that causal structure determines the metric up to a conformal factor, but that conformal factor is precisely what is needed and cannot be obtained from causal structure alone.

### The SVT circularity problem

Superfluid Vacuum Theory claims the speed of light emerges as c² = ∂P/∂ρ from vacuum fluid properties. If one attempts to combine this with Jacobson-type reasoning, a fundamental circularity arises: **Jacobson's derivation requires pre-existing causal structure to define local Rindler horizons, but causal structure is determined by c, which SVT claims is emergent.** The Unruh temperature T = ℏa/(2πc) explicitly contains c. The Bekenstein-Hawking entropy uses areas defined by a Lorentzian metric whose causal structure depends on c. One cannot use the Unruh effect as input without first establishing c.

SVT proponents might argue for a two-stage process: first, superfluid dynamics establishes an effective metric with c as the sound speed; then Jacobson-type reasoning applies within the effective spacetime. But this does not constitute a thermodynamic derivation of gravity—it is a hydrodynamic derivation of effective spacetime followed by a thermodynamic reinterpretation of emergent field equations. The logical circularity remains unresolved in any single-stage derivation.

---

## No one has derived geometry from thermodynamics

### Post-Jacobson programs and their presuppositions

**Padmanabhan's program** (Reports on Progress in Physics 73, 046901, 2010) significantly extended Jacobson's result by showing that field equations of *any* diffeomorphism-invariant gravity theory reduce to TdS = dE + PdV on horizons, and by introducing the "cosmic space emergence" interpretation. However, Padmanabhan did **not** reduce the geometric presuppositions. His construction explicitly requires a differentiable manifold, causal structure, local Rindler horizons, and diffeomorphism invariance.

**Verlinde's entropic gravity** (JHEP 2011:029) arguably required *more* geometric input—holographic screens presuppose area and spatial embedding, plus the Unruh temperature and the Bekenstein entropy bound. Multiple criticisms identified circularity: Gao (2011) showed the entropy increase is caused by gravity rather than the reverse; Kobakhidze (2011) argued incompatibility with quantum coherence observations; Pardo (2017) found inconsistency with dwarf galaxy rotation curves.

**Chirco-Haggard-Riello-Rovelli** (Physical Review D 90, 044044, 2014) provided a valuable reinterpretation showing Jacobson's result is consistent with loop quantum gravity without hidden degrees of freedom—the relevant microscopic degrees of freedom are quanta of the gravitational field itself, and the entropy is entanglement entropy rather than statistical entropy. But they required all the same geometric structures as Jacobson.

**Jacobson's own 2015 refinement** ("Entanglement Equilibrium," Physical Review Letters 116, 201101, 2016) replaced the Clausius relation with the maximal vacuum entanglement hypothesis—the Einstein equation holds if and only if vacuum entanglement entropy is stationary. This shifts the input from thermodynamics to entanglement equilibrium but still requires a pre-existing spacetime manifold with Lorentzian metric, causal diamonds, and the Bisognano-Wichmann theorem.

### The frontier: geometry from non-geometric inputs

The most ambitious attempt is **Cao, Carroll, and Michalakis** (Physical Review D 95, 024031, 2017), who start from an abstract quantum state in Hilbert space, decompose it into tensor product factors, use mutual information to define distance, and extract spatial geometry via multidimensional scaling. They recover a spatial analog of Einstein's equation from entanglement perturbations. However, the approach is self-described as "extremely preliminary": it does not derive the Lorentzian signature, causal structure, or full spacetime, and it assumes a Hilbert space decomposition that constitutes an unresolved "factorization problem."

**Causal set theory** (Bombelli-Lee-Meyer-Sorkin, 1987) makes the most progress on recovering manifold geometry from discrete structures—recovering dimension, topology, and scalar curvature from locally finite partial orders. But it takes the causal partial order as fundamental rather than deriving it. The Lorentzian signature is built in from the start.

As of 2026, the hierarchy of what has been derived from non-geometric inputs is clear: gravitational dynamics can be derived from entanglement plus geometry (well-established); spatial metric can tentatively be extracted from entanglement (preliminary); manifold topology can partially be recovered from causal sets. But **differentiable structure, causal structure, and Lorentzian signature remain underived in all programs.** This is widely recognized as one of the central open problems in quantum gravity.

---

## THREAD 2: What a matched filter for topological signatures would require

### Why LIGO's matched filtering works—and what it demands

LIGO's detection pipeline rests on a remarkable fact: general relativity predicts **exact waveform templates** from a small number of physical parameters. The chirp mass, mass ratio, and spin parameters determine the complete time-frequency morphology of gravitational wave signals from compact binary coalescences. Post-Newtonian theory provides analytic inspiral waveforms to 4PN order; numerical relativity solves the full merger and ringdown; effective-one-body and phenomenological models stitch these together into complete inspiral-merger-ringdown templates calibrated against numerical simulations to **~99% faithfulness**.

The O4 template bank contains approximately **1.8 million templates** (Sakon et al., Physical Review D 109, 044066, 2024), placed to achieve minimal match ≥95%—any real signal overlaps with at least one template at 95% of optimal signal-to-noise ratio. GW150914 achieved a combined matched-filter SNR of ~24, with a false alarm rate below 1 event per 203,000 years, corresponding to significance exceeding 5.1σ. Background estimation uses time-sliding—shifting one detector's data by unphysical time offsets and rerunning the analysis to accumulate background statistics.

Three features make this possible: (1) theory predicts waveform shape to sub-percent accuracy; (2) the relevant parameter space is low-dimensional (~3-4 parameters for detection); (3) detector noise is well-characterized and approximately Gaussian and stationary.

### The Majorana detection problem: ZBCP insufficiency and the 2021 retraction

The zero-bias conductance peak at **2e²/h** was long considered the "smoking gun" for Majorana zero modes, following from particle-hole symmetry and perfect Andreev reflection. The 2018 Nature paper by Zhang et al. (Nature 556, 74) from Kouwenhoven's group at TU Delft reported quantized conductance plateaus in InSb-Al nanowires.

The paper was **retracted on March 8, 2021** (Nature 591, E30) after Frolov and Mourik discovered that data in multiple figures had been "unnecessarily corrected for charge jumps" without disclosure, an axis was mislabeled, and the full parameter range—including data not originally shown—revealed conductance values shifted ~8% above 2e²/h. The retraction stated: "We can therefore no longer claim the observation of a quantized Majorana conductance." Frolov's assessment was direct: "From the fuller data, there's no doubt that there's no Majorana."

The retraction crystallized what multiple groups had been demonstrating: **trivial Andreev bound states are ubiquitous mimics of Majorana signatures.** Chen et al. (Physical Review Letters 123, 107703, 2019) showed "ubiquitous non-Majorana zero-bias conductance peaks"; Yu et al. (Nature Physics 17, 482, 2021) demonstrated that non-Majorana states produce nearly quantized conductance. Smooth confinement potentials and disorder create "quasi-Majorana" states—pairs of weakly hybridized Andreev bound states where one couples strongly to the external lead and mimics a true Majorana in local transport measurements.

### Distinguishing true Majorana modes from trivial states

Theory predicts several morphological features that should discriminate:

- **Spatial nonlocality**: true Majorana pairs produce correlated signals at *both* wire ends simultaneously; trivial states are typically localized at one end.
- **Exponential energy splitting**: ΔE ~ exp(−L/ξ) for true Majorana pairs, with ξ the coherence length—directly measurable as a function of chain length.
- **Parameter robustness**: true Majorana ZBCPs persist as plateaus across extended ranges of magnetic field and gate voltage; disorder-induced peaks are spike-like and parameter-sensitive.
- **Gap closing and reopening**: the topological phase transition manifests as the bulk gap closing at critical magnetic field B_c and reopening—detectable in non-local conductance.
- **Spin-resolved correlations**: spin-up and spin-down currents are **anticorrelated** at low bias for Majorana states but positively correlated for trivial states.
- **Non-Abelian braiding statistics**: the definitive signature, but **never experimentally demonstrated** in any material system as of 2026. (Google and Quantinuum demonstrated braiding on quantum processors in 2023, but these are engineered simulations, not intrinsic material properties.)

### Kitaev chain predictions as potential templates

Kitaev's 2001 model (Physics-Uspekhi 44, 131) makes specific quantitative predictions. The topological phase exists for |μ| < 2|t| with Δ ≠ 0, with bulk spectrum E(k) = ±√[(μ + 2t cos k)² + 4|Δ|² sin² k]. For a finite chain of length L, the Majorana energy splitting is **ΔE ∝ exp(−L/ℓ₀)**, where ℓ₀ is the localization length. The tunneling conductance at zero temperature reaches exactly 2e²/h in the tunneling limit. A 4π-periodic Josephson effect (versus 2π conventional) is predicted. Critical chain lengths for observing nearly quantized conductance (within 1%) depend on the ratio t/Δ: for t/Δ = 40, approximately 344 sites (~5.5 μm); for t/Δ ~ 10, approximately 74 sites (~1.2 μm).

However, realistic disorder dramatically complicates these predictions. Das Sarma's group showed that disorder produces "trivial but quite sharp and large zero-bias Andreev tunneling peaks with conductance ~2e²/h, closely mimicking the data." The clean-system predictions become unreliable templates when disorder—an effectively infinite-dimensional nuisance parameter—is present.

---

## The fundamental asymmetry between gravitational wave and topological detection

### Why no matched filter exists for topological phases

The comparison between LIGO and Majorana detection reveals a **structural asymmetry that goes beyond engineering**. In gravitational wave astronomy, general relativity is universal: all black holes of given mass and spin produce identical waveforms to extraordinary precision. The "noise" (detector noise) is independent of the "signal" (the waveform). The parameter space is low-dimensional. These features make template matching both possible and powerful.

In condensed matter, every device is unique. Its specific disorder realization, interface quality, and geometry create a one-off system. There is no universal "Majorana waveform." The dominant source of uncertainty—disorder—directly couples to and modifies the predicted signal. The effective parameter space is infinite-dimensional. This means:

- **Prediction accuracy**: GR predicts waveforms to ~99%; topological predictions reach only qualitative or semi-quantitative agreement due to uncontrolled disorder.
- **Signal specificity**: the chirp morphology is unique to binary mergers; ZBCPs arise from multiple mechanisms.
- **Background estimation**: LIGO uses time-slides to compute false alarm rates precisely; no equivalent exists in condensed matter.

### Microsoft's topological gap protocol—the closest analogue

The topological gap protocol (Pikulin et al., arXiv:2103.12217, 2021) represents the most systematic attempt at rigorous topological detection. It uses three-terminal devices with automated scanning of the full (B, V_gate) parameter space, requires simultaneous ZBCPs at both wire ends, and validates via non-local conductance gap closing/reopening. Microsoft reported devices passing the TGP with topological gaps of **20–60 μeV** (Physical Review B 107, 245423, 2023).

However, Legg's critique (arXiv:2502.19560, February 2025) exposed significant weaknesses: the TGP's outcome depends on experimenter-chosen parameters including magnetic field range, bias voltage range, and data resolution. A device can pass the TGP with one field range and fail with a slightly narrower range that still contains the putative topological region. The definition of "topological" was weakened between the protocol and experimental papers, with one threshold change causing ~37.7% of all phase space to be classified as "topological." Physical Review B editors issued an unusual note that Microsoft's intellectual property restrictions prevented release of device parameters needed for reproduction.

Microsoft's February 2025 announcement of "Majorana 1"—an eight-qubit chip described as "the world's first quantum processor powered by a Topological Core"—went considerably beyond the peer-reviewed evidence. Nature's editorial assessment of the accompanying paper (Nature 638, 651, 2025) stated explicitly that **"the results do not represent evidence for the presence of Majorana zero modes."** The paper demonstrated interferometric single-shot parity measurement—a genuine technical achievement—but not definitive topological qubit operation. Community reception at APS March Meeting 2025 was skeptical, with estimates placing topological quantum computing "probably 20–30 years behind other platforms."

### No formal detection threshold exists in condensed matter

Condensed matter physics has **no equivalent to the 5σ standard**. The particle physics convention arose from specific features of that field: enormous datasets, the look-elsewhere effect when scanning many hypotheses, and historical false discoveries at 3–4σ. Condensed matter instead relies on qualitative agreement with theoretical phase diagrams, multiple corroborating signatures from independent measurement types, and reproducibility across devices and laboratories.

The Majorana controversy has exposed critical weaknesses in this framework: no formal false-positive-rate accounting, no correction for the look-elsewhere effect when scanning parameter spaces, publication bias toward positive results, and no blinding protocols. The field is now moving toward open data mandates (TU Delft adopted this in 2018), comprehensive parameter-space reporting, and reproducibility conferences (Pittsburgh Quantum Institute, 2024). Das Sarma's assessment (Nature Physics 19, 165, 2023) identifies disorder as the primary limiting factor and argues that **all experimental Majorana signatures to date can be explained by disorder-induced trivial states**.

---

## Conclusion: what these two threads reveal together

The juxtaposition of these two research threads illuminates a shared structural challenge. Jacobson's derivation shows that thermodynamics can determine gravitational *dynamics* given sufficient geometric input—but deriving the geometry itself remains an open frontier. The detection of topological boundary signatures shows that theory can predict qualitative features of topological phases—but achieving the quantitative specificity needed for definitive detection remains blocked by the non-universality of condensed matter systems.

In both cases, the gap between what is presupposed and what is derived is the critical scientific question. For emergent gravity, the gap is between geometric structure (presupposed) and dynamical equations (derived). For topological detection, the gap is between qualitative phase predictions (available) and device-specific quantitative templates (needed). Closing either gap would constitute a major advance: deriving Lorentzian causal structure from non-geometric principles in the first case, or achieving disorder-averaged universal predictions sufficient for matched-filter construction in the second.

The Kitaev chain's exponential splitting prediction E ~ exp(−L/ξ) is the closest topological analogue to a matched-filter template—it is a specific, parameter-dependent, measurable quantity. But it operates in a regime where the "noise" (disorder) is entangled with the "signal" (Majorana physics), unlike gravitational wave detection where detector noise is independent of the astrophysical waveform. A viable detection framework for topological signatures will likely require not a single template but a **composite multi-observable vector**—combining local and non-local conductance, shot noise, Josephson periodicity, and parity measurements—analyzed through Bayesian model comparison that marginalizes over disorder realizations. This is the direction Microsoft's topological gap protocol gestures toward, but as the ongoing controversy demonstrates, achieving the rigor of LIGO-style detection in condensed matter may require fundamentally new statistical methodology.