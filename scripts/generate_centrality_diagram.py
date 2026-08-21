"""
Generates a publication-grade visual explanation of graph centrality measures (Degree, Betweenness, Closeness, Eigenvector).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.pyplot as plt
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def create_centrality_diagram():
    fig, axes = plt.subplots(2, 2, figsize=(11, 9), dpi=300)
    fig.suptitle(
        "Network Centrality Measures in Financial & Economic Graphs",
        fontsize=14,
        fontweight="bold",
        y=0.96,
        color=COLORS["primary"],
    )

    measures = [
        (
            "Degree Centrality",
            "Local connectivity: C_D(v) = deg(v)",
            "Node with most direct counterparty linkages",
            axes[0, 0],
            COLORS["primary"],
        ),
        (
            "Betweenness Centrality",
            r"Bridge role: C_B(v) = \sum \sigma_{st}(v) / \sigma_{st}",
            "Node on shortest path between other institutions",
            axes[0, 1],
            COLORS["accent_amber"],
        ),
        (
            "Closeness Centrality",
            r"Information speed: C_C(v) = 1 / \sum d(v, u)",
            "Node with shortest average distance to all nodes",
            axes[1, 0],
            COLORS["accent_green"],
        ),
        (
            "Eigenvector Centrality",
            r"Systemic influence: \lambda v = A v",
            "Node connected to highly connected central nodes",
            axes[1, 1],
            COLORS["accent_purple"],
        ),
    ]

    for title, formula, desc, ax, color in measures:
        apply_academic_style(ax, grid=False)
        ax.set_xlim(-1.5, 1.5)
        ax.set_ylim(-1.5, 1.5)
        ax.axis("off")
        ax.set_title(title, fontsize=11, fontweight="bold", color=color, pad=10)

        # Draw a toy 6-node network
        coords = {
            0: (0.0, 0.0),  # Center target
            1: (-0.9, 0.8),
            2: (0.9, 0.8),
            3: (-1.0, -0.6),
            4: (1.0, -0.6),
            5: (0.0, -1.1),
        }
        edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (3, 5), (4, 5)]
        for u, v in edges:
            ax.plot(
                [coords[u][0], coords[v][0]],
                [coords[u][1], coords[v][1]],
                color=COLORS["border"],
                lw=1.2,
                zorder=1,
            )

        for n, (x, y) in coords.items():
            is_target = n == 0
            c = color if is_target else "#EFF6FF"
            ec = color if is_target else COLORS["border"]
            size = 0.24 if is_target else 0.16
            circle = plt.Circle(
                (x, y), size, facecolor=c, edgecolor=ec, lw=1.5, zorder=3
            )
            ax.add_patch(circle)
            label = "Node v" if is_target else f"N_{n}"
            ax.text(
                x,
                y,
                label,
                ha="center",
                va="center",
                fontsize=8 if is_target else 6.5,
                fontweight="bold" if is_target else "normal",
                color="white" if is_target else COLORS["text_dark"],
                zorder=4,
            )

        ax.text(
            0,
            -1.35,
            f"{formula}\n{desc}",
            ha="center",
            va="center",
            fontsize=8,
            color=COLORS["text_muted"],
        )

    output_path = "images/09-Networks/network_centrality_measures.png"
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Network centrality measures comparison illustrating Degree, Betweenness, Closeness, and Eigenvector centrality.",
    )


if __name__ == "__main__":
    create_centrality_diagram()
