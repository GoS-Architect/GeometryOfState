/-
  SpinGroup.lean
  Geometry of State — Bivector Discrimination Pipeline (File 1 of 3)

  GoS-Architect | github.com/GoS-Architect
  March 2026

  EPISTEMIC STATUS: Target PROVED (zero sorry)
  DEPENDENCY: GeometryOfState.lean §1–§2 (Cl(2,0) basis, geometric product, rotors)

  This file formalizes Spin(2,0) and Pin(2,0) as the even and full Clifford
  groups acting by sandwich products on Cl(2,0). It provides the group-theoretic
  infrastructure that BivectorDiscrimination.lean depends on.

  MATHEMATICAL CONTENT:
    Cl(2,0) is 4-dimensional: {1, e₁, e₂, e₁₂}
    Even subalgebra (grade 0 + grade 2): {a + b·e₁₂ | a,b ∈ ℚ}
    Spin(2,0) = {R in even subalgebra | R·R† = 1}
    Pin(2,0)  = {R in full algebra    | R·R† = ±1}

    Key fact: The even subalgebra of Cl(2,0) is isomorphic to ℂ
    and is therefore COMMUTATIVE. This is the structural reason
    the bivector e₁₂ is invariant under Spin(2,0) conjugation.
-/

-- ============================================================
-- §1. Cl(2,0) over ℚ — Exact Arithmetic for Decidable Proofs
-- ============================================================

/-- Clifford algebra Cl(2,0) over the rationals.
    4-dimensional: scalar (grade 0), e₁ and e₂ (grade 1), e₁₂ (grade 2).
    Using ℚ instead of Float ensures all equalities are decidable. -/
structure Cl2Q where
  s  : ℚ    -- scalar component (grade 0)
  x₁ : ℚ    -- e₁ component (grade 1)
  x₂ : ℚ    -- e₂ component (grade 1)
  b  : ℚ    -- e₁₂ component (grade 2)
  deriving Repr, DecidableEq

namespace Cl2Q

-- Basis elements
def one   : Cl2Q := ⟨1, 0, 0, 0⟩
def e₁    : Cl2Q := ⟨0, 1, 0, 0⟩
def e₂    : Cl2Q := ⟨0, 0, 1, 0⟩
def e₁₂   : Cl2Q := ⟨0, 0, 0, 1⟩

-- ============================================================
-- §2. Geometric Product
-- ============================================================

/-- The geometric product of Cl(2,0).
    Multiplication table:
      e₁·e₁ = +1,  e₂·e₂ = +1     (signature (2,0))
      e₁·e₂ = e₁₂, e₂·e₁ = -e₁₂   (anticommutativity of basis vectors)
      e₁₂·e₁₂ = -1                  (bivector squares to -1 in Cl(2,0))
      e₁·e₁₂ = e₂,  e₁₂·e₁ = -e₂
      e₂·e₁₂ = -e₁, e₁₂·e₂ = e₁   -/
def mul (a b : Cl2Q) : Cl2Q :=
  ⟨ a.s * b.s + a.x₁ * b.x₁ + a.x₂ * b.x₂ - a.b * b.b,
    a.s * b.x₁ + a.x₁ * b.s - a.x₂ * b.b + a.b * b.x₂,
    a.s * b.x₂ + a.x₁ * b.b + a.x₂ * b.s - a.b * b.x₁,
    a.s * b.b + a.x₁ * b.x₂ - a.x₂ * b.x₁ + a.b * b.s ⟩

instance : Mul Cl2Q := ⟨mul⟩

/-- Addition for the algebra -/
def add (a b : Cl2Q) : Cl2Q :=
  ⟨a.s + b.s, a.x₁ + b.x₁, a.x₂ + b.x₂, a.b + b.b⟩

instance : Add Cl2Q := ⟨add⟩

/-- Scalar multiplication -/
def smul (k : ℚ) (a : Cl2Q) : Cl2Q :=
  ⟨k * a.s, k * a.x₁, k * a.x₂, k * a.b⟩

/-- Negation -/
def neg (a : Cl2Q) : Cl2Q :=
  ⟨-a.s, -a.x₁, -a.x₂, -a.b⟩

instance : Neg Cl2Q := ⟨neg⟩

-- ============================================================
-- §3. Reversal (Dagger) and Grade Involution
-- ============================================================

