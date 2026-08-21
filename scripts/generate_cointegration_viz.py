"""
Generates publication-grade visualization of Cointegration and Error Correction (Engle-Granger) with LaTeX math.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.pyplot as plt
import numpy as np
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def generate_plot():
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 7), dpi=300, sharex=True)

    np.random.seed(42)
    n = 200
    t = np.arange(n)

    # Common non-stationary trend I(1)
    common_trend = np.cumsum(np.random.normal(0, 1, n))
    noise1 = np.random.normal(0, 0.5, n)
    noise2 = np.random.normal(0, 0.5, n)

    # Cointegrated series y1, y2
    y1 = common_trend + noise1 + 10.0
    y2 = 1.5 * common_trend + noise2 + 5.0
    stationary_spread = y2 - 1.5 * y1  # Stationary linear combination I(0)

    # Top: Non-stationary series
    apply_academic_style(ax1, grid=True)
    ax1.plot(
        t,
        y1,
        color=COLORS["primary"],
        lw=2.0,
        label=r"Series $Y_{1,t} \sim I(1)$ (Random Walk with Drift)",
    )
    ax1.plot(
        t,
        y2,
        color=COLORS["accent_purple"],
        lw=2.0,
        label=r"Series $Y_{2,t} \sim I(1)$ (Cointegrated with $Y_{1,t}$)",
    )
    ax1.set_title(
        r"Engle--Granger Cointegration: Non-Stationary Processes Sharing Common Stochastic Trend",
        fontsize=12,
        fontweight="bold",
        pad=10,
        color=COLORS["primary"],
    )
    ax1.set_ylabel(r"Price Levels ($Y_t$)", fontsize=10, fontweight="bold")
    ax1.legend(
        loc="upper left",
        frameon=True,
        facecolor="white",
        edgecolor=COLORS["border"],
        fontsize=9,
    )

    # Bottom: Stationary spread
    apply_academic_style(ax2, grid=True)
    ax2.plot(
        t,
        stationary_spread,
        color=COLORS["accent_green"],
        lw=1.8,
        label=r"Cointegrating Residual: $z_t = Y_{2,t} - 1.5 Y_{1,t} \sim I(0)$ (Mean-Reverting)",
    )
    ax2.axhline(
        np.mean(stationary_spread),
        color=COLORS["accent_red"],
        linestyle="--",
        lw=1.2,
        label=r"Long-Run Mean $\mathbb{E}[z_t]$",
    )
    ax2.set_xlabel(r"Time Index ($t$)", fontsize=10, fontweight="bold")
    ax2.set_ylabel(r"Spread Resid ($z_t$)", fontsize=10, fontweight="bold")
    ax2.legend(
        loc="upper left",
        frameon=True,
        facecolor="white",
        edgecolor=COLORS["border"],
        fontsize=9,
    )

    output_path = "images/08-Time-Series/cointegration_analysis.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Engle-Granger cointegration analysis showing I(1) series and stationary mean-reverting spread I(0).",
    )


if __name__ == "__main__":
    generate_plot()
