#!/usr/bin/env python3
"""README for figures/src — executable Matplotlib figure generators (WP-7).

Each script in this directory builds one figure used by the curriculum and
writes it into `images/<module>/<name>.png` relative to the repository root.
Scripts are:

- deterministic (fixed RNG seeds; no network, no filesystem inputs)
- headless (`matplotlib.use("Agg")`)
- standalone: runnable with any Python that has matplotlib + numpy

    # regenerate a single figure
    python figures/src/solow_diagram.py

    # regenerate every figure
    for f in figures/src/*.py; do python "$f"; done   (see run_all.sh)

Figures marked "illustrative" visualize a concept with chosen parameters;
they are teaching aids, not empirical results. Empirical-style plots
(e.g. rd_sharp_fit) simulate data from the stated DGP with a fixed seed so
the picture is exactly reproducible.

Index (script -> lecture wired):
  solow_diagram.py              -> 04-Macro/02_Neoclassical_Growth (sec 1.1)
  nk_determinacy_regions.py     -> 04-Macro/05_New_Keynesian (policy rule)
  consumer_tangency.py          -> 05-Micro/01_Consumer_Producer (duality)
  ols_projection_geometry.py    -> 06-Econometrics/01_OLS (theory)
  did_parallel_trends.py        -> 06-Econometrics/08_DiD (sec 1)
  rd_sharp_fit.py               -> 06-Econometrics/06_RD (sec 1)
  garch_volatility_clustering.py-> 08-Time-Series/05_ARCH_GARCH (stylized facts)
  amdahls_law.py                -> high_performance_python/01_HPC (Amdahl)
  vfi_convergence.py            -> 03-Economic-Modeling/01_DP (VFI section)
"""
