import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import seaborn as sns

# --- Define the function and its gradient ---
def f(x, y):
    """A simple quadratic function."""
    return x**2 + 2 * y**2

def grad_f(x, y):
    """The gradient of f(x, y)."""
    df_dx = 2 * x
    df_dy = 4 * y
    return df_dx, df_dy

# --- Setup data for the plots ---
x = np.linspace(-4, 4, 20)
y = np.linspace(-4, 4, 20)
X, Y = np.meshgrid(x, y)
Z = f(X, Y)

# Gradient components
U, V = grad_f(X, Y)

# Normalize arrows for better visualization in the quiver plot
N = np.sqrt(U**2 + V**2)
U_norm, V_norm = U / N, V / N

# --- Create the combined plot ---
sns.set_style("whitegrid")
fig = plt.figure(figsize=(16, 7), dpi=150)

# --- 1. The 3D Surface Plot ---
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
surf = ax1.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none', alpha=0.9)
ax1.set_title('Surface Plot of $f(x,y) = x^2 + 2y^2$', fontsize=16)
ax1.set_xlabel('$x$')
ax1.set_ylabel('$y$')
ax1.set_zlabel('$f(x,y)$')
ax1.view_init(elev=30, azim=45) # Set a nice viewing angle
#fig.colorbar(surf, shrink=0.5, aspect=10, ax=ax1, label='Function Value')

# --- 2. The 2D Gradient Field and Contour Plot ---
ax2 = fig.add_subplot(1, 2, 2)
# Plot the contour lines
contours = ax2.contour(X, Y, Z, levels=10, colors='gray', alpha=0.8)
ax2.clabel(contours, inline=True, fontsize=10)
# Plot the gradient field (quiver plot)
# We use the magnitude of the gradient to color the arrows
quiver = ax2.quiver(X, Y, U, V, N, cmap='viridis', norm=LogNorm())
ax2.set_title('Gradient Field and Level Curves', fontsize=16)
ax2.set_xlabel('$x$')
ax2.set_ylabel('$y$')
ax2.set_aspect('equal', adjustable='box')
fig.colorbar(quiver, ax=ax2, label='Magnitude of Gradient')


plt.tight_layout()

# --- Save the Figure ---
output_path = 'images/appendix/gradient_field.png'
plt.savefig(output_path)
print(f"Plot saved to {output_path}")