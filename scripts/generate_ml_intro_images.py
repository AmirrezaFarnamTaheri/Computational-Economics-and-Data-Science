"""
Generates publication-grade plots illustrating the Bias-Variance Trade-off in pure NumPy/Matplotlib.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.pyplot as plt
import numpy as np
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def generate_bias_variance_tradeoff_image():
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    apply_academic_style(ax, grid=True)

    complexity = np.linspace(1, 10, 100)

    # Theoretical curves
    bias_sq = 8.0 * np.exp(-0.6 * complexity) + 0.2
    variance = 0.15 * np.exp(0.45 * complexity)
    irreducible_noise = 0.5 * np.ones_like(complexity)
    total_error = bias_sq + variance + irreducible_noise

    ax.plot(
        complexity,
        bias_sq,
        color=COLORS["primary"],
        lw=2.2,
        label=r"$\text{Bias}^2$ (Underfitting Risk)",
    )
    ax.plot(
        complexity,
        variance,
        color=COLORS["accent_red"],
        lw=2.2,
        label=r"$\text{Variance}$ (Overfitting Risk)",
    )
    ax.plot(
        complexity,
        irreducible_noise,
        color=COLORS["text_muted"],
        lw=1.5,
        linestyle=":",
        label=r"Irreducible Error $\sigma^2$",
    )
    ax.plot(
        complexity,
        total_error,
        color=COLORS["accent_purple"],
        lw=2.8,
        label=r"Total Expected Test Error $\text{MSE}$",
    )

    # Optimal complexity vertical line
    opt_idx = np.argmin(total_error)
    opt_comp = complexity[opt_idx]
    ax.axvline(
        opt_comp,
        color=COLORS["accent_amber"],
        linestyle="--",
        lw=1.8,
        label=f"Optimal Complexity (d*={opt_comp:.1f})",
    )

    ax.set_title(
        "The Fundamental Bias-Variance Trade-off in Machine Learning",
        fontsize=13,
        fontweight="bold",
        pad=15,
        color=COLORS["primary"],
    )
    ax.set_xlabel(
        "Model Complexity / Capacity (Polynomial Degree d)",
        fontsize=11,
        fontweight="bold",
    )
    ax.set_ylabel("Expected Prediction Error", fontsize=11, fontweight="bold")
    ax.set_ylim(0, 10)
    ax.legend(
        frameon=True,
        facecolor="white",
        edgecolor=COLORS["border"],
        fontsize=9.5,
        loc="upper right",
    )

    output_path = "images/07-Machine-Learning/figure1_bias_variance_tradeoff.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Bias-variance trade-off curve illustrating underfitting, overfitting, and optimal model capacity.",
    )


if __name__ == "__main__":
    generate_bias_variance_tradeoff_image()
