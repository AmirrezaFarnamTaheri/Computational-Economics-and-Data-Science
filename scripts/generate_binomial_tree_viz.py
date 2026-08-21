"""
Generates a publication-grade Cox-Ross-Rubinstein (CRR) Binomial Tree option pricing visualization.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.pyplot as plt
import numpy as np
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def generate_binomial_tree_viz():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    apply_academic_style(ax, grid=False)
    ax.set_xlim(-0.5, 4.5)
    ax.set_ylim(-3.5, 3.5)
    ax.axis("off")

    ax.text(
        2.0,
        3.2,
        "Cox-Ross-Rubinstein (CRR) Binomial Tree Lattice (T=3)",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color=COLORS["primary"],
    )

    S0 = 100.0
    u = 1.15
    d = 0.90
    r = 0.05
    dt = 1.0 / 3.0
    q = (np.exp(r * dt) - d) / (u - d)

    levels = 3
    nodes = {}
    for step in range(levels + 1):
        for j in range(step + 1):
            price = S0 * (u ** (step - j)) * (d**j)
            y_pos = (step - 2 * j) * 0.9
            nodes[(step, j)] = (step, y_pos, price)

    # Draw branches
    for (step, j), (x, y, p) in nodes.items():
        if step < levels:
            # Up move
            x_u, y_u, _ = nodes[(step + 1, j)]
            ax.plot([x, x_u], [y, y_u], color=COLORS["border"], lw=1.5, zorder=1)
            ax.text(
                (x + x_u) / 2 - 0.05,
                (y + y_u) / 2 + 0.1,
                f"q={q:.2f}",
                fontsize=7.5,
                color=COLORS["accent_green"],
            )

            # Down move
            x_d, y_d, _ = nodes[(step + 1, j + 1)]
            ax.plot([x, x_d], [y, y_d], color=COLORS["border"], lw=1.5, zorder=1)
            ax.text(
                (x + x_d) / 2 - 0.05,
                (y + y_d) / 2 - 0.15,
                f"1-q={1 - q:.2f}",
                fontsize=7.5,
                color=COLORS["accent_amber"],
            )

    # Draw nodes
    for (step, j), (x, y, price) in nodes.items():
        circle = plt.Circle(
            (x, y),
            0.28,
            facecolor="#EFF6FF",
            edgecolor=COLORS["primary"],
            lw=1.5,
            zorder=3,
        )
        ax.add_patch(circle)
        ax.text(
            x,
            y + 0.04,
            f"S={price:.1f}",
            ha="center",
            va="center",
            fontsize=8.5,
            fontweight="bold",
            color=COLORS["text_dark"],
            zorder=4,
        )
        ax.text(
            x,
            y - 0.10,
            f"t={step}",
            ha="center",
            va="center",
            fontsize=7,
            color=COLORS["text_muted"],
            zorder=4,
        )

    output_path = "images/07-Financial-Economics/binomial_tree_visualization.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Cox-Ross-Rubinstein (CRR) 3-step recombining binomial tree lattice with risk-neutral transition probabilities.",
    )


if __name__ == "__main__":
    generate_binomial_tree_viz()
