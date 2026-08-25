#!/usr/bin/env python3
"""OLS as orthogonal projection of y onto the column space of X.

Target lecture: 06-Econometrics/01_Linear_Model_and_OLS.ipynb (theory section).
Run:  python figures/src/ols_projection_geometry.py
  ->  images/06-Econometrics/ols_projection_geometry.png

Two-regressor schematic drawn in the plane spanned by x1 and x2.
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
    / "ols_projection_geometry.png"
)


def main() -> None:
    fig, ax = plt.subplots(figsize=(6.2, 5.4))
    ax.set_aspect("equal")

    origin = np.array([0.0, 0.0])
    x1 = np.array([3.6, 0.9])
    x2 = np.array([1.1, 2.9])
    beta = np.array([1.15, 0.75])
    yhat = beta[0] * x1 + beta[1] * x2
    y = yhat + np.array([0.55, 1.85])

    for vec, color, label in (
        (x1, "#48688a", r"$\mathbf{x}_1$"),
        (x2, "#48688a", r"$\mathbf{x}_2$"),
        (y, "#b03a2e", r"$\mathbf{y}$"),
        (yhat, "#2e7d32", r"$\hat{\mathbf{y}} = \mathbf{P}_X \mathbf{y}$"),
    ):
        ax.annotate(
            "",
            xy=vec,
            xytext=origin,
            arrowprops=dict(arrowstyle="-|>", color=color, lw=2.0),
        )
        ax.annotate(label, xy=vec * 1.04, fontsize=12, color=color)

    ax.plot([y[0], yhat[0]], [y[1], yhat[1]], ls="--", color="#7a5aa0", lw=1.8)
    mid = (y + yhat) / 2
    ax.annotate(
        r"$\mathbf{u} = \mathbf{y} - \hat{\mathbf{y}}$",
        xy=mid,
        xytext=(8, 4),
        textcoords="offset points",
        fontsize=12,
        color="#7a5aa0",
    )
    ax.annotate(
        "",
        xy=yhat,
        xytext=y,
        arrowprops=dict(arrowstyle="-|>", color="#7a5aa0", lw=1.8),
    )

    t = np.linspace(-0.35, 1.45, 24)
    dir_hat = yhat / np.linalg.norm(yhat)
    perp = np.array([-dir_hat[1], dir_hat[0]])
    line = yhat[None, :] + 2.05 * t[:, None] * perp[None, :]
    ax.plot(line[:, 0], line[:, 1], color="#bbbbbb", lw=1.0)
    ax.annotate(r"col($\mathbf{X}$)", xy=line[-1] * 1.02, fontsize=10, color="#888888")
    ax.add_patch(plt.Rectangle((0, 0), 0, 0))  # keep frame stable

    ax.set_xlim(-1.4, 6.4)
    ax.set_ylim(-1.2, 5.6)
    ax.axis("off")
    ax.set_title("OLS: project y onto col(X); residuals are orthogonal")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
