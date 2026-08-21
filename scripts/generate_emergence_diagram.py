"""
Generates a publication-grade diagram illustrating Emergence across Micro, Meso, and Macro scales.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def create_emergence_diagram():
    fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
    apply_academic_style(ax, grid=False)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis("off")

    ax.text(
        5,
        6.5,
        "The Concept of Emergence in Complex Economic Systems",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color=COLORS["primary"],
    )

    def draw_tier(y, title, subtitle, examples, color, border):
        box = patches.FancyBboxPatch(
            (1.0, y),
            8.0,
            1.4,
            boxstyle="round,pad=0.1,rounding_size=0.1",
            facecolor=color,
            edgecolor=border,
            linewidth=1.4,
            zorder=3,
        )
        ax.add_patch(box)
        ax.text(
            1.3,
            y + 1.0,
            title,
            ha="left",
            va="center",
            fontsize=11,
            fontweight="bold",
            color=COLORS["text_dark"],
            zorder=4,
        )
        ax.text(
            1.3,
            y + 0.65,
            subtitle,
            ha="left",
            va="center",
            fontsize=9,
            color=COLORS["text_muted"],
            zorder=4,
        )
        ax.text(
            1.3,
            y + 0.3,
            f"Examples: {examples}",
            ha="left",
            va="center",
            fontsize=8.5,
            fontstyle="italic",
            color=COLORS["primary"],
            zorder=4,
        )

    draw_tier(
        4.6,
        "MACRO LEVEL: Emergent System Phenomena",
        "Non-linear global properties not present in individual components",
        "Market clearing, financial crashes, price dispersion, spontaneous order",
        "#ECFDF5",
        COLORS["accent_green"],
    )

    draw_tier(
        2.6,
        "MESO LEVEL: Organizational Patterns & Networks",
        "Intermediate self-organizing clusters and interaction topologies",
        "Interbank lending networks, supply chain cascades, spatial clustering (Schelling)",
        "#FEF3C7",
        COLORS["accent_amber"],
    )

    draw_tier(
        0.6,
        "MICRO LEVEL: Individual Agent Decision Rules",
        "Decentralized autonomous agents following local optimization and heuristics",
        "Bounded rationality, utility maximization, local trade, imitation rules",
        "#EFF6FF",
        COLORS["primary"],
    )

    # Bottom-up Emergence Arrow
    ax.annotate(
        "",
        xy=(0.5, 5.5),
        xytext=(0.5, 1.0),
        arrowprops=dict(
            arrowstyle="-|>", mutation_scale=20, lw=2.5, color=COLORS["accent_green"]
        ),
        zorder=2,
    )
    ax.text(
        0.35,
        3.3,
        "BOTTOM-UP\nEMERGENCE",
        ha="center",
        va="center",
        rotation=90,
        fontsize=10,
        fontweight="bold",
        color=COLORS["accent_green"],
    )

    # Top-down Downward Causation Arrow
    ax.annotate(
        "",
        xy=(9.5, 1.0),
        xytext=(9.5, 5.5),
        arrowprops=dict(
            arrowstyle="-|>",
            mutation_scale=20,
            lw=2.0,
            linestyle="--",
            color=COLORS["accent_amber"],
        ),
        zorder=2,
    )
    ax.text(
        9.65,
        3.3,
        "TOP-DOWN\nFEEDBACK",
        ha="center",
        va="center",
        rotation=-90,
        fontsize=9.5,
        fontweight="bold",
        color=COLORS["accent_amber"],
    )

    output_path = "images/10-Specialized/emergence_hierarchy_concept.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Emergence hierarchy schematic showing micro agent rules, meso networks, and macro macroeconomic equilibria.",
    )


if __name__ == "__main__":
    create_emergence_diagram()
