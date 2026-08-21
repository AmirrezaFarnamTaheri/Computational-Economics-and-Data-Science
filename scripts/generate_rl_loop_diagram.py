"""
Generates a publication-grade Reinforcement Learning Agent-Environment interaction loop diagram with proper LaTeX math.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.patches as patches
import matplotlib.pyplot as plt
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata


def generate_diagram():
    fig, ax = plt.subplots(figsize=(9.5, 5.2), dpi=300)
    apply_academic_style(ax, grid=False)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis("off")

    ax.text(
        5,
        5.4,
        "Markov Decision Process: Agent-Environment Interaction Loop",
        ha="center",
        va="center",
        fontsize=13,
        fontweight="bold",
        color=COLORS["primary"],
    )

    # Agent Box
    box_agent = patches.FancyBboxPatch(
        (1.0, 1.8),
        2.8,
        2.2,
        boxstyle="round,pad=0.1,rounding_size=0.1",
        facecolor="#EFF6FF",
        edgecolor=COLORS["primary"],
        linewidth=1.5,
        zorder=3,
    )
    ax.add_patch(box_agent)
    ax.text(
        2.4,
        3.2,
        "AGENT",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color=COLORS["primary"],
        zorder=4,
    )
    ax.text(
        2.4,
        2.5,
        r"Policy $\pi(a \mid s)$" + "\n" + r"Value $V(s), \; Q(s, a)$",
        ha="center",
        va="center",
        fontsize=9,
        color=COLORS["text_dark"],
        zorder=4,
    )

    # Environment Box
    box_env = patches.FancyBboxPatch(
        (6.2, 1.8),
        2.8,
        2.2,
        boxstyle="round,pad=0.1,rounding_size=0.1",
        facecolor="#ECFDF5",
        edgecolor=COLORS["accent_green"],
        linewidth=1.5,
        zorder=3,
    )
    ax.add_patch(box_env)
    ax.text(
        7.6,
        3.2,
        "ENVIRONMENT",
        ha="center",
        va="center",
        fontsize=12,
        fontweight="bold",
        color=COLORS["accent_green"],
        zorder=4,
    )
    ax.text(
        7.6,
        2.5,
        r"Transition $P(s' \mid s, a)$" + "\n" + r"Reward $R(s, a)$",
        ha="center",
        va="center",
        fontsize=9,
        color=COLORS["text_dark"],
        zorder=4,
    )

    # Action Arrow (Top: Left to Right)
    arrow_props_act = dict(
        arrowstyle="-|>", mutation_scale=18, lw=2.2, color=COLORS["primary"]
    )
    ax.annotate(
        "", xy=(6.2, 3.3), xytext=(3.8, 3.3), arrowprops=arrow_props_act, zorder=2
    )
    ax.text(
        5.0,
        3.65,
        r"Action $A_t \in \mathcal{A}(S_t)$",
        ha="center",
        va="bottom",
        fontsize=10.5,
        color=COLORS["primary"],
    )

    # State & Reward Arrow (Bottom: Right to Left)
    arrow_props_obs = dict(
        arrowstyle="-|>", mutation_scale=18, lw=2.2, color=COLORS["accent_green"]
    )
    ax.annotate(
        "", xy=(3.8, 2.3), xytext=(6.2, 2.3), arrowprops=arrow_props_obs, zorder=2
    )
    ax.text(
        5.0,
        1.65,
        r"State $S_{t+1}, \quad$ Reward $R_{t+1}$",
        ha="center",
        va="top",
        fontsize=10.5,
        color=COLORS["accent_green"],
    )

    output_path = (
        "images/03-Economic-Modeling/reinforcement_learning_agent_environment_loop.png"
    )
    save_figure(fig, output_path)
    update_metadata(
        output_path,
        "Reinforcement learning MDP agent-environment interactive feedback loop.",
    )


if __name__ == "__main__":
    generate_diagram()
