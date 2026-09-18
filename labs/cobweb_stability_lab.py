#!/usr/bin/env python3
"""Lab: stability of the cobweb model, P_t = (a-c)/b - (d/b) P_{t-1}.

Lectures: 01-Foundations/01_Introduction.ipynb (cobweb example) and
02-Numerical-Methods/04_Root_Finding.ipynb (fixed points).

Run:
    python labs/cobweb_stability_lab.py            # interactive if widgets present
    python labs/cobweb_stability_lab.py --static   # static panel, saved as PNG
    python labs/cobweb_stability_lab.py --static --out build/labs/cobweb.png

Stability condition (derived in the lecture): the price converges iff
|d/b| < 1. Fully deterministic.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT_DEFAULT = (
    Path(__file__).resolve().parents[1] / "build" / "labs" / "cobweb_stability.png"
)

A, C = 10.0, 2.0  # demand intercept / supply intercept (deterministic setup)


def price_path(b: float, d: float, p0: float, n_periods: int) -> np.ndarray:
    rho = -d / b
    path = np.empty(n_periods + 1)
    path[0] = p0
    for t in range(n_periods):
        path[t + 1] = rho * path[t] + (A - C) / b
    return path


def cobweb_points(b: float, d: float, p0: float, n_periods: int):
    """Step points for the cobweb plot: alternating on demand and supply."""
    demand = lambda p: (A - p) / b  # noqa: E731  (quantity from price, demand)
    pts = [(p0, 0.0)]
    p = p0
    for _ in range(n_periods):
        q = demand(p)
        pts.append((p, q))
        p_next = C + d * q
        pts.append((p_next, q))
        p = p_next
    return np.array(pts)


def draw(ax_cob, ax_ts, b: float, d: float, p0: float, n_periods: int) -> None:
    rho = -d / b

    # cobweb plot: demand p -> q, supply inverted q -> p
    p_grid = np.linspace(0.0, max(A / b, (A - C) / d + 2.0, p0 * 1.4), 200)
    ax_cob.plot(
        p_grid, (A - p_grid) / b, color="#48688a", lw=1.8, label="demand $Q^D(p)$"
    )
    ax_cob.plot(
        p_grid, (p_grid - C) / d, color="#2e7d32", lw=1.8, label="supply $Q^S(p)$"
    )
    pts = cobweb_points(b, d, p0, n_periods)
    ax_cob.plot(
        pts[:, 0], pts[:, 1], color="#b03a2e", lw=1.0, alpha=0.85, label="cobweb steps"
    )
    p_star = (A - C) / (b + d)
    ax_cob.axvline(p_star, color="gray", ls=":", lw=0.9)
    ax_cob.set_title(f"cobweb: $\\rho = -d/b$ = {rho:+.3f}", fontsize=10)
    ax_cob.set_xlabel("price $p$")
    ax_cob.set_ylabel("quantity $Q$")
    ax_cob.legend(frameon=False, fontsize=8)

    path = price_path(b, d, p0, n_periods)
    ax_ts.plot(np.arange(n_periods + 1), path, "o-", ms=3.5, lw=1.4, color="#b03a2e")
    ax_ts.axhline(p_star, color="gray", ls=":", lw=0.9)
    ax_ts.set_title(
        f"time path (|d/b| = {abs(d / b):.2f} "
        f"{'<' if abs(d / b) < 1 else '>/='} 1)",
        fontsize=10,
    )
    ax_ts.set_xlabel("period")
    ax_ts.set_ylabel("price $p_t$")


def render_static(b: float, d: float, p0: float, n_periods: int, out: Path) -> None:
    settings = ((1.0, 0.6), (1.0, 1.0), (1.0, 1.35), (1.0, 1.8))
    fig, axes = plt.subplots(2, 4, figsize=(14.0, 5.4))
    for k, (bb, dd) in enumerate(settings):
        draw(axes[0, k], axes[1, k], bb, dd, p0, n_periods)
    fig.suptitle(
        f"Cobweb stability (b=1; d={', '.join(str(s[1]) for s in settings)}; "
        f"p0={p0:g})",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"wrote {out}")


def render_interactive(b: float, d: float, p0: float, n_periods: int) -> None:
    import ipywidgets as widgets

    b_s = widgets.FloatSlider(value=b, min=0.4, max=2.5, step=0.05, description="b")
    d_s = widgets.FloatSlider(value=d, min=0.1, max=3.0, step=0.05, description="d")
    p_s = widgets.FloatSlider(value=p0, min=0.0, max=12.0, step=0.1, description="p0")
    n_s = widgets.IntSlider(
        value=n_periods, min=5, max=60, step=1, description="periods"
    )

    def show(b_value, d_value, p_value, n_value):
        fig, (ax_cob, ax_ts) = plt.subplots(1, 2, figsize=(10.5, 4.4))
        draw(ax_cob, ax_ts, b_value, d_value, p_value, int(n_value))
        fig.tight_layout()
        plt.show()

    widgets.interact(show, b_value=b_s, d_value=d_s, p_value=p_s, n_value=n_s)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--static", action="store_true", help="render a static panel")
    parser.add_argument("--out", type=Path, default=OUT_DEFAULT)
    parser.add_argument("--b", type=float, default=1.0)
    parser.add_argument("--d", type=float, default=1.35)
    parser.add_argument("--p0", type=float, default=1.0)
    parser.add_argument("--periods", type=int, default=24)
    args = parser.parse_args()

    if args.static:
        render_static(args.b, args.d, args.p0, args.periods, args.out)
        return
    try:
        import ipywidgets  # noqa: F401
    except ImportError:
        print("ipywidgets not installed - falling back to static rendering")
        render_static(args.b, args.d, args.p0, args.periods, args.out)
        return
    render_interactive(args.b, args.d, args.p0, args.periods)


if __name__ == "__main__":
    main()
