import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---
plt.style.use('seaborn-v0_8-whitegrid')

# --- Setup Plot ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Option Payoff and Profit/Loss Diagrams at Expiration', fontsize=18, y=1.02)

# --- Common Parameters ---
K = 100  # Strike price
S_range = np.linspace(K - 50, K + 50, 100)
call_premium = 5
put_premium = 5

# --- Call Option Plot ---
call_payoff = np.maximum(S_range - K, 0)
call_profit = call_payoff - call_premium

ax1.plot(S_range, call_payoff, 'b-', lw=2, label='Payoff (Intrinsic Value)')
ax1.plot(S_range, call_profit, 'g--', lw=2, label='Profit / Loss')
ax1.axhline(0, color='k', linestyle='-', lw=1)
ax1.axvline(K, color='k', linestyle=':', lw=1, label=f'Strike Price (K={K})')
ax1.fill_between(S_range, call_profit, where=call_profit>0, color='lightgreen', alpha=0.5)
ax1.fill_between(S_range, call_profit, where=call_profit<0, color='lightcoral', alpha=0.5)
ax1.set_title('Long Call Option', fontsize=14)
ax1.set_xlabel('Stock Price at Expiration ($S_T$)')
ax1.set_ylabel('Profit / Loss')
ax1.legend()
ax1.grid(True)

# --- Put Option Plot ---
put_payoff = np.maximum(K - S_range, 0)
put_profit = put_payoff - put_premium

ax2.plot(S_range, put_payoff, 'b-', lw=2, label='Payoff (Intrinsic Value)')
ax2.plot(S_range, put_profit, 'g--', lw=2, label='Profit / Loss')
ax2.axhline(0, color='k', linestyle='-', lw=1)
ax2.axvline(K, color='k', linestyle=':', lw=1, label=f'Strike Price (K={K})')
ax2.fill_between(S_range, put_profit, where=put_profit>0, color='lightgreen', alpha=0.5)
ax2.fill_between(S_range, put_profit, where=put_profit<0, color='lightcoral', alpha=0.5)
ax2.set_title('Long Put Option', fontsize=14)
ax2.set_xlabel('Stock Price at Expiration ($S_T$)')
ax2.set_ylabel('Profit / Loss')
ax2.legend()
ax2.grid(True)


# --- Save Plot ---
# Create the directory if it doesn't exist
import os
output_dir = 'images/finance/options'
os.makedirs(output_dir, exist_ok=True)
output_path = f'images/png/call_put_payoffs.png'

plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(output_path, dpi=300, bbox_inches='tight')

print(f"Plot saved to {output_path}")