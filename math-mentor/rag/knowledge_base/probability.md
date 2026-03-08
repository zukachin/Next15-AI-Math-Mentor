# Probability – Formulas and identities

## Basic definition
- P(A) = (number of favorable outcomes) / (number of total outcomes) when outcomes are equally likely.
- 0 ≤ P(A) ≤ 1; P(sample space) = 1; P(∅) = 0.

## Addition rule
- P(A or B) = P(A) + P(B) - P(A and B). For mutually exclusive events, P(A and B) = 0 so P(A or B) = P(A) + P(B).

## Complement
- P(not A) = P(A') = 1 - P(A).

## Conditional probability
- P(A|B) = P(A and B) / P(B), provided P(B) > 0.
- Multiplication rule: P(A and B) = P(B) · P(A|B) = P(A) · P(B|A).

## Independence
- A and B independent iff P(A and B) = P(A) · P(B), or equivalently P(A|B) = P(A) when P(B) > 0.

## Bayes’ theorem
- P(A|B) = P(B|A) · P(A) / P(B). Often use P(B) = P(B|A)P(A) + P(B|A')P(A') when applying.

# Probability – Solution templates (JEE-style)

## “Find P(A)” (single event)
1. Identify sample space and confirm equally likely if using counting.
2. Count favorable and total; P(A) = favorable / total. Or use given probabilities and rules (complement, addition).

## “Find P(A and B)” or “both”
1. Check independence; if yes, P(A and B) = P(A)·P(B).
2. If not, use P(A and B) = P(A)·P(B|A) or P(B)·P(A|B); compute the conditional from the problem.

## “Find P(A or B)”
1. Use P(A or B) = P(A) + P(B) - P(A and B). Compute P(A and B) first if needed.

## “Given B, find P(A)” (conditional)
1. Apply P(A|B) = P(A and B) / P(B). Find P(A and B) and P(B) from the problem or tree.

## “At least one” / “none”
1. P(at least one) = 1 - P(none). Often P(none) = P(A₁' and A₂' and …) = product if independent.

# Probability – Common mistakes and pitfalls

- Assuming independence without justification; independence must be stated or shown.
- Using “and” when the problem means “or” (e.g. “both” vs “at least one”).
- Wrong sample space: e.g. “two dice” means 36 outcomes, not 11; “two cards without replacement” changes denominator on second draw.
- For conditional probability, using P(A|B) = P(A and B) but then computing P(B|A) by mistake.
- Not checking 0 ≤ P ≤ 1; probabilities must sum to 1 over a partition.
- Confusing “given” order: P(A|B) is probability of A when B has already occurred.

# Probability – Domain and constraints

- All probabilities must be in [0, 1]. Sum of probabilities of all outcomes (or of a partition) = 1.
- For conditional probability, the “given” event must have P(B) > 0.
- In counting-based probability, sample space must be clearly defined and outcomes equally likely where the formula is used.
- “Without replacement” changes successive probabilities; “with replacement” keeps them independent.
