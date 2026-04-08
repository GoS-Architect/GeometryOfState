# Geometry of State
## Thesis Document for Antithesis Preparation

**Adrian — Visual Systems Architect & Proof Engineer**  
github.com/GoS-Architect  
April 2026 · Lean 4 Formalization

---

*The compiler is the credential.*  
*The kill condition is the integrity.*  
*The retraction is the proof of honesty.*  
*The human is the purpose.*  
*The treaty is the architecture.*

---

## Purpose of This Document

This document presents the Geometry of State (GoS) architecture in thesis form — structured explicitly for adversarial review. Every major claim is stated precisely, tagged with its epistemic status, and supplied with a kill condition. The antithesis process should interrogate each claim at the level of its weakest axiom.

A thesis document is not a defense. It is a target. The goal is to present the architecture's claims with enough precision that the antithesis can identify exactly where the load-bearing assumptions sit and apply the strongest possible counter-pressure.

Operate under Glassbox constraints: no claim may inherit a higher epistemic status than its weakest dependency. The compiler has final authority on PROVED. Everything else is provisional.

---

## Architecture Overview

### The Five-File Lean Corpus

| File | Core claim | Proof status |
|------|-----------|-------------|
| `KitaevChain.lean` | IsGapped as proof obligation; type error at phase boundary | `winding_undefined_at_boundary` proven; 2 sorry in gamma lemmas |
| `TopologicalLock3D.lean` | 3D knotted filament preserves knot type below E_reconnect | 3 theorems proven, 0 sorry |
| `TopologicalComputation.lean` | Knot types as registers; read/write cycle | 4 theorems proven, 0 sorry |
| `PinnedPseudoKnot.lean` | φ-pinning enhances but cannot topologize 2D protection | 2 theorems proven; simulation confirms negative result |
| `MHDTopology.lean` | Plasma analog: quasi-topological via helicity conservation | 1 theorem proven; axiom-heavy; weakest file |

### The Protection Hierarchy

Three levels of topological protection, ordered by strength:

- **Level 3 (exact):** 3D knotted vortex filament below E_reconnect. Protection is unconditional — the only input required is the energy bound. Knot type is preserved for all time, exactly.
- **Level 2 (approximate):** 2D vortex with φ-spaced pinning lattice. Protection is conditional on vortex kinetic energy remaining below the barrier. Fails in all five simulation configurations tested.
- **Level 1 (none):** 2D vortex, no pinning. Winding number W=3 decays in all cases. The simulation confirmed this baseline.

The plasma (MHD) case is Level 3 quasi-topological: helicity conservation is exact in ideal MHD (η=0) and approximate for finite resistivity. The Lundquist number S ~ 10⁸ ensures helicity decay timescale far exceeds fusion burn time.

---

## The Core Theorems: Full Statements

### From KitaevChain.lean

#### `winding_undefined_at_boundary`

```lean
theorem winding_undefined_at_boundary (p : KitaevParams)
    (h_boundary : at_phase_boundary p) :
    ¬ ∃ (hGap : IsGapped (kitaev_bivector p)), True
```

At the phase boundary (|μ| = 2t), there exists no proof of `IsGapped`, and therefore `topological_invariant` cannot be called. The phase transition is an inhabitation failure, not a runtime error. The proof is a two-line contradiction: assume `hGap` exists, apply `phase_boundary_not_gapped` to derive `False`.

**Antithesis pressure point:** the theorem depends on the physical axioms `at_phase_boundary` and `phase_boundary_not_gapped`. Neither is proven from first principles — both encode analytic properties of the Bloch Hamiltonian. A complete formalization would replace them with proofs about trigonometric zeros.

---

### From TopologicalLock3D.lean

#### `level_three_topological_lock`

```lean
theorem level_three_topological_lock
    (state : Superfluid3D) (E_ambient : ℝ)
    (h_below : E_ambient < E_reconnect) :
    ∀ t : ℝ, t ≥ 0 →
    vortex_knot_type (evolve state E_ambient t) = vortex_knot_type state
```

