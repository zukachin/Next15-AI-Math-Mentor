# Calculus – Derivatives (formulas and rules)

## Basic rules
- d/dx (x^n) = n x^(n-1) (n real, x > 0 if n not a positive integer).
- d/dx (c) = 0; d/dx (c f(x)) = c f'(x).
- Sum/difference: (f ± g)' = f' ± g'.
- Product: (f g)' = f' g + f g'.
- Quotient: (f/g)' = (f' g - f g') / g², g ≠ 0.

## Chain rule
- d/dx f(g(x)) = f'(g(x)) · g'(x). For power of a function: d/dx [u(x)]^n = n u^(n-1) · u'(x).

## Standard derivatives
- d/dx sin x = cos x; d/dx cos x = -sin x; d/dx tan x = sec² x.
- d/dx e^x = e^x; d/dx ln x = 1/x (x > 0); d/dx a^x = a^x ln a (a > 0).

## Second derivative
- f''(x) = derivative of f'(x); used for concavity and second derivative test.

# Calculus – Derivatives solution template and pitfalls

## Solution template
1. Identify which rule(s) apply (sum, product, quotient, chain).
2. Apply rules step by step; for composite functions, use chain rule from outside in.
3. Simplify the expression; state domain where derivative exists (e.g. avoid division by zero, ln of non-positive).

## Common mistakes
- Chain rule: forgetting to multiply by the “inner” derivative.
- Quotient rule: wrong order in numerator (must be f' g - f g', not f g' - f' g).
- d/dx (1/x) = -1/x², not 1/x or ln x.
- Domain: derivative of √u requires u > 0; derivative of ln u requires u > 0.
- Treating variable as constant or constant as variable when differentiating.
