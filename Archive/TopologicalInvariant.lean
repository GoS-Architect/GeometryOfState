namespace GeometryOfState.TopologicalInvariant

-- ============================================================
-- 1. Real numbers with safe division
-- ============================================================
axiom Real'       : Type
axiom Real'.zero  : Real'
axiom Real'.one   : Real'
axiom Real'.pi    : Real'
axiom Real'.add   : Real' → Real' → Real'
axiom Real'.sub   : Real' → Real' → Real'
axiom Real'.mul   : Real' → Real' → Real'
axiom Real'.neg   : Real' → Real'

-- Nonzero predicate — the gap condition lives here
axiom IsNonzero   : Real' → Prop
axiom IsNonzero.one : IsNonzero Real'.one

-- SAFE division: denominator must be proven nonzero
axiom Real'.div   : Real' → (r : Real') → IsNonzero r → Real'

instance : Add Real'  := ⟨Real'.add⟩
instance : Sub Real'  := ⟨Real'.sub⟩
instance : Mul Real'  := ⟨Real'.mul⟩
instance : Neg Real'  := ⟨Real'.neg⟩
instance : OfNat Real' 0 := ⟨Real'.zero⟩
instance : OfNat Real' 1 := ⟨Real'.one⟩

-- ============================================================
-- 2. Bivector and Rotor
-- ============================================================
structure Bivector where
  xy : Real'
  yz : Real'
  zx : Real'

structure Rotor where
  s  : Real'
  xy : Real'
  yz : Real'
  zx : Real'

def bivector_sq (B : Bivector) : Real' :=
  B.xy * B.xy + B.yz * B.yz + B.zx * B.zx

-- IsGapped: the Hamiltonian bivector has nonzero magnitude
def IsGappedAt (B : Bivector) : Prop :=
  IsNonzero (bivector_sq B)

-- ============================================================
-- 3. Safe bivector inversion
-- The gap proof is carried in the TYPE — no silent singularity
-- ============================================================
def bivector_inv (B : Bivector) (h : IsGappedAt B) : Bivector :=
  { xy := Real'.neg (Real'.div B.xy (bivector_sq B) h)
    yz := Real'.neg (Real'.div B.yz (bivector_sq B) h)
    zx := Real'.neg (Real'.div B.zx (bivector_sq B) h) }

-- The singularity is now a TYPE ERROR:
-- bivector_inv B  requires proof that |B|² ≠ 0
-- At gap closing, this proof DOES NOT EXIST
-- Therefore bivector_inv CANNOT BE CALLED at the singularity ✓

-- ============================================================
-- 4. Bivector geometric product (unchanged — correct)
-- ============================================================
def bivector_mul (B1 B2 : Bivector) : Rotor :=
  { s  := Real'.neg (B1.xy * B2.xy + B1.yz * B2.yz + B1.zx * B2.zx)
    xy := B1.yz * B2.zx - B1.zx * B2.yz
    yz := B1.zx * B2.xy - B1.xy * B2.zx
    zx := B1.xy * B2.yz - B1.yz * B2.xy }

-- ============================================================
-- 5. Brillouin zone and derivative
-- ============================================================
axiom BrillouinZone : Type
axiom deriv_k (H : BrillouinZone → Bivector) : BrillouinZone → Bivector

-- A Hamiltonian is globally gapped if gapped at every k
def IsGapped (H : BrillouinZone → Bivector) : Prop :=
  ∀ k : BrillouinZone, IsGappedAt (H k)

-- ============================================================
-- 6. Winding integrand — now requires gap proof
-- ============================================================
def winding_integrand
    (H : BrillouinZone → Bivector)
    (hGap : IsGapped H)
    (k : BrillouinZone) : Real' :=
  let B_inv  := bivector_inv (H k) (hGap k)  -- gap proof used here!
  let dB_dk  := deriv_k H k
  let rate   := bivector_mul B_inv dB_dk
  rate.yz

-- ============================================================
-- 7. Integration
-- ============================================================
axiom integral_BZ (f : BrillouinZone → Real') : Real'

-- ============================================================
-- 8. Continuous winding number — gap required
-- ============================================================
def continuous_winding_number
    (H   : BrillouinZone → Bivector)
    (hGap : IsGapped H) : Real' :=
  let two_pi := Real'.mul (Real'.add 1 1) Real'.pi
  Real'.div
    (integral_BZ (winding_integrand H hGap))
    two_pi
    (by sorry)  -- Honest Sorry: 2π ≠ 0 requires Real' axioms

-- ============================================================
-- 9. Quantization — gap forces integer value
-- ============================================================

-- Use consistent Nat' from Layer 3
inductive Nat' : Type | z : Nat' | s : Nat' → Nat'

inductive Int' : Type
  | pos     : Nat' → Int'   -- consistent with GeometryOfState.Int'
  | negSucc : Nat' → Int'

-- Honest Sorry 1 (spectral gap → integer quantization)
axiom exact_quantization :
    (H    : BrillouinZone → Bivector) →
    (hGap : IsGapped H) →            -- gap is REQUIRED
    Int'                              -- returns exact integer

def topological_invariant
    (H    : BrillouinZone → Bivector)
    (hGap : IsGapped H) : Int' :=
  exact_quantization H hGap

-- ============================================================
-- 10. The singularity theorem — final form
-- ============================================================

-- Attempting to compute the invariant at a gapless point
-- is a TYPE ERROR: you cannot supply (hGap : IsGapped H)

theorem gapless_invariant_undefined
    (H       : BrillouinZone → Bivector)
    (hGapless : ¬ IsGapped H) :
    -- There is no way to call topological_invariant on H
    ¬ ∃ (hGap : IsGapped H), True := by
  intro ⟨hGap, _⟩
  exact hGapless hGap
-- The singularity is not a runtime error.
-- It is the absence of a proof term.
-- TYPE ERROR. QED. ✓

end GeometryOfState.TopologicalInvariant