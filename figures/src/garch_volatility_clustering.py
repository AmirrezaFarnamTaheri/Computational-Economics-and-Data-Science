#!/usr/bin/env python3
"""GARCH(1,1) volatility clustering: simulated returns and conditional sigma.

Target lecture: 08-Time-Series/05_Volatility_Modeling_ARCH_GARCH.ipynb (sec 1).
Run:  python figures/src/garch_volatility_clustering.py
  ->  images/08-Time-Series/garch_volatility_clustering.png

Simulated with omega=0.05e-4, alpha=0.09, beta=0.90 (stationary persistence).
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = (
    Path(__file__).resolve().parents[2]
    / "images"
    / "08-Time-Series"
    / "garch_volatility_clustering.png"
)

OMEGA, ALPHA, BETA = 0.05e-4, 0.09, 0.90


def main() -> None:
    rng = np.random.default_rng(11)
    n = 750
    eps = rng.standard_normal(n)
    ret = np.empty(n)
    var = np.empty(n)
    var[0] = OMEGA / (1 - ALPHA - BETA)
    ret[0] = np.sqrt(var[0]) * eps[0]
    for t in range(1, n):
        var[t] = OMEGA + ALPHA * ret[t - 1] ** 2 + BETA * var[t - 1]
        ret[t] = np.sqrt(var[t]) * eps[t]

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(7.6, 4.8), sharex=True, height_ratios=[1.0, 0.75]
    )
    ax1.plot(ret, lw=0.7, color="#48688a")
    ax1.set_ylabel("returns")
    ax1.set_title("Simulated GARCH(1,1): clustered volatility (illustrative)")
    ax2.plot(np.sqrt(var), lw=0.9, color="#b03a2e")
    ax2.set_ylabel(r"$\sigma_t$")
    ax2.set_xlabel("time")
    fig.align_ylabels()
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
