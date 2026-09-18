#!/usr/bin/env python3
"""Value-function iteration on the cake-eating problem: convergence picture.

Target lecture: 03-Economic-Modeling/01_Dynamic_Programming.ipynb (VFI section).
Run:  python figures/src/vfi_convergence.py
  ->  images/03-Economic-Modeling/vfi_convergence.png

For CRRA gamma=0.5, u(c)=2*sqrt(c), beta=0.95 and zero terminal value,
iterate T(v)(w) = max_{0 <= c <= w} [u(c) + beta*v(w-c)] on a grid.
The zero-cake boundary is V(0)=0. The continuous-choice infinite-horizon
benchmark is V(w)=2*sqrt(w)/sqrt(1-beta**2).
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
    w_grid = np.linspace(0.0, 1.0, 201)

    def u(c: np.ndarray) -> np.ndarray:
        return c ** (1 - GAMMA) / (1 - GAMMA)

    v = np.zeros_like(w_grid)  # zero terminal value; T^1(0)=u(w)

    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    for it in range(1, 51):
        v_new = np.empty_like(v)
        for i, w in enumerate(w_grid):
            feasible = np.linspace(0.0, w, 201)
            cont = np.interp(w - feasible, w_grid, v)
            v_new[i] = np.max(u(feasible) + BETA * cont)
        v = v_new
        if it in (1, 2, 5, 50):
            ax.plot(
                w_grid,
                v,
                lw=1.8,
                label=f"iteration {it}",
                ls={1: "-", 2: "--", 5: "-.", 50: ":"}[it],
            )
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
