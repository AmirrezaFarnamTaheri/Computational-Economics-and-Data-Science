# High-Performance Python — Bibliography

> Pathway in one line: performance is a property of algorithms and memory, not of hope.

## Reading pathway

1. Sutter (2005) — why the free lunch ended.
2. Amdahl (1967) & Gustafson (1988) — the two speedup laws.
3. Harris et al. (2020) — NumPy's design, from its authors.
4. Lam, Pitrou & Seibert (2015) — how Numba's JIT actually works.
5. Hennessy & Patterson — the hardware model underneath the roofline.

## Seminal

- **Moore (1965).** *Cramming More Components onto Integrated Circuits.*
  Electronics. — The extrapolation that set four decades of expectations.
- **Amdahl (1967).** *Validity of the Single Processor Approach...* AFIPS
  Conference. — The serial-fraction bound on speedup.
- **Knuth (1974).** *Structured Programming with go to Statements.* Computing
  Surveys. — Source of "premature optimization is the root of all evil";
  profile before you tune.
- **Gustafson (1988).** *Reevaluating Amdahl's Law.* Communications of the ACM.
  — Scaled speedup: what happens when the problem grows with the hardware.

## Modern

- **Sutter (2005).** *The Free Lunch Is Over.* Dr. Dobb's Journal. — Clock
  speeds plateau; cores multiply; software must go concurrent. The module's
  founding premise.
- **Harris et al. (2020).** *Array Programming with NumPy.* Nature. — The
  design paper for the array model this curriculum runs on.
- **Lam, Pitrou & Seibert (2015).** *Numba: A LLVM-Based Python JIT Compiler.*
  Proceedings of SciPy. — The `@njit` pipeline explained by its builders.

## Theoretical

- **Williams, Waterman & Patterson (2009).** *Roofline: An Insightful Visual
  Performance Model.* Communications of the ACM. — Compute-bound vs
  bandwidth-bound in one picture.
- **Hennessy & Patterson (2019).** *Computer Architecture: A Quantitative
  Approach*, 6th ed. Morgan Kaufmann. — The hardware reality that the roofline
  summarizes.
