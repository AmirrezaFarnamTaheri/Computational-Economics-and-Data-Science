# Economic Modeling (Dynamic Programming) — Bibliography

> Pathway in one line: from Bellman's operator to Rust's buses to your own structural model.

## Reading pathway

1. Stokey & Lucas — the recursive formalism done with full rigor.
2. Judd — the numerical toolbox in economic language.
3. Miranda & Fackler — the code-first companion (CompEcon).
4. Rust (1996) — how to actually implement and estimate a DP model.
5. Puterman or Bertsekas — when you need MDP theory in full.

## Seminal

- **Bellman (1957).** *Dynamic Programming.* Princeton University Press. — The
  principle of optimality and the operator viewpoint behind every value
  function iteration in this curriculum.
- **Howard (1960).** *Dynamic Programming and Markov Processes.* MIT Press. —
  Policy iteration: still the fastest converging workhorse for discrete DP.
- **Blackwell (1965).** *Discounted Dynamic Programming.* Annals of
  Mathematical Statistics. — The discounting lemma that makes Bellman
  operators contractions in one line.

## Modern

- **Judd (1998).** *Numerical Methods in Economics.* MIT Press. — The bridge
  text between numerical analysis and economic application.
- **Miranda & Fackler (2002).** *Applied Computational Economics and Finance.*
  MIT Press. — Implementable algorithms with code; CompEcon is its toolkit.
- **Rust (1996).** *Numerical Dynamic Programming in Economics.* Handbook of
  Computational Economics, Vol. 1. — Practical wisdom on discretization,
  interpolation, and convergence criteria; the source of this module's
  checklists.
- **Adda & Cooper (2003).** *Dynamic Economics.* MIT Press. — Applied
  discrete-choice dynamics for economists.

## Theoretical

- **Stokey & Lucas (1989).** *Recursive Methods in Economic Dynamics* (with
  Prescott). Harvard University Press. — The theorem-proof scaffolding
  (existence, monotone comparative statics) assumed by every applied lecture.
- **Puterman (1994).** *Markov Decision Processes.* Wiley. — MDP theory in
  full generality.
- **Bertsekas (2017).** *Dynamic Programming and Optimal Control*, 4th ed.
  Athena Scientific. — Modern synthesis including approximate DP.
