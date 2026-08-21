"""
Generates a publication-grade diagram illustrating Python 3.7+ Compact Ordered Dict Memory Architecture.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def generate_ordered_dict_diagram():
    fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
    apply_academic_style(ax, grid=False)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    ax.text(
        5,
        5.5,
        "Python 3.7+ Compact & Ordered Dict Memory Layout (PyDictObject)",
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
        color=COLORS["primary"],
    )

    # Indices Array (Sparse)
    ax.text(
        1.0,
        4.3,
        "1. Sparse Indices Hash Table: [hash(key) & mask] -> index",
        fontsize=9.5,
        fontweight="bold",
        color=COLORS["secondary"],
    )
    indices = ["-1", "0", "-1", "2", "-1", "1", "-1", "-1"]
    for i, val in enumerate(indices):
        x = 1.0 + i * 1.0
        rect = patches.Rectangle(
            (x, 3.4),
            0.9,
            0.6,
            facecolor="#EFF6FF" if val != "-1" else "#F8FAFC",
            edgecolor=COLORS["border"],
            linewidth=1.2,
            zorder=3,
        )
        ax.add_patch(rect)
        ax.text(
            x + 0.45,
            3.8,
            f"idx {i}",
            ha="center",
            va="center",
            fontsize=7.5,
            color=COLORS["text_muted"],
            zorder=4,
        )
        ax.text(
            x + 0.45,
            3.55,
            val,
            ha="center",
            va="center",
            fontsize=10,
            fontweight="bold",
            color=COLORS["primary"] if val != "-1" else COLORS["border"],
            zorder=4,
        )

    # Entries Array (Dense)
    ax.text(
        1.0,
        2.5,
        "2. Dense Entries Array: insertion-order preserved [hash, key, value]",
        fontsize=9.5,
        fontweight="bold",
        color=COLORS["secondary"],
    )
    entries = [
        ("0", "hash('alpha')", "'alpha'", "100"),
        ("1", "hash('beta')", "'beta'", "200"),
        ("2", "hash('gamma')", "'gamma'", "300"),
    ]
    for row_idx, (pos, h, k, v) in enumerate(entries):
        y = 1.6 - row_idx * 0.6
        rect = patches.Rectangle(
            (1.0, y),
            8.0,
            0.48,
            facecolor="#ECFDF5",
            edgecolor=COLORS["border"],
            linewidth=1.0,
            zorder=3,
        )
        ax.add_patch(rect)
        ax.text(
            1.3,
            y + 0.24,
            f"Pos {pos}",
            fontsize=8.5,
            fontweight="bold",
            color=COLORS["accent_green"],
            zorder=4,
        )
        ax.text(
            3.0,
            y + 0.24,
            f"Hash: {h}",
            fontsize=8,
            color=COLORS["text_muted"],
            zorder=4,
        )
        ax.text(
            5.5,
            y + 0.24,
            f"Key: {k}",
            fontsize=8.5,
            fontweight="bold",
            color=COLORS["text_dark"],
            zorder=4,
        )
        ax.text(
            7.8,
            y + 0.24,
            f"Val: {v}",
            fontsize=8.5,
            fontweight="bold",
            color=COLORS["primary"],
            zorder=4,
        )

    # Connecting arrows from indices to entries
    arrow_props = dict(
        arrowstyle="-|>", mutation_scale=12, lw=1.5, color=COLORS["primary"]
    )
    ax.annotate(
        "", xy=(1.0, 1.84), xytext=(2.45, 3.4), arrowprops=arrow_props, zorder=2
    )
    ax.annotate(
        "", xy=(1.0, 1.24), xytext=(6.45, 3.4), arrowprops=arrow_props, zorder=2
    )
    ax.annotate(
        "", xy=(1.0, 0.64), xytext=(4.45, 3.4), arrowprops=arrow_props, zorder=2
    )

    output_path = "images/01-Foundations/python_ordered_dict_architecture.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Python 3.7+ compact ordered dictionary memory architecture diagram showing sparse hash table and dense entries array.",
    )


if __name__ == "__main__":
    generate_ordered_dict_diagram()
