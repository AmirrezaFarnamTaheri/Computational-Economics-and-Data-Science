import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'font.size': 14, 'figure.figsize': (12, 8), 'figure.dpi': 150})

# --- Simulation Parameters ---
np.random.seed(42)
n_realizations = 5
n_steps = 100
ar_param = 0.9
process_mean = 10.0

# --- Generate and Plot Realizations ---
fig, ax = plt.subplots()

for i in range(n_realizations):
    # Start each realization from the process mean
    path = np.zeros(n_steps)
    path[0] = process_mean

    # Generate the time series path
    for t in range(1, n_steps):
        # AR(1) process: y_t = c + phi * y_{t-1} + e_t
        # where c = mean * (1 - phi)
        c = process_mean * (1 - ar_param)
        path[t] = c + ar_param * path[t-1] + np.random.normal(0, 1.5) # Add some noise

    ax.plot(path, marker='o', linestyle='-', markersize=4, alpha=0.7, label=f'Realization {i+1}')

# --- Formatting ---
ax.axhline(process_mean, color='black', linestyle='--', linewidth=2, label=f'Process Mean ($\\mu$={process_mean})')
ax.set_title('Multiple Realizations of a Single Stochastic Process', fontsize=16)
ax.set_xlabel('Time Step (t)')
ax.set_ylabel('Value ($y_t$)')
ax.legend()
ax.grid(True, which='both', linestyle='--', linewidth=0.5)

# --- Save the Plot ---
output_path = 'images/stochastic_process_realizations.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')

print(f"Plot saved to {output_path}")