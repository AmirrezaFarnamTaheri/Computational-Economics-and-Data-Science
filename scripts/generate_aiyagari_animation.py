"""
Generates an animated GIF of the wealth distribution converging to stationary equilibrium in the Aiyagari model.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.pyplot as plt
import numpy as np
from diagram_style import COLORS, apply_academic_style, update_metadata
from matplotlib.animation import FuncAnimation


def generate_aiyagari_animation():
    output_dir = "images/04-Macro-Models"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "aiyagari_equilibrium.gif")

    n_frames = 30
    x = np.linspace(0.01, 20, 150)
    dx = x[1] - x[0]

    fig, ax = plt.subplots(figsize=(8, 5), dpi=150)

    def update(frame):
        ax.clear()
        apply_academic_style(ax, grid=True)
        t = frame / float(n_frames)
        mean = 1.0 + 2.5 * (1.0 - np.exp(-3 * t))
        sigma = 0.5 + 0.3 * (1.0 - np.exp(-3 * t))
        dist = (1.0 / (x * sigma * np.sqrt(2 * np.pi))) * np.exp(
            -((np.log(x) - mean) ** 2) / (2 * sigma**2)
        )
        total_area = np.sum(dist) * dx
        if total_area > 0:
            dist = dist / total_area

        ax.plot(
            x,
            dist,
            color=COLORS["primary"],
            lw=2.5,
            label=f"Iteration {frame + 1}/{n_frames}",
        )
        ax.fill_between(x, dist, color=COLORS["primary"], alpha=0.15)
        ax.set_title(
            "Convergence to Stationary Wealth Distribution $\\mu^*(a)$",
            fontsize=12,
            fontweight="bold",
            color=COLORS["primary"],
        )
        ax.set_xlabel("Asset Holdings ($a$)", fontsize=10, fontweight="bold")
        ax.set_ylabel("Probability Density", fontsize=10, fontweight="bold")
        ax.set_ylim(0, 0.35)
        ax.legend(
            loc="upper right",
            frameon=True,
            facecolor="white",
            edgecolor=COLORS["border"],
            fontsize=9,
        )

    anim = FuncAnimation(fig, update, frames=n_frames, interval=100)
    anim.save(output_path, writer="pillow", fps=10)
    plt.close(fig)
    print(f"  [SAVED] {output_path}")
    update_metadata(
        output_path,
        "Animated convergence of the household wealth distribution to stationary general equilibrium.",
    )


if __name__ == "__main__":
    generate_aiyagari_animation()
