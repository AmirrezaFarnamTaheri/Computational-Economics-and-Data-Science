#!/usr/bin/env python3
"""New-Keynesian determinacy regions in the (phi_pi, phi_y) Taylor-rule plane.

Target lecture: 04-Macro-Models/05_New_Keynesian_Models.ipynb (policy rule).
Run:  python figures/src/nk_determinacy_regions.py
  ->  images/04-Macro-Models/nk_determinacy_regions.png

Illustrative frontier phi_pi = 1 - m * phi_y: above it the equilibrium is
unique (determinate), below it indeterminate (sunspot equilibria exist).
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
    / "nk_determinacy_regions.png"
)

SLOPE = 0.4  # illustrative trade-off between phi_pi and phi_y on the frontier


def main() -> None:
    phi_y = np.linspace(0.0, 1.5, 300)
    frontier = 1.0 - SLOPE * phi_y

    fig, ax = plt.subplots(figsize=(6.8, 4.6))
    ax.fill_between(
        phi_y,
        np.maximum(frontier, 0.0),
        2.5,
        color="#c7e5c7",
        label="unique (determinate)",
    )
    ax.fill_between(
        phi_y,
        0.0,
        np.maximum(frontier, 0.0),
        color="#f5d3a3",
        label="indeterminate (sunspots)",
    )
    ax.plot(
        phi_y[frontier >= 0],
        frontier[frontier >= 0],
        color="black",
        lw=2.2,
        label=r"frontier $\phi_\pi = 1 - m\,\phi_y$",
    )
    ax.axhline(1.0, color="gray", lw=0.9, ls=":")
    ax.annotate(
        "Taylor principle " + r"$(\phi_\pi > 1)$",
        xy=(0.72, 1.05),
        fontsize=9,
        color="dimgray",
    )
    ax.set_xlim(0.0, 1.5)
    ax.set_ylim(0.0, 2.5)
    ax.set_xlabel(r"output-gap response $\phi_y$")
    ax.set_ylabel(r"inflation response $\phi_\pi$")
    ax.set_title("Taylor-rule determinacy regions (illustrative)")
    ax.legend(frameon=False, loc="upper right")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
