"""
Generates a stylized plot showing the breakdown of the stable Phillips Curve relationship in the 1970s (Lucas Critique).
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def main():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    apply_academic_style(ax, grid=True)

    np.random.seed(42)

    # 1960s Data: Stable downward sloping trade-off
    u_60s = np.linspace(3.5, 7.0, 10)
    inf_60s = 8.0 - 1.1 * u_60s + np.random.normal(0, 0.3, len(u_60s))
    years_60s = np.arange(1960, 1970)

    # 1970s Data: Stagflation shifts outward
    u_70s = np.array([4.9, 5.9, 5.6, 4.9, 5.6, 8.5, 7.7, 7.1, 6.1, 5.8])
    inf_70s = np.array([5.7, 4.4, 3.2, 6.2, 11.0, 9.1, 5.8, 6.5, 7.6, 11.3])
    years_70s = np.arange(1970, 1980)

    # Plot 1960s
    ax.scatter(
        u_60s,
        inf_60s,
        color=COLORS["primary"],
        s=60,
        label="1960s (Stable Trade-off)",
        zorder=4,
    )
    z60 = np.polyfit(u_60s, inf_60s, 1)
    p60 = np.poly1d(z60)
    u_line = np.linspace(3.0, 9.0, 100)
    ax.plot(
        u_line, p60(u_line), color=COLORS["primary"], linestyle="--", lw=1.8, alpha=0.8
    )

    for i, txt in enumerate(years_60s):
        ax.annotate(
            str(txt)[2:],
            (u_60s[i], inf_60s[i]),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=8,
            color=COLORS["primary"],
        )

    # Plot 1970s
    ax.scatter(
        u_70s,
        inf_70s,
        color=COLORS["accent_red"],
        s=60,
        label="1970s (Stagflation / Lucas Critique)",
        zorder=4,
    )
    for i, txt in enumerate(years_70s):
        ax.annotate(
            str(txt)[2:],
            (u_70s[i], inf_70s[i]),
            textcoords="offset points",
            xytext=(0, 6),
            ha="center",
            fontsize=8,
            color=COLORS["accent_red"],
        )

    # Connect 1970s path to show shift
    ax.plot(
        u_70s, inf_70s, color=COLORS["accent_red"], alpha=0.3, lw=1.2, linestyle=":"
    )

    ax.set_title(
        "The Breakdown of the Phillips Curve (1960-1979) and the Lucas Critique",
        fontsize=13,
        fontweight="bold",
        pad=15,
        color=COLORS["primary"],
    )
    ax.set_xlabel("Unemployment Rate (%)", fontsize=11, fontweight="bold")
    ax.set_ylabel("Inflation Rate (%)", fontsize=11, fontweight="bold")
    ax.legend(frameon=True, facecolor="white", edgecolor=COLORS["border"], fontsize=10)

    output_path = "images/01-Foundations/1.1-phillips-curve-breakdown.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Empirical breakdown of the Phillips curve during 1970s stagflation illustrating the Lucas critique.",
    )


if __name__ == "__main__":
    main()
