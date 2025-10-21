import json
import matplotlib.pyplot as plt
import numpy as np
from scipy.linalg import svd
from matplotlib.patches import Polygon
import os

# --- Visualization 1: Four Fundamental Subspaces ---
if not os.path.exists("../images/02-Numerical-Methods/four_fundamental_subspaces.png"):
    A = np.array([[1, 1], [2, 3], [3, 2]])
    U, s, Vt = svd(A)
    V = Vt.T
    rank = np.sum(s > 1e-10)

    col_space_basis = U[:, :rank]
    left_null_space_basis = U[:, rank:]

    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122)

    xx, yy = np.meshgrid(np.linspace(-2, 2, 10), np.linspace(-2, 2, 10))
    col_plane = col_space_basis[:, 0, None, None] * xx + col_space_basis[:, 1, None, None] * yy
    ax1.plot_surface(col_plane[0,:,:], col_plane[1,:,:], col_plane[2,:,:], alpha=0.3, color="blue")
    ax1.text(*col_space_basis[:,0]*1.5, 'C(A)', color='blue', fontsize=14)
    ax1.quiver(0, 0, 0, *left_null_space_basis.flatten(), color="red", length=2.0, normalize=True)
    ax1.text(*left_null_space_basis.flatten()*2.2, 'N(A^T)', color='red', fontsize=14)
    ax1.set_title('Output Space (R^3)')
    ax1.set_xlim([-3, 3]); ax1.set_ylim([-3, 3]); ax1.set_zlim([-3, 3])

    ax2.fill_between([-2, 2], -2, 2, color='lightgreen', alpha=0.3, label='Row Space C(A^T) = R^2')
    ax2.plot(0, 0, 'mo', markersize=10, label='Null Space N(A) = {0}')
    ax2.set_xlim(-2, 2); ax2.set_ylim(-2, 2); ax2.set_aspect('equal'); ax2.grid(True)
    ax2.set_title('Input Space (R^2)'); ax2.legend()

    plt.tight_layout()
    plt.savefig("../images/02-Numerical-Methods/four_fundamental_subspaces.png", dpi=300, bbox_inches='tight')
    plt.close()

# --- Visualization 2: Matrix Transformation ---
if not os.path.exists("../images/02-Numerical-Methods/matrix_transformation.png"):
    def plot_transformation(matrix, ax, title):
        i_hat, j_hat = np.array([1, 0]), np.array([0, 1])
        transformed_i, transformed_j = matrix @ i_hat, matrix @ j_hat
        ax.quiver(0, 0, *i_hat, color='gray', scale=1, scale_units='xy', angles='xy', label='$\\hat{i}$')
        ax.quiver(0, 0, *j_hat, color='gray', scale=1, scale_units='xy', angles='xy', label='$\\hat{j}$')
        ax.quiver(0, 0, *transformed_i, color='red', scale=1, scale_units='xy', angles='xy', label='$A\\hat{i}$')
        ax.quiver(0, 0, *transformed_j, color='blue', scale=1, scale_units='xy', angles='xy', label='$A\\hat{j}$')
        unit_square = np.array([[0,0], [1,0], [1,1], [0,1], [0,0]])
        ax.add_patch(Polygon((matrix @ unit_square.T).T, facecolor='lightblue', alpha=0.5))
        ax.set_xlim(-1, 4); ax.set_ylim(-1, 4); ax.set_aspect('equal', adjustable='box')
        ax.legend(); ax.grid(True); ax.set_title(f"{title}\\nDeterminant = {np.linalg.det(matrix):.2f}")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    A_shear = np.array([[1, 1.5], [0, 1]])
    A_rotate_scale = np.array([[2, 1], [1, 2]])
    plot_transformation(A_shear, ax1, 'Shear Transformation')
    plot_transformation(A_rotate_scale, ax2, 'Rotation and Scale')
    plt.tight_layout()
    plt.savefig("../images/02-Numerical-Methods/matrix_transformation.png", dpi=300, bbox_inches='tight')
    plt.close()

# --- Visualization 3: System Dynamics ---
if not os.path.exists("../images/02-Numerical-Methods/system_dynamics.png"):
    def plot_dynamics(A, ax, title):
        eigvals, _ = np.linalg.eig(A)
        ax.set_title(f"{title}\\nEigenvalues: {eigvals[0]:.2f}, {eigvals[1]:.2f}", fontsize=10)
        ax.set_xlim(-5, 5); ax.set_ylim(-5, 5); ax.grid(True)
        for i in range(20):
            x0 = np.random.rand(2) * 4 - 2
            path = [x0]
            for t in range(15):
                x_next = A @ path[-1]
                path.append(x_next)
            path = np.array(path)
            ax.plot(path[:, 0], path[:, 1], '-o', markersize=2, alpha=0.7)

    A_stable = np.array([[0.5, 0.2], [0.1, 0.7]])
    A_unstable = np.array([[1.1, 0.2], [0.1, 1.3]])
    A_saddle = np.array([[0.8, 0.3], [0.2, 1.2]])
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))
    plot_dynamics(A_stable, ax1, 'Stable System')
    plot_dynamics(A_unstable, ax2, 'Unstable System')
    plot_dynamics(A_saddle, ax3, 'Saddle-Path System')
    plt.tight_layout()
    plt.savefig("../images/02-Numerical-Methods/system_dynamics.png", dpi=300, bbox_inches='tight')
    plt.close()