Below the reconnection energy threshold, knot type is preserved for all non-negative time. The proof composes two axioms: `sub_threshold_is_isotopy` (physical) and `ambient_isotopy_preserves_knot_type` (mathematical). Three lines.

#### `trefoil_never_unknots`

```lean
theorem trefoil_never_unknots
    (state : Superfluid3D) (E_ambient : ℝ)
    (h_trefoil : vortex_knot_type state = KnotType.trefoil)
    (h_below : E_ambient < E_reconnect) :
    ∀ t : ℝ, t ≥ 0 →
    vortex_knot_type (evolve state E_ambient t) ≠ KnotType.unknot
```

Proven by contradiction using `trefoil_stays_trefoil` and `KnotType.trefoil_ne_unknot`. No sorry.

---

### From TopologicalComputation.lean

#### `read_write_cycle`

```lean
theorem read_write_cycle
    (state : Superfluid3D) (x : XPoint) (E_write E_ambient : ℝ)
    (h_write : E_write > E_reconnect)
    (h_ambient : E_ambient < E_reconnect) :
    (∃ c, vortex_knot_type (splice state x E_write) =
           knot_surgery (vortex_knot_type state) c) ∧
    (∀ t, t ≥ 0 →
      vortex_knot_type (evolve (splice state x E_write) E_ambient t) =
      vortex_knot_type (splice state x E_write))
```

The full read/write cycle: a splice above threshold implements a crossing change (WRITE), and the resulting state is preserved indefinitely below threshold (READ). This is the topological state machine in one theorem.

---

### From PinnedPseudoKnot.lean

#### `fibonacci_enhances_but_does_not_topologize`

A Fibonacci φ-lattice enhances migration barriers via `golden_ratio_anti_resonance` — the φ-spacing prevents rational resonance, a consequence of φ having maximally poor rational approximations — but does not convert energetic protection into topological protection. The protection type remains conditional.

The simulation confirms: five configurations tested (control, φ depth 5/20/50, triangular), zero retention above 12.2%. Deep pinning (depth=50) accelerated vortex migration by introducing additional energy gradients.

---

## Axiom Accounting

Every axiom in the corpus falls into one of three categories. The antithesis should classify each axiom and determine whether it can be promoted to a theorem or must remain as empirical input.

### Mathematical axioms — provable from established mathematics

| File | Axiom | Path to proof |
|------|-------|--------------|
| `TopologicalLock3D` | `ambient_isotopy_preserves_knot_type` | Theorem in knot theory; proof requires Reidemeister moves not yet formalized |
| `TopologicalLock3D` | `reconnection_reduces_unknotting` | Theorem about crossing changes; trefoil unknotting number = 1 |
| `TopologicalComputation` | knot surgery results | unlink→hopf, hopf→unlink, trefoil unknotting; all are theorems in knot theory |
| `KitaevChain` | `exact_quantization` | Degree of continuous map S¹→S¹∖{0} is an integer; requires homotopy theory not yet in Mathlib |

### Physical axioms — require experimental input

| File | Axiom | Status |
|------|-------|--------|
| `TopologicalLock3D` | `sub_threshold_is_isotopy` | Core physical claim. GP dynamics below E_reconnect is ambient isotopy. Cannot be proven from type theory alone. |
| `KitaevChain` | `topological_phase_implies_gapped` / `phase_boundary_not_gapped` | Analytic properties of the Bloch Hamiltonian bivector. Replaceable by trigonometric proofs. |
| `MHDTopology` | `woltjer_theorem`, `alfven_frozen_flux`, `taylor_preserves_helicity` | Established MHD results (1942–1974). Proofs exist in literature; not yet formalized in Lean. |

### Bridge axioms — highest risk, connect two formally distinct systems

| File | Axiom | Why it is load-bearing |
|------|-------|----------------------|
| `TopologicalComputation` | `splice_implements_surgery` | X-point reconnection in the fluid implements a crossing change in knot theory. Requires both fluid dynamics and knot theory simultaneously. |
| `KitaevChain` | `topological_implies_majorana` | Winding number ±1 implies existence of Majorana zero mode. The bulk-boundary correspondence. Most important unformalized claim in the corpus. |

