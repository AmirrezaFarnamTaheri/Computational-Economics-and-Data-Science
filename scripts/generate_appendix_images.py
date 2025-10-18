import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm, binom
from matplotlib.patches import ConnectionPatch, FancyArrowPatch, Circle, Ellipse, Polygon

# --- Configuration ---
OUTPUT_DIR = "images/appendix"
DPI = 300
BACKGROUND_COLOR = "#f4f4f4"
FIG_SIZE = (10, 6)
FONT_SIZE = 14

# --- Helper Functions ---
def setup_plot(title, xlabel, ylabel, fig_size=FIG_SIZE):
    """Set up a standard plot with consistent styling."""
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=fig_size, dpi=DPI)
    fig.patch.set_facecolor('white')
    ax.set_facecolor(BACKGROUND_COLOR)
    ax.set_title(title, fontsize=FONT_SIZE + 2, pad=20)
    ax.set_xlabel(xlabel, fontsize=FONT_SIZE)
    ax.set_ylabel(ylabel, fontsize=FONT_SIZE)
    ax.tick_params(axis='both', which='major', labelsize=FONT_SIZE - 2)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    return fig, ax

def save_plot(fig, filename):
    """Save a plot to the specified directory."""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Saved {path}")

# --- Image Generation Functions ---

def generate_convergence_rates():
    """Generates a plot comparing different rates of convergence."""
    fig, ax = setup_plot("Convergence Rates of Sequences", "Iteration (k)", "Error $|x_k - x^*|$")
    k = np.arange(1, 11)

    # Superlinear (quadratic)
    c_k = 0.5**(2**k)
    ax.plot(k, c_k, 'o-', label=r'Superlinear ($x_{k+1} \approx x_k^2$)', color='red')

    # Linear
    a_k = 0.5**k
    b_k = 0.9**k
    ax.plot(k, a_k, 's--', label=r'Linear (rate 0.5)', color='green')
    ax.plot(k, b_k, '^--', label=r'Linear (rate 0.9)', color='orange')

    # Sublinear
    d_k = 1 / (k + 1)
    ax.plot(k, d_k, 'd:', label=r'Sublinear ($x_{k+1} \approx 1/k$)', color='purple')

    ax.set_yscale('log')
    ax.set_xticks(k)
    ax.legend(fontsize=FONT_SIZE - 2)
    ax.set_ylim(1e-10, 1)
    save_plot(fig, "convergence_rates.png")

def generate_intermediate_value_theorem():
    """Generates a plot illustrating the Intermediate Value Theorem."""
    fig, ax = setup_plot("Intermediate Value Theorem", "x", "f(x)")

    x = np.linspace(0, 10, 100)
    f = lambda x: 0.1 * x**2 - np.sin(x) - 2
    y = f(x)

    a, b = 2, 9
    fa, fb = f(a), f(b)

    ax.plot(x, y, label=r'$f(x)$ - a continuous function')
    ax.plot([a, b], [fa, fb], 'ro')
    ax.text(a, fa + 0.5, 'f(a)', ha='center', va='bottom', fontsize=FONT_SIZE)
    ax.text(b, fb - 0.5, 'f(b)', ha='center', va='top', fontsize=FONT_SIZE)

    y_val = 1.0
    ax.axhline(y_val, color='g', linestyle='--', label=f'y = {y_val}')

    # Find c such that f(c) = y_val
    from scipy.optimize import brentq
    c = brentq(lambda x: f(x) - y_val, a, b)

    ax.plot(c, y_val, 'go')
    ax.text(c, y_val + 0.5, 'y', ha='center', va='bottom', fontsize=FONT_SIZE)
    ax.plot([c, c], [ax.get_ylim()[0], y_val], 'g--')
    ax.plot([a, b], [ax.get_ylim()[0], ax.get_ylim()[0]], 'k-', lw=2)
    ax.text(c, ax.get_ylim()[0]-0.5, 'c', ha='center', va='top', fontsize=FONT_SIZE)

    ax.set_xticks([a, c, b])
    ax.set_xticklabels(['a', 'c', 'b'])
    ax.set_yticks([fa, y_val, fb])
    ax.set_yticklabels(['f(a)', 'y', 'f(b)'])

    ax.legend()
    save_plot(fig, "intermediate_value_theorem.png")

