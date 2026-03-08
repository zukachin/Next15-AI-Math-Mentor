# Calculus – Limits (formulas and facts)

## Basic limits
- lim_{x→c} k = k; lim_{x→c} x = c.
- lim_{x→0} sin(x)/x = 1; lim_{x→0} (1 - cos x)/x = 0; lim_{x→0} (e^x - 1)/x = 1.
- lim_{x→∞} 1/x = 0; lim_{x→∞} (1 + 1/x)^x = e.

## Limit laws
- Sum, difference, product, quotient (denominator limit ≠ 0): limit of (f ± g), f·g, f/g is the corresponding combination of limits, provided the denominator limit is not 0.
- lim (f(x))^n = (lim f(x))^n when the limit exists.

## Indeterminate forms
- 0/0, ∞/∞, ∞ - ∞, 0·∞: try algebraic simplification, rationalization, or L’Hôpital’s rule (for 0/0 or ∞/∞).
- L’Hôpital: If lim f(x)/g(x) is 0/0 or ∞/∞, then lim f(x)/g(x) = lim f'(x)/g'(x) if the latter limit exists (same limit process).

## One-sided limits
- lim_{x→c⁺} f(x) and lim_{x→c⁻} f(x). Limit at c exists iff both one-sided limits exist and are equal.

# Calculus – Limits solution template and pitfalls

## Solution template
1. Substitute the limit point; if you get a definite value, state it.
2. If indeterminate, simplify (factor, rationalize, use standard limits like sin x/x).
3. For 0/0 or ∞/∞, consider L’Hôpital: differentiate numerator and denominator separately, then take limit.
4. State the final limit clearly.

## Common mistakes
- Using L’Hôpital when the form is not 0/0 or ∞/∞.
- Differentiating the whole fraction instead of numerator and denominator separately in L’Hôpital.
- Ignoring one-sided limits when f has a jump or undefined point at c.
- Forgetting that lim (f · g) can be 0·∞; convert to 0/0 or ∞/∞ (e.g. write f·g = f/(1/g)) then apply L’Hôpital if needed.
