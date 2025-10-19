import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---
plt.style.use('seaborn-v0_8-whitegrid')

# --- Setup Plot ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))
fig.suptitle('The Capital Market Line (CML) vs. The Security Market Line (SML)', fontsize=18, y=1.02)

# --- Common Parameters ---
rf = 0.02
rm = 0.10
sigma_m = 0.20

# --- CML Plot ---
ax1.set_title('Capital Market Line (CML)', fontsize=14)
ax1.set_xlabel('Total Risk (Standard Deviation, σ)')
ax1.set_ylabel('Expected Return, E[R]')
ax1.grid(True)

# Plot the efficient frontier (schematic)
mus = np.linspace(0.05, 0.15, 100)
sigmas = np.sqrt((mus - 0.05)**2 / 0.01 + 0.15**2)
ax1.plot(sigmas, mus, color='lightblue', lw=2, label='Efficient Frontier of Risky Assets')

# Plot the CML
sigma_p = np.linspace(0, 0.3, 100)
cml = rf + (rm - rf) / sigma_m * sigma_p
ax1.plot(sigma_p, cml, 'r-', lw=2, label='Capital Market Line (CML)')

# Mark points
ax1.plot(0, rf, 'ko', markersize=8)
ax1.text(0.005, rf, 'Risk-Free Asset', va='center')
ax1.plot(sigma_m, rm, 'bo', markersize=8)
ax1.text(sigma_m + 0.005, rm, 'Market Portfolio (M)', va='center')

# Show an individual stock (inefficient)
sigma_i = 0.35
beta_i = 1.2
exp_r_i = rf + beta_i * (rm - rf)
ax1.plot(sigma_i, exp_r_i, 'go', markersize=8)
ax1.text(sigma_i + 0.005, exp_r_i, 'Individual Stock (i)', va='center')
ax1.set_xlim(0, 0.4)
ax1.set_ylim(0, 0.16)
ax1.legend()


# --- SML Plot ---
ax2.set_title('Security Market Line (SML)', fontsize=14)
ax2.set_xlabel('Systematic Risk (Beta, β)')
ax2.set_ylabel('Expected Return, E[R]')
ax2.grid(True)

# Plot the SML
beta_p = np.linspace(0, 2, 100)
sml = rf + beta_p * (rm - rf)
ax2.plot(beta_p, sml, 'r-', lw=2, label='Security Market Line (SML)')

# Mark points
ax2.plot(0, rf, 'ko', markersize=8)
ax2.text(0.02, rf, 'Risk-Free Asset', va='center')
ax2.plot(1, rm, 'bo', markersize=8)
ax2.text(1.02, rm, 'Market Portfolio (M)', va='center')

# Show the same individual stock
ax2.plot(beta_i, exp_r_i, 'go', markersize=8)
ax2.text(beta_i + 0.02, exp_r_i, 'Individual Stock (i)', va='center')
ax2.set_xlim(0, 2)
ax2.set_ylim(0, 0.16)
ax2.legend()

# --- Save Plot ---
output_path = 'images\png\cml_sml_distinction.png'
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig(output_path, dpi=300, bbox_inches='tight')

print(f"Plot saved to {output_path}")