def generate_convex_sets():
    """Generates plots for a convex and a non-convex set."""
    # Convex Set
    fig, ax = setup_plot("A Convex Set", "", "")
    ellipse = Ellipse(xy=(0.5, 0.5), width=0.8, height=0.6, angle=10, color='skyblue', alpha=0.6)
    ax.add_patch(ellipse)

    p1 = (0.3, 0.6)
    p2 = (0.7, 0.4)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'r-o')
    ax.text(p1[0] - 0.05, p1[1], 'x', fontsize=FONT_SIZE)
    ax.text(p2[0] + 0.05, p2[1], 'y', fontsize=FONT_SIZE)
    ax.text(0.5, 0.5, r'$\theta x + (1-\theta)y$', fontsize=FONT_SIZE, ha='center')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')
    save_plot(fig, "convex_set.png")

    # Non-Convex Set
    fig, ax = setup_plot("A Non-Convex Set", "", "")

    # Create a C-shape
    verts = [(0.2, 0.2), (0.8, 0.2), (0.8, 0.3), (0.4, 0.3), (0.4, 0.7), (0.8, 0.7), (0.8, 0.8), (0.2, 0.8), (0.2, 0.2)]
    polygon = Polygon(verts, color='lightcoral', alpha=0.6)
    ax.add_patch(polygon)

    p1 = (0.3, 0.75)
    p2 = (0.7, 0.25)
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], 'b-o')
    ax.text(p1[0] - 0.05, p1[1], 'x', fontsize=FONT_SIZE)
    ax.text(p2[0] + 0.05, p2[1], 'y', fontsize=FONT_SIZE)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')
    save_plot(fig, "non_convex_set.png")

def generate_separating_hyperplane():
    """Generates a plot illustrating the Separating Hyperplane Theorem."""
    fig, ax = setup_plot("Separating Hyperplane Theorem", "", "")

    # Set A
    ellipse_A = Ellipse(xy=(0.3, 0.6), width=0.4, height=0.3, color='skyblue', alpha=0.7)
    ax.add_patch(ellipse_A)
    ax.text(0.3, 0.6, 'A', fontsize=FONT_SIZE, ha='center', va='center')

    # Set B
    ellipse_B = Ellipse(xy=(0.7, 0.3), width=0.3, height=0.4, color='lightcoral', alpha=0.7)
    ax.add_patch(ellipse_B)
    ax.text(0.7, 0.3, 'B', fontsize=FONT_SIZE, ha='center', va='center')

    # Hyperplane
    x_hyper = np.linspace(0.1, 0.9, 100)
    y_hyper = -x_hyper + 1.0
    ax.plot(x_hyper, y_hyper, 'k-', lw=2, label='Separating Hyperplane ($p \cdot z = c$)')

    # Normal vector p
    ax.arrow(0.5, 0.5, 0.1, 0.1, head_width=0.03, head_length=0.03, fc='k', ec='k')
    ax.text(0.62, 0.62, 'p', fontsize=FONT_SIZE)

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal', adjustable='box')
    ax.axis('off')
    ax.legend(loc='upper right')
    save_plot(fig, "separating_hyperplane_theorem.png")

