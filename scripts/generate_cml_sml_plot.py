import numpy as np
import matplotlib.pyplot as plt

def generate_cml_sml_plot():
    """
    Generates and saves a plot clearly distinguishing the CML and SML.
    """
    # --- Configuration ---
    plt.style.use('seaborn-v0_8-whitegrid')

    # --- Create Figure ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

    # --- Panel 1: Capital Market Line (CML) ---
    rf = 0.02
    market_return = 0.10
    market_std = 0.20

    # Efficient Frontier (hyperbola)
    portfolio_std = np.linspace(market_std - 0.05, 0.4, 100)
    portfolio_return = rf + (portfolio_std / market_std) * (market_return - rf) + 0.05 * (portfolio_std - market_std)**2

    ax1.plot(portfolio_std, portfolio_return, 'b-', lw=2, label='Efficient Frontier of Risky Assets')

    # CML
    cml_x = np.linspace(0, 0.4, 100)
    cml_y = rf + (cml_x / market_std) * (market_return - rf)
    ax1.plot(cml_x, cml_y, 'r--', lw=2, label='Capital Market Line (CML)')

    # Markowitz Bullet
    ax1.scatter([market_std], [market_return], color='red', s=150, zorder=5, label='Market Portfolio (M)')
    ax1.scatter([0], [rf], color='green', s=150, zorder=5, label='Risk-Free Asset')

    # Example of an inefficient individual asset
    ax1.scatter([0.25], [0.08], color='black', s=100, zorder=5, label='Individual Asset (e.g., Stock A)')

    ax1.set_title('Capital Market Line (CML)', fontsize=16)
    ax1.set_xlabel('Total Risk (Standard Deviation, σ)')
    ax1.set_ylabel('Expected Return, E[R]')
    ax1.set_xlim(0, 0.4)
    ax1.set_ylim(0, 0.2)
    ax1.legend()
    ax1.grid(True)

    # --- Panel 2: Security Market Line (SML) ---
    sml_x = np.linspace(0, 2.0, 100)
    sml_y = rf + sml_x * (market_return - rf)
    ax2.plot(sml_x, sml_y, 'g-', lw=2, label='Security Market Line (SML)')

    # Assets on the SML
    ax2.scatter([1.0], [market_return], color='red', s=150, zorder=5, label='Market Portfolio (β=1)')
    ax2.scatter([0.0], [rf], color='green', s=150, zorder=5, label='Risk-Free Asset (β=0)')

    # Example individual assets
    ax2.scatter([1.25], [0.12], color='black', s=100, zorder=5, label='Stock A (Correctly Priced)')
    ax2.scatter([0.8], [0.11], color='purple', s=100, zorder=5, label='Stock B (Undervalued)')
    ax2.scatter([1.5], [0.11], color='orange', s=100, zorder=5, label='Stock C (Overvalued)')

    ax2.set_title('Security Market Line (SML)', fontsize=16)
    ax2.set_xlabel('Systematic Risk (Beta, β)')
    ax2.set_ylabel('Expected Return, E[R]')
    ax2.set_xlim(0, 2.0)
    ax2.set_ylim(0, 0.2)
    ax2.legend()
    ax2.grid(True)

    fig.suptitle('Distinction between CML and SML in CAPM', fontsize=20, y=1.02)
    plt.tight_layout()

    # --- Save Figure ---
    import os
    if not os.path.exists('images'):
        os.makedirs('images')

    save_path = 'images/png/cml_sml_distinction.png'
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Plot saved to {save_path}")

if __name__ == '__main__':
    generate_cml_sml_plot()