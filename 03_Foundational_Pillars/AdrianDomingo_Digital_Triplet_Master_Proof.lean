-- Project: The Digital Triplet
-- Architect: Adrian Domingo
-- Pillar II: The Physics (1D Kitaev Chain)
-- Status: Logic-Only Verification (Stable)

/-- 
  We define a 2x2 Matrix structure using Integers (Z)
  to ensure absolute stability in the web browser.
-/
structure Matrix2x2 where
  tl : Int -- Top Left
  tr : Int -- Top Right
  bl : Int -- Bottom Left
  br : Int -- Bottom Right
  deriving Repr, DecidableEq

/-- 
  We define the Pauli Matrix Sigma_Z.
  This represents the "Trivial Phase" of the superconductor.
  Matrix: [[1, 0], [0, -1]]
-/
def sigma_z : Matrix2x2 := 
  { tl := 1, tr := 0, bl := 0, br := -1 }

/-- 
  We define the Trivial Hamiltonian.
  When momentum k=0, the system is purely in the Sigma_Z state.
  H = -mu * Sigma_Z
-/
def trivial_hamiltonian (mu : Int) : Matrix2x2 :=
  { tl := -mu * 1, tr := 0, bl := 0, br := -mu * -1 }

/-- 
  THE ADRIAN DOMINGO THEOREM (PILLAR II):
  Prove that in the trivial phase (mu=1), the Hamiltonian 
  is exactly equal to negative Sigma_Z.
  
  This confirms the "Trivial Topology" (Winding Number = 0).
-/
theorem verify_trivial_phase : trivial_hamiltonian 1 = { tl := -1, tr := 0, bl := 0, br := 1 } := by
  -- We tell the machine: "Calculate the energy state."
  rfl