def generate_taylor_sin():
    """Generates a plot of Taylor series approximations for sin(x)."""
    fig, ax = setup_plot("Taylor Series Approximations of sin(x)", "x", "f(x)")
    x = np.linspace(-np.pi, np.pi, 200)
    ax.plot(x, np.sin(x), 'k-', lw=3, label='sin(x)')

    # Taylor approximations
    p1 = x
    p3 = p1 - x**3 / 6
    p5 = p3 + x**5 / 120

    ax.plot(x, p1, 'r--', label='Order 1 Approx.')
    ax.plot(x, p3, 'g:', label='Order 3 Approx.')
    ax.plot(x, p5, 'b-.', label='Order 5 Approx.')

    ax.set_ylim(-1.5, 1.5)
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.legend()
    save_plot(fig, "taylor_sin.png")

def generate_gradient_field():
    """Generates a visualization of a function's gradient field."""
    fig = plt.figure(figsize=(14, 6), dpi=DPI)
    fig.patch.set_facecolor('white')

    # 3D Surface Plot
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    x = np.linspace(-2, 2, 50)
    y = np.linspace(-2, 2, 50)
    X, Y = np.meshgrid(x, y)
    Z = X**2 + 2*Y**2
    ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    ax1.set_title('3D Surface Plot of $f(x,y) = x^2 + 2y^2$')
    ax1.set_xlabel('x')
    ax1.set_ylabel('y')
    ax1.set_zlabel('f(x,y)')

    # 2D Contour and Gradient Plot
    ax2 = fig.add_subplot(1, 2, 2)
    CS = ax2.contour(X, Y, Z, levels=np.arange(0, 10, 1), cmap='viridis')
    ax2.clabel(CS, inline=True, fontsize=10)

    # Gradient field
    X_q, Y_q = np.meshgrid(np.linspace(-2, 2, 15), np.linspace(-2, 2, 15))
    U = 2 * X_q  # df/dx
    V = 4 * Y_q  # df/dy
    # Normalize for better visualization
    N = np.sqrt(U**2 + V**2)
    U, V = U/N, V/N
    ax2.quiver(X_q, Y_q, U, V, color='red', alpha=0.8, scale=25)

    ax2.set_title('Contour Plot and Gradient Field')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    ax2.set_aspect('equal', adjustable='box')

    plt.tight_layout()
    save_plot(fig, "gradient_field.png")

def generate_comparative_statics():
    """Generates a plot for a supply-demand comparative statics exercise."""
    fig, ax = setup_plot("Comparative Statics: Demand Shift", "Quantity", "Price")

    q = np.linspace(1, 10, 100)
    supply = q
    demand1 = 11 - q
    demand2 = 13 - q # Shift out

    ax.plot(q, supply, 'g-', lw=2, label='Supply')
    ax.plot(q, demand1, 'r-', lw=2, label='Demand (D1)')
    ax.plot(q, demand2, 'r--', lw=2, label='Demand (D2)')

    # Equilibrium 1
    p1 = 5.5
    q1 = 5.5
    ax.plot(q1, p1, 'ko')
    ax.plot([q1, 0], [p1, p1], 'k:')
    ax.plot([q1, q1], [0, p1], 'k:')
    ax.text(q1, -0.5, r'$Q_1^*$', ha='center')
    ax.text(-0.5, p1, r'$P_1^*$', va='center')

    # Equilibrium 2
    p2 = 7
    q2 = 7
    ax.plot(q2, p2, 'ko')
    ax.plot([q2, 0], [p2, p2], 'k:')
    ax.plot([q2, q2], [0, p2], 'k:')
    ax.text(q2, -0.5, r'$Q_2^*$', ha='center')
    ax.text(-0.5, p2, r'$P_2^*$', va='center')

    ax.set_xlim(0, 11)
    ax.set_ylim(0, 14)
    ax.legend()
    save_plot(fig, "comparative_statics.png")

