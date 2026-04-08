/-
  ==============================================================================
  RUNG DESCENT: The Algebraic Ladder and Topological Phase Classification
  ==============================================================================
  Author: Adrian Domingo & Claude (Anthropic)
  Project: Geometry of State
  Date: March 2026

  Epistemic Status:
    PROVED    — Definitions follow established mathematics (Bott periodicity,
                Altland-Zirnbauer classification, Kitaev chain)
    DEMONSTRATED — Type-level encoding is faithful to the classification
    CONJECTURED  — That 5/7 curvature boundary constitutes a rung descent

  Dependencies: None (zero-dependency, consistent with GoS architecture)
  ==============================================================================

  THE CORE IDEA:

  The division algebras ℝ → ℂ → ℍ → 𝕆 lose one algebraic property at each
  step. The tenfold way (Altland-Zirnbauer classification) of topological
  phases is indexed by Clifford algebra periodicity — the SAME ladder.

  A topological phase transition occurs when the effective Hamiltonian
  crosses from one symmetry class to another. At that boundary, the
  topological invariant changes value. The boundary mode (e.g., MZM)
  exists because the proof of triviality that works on one side FAILS
  on the other.

  The MZM is the witness of a type error at the rung boundary.
  ==============================================================================
-/

-- ============================================================
-- §1. THE ALGEBRAIC LADDER
-- ============================================================
-- Each rung is a normed division algebra.
-- Ascending index = descending structure.

inductive Rung : Type where
  | real       : Rung  -- ℝ  Cl(0,0)
  | complex    : Rung  -- ℂ  Cl(0,1)
  | quaternion : Rung  -- ℍ  Cl(0,2)
  | octonion   : Rung  -- 𝕆  (non-associative; beyond Clifford)
  deriving DecidableEq, Repr

-- What algebraic properties survive at each rung
structure AlgebraicStructure where
  ordered      : Bool
  commutative  : Bool
  associative  : Bool
  deriving DecidableEq, Repr

def structureAt : Rung → AlgebraicStructure
  | .real       => ⟨true,  true,  true⟩   -- all three
  | .complex    => ⟨false, true,  true⟩   -- lost ordering
  | .quaternion => ⟨false, false, true⟩   -- lost commutativity
  | .octonion   => ⟨false, false, false⟩  -- lost associativity

-- What is sacrificed at each descent
inductive Sacrifice : Type where
  | ordering      : Sacrifice  -- ℝ → ℂ : can no longer compare
  | commutativity : Sacrifice  -- ℂ → ℍ : order of multiplication matters
  | associativity : Sacrifice  -- ℍ → 𝕆 : grouping of multiplication matters
  deriving DecidableEq, Repr

def descent : Rung → Option (Sacrifice × Rung)
  | .real       => some (.ordering,      .complex)
  | .complex    => some (.commutativity, .quaternion)
  | .quaternion => some (.associativity, .octonion)
  | .octonion   => none  -- floor of the ladder

