"""
Generates a visualization of expanding window cross-validation (TimeSeriesSplit) in pure NumPy/Matplotlib.
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def generate_timeseries_split_plot():
    fig, axes = plt.subplots(5, 1, figsize=(10, 8), dpi=300, sharex=True)
    fig.suptitle(
        "Expanding Window Cross-Validation for Time Series",
        fontsize=14,
        fontweight="bold",
        y=0.96,
        color=COLORS["primary"],
    )

    np.random.seed(101)
    n_points = 150
    t = np.arange(n_points)
    y = 0.5 * t + 15 * np.sin(t * 2 * np.pi / 30) + np.random.randn(n_points) * 4 + 30

    n_splits = 5
    test_size = n_points // (n_splits + 1)

    for i in range(n_splits):
        ax = axes[i]
        apply_academic_style(ax, grid=True)

        train_end = (i + 1) * test_size
        test_end = train_end + test_size

        # Full series in muted gray
        ax.plot(
            t, y, color=COLORS["grid"], lw=1.2, label="Full Series" if i == 0 else None
        )

        # Train data
        ax.plot(
            t[:train_end],
            y[:train_end],
            color=COLORS["primary"],
            lw=2.0,
            label="Training Fold" if i == 0 else None,
        )

        # Test data
        ax.plot(
            t[train_end:test_end],
            y[train_end:test_end],
            color=COLORS["accent_red"],
            lw=2.0,
            linestyle="--",
            label="Test Fold (Evaluation)" if i == 0 else None,
        )

        ax.set_ylabel(
            f"Fold {i + 1}", fontsize=9, fontweight="bold", color=COLORS["text_dark"]
        )
        ax.set_yticks([])

    axes[-1].set_xlabel(
        "Time Index (t)", fontsize=11, fontweight="bold", color=COLORS["text_dark"]
    )
    axes[0].legend(
        loc="upper left",
        frameon=True,
        facecolor="white",
        edgecolor=COLORS["border"],
        fontsize=8.5,
    )

    output_path = "images/08-Time-Series/timeseries_cross_validation_splits.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Expanding window time series cross-validation diagram showing non-overlapping forward test splits.",
    )


if __name__ == "__main__":
    generate_timeseries_split_plot()
