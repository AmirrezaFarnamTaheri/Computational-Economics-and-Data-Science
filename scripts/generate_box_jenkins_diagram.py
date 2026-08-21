"""
Generates a publication-grade Box-Jenkins time series modeling methodology flowchart.
"""

import sys
from pathlib import Path

import matplotlib.patches as patches
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def generate_box_jenkins_diagram():
    fig, ax = plt.subplots(figsize=(9, 10), dpi=300)
    apply_academic_style(ax, grid=False)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 11)
    ax.axis("off")

    ax.text(
        5,
        10.4,
        "Box-Jenkins Time Series Methodology (ARIMA / SARIMA)",
        ha="center",
        va="center",
        fontsize=14,
        fontweight="bold",
        color=COLORS["primary"],
    )

    def draw_step(
        x,
        y,
        w,
        h,
        title,
        details,
        color="#F8FAFC",
        border=COLORS["border"],
        is_decision=False,
    ):
        if is_decision:
            diamond = patches.Polygon(
                [
                    [x + w / 2, y],
                    [x + w, y + h / 2],
                    [x + w / 2, y + h],
                    [x, y + h / 2],
                ],
                closed=True,
                facecolor=color,
                edgecolor=COLORS["primary"],
                linewidth=1.5,
                zorder=3,
            )
            ax.add_patch(diamond)
            ax.text(
                x + w / 2,
                y + h / 2 + 0.1,
                title,
                ha="center",
                va="center",
                fontsize=10,
                fontweight="bold",
                color=COLORS["primary"],
                zorder=4,
            )
            ax.text(
                x + w / 2,
                y + h / 2 - 0.25,
                details,
                ha="center",
                va="center",
                fontsize=8.5,
                color=COLORS["text_muted"],
                zorder=4,
            )
        else:
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
                y + h * 0.65,
                title,
                ha="center",
                va="center",
                fontsize=10.5,
                fontweight="bold",
                color=COLORS["text_dark"],
                zorder=4,
            )
            ax.text(
                x + w / 2,
                y + h * 0.32,
                details,
                ha="center",
                va="center",
                fontsize=8.5,
                color=COLORS["text_muted"],
                zorder=4,
            )

    draw_step(
        1.5,
        8.8,
        7.0,
        1.1,
        "1. Model Identification & Stationarity",
        "ADF / KPSS tests, transformations (log, diff d), inspect ACF & PACF signatures for (p, q)",
        "#EFF6FF",
    )
    draw_step(
        1.5,
        7.0,
        7.0,
        1.1,
        "2. Parameter Estimation",
        "Estimate AR and MA coefficients via Maximum Likelihood Estimation (MLE) or CSS",
        "#F8FAFC",
    )
    draw_step(
        1.5,
        5.2,
        7.0,
        1.1,
        "3. Diagnostic Checking",
        "Ljung-Box Q-test, residual white noise ACF, normality, AIC / BIC model selection",
        "#F8FAFC",
    )
    draw_step(
        2.0,
        3.1,
        6.0,
        1.4,
        "Residuals White Noise?",
        "Pass Ljung-Box test at all lags",
        "#FEF3C7",
        is_decision=True,
    )
    draw_step(
        1.5,
        1.1,
        7.0,
        1.1,
        "4. Forecasting & Policy Analysis",
        "Generate point forecasts, confidence intervals, and dynamic impulse response functions",
        "#ECFDF5",
        border=COLORS["accent_green"],
    )

    arrow_props = dict(
        arrowstyle="-|>", mutation_scale=16, lw=1.8, color=COLORS["secondary"]
    )
    ax.annotate("", xy=(5, 8.1), xytext=(5, 8.8), arrowprops=arrow_props, zorder=2)
    ax.annotate("", xy=(5, 6.3), xytext=(5, 7.0), arrowprops=arrow_props, zorder=2)
    ax.annotate("", xy=(5, 4.5), xytext=(5, 5.2), arrowprops=arrow_props, zorder=2)
    ax.annotate("", xy=(5, 2.2), xytext=(5, 3.1), arrowprops=arrow_props, zorder=2)
    ax.text(
        5.2,
        2.6,
        "Yes (Adequate)",
        fontsize=9,
        fontweight="bold",
        color=COLORS["accent_green"],
    )

    # Loop back
    ax.annotate(
        "",
        xy=(8.5, 9.35),
        xytext=(8.0, 3.8),
        arrowprops=dict(
            arrowstyle="-|>",
            mutation_scale=16,
            lw=1.8,
            color=COLORS["accent_red"],
            connectionstyle="arc3,rad=-0.3",
        ),
        zorder=2,
    )
    ax.text(
        8.8,
        6.5,
        "No: Modify (p, d, q)\nRe-identify model",
        fontsize=9,
        fontweight="bold",
        color=COLORS["accent_red"],
        ha="left",
    )

    output_path = "images/08-Time-Series/box_jenkins_flowchart.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Box-Jenkins time series iterative identification, estimation, diagnostic checking, and forecasting methodology.",
    )


if __name__ == "__main__":
    generate_box_jenkins_diagram()
