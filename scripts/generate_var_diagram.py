"""
Generates a publication-grade Structural VAR (SVAR) identification and Cholesky ordering schematic with LaTeX math.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def generate_var_diagram():
    fig, ax = plt.subplots(figsize=(10, 6.2), dpi=300)
    apply_academic_style(ax, grid=False)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.2)
    ax.axis("off")

    ax.text(
        5,
        5.7,
        "Structural VAR Identification: Cholesky Recursive Ordering",
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
        color=COLORS["primary"],
    )

    def draw_node(x, y, label, sublabel, color):
        box = patches.FancyBboxPatch(
            (x - 1.2, y - 0.4),
            2.4,
            0.8,
            boxstyle="round,pad=0.1,rounding_size=0.1",
            facecolor=color,
            edgecolor=COLORS["border"],
            linewidth=1.2,
            zorder=3,
        )
        ax.add_patch(box)
        ax.text(
            x,
            y + 0.1,
            label,
            ha="center",
            va="center",
            fontsize=10.5,
            color=COLORS["text_dark"],
            zorder=4,
        )
        ax.text(
            x,
            y - 0.16,
            sublabel,
            ha="center",
            va="center",
            fontsize=8.5,
            color=COLORS["text_muted"],
            zorder=4,
        )

    # Shocks
    ax.text(
        2,
        4.5,
        r"Structural Shocks $u_t \sim (0, I)$",
        ha="center",
        fontsize=10,
        fontweight="bold",
        color=COLORS["secondary"],
    )
    draw_node(2, 3.5, r"$u_{\mathrm{GDP}}$ (Supply Shock)", "Slow-moving", "#EFF6FF")
    draw_node(2, 2.3, r"$u_{\pi}$ (Cost-Push Shock)", "Medium-moving", "#EFF6FF")
    draw_node(2, 1.1, r"$u_R$ (Monetary Policy Shock)", "Fast-moving", "#EFF6FF")

    # Observed Variables
    ax.text(
        8,
        4.5,
        r"Endogenous Variables $y_t$",
        ha="center",
        fontsize=10,
        fontweight="bold",
        color=COLORS["primary"],
    )
    draw_node(
        8, 3.5, r"GDP Growth ($y_{1,t}$)", r"Affected by $u_{\mathrm{GDP}}$", "#ECFDF5"
    )
    draw_node(
        8,
        2.3,
        r"Inflation ($y_{2,t}$)",
        r"Affected by $u_{\mathrm{GDP}}, u_{\pi}$",
        "#ECFDF5",
    )
    draw_node(
        8, 1.1, r"Interest Rate ($y_{3,t}$)", r"Affected by all shocks", "#ECFDF5"
    )

    arrow_props = dict(
        arrowstyle="-|>", mutation_scale=16, lw=1.8, color=COLORS["secondary"]
    )

    # Direct shocks to variables
    ax.annotate("", xy=(6.8, 3.5), xytext=(3.2, 3.5), arrowprops=arrow_props, zorder=2)
    ax.annotate("", xy=(6.8, 2.3), xytext=(3.2, 2.3), arrowprops=arrow_props, zorder=2)
    ax.annotate("", xy=(6.8, 1.1), xytext=(3.2, 1.1), arrowprops=arrow_props, zorder=2)

    # Recursive Contemporaneous Spillovers (Cholesky Lower Triangular)
    # GDP -> Inflation
    ax.annotate(
        "",
        xy=(7.2, 2.7),
        xytext=(7.2, 3.1),
        arrowprops=dict(
            arrowstyle="-|>", mutation_scale=14, lw=1.5, color=COLORS["accent_amber"]
        ),
        zorder=2,
    )
    # Inflation -> Rate
    ax.annotate(
        "",
        xy=(7.2, 1.5),
        xytext=(7.2, 1.9),
        arrowprops=dict(
            arrowstyle="-|>", mutation_scale=14, lw=1.5, color=COLORS["accent_amber"]
        ),
        zorder=2,
    )
    # GDP -> Rate
    ax.annotate(
        "",
        xy=(8.8, 1.5),
        xytext=(8.8, 3.1),
        arrowprops=dict(
            arrowstyle="-|>",
            mutation_scale=14,
            lw=1.5,
            color=COLORS["accent_amber"],
            connectionstyle="arc3,rad=-0.4",
        ),
        zorder=2,
    )

    ax.text(
        5,
        0.4,
        r"Structural Impact: $e_t = A_0^{-1} u_t \quad (A_0^{-1} \mathrm{\; Lower \; Triangular \; Factor})$",
        ha="center",
        va="center",
        fontsize=9.5,
        color=COLORS["primary"],
    )

    output_path = "images/08-Time-Series/var_identification_diagram.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Structural VAR identification schematic showing Cholesky recursive ordering from slow to fast moving variables.",
    )


if __name__ == "__main__":
    generate_var_diagram()
