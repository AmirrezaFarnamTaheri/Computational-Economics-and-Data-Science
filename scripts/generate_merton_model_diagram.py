import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---
plt.style.use('seaborn-v0_8-whitegrid')

# --- Parameters ---
F = 100  # Face value of debt
S_range = np.linspace(0, 200, 200)

# --- Payoffs ---
# Total asset value is just the 45-degree line
asset_value = S_range

# Debt payoff
debt_payoff = np.minimum(S_range, F)

# Equity payoff
equity_payoff = np.maximum(S_range - F, 0)

# --- Plotting ---
fig, ax = plt.subplots(figsize=(12, 8))
fig.suptitle('Merton Model: Payoffs to Debt and Equity Holders at Maturity', fontsize=18)

# Plot the 45-degree line for total asset value
ax.plot(S_range, asset_value, 'k--', label="Total Value of Firm's Assets ($V_T$)")

# Plot the debt and equity payoffs
ax.plot(S_range, debt_payoff, 'b-', lw=2.5, label='Payoff to Debtholders')
ax.plot(S_range, equity_payoff, 'g-', lw=2.5, label="Payoff to Equityholders (a Call Option)")

# Add annotations and fills
ax.axvline(F, color='r', linestyle=':', lw=1.5, label=f'Face Value of Debt (F={F})')
ax.fill_between(S_range, debt_payoff, color='lightblue', alpha=0.5)
ax.fill_between(S_range, debt_payoff, asset_value, color='lightgreen', alpha=0.5)

ax.text(F/2, F/2 + 5, 'Debtholders receive all assets', ha='center')
ax.text(F + (F/2), F + 5, 'Debtholders receive F', ha='center')
ax.text(F + (F/2), F/2, 'Equityholders receive residual', ha='center')
ax.text(F/2, 5, 'Equity is worthless', ha='center')

ax.set_xlabel("Value of Firm's Assets at Maturity ($V_T$)")
ax.set_ylabel("Payoff Value")
ax.set_title("The firm's value is split between debtholders and equityholders")
ax.legend(loc='upper left')
ax.grid(True)
ax.set_xlim(0, 200)
ax.set_ylim(0, 200)

# --- Save Plot ---
output_path = 'images/png/merton_model_payoffs.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')

print(f"Plot saved to {output_path}")