import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- Setup Plot Style ---
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12, 'figure.dpi': 150})

# --- Define the transformation matrix and find its eigenvectors ---
# A simple shear matrix
A = np.array([[1, 0.5],
              [0.5, 2]])

eigenvalues, eigenvectors = np.linalg.eig(A)
v1 = eigenvectors[:, 0]
v2 = eigenvectors[:, 1]

# Define a non-eigenvector
v_other = np.array([1, 0.2])

# Apply the transformation
Av1 = A @ v1
Av2 = A @ v2
Av_other = A @ v_other

# --- Create the Plot ---
fig, ax = plt.subplots(figsize=(8, 8))

# Helper function to draw vectors
def draw_vector(start, end, color, label, linestyle='-'):
    ax.arrow(start[0], start[1], end[0] - start[0], end[1] - start[1],
             head_width=0.1, head_length=0.15, fc=color, ec=color, length_includes_head=True,
             linestyle=linestyle)
    # Add a label slightly offset from the vector's end
    ax.text(end[0] * 1.1, end[1] * 1.1, label, color=color, fontsize=14, ha='center')

# --- Plot Original Vectors ---
draw_vector([0,0], v1, 'magenta', r'$v_1$')
draw_vector([0,0], v2, 'blue', r'$v_2$')
draw_vector([0,0], v_other, 'red', r'$v_{other}$')

# --- Plot Transformed Vectors ---
draw_vector([0,0], Av1, 'magenta', r'$Av_1$', linestyle='--')
draw_vector([0,0], Av2, 'blue', r'$Av_2$', linestyle='--')
draw_vector([0,0], Av_other, 'red', r'$Av_{other}$', linestyle='--')

# --- Formatting ---
ax.set_xlim(-0.5, 3)
ax.set_ylim(-0.5, 3)
ax.set_aspect('equal', adjustable='box')
ax.set_title('Effect of a Linear Transformation on Eigenvectors', fontsize=16)
ax.set_xlabel('$x_1$')
ax.set_ylabel('$x_2$')
ax.grid(True)
ax.axhline(0, color='black', lw=0.5)
ax.axvline(0, color='black', lw=0.5)

# Add a legend manually
ax.text(1.8, 0.2, 'Original Vectors (Solid)', fontsize=12)
ax.text(1.8, 0.0, 'Transformed Vectors (Dashed)', fontsize=12)


plt.tight_layout()

# --- Save the Figure ---
output_path = 'images/appendix/eigenvectors.png'
plt.savefig(output_path)
print(f"Plot saved to {output_path}")