Bridge axioms are the highest-risk category. They connect two formally distinct systems and require both to be true simultaneously. The antithesis should concentrate here.

---

## Epistemic Status of All Major Claims

| Claim | Status | Kill condition |
|-------|--------|---------------|
| `winding_undefined_at_boundary` | **PROVED** | None — proven from axioms, no sorry |
| `level_three_topological_lock` | **PROVED** | None — proven from axioms, no sorry |
| `trefoil_never_unknots` | **PROVED** | None — proven from axioms, no sorry |
| `read_write_cycle` | **PROVED** | None — proven from axioms, no sorry |
| `positive_noise_margin_implies_stability` | **PROVED** | None — proven from axioms, no sorry |
| 2D φ-pinning fails to preserve W=3 (simulation) | **DEMONSTRATED** | Simulation error preserving W=3 above 50% retention in any configuration |
| Taylor relaxation: energy decays faster than helicity | **DEMONSTRATED** | Physical regime where this separation fails |
| `sub_threshold_is_isotopy` (physical axiom) | **CONJECTURED** | GP simulation showing knot type change below E_reconnect |
| `splice_implements_surgery` (bridge axiom) | **CONJECTURED** | Reconnection event that does not implement a crossing change |
| `topological_implies_majorana` (bridge axiom) | **CONJECTURED** | Topological phase without localized edge mode |
| Plasma protection survives fusion burn timescale | **CONJECTURED** | S < 10⁶ in achievable stellarator geometry |
| Cubical Agda migration feasibility | **SPECULATIVE** | N/A — resource and timeline dependent |
| Full tenfold way formalization in Lean | **SPECULATIVE** | N/A — no such formalization exists anywhere |
| Literal multi-agent Socratic architecture | **SPECULATIVE** | N/A — engineering challenge, not mathematical |

---

## Open Vulnerabilities for Antithesis

These are the weakest joints in the architecture. Maximum pressure should be applied at each.

### V-1: The Two Sorry Lemmas in KitaevChain.lean

`gamma_sq` and `gamma_anticomm'` are the Clifford algebra anticommutation relations. They carry sorry. The comments correctly identify which Mathlib lemmas would close them (`iota_sq`, `weightedSumSquares` on `Finsupp.single`). Until these are proven, the MSTA layer has unverified debt. The theorems in Part C do not depend on Part B's sorry lemmas directly — but the conceptual claim that the Kitaev chain lives inside the MSTA requires them.

**Antithesis question:** do the Part C bridge axioms silently assume the content of the sorry lemmas? If so, the sorry debt is larger than declared.

### V-2: The Bridge Axioms Are Not Yet Formalizable

`splice_implements_surgery` and `topological_implies_majorana` are the most important claims in the corpus and the ones furthest from proof. They connect continuous physical dynamics to discrete mathematical structures. The formalization strategy for either is not yet determined.

**Antithesis question:** is there a principled reason to believe these bridges are formalizable at all? What would a proof of `splice_implements_surgery` require — does it demand a full formalization of vortex dynamics, or is there a topological argument that bypasses the dynamics?

### V-3: MHDTopology.lean Is Axiom-Heavy

`stellarator_fusion_stability` is proven but thin — it directly invokes `stellarator_topology_preservation`, which is itself an axiom. The file has the largest ratio of axioms to proven theorems. Several axiom bodies prove `True` as placeholders (`high_lundquist_helicity_conservation`). The mapping between superfluid and plasma is asserted rather than derived.

**Antithesis question:** does `MHDTopology.lean` contain any result that goes beyond restating known MHD physics in Lean syntax? If not, it is documentation, not formalization.

### V-4: The Zero-Mathlib Tension

