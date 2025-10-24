import numpy as np
import matplotlib.pyplot as plt

# --- Create Data for the Plot ---
# Number of iterations
k = np.arange(1, 11)

# Sequence with sublinear convergence (e.g., logarithmic)
# We use a small offset to avoid log(0) issues and scale it to look reasonable
d_k = 0.8 / np.log(k + 1)

# Sequences with linear convergence (geometric)
a_k = 0.5**k
b_k = 0.2**k

# Sequence with superlinear/quadratic convergence
# This rate is often seen with Newton's method
c_k = 0.5**(2**k)

# --- Create the Plot ---
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(10, 6), dpi=150)

ax.plot(k, a_k, 'o-', label=r'Linear Convergence ($q=0.5$)')
ax.plot(k, b_k, 's--', label=r'Linear Convergence ($q=0.2$)')
ax.plot(k, c_k, '^-', label=r'Quadratic Convergence')
ax.plot(k, d_k, 'd:', label=r'Sublinear Convergence')

# --- Formatting ---
ax.set_yscale('log')
ax.set_xlabel('Iteration (k)', fontsize=14)
ax.set_ylabel(r'Error $|x_k - x^*|$ (log scale)', fontsize=14)
ax.set_title('Comparison of Convergence Rates', fontsize=16)
ax.legend(fontsize=12)
ax.grid(True, which="both", ls="--")
ax.set_xticks(k)
ax.tick_params(axis='both', which='major', labelsize=12)

plt.tight_layout()

# --- Save the Figure ---
# The target directory should already exist
output_path = 'images/png/convergence_rates.png'
plt.savefig(output_path)

print(f"Plot saved to {output_path}")