/-- The reversal (†) operation: reverses the order of basis vector products.
    grade 0: unchanged, grade 1: unchanged, grade 2: negated.
    For a rotor R, R† is its Clifford conjugate. -/
def rev (a : Cl2Q) : Cl2Q :=
  ⟨a.s, a.x₁, a.x₂, -a.b⟩

/-- Grade involution (hat): negates odd-grade components.
    grade 0: unchanged, grade 1: negated, grade 2: unchanged. -/
def involute (a : Cl2Q) : Cl2Q :=
  ⟨a.s, -a.x₁, -a.x₂, a.b⟩

/-- Clifford conjugate: composition of reversal and grade involution.
    grade 0: unchanged, grade 1: negated, grade 2: negated. -/
def conj (a : Cl2Q) : Cl2Q :=
  ⟨a.s, -a.x₁, -a.x₂, -a.b⟩

-- ============================================================
-- §4. Grade Projections
-- ============================================================

/-- Grade-0 projection (scalar part) -/
def grade0 (a : Cl2Q) : Cl2Q := ⟨a.s, 0, 0, 0⟩

/-- Grade-1 projection (vector part) -/
def grade1 (a : Cl2Q) : Cl2Q := ⟨0, a.x₁, a.x₂, 0⟩

/-- Grade-2 projection (bivector part) -/
def grade2 (a : Cl2Q) : Cl2Q := ⟨0, 0, 0, a.b⟩

/-- Even subalgebra projection (grade 0 + grade 2) -/
def evenPart (a : Cl2Q) : Cl2Q := ⟨a.s, 0, 0, a.b⟩

/-- Odd part projection (grade 1) -/
def oddPart (a : Cl2Q) : Cl2Q := ⟨0, a.x₁, a.x₂, 0⟩

/-- Predicate: element is in the even subalgebra -/
def IsEven (a : Cl2Q) : Prop := a.x₁ = 0 ∧ a.x₂ = 0

/-- Predicate: element is a pure vector (grade 1) -/
def IsVector (a : Cl2Q) : Prop := a.s = 0 ∧ a.b = 0

/-- Predicate: element is a pure bivector (grade 2) -/
def IsBivector (a : Cl2Q) : Prop := a.s = 0 ∧ a.x₁ = 0 ∧ a.x₂ = 0

-- ============================================================
-- §5. Sandwich Product
-- ============================================================

/-- The sandwich product: R · x · R†
    This is the fundamental action of the Spin/Pin groups on Cl(2,0). -/
def sandwich (R x : Cl2Q) : Cl2Q :=
  mul (mul R x) (rev R)

-- ============================================================
-- §6. Spin(2,0) and Pin(2,0) Predicates
-- ============================================================

/-- Norm squared: a · a† (scalar part).
    For the product a · rev(a) in Cl(2,0), only the scalar part matters
    for the group condition. -/
def normSq (a : Cl2Q) : ℚ :=
  a.s * a.s + a.b * a.b + a.x₁ * a.x₁ + a.x₂ * a.x₂

/-- An element is in Spin(2,0) if it is even and has unit norm.
    Spin(2,0) = {R ∈ Cl⁺(2,0) | R·R† = 1} -/
def IsSpin (R : Cl2Q) : Prop :=
  IsEven R ∧ (R.s * R.s + R.b * R.b = 1)

/-- An element is in Pin(2,0) if it has unit norm (even or odd).
    Pin(2,0) = {R ∈ Cl(2,0) | R·R† = ±1} -/
def IsPin (R : Cl2Q) : Prop :=
  normSq R = 1

-- ============================================================
-- §7. Fundamental Verification: Basis Element Properties
-- ============================================================

/-- e₁₂ is in the even subalgebra -/
theorem e₁₂_is_even : IsEven e₁₂ := by
  unfold IsEven e₁₂
  exact ⟨rfl, rfl⟩

/-- e₁ is a pure vector -/
theorem e₁_is_vector : IsVector e₁ := by
  unfold IsVector e₁
  exact ⟨rfl, rfl⟩

/-- e₂ is a pure vector -/
theorem e₂_is_vector : IsVector e₂ := by
  unfold IsVector e₂
  exact ⟨rfl, rfl⟩

/-- e₁₂ is a pure bivector -/
theorem e₁₂_is_bivector : IsBivector e₁₂ := by
  unfold IsBivector e₁₂
  exact ⟨rfl, rfl, rfl⟩

