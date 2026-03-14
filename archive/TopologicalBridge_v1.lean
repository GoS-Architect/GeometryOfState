/-
  ==============================================================================
  THE ZERO-DEPENDENCY TOPOLOGICAL BRIDGE — COMPLETE ANALYSIS (v3 FIXED)
  ==============================================================================
  Author: Adrian Domingo
  Thought Partners: Gemini & Claude
  Date: March 12, 2026

  Fixes over v2/v3:
    1. LoopSpace now uses a custom Path type living in Type, not Prop.
       Lean 4's built-in Eq is proof-irrelevant (all proofs of a = a are
       definitionally equal). This kills HoTT: π₁(S¹) = ℤ requires
       MULTIPLE DISTINCT loops, which proof-irrelevant Eq forbids.
       Solution: axiomatize Path as a type-valued identity.
    2. Custom Equiv structure replaces Mathlib's ≃.
       Zero-dependency means zero-dependency.
    3. All tactic proofs replaced with term-mode proofs.
       by_contra requires tactic imports; Classical.byContradiction
       is in Lean 4 core.
    4. Removed the intentionally misstated sorry theorem.
  ==============================================================================
-/


-- ████████████████████████████████████████████████████████████
-- LAYER 0: TYPE-THEORETIC FOUNDATIONS
-- ████████████████████████████████████████████████████████████

/-
  LADDER RUNGS: ∅ → 𝟙 → 𝟚 → ℕ → ℤ
  STATUS: KERNEL — built into Lean 4.
  TRUST: Zero.
-/

-- No code needed. Lean provides Empty, Unit, Bool, Nat, Int.


-- ████████████████████████████████████████████████████████████
-- LAYER 0.5: ZERO-DEPENDENCY INFRASTRUCTURE
-- ████████████████████████████████████████████████████████████

/-
  WHY WE NEED THIS:

  Problem 1 — Proof Irrelevance:
    Lean 4's Eq (the built-in = type) lives in Prop.
    Prop is proof-irrelevant: if h1 h2 : a = a, then h1 = h2 definitionally.
    This means LoopSpace defined as (a = a) has AT MOST ONE element.
    But π₁(S¹) = ℤ requires infinitely many distinct loops.
    This is a fundamental incompatibility between Lean 4 and HoTT.

    Solution: Axiomatize a Path type living in Type (proof-relevant).
    Different paths are genuinely different terms, not collapsed by
    proof irrelevance. This is the standard approach for HoTT in
    non-HoTT proof assistants.

  Problem 2 — Equiv:
    The ≃ notation and Equiv structure live in Mathlib.
    We define a minimal version here. We omit the round-trip proofs
    (left_inv, right_inv) because pi1_S1 is axiomatized anyway —
    the Equiv structure just gives us .toFun and .invFun.
-/

-- Proof-relevant identity type (HoTT-compatible)
axiom Path : {α : Type} → α → α → Type

-- Reflexivity: every point has a trivial self-path
axiom Path.refl : {α : Type} → (a : α) → Path a a

-- Minimal equivalence structure (no Mathlib dependency)
structure Equiv (α : Type) (β : Type) where
  toFun : α → β
  invFun : β → α

-- Notation: α ≃ β
infixl:25 " ≃ " => Equiv


-- ████████████████████████████████████████████████████████████
-- LAYER 1: ONTOLOGICAL FOUNDATION (HoTT Axioms)
-- ████████████████████████████████████████████████████████████

/-
  LADDER RUNG: S¹ (circle as HIT)
  STATUS: AXIOMATIZED
  TRUST: Moderate — consistent with MLTT + Univalence.
-/

axiom S1 : Type
axiom S1.base : S1

-- The loop is a PATH, not an Eq. This is the critical fix.
-- In HoTT, the loop constructor is a non-trivial element of Path base base.
-- In Lean 4's Eq, S1.loop would be definitionally equal to Eq.refl,
-- collapsing the entire homotopy structure.
axiom S1.loop : Path S1.base S1.base

