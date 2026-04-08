import Lake
open Lake DSL

package «geometry-of-state» where
  leanOptions := #[⟨`autoImplicit, false⟩]

require mathlib from git
  "https://github.com/leanprover-community/mathlib4" @ "v4.12.0"

-- L1: Zero-dependency layer (Int, Float, decide)
-- These files do NOT import Mathlib
@[default_target]
lean_lib «L1_Algebra» where
  srcDir := "L1_Algebra"
  roots := #[`Clifford, `CayleyDickson, `Winding, `CLHoTT]

-- L2: Classification layer (ℚ, ring, norm_num, linarith)
-- These files import Mathlib for exact rational arithmetic
lean_lib «L2_Classification» where
  srcDir := "L2_Classification"
  roots := #[`AlgebraicLadder, `Chain, `EdgeModes, `Bridge, `FWS,
             `SpinGroup, `BivectorDiscrimination, `EdgeModeBivector,
             `ER_EPR, `RunGDescend]
