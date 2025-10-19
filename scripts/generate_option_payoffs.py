import numpy as np
import matplotlib.pyplot as plt

def generate_option_payoff_diagrams():
    """
    Generates and saves a high-quality plot of call and put option payoffs.
    """
    # --- Parameters ---
    K = 100  # Strike price
    premium_call = 5
    premium_put = 5
    S = np.linspace(70, 130, 400) # Range of stock prices at expiration

    # --- Payoffs ---
    payoff_call = np.maximum(S - K, 0)
    payoff_put = np.maximum(K - S, 0)

    # --- Profits ---
    profit_call = payoff_call - premium_call
    profit_put = payoff_put - premium_put

    # --- Plotting ---
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
    plt.style.use('seaborn-v0_8-whitegrid')

    # Panel 1: Call Option
    ax1.plot(S, payoff_call, 'b--', label='Payoff at Expiration (max(S-K, 0))')
    ax1.plot(S, profit_call, 'b-', lw=2.5, label='Profit/Loss (Payoff - Premium)')
    ax1.axhline(0, color='k', linestyle='-', lw=1)
    ax1.axvline(K, color='k', linestyle='--', lw=1, label=f'Strike Price (K=${K})')
    ax1.fill_between(S, profit_call, 0, where=profit_call > 0, color='green', alpha=0.1, label='Profit Zone')
    ax1.fill_between(S, profit_call, 0, where=profit_call < 0, color='red', alpha=0.1, label='Loss Zone')
    ax1.set_title('Long Call Option', fontsize=16)
    ax1.set_xlabel('Stock Price at Expiration ($S_T$)')
    ax1.set_ylabel('Profit / Loss')
    ax1.legend()
    ax1.grid(True)

    # Panel 2: Put Option
    ax2.plot(S, payoff_put, 'r--', label='Payoff at Expiration (max(K-S, 0))')
    ax2.plot(S, profit_put, 'r-', lw=2.5, label='Profit/Loss (Payoff - Premium)')
    ax2.axhline(0, color='k', linestyle='-', lw=1)
    ax2.axvline(K, color='k', linestyle='--', lw=1, label=f'Strike Price (K=${K})')
    ax2.fill_between(S, profit_put, 0, where=profit_put > 0, color='green', alpha=0.1, label='Profit Zone')
    ax2.fill_between(S, profit_put, 0, where=profit_put < 0, color='red', alpha=0.1, label='Loss Zone')
    ax2.set_title('Long Put Option', fontsize=16)
    ax2.set_xlabel('Stock Price at Expiration ($S_T$)')
    ax2.set_ylabel('Profit / Loss')
    ax2.legend()
    ax2.grid(True)

    fig.suptitle('Option Payoff and Profit/Loss Diagrams', fontsize=20, y=1.02)
    plt.tight_layout()

    # --- Save Figure ---
    import os
    save_dir = 'images/finance/options'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_path = os.path.join(save_dir, 'images\png\call_put_payoffs.png')
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Plot saved to {save_path}")

if __name__ == '__main__':
    generate_option_payoff_diagrams()