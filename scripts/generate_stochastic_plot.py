import numpy as np
import matplotlib.pyplot as plt
import os

# Ensure the target directory exists
output_dir = 'images/08-Time-Series'
os.makedirs(output_dir, exist_ok=True)

# --- Parameters ---
np.random.seed(42)
n_realizations = 5
n_steps = 200
ar_param = 0.9  # Autoregressive parameter
mean = 0

# --- Generate Realizations of an AR(1) Process ---
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(12, 8))

for _ in range(n_realizations):
    series = np.zeros(n_steps)
    series[0] = np.random.normal(loc=mean, scale=1)
    for t in range(1, n_steps):
        series[t] = ar_param * series[t-1] + np.random.normal(loc=mean, scale=1)
    ax.plot(series, lw=1.5, alpha=0.8)

# --- Formatting ---
ax.axhline(mean, color='black', linestyle='--', lw=2, label=f'Process Mean ({mean})')
ax.set_title(f'{n_realizations} Realizations of a Stationary AR(1) Process ($\\phi$={ar_param})', fontsize=16)
ax.set_xlabel('Time', fontsize=12)
ax.set_ylabel('Value', fontsize=12)
ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# --- Save and Close ---
output_path = os.path.join(output_dir, 'stochastic_process_realizations.png')
plt.savefig(output_path, dpi=300, bbox_inches='tight')
plt.close(fig)

print(f"Plot saved to {output_path}")