def generate_normal_plots():
    """Generates plots for the Normal PDF and CDF."""
    x = np.linspace(-4, 4, 1000)
    y_pdf = norm.pdf(x, 0, 1)
    y_cdf = norm.cdf(x, 0, 1)

    # PDF
    fig, ax = setup_plot("Normal Probability Density Function (PDF)", "z", "Density")
    ax.plot(x, y_pdf)
    x_fill = np.linspace(-4, 1, 500)
    ax.fill_between(x_fill, norm.pdf(x_fill, 0, 1), color='skyblue', alpha=0.5)
    ax.text(0, 0.1, r'$P(Z \leq 1) = \int_{-\infty}^{1} \phi(z)dz$', ha='center', fontsize=12)
    save_plot(fig, "normal_pdf.png")

    # CDF
    fig, ax = setup_plot("Normal Cumulative Distribution Function (CDF)", "z", "Cumulative Probability")
    ax.plot(x, y_cdf)
    ax.axhline(1, ls='--', color='gray')
    ax.axhline(0, ls='--', color='gray')
    ax.axvline(0, ls='--', color='gray')
    prob_at_1 = norm.cdf(1)
    ax.plot([1, 1], [0, prob_at_1], 'r--')
    ax.plot([-4, 1], [prob_at_1, prob_at_1], 'r--')
    ax.set_yticks([0, 0.5, prob_at_1, 1.0])
    ax.set_yticklabels(['0', '0.5', f'{prob_at_1:.2f}', '1.0'])
    ax.set_xticks([-4, 0, 1, 4])
    save_plot(fig, "normal_cdf.png")

def generate_jensen_inequality():
    """Generates a plot illustrating Jensen's Inequality."""
    fig, ax = setup_plot("Jensen's Inequality for a Concave Function", "Wealth (x)", "Utility U(x)")

    x = np.linspace(1, 20, 100)
    u = np.log(x)

    x1, x2 = 5, 15
    u1, u2 = np.log(x1), np.log(x2)

    ax.plot(x, u, label=r'$U(x) = \log(x)$ (Concave)')
    ax.plot([x1, x2], [u1, u2], 'ro-')

    # Expected values
    ex = 0.5 * x1 + 0.5 * x2
    eu = 0.5 * u1 + 0.5 * u2

    # Utility of expected value
    u_ex = np.log(ex)

    ax.plot(ex, eu, 'go', markersize=10, label='(E[X], E[U(X)])')
    ax.plot(ex, u_ex, 'bo', markersize=10, label='(E[X], U(E[X]))')

    ax.plot([ex, ex], [0, u_ex], 'b:')
    ax.text(ex, -0.2, 'E[X]', ha='center')

    ax.plot([0, ex], [u_ex, u_ex], 'b:')
    ax.text(0.5, u_ex, 'U(E[X])', va='center')

    ax.plot([0, ex], [eu, eu], 'g:')
    ax.text(0.5, eu, 'E[U(X)]', va='center')

    ax.legend()
    ax.set_ylim(0, 3.5)
    ax.set_xlim(0, 21)
    save_plot(fig, "jensen_inequality.png")

def generate_clt_plots():
    """Generates plots illustrating the Central Limit Theorem with dice rolls."""
    def plot_sum_dist(n, ax):
        # Create distribution for sum of n dice
        outcomes = np.arange(1, 7)
        dist = {k: 1/6 for k in outcomes}

        current_dist = dist.copy()
        for _ in range(n - 1):
            new_dist = {}
            for s1, p1 in current_dist.items():
                for s2, p2 in dist.items():
                    new_sum = s1 + s2
                    new_dist[new_sum] = new_dist.get(new_sum, 0) + p1 * p2
            current_dist = new_dist

        x = list(current_dist.keys())
        y = list(current_dist.values())

        ax.bar(x, y, width=0.8, alpha=0.7)
        ax.set_title(f'Distribution of the Sum of {n} Dice')
        ax.set_xlabel('Sum')
        ax.set_ylabel('Probability')
        ax.set_xticks(np.arange(n, 6*n + 1, max(1, 5*(n-1))))

    # Plot for n=1, 2, 3
    fig1, ax1 = setup_plot("", "", "", fig_size=(8,5))
    plot_sum_dist(1, ax1)
    save_plot(fig1, "clt_1.png")

    fig2, ax2 = setup_plot("", "", "", fig_size=(8,5))
    plot_sum_dist(2, ax2)
    save_plot(fig2, "clt_2.png")

    fig3, ax3 = setup_plot("", "", "", fig_size=(8,5))
    plot_sum_dist(3, ax3)
    save_plot(fig3, "clt_3.png")

