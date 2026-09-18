#!/usr/bin/env python3
"""OLS as orthogonal projection of y onto the column space of X.

Target lecture: 06-Econometrics/01_Linear_Model_and_OLS.ipynb (theory section).
Run:  python figures/src/ols_projection_geometry.py
  ->  images/06-Econometrics/ols_projection_geometry.png

One-regressor, no-intercept example in R^2. With two independent regressors
in R^2 the column space would be all of R^2 and the residual would be zero.
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
    origin = np.zeros(2)
    x = np.array([4.0, 1.6])
    y = np.array([2.7, 4.1])
    yhat = x * (x @ y) / (x @ x)
    residual = y - yhat
    assert np.isclose(x @ residual, 0.0)

    line = np.array([-0.15, 1.45])[:, None] * x
    ax.plot(line[:, 0], line[:, 1], color="#bbbbbb", lw=1.0)
    ax.annotate(r"col($\mathbf{X}$) = span($\mathbf{x}$)", xy=(4.0, 0.55), fontsize=10)
    for vec, color, label, offset in (
        (x, "#48688a", r"$\mathbf{x}$", (6, -12)),
        (y, "#b03a2e", r"$\mathbf{y}$", (0, 9)),
        (yhat, "#2e7d32", r"$\hat{\mathbf{y}} = \mathbf{P}_X\mathbf{y}$", (9, -22)),
    ):
        ax.annotate(
            "",
            xy=vec,
            xytext=origin,
            arrowprops=dict(arrowstyle="-|>", color=color, lw=2.0),
        )
        ax.annotate(
            label, xy=vec, xytext=offset, textcoords="offset points", fontsize=12
        )
    ax.annotate(
        "",
        xy=y,
        xytext=yhat,
        arrowprops=dict(arrowstyle="-|>", color="#7a5aa0", lw=1.8),
    )
    ax.annotate(
        r"$\mathbf{u} = \mathbf{y} - \hat{\mathbf{y}}$",
        xy=(y + yhat) / 2,
        xytext=(10, 3),
        textcoords="offset points",
        fontsize=12,
    )

    # A right-angle mark is meaningful because the axes use equal scaling.
    along = x / np.linalg.norm(x)
    normal = residual / np.linalg.norm(residual)
    corner = np.array(
        [yhat - 0.22 * along, yhat - 0.22 * along + 0.22 * normal, yhat + 0.22 * normal]
    )
    ax.plot(corner[:, 0], corner[:, 1], color="gray", lw=1.0)
    ax.set_xlim(-0.7, 6.3)
    ax.set_ylim(-0.5, 5.0)
    ax.axis("off")
    ax.set_title("OLS: project y onto col(X); residuals are orthogonal")
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
