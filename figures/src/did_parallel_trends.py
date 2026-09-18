#!/usr/bin/env python3
"""Difference-in-Differences: parallel trends and the 2x2 contrast.

Target lecture: 06-Econometrics/08_Difference_in_Differences.ipynb (sec 1).
Run:  python figures/src/did_parallel_trends.py
  ->  images/06-Econometrics/did_parallel_trends.png

Illustrative series with a constant treatment effect after the policy date.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = (
    Path(__file__).resolve().parents[2]
    / "images"
    / "06-Econometrics"
    / "did_parallel_trends.png"
)


def main() -> None:
    t = np.arange(-4, 5)
    treated = 2.0 + 0.55 * t + np.where(t >= 0, 1.6, 0.0)
    control = 1.4 + 0.55 * t
    counterfactual = control + (treated[0] - control[0])

    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    ax.plot(t[t < 0], treated[t < 0], "o-", color="#b03a2e", label="treated group")
    ax.plot(t[t >= 0], treated[t >= 0], "o-", color="#b03a2e")
    ax.plot(t, control, "s-", color="#48688a", label="control group")
    ax.plot(
        t[t >= 0],
        counterfactual[t >= 0],
        "o--",
        color="#b03a2e",
        alpha=0.55,
        label="treated counterfactual",
    )
    ax.axvline(0.0, color="gray", lw=1.0, ls=":")
    ax.annotate(
        "",
        xy=(t[-1], treated[-1]),
        xytext=(t[-1], counterfactual[-1]),
        arrowprops=dict(arrowstyle="<->", color="#2e7d32", lw=1.8),
    )
    ax.annotate(
        r"DiD estimate $\hat{\delta}$",
        xy=(t[-1], (treated[-1] + counterfactual[-1]) / 2),
        xytext=(-8, -18),
        textcoords="offset points",
        fontsize=10,
        color="#2e7d32",
        ha="right",
    )
    ax.annotate(
        "policy", xy=(0.05, ax.get_ylim()[0] + 0.08), fontsize=9, color="dimgray"
    )
    ax.set_xlabel("period relative to policy")
    ax.set_ylabel("outcome (illustrative)")
    ax.legend(frameon=False, loc="upper left", fontsize=9)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
