"""
Generates publication-grade Call and Put option payoff diagrams with LaTeX math.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.pyplot as plt
import numpy as np
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def generate_plot():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), dpi=300)

    K = 100.0  # Strike price
    premium = 8.0
    S = np.linspace(60, 140, 200)

    # Call
    apply_academic_style(ax1, grid=True)
    payoff_call_long = np.maximum(S - K, 0) - premium
    payoff_call_short = -payoff_call_long

    ax1.plot(
        S,
        payoff_call_long,
        color=COLORS["primary"],
        lw=2.5,
        label=r"Long Call: $\max(S_T - K, 0) - C_0$",
    )
    ax1.plot(
        S,
        payoff_call_short,
        color=COLORS["accent_red"],
        linestyle="--",
        lw=2.0,
        label=r"Short Call: $-\max(S_T - K, 0) + C_0$",
    )
    ax1.axhline(0, color=COLORS["secondary"], lw=0.8, linestyle=":")
    ax1.axvline(
        K, color=COLORS["text_muted"], lw=1.0, linestyle="--", label=r"Strike $K = 100$"
    )
    ax1.set_title(
        r"European Call Option Payoff \& Profit at Expiry $T$",
        fontsize=11.5,
        fontweight="bold",
        color=COLORS["primary"],
    )
    ax1.set_xlabel(
        r"Underlying Asset Price at Expiry $S_T$", fontsize=10, fontweight="bold"
    )
    ax1.set_ylabel(r"Net Profit / Loss ($\$$)", fontsize=10, fontweight="bold")
    ax1.legend(
        loc="upper left",
        frameon=True,
        facecolor="white",
        edgecolor=COLORS["border"],
        fontsize=8.5,
    )

    # Put
    apply_academic_style(ax2, grid=True)
    payoff_put_long = np.maximum(K - S, 0) - premium
    payoff_put_short = -payoff_put_long

    ax2.plot(
        S,
        payoff_put_long,
        color=COLORS["accent_green"],
        lw=2.5,
        label=r"Long Put: $\max(K - S_T, 0) - P_0$",
    )
    ax2.plot(
        S,
        payoff_put_short,
        color=COLORS["accent_amber"],
        linestyle="--",
        lw=2.0,
        label=r"Short Put: $-\max(K - S_T, 0) + P_0$",
    )
    ax2.axhline(0, color=COLORS["secondary"], lw=0.8, linestyle=":")
    ax2.axvline(
        K, color=COLORS["text_muted"], lw=1.0, linestyle="--", label=r"Strike $K = 100$"
    )
    ax2.set_title(
        r"European Put Option Payoff \& Profit at Expiry $T$",
        fontsize=11.5,
        fontweight="bold",
        color=COLORS["accent_green"],
    )
    ax2.set_xlabel(
        r"Underlying Asset Price at Expiry $S_T$", fontsize=10, fontweight="bold"
    )
    ax2.set_ylabel(r"Net Profit / Loss ($\$$)", fontsize=10, fontweight="bold")
    ax2.legend(
        loc="upper right",
        frameon=True,
        facecolor="white",
        edgecolor=COLORS["border"],
        fontsize=8.5,
    )

    output_path = "images/07-Financial-Economics/option_payoffs_call_put.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "European call and put option profit-loss payoff profiles at expiration.",
    )


if __name__ == "__main__":
    generate_plot()
