import Lake
open Lake DSL

package «geometry-of-state» where
  -- default options

@[default_target]
lean_lib «GeometryOfState» where
  srcDir := "."

lean_exe «geometry_of_state» where
  root := `GeometryOfState
