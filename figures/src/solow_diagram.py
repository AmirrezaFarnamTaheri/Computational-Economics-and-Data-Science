#!/usr/bin/env python3
"""Solow diagram: sf(k) vs break-even investment with the steady state.

Target lecture: 04-Macro-Models/02_Neoclassical_Growth.ipynb (sec 1.1).
Run:  python figures/src/solow_diagram.py   ->  images/04-Macro-Models/solow_diagram.png
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = (
    Path(__file__).resolve().parents[2]
    / "images"
    / "04-Macro-Models"
    / "solow_diagram.png"
)


def main() -> None:
    s, n, g, delta = 0.3, 0.01, 0.015, 0.05
    k_star = (s / (n + g + delta)) ** 2
    k_max = 1.5 * k_star
    k = np.linspace(0.0, k_max, 400)
    f_k = k**0.5

    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    ax.plot(k, s * f_k, lw=2.2, label=r"saving $s\,f(k)$")
    ax.plot(
        k, (n + g + delta) * k, lw=2.0, ls="--", label=r"break-even $(n+g+\delta)k$"
    )
    y_star = s * k_star**0.5
    ax.plot([k_star, k_star], [0, y_star], color="gray", lw=0.9, ls=":")
    ax.plot([0, k_star], [y_star, y_star], color="gray", lw=0.9, ls=":")
    ax.scatter([k_star], [y_star], zorder=5, color="black")
    ax.annotate(
        r"$k^*$",
        (k_star, 0),
        xytext=(4, 6),
        textcoords="offset points",
        fontsize=13,
    )
    ax.annotate(
        r"$sf(k^*)$",
        (0, y_star),
        xytext=(6, -14),
        textcoords="offset points",
        fontsize=13,
    )
    ax.set_xlabel(r"capital per effective worker $k$")
    ax.set_ylabel("investment per effective worker")
    ax.set_xlim(0, k_max)
    ax.set_ylim(0, None)
    ax.legend(frameon=False)
    ax.set_title("Solow-Swan: saving vs break-even investment (illustrative)")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