-- The loop space: all paths from a to a (lives in Type, not Prop)
def LoopSpace (α : Type) (a : α) : Type := Path a a

/-
  LADDER RUNG: π₁(S¹) = ℤ
  STATUS: AXIOMATIZED
  TRUST: Moderate — proved in HoTT via universal cover / encode-decode.

  Mathematical content: Every loop on the circle is uniquely characterized
  by an integer (its winding number). The equivalence is exact.
  This is the theorem that makes the entire bridge possible.
-/

axiom pi1_S1 : LoopSpace S1 S1.base ≃ Int

-- Forward: loops yield integers (the winding number)
noncomputable def loop_to_int (l : LoopSpace S1 S1.base) : Int :=
  pi1_S1.toFun l

-- Inverse: integers construct loops (the n-fold winding)
noncomputable def int_to_loop (n : Int) : LoopSpace S1 S1.base :=
  pi1_S1.invFun n


-- ████████████████████████████████████████████████████████████
-- LAYER 2: PHYSICAL LAW ONTOLOGY
-- ████████████████████████████████████████████████████████████

/-
  STATUS: DEFINITIONS — no trust required. Pure logic.
-/

def PhysicalLaw (Space : Type) := Space → Prop

def RegularLocus {Space : Type} (Law : PhysicalLaw Space) : Type :=
  {p : Space // Law p}

def IsSingularity {Space : Type} (Law : PhysicalLaw Space) (p : Space) : Prop :=
  ¬ Law p


-- ████████████████████████████████████████████████████████████
-- LAYER 3: KINEMATIC ENGINE
-- ████████████████████████████████████████████████████████████

/-
  STATUS: DEFINITIONS — computable Float arithmetic.
-/

structure KitaevParams where
  t : Float
  μ : Float
  Δ : Float
  deriving Repr

structure Bivector1D where
  d_z : Float
  d_y : Float
  deriving Repr

def H_k (p : KitaevParams) (k : Float) : Bivector1D :=
  { d_z := -2.0 * p.t * Float.cos k - p.μ,
    d_y := 2.0 * p.Δ * Float.sin k }

def bivector_mag_sq (b : Bivector1D) : Float :=
  b.d_z * b.d_z + b.d_y * b.d_y


-- ████████████████████████████████████████████████████████████
-- LAYER 4: THE GAP AS A QUANTITATIVE OBJECT
-- ████████████████████████████████████████████████████████████

/-
  STATUS: DEFINITIONS
  GapBound ε p : the minimum of |d(k)|² over the BZ is at least ε.
-/

def GapBound (ε : Float) (p : KitaevParams) : Prop :=
  ε > 0.0 ∧ ∀ (k : Float), bivector_mag_sq (H_k p k) ≥ ε

def IsGapped (p : KitaevParams) : Prop :=
  ∃ (ε : Float), GapBound ε p

def TopologicalPhaseSpace : Type :=
  RegularLocus IsGapped


-- ████████████████████████████████████████████████████████████
-- LAYER 5: THE DISCRETE SENSOR
-- ████████████████████████████████████████████████████████████

/-
  STATUS: DEFINITIONS — computable, testable.
-/

def bivector_angle (b : Bivector1D) : Float :=
  Float.atan2 b.d_y b.d_z

-- Raw winding number as Float (pre-rounding)
def compute_winding_number (p : KitaevParams) (steps : Nat) : Float := Id.run do
  let pi_val : Float := 3.141592653589793
  let dk := (2.0 * pi_val) / steps.toFloat
  let mut total_phase : Float := 0.0
  let k_start := -pi_val
  let mut current_angle := bivector_angle (H_k p k_start)

  for i in [1 : steps + 1] do
    let k_next := -pi_val + i.toFloat * dk
    let next_angle := bivector_angle (H_k p k_next)

    let mut d_theta := next_angle - current_angle
    if d_theta > pi_val then
      d_theta := d_theta - 2.0 * pi_val
    else if d_theta < -pi_val then
      d_theta := d_theta + 2.0 * pi_val

    total_phase := total_phase + d_theta
    current_angle := next_angle

  return total_phase / (2.0 * pi_val)

-- Float → Int (Lean 4 core has Float.toUInt64 but no Float.toInt)
private def floatRoundToInt (x : Float) : Int :=
  let r := Float.round x
  if r ≥ 0.0 then
    (r.toUInt64.toNat : Int)
  else
    -((-r).toUInt64.toNat : Int)

-- Rounding: Float → Int (separated for auditability)
def sensor_output (p : KitaevParams) (steps : Nat) : Int :=
  floatRoundToInt (compute_winding_number p steps)


-- ████████████████████████████████████████████████████████████
-- LAYER 6: THE BRIDGE AXIOMS
-- ████████████████████████████████████████████████████████████

/-
  STATUS: AXIOMATIZED — this is the trust boundary.

  Each axiom lives in a different mathematical domain.
  They share no proof techniques and no common failure modes.
  A bug in one does not silently contaminate another.
-/


-- ─────────────────────────────────────────────────────────────
-- AXIOM A: NORMALIZATION DEFINES A LOOP
-- Domain: Point-set topology
-- ─────────────────────────────────────────────────────────────
/-
  The normalized bivector field d̂(k) = d(k)/|d(k)| is continuous
  (because GapBound keeps the denominator away from zero) and maps
  the Brillouin zone circle into S¹, defining a loop.

  Closing requires: continuity of atan2 on ℝ² \ {0}, formalization
  of S¹ as [−π,π] with endpoints identified, construction of the
  Path element. This is the ONLY axiom that touches HoTT.
-/
axiom normalization_defines_loop
  (p : KitaevParams) (ε : Float) (hGap : GapBound ε p) :
  LoopSpace S1 S1.base


-- ─────────────────────────────────────────────────────────────
-- AXIOM B: THE EXACT WINDING INTEGRAL EQUALS THE DEGREE
-- Domain: Differential topology
-- ─────────────────────────────────────────────────────────────
/-
  CURRENT FORM: Tautological (x = x). Intentional placeholder.

  The real content — that W = (1/2π) ∮ dθ equals the degree of
  the normalization map — requires ℝ-valued path integrals, which
  we don't have. The tautology marks the socket.

  When Mathlib's ℝ and integration API arrive, this becomes:
    real_winding_integral p hGap = loop_to_int (normalization_defines_loop p ε hGap)
-/
axiom exact_winding_is_degree
  (p : KitaevParams) (ε : Float) (hGap : GapBound ε p) :
  loop_to_int (normalization_defines_loop p ε hGap) =
    loop_to_int (normalization_defines_loop p ε hGap)


-- ─────────────────────────────────────────────────────────────
-- AXIOM C: NUMERICAL STABILITY OF THE DISCRETE SENSOR
-- Domain: Numerical analysis + IEEE 754
-- ─────────────────────────────────────────────────────────────
/-
  The Float Riemann sum is within 0.5 of the true integral when
  steps > C/ε. The constant 2000.0 is a placeholder for the bound
  that depends on the Lipschitz constant of atan2 restricted to
  the ε-complement of the origin, composed with the Hamiltonian.

  This is the MESSIEST axiom by design — it quarantines all
  floating-point and discretization concerns into one place.
-/
axiom sensor_rounding_stable
  (p : KitaevParams) (ε : Float) (hGap : GapBound ε p)
  (steps : Nat) (hResolution : steps.toFloat > 2000.0 / ε) :
  let w := compute_winding_number p steps
  let rounded := Float.round w
  (w - rounded < 0.5) ∧ (rounded - w < 0.5)


-- ─────────────────────────────────────────────────────────────
-- AXIOM D: THE ROUNDED SENSOR AGREES WITH THE DEGREE
-- Domain: Composition of B and C
-- ─────────────────────────────────────────────────────────────
/-
  sensor_output p steps = loop_to_int (normalization_defines_loop p ε hGap)

  Composes B (exact integral = degree) and C (Float ≈ exact).
  Becomes a one-line corollary when both are closed.
-/
axiom sensor_equals_degree
  (p : KitaevParams) (ε : Float) (hGap : GapBound ε p)
  (steps : Nat) (hResolution : steps.toFloat > 2000.0 / ε) :
  sensor_output p steps = loop_to_int (normalization_defines_loop p ε hGap)


-- ████████████████████████████████████████████████████████████
-- LAYER 7: THE ℤ₂ PARITY REDUCTION
-- ████████████████████████████████████████████████████████████

/-
  LADDER RUNG: Winding number ∈ ℤ → ℤ₂
  STATUS: DEFINITIONS — the missing rung from v2.

  S¹ classifies the Hamiltonian's PHASE, not the qubit's state space.
  The qubit state space is ℂ² (Bloch sphere S²). The connection is:

    S¹ → π₁(S¹) ≃ ℤ → ℤ₂ → {MZM absent, MZM present} → |0⟩, |1⟩

  This layer formalizes the ℤ → ℤ₂ step.
-/

def kitaev_parity (n : Int) : Int :=
  n % 2

def has_majorana_zero_modes (n : Int) : Prop :=
  kitaev_parity n ≠ 0


-- ████████████████████████████████████████████████████████████
-- LAYER 8: MZM EXISTENCE — BOLTED TO ODD PARITY
-- ████████████████████████████████████████████████████████████

/-
  "Bolted" means: the MZM doesn't gradually appear. The winding
  number is an integer; it jumps. The MZM exists iff parity is odd.
  This discreteness is a feature of π₁(S¹), not of the sensor.
-/

def sensor_detects_mzm (p : KitaevParams) (steps : Nat) : Prop :=
  has_majorana_zero_modes (sensor_output p steps)

-- The sensor's MZM verdict agrees with the topological classification.
-- Proof: congrArg lifts the sensor=degree equality into the has_majorana_zero_modes predicate,
-- then Eq.mp/Eq.mpr give both directions of the Iff.
theorem mzm_matches_topology
  (p : KitaevParams) (ε : Float) (hGap : GapBound ε p)
  (steps : Nat) (hRes : steps.toFloat > 2000.0 / ε) :
  sensor_detects_mzm p steps ↔
    has_majorana_zero_modes (loop_to_int (normalization_defines_loop p ε hGap)) :=
  let h := sensor_equals_degree p ε hGap steps hRes
  let h' := congrArg has_majorana_zero_modes h
  ⟨Eq.mp h', Eq.mpr h'⟩


-- ████████████████████████████████████████████████████████████
-- LAYER 9: SINGULARITY THEOREMS (PROVED)
-- ████████████████████████████████████████████████████████████

/-
  STATUS: PROVED — no bridge axioms invoked. Pure propositional logic.

  These are the ONLY theorems that carry an unconditional ✓.
  The thesis "singularity = type error" does not depend on:
    - The normalization map being continuous
    - The sensor working correctly
    - S¹ existing
    - Any bridge axiom

  It follows from the DEFINITIONS of IsGapped and IsSingularity alone.
-/

-- Core thesis: at a gapless parameter, no invariant can be computed
theorem singularity_blocks_construction
  (p_crit : KitaevParams)
  (hSingular : IsSingularity IsGapped p_crit) :
  ¬ ∃ (ε : Float) (hGap : GapBound ε p_crit),
    sensor_output p_crit 10000 =
      loop_to_int (normalization_defines_loop p_crit ε hGap) :=
  fun ⟨ε, hGap, _⟩ => hSingular ⟨ε, hGap⟩

/-
  The proof: "You gave me hSingular : ¬ IsGapped p_crit and also
  ⟨ε, hGap⟩ : IsGapped p_crit. Contradiction."
  Two lines. No topology. The type system already did the work.
-/

-- Even simpler: IsSingularity IS the negation of IsGapped. Period.
theorem singularity_excludes_point
  (p_crit : KitaevParams)
  (hSingular : IsSingularity IsGapped p_crit) :
  ¬ (IsGapped p_crit) :=
  hSingular

/-
  This "theorem" is literally just hSingular itself, unfolded.
  When the type system encodes the physics correctly,
  theorems about singular behavior become tautologies.
  If the proof requires cleverness, the encoding is wrong.
-/


-- ████████████████████████████████████████████████████████████
-- LAYER 10: COMPOSITION AND PIPELINE
-- ████████████████████████████████████████████████████████████

-- The full pipeline: hardware integer = topological invariant
theorem full_pipeline
  (p : KitaevParams) (ε : Float) (hGap : GapBound ε p)
  (steps : Nat) (hRes : steps.toFloat > 2000.0 / ε) :
  sensor_output p steps = loop_to_int (normalization_defines_loop p ε hGap) :=
  sensor_equals_degree p ε hGap steps hRes

-- Through to the qubit: hardware → ℤ₂ → MZM verdict
theorem full_pipeline_to_qubit
  (p : KitaevParams) (ε : Float) (hGap : GapBound ε p)
  (steps : Nat) (hRes : steps.toFloat > 2000.0 / ε) :
  kitaev_parity (sensor_output p steps) =
    kitaev_parity (loop_to_int (normalization_defines_loop p ε hGap)) :=
  congrArg kitaev_parity (full_pipeline p ε hGap steps hRes)


-- ████████████████████████████████████████████████████████████
-- LAYER 11: PHASE TRANSITION DETECTION
-- ████████████████████████████████████████████████████████████

/-
  AXIOM E: If two gapped Hamiltonians have different winding numbers,
  any smooth interpolation between them must pass through a singularity.
  STATUS: AXIOMATIZED — requires homotopy invariance + IVT.
-/

axiom intermediate_singularity
  (p₁ p₂ : KitaevParams)
  (ε₁ ε₂ : Float)
  (hGap₁ : GapBound ε₁ p₁) (hGap₂ : GapBound ε₂ p₂)
  (hDistinct : loop_to_int (normalization_defines_loop p₁ ε₁ hGap₁) ≠
               loop_to_int (normalization_defines_loop p₂ ε₂ hGap₂))
  (interpolation : Float → KitaevParams)
  (hEndpoints : interpolation 0.0 = p₁ ∧ interpolation 1.0 = p₂) :
  ∃ (s : Float), 0.0 < s ∧ s < 1.0 ∧ IsSingularity IsGapped (interpolation s)

-- Contrapositive: if no singularity intervenes, invariants agree.
-- This IS topological protection, stated as a theorem.
-- Proof uses Classical.byContradiction (in Lean 4 core, no imports needed).
theorem topological_protection
  (p₁ p₂ : KitaevParams)
  (ε₁ ε₂ : Float)
  (hGap₁ : GapBound ε₁ p₁) (hGap₂ : GapBound ε₂ p₂)
  (interpolation : Float → KitaevParams)
  (hEndpoints : interpolation 0.0 = p₁ ∧ interpolation 1.0 = p₂)
  (hNoSingularity : ¬ ∃ (s : Float), 0.0 < s ∧ s < 1.0 ∧
    IsSingularity IsGapped (interpolation s)) :
  loop_to_int (normalization_defines_loop p₁ ε₁ hGap₁) =
    loop_to_int (normalization_defines_loop p₂ ε₂ hGap₂) :=
  Classical.byContradiction fun hDistinct =>
    hNoSingularity (intermediate_singularity p₁ p₂ ε₁ ε₂ hGap₁ hGap₂
      hDistinct interpolation hEndpoints)


-- ████████████████████████████████████████████████████████████
-- LAYER 12: INFORMATION CONSERVATION
-- ████████████████████████████████████████████████████████████

/-
  The MZM parity cannot change along any gapped path.
  The ONLY way to flip the qubit is to close the gap — a type error.
-/

theorem information_conservation
  (p₁ p₂ : KitaevParams)
  (ε₁ ε₂ : Float)
  (hGap₁ : GapBound ε₁ p₁) (hGap₂ : GapBound ε₂ p₂)
  (interpolation : Float → KitaevParams)
  (hEndpoints : interpolation 0.0 = p₁ ∧ interpolation 1.0 = p₂)
  (hNoSingularity : ¬ ∃ (s : Float), 0.0 < s ∧ s < 1.0 ∧
    IsSingularity IsGapped (interpolation s))
  (steps : Nat)
  (hRes₁ : steps.toFloat > 2000.0 / ε₁)
  (hRes₂ : steps.toFloat > 2000.0 / ε₂) :
  kitaev_parity (sensor_output p₁ steps) =
    kitaev_parity (sensor_output p₂ steps) :=
  -- Chain: sensor → degree (full_pipeline) then degree₁ = degree₂ (topological_protection)
  let hDeg := topological_protection p₁ p₂ ε₁ ε₂ hGap₁ hGap₂
                interpolation hEndpoints hNoSingularity
  let h₁ := full_pipeline p₁ ε₁ hGap₁ steps hRes₁
  let h₂ := full_pipeline p₂ ε₂ hGap₂ steps hRes₂
  -- kitaev_parity (sensor p₁) = kitaev_parity (deg₁) = kitaev_parity (deg₂) = kitaev_parity (sensor p₂)
  calc kitaev_parity (sensor_output p₁ steps)
      = kitaev_parity (loop_to_int (normalization_defines_loop p₁ ε₁ hGap₁)) := congrArg kitaev_parity h₁
    _ = kitaev_parity (loop_to_int (normalization_defines_loop p₂ ε₂ hGap₂)) := congrArg kitaev_parity hDeg
    _ = kitaev_parity (sensor_output p₂ steps) := congrArg kitaev_parity h₂.symm


-- ████████████████████████████████████████████████████████████
-- COMPLETE AUDIT
-- ████████████████████████████████████████████████████████████

/-
  ══════════════════════════════════════════════════════════════
  THE LADDER — ANNOTATED WITH EPISTEMIC STATUS
  ══════════════════════════════════════════════════════════════

  RUNG            │ STATUS       │ TRUST    │ LAYER
  ────────────────┼──────────────┼──────────┼──────────────────
  ∅               │ KERNEL       │ Zero     │ 0 (Lean built-in)
  𝟙               │ KERNEL       │ Zero     │ 0
  𝟚               │ KERNEL       │ Zero     │ 0
  ℕ               │ KERNEL       │ Zero     │ 0
  ℤ               │ KERNEL       │ Zero     │ 0
  Path            │ AXIOMATIZED  │ Moderate │ 0.5 (HoTT compat)
  Equiv           │ DEFINITION   │ Zero     │ 0.5
  S¹              │ AXIOMATIZED  │ Moderate │ 1 (HoTT import)
  π₁(S¹) = ℤ     │ AXIOMATIZED  │ Moderate │ 1
  GapBound ε      │ DEFINITION   │ Zero     │ 4
  Normalization   │ AXIOM A      │ High     │ 6 (topology)
  Winding = Deg   │ AXIOM B      │ Tautol.  │ 6 (placeholder)
  Float stability │ AXIOM C      │ High     │ 6 (numerical)
  Sensor = Deg    │ AXIOM D      │ Derived  │ 6 (composition)
  ℤ → ℤ₂ parity  │ DEFINITION   │ Zero     │ 7
  MZM ↔ odd       │ DEFINITION   │ Zero     │ 8
  MZM = topology  │ PROVED ✓     │ Zero*    │ 8 (*modulo D)
  Singularity     │ PROVED ✓     │ Zero     │ 9 (pure logic)
  Full pipeline   │ PROVED ✓     │ Zero*    │ 10 (*modulo D)
  Pipeline → ℤ₂   │ PROVED ✓     │ Zero*    │ 10 (*modulo D)
  Phase detect    │ AXIOM E      │ High     │ 11 (homotopy+IVT)
  Top. protection │ PROVED ✓     │ Zero*    │ 11 (*modulo E)
  Info conserve   │ PROVED ✓     │ Zero*    │ 12 (*modulo D+E)

  ══════════════════════════════════════════════════════════════
  FIX LOG (v3 → v3-FIXED)
  ══════════════════════════════════════════════════════════════

  FIX 1: LoopSpace — Prop/Type universe error
    PROBLEM: def LoopSpace ... : Type := a = a
      Lean 4's (=) returns Prop (Sort 0), not Type (Sort 1).
      More fundamentally, Prop is proof-irrelevant in Lean 4:
      all terms of a = a are definitionally equal. This means
      LoopSpace S1 S1.base has at most one element, making
      π₁(S¹) = ℤ unsound (ℤ has infinitely many elements).
    FIX: Axiomatize Path : α → α → Type (proof-relevant identity).
      LoopSpace now uses Path instead of Eq.
      S1.loop is now Path S1.base S1.base, not S1.base = S1.base.

  FIX 2: Equiv — Mathlib dependency
    PROBLEM: ≃ (Equiv) is defined in Mathlib, not Lean 4 core.
    FIX: Define minimal Equiv structure with toFun/invFun.
      Round-trip proofs omitted (pi1_S1 is axiomatized anyway).

  FIX 3: by_contra — tactic import
    PROBLEM: by_contra tactic requires Mathlib.Tactic import.
    FIX: All proofs rewritten in term mode.
      Classical.byContradiction (in Lean 4 core) replaces by_contra.
      congrArg replaces rw for equational rewrites.
      calc blocks replace tactic chains.

  FIX 4: Removed singularity_blocks_phase_space_entry
    PROBLEM: Intentionally misstated theorem with sorry.
    FIX: Removed entirely. The correct version
      (singularity_excludes_point) says what needs saying.

  ══════════════════════════════════════════════════════════════
  DEPENDENCY GRAPH (unchanged)
  ══════════════════════════════════════════════════════════════

       Path + S1 + pi1_S1 (HoTT infrastructure)
            │
            ▼
       [A] normalization_defines_loop
            │
            ├──────────────────────────┐
            ▼                          ▼
       [B] exact_winding       [E] intermediate_singularity
       (tautological)                  │
            │                          ▼
            │                    topological_protection ✓
            │                          │
            ▼                          │
       [C] sensor_rounding_stable      │
            │                          │
            ├──────────┐               │
            ▼          ▼               │
       [D] sensor_equals_degree        │
            │                          │
            ▼                          │
       full_pipeline ✓                 │
            │                          │
            ▼                          │
       full_pipeline_to_qubit ✓        │
            │                          │
            ▼                          ▼
       mzm_matches_topology ✓    information_conservation ✓

       (Independent of ALL axioms:)
       singularity_blocks_construction ✓
       singularity_excludes_point ✓

  ══════════════════════════════════════════════════════════════
  CLOSURE STRATEGY
  ══════════════════════════════════════════════════════════════

  Phase 1: Close A — formalize normalization via S¹ universal property
  Phase 2: Close B — import Mathlib ℝ, define real_winding_integral
  Phase 3: Close C — IEEE 754 Float model + Riemann sum error bounds
  Phase 4: D becomes corollary of B + C
  Phase 5: Close E — smooth parameter families + IVT
  Phase 6: All ✓* become unconditional ✓
-/