-- PROVED: Each descent loses exactly one property
theorem descent_loses_one (r : Rung) (s : Sacrifice) (r' : Rung)
    (h : descent r = some (s, r')) :
    let above := structureAt r
    let below := structureAt r'
    -- Exactly one field flips from true to false
    (above.ordered      = true  ∧ below.ordered      = false ∧
     above.commutative  = below.commutative ∧
     above.associative  = below.associative) ∨
    (above.commutative  = true  ∧ below.commutative  = false ∧
     above.ordered      = below.ordered ∧
     above.associative  = below.associative) ∨
    (above.associative  = true  ∧ below.associative  = false ∧
     above.ordered      = below.ordered ∧
     above.commutative  = below.commutative) := by
  cases r <;> simp [descent] at h <;> obtain ⟨_, rfl⟩ := h <;>
    simp [structureAt] <;> decide


-- ============================================================
-- §2. THE TENFOLD WAY (Altland-Zirnbauer Classification)
-- ============================================================
-- Ten symmetry classes of free-fermion Hamiltonians.
-- T = time-reversal, C = particle-hole, S = chiral.
-- The real classes cycle with period 8 = Bott periodicity
-- = Clifford algebra periodicity.

inductive AZClass : Type where
  -- Complex classes (no T or C constraint on sign)
  | A    : AZClass   -- unitary, no symmetry
  | AIII : AZClass   -- chiral unitary
  -- Real classes (8, cycling with period 8)
  | AI   : AZClass   -- T²=+1
  | BDI  : AZClass   -- T²=+1, C²=+1, S
  | D    : AZClass   -- C²=+1              ← KITAEV CHAIN
  | DIII : AZClass   -- T²=-1, C²=+1, S
  | AII  : AZClass   -- T²=-1
  | CII  : AZClass   -- T²=-1, C²=-1, S
  | C    : AZClass   -- C²=-1
  | CI   : AZClass   -- T²=+1, C²=-1, S
  deriving DecidableEq, Repr

-- Symmetry content of each class
structure DiscreteSymmetries where
  hasTimeReversal  : Option Bool  -- None = absent, some true = T²=+1, some false = T²=-1
  hasParticleHole  : Option Bool  -- None = absent, some true = C²=+1, some false = C²=-1
  hasChiral        : Bool
  deriving DecidableEq, Repr

def symmetriesOf : AZClass → DiscreteSymmetries
  | .A    => ⟨none,       none,       false⟩
  | .AIII => ⟨none,       none,       true⟩
  | .AI   => ⟨some true,  none,       false⟩
  | .BDI  => ⟨some true,  some true,  true⟩
  | .D    => ⟨none,       some true,  false⟩
  | .DIII => ⟨some false, some true,  true⟩
  | .AII  => ⟨some false, none,       false⟩
  | .CII  => ⟨some false, some false, true⟩
  | .C    => ⟨none,       some false, false⟩
  | .CI   => ⟨some true,  some false, true⟩


-- ============================================================
-- §3. TOPOLOGICAL INVARIANTS BY DIMENSION
-- ============================================================
-- The periodic table of topological insulators/superconductors.
-- In each spatial dimension d, each AZ class has a topological
-- invariant type: trivial (0), ℤ, or ℤ₂.

inductive TopInvariant : Type where
  | trivial : TopInvariant   -- no topological distinction
  | Z       : TopInvariant   -- ℤ-valued (winding number, Chern number)
  | Z2      : TopInvariant   -- ℤ/2-valued (fermion parity, Kane-Mele)
  deriving DecidableEq, Repr

-- The classification in d=1 (the Kitaev chain dimension)
def classifyDim1 : AZClass → TopInvariant
  | .A    => .trivial
  | .AIII => .Z         -- ℤ winding number (SSH model)
  | .AI   => .trivial
  | .BDI  => .Z         -- ℤ winding number
  | .D    => .Z2        -- ℤ/2 fermion parity ← KITAEV
  | .DIII => .Z2        -- ℤ/2 (helical Majorana)
  | .AII  => .trivial
  | .CII  => .Z         -- ℤ
  | .C    => .trivial
  | .CI   => .trivial

-- The classification in d=2 (quantum Hall, Chern insulators)
def classifyDim2 : AZClass → TopInvariant
  | .A    => .Z         -- ℤ Chern number (IQHE)
  | .AIII => .trivial
  | .AI   => .trivial
  | .BDI  => .trivial
  | .D    => .Z         -- ℤ Chern number (chiral p-wave)
  | .DIII => .Z2        -- ℤ/2
  | .AII  => .Z2        -- ℤ/2 (QSHE, Kane-Mele)
  | .CII  => .trivial
  | .C    => .Z         -- ℤ
  | .CI   => .trivial


-- ============================================================
-- §4. THE KITAEV CHAIN — CLASS D IN d=1
-- ============================================================

def kitaevClass : AZClass := .D

-- PROVED: Kitaev chain has Z₂ classification in 1D
theorem kitaev_is_Z2 : classifyDim1 kitaevClass = .Z2 := rfl

-- PROVED: Kitaev chain has particle-hole symmetry, no time-reversal
theorem kitaev_has_PH : (symmetriesOf kitaevClass).hasParticleHole = some true := rfl
theorem kitaev_no_TR  : (symmetriesOf kitaevClass).hasTimeReversal = none := rfl

-- The Z₂ invariant: fermion parity
-- In a Kitaev chain, this is winding number mod 2
inductive FermionParity : Type where
  | even : FermionParity  -- trivial phase, MZMs paired
  | odd  : FermionParity  -- topological phase, unpaired MZM
  deriving DecidableEq, Repr

def parityFromWinding (w : Int) : FermionParity :=
  if w % 2 = 0 then .even else .odd

-- PROVED: winding 0 is trivial, winding 1 is topological
theorem winding_zero_trivial : parityFromWinding 0 = .even := rfl
theorem winding_one_topological : parityFromWinding 1 = .odd := rfl


-- ============================================================
-- §5. THE PHASE BOUNDARY — WHERE THE TYPE ERROR LIVES
-- ============================================================
-- A domain wall separates two regions with different topological
-- invariants. The MZM exists at the wall because the proof of
-- triviality valid on one side has no corresponding proof on
-- the other.

structure DomainWall where
  classLeft   : AZClass
  classRight  : AZClass
  dim         : Nat
  deriving Repr

-- Classify by dimension
def classifyAtDim (d : Nat) : AZClass → TopInvariant
  | c => match d with
    | 1 => classifyDim1 c
    | 2 => classifyDim2 c
    | _ => .trivial  -- we only encode d=1,2 for now

-- Does a domain wall support a boundary mode?
def wallIsTopological (wall : DomainWall) : Prop :=
  classifyAtDim wall.dim wall.classLeft ≠ classifyAtDim wall.dim wall.classRight

-- The wall is trivial if both sides have the same invariant
def wallIsTrivial (wall : DomainWall) : Prop :=
  classifyAtDim wall.dim wall.classLeft = classifyAtDim wall.dim wall.classRight

-- PROVED: These are complementary
theorem wall_trichotomy (wall : DomainWall) :
    wallIsTopological wall ∨ wallIsTrivial wall := by
  unfold wallIsTopological wallIsTrivial
  by_cases h : classifyAtDim wall.dim wall.classLeft = classifyAtDim wall.dim wall.classRight
  · exact Or.inr h
  · exact Or.inl h

-- The critical construction: a domain wall between trivial and
-- class D in d=1
def kitaevEdge : DomainWall := {
  classLeft  := .AI    -- trivial in d=1 (normal metal / vacuum)
  classRight := .D     -- topological (Kitaev chain)
  dim        := 1
}

-- PROVED: The Kitaev edge is topological
theorem kitaev_edge_is_topological : wallIsTopological kitaevEdge := by
  unfold wallIsTopological kitaevEdge classifyAtDim classifyDim1
  decide


-- ============================================================
-- §6. RUNG DESCENT AS PHASE TRANSITION
-- ============================================================
-- The central construction: descending the algebraic ladder
-- corresponds to crossing an AZ class boundary. The MZM lives
-- at the rung transition.

-- The Bott clock: real AZ classes in cyclic order (period 8)
-- AI → BDI → D → DIII → AII → CII → C → CI → AI → ...
def bottSucc : AZClass → AZClass
  | .AI   => .BDI
  | .BDI  => .D
  | .D    => .DIII
  | .DIII => .AII
  | .AII  => .CII
  | .CII  => .C
  | .C    => .CI
  | .CI   => .AI
  -- Complex classes are their own 2-cycle
  | .A    => .AIII
  | .AIII => .A

-- PROVED: Bott periodicity — 8 steps returns to start (real classes)
theorem bott_period_8_AI   : (bottSucc ∘ bottSucc ∘ bottSucc ∘ bottSucc ∘
                              bottSucc ∘ bottSucc ∘ bottSucc ∘ bottSucc) .AI = .AI := rfl

-- The rung descent: stepping from one AZ class to the next on the
-- Bott clock, and checking whether the topological invariant changes
structure RungTransition where
  above : AZClass      -- class before descent
  below : AZClass      -- class after descent (= bottSucc above)
  dim   : Nat
  step  : below = bottSucc above  -- proof it's a genuine Bott step

-- Does the rung transition change the topological invariant?
def rungChangesInvariant (rt : RungTransition) : Prop :=
  classifyAtDim rt.dim rt.above ≠ classifyAtDim rt.dim rt.below

-- The BDI → D transition in d=1: ℤ → ℤ/2
-- This is a rung descent that changes invariant type
def bdi_to_d : RungTransition := {
  above := .BDI
  below := .D
  dim   := 1
  step  := rfl
}

-- PROVED: BDI → D changes invariant in d=1 (ℤ → ℤ₂)
theorem bdi_d_changes : rungChangesInvariant bdi_to_d := by
  unfold rungChangesInvariant bdi_to_d classifyAtDim classifyDim1
  decide

-- PROVED: The invariant types on each side
theorem bdi_is_Z  : classifyDim1 .BDI = .Z  := rfl
theorem d_is_Z2   : classifyDim1 .D   = .Z2 := rfl


-- ============================================================
-- §7. THE 5/7 BOUNDARY — CONJECTURED RUNG DESCENT
-- ============================================================
--
-- CONJECTURED: The curvature sign change at a 5/7 Stone-Wales
-- boundary, with appropriate superconducting pairing, constitutes
-- a transition from a trivial to a topological phase in class D.
--
-- What this requires (the open computation):
--   1. Write the tight-binding + BdG Hamiltonian on the buckled lattice
--   2. Show pentagonal region has classifyDim1 = .trivial
--   3. Show heptagonal region has classifyDim1 = .Z2
--   4. The 5/7 interface is then a DomainWall with wallIsTopological
--
-- The golden angle screw selects a 1D path through the 2D lattice.
-- Along that path, the effective 1D Hamiltonian is a Kitaev chain
-- with geometry-modulated hopping parameters.
--
-- The falsifiable claim: |μ| < 2t(x) at each site x along the
-- screw path, where t(x) depends on local bond length (curvature).

-- Curvature sign at a lattice vertex
inductive CurvatureSign : Type where
  | positive : CurvatureSign  -- pentagon: κ > 0
  | zero     : CurvatureSign  -- hexagon:  κ = 0
  | negative : CurvatureSign  -- heptagon: κ < 0
  deriving DecidableEq, Repr

-- The conjectured mapping (NOT proved — this is the gap)
-- This is a placeholder for the Hamiltonian computation
noncomputable def conjecturedClass : CurvatureSign → AZClass
  | .positive => .AI   -- trivial in d=1 (CONJECTURED)
  | .zero     => .AI   -- trivial in d=1
  | .negative => .D    -- topological in d=1 (CONJECTURED)

-- IF the conjecture holds, THEN the 5/7 wall is topological
-- This is a conditional theorem: honest about its dependency
theorem if_conjecture_then_MZM
    (h_pos : conjecturedClass .positive = .AI)
    (h_neg : conjecturedClass .negative = .D) :
    classifyAtDim 1 (conjecturedClass .positive) ≠
    classifyAtDim 1 (conjecturedClass .negative) := by
  rw [h_pos, h_neg]
  unfold classifyAtDim classifyDim1
  decide


-- ============================================================
-- §8. CONNECTING TO GoS: Cl(2,0) AS THE KITAEV ALGEBRA
-- ============================================================
--
-- In the existing GeometryOfState.lean:
--   • Cl(2,0) encodes the Kitaev Hamiltonian as a bivector field
--   • The gap condition requires a proof witness (IsGappedAt)
--   • At the phase transition, the witness vanishes → type error
--
-- This file adds the classification layer:
--   • The TYPE of topological invariant depends on the AZ class
--   • The AZ class depends on which symmetries the Hamiltonian has
--   • A rung descent changes the AZ class → changes invariant type
--   • At the boundary, neither classification applies → type error
--
-- The singularity IS the rung boundary.
-- The MZM IS the boundary mode.
-- The type error IS the phase transition.
-- These are three descriptions of one object.

-- Summary: what is proved, what is open
--
-- PROVED (rfl):
--   • kitaev_is_Z2           : Class D in d=1 has ℤ/2 invariant
--   • kitaev_edge_is_topological : Trivial-to-D wall supports boundary mode
--   • bdi_d_changes          : BDI→D rung descent changes invariant type
--   • bott_period_8_AI       : Real AZ classes have period 8
--   • descent_loses_one      : Each algebraic rung loses exactly one property
--   • winding_one_topological : w=1 gives odd fermion parity
--
-- CONJECTURED (requires Hamiltonian computation):
--   • 5/7 curvature boundary constitutes AI→D class transition
--   • Golden angle screw path satisfies |μ| < 2t(x) everywhere
--   • Resulting 1D chain has winding number 1
--
-- The gap between PROVED and CONJECTURED is one computation:
-- a tight-binding BdG Hamiltonian on a finite 5/7 lattice patch.


-- ============================================================
-- §9. VERIFICATION
-- ============================================================

#eval kitaevClass                          -- AZClass.D
#eval classifyDim1 kitaevClass             -- TopInvariant.Z2
#eval classifyDim1 .BDI                    -- TopInvariant.Z
#eval classifyDim2 .A                      -- TopInvariant.Z (quantum Hall)
#eval parityFromWinding 0                  -- FermionParity.even
#eval parityFromWinding 1                  -- FermionParity.odd
#eval structureAt .real                    -- ordered, commutative, associative
#eval structureAt .quaternion              -- not ordered, not commutative, associative
#eval descent .real                        -- some (ordering, complex)
#eval descent .octonion                    -- none (floor)
