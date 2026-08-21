"""
Generates publication-grade Capital Market Line (CML) and Security Market Line (SML) plots with LaTeX math.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.pyplot as plt
import numpy as np
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def generate_plot():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), dpi=300)

    # --- CML (Total Risk: sigma) ---
    apply_academic_style(ax1, grid=True)
    rf = 0.03
    rm = 0.10
    sigma_m = 0.15
    sharpe = (rm - rf) / sigma_m

    sigma_p = np.linspace(0, 0.35, 100)
    cml = rf + sharpe * sigma_p

    # Efficient frontier curve
    sigma_f = np.linspace(0.12, 0.35, 100)
    er_f = 0.05 + 0.25 * np.sqrt(sigma_f - 0.11)

    ax1.plot(
        sigma_f,
        er_f,
        color=COLORS["secondary"],
        linestyle="--",
        lw=1.8,
        label="Markowitz Efficient Frontier",
    )
    ax1.plot(
        sigma_p,
        cml,
        color=COLORS["primary"],
        lw=2.5,
        label=r"Capital Market Line: $\mathbb{E}[R_p] = R_f + \frac{\mathbb{E}[R_m] - R_f}{\sigma_m} \sigma_p$",
    )
    ax1.scatter([0, sigma_m], [rf, rm], color=COLORS["accent_red"], s=70, zorder=5)
    ax1.annotate(
        r"Risk-Free Asset $(0, R_f)$",
        (0, rf),
        xytext=(10, -5),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold",
    )
    ax1.annotate(
        r"Market Portfolio $M (\sigma_m, \mathbb{E}[R_m])$",
        (sigma_m, rm),
        xytext=(10, -5),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold",
    )

    ax1.set_title(
        r"Capital Market Line (CML) --- Efficient Portfolios",
        fontsize=12,
        fontweight="bold",
        color=COLORS["primary"],
    )
    ax1.set_xlabel(
        r"Total Risk ($\text{Standard Deviation } \sigma_p$)",
        fontsize=10,
        fontweight="bold",
    )
    ax1.set_ylabel(r"Expected Return $\mathbb{E}[R_p]$", fontsize=10, fontweight="bold")
    ax1.set_xlim(0, 0.35)
    ax1.set_ylim(0, 0.20)
    ax1.legend(
        loc="upper left",
        frameon=True,
        facecolor="white",
        edgecolor=COLORS["border"],
        fontsize=8.5,
    )

    # --- SML (Systematic Risk: beta) ---
    apply_academic_style(ax2, grid=True)
    beta = np.linspace(0, 2.0, 100)
    sml = rf + beta * (rm - rf)

    ax2.plot(
        beta,
        sml,
        color=COLORS["accent_green"],
        lw=2.5,
        label=r"Security Market Line: $\mathbb{E}[R_i] = R_f + \beta_i (\mathbb{E}[R_m] - R_f)$",
    )
    ax2.scatter([0, 1.0], [rf, rm], color=COLORS["accent_red"], s=70, zorder=5)
    ax2.annotate(
        r"Risk-Free Asset $(0, R_f)$",
        (0, rf),
        xytext=(10, -5),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold",
    )
    ax2.annotate(
        r"Market Portfolio $(\beta=1, \mathbb{E}[R_m])$",
        (1.0, rm),
        xytext=(10, -5),
        textcoords="offset points",
        fontsize=9,
        fontweight="bold",
    )

    # Alpha assets
    ax2.scatter(
        [1.2],
        [0.14],
        color=COLORS["accent_purple"],
        s=60,
        zorder=5,
        label=r"Underpriced Asset ($\alpha > 0$)",
    )
    ax2.scatter(
        [0.8],
        [0.06],
        color=COLORS["accent_amber"],
        s=60,
        zorder=5,
        label=r"Overpriced Asset ($\alpha < 0$)",
    )

    ax2.set_title(
        r"Security Market Line (SML) --- All Individual Assets",
        fontsize=12,
        fontweight="bold",
        color=COLORS["accent_green"],
    )
    ax2.set_xlabel(
        r"Systematic Risk ($\text{Beta } \beta_i = \frac{\text{Cov}(R_i, R_m)}{\sigma_m^2}$)",
        fontsize=10,
        fontweight="bold",
    )
    ax2.set_ylabel(r"Expected Return $\mathbb{E}[R_i]$", fontsize=10, fontweight="bold")
    ax2.set_xlim(0, 2.0)
    ax2.set_ylim(0, 0.20)
    ax2.legend(
        loc="upper left",
        frameon=True,
        facecolor="white",
        edgecolor=COLORS["border"],
        fontsize=8.5,
    )

    output_path = "images/07-Financial-Economics/cml_vs_sml_plot.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Comparison of Capital Market Line (total risk) vs Security Market Line (systematic beta risk) in CAPM.",
    )


if __name__ == "__main__":
    generate_plot()
