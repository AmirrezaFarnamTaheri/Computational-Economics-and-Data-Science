# Targeted Runtime Notebook Smoke Report

The repository-wide notebook audit is static by design. This runtime layer executes the numerically modified and newly added high-risk notebooks in a CPU/offline-capable environment. It does **not** claim that every optional GPU, browser, network, TensorFlow, or PyTorch path in all 129 notebooks was executed.

| Notebook | Result |
|---|---|
| `03-Economic-Modeling/01_Dynamic_Programming.ipynb` | PASS |
| `06-Econometrics/07_Synthetic_Control_Methods.ipynb` | PASS |
| `04-Macro-Models/08_Continuous_Time_Macro_HJB.ipynb` | PASS |
| `05-Micro-Models/07_BLP_Demand_Estimation.ipynb` | PASS |
| `06-Econometrics/13_Modern_Causal_Frontiers_SDID.ipynb` | PASS |
| `08-Time-Series/07_Nonlinear_Time_Series_and_Particle_Filters.ipynb` | PASS |
| `09-Finance/08_Hawkes_Processes_and_Market_Impact.ipynb` | PASS |
| `10-Specialized-Models/04_Climate_Macro_Integrated_Assessment_DICE.ipynb` | PASS |
| `high_performance_python/04_GPU_Acceleration_with_CuPy.ipynb` | PASS (no-GPU fallback path) |
| `Appendix/T4_Replication_Card_Krueger_1994.ipynb` | PASS |
| `Appendix/T5_Replication_Fama_French_Five_Factor.ipynb` | PASS |

The first aggregate smoke wrapper hit the outer command-time limit after SDID had already completed and written its executed notebook. The remaining notebooks were then executed in smaller batches; all eleven executed artifacts exist in the runtime receipt directory used during packaging.
