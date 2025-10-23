import numpy as np
import matplotlib.pyplot as plt

def generate_stochastic_process_plot():
    """
    Generates and saves a plot illustrating multiple realizations of a single
    stochastic process (specifically, an AR(1) process).
    """
    # --- Configuration ---
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({'font.size': 14, 'figure.figsize': (12, 8), 'figure.dpi': 150})

    # --- Process Parameters ---
    np.random.seed(42)
    n_realizations = 5
    n_steps = 100
    ar_param = 0.9  # Autoregressive parameter
    process_mean = 10
    shock_std = 1.0

    # --- Generate Data ---
    realizations = np.zeros((n_realizations, n_steps))
    for i in range(n_realizations):
        # Start each realization at the mean
        realizations[i, 0] = process_mean
        for t in range(1, n_steps):
            shock = np.random.normal(0, shock_std)
            realizations[i, t] = process_mean + ar_param * (realizations[i, t-1] - process_mean) + shock

    # --- Plotting ---
    fig, ax = plt.subplots()

    for i in range(n_realizations):
        ax.plot(realizations[i, :], lw=2, alpha=0.7, label=f'Realization {i+1}')

    ax.axhline(process_mean, color='black', ls='--', lw=2, label='Process Mean ($\\mu$)')

    ax.set_title('Multiple Realizations of a Stationary Stochastic Process (AR(1))', fontsize=16)
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Value')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.tight_layout()

    # --- Save Figure ---
    # Ensure the images directory exists
    import os
    if not os.path.exists('images'):
        os.makedirs('images')

    save_path = 'images\png\stochastic_process_realizations.png'
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Plot saved to {save_path}")

if __name__ == '__main__':
    generate_stochastic_process_plot()