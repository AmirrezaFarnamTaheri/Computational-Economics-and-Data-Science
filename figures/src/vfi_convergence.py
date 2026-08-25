#!/usr/bin/env python3
"""Value-function iteration on the cake-eating problem: convergence picture.

Target lecture: 03-Economic-Modeling/01_Dynamic_Programming.ipynb (VFI section).
Run:  python figures/src/vfi_convergence.py
  ->  images/03-Economic-Modeling/vfi_convergence.png

Analytic cake-eating value v(w) = ((1-gamma)*psi)^{-1/gamma} * w^{1-gamma} with
CRRA gamma=0.5 and psi solving psi = beta*(1+... ) under linear depletion;
here we simply iterate the contraction T(v)(w) = u(c) + beta*v(w-c) on a grid,
which is the algorithm taught in the lecture.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = (
    Path(__file__).resolve().parents[2]
    / "images"
    / "03-Economic-Modeling"
    / "vfi_convergence.png"
)

BETA, GAMMA = 0.95, 0.5


def main() -> None:
    w_grid = np.linspace(0.05, 1.0, 200)
    c_grid = np.linspace(1e-3, 1.0, 200)

    def u(c: np.ndarray) -> np.ndarray:
        return c ** (1 - GAMMA) / (1 - GAMMA)

    v = u(w_grid)  # start from utility of eating everything

    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    for k, it in enumerate((1, 2, 5, 50)):
        v_new = np.empty_like(v)
        for i, w in enumerate(w_grid):
            feasible = c_grid[c_grid <= w]
            cont = np.interp(w - feasible, w_grid, v)
            v_new[i] = np.max(u(feasible) + BETA * cont)
        v = v_new
        if it in (1, 2, 5, 50):
            ax.plot(w_grid, v, lw=1.8, label=f"iteration {it}")
    ax.set_xlabel("cake size $w$")
    ax.set_ylabel("value $V(w)$")
    ax.set_title("Value function iteration converging (illustrative)")
    ax.legend(frameon=False)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
