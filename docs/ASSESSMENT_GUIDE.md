# Assessment and Solution Standards

This guide defines the common grading language used by the course. Notebook exercises should keep their **model-specific** checkpoints in the notebook rather than repeating this policy verbatim.

## What every strong solution must show

A complete solution should make five things inspectable:

1. **Assumptions and domain.** State the assumptions actually used, including support, admissible parameter ranges, units, timing, conditioning information, and any numerical regularity conditions.
2. **Mechanism or derivation.** Show the equation, transformation, algorithm, or causal mechanism that connects the premise to the answer. Do not replace a derivation with a library call.
3. **Independent check.** Use a limiting case, invariant, alternative estimator, residual, first-order condition, conservation condition, no-arbitrage bound, market-clearing residual, or other diagnostic that is independent of the main calculation.
4. **Interpretation.** Report the result in the units and economic/statistical meaning of the problem. Distinguish estimation error, approximation error, identification assumptions, and model misspecification.
5. **Failure analysis.** For challenge exercises, identify at least one parameterization or data condition under which the method should fail, explain why, and show how the diagnostic exposes that failure.

## Tier-specific expectations

### Conceptual
Explain the mechanism in words and equations. Name the assumption that carries the result and one case in which it does not apply.

### Applied
Produce the requested computation, show at least one intermediate checkpoint, and verify it with an independent diagnostic. Numerical answers should include units or scale and enough precision to reproduce the conclusion.

### Challenge
Compare alternatives or stress the method outside its comfortable regime. Separate changes caused by the economic/statistical assumption from changes caused by approximation, tuning, sampling, or compute budget.

### Failure-analysis challenge
Construct or analyze a concrete failure case. A strong answer includes the triggering condition, the observed symptom, the diagnostic that catches it, and the appropriate response (reject, re-specify, refine, or report uncertainty).

## Feedback and marking

Notebook-specific exercises should state their own expected objects: for example, a Bellman residual, a no-arbitrage bound, an ADF hypothesis, a market-clearing residual, a forecast baseline, or a proof step. Those local objects take precedence over generic prose here.

A suggested rubric for instructor use is:

| Dimension | Weight |
|---|---:|
| Correct setup and assumptions | 20% |
| Derivation / implementation correctness | 35% |
| Independent verification | 20% |
| Interpretation and units | 15% |
| Failure analysis / limitations | 10% |

Instructor solutions may be maintained separately when revealing full worked answers in the learner notebook would undermine the exercise.