def generate_multivariate_normal():
    """Generates scatter plots of bivariate normal distributions."""
    fig, axes = plt.subplots(1, 3, figsize=(18, 5), dpi=DPI)
    fig.patch.set_facecolor('white')

    means = [0, 0]
    rhos = [-0.7, 0, 0.7]
    titles = [r'$\rho = -0.7$', r'$\rho = 0$', r'$\rho = 0.7$']

    for ax, rho, title in zip(axes, rhos, titles):
        cov = [[1, rho], [rho, 1]]
        data = np.random.multivariate_normal(means, cov, 1000)

        ax.scatter(data[:, 0], data[:, 1], alpha=0.5)
        ax.set_title(title, fontsize=FONT_SIZE + 2)
        ax.set_xlabel('X1', fontsize=FONT_SIZE)
        ax.set_ylabel('X2', fontsize=FONT_SIZE)
        ax.set_aspect('equal', adjustable='box')
        ax.grid(True, linestyle='--', linewidth=0.5)
        ax.set_facecolor(BACKGROUND_COLOR)

    fig.suptitle("Samples from Bivariate Normal Distributions", fontsize=FONT_SIZE + 4)
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    save_plot(fig, "multivariate_normal_distribution.png")

def generate_martingale_paths():
    """Generates a plot of simulated martingale (random walk) paths."""
    fig, ax = setup_plot("Martingale Paths (Random Walks)", "Time Step", "Value")

    n_steps = 100
    n_paths = 5

    for _ in range(n_paths):
        steps = np.random.choice([-1, 1], size=n_steps)
        path = np.cumsum(steps)
        ax.plot(np.arange(n_steps + 1), np.insert(path, 0, 0), alpha=0.7)

    ax.axhline(0, color='k', linestyle='--')
    save_plot(fig, "martingale_paths.png")

def generate_eigenvectors():
    """Generates a plot illustrating the effect of a matrix transformation on eigenvectors."""
    fig, ax = setup_plot("Action of a Matrix on its Eigenvectors", "x", "y")

    A = np.array([[3, 1], [1, 2]])
    eigvals, eigvecs = np.linalg.eig(A)

    v1 = eigvecs[:, 0]
    v2 = eigvecs[:, 1]
    v_other = np.array([1, -1])

    # Transform vectors
    Av1 = A @ v1
    Av2 = A @ v2
    Av_other = A @ v_other

    # Plotting function
    def plot_vec(vec, color, label, style='-'):
        ax.arrow(0, 0, vec[0], vec[1], head_width=0.1, head_length=0.1, fc=color, ec=color, length_includes_head=True, ls=style)
        ax.text(vec[0]*1.1, vec[1]*1.1, label, color=color, fontsize=12)

    # Original vectors
    plot_vec(v1, 'blue', r'$v_1$')
    plot_vec(v2, 'green', r'$v_2$')
    plot_vec(v_other, 'purple', r'$v_{other}$')

    # Transformed vectors
    plot_vec(Av1, 'red', r'$A v_1$', style='--')
    plot_vec(Av2, 'orange', r'$A v_2$', style='--')
    plot_vec(Av_other, 'magenta', r'$A v_{other}$', style='--')

    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)
    ax.axhline(0, color='gray', lw=0.5)
    ax.axvline(0, color='gray', lw=0.5)
    ax.set_aspect('equal', adjustable='box')

    save_plot(fig, "eigenvectors.png")

# --- Main Execution ---
def main():
    """Generate all images for the appendix."""
    print("--- Generating Appendix Images ---")
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
    print("--- All images generated successfully. ---")

if __name__ == "__main__":
    main()