-- ============================================================
-- §8. Fundamental Products — rfl-verified
-- ============================================================

/-- e₁ · e₁ = 1 (signature +) -/
theorem e₁_sq : e₁ * e₁ = one := by native_decide

/-- e₂ · e₂ = 1 (signature +) -/
theorem e₂_sq : e₂ * e₂ = one := by native_decide

/-- e₁₂ · e₁₂ = -1 (bivector squares to minus one in Cl(2,0)) -/
theorem e₁₂_sq : e₁₂ * e₁₂ = neg one := by native_decide

/-- e₁ · e₂ = e₁₂ -/
theorem e₁_e₂ : e₁ * e₂ = e₁₂ := by native_decide

/-- e₂ · e₁ = -e₁₂ (anticommutativity) -/
theorem e₂_e₁ : e₂ * e₁ = neg e₁₂ := by native_decide

-- ============================================================
-- §9. Even Subalgebra Commutativity
-- ============================================================

/-- The product of two even elements is even.
    This is the closure property of the even subalgebra. -/
theorem even_mul_even (a b : Cl2Q) (ha : IsEven a) (hb : IsEven b) :
    IsEven (a * b) := by
  obtain ⟨ha1, ha2⟩ := ha
  obtain ⟨hb1, hb2⟩ := hb
  unfold IsEven Mul.mul mul
  simp [ha1, ha2, hb1, hb2]
  ring_nf
  exact ⟨by ring, by ring⟩

/-- CRITICAL THEOREM: The even subalgebra of Cl(2,0) is commutative.
    For any two even elements a = (a.s, 0, 0, a.b) and b = (b.s, 0, 0, b.b),
    their geometric product commutes: a * b = b * a.

    This is the structural reason bivector invariance holds:
    Spin(2,0) rotors are even, e₁₂ is even, and even × even commutes.

    Proof: Direct computation. The even subalgebra {a + b·e₁₂} is
    isomorphic to ℂ (with e₁₂ playing the role of i), and ℂ is commutative. -/
theorem even_subalgebra_comm (a b : Cl2Q) (ha : IsEven a) (hb : IsEven b) :
    a * b = b * a := by
  obtain ⟨ha1, ha2⟩ := ha
  obtain ⟨hb1, hb2⟩ := hb
  unfold Mul.mul mul
  simp [ha1, ha2, hb1, hb2]
  constructor <;> ring

-- ============================================================
-- §10. Reversal Properties
-- ============================================================

/-- Reversal of an even element: only the bivector component is negated -/
theorem rev_even (a : Cl2Q) (ha : IsEven a) :
    rev a = ⟨a.s, 0, 0, -a.b⟩ := by
  obtain ⟨ha1, ha2⟩ := ha
  unfold rev
  simp [ha1, ha2]

/-- For the unit bivector, its reversal is its negation -/
theorem rev_e₁₂ : rev e₁₂ = neg e₁₂ := by native_decide

/-- For any basis vector, reversal is identity -/
theorem rev_e₁ : rev e₁ = e₁ := by native_decide
theorem rev_e₂ : rev e₂ = e₂ := by native_decide

end Cl2Q

-- ============================================================
-- §11. Computational Verification
-- ============================================================

section Computation

open Cl2Q

/-- Example rotor: 45° rotation, R = (√2/2)(1 + e₁₂)
    For decidability we use the exact rational rotor at specific angles.
    The rotor R = (3/5) + (4/5)e₁₂ satisfies R·R† = 1 exactly. -/
def R_example : Cl2Q := ⟨3/5, 0, 0, 4/5⟩

/-- Verify R_example is in Spin(2,0): even and unit norm -/
theorem R_example_is_spin : Cl2Q.IsSpin R_example := by
  unfold Cl2Q.IsSpin Cl2Q.IsEven R_example
  norm_num

/-- Verify sandwich product of e₁₂ by R_example equals e₁₂.
    This is a concrete instance of the core discrimination theorem. -/
theorem sandwich_e₁₂_by_R_example :
    Cl2Q.sandwich R_example Cl2Q.e₁₂ = Cl2Q.e₁₂ := by native_decide

/-- Verify sandwich product of e₁ by R_example does NOT equal e₁.
    The vector is rotated — this models ABS behavior. -/
theorem sandwich_e₁_by_R_example_ne :
    Cl2Q.sandwich R_example Cl2Q.e₁ ≠ Cl2Q.e₁ := by native_decide

end Computation
