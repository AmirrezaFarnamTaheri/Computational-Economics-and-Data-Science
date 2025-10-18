import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Set a professional font
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Source Serif Pro'
plt.rcParams['font.weight'] = 'regular'

# Create the figure and axes
fig, ax = plt.subplots(figsize=(12, 10), dpi=300)
ax.set_aspect('equal')

# Define triangle vertices
A = np.array([0.5, 0.9])
B = np.array([0.05, 0.15])
C = np.array([0.95, 0.15])
vertices = np.array([A, B, C])

# Draw the main triangle
triangle = patches.Polygon(vertices, closed=True,
                           edgecolor='black',
                           facecolor='#EAEAEA',
                           linewidth=2.5)
ax.add_patch(triangle)

# Add corner labels
ax.text(A[0], A[1] + 0.05, 'Generality', ha='center', fontsize=20, weight='bold')
ax.text(B[0] - 0.05, B[1], 'Realism', ha='center', va='center',
        rotation=60, fontsize=20, weight='bold')
ax.text(C[0] + 0.05, C[1], 'Precision', ha='center', va='center',
        rotation=-60, fontsize=20, weight='bold')

# Add tradeoff labels on the edges
ax.text(np.mean([A[0], B[0]]), np.mean([A[1], B[1]]) + 0.02, 'Sacrifice Precision',
        ha='center', va='bottom', rotation=-60, fontsize=14, style='italic', color='#555555')
ax.text(np.mean([A[0], C[0]]), np.mean([A[1], C[1]]) + 0.02, 'Sacrifice Realism',
        ha='center', va='bottom', rotation=60, fontsize=14, style='italic', color='#555555')
ax.text(np.mean([B[0], C[0]]), B[1] - 0.05, 'Sacrifice Generality',
        ha='center', va='top', fontsize=14, style='italic', color='#555555')


# Add examples in the corners
ax.text(A[0], A[1] - 0.15, 'Arrow-Debreu Model',
        ha='center', fontsize=14, style='italic', color='#333333')
ax.text(B[0] + 0.1, B[1] + 0.2, 'Agent-Based Models',
        ha='center', fontsize=14, style='italic', color='#333333')
ax.text(C[0] - 0.1, C[1] + 0.2, 'DSGE Models',
        ha='center', fontsize=14, style='italic', color='#333333')

# Add a central text
ax.text(0.5, 0.4, "Levins' (1966)\nModeler's Trilemma", ha='center',
        fontsize=18, weight='bold', wrap=True)

# Clean up the plot
ax.set_xlim(0, 1)
ax.set_ylim(0, 1.05)
ax.axis('off')

# Save the figure
output_path = 'images/1.1-modelers-trilemma.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', pad_inches=0.1)

print(f"Diagram saved to {output_path}")