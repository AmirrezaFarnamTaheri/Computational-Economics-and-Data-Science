#!/usr/bin/env python3
"""Lab: learning-rate schedules and their effect on gradient descent.

Lecture: 07-Machine-Learning/06_Deep_Learning_Foundations.ipynb.

Run:
    python labs/lr_schedules_lab.py            # interactive if ipywidgets present
    python labs/lr_schedules_lab.py --static   # static 2x2 panel, saved as PNG
    python labs/lr_schedules_lab.py --static --out build/labs/lr.png

Deterministic: no randomness anywhere.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT_DEFAULT = (
    Path(__file__).resolve().parents[1] / "build" / "labs" / "lr_schedules.png"
)

SCHEDULES = ("constant", "step", "exponential", "cosine", "warmup+cosine")


def lr_at(schedule: str, lr0: float, t: int, total: int, decay: float) -> float:
    """Learning rate of ``schedule`` at iteration ``t`` (0-indexed)."""
    if schedule == "constant":
        return lr0
    if schedule == "step":
        return lr0 * decay ** (t // max(total // 4, 1))
    if schedule == "exponential":
        return lr0 * decay**t
    if schedule == "cosine":
        cos = np.cos(np.pi * t / max(total, 1))
        return lr0 * 0.5 * (1.0 + cos)
    if schedule == "warmup+cosine":
        warm = max(total // 10, 1)
        if t < warm:
            return lr0 * (t + 1) / warm
        cos = np.cos(np.pi * (t - warm) / max(total - warm, 1))
        return lr0 * 0.5 * (1.0 + cos)
    raise ValueError(f"unknown schedule {schedule!r}")


def gd_trajectory(schedule: str, lr0: float, total: int, decay: float) -> np.ndarray:
    """Gradient descent on f(w) = 0.5 * a * w^2 with per-iteration lr."""
    curvature = 1.6
    w, path = 4.0, np.empty(total + 1)
    path[0] = w
    for t in range(total):
        w = w - lr_at(schedule, lr0, t, total, decay) * curvature * w
        path[t + 1] = w
    return path


def draw(
    ax_sched, ax_loss, schedule: str, lr0: float, total: int, decay: float
) -> None:
    iters = np.arange(total)
    lrs = [lr_at(schedule, lr0, int(t), total, decay) for t in iters]
    ax_sched.plot(iters, lrs, lw=2.0, color="#48688a")
    ax_sched.set_title(f"schedule: {schedule}", fontsize=11)
    ax_sched.set_xlabel("iteration")
    ax_sched.set_ylabel("learning rate")

    path = gd_trajectory(schedule, lr0, total, decay)
    ax_loss.plot(np.arange(total + 1), 0.8 * path**2, lw=2.0, color="#b03a2e")
    ax_loss.set_title("loss $0.8\\,w_t^2$", fontsize=11)
    ax_loss.set_xlabel("iteration")
    ax_loss.set_ylabel("loss")
    ax_loss.set_yscale("symlog", linthresh=0.01)


def render_static(lr0: float, total: int, decay: float, out: Path) -> None:
    fig, axes = plt.subplots(2, 5, figsize=(16.5, 5.4))
    for k, schedule in enumerate(SCHEDULES):
        draw(axes[0, k], axes[1, k], schedule, lr0, total, decay)
    fig.suptitle(
        f"Learning-rate schedules (lr0={lr0}, decay={decay}, {total} steps)",
        fontsize=12,
    )
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150)
    plt.close(fig)
    print(f"wrote {out}")


def render_interactive(lr0: float, total: int, decay: float, out: Path) -> None:
    import ipywidgets as widgets

    sched = widgets.Dropdown(options=SCHEDULES, value="cosine", description="schedule")
    lr_slider = widgets.FloatLogSlider(
        value=lr0, base=10, min=-3, max=0, step=0.1, description="lr0"
    )
    it_slider = widgets.IntSlider(
        value=total, min=20, max=400, step=10, description="iters"
    )
    dec_slider = widgets.FloatLogSlider(
        value=decay, base=10, min=-4, max=-0.3, step=0.05, description="decay"
    )

    def show(schedule, lr_slider_value, iters, decay_value):
        fig, (ax_sched, ax_loss) = plt.subplots(1, 2, figsize=(10.5, 4.2))
        draw(ax_sched, ax_loss, schedule, lr_slider_value, int(iters), decay_value)
        fig.tight_layout()
        plt.show()

    widgets.interact(
        show,
        schedule=sched,
        lr_slider_value=lr_slider,
        iters=it_slider,
        decay_value=dec_slider,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--static", action="store_true", help="render a static panel")
    parser.add_argument("--out", type=Path, default=OUT_DEFAULT)
    parser.add_argument("--lr0", type=float, default=0.55)
    parser.add_argument("--iters", type=int, default=120)
    parser.add_argument("--decay", type=float, default=0.05)
    args = parser.parse_args()

    if args.static:
        render_static(args.lr0, args.iters, args.decay, args.out)
        return
    try:
        import ipywidgets  # noqa: F401
    except ImportError:
        print("ipywidgets not installed - falling back to static rendering")
        render_static(args.lr0, args.iters, args.decay, args.out)
        return
    render_interactive(args.lr0, args.iters, args.decay, args.out)


if __name__ == "__main__":
    main()
