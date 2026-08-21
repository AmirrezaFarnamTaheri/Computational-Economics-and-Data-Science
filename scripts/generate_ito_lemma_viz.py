"""
Generates publication-grade geometric intuition plot for Ito's Lemma with LaTeX math.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.pyplot as plt
import numpy as np
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def generate_plot():
    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    apply_academic_style(ax, grid=True)

    x = np.linspace(0.5, 3.5, 200)

    def f(z):
        return z**2  # Convex function

    x0 = 2.0
    dx = 0.6

    ax.plot(
        x,
        f(x),
        color=COLORS["primary"],
        lw=2.5,
        label=r"Convex Payoff $f(X_t) = X_t^2$",
    )

    # First-order tangent line (Ordinary Calculus)
    tangent = f(x0) + 2 * x0 * (x - x0)
    ax.plot(
        x,
        tangent,
        color=COLORS["accent_amber"],
        linestyle="--",
        lw=1.8,
        label=r"Ordinary 1st-Order Taylor: $f'(X_t) \, dX_t$",
    )

    # Second-order curve (Ito Calculus correction)
    second_order = tangent + 0.5 * 2 * (x - x0) ** 2
    ax.plot(
        x,
        second_order,
        color=COLORS["accent_green"],
        linestyle=":",
        lw=2.0,
        label=r"$\text{It\^o Correction: } + \frac{1}{2} f''(X_t) (dX_t)^2 \text{ where } (dW_t)^2 = dt$",
    )

    # Point x0
    ax.scatter(
        [x0],
        [f(x0)],
        color=COLORS["accent_red"],
        s=70,
        zorder=5,
        label=r"Current State $X_t$",
    )
    ax.scatter([x0 + dx], [f(x0 + dx)], color=COLORS["primary"], s=50, zorder=5)

    ax.set_title(
        r"$\text{Geometric Intuition of It\^o's Lemma: Drift Correction Term } \frac{1}{2} \sigma^2 f''(X_t) \, dt$",
        fontsize=11.5,
        fontweight="bold",
        pad=15,
        color=COLORS["primary"],
    )
    ax.set_xlabel(r"Stochastic State $X_t$", fontsize=10, fontweight="bold")
    ax.set_ylabel(r"Function Value $f(X_t)$", fontsize=10, fontweight="bold")
    ax.legend(
        loc="upper left",
        frameon=True,
        facecolor="white",
        edgecolor=COLORS["border"],
        fontsize=8.5,
    )

    output_path = "images/07-Financial-Economics/ito_lemma_geometric_intuition.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Geometric intuition of Ito lemma second-order convexity correction term.",
    )


if __name__ == "__main__":
    generate_plot()
