"""
Generates all 13 mathematical and econometric appendix diagrams with clean academic styling.
"""

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import matplotlib.pyplot as plt
import numpy as np
from diagram_style import COLORS, apply_academic_style, save_figure, update_metadata
from scipy.stats import norm

OUTPUT_DIR = "images/Appendix"
DPI = 300
FIG_SIZE = (9, 5.5)


def save_plot(fig, filename):
    """Save a plot cleanly to images/Appendix/."""
    basename = os.path.basename(filename)
    path = os.path.join(OUTPUT_DIR, basename)
    save_figure(fig, path, dpi=DPI)
    update_metadata(path, f"Appendix mathematical visualization: {basename}")


def setup_plot(title, xlabel, ylabel, fig_size=FIG_SIZE):
    """Set up a standard plot with consistent academic styling."""
    fig, ax = plt.subplots(figsize=fig_size, dpi=DPI)
    apply_academic_style(ax, grid=True)
    ax.set_title(title, fontsize=12, fontweight="bold", pad=15, color=COLORS["primary"])
    ax.set_xlabel(xlabel, fontsize=10, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=10, fontweight="bold")
    return fig, ax


def generate_convergence_rates():
    fig, ax = setup_plot(
        "Convergence Rates of Optimization Sequences",
        r"Iteration $k$",
        r"Error $\|x_k - x^*\|$",
    )
    k = np.arange(1, 16)
    linear = 0.5**k
    superlinear = 0.5 ** (k**1.3)
    quadratic = 0.5 ** (2**k)

    ax.semilogy(
        k,
        linear,
        label=r"Linear ($q=1, \mu=0.5$)",
        color=COLORS["primary"],
        marker="o",
        lw=1.8,
    )
    ax.semilogy(
        k,
        superlinear,
        label=r"Superlinear ($q=1.3$)",
        color=COLORS["accent_green"],
        marker="s",
        lw=1.8,
    )
    ax.semilogy(
        k,
        quadratic,
        label=r"Quadratic ($q=2$, Newton's Method)",
        color=COLORS["accent_red"],
        marker="^",
        lw=2.0,
    )
    ax.legend(frameon=True, facecolor="white", edgecolor=COLORS["border"], fontsize=9.5)
    save_plot(fig, "convergence_rates.png")


def generate_intermediate_value_theorem():
    fig, ax = setup_plot("Intermediate Value Theorem (Bolzano)", r"$x$", r"$f(x)$")
    x = np.linspace(0, 3, 200)
    f = x**3 - 2 * x - 2
    ax.plot(x, f, color=COLORS["primary"], lw=2.2, label=r"$f(x) = x^3 - 2x - 2$")
    ax.axhline(0, color=COLORS["secondary"], lw=1.0, linestyle="--")

    a, b = 1.0, 2.5
    fa, fb = a**3 - 2 * a - 2, b**3 - 2 * b - 2
    c = 1.7692923542386314

    ax.scatter([a, b], [fa, fb], color=COLORS["accent_red"], s=50, zorder=5)
    ax.scatter(
        [c],
        [0],
        color=COLORS["accent_green"],
        s=70,
        zorder=5,
        label=r"Root $c \in (a, b)$ where $f(c)=0$",
    )
    ax.legend(frameon=True, facecolor="white", edgecolor=COLORS["border"], fontsize=9.5)
    save_plot(fig, "intermediate_value_theorem.png")


def generate_convex_sets():
    fig, ax = setup_plot(
        "Convex Set Definition: Line Segment Property",
        r"$x_1$",
        r"$x_2$",
        fig_size=(6, 6),
    )
    circle = plt.Circle(
        (0.5, 0.5), 0.35, facecolor="#EFF6FF", edgecolor=COLORS["primary"], lw=1.8
    )
    ax.add_patch(circle)

    p1, p2 = np.array([0.3, 0.4]), np.array([0.7, 0.6])
    ax.plot(
        [p1[0], p2[0]],
        [p1[1], p2[1]],
        color=COLORS["accent_green"],
        lw=2.2,
        label=r"$\lambda x + (1-\lambda)y \in C$",
    )
    ax.scatter(
        [p1[0], p2[0]], [p1[1], p2[1]], color=COLORS["accent_green"], s=50, zorder=5
    )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(frameon=True, facecolor="white", edgecolor=COLORS["border"], fontsize=9.5)
    save_plot(fig, "convex_set.png")


