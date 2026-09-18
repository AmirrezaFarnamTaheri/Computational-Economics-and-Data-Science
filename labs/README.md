# Labs — Interactive Widget Laboratories (WP-13)

Self-contained, dependency-light lab scripts. Each script:

- runs standalone: `python labs/<name>.py`
- uses **ipywidgets** sliders when available (run inside Jupyter for the full
  interactive experience)
- falls back to a **static multi-panel rendering** otherwise, so the labs work
  in any environment, including CI
- is deterministic: fixed seeds, no network access

| Lab | Lecture | Concepts |
|---|---|---|
| `lr_schedules_lab.py` | 07-Machine-Learning/06 Deep Learning Foundations | learning-rate schedules (constant, step, exponential, cosine, warmup) and their effect on gradient descent |
| `ode_stability_lab.py` | 02-Numerical-Methods/08 Differential Equations | explicit vs implicit Euler and RK4 stability on $y' = -\lambda y$; stability regions |
| `cobweb_stability_lab.py` | 01-Foundations/01 Introduction; 02-Numerical-Methods/04 Root Finding | cobweb model stability condition $\|d/b\| < 1$, cobweb plot and time path |

Usage:

```bash
python labs/lr_schedules_lab.py            # interactive if ipywidgets present
python labs/lr_schedules_lab.py --static   # static panel, saved as PNG
python labs/lr_schedules_lab.py --static --out build/labs/lr.png
```

Static outputs default to `build/labs/` (gitignored).
