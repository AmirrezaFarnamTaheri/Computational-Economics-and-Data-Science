import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- Setup Plot Style ---
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12, 'figure.dpi': 150})

# --- Simulation Parameters ---
n_paths = 5
n_steps = 100
np.random.seed(123)

# --- Simulate Martingale Paths (Random Walks) ---
# Each step is a random draw from {-1, 1}
steps = np.random.choice([-1, 1], size=(n_paths, n_steps))

# The path is the cumulative sum of the steps
# We add a zero at the beginning for the starting point
paths = np.hstack([np.zeros((n_paths, 1)), np.cumsum(steps, axis=1)])

# --- Create the Plot ---
fig, ax = plt.subplots(figsize=(10, 6))

for i in range(n_paths):
    ax.plot(paths[i, :], lw=1.5, alpha=0.8)

# --- Formatting ---
ax.set_title('Simulation of Martingale Paths (Random Walks)', fontsize=16)
ax.set_xlabel('Time Step (t)')
ax.set_ylabel('Value ($M_t$)')
ax.grid(True, which="both", ls="--")
ax.axhline(0, color='black', lw=0.75, linestyle='--')

plt.tight_layout()

# --- Save the Figure ---
# Note: The original file was an SVG, but PNG is fine for consistency.
output_path = 'images/png/martingale_paths.png'
plt.savefig(output_path)
print(f"Plot saved to {output_path}")