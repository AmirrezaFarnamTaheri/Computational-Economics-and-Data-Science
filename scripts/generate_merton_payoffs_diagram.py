import numpy as np
import matplotlib.pyplot as plt

def generate_merton_payoffs_diagram():
    """
    Generates and saves a diagram illustrating the payoffs in the Merton model.
    """
    # --- Parameters ---
    F = 100  # Face value of debt
    V_T = np.linspace(50, 150, 400) # Range of firm asset values at maturity T

    # --- Payoffs at Maturity T ---
    # Payoff to Equity Holders = max(V_T - F, 0) -> A call option
    payoff_equity = np.maximum(V_T - F, 0)

    # Payoff to Debt Holders = min(V_T, F)
    payoff_debt = np.minimum(V_T, F)

    # Payoff of a risk-free bond is always F
    payoff_risk_free = np.full_like(V_T, F)

    # Payoff of a short put option = -max(F - V_T, 0)
    payoff_short_put = -np.maximum(F - V_T, 0)

    # --- Plotting ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    plt.style.use('seaborn-v0_8-whitegrid')

    # Panel 1: Equity as a Call Option
    ax1.plot(V_T, payoff_equity, 'b-', lw=3, label='Equity Payoff')
    ax1.plot(V_T, V_T - F, 'b--', alpha=0.5, label='$V_T - F$')
    ax1.axhline(0, color='k', linestyle='-', lw=1)
    ax1.axvline(F, color='k', linestyle='--', lw=1.5, label=f'Debt Face Value (F=${F})')
    ax1.set_title('Equity as a Call Option', fontsize=16)
    ax1.set_xlabel('Firm Asset Value at Maturity ($V_T$)')
    ax1.set_ylabel('Payoff to Equity Holders')
    ax1.legend()
    ax1.grid(True)
    ax1.spines['left'].set_position('zero')
    ax1.spines['bottom'].set_position('zero')

    # Panel 2: Risky Debt
    ax2.plot(V_T, payoff_debt, 'r-', lw=3, label='Risky Debt Payoff')
    ax2.plot(V_T, payoff_risk_free + payoff_short_put, 'g--', lw=2, alpha=0.7, label='Risk-Free Bond + Short Put')
    ax2.axvline(F, color='k', linestyle='--', lw=1.5, label=f'Debt Face Value (F=${F})')
    ax2.set_title('Risky Debt = Risk-Free Bond - Put Option', fontsize=16)
    ax2.set_xlabel('Firm Asset Value at Maturity ($V_T$)')
    ax2.set_ylabel('Payoff to Debt Holders')
    ax2.legend()
    ax2.grid(True)

    fig.suptitle('Merton Model: Equity and Debt as Options on Firm Assets', fontsize=20, y=1.02)
    plt.tight_layout()

    # --- Save Figure ---
    import os
    save_dir = 'images'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_path = os.path.join(save_dir, 'images\png\merton_model_payoffs.png')
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Plot saved to {save_path}")

if __name__ == '__main__':
    generate_merton_payoffs_diagram()