# --- Visualization 4: PCA via SVD ---
if not os.path.exists("../images/02-Numerical-Methods/pca_svd.png"):
    rng = np.random.default_rng(123)
    X_orig = rng.multivariate_normal([0, 0], [[1, 0.8], [0.8, 1]], size=200)
    X_centered = X_orig - X_orig.mean(axis=0)
    U, s, Vt = np.linalg.svd(X_centered)
    V = Vt.T

    plt.figure(figsize=(8, 6))
    plt.scatter(X_centered[:, 0], X_centered[:, 1], alpha=0.6, label='Original Centered Data')
    plt.quiver(0, 0, V[0, 0]*s[0], V[1, 0]*s[0], color='r', scale=1, scale_units='xy', angles='xy', label='PC1')
    plt.quiver(0, 0, V[0, 1]*s[1], V[1, 1]*s[1], color='g', scale=1, scale_units='xy', angles='xy', label='PC2')
    plt.xlabel('X1'); plt.ylabel('X2'); plt.legend(); plt.axis('equal'); plt.grid(True)
    plt.title('Principal Components via SVD')
    plt.savefig("../images/02-Numerical-Methods/pca_svd.png", dpi=300, bbox_inches='tight')
    plt.close()

# --- Patch the Notebook ---
with open('../02-Numerical-Methods/01_Linear_Algebra.ipynb', 'r', encoding='utf-8') as f:
    notebook_data = json.load(f)

for cell in notebook_data['cells']:
    source_str = "".join(cell.get('source', []))
    if 'sec("Visualizing the Four Fundamental Subspaces")' in source_str:
        cell['source'] = ["![The Four Fundamental Subspaces of a Matrix](../images/02-Numerical-Methods/four_fundamental_subspaces.png)"]
        cell['cell_type'] = 'markdown'
        cell['outputs'] = []
    elif 'sec("Visualizing a Matrix Transformation")' in source_str:
        cell['source'] = ["![Visualizing a matrix as a linear transformation](../images/02-Numerical-Methods/matrix_transformation.png)"]
        cell['cell_type'] = 'markdown'
        cell['outputs'] = []
    elif 'sec("Eigen-analysis of a 2D Dynamic System")' in source_str:
        cell['source'] = ["![Phase portraits for dynamic systems with different eigenvalues](../images/02-Numerical-Methods/system_dynamics.png)"]
        cell['cell_type'] = 'markdown'
        cell['outputs'] = []
    elif 'sec("Dimensionality Reduction with SVD (PCA)")' in source_str:
        cell['source'] = ["![Principal components of a dataset found via SVD](../images/02-Numerical-Methods/pca_svd.png)"]
        cell['cell_type'] = 'markdown'
        cell['outputs'] = []
    elif 'sec("Solving the Leontief Input-Output Model")' in source_str:
        cell['source'] = [
            'sec("Solving the Leontief Input-Output Model")\\n',
            '# ... existing Leontief model code ...'
        ]
    elif 'note("The Leontief matrix (I - A) is LU-decomposed once for efficiency.")' in source_str:
        cell['source'].insert(0, "The Leontief model, developed by Wassily Leontief (who won the Nobel Prize in 1973 for this work), is a foundational concept in economics for understanding inter-industry relationships. It represents the economy as a system of linear equations, making it a perfect application for the numerical methods we are discussing.\\n\\n")
    elif 'sec("Solving Systems of Linear Equations: `Ax = b`")' in source_str:
         cell['source'].append('\\n\\n**Best Practice: `solve()` is Better Than `inv()`**\\n\\n'
                             'A common mistake is to solve the system by computing the matrix inverse, i.e., `x = inv(A) @ b`. '
                             'This is **less accurate and slower** than using a solver function like `np.linalg.solve()`, which uses stable and efficient matrix decompositions (like LU factorization) under the hood. '
                             'Let\\'s prove this:')

# Add the new code cell
new_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "sec(\\"Proof: `solve` is Superior to `inv`\\")\\n",
        "N = 500\\n",
        "A = np.random.rand(N, N)\\n",
        "b = np.random.rand(N)\\n",
        "\\n",
        "print(\\"Timing np.linalg.solve(A, b):\\")\\n",
        "%timeit np.linalg.solve(A, b)\\n",
        "\\n",
        "print(\\"Timing np.linalg.inv(A) @ b:\\")\\n",
        "%timeit np.linalg.inv(A) @ b"
    ]
}
# Find the right place to insert the new cell
insertion_index = -1
for i, cell in enumerate(notebook_data['cells']):
    if 'sec("Solving Systems of Linear Equations: `Ax = b`")' in "".join(cell.get('source', [])):
        insertion_index = i + 1
        break
if insertion_index != -1:
    notebook_data['cells'].insert(insertion_index, new_cell)


with open('../02-Numerical-Methods/01_Linear_Algebra.ipynb', 'w', encoding='utf-8') as f:
    json.dump(notebook_data, f, indent=1, ensure_ascii=False)
    f.write('\\n')

print("Assets localized and notebook patched successfully.")
