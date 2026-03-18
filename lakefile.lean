import Lake
open Lake DSL

package «geometry-of-state» where
  -- Zero external dependencies

@[default_target]
lean_lib «L1_Algebra» where
  srcDir := "L1_Algebra"
  roots := #[`Clifford, `CayleyDickson, `Winding, `CLHoTT]

lean_lib «L2_Classification» where
  srcDir := "L2_Classification"
  roots := #[`AlgebraicLadder, `KitaevChain, `EdgeModes, `Bridge, `FWS]
