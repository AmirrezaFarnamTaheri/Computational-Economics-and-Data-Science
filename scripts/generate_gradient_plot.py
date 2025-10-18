import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# --- Plotting Configuration ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'font.size': 14, 'figure.figsize': (12, 6), 'figure.dpi': 150})

x_grid = np.linspace(-2, 2, 20)
y_grid = np.linspace(-2, 2, 20)
X, Y = np.meshgrid(x_grid, y_grid)

# Function: f(x,y) = x^2 + 2*y^2
Z = X**2 + 2*Y**2
U = 2*X  # df/dx
V = 4*Y  # df/dy

fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
ax1.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
ax1.set_title('Surface Plot of $f(x,y) = x^2 + 2y^2$')

ax2 = fig.add_subplot(1, 2, 2)
ax2.quiver(X, Y, U, V)
ax2.set_title('Gradient Field (Direction of Steepest Ascent)')
ax2.set_aspect('equal')
plt.tight_layout()

# Create images/appendix directory if it doesn't exist
import os
if not os.path.exists('images/appendix'):
    os.makedirs('images/appendix')

plt.savefig('images/appendix/gradient_field.png')
print("Image saved to images/appendix/gradient_field.png")