The GoS architecture's epistemic design calls for zero external dependencies. `KitaevChain.lean` imports `Mathlib.LinearAlgebra.CliffordAlgebra.Basic`. This is a genuine tension, not resolved. The Glassbox methodology demands transparency about trade-offs rather than treating the zero-Mathlib principle as an unqualified virtue.

**Antithesis question:** does importing Mathlib's CliffordAlgebra infrastructure undermine the auditability claim? Is every definition and axiom in the Mathlib dependency chain visible and verified?

### V-5: The Protection Hierarchy Is Not Exhaustive

The hierarchy has three levels. Are there protection mechanisms that don't fit Level 1, 2, or 3? The anyonic protection used in actual MZM-based quantum computing (topological degeneracy, not knot topology) is not represented in the hierarchy. Is this an intentional scope decision or a gap?

### V-6: The Experimental Protocol Remains Unspecified

`TopologicalLock3D.lean` Part 9 lists experimental obligations: fabricate a system supporting 3D vortex filaments, imprint a trefoil, cool below E_reconnect, measure knot type persistence. Kleckner & Irvine (2013) demonstrated trefoil knotting in water vortices. The superfluid adaptation is not detailed.

**Antithesis question:** is the experimental protocol physically achievable with current technology? What is E_reconnect numerically for He-4 at T < 1K, and what imaging resolution is required to verify knot type persistence?

---

## Dependency Map: What Retracting What Cascades Where

| If this is retracted | Severity | Downstream effect |
|---------------------|----------|------------------|
| `sub_threshold_is_isotopy` | **CASCADE** | `level_three_topological_lock`, `trefoil_stays_trefoil`, `trefoil_never_unknots`, `read_write_cycle`, `stellarator_fusion_stability` — entire protection hierarchy collapses |
| `IsGapped` type structure (Part A) | **CASCADE** | `topological_invariant`, `kitaev_winding_number`, `winding_undefined_at_boundary` — the core type error theorem loses its foundation |
| `splice_implements_surgery` | **LOCAL** | `read_write_cycle`, `hopf_splice_exists` — computational architecture loses its write mechanism; read (lock) theorems unaffected |
| `topological_implies_majorana` | **LOCAL** | Disconnects the GoS corpus from MZM physics. All Lean theorems remain valid — they just no longer imply anything about Majorana zero modes |
| MHDTopology axioms (`woltjer`, `alfven`) | **LOCAL** | `stellarator_fusion_stability` — plasma extension retracted. Superfluid results unaffected |
| `gamma_sq` / `gamma_anticomm'` (sorry) | **CONTAINED** | MSTA layer loses its foundation. Part C bridge axioms may silently depend on this — needs audit. Parts A and B topological theorems unaffected |

---

## Recommended Antithesis Protocol

Apply the Socratic Partner constitutions in order from highest to lowest epistemic authority:

1. **Voevodsky first:** identify every claim tagged PROVED and verify the proof chain has no hidden sorry. Audit the two sorry lemmas in `KitaevChain.lean`. Determine whether Part C bridge axioms depend on their content.

2. **Dirac second:** for each physical axiom, ask what physical system instantiates it and what experiment would falsify it. `sub_threshold_is_isotopy` is the highest-priority target.

3. **Kitaev third:** perturb the assumptions. Does `level_three_topological_lock` survive if E_reconnect is not a sharp threshold but a probabilistic one? Does it survive finite-temperature corrections?

4. **Noether fourth:** for each CONJECTURED claim, ask what structural principle makes it true. If no principle can be identified, downgrade to SPECULATIVE.

5. **Grothendieck fifth:** is the language of the formalization correct? Are `KnotType`, `AmbientIsotopic`, and `XPoint` the right abstractions, or are there formalization choices that would make the bridge axioms more tractable?

6. **Cayley-Dickson sixth:** state explicitly what is sacrificed at each level of the hierarchy. Level 3 requires 3D + knotted + below threshold. What is the cost of each requirement? What is gained by relaxing each?

---

*The compiler is the credential. The kill condition is the integrity. The retraction is the proof of honesty.*

Geometry of State Research Program · github.com/GoS-Architect · April 2026
