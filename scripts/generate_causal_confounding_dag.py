"""
Generates a publication-grade causal DAG illustrating Classic Confounding and Backdoor Paths.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def generate_diagram():
    fig, ax = plt.subplots(figsize=(8, 5), dpi=300)
    apply_academic_style(ax, grid=False)
    ax.set_xlim(-0.5, 3.5)
    ax.set_ylim(-0.5, 2.5)
    ax.axis("off")

    ax.text(
        1.5,
        2.3,
        "Confounding DAG: The Backdoor Path Identification Problem",
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
        color=COLORS["primary"],
    )

    def draw_node(x, y, text, subtext, color):
        box = patches.FancyBboxPatch(
            (x - 0.55, y - 0.35),
            1.1,
            0.7,
            boxstyle="round,pad=0.1,rounding_size=0.1",
            facecolor=color,
            edgecolor=COLORS["border"],
            linewidth=1.2,
            zorder=3,
        )
        ax.add_patch(box)
        ax.text(
            x,
            y + 0.08,
            text,
            ha="center",
            va="center",
            fontsize=11,
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
            fontsize=8.5,
            color=COLORS["text_muted"],
            zorder=4,
        )

    draw_node(1.5, 1.5, r"Confounder $Z$", "Ability / Background", "#FEF3C7")
    draw_node(0.5, 0.3, r"Treatment $D$", "Education", "#EFF6FF")
    draw_node(2.5, 0.3, r"Outcome $Y$", "Earnings", "#ECFDF5")

    # Arrows
    arrow_props_causal = dict(
        arrowstyle="-|>", mutation_scale=20, lw=2.5, color=COLORS["accent_green"]
    )
    arrow_props_confound = dict(
        arrowstyle="-|>", mutation_scale=20, lw=2.0, color=COLORS["accent_amber"]
    )

    ax.annotate(
        "", xy=(1.05, 0.3), xytext=(1.95, 0.3), arrowprops=arrow_props_causal, zorder=2
    )
    ax.text(
        1.5,
        0.45,
        r"True Causal Effect $\beta$",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
        color=COLORS["accent_green"],
    )

    ax.annotate(
        "",
        xy=(0.65, 0.65),
        xytext=(1.35, 1.2),
        arrowprops=arrow_props_confound,
        zorder=2,
    )
    ax.annotate(
        "",
        xy=(2.35, 0.65),
        xytext=(1.65, 1.2),
        arrowprops=arrow_props_confound,
        zorder=2,
    )
    ax.text(
        1.5,
        0.95,
        r"Backdoor Path: $D \leftarrow Z \rightarrow Y$",
        ha="center",
        va="center",
        fontsize=9.5,
        color=COLORS["accent_amber"],
    )

    output_path = "images/06-Econometrics/confounding_dag.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Confounding DAG showing omitted variable bias and backdoor path from treatment to outcome via confounder Z.",
    )


if __name__ == "__main__":
    generate_diagram()
