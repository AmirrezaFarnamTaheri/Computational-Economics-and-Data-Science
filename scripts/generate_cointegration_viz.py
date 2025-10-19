import numpy as np
import matplotlib.pyplot as plt

def generate_cointegration_plot():
    """
    Generates and saves a plot illustrating two cointegrated time series.
    """
    # --- Configuration ---
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({'font.size': 14, 'figure.figsize': (14, 10), 'figure.dpi': 150})

    # --- Generate Data ---
    np.random.seed(123)
    n_obs = 500

    # 1. Common stochastic trend (a random walk)
    common_trend = np.random.normal(size=n_obs).cumsum()

    # 2. Two I(1) series that share this common trend
    y1 = 0.5 * common_trend + np.random.normal(size=n_obs, scale=0.5)
    y2 = 1.0 * common_trend + np.random.normal(size=n_obs, scale=0.5)

    # 3. The linear combination (error term) should be stationary
    # The true cointegrating vector is [1, -0.5] for [y2, y1]
    error_term = y2 - 2 * y1

    # --- Plotting ---
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3, 1]})

    # Plot the two cointegrated series
    ax1.plot(y1, label='Series Y1 (I(1))', lw=2)
    ax1.plot(y2, label='Series Y2 (I(1))', lw=2)
    ax1.set_title('Two Cointegrated Time Series')
    ax1.legend()
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Plot the stationary error correction term
    ax2.plot(error_term, label='Error Term (Y2 - 2*Y1)', color='green', lw=2)
    ax2.axhline(0, color='black', linestyle='--', lw=1)
    ax2.set_title('Cointegrating Relationship (Stationary)')
    ax2.legend()
    ax2.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.xlabel('Time')
    plt.tight_layout()

    # --- Save Figure ---
    import os
    if not os.path.exists('images'):
        os.makedirs('images')

    save_path = 'images\png\cointegration_visualization.png'
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Plot saved to {save_path}")

if __name__ == '__main__':
    generate_cointegration_plot()