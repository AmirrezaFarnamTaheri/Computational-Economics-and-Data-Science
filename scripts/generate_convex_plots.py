import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse, Circle
import seaborn as sns

# --- General Plotting Setup ---
sns.set_style("whitegrid")

def setup_plot(ax, title):
    """Helper function to set up plot aesthetics."""
    ax.set_xlim(-0.1, 1.1)
    ax.set_ylim(-0.1, 1.1)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title(title, fontsize=16)

# --- 1. Create the Convex Set Plot ---
fig1, ax1 = plt.subplots(figsize=(6, 6), dpi=150)
setup_plot(ax1, "A Convex Set")

# Create a convex polygon (a pentagon)
convex_shape = Polygon(np.array([[0.1, 0.2], [0.4, 0.8], [0.9, 0.7], [0.8, 0.1], [0.3, 0.1]]),
                       closed=True, color=sns.color_palette("Blues")[2], alpha=0.6)
ax1.add_patch(convex_shape)

# Add points and the line segment between them
p1_c = np.array([0.3, 0.5])
p2_c = np.array([0.7, 0.2])
ax1.plot([p1_c[0], p2_c[0]], [p1_c[1], p2_c[1]], 'ko-', lw=2)
ax1.text(p1_c[0] - 0.05, p1_c[1], '$x$', fontsize=14)
ax1.text(p2_c[0] + 0.02, p2_c[1], '$y$', fontsize=14)
ax1.text(np.mean([p1_c[0], p2_c[0]]), np.mean([p1_c[1], p2_c[1]]) + 0.03, r'$\theta x + (1-\theta)y$', fontsize=12)

plt.tight_layout()
fig1.savefig('images/png/convex_set.png')
print("Saved convex_set.png")


# --- 2. Create the Non-Convex Set Plot ---
fig2, ax2 = plt.subplots(figsize=(6, 6), dpi=150)
setup_plot(ax2, "A Non-Convex Set")

# Create a non-convex shape (a crescent)
# We can do this by overlaying two circles
circle1 = Circle((0.5, 0.5), 0.4, color=sns.color_palette("Reds")[2], alpha=0.6)
circle2 = Circle((0.8, 0.5), 0.4, color='white', alpha=1.0) # White circle to "cut out" a piece
ax2.add_patch(circle1)
ax2.add_patch(circle2)
ax2.add_line(plt.Line2D((0.5, 0.8), (0.9, 0.9), color='white', alpha=0)) # dummy line to enforce bounds

# Add points and the line segment
p1_nc = np.array([0.3, 0.8])
p2_nc = np.array([0.8, 0.2])
ax2.plot([p1_nc[0], p2_nc[0]], [p1_nc[1], p2_nc[1]], 'ko-', lw=2, zorder=3)
ax2.text(p1_nc[0] - 0.05, p1_nc[1], '$x$', fontsize=14)
ax2.text(p2_nc[0] + 0.02, p2_nc[1], '$y$', fontsize=14)

plt.tight_layout()
fig2.savefig('images/png/non_convex_set.png')
print("Saved non_convex_set.png")