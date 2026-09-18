# Reproducible teaching figures

Each script generates a PNG in `images/<module>/` relative to the repository root.
The scripts require NumPy and Matplotlib, use the noninteractive Agg backend, and
use fixed random seeds when simulating data. They make no network requests.

From the repository root, regenerate one figure:

```bash
python figures/src/solow_diagram.py
```

Or regenerate all nine figures in Bash:

```bash
for f in figures/src/*.py; do python "$f"; done
```

| Generator | Target notebook |
|---|---|
| `solow_diagram.py` | `04-Macro-Models/02_Neoclassical_Growth.ipynb` |
| `nk_determinacy_regions.py` | `04-Macro-Models/05_New_Keynesian_Models.ipynb` |
| `consumer_tangency.py` | `05-Micro-Models/01_Consumer_and_Producer_Theory.ipynb` |
| `ols_projection_geometry.py` | `06-Econometrics/01_Linear_Model_and_OLS.ipynb` |
| `did_parallel_trends.py` | `06-Econometrics/08_Difference_in_Differences.ipynb` |
| `rd_sharp_fit.py` | `06-Econometrics/06_Regression_Discontinuity.ipynb` |
| `garch_volatility_clustering.py` | `08-Time-Series/05_Volatility_Modeling_ARCH_GARCH.ipynb` |
| `amdahls_law.py` | `high_performance_python/01_High_Performance_Computing.ipynb` |
| `vfi_convergence.py` | `03-Economic-Modeling/01_Dynamic_Programming.ipynb` |

These are teaching illustrations, not empirical estimates. The RD plot fits
simulated data, so its estimated discontinuity differs from the generating
parameter. The VFI plot performs the stated number of Bellman updates with a
zero-cake boundary. The OLS diagram is a one-regressor, no-intercept example in
two-dimensional observation space.
