import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- Setup Plot Style ---
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 14, 'figure.dpi': 150})

# --- Define a concave function (e.g., log utility) ---
def concave_function(x):
    return np.log(x)

# --- Create Data ---
x = np.linspace(1, 20, 100)
y = concave_function(x)

# Define two points for the inequality
x1, x2 = 3, 15
y1, y2 = concave_function(x1), concave_function(x2)

# Expected value of x
E_x = (x1 + x2) / 2
# Value of the function at the expected value of x
f_E_x = concave_function(E_x)
# Expected value of the function
E_f_x = (y1 + y2) / 2

# --- Create the Plot ---
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the concave function
ax.plot(x, y, label=r'$U(x) = \log(x)$ (Concave Function)', color='C0')

# Plot the chord connecting (x1, y1) and (x2, y2)
ax.plot([x1, x2], [y1, y2], 'ko--', alpha=0.7)

# Mark the points
ax.plot(E_x, f_E_x, 'ro', markersize=8, label=r'$U(E[X])$')
ax.plot(E_x, E_f_x, 'go', markersize=8, label=r'$E[U(X)]$')

# Add annotations and lines
ax.vlines(E_x, 0, f_E_x, colors='gray', linestyles='dotted')
ax.hlines(f_E_x, 0, E_x, colors='gray', linestyles='dotted')
ax.hlines(E_f_x, 0, E_x, colors='gray', linestyles='dotted')

# Add text labels
ax.text(E_x + 0.5, 0.1, r'$E[X]$', fontsize=12)
ax.text(0.2, f_E_x, r'$U(E[X])$', fontsize=12)
ax.text(0.2, E_f_x, r'$E[U(X)]$', fontsize=12)
ax.text(x1-1, y1, r'$(x_1, U(x_1))$', fontsize=12)
ax.text(x2+0.5, y2, r'$(x_2, U(x_2))$', fontsize=12)

# --- Final Formatting ---
ax.set_title("Jensen's Inequality for a Concave Function", fontsize=16)
ax.set_xlabel('Wealth (x)')
ax.set_ylabel('Utility (U(x))')
ax.set_xlim(0, 22)
ax.set_ylim(0, 3.5)
ax.legend()
ax.grid(True)

plt.tight_layout()

# --- Save the Figure ---
output_path = 'images/appendix/jensen_inequality.png'
plt.savefig(output_path)
print(f"Plot saved to {output_path}")