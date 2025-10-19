import numpy as np
import matplotlib.pyplot as plt
from math import factorial
import seaborn as sns

# --- Function for Taylor Approximation of sin(x) ---
def taylor_sin(x, n_terms):
    """Calculates the Taylor series approximation of sin(x) around 0."""
    series = np.zeros_like(x, dtype=float)
    for n in range(n_terms):
        # The nth term in the Taylor series for sin(x) is (-1)^n * x^(2n+1) / (2n+1)!
        term = ((-1)**n) * (x**(2*n + 1)) / factorial(2*n + 1)
        series += term
    return series

# --- Create Data for the Plot ---
x = np.linspace(-np.pi * 2, np.pi * 2, 400)
y_true = np.sin(x)

# Taylor approximations with different numbers of terms
y_p1 = taylor_sin(x, 1) # P_1(x) = x
y_p3 = taylor_sin(x, 2) # P_3(x) = x - x^3/6
y_p5 = taylor_sin(x, 3) # P_5(x) = x - x^3/6 + x^5/120
y_p7 = taylor_sin(x, 4) # P_7(x) = ...

# --- Create the Plot ---
sns.set_style("whitegrid")
fig, ax = plt.subplots(figsize=(10, 7), dpi=150)

ax.plot(x, y_true, 'k-', lw=2.5, label='True $\\sin(x)$')
ax.plot(x, y_p1, '--', label='Degree 1 Approx.')
ax.plot(x, y_p3, '--', label='Degree 3 Approx.')
ax.plot(x, y_p5, '--', label='Degree 5 Approx.')
ax.plot(x, y_p7, '--', label='Degree 7 Approx.')

# --- Formatting ---
ax.set_ylim(-2, 2)
ax.set_xlim(-np.pi * 2, np.pi * 2)
ax.set_xlabel('$x$', fontsize=14)
ax.set_ylabel('$f(x)$', fontsize=14)
ax.set_title('Taylor Series Approximations of $\\sin(x)$ at $a=0$', fontsize=16)
ax.legend(fontsize=12)
ax.grid(True, which="both", ls="--")
ax.axhline(0, color='black', lw=0.5)
ax.axvline(0, color='black', lw=0.5)

plt.tight_layout()

# --- Save the Figure ---
output_path = 'images\png\taylor_sin.png'
plt.savefig(output_path)

print(f"Plot saved to {output_path}")