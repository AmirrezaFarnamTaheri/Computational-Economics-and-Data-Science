#!/usr/bin/env python3
"""Sharp RD: binned outcome, cutoff, and local linear fits on either side.

Target lecture: 06-Econometrics/06_Regression_Discontinuity.ipynb (sec 1).
Run:  python figures/src/rd_sharp_fit.py
  ->  images/06-Econometrics/rd_sharp_fit.png

Simulated data with a constant treatment effect tau = 1.2 at the cutoff.
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
    / "rd_sharp_fit.png"
)

CUTOFF, TAU = 50.0, 1.2


def main() -> None:
    rng = np.random.default_rng(7)
    n = 1200
    x = rng.uniform(30, 70, n)
    d = (x >= CUTOFF).astype(float)
    y = (
        3.0
        + 0.05 * (x - CUTOFF)
        + TAU * d
        + 0.02 * (x - CUTOFF) * d
        + rng.normal(0, 0.45, n)
    )

    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    bins = np.linspace(30, 70, 21)
    centers, means = [], []
    for lo, hi in zip(bins[:-1], bins[1:]):
        mask = (x >= lo) & (x < hi)
        if mask.any():
            centers.append(0.5 * (lo + hi))
            means.append(y[mask].mean())
    ax.scatter(centers, means, s=26, color="#48688a", zorder=4, label="bin means")

    intercepts = []
    for side_mask, color, side in (
        (x < CUTOFF, "#b03a2e", "left"),
        (x >= CUTOFF, "#2e7d32", "right"),
    ):
        xs = x[side_mask]
        coef = np.polyfit(xs - CUTOFF, y[side_mask], 1)
        intercepts.append(coef[1])
        bounds = (xs.min(), CUTOFF) if side == "left" else (CUTOFF, xs.max())
        grid = np.linspace(*bounds, 40)
        ax.plot(
            grid,
            np.polyval(coef, grid - CUTOFF),
            color=color,
            lw=2.2,
            label=f"{side} linear fit",
        )

    ax.axvline(CUTOFF, color="gray", ls=":", lw=1.0)
    ax.annotate(
        "cutoff c",
        xy=(CUTOFF, 0.02),
        xycoords=("data", "axes fraction"),
        xytext=(5, 0),
        textcoords="offset points",
        fontsize=9,
        color="dimgray",
    )
    ax.annotate(
        "",
        xy=(CUTOFF, intercepts[1]),
        xytext=(CUTOFF, intercepts[0]),
        arrowprops=dict(arrowstyle="<->", color="#b03a2e", lw=1.8),
    )
    ax.annotate(
        r"$\hat{\tau}$",
        xy=(CUTOFF + 0.5, np.mean(intercepts)),
        fontsize=12,
        color="#b03a2e",
    )
    ax.set_title("Sharp RD: simulated data and fitted discontinuity")
    ax.set_xlabel("running variable X")
    ax.set_ylabel("outcome Y")
    ax.legend(frameon=False, loc="lower right", fontsize=9)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
