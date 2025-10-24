import numpy as np
import matplotlib.pyplot as plt

def generate_ito_lemma_viz():
    """
    Generates a conceptual visualization to build intuition for Ito's Lemma.
    """
    # --- Setup ---
    plt.style.use('seaborn-v0_8-whitegrid')
    fig = plt.figure(figsize=(14, 8))

    # --- Data for a convex function f(x) = x^2 ---
    x = np.linspace(-1.5, 1.5, 100)
    y = x**2

    # --- Panel 1: Standard Calculus (Smooth Path) ---
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.plot(x, y, 'b-', label='$f(x) = x^2$')

    # A smooth, deterministic path
    x_smooth = np.array([-0.5, 0.5])
    y_smooth = x_smooth**2
    ax1.plot(x_smooth, y_smooth, 'ro-', markersize=8, label='Deterministic Path')

    # Taylor approximation
    f_a = (-0.5)**2
    f_prime_a = 2 * (-0.5)
    dx = 1.0
    taylor_approx = f_a + f_prime_a * dx
    ax1.plot([0.5], [taylor_approx], 'gx', markersize=12, mew=3, label='1st Order Approx. $f(a) + f\'(a)dx$')

    ax1.set_title('Standard Calculus (Smooth Path)', fontsize=14)
    ax1.set_xlabel('x')
    ax1.set_ylabel('f(x)')
    ax1.legend()
    ax1.grid(True)

    # --- Panel 2: Stochastic Calculus (Random Walk) ---
    ax2 = fig.add_subplot(1, 2, 2)
    ax2.plot(x, y, 'b-', label='$f(x) = x^2$')

    # A stochastic path
    np.random.seed(42)
    t = np.linspace(0, 1, 21)
    dt = t[1] - t[0]
    dW = np.random.randn(len(t)-1) * np.sqrt(dt)
    W = np.concatenate(([0], np.cumsum(dW)))
    W = W - W[10] # Center the path

    ax2.plot(W, W**2, 'r-', marker='o', markersize=4, alpha=0.7, label='Stochastic Path')

    # Illustrate the Ito term
    # The expected value of f(W_t) is E[t], which is non-zero due to the Ito term
    final_positions = []
    for _ in range(5000):
        dW_sim = np.random.randn(len(t)-1) * np.sqrt(dt)
        W_sim = np.concatenate(([0], np.cumsum(dW_sim)))
        final_positions.append(W_sim[-1]**2)

    expected_f_WT = np.mean(final_positions)
    ax2.axhline(expected_f_WT, color='purple', ls='--', lw=2, label=f'E[$f(W_T)$] ≈ {expected_f_WT:.2f} (Ito term)')

    ax2.set_title('Stochastic Calculus (Ito\'s Lemma)', fontsize=14)
    ax2.set_xlabel('W(t)')
    ax2.set_ylabel('f(W(t))')
    ax2.legend()
    ax2.grid(True)

    fig.suptitle('Intuition for Ito\'s Lemma: Why the Second Derivative Matters', fontsize=18, y=1.02)
    plt.tight_layout()

    # --- Save Figure ---
    import os
    save_dir = 'images/finance'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_path = os.path.join(save_dir, 'images/png/ito_lemma_intuition.png')
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Plot saved to {save_path}")

if __name__ == '__main__':
    generate_ito_lemma_viz()