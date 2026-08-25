#!/usr/bin/env python3
"""Lab: stability of ODE solvers on y' = -lambda * y.

Lecture: 02-Numerical-Methods/08_Differential_Equations.ipynb (stiffness and
stability).

Run:
    python labs/ode_stability_lab.py            # interactive if ipywidgets present
    python labs/ode_stability_lab.py --static   # static panel, saved as PNG
    python labs/ode_stability_lab.py --static --out build/labs/ode.png

Fully deterministic: the test problem has a closed-form solution.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT_DEFAULT = (
    Path(__file__).resolve().parents[1] / "build" / "labs" / "ode_stability.png"
)

METHODS = ("explicit Euler", "implicit Euler", "RK4")


def step(method: str, lam: float, h: float, y: float) -> float:
    """One step of ``method`` for y' = -lam*y (amplification-factor form)."""
    if method == "explicit Euler":
        return (1.0 - lam * h) * y
    if method == "implicit Euler":
        return y / (1.0 + lam * h)
    if method == "RK4":
        k1 = -lam * y
        k2 = -lam * (y + 0.5 * h * k1)
        k3 = -lam * (y + 0.5 * h * k2)
        k4 = -lam * (y + h * k3)
        return y + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    raise ValueError(f"unknown method {method!r}")


def simulate(method: str, lam: float, h: float, n_steps: int) -> np.ndarray:
    ys = np.empty(n_steps + 1)
    ys[0] = 1.0
    for k in range(n_steps):
        ys[k + 1] = step(method, lam, h, ys[k])
    return ys


def draw(ax_traj, ax_region, method: str, lam: float, h: float, n_steps: int) -> None:
    t = np.arange(n_steps + 1) * h
    exact = np.exp(-lam * t)
    ys = simulate(method, lam, h, n_steps)
    ax_traj.plot(t, exact, lw=1.6, color="#48688a", label="exact $e^{-\\lambda t}$")
    ax_traj.plot(t, ys, "o-", ms=3.5, lw=1.4, color="#b03a2e", label=method)
    ax_traj.set_title(f"{method}  (h={h:g}, $\\lambda$={lam:g})", fontsize=10)
    ax_traj.set_xlabel("t")
    ax_traj.set_ylabel("y")
    ax_traj.legend(frameon=False, fontsize=8)

    # stability region for the point z = h * lambda (negative real axis)
    z = -h * lam
    ax_region.axhline(0.0, color="#cccccc", lw=0.8)
    ax_region.axvline(0.0, color="#cccccc", lw=0.8)
    if method == "explicit Euler":
        theta = np.linspace(0.0, 2.0 * np.pi, 200)
        ax_region.plot(1 + np.cos(theta), np.sin(theta), color="#48688a", lw=1.6)
        ax_region.fill(1 + np.cos(theta), np.sin(theta), color="#c7e5c7", alpha=0.6)
        ax_region.set_title("explicit Euler: stable inside |1+z|<1", fontsize=9)
    elif method == "implicit Euler":
        re = np.linspace(-4.0, 0.5, 300)
        ax_region.fill_between(
            re, -np.abs(1 + re), np.abs(1 + re), color="#c7e5c7", alpha=0.6
        )
        ax_region.set_title("implicit Euler: stable for Re(z)<0", fontsize=9)
    else:  # RK4: |1 + z + z^2/2 + z^3/6 + z^4/24| = 1
        re = np.linspace(-4.0, 0.5, 300)
        im = np.linspace(-3.0, 3.0, 300)
        rr, ii = np.meshgrid(re, im)
        z_grid = rr + 1j * ii
        p = np.abs(
            1.0
            + z_grid
            * (1.0 + z_grid / 2.0 * (1.0 + z_grid / 3.0 * (1.0 + z_grid / 4.0)))
        )
        ax_region.contour(rr, ii, p, levels=[1.0], colors="#48688a")
        ax_region.contourf(rr, ii, p, levels=[0.0, 1.0], colors=["#c7e5c7"], alpha=0.6)
        ax_region.set_title("RK4: stable inside |p(z)|=1 region", fontsize=9)
    ax_region.plot([z], [0.0], "o", ms=7, color="#b03a2e")
    ax_region.annotate(
        f"z = {z:g}", xy=(z, 0.0), xytext=(4, 6), textcoords="offset points", fontsize=9
    )
    ax_region.set_xlabel("Re(z)")
    ax_region.set_ylabel("Im(z)")


def render_static(lam: float, h: float, n_steps: int, out: Path) -> None:
    fig, axes = plt.subplots(2, 3, figsize=(13.5, 5.6))
    for k, method in enumerate(METHODS):
        draw(axes[0, k], axes[1, k], method, lam, h, n_steps)
    fig.suptitle(
        f"Solver stability on y' = -\u03bb y (\u03bb={lam:g}, h={h:g}, "
        f"{n_steps} steps)",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"wrote {out}")


def render_interactive(lam: float, h: float, n_steps: int, out: Path) -> None:
    import ipywidgets as widgets

    method = widgets.Dropdown(
        options=METHODS, value="explicit Euler", description="method"
    )
    lam_s = widgets.FloatSlider(
        value=lam, min=0.1, max=12.0, step=0.1, description="lambda"
    )
    h_s = widgets.FloatSlider(value=h, min=0.05, max=2.5, step=0.05, description="h")
    n_s = widgets.IntSlider(value=n_steps, min=5, max=80, step=5, description="steps")

    def show(method_value, lam_value, h_value, n_value):
        fig, (ax_traj, ax_region) = plt.subplots(1, 2, figsize=(10.5, 4.4))
        draw(ax_traj, ax_region, method_value, lam_value, h_value, int(n_value))
        fig.tight_layout()
        plt.show()

    widgets.interact(
        show, method_value=method, lam_value=lam_s, h_value=h_s, n_value=n_s
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--static", action="store_true", help="render a static panel")
    parser.add_argument("--out", type=Path, default=OUT_DEFAULT)
    parser.add_argument("--lambda", dest="lam", type=float, default=6.0)
    parser.add_argument("--h", type=float, default=0.35)
    parser.add_argument("--steps", type=int, default=30)
    args = parser.parse_args()

    if args.static:
        render_static(args.lam, args.h, args.steps, args.out)
        return
    try:
        import ipywidgets  # noqa: F401
    except ImportError:
        print("ipywidgets not installed - falling back to static rendering")
        render_static(args.lam, args.h, args.steps, args.out)
        return
    render_interactive(args.lam, args.h, args.steps, args.out)


if __name__ == "__main__":
    main()
