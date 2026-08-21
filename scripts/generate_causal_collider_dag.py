"""
Generates a publication-grade causal DAG illustrating Collider Bias (Berkson's Paradox).
"""

import sys
from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def generate_diagram():
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    apply_academic_style(ax, grid=False)
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, 2.5)
    ax.axis("off")

    # Title
    ax.text(
        1.5,
        2.2,
        "Collider Bias DAG: Conditioning on a Common Effect",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color=COLORS["primary"],
    )

    # Draw Nodes
    def draw_node(x, y, text, subtext, color, is_conditioned=False):
        ec = COLORS["accent_red"] if is_conditioned else COLORS["border"]
        lw = 2.5 if is_conditioned else 1.2
        box = patches.FancyBboxPatch(
            (x - 0.5, y - 0.35),
            1.0,
            0.7,
            boxstyle="round,pad=0.1,rounding_size=0.1",
            facecolor=color,
            edgecolor=ec,
            linewidth=lw,
            zorder=3,
        )
        ax.add_patch(box)
        ax.text(
            x,
            y + 0.08,
            text,
            ha="center",
            va="center",
            fontsize=12,
            fontweight="bold",
            color=COLORS["text_dark"],
            zorder=4,
        )
        ax.text(
            x,
            y - 0.14,
            subtext,
            ha="center",
            va="center",
            fontsize=9,
            color=COLORS["text_muted"],
            zorder=4,
        )

    draw_node(0.5, 1.2, "Talent (T)", "Exogenous", "#EFF6FF")
    draw_node(2.5, 1.2, "Luck (L)", "Exogenous", "#EFF6FF")
    draw_node(
        1.5,
        0.2,
        "Admission (A)",
        "Collider [Conditioned]",
        "#FEF2F2",
        is_conditioned=True,
    )

    # Draw Arrows
    arrow_props = dict(
        arrowstyle="-|>", mutation_scale=20, lw=2.0, color=COLORS["secondary"]
    )
    ax.annotate(
        "", xy=(1.3, 0.55), xytext=(0.7, 0.95), arrowprops=arrow_props, zorder=2
    )
    ax.annotate(
        "", xy=(1.7, 0.55), xytext=(2.3, 0.95), arrowprops=arrow_props, zorder=2
    )

    # Spurious correlation induced
    ax.annotate(
        "",
        xy=(2.0, 1.2),
        xytext=(1.0, 1.2),
        arrowprops=dict(
            arrowstyle="<->",
            linestyle="dashed",
            mutation_scale=15,
            lw=2.0,
            color=COLORS["accent_red"],
        ),
        zorder=2,
    )
    ax.text(
        1.5,
        1.45,
        "Spurious Negative Correlation\n(Conditioned on A)",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
        color=COLORS["accent_red"],
    )

    output_path = "images/06-Econometrics/collider_bias_dag.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Collider bias DAG showing Berkson paradox where conditioning on admission induces negative correlation between talent and luck.",
    )


if __name__ == "__main__":
    generate_diagram()
