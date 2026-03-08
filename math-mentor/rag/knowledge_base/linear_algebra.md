# Linear algebra – Basics (JEE-style)

## Vectors (2D/3D)
- Magnitude: |v| = √(v₁² + v₂²) or √(v₁² + v₂² + v₃²).
- Dot product: u·v = u₁v₁ + u₂v₂ (+ u₃v₃ in 3D); u·v = |u||v| cos θ; perpendicular when u·v = 0.
- Cross product (3D): u × v is a vector perpendicular to both; |u × v| = |u||v| sin θ; direction by right-hand rule.

## Matrices (2×2 and basics)
- Entry a_ij: row i, column j.
- Addition/subtraction: entrywise (same dimensions).
- Scalar multiplication: multiply every entry.
- Matrix multiplication: (AB)_{ij} = row i of A · column j of B; number of columns of A = number of rows of B.

## Determinant (2×2)
- det [[a,b],[c,d]] = ad - bc. Matrix is invertible iff determinant ≠ 0.

## Inverse (2×2)
- If A = [[a,b],[c,d]] and det A = ad - bc ≠ 0, then A⁻¹ = (1/det A) [[d,-b],[-c,a]].
- A A⁻¹ = A⁻¹ A = I (identity).

## Solution template (linear system / matrix equation)
1. Write system as Ax = b (matrix form).
2. Find det A; if det A ≠ 0, unique solution x = A⁻¹ b.
3. If det A = 0, check consistency (e.g. row reduction); either no solution or infinitely many.

# Linear algebra – Common mistakes and pitfalls

- Matrix multiplication is not commutative: AB ≠ BA in general.
- Determinant: for 2×2, ad - bc (order matters: “first diagonal minus second”), not (a+d)-(b+c).
- Inverse exists only when determinant ≠ 0; do not divide by zero.
- Dot product gives a scalar; cross product (3D) gives a vector.
- When solving Ax = b, dimensions must match: A is m×n, x is n×1, b is m×1.
