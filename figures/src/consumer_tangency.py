#!/usr/bin/env python3
"""Consumer tangency: budget line, indifference curves, and the optimum.

Target lecture: 05-Micro-Models/01_Consumer_and_Producer_Theory.ipynb (duality).
Run:  python figures/src/consumer_tangency.py
  ->  images/05-Micro-Models/consumer_tangency.png

Illustrative Cobb-Douglas u = x^0.5 * y^0.5 with income I = 10, prices (1, 2).
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = (
    Path(__file__).resolve().parents[2]
    / "images"
    / "05-Micro-Models"
    / "consumer_tangency.png"
)

ALPHA, INCOME, PX, PY = 0.5, 10.0, 1.0, 2.0


def main() -> None:
    x = np.linspace(0.5, 12, 300)

    fig, ax = plt.subplots(figsize=(6.4, 4.8))
    for level in (2.0, 2.9, 3.8):
        y = level**2 / x ** (2 * ALPHA)
        ax.plot(x, y, lw=1.4, color="#7fa6c9")
    ax.annotate("indifference curves", xy=(7.4, 2.55), fontsize=9, color="#48688a")

    x_budget = np.array([0.0, INCOME / PX])
    ax.plot(
        x_budget,
        INCOME / PY - (PY / PX) * x_budget,
        lw=2.2,
        color="#b03a2e",
        label=f"budget: ${PX:g}x + ${PY:g}y = {INCOME:g}",
    )

    x_star = ALPHA * INCOME / PX
    y_star = (1 - ALPHA) * INCOME / PY
    ax.scatter([x_star], [y_star], zorder=5, color="black")
    ax.plot([x_star, x_star], [0, y_star], color="gray", lw=0.9, ls=":")
    ax.plot([0, x_star], [y_star, y_star], color="gray", lw=0.9, ls=":")
    ax.annotate(
        r"tangency: $MRS = p_x/p_y$",
        (x_star, y_star),
        xytext=(10, 14),
        textcoords="offset points",
        fontsize=10,
    )
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_xlabel(r"good $x$")
    ax.set_ylabel(r"good $y$")
    ax.set_title("Consumer optimum where MRS equals the price ratio")
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
