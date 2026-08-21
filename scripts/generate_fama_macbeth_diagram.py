"""
Generates a publication-grade schematic of the Fama-MacBeth (1973) Two-Pass Regression Procedure.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def generate_fama_macbeth_diagram():
    fig, ax = plt.subplots(figsize=(10, 8), dpi=300)
    apply_academic_style(ax, grid=False)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 9)
    ax.axis("off")

    ax.text(
        5,
        8.5,
        "Fama-MacBeth (1973) Two-Pass Asset Pricing Procedure",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color=COLORS["primary"],
    )

    def draw_card(x, y, w, h, title, lines, color="#F8FAFC", border=COLORS["border"]):
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
            y + h - 0.25,
            title,
            ha="center",
            va="center",
            fontsize=10.5,
            fontweight="bold",
            color=COLORS["primary"],
            zorder=4,
        )
        for i, line in enumerate(lines):
            ax.text(
                x + w / 2,
                y + h - 0.55 - i * 0.28,
                line,
                ha="center",
                va="center",
                fontsize=8.5,
                color=COLORS["text_dark"],
                zorder=4,
            )

    # Pass 1
    draw_card(
        0.5,
        5.0,
        9.0,
        2.7,
        "PASS 1: N Time-Series Regressions (Estimate Factor Betas)",
        [
            r"For each asset i = 1, ..., N, regress excess returns on factor realizations across t = 1, ..., T:",
            r"R_{i,t} - R_{f,t} = \alpha_i + \beta_{i,MKT} f_{MKT,t} + \beta_{i,SMB} f_{SMB,t} + ... + \epsilon_{i,t}",
            r"Output: Estimated factor exposures \hat{\beta}_i = [\hat{\beta}_{i,1}, ..., \hat{\beta}_{i,K}] for all N assets",
        ],
        color="#EFF6FF",
    )

    # Pass 2
    draw_card(
        0.5,
        2.0,
        9.0,
        2.4,
        "PASS 2: T Cross-Sectional Regressions (Estimate Risk Premia)",
        [
            r"At each time period t = 1, ..., T, regress cross-section of returns on estimated betas \hat{\beta}_i:",
            r"R_{i,t} - R_{f,t} = \lambda_{0,t} + \lambda_{1,t} \hat{\beta}_{i,1} + ... + \lambda_{K,t} \hat{\beta}_{i,K} + \eta_{i,t}",
            r"Output: Time-series of estimated factor risk premia \hat{\lambda}_t = [\hat{\lambda}_{1,t}, ..., \hat{\lambda}_{K,t}]",
        ],
        color="#F8FAFC",
    )

    # Final Average
    draw_card(
        1.5,
        0.2,
        7.0,
        1.3,
        "FINAL ESTIMATE: Average Risk Premia & Standard Errors",
        [
            r"\hat{\lambda}_k = \frac{1}{T} \sum_{t=1}^T \hat{\lambda}_{k,t},   \sigma^2(\hat{\lambda}_k) = \frac{1}{T^2} \sum_{t=1}^T (\hat{\lambda}_{k,t} - \hat{\lambda}_k)^2",
            r"t-statistic: t = \hat{\lambda}_k / \text{SE}(\hat{\lambda}_k)  [with Shanken (1992) EIV correction]",
        ],
        color="#ECFDF5",
        border=COLORS["accent_green"],
    )

    arrow_props = dict(
        arrowstyle="-|>", mutation_scale=16, lw=1.8, color=COLORS["secondary"]
    )
    ax.annotate("", xy=(5, 4.4), xytext=(5, 5.0), arrowprops=arrow_props, zorder=2)
    ax.annotate("", xy=(5, 1.5), xytext=(5, 2.0), arrowprops=arrow_props, zorder=2)

    output_path = "images/07-Financial-Economics/fama_macbeth_twopass_procedure.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Fama-MacBeth (1973) two-pass cross-sectional regression procedure schematic.",
    )


if __name__ == "__main__":
    generate_fama_macbeth_diagram()
