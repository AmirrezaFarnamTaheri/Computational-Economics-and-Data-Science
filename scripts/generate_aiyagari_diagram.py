"""
Generates a publication-grade flowchart of the Aiyagari (1994) General Equilibrium Algorithm.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def generate_aiyagari_flowchart():
    fig, ax = plt.subplots(figsize=(9.5, 11), dpi=300)
    apply_academic_style(ax, grid=False)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)
    ax.axis("off")

    ax.text(
        5,
        11.4,
        "Aiyagari (1994) Stationary General Equilibrium Algorithm",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color=COLORS["primary"],
    )

    def draw_box(
        x,
        y,
        w,
        h,
        title,
        details,
        color="#F8FAFC",
        border=COLORS["border"],
        is_decision=False,
    ):
        if is_decision:
            diamond = patches.Polygon(
                [
                    [x + w / 2, y],
                    [x + w, y + h / 2],
                    [x + w / 2, y + h],
                    [x, y + h / 2],
                ],
                closed=True,
                facecolor=color,
                edgecolor=COLORS["primary"],
                linewidth=1.5,
                zorder=3,
            )
            ax.add_patch(diamond)
            ax.text(
                x + w / 2,
                y + h / 2 + 0.12,
                title,
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                color=COLORS["primary"],
                zorder=4,
            )
            ax.text(
                x + w / 2,
                y + h / 2 - 0.25,
                details,
                ha="center",
                va="center",
                fontsize=9,
                color=COLORS["text_dark"],
                zorder=4,
            )
        else:
            box = patches.FancyBboxPatch(
                (x, y),
                w,
                h,
                boxstyle="round,pad=0.1,rounding_size=0.08",
                facecolor=color,
                edgecolor=border,
                linewidth=1.2,
                zorder=3,
            )
            ax.add_patch(box)
            ax.text(
                x + w / 2,
                y + h * 0.65,
                title,
                ha="center",
                va="center",
                fontsize=10.5,
                fontweight="bold",
                color=COLORS["text_dark"],
                zorder=4,
            )
            ax.text(
                x + w / 2,
                y + h * 0.30,
                details,
                ha="center",
                va="center",
                fontsize=8.5,
                color=COLORS["text_muted"],
                zorder=4,
            )

    draw_box(
        1.5,
        9.6,
        7.0,
        1.1,
        r"1. Outer Loop: Guess Aggregate Interest Rate $r^{(0)}$",
        r"Initialize bounds $[r_{\min}, r_{\max}]$, set initial guess $r^{(0)} \in (0, 1/\beta - 1)$",
        "#EFF6FF",
    )
    draw_box(
        1.5,
        7.9,
        7.0,
        1.1,
        r"2. Solve Household Dynamic Program $V(a, z; r)$",
        r"Compute policy $a'(a, z; r)$ via Value Function Iteration (VFI) or Euler Equation",
        "#F8FAFC",
    )
    draw_box(
        1.5,
        6.2,
        7.0,
        1.1,
        r"3. Compute Stationary Distribution $\mu(a, z)$",
        r"Solve fixed point of Markov transition operator $T_r(\mu) = \mu$",
        "#F8FAFC",
    )
    draw_box(
        1.5,
        4.5,
        7.0,
        1.1,
        r"4. Aggregate Capital Supply $K_s(r)$ vs. Demand $K_d(r)$",
        r"$K_s(r) = \int a \, d\mu(a, z; r), \quad K_d(r) = [(r+\delta)/\alpha]^{1/(\alpha-1)}$",
        "#EFF6FF",
    )
    draw_box(
        2.0,
        2.4,
        6.0,
        1.4,
        "5. Capital Market Clearing?",
        r"$|K_s(r) - K_d(r)| < \epsilon$",
        "#FEF3C7",
        is_decision=True,
    )
    draw_box(
        1.5,
        0.4,
        7.0,
        1.1,
        r"6. Stationary Equilibrium $(r^*, w^*, \mu^*)$",
        r"Output equilibrium prices $(r^*, w^*)$, wealth distribution $\mu^*(a, z)$, and aggregates",
        "#ECFDF5",
        border=COLORS["accent_green"],
    )

    # Arrows
    arrow_props = dict(
        arrowstyle="-|>", mutation_scale=16, lw=1.8, color=COLORS["secondary"]
    )
    ax.annotate("", xy=(5, 9.0), xytext=(5, 9.6), arrowprops=arrow_props, zorder=2)
    ax.annotate("", xy=(5, 7.3), xytext=(5, 7.9), arrowprops=arrow_props, zorder=2)
    ax.annotate("", xy=(5, 5.6), xytext=(5, 6.2), arrowprops=arrow_props, zorder=2)
    ax.annotate("", xy=(5, 3.8), xytext=(5, 4.5), arrowprops=arrow_props, zorder=2)

    # Decision arrows
    ax.annotate("", xy=(5, 1.5), xytext=(5, 2.4), arrowprops=arrow_props, zorder=2)
    ax.text(
        5.2,
        1.9,
        "Yes (Converged)",
        fontsize=9,
        fontweight="bold",
        color=COLORS["accent_green"],
    )

    # Loop back arrow (No)
    ax.annotate(
        "",
        xy=(8.5, 10.15),
        xytext=(8.0, 3.1),
        arrowprops=dict(
            arrowstyle="-|>",
            mutation_scale=16,
            lw=1.8,
            color=COLORS["accent_amber"],
            connectionstyle="arc3,rad=-0.3",
        ),
        zorder=2,
    )
    ax.text(
        8.8,
        6.0,
        r"No: Update $r^{(k+1)}$" + "\n" + r"via Bisection",
        fontsize=9,
        fontweight="bold",
        color=COLORS["accent_amber"],
        ha="left",
    )

    output_path = "images/04-Macro-Models/aiyagari_algorithm_flowchart.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Aiyagari (1994) incomplete markets general equilibrium computational algorithm flowchart.",
    )


if __name__ == "__main__":
    generate_aiyagari_flowchart()
