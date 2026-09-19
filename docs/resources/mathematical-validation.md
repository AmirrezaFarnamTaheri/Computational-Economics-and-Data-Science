# Mathematical Review and Validation Policy

The course uses three different kinds of evidence. They must never be collapsed into a single “verified” label.

## Evidence levels

| Level | What it establishes | What it does **not** establish |
|---|---|---|
| **Structure-complete** | The exposition contains the expected assumptions, statement, derivation/proof working, and interpretation. | That every mathematical step is correct. |
| **Mathematically reviewed** | A named reviewer has checked the actual derivation or proof against its assumptions and recorded review evidence. | That numerical code implements the result correctly in every case. |
| **Numerically validated** | Executable tests, limiting cases, counterexamples, or independent calculations support a computational claim. | A general mathematical proof. |

The structural scanner in `scripts/audit_proofs.py` is deliberately limited to the first level. Its output is triage evidence, not a proof certificate.

## Release rule

A page may say that a derivation or theorem is **mathematically reviewed** only when its claim entry in `ci/mathematical_claims.json` has:

1. `mathematical_review.status = "reviewed"`;
2. a non-empty reviewer identity;
3. a non-empty review-evidence reference; and
4. the relevant assumptions stated in the source.

A computational claim may say **numerically validated** only when its ledger entry points to an executable regression or independent numerical check. Numerical evidence must include a failure case or limiting-case check when one is material to the claim.

CI validates the ledger schema and rejects unsupported “reviewed” or “numerically validated” labels. CI cannot create independent mathematical sign-off by itself.

## High-risk review priorities

The claim ledger covers the repository areas where an apparently successful calculation can otherwise produce a materially false teaching conclusion: dynamic-programming kernels, general-equilibrium residuals, option-pricing bounds, annualization/frequency conversion, statistical-test interpretation, theorem proofs, machine-learning preprocessing, and unit conversions.

When a derivation changes, its review evidence is invalidated unless the reviewer checks the changed lines again. When an implementation changes, its numerical evidence must be rerun. The two forms of evidence are intentionally independent.

## Reviewer checklist

For a mathematical derivation, record the assumptions, domains, boundary cases, existence/uniqueness conditions, and the exact step where each assumption is used. For a numerical implementation, compare against an independent formula or implementation where possible, test invalid inputs explicitly, report residuals or invariants, and preserve a counterexample that failed before the fix.

The ledger is a release-control mechanism, not a claim that every line of mathematics has been independently peer reviewed. Items without independent sign-off remain clearly marked as such.