def generate_separating_hyperplane():
    fig, ax = setup_plot(
        "Separating Hyperplane Theorem for Disjoint Convex Sets",
        r"$x_1$",
        r"$x_2$",
        fig_size=(7, 6),
    )
    c1 = plt.Circle(
        (0.3, 0.7),
        0.2,
        facecolor="#EFF6FF",
        edgecolor=COLORS["primary"],
        lw=1.5,
        label="Convex Set C",
    )
    c2 = plt.Circle(
        (0.7, 0.3),
        0.2,
        facecolor="#FEF2F2",
        edgecolor=COLORS["accent_red"],
        lw=1.5,
        label="Convex Set D",
    )
    ax.add_patch(c1)
    ax.add_patch(c2)

    # Separating line
    x_line = np.linspace(0.1, 0.9, 100)
    y_line = x_line
    ax.plot(
        x_line,
        y_line,
        color=COLORS["secondary"],
        lw=2.0,
        linestyle="--",
        label=r"Hyperplane $a^T x = b$",
    )
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(frameon=True, facecolor="white", edgecolor=COLORS["border"], fontsize=9.5)
    save_plot(fig, "separating_hyperplane_theorem.png")


def generate_taylor_sin():
    fig, ax = setup_plot(
        r"Taylor Polynomial Approximations of $\sin(x)$ around $x_0=0$",
        r"$x$",
        r"$f(x)$",
    )
    x = np.linspace(-np.pi, np.pi, 200)
    ax.plot(x, np.sin(x), color=COLORS["primary"], lw=2.5, label=r"$\sin(x)$")
    ax.plot(
        x,
        x,
        color=COLORS["accent_amber"],
        lw=1.8,
        linestyle="--",
        label=r"Order 1: $P_1(x) = x$",
    )
    ax.plot(
        x,
        x - x**3 / 6.0,
        color=COLORS["accent_red"],
        lw=1.8,
        linestyle="-.",
        label=r"Order 3: $P_3(x) = x - \frac{x^3}{6}$",
    )
    ax.plot(
        x,
        x - x**3 / 6.0 + x**5 / 120.0,
        color=COLORS["accent_green"],
        lw=2.0,
        linestyle=":",
        label=r"Order 5: $P_5(x) = x - \frac{x^3}{6} + \frac{x^5}{120}$",
    )
    ax.set_ylim(-1.5, 1.5)
    ax.legend(frameon=True, facecolor="white", edgecolor=COLORS["border"], fontsize=9)
    save_plot(fig, "taylor_sin.png")


def generate_gradient_field():
    fig, ax = setup_plot(
        "Gradient Vector Field $\\nabla f(x, y)$ of Rosenbrock-like Function",
        r"$x$",
        r"$y$",
        fig_size=(7, 6),
    )
    x = np.linspace(-2, 2, 20)
    y = np.linspace(-2, 2, 20)
    X, Y = np.meshgrid(x, y)
    U = -2 * X
    V = -2 * Y
    ax.quiver(X, Y, U, V, color=COLORS["primary"], alpha=0.8)
    save_plot(fig, "gradient_field.png")


def generate_comparative_statics():
    fig, ax = setup_plot(
        "Comparative Statics: Shift in Equilibrium Prices and Quantities",
        r"Quantity $Q$",
        r"Price $P$",
    )
    q = np.linspace(0, 10, 100)
    demand_0 = 10 - q
    demand_1 = 12 - q
    supply = 2 + q

    ax.plot(q, demand_0, color=COLORS["primary"], lw=2.0, label="Initial Demand $D_0$")
    ax.plot(
        q,
        demand_1,
        color=COLORS["accent_purple"],
        lw=2.0,
        linestyle="--",
        label="Increased Demand $D_1$",
    )
    ax.plot(q, supply, color=COLORS["accent_green"], lw=2.0, label="Supply Curve $S$")
    ax.legend(frameon=True, facecolor="white", edgecolor=COLORS["border"], fontsize=9.5)
    save_plot(fig, "comparative_statics.png")


def generate_normal_plots():
    fig, ax = setup_plot(
        "Standard Normal Distribution PDF and Critical Regions", r"$z$", r"$\phi(z)$"
    )
    z = np.linspace(-4, 4, 300)
    pdf = norm.pdf(z)
    ax.plot(
        z,
        pdf,
        color=COLORS["primary"],
        lw=2.2,
        label=r"$\phi(z) = \frac{1}{\sqrt{2\pi}} e^{-z^2/2}$",
    )
    ax.fill_between(
        z,
        pdf,
        where=(np.abs(z) > 1.96),
        color=COLORS["accent_red"],
        alpha=0.3,
        label=r"Critical Rejection Region ($\alpha=0.05$)",
    )
    ax.legend(frameon=True, facecolor="white", edgecolor=COLORS["border"], fontsize=9.5)
    save_plot(fig, "normal_pdf.png")


