-- Project: The Digital Triplet
-- Architect: Adrian Domingo
-- Date: January 19, 2026
-- Pillar I: Geometric Algebra (Lightweight Version)

/--
  We define a "Geometric Number" structure manually.
  This represents your i_hat (the bivector).
-/
structure GeometricNumber where
  real_part : Int
  imaginary_part : Int

/--
  We define how to MULTIPLY two Geometric Numbers.
  This is the rule of your universe:
  (a + bi) * (c + di) = (ac - bd) + (ad + bc)i
-/
def mul (a b : GeometricNumber) : GeometricNumber :=
  { real_part := a.real_part * b.real_part - a.imaginary_part * b.imaginary_part,
    imaginary_part := a.real_part * b.imaginary_part + a.imaginary_part * b.real_part }

-- We define "i_hat" as having 0 real part and 1 imaginary part.
def i_hat : GeometricNumber := { real_part := 0, imaginary_part := 1 }

-- We define "-1" as having -1 real part and 0 imaginary part.
def negative_one : GeometricNumber := { real_part := -1, imaginary_part := 0 }

/--
  THE ADRIAN DOMINGO THEOREM:
  Prove that i_hat * i_hat equals -1.
-/
theorem verify_triplet_core : mul i_hat i_hat = negative_one := by
  -- We tell the computer to just calculate it.
  rfl
