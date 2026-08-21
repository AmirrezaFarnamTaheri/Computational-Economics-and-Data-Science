"""
Generates a publication-grade Causal Tree splitting logic diagram with rigorous LaTeX math.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def generate_causal_tree_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=300)
    apply_academic_style(ax, grid=False)
    ax.set_xlim(-0.5, 5.5)
    ax.set_ylim(-0.5, 3.6)
    ax.axis("off")

    ax.text(
        2.5,
        3.3,
        "Causal Tree Recursive Partitioning (Athey & Imbens, 2016)",
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
        color=COLORS["primary"],
    )

    def draw_tree_node(x, y, title, tau_val, n_t, n_c, color):
        box = patches.FancyBboxPatch(
            (x - 0.85, y - 0.45),
            1.7,
            0.9,
            boxstyle="round,pad=0.1,rounding_size=0.1",
            facecolor=color,
            edgecolor=COLORS["border"],
            linewidth=1.2,
            zorder=3,
        )
        ax.add_patch(box)
        ax.text(
            x,
            y + 0.22,
            title,
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            color=COLORS["text_dark"],
            zorder=4,
        )
        ax.text(
            x,
            y,
            r"$\hat{\tau} = " + tau_val + r"$",
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            color=COLORS["primary"],
            zorder=4,
        )
        ax.text(
            x,
            y - 0.22,
            r"$N_{\mathrm{treated}}="
            + str(n_t)
            + r", \; N_{\mathrm{control}}="
            + str(n_c)
            + r"$",
            ha="center",
            va="center",
            fontsize=8,
            color=COLORS["text_muted"],
            zorder=4,
        )

    # Root
    draw_tree_node(2.5, 2.2, r"Parent Node $\mathcal{S}$", "+2.40", 500, 500, "#F8FAFC")

    # Split criterion
    ax.text(
        2.5,
        1.5,
        r"$\mathrm{Split \; on \; Feature } \; X_1 \leq 45.0 \quad \left(\max \; \mathrm{Heterogeneity \; of } \; \hat{\tau}\right)$",
        ha="center",
        va="center",
        fontsize=10,
        fontweight="bold",
        color=COLORS["secondary"],
    )

    # Children
    draw_tree_node(
        1.0,
        0.5,
        r"Left Leaf $\mathcal{S}_L \; (X_1 \leq 45)$",
        "+0.85",
        240,
        260,
        "#EFF6FF",
    )
    draw_tree_node(
        4.0,
        0.5,
        r"Right Leaf $\mathcal{S}_R \; (X_1 > 45)$",
        "+3.95",
        260,
        240,
        "#ECFDF5",
    )

    # Arrows
    arrow_props = dict(
        arrowstyle="-|>", mutation_scale=18, lw=1.8, color=COLORS["secondary"]
    )
    ax.annotate(
        "", xy=(1.2, 0.95), xytext=(2.2, 1.75), arrowprops=arrow_props, zorder=2
    )
    ax.annotate(
        "", xy=(3.8, 0.95), xytext=(2.8, 1.75), arrowprops=arrow_props, zorder=2
    )

    output_path = "images/causal_ml/causal_tree_split.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Causal Tree recursive partitioning maximizing treatment effect heterogeneity across subsets.",
    )


if __name__ == "__main__":
    generate_causal_tree_diagram()