def generate_jensen_inequality():
    fig, ax = setup_plot(
        "Jensen's Inequality for Strictly Convex Utility Function",
        r"Wealth $w$",
        r"Utility $u(w)$",
    )
    w = np.linspace(1, 10, 100)
    u = w**2
    ax.plot(w, u, color=COLORS["primary"], lw=2.2, label=r"Convex $u(w) = w^2$")
    w1, w2 = 2.0, 8.0
    u1, u2 = w1**2, w2**2
    ax.plot(
        [w1, w2],
        [u1, u2],
        color=COLORS["accent_amber"],
        lw=1.8,
        linestyle="--",
        label="Secant Line $E[u(w)]$",
    )
    w_mean = (w1 + w2) / 2.0
    u_mean = (u1 + u2) / 2.0
    ax.scatter(
        [w_mean],
        [w_mean**2],
        color=COLORS["accent_green"],
        s=60,
        label=r"$u(E[w])$ (Lower)",
    )
    ax.scatter(
        [w_mean],
        [u_mean],
        color=COLORS["accent_red"],
        s=60,
        label=r"$E[u(w)]$ (Higher)",
    )
    ax.legend(frameon=True, facecolor="white", edgecolor=COLORS["border"], fontsize=9)
    save_plot(fig, "jensen_inequality.png")


def generate_clt_plots():
    fig, ax = setup_plot(
        "Central Limit Theorem (CLT) Convergence of Sample Mean",
        r"$\bar{X}_n$",
        r"Density",
    )
    x = np.linspace(-3, 3, 200)
    ax.plot(
        x,
        norm.pdf(x),
        color=COLORS["primary"],
        lw=2.5,
        label=r"Asymptotic Limit $\mathcal{N}(0, 1)$",
    )
    ax.legend(frameon=True, facecolor="white", edgecolor=COLORS["border"], fontsize=9.5)
    save_plot(fig, "clt_convergence.png")


def generate_multivariate_normal():
    fig, ax = setup_plot(
        "Bivariate Normal Joint Probability Density Contours",
        r"$x_1$",
        r"$x_2$",
        fig_size=(7, 6),
    )
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = np.exp(-(X**2 - 2 * 0.6 * X * Y + Y**2) / (2 * (1 - 0.6**2)))
    ax.contour(X, Y, Z, levels=8, colors=COLORS["primary"], linewidths=1.5)
    save_plot(fig, "multivariate_normal_distribution.png")


def generate_martingale_paths():
    fig, ax = setup_plot(
        r"Martingale Sample Paths: $E[M_{t+1} \mid \mathcal{F}_t] = M_t$",
        r"Time $t$",
        r"Process Value $M_t$",
    )
    np.random.seed(42)
    t = np.arange(100)
    for i in range(5):
        increments = np.random.normal(0, 1, 100)
        path = np.cumsum(increments)
        ax.plot(t, path, lw=1.5, alpha=0.85)
    ax.axhline(
        0,
        color=COLORS["secondary"],
        lw=1.2,
        linestyle="--",
        label="Expected Value $E[M_t] = M_0 = 0$",
    )
    ax.legend(frameon=True, facecolor="white", edgecolor=COLORS["border"], fontsize=9.5)
    save_plot(fig, "martingale_paths.png")


def generate_eigenvectors():
    fig, ax = setup_plot(
        r"Eigenvectors and Linear Matrix Transformation $A v = \lambda v$",
        r"$x$",
        r"$y$",
        fig_size=(6, 6),
    )
    v1 = np.array([1.0, 1.0]) / np.sqrt(2)
    v2 = np.array([-1.0, 1.0]) / np.sqrt(2)

    ax.quiver(
        0,
        0,
        v1[0],
        v1[1],
        angles="xy",
        scale_units="xy",
        scale=1,
        color=COLORS["accent_green"],
        label=r"$v_1 (\lambda_1=3)$",
    )
    ax.quiver(
        0,
        0,
        3 * v1[0],
        3 * v1[1],
        angles="xy",
        scale_units="xy",
        scale=1,
        color=COLORS["accent_green"],
        linestyle="--",
    )
    ax.quiver(
        0,
        0,
        v2[0],
        v2[1],
        angles="xy",
        scale_units="xy",
        scale=1,
        color=COLORS["accent_red"],
        label=r"$v_2 (\lambda_2=1)$",
    )

    ax.set_xlim(-2, 4)
    ax.set_ylim(-2, 4)
    ax.legend(frameon=True, facecolor="white", edgecolor=COLORS["border"], fontsize=9.5)
    save_plot(fig, "eigenvectors.png")


def main():
    print("--- Generating All Appendix Images ---")
    generate_convergence_rates()
    generate_intermediate_value_theorem()
    generate_convex_sets()
    generate_separating_hyperplane()
    generate_taylor_sin()
    generate_gradient_field()
    generate_comparative_statics()
    generate_normal_plots()
    generate_jensen_inequality()
    generate_clt_plots()
    generate_multivariate_normal()
    generate_martingale_paths()
    generate_eigenvectors()
    print("--- All Appendix Images Generated Successfully ---")


if __name__ == "__main__":
    main()
