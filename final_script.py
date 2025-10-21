import timeit
# === Environment Setup ===

import os, sys, math, time, random, json, textwrap, warnings

import numpy as np, pandas as pd

from scipy.linalg import lu, lu_factor, lu_solve, solve_triangular, cholesky, qr, svd

from scipy.sparse import csr_matrix

from scipy.sparse.linalg import spsolve

from scipy.datasets import face

import sympy as sp

import matplotlib.pyplot as plt

from mpl_toolkits.mplot3d import Axes3D

from matplotlib.patches import Polygon, Arrow

from IPython.display import display, Image, Markdown



# --- Configuration ---

plt.style.use('seaborn-v0_8-whitegrid')

plt.rcParams.update({'figure.dpi': 130, 'font.size': 12, 'axes.titlesize': 'x-large',

    'axes.labelsize': 'large', 'xtick.labelsize': 'medium', 'ytick.labelsize': 'medium'})

np.set_printoptions(suppress=True, precision=4, linewidth=120)

sp.init_printing(use_unicode=True)



# --- Utility Functions ---

def note(msg, **kwargs):

    display(Markdown(f"<div class='alert alert-info'>📝 {textwrap.fill(msg, width=100)}</div>"))

def sec(title):

    print(f"\n{100*'='}\n| {title.upper()} |\n{100*'='}")



note("Environment initialized.")
sec("Visualizing the Four Fundamental Subspaces")

# A 3x2 matrix with rank 2 maps from R^2 to R^3

# Note: The original matrix had linearly dependent columns, which was incorrect for the visualization.

# I've adjusted it to be a clear rank-2 matrix to make the visualization more illustrative.

A = np.array([[1, 1], [2, 3], [3, 2]])



# --- Correctly calculate bases for the four fundamental subspaces using one SVD ---

U, s, Vt = svd(A)

V = Vt.T

rank = np.sum(s > 1e-10)



# 1. Column Space C(A) basis (r columns)

col_space_basis = U[:, :rank]

# 2. Left Null Space N(A^T) basis (m-r columns)

left_null_space_basis = U[:, rank:]

# 3. Row Space C(A^T) basis (r columns)

row_space_basis = V[:, :rank]

# 4. Null Space N(A) basis (n-r columns)

null_space_basis = V[:, rank:]



# For a 3x2 matrix of rank 2:

# C(A) is a 2D plane in R^3. N(A^T) is a 1D line in R^3.

# C(A^T) is all of R^2. N(A) is the origin {0} in R^2.



fig = plt.figure(figsize=(12, 6))

ax1 = fig.add_subplot(121, projection='3d') # Output space R^3

ax2 = fig.add_subplot(122) # Input space R^2



# Plotting Output Space (R^3)

# Create a grid for the plane spanning the column space

xx, yy = np.meshgrid(np.linspace(-2, 2, 10), np.linspace(-2, 2, 10))

# Use broadcasting to create the plane coordinates

col_plane = col_space_basis[:, 0, None, None] * xx + col_space_basis[:, 1, None, None] * yy

ax1.plot_surface(col_plane[0,:,:], col_plane[1,:,:], col_plane[2,:,:], alpha=0.3, color="blue")

ax1.text(*col_space_basis[:,0]*1.5, 'C(A)', color='blue', fontsize=14)

# The left null space is a vector orthogonal to the column space plane

q = ax1.quiver(0, 0, 0, *left_null_space_basis.flatten(), color="red", length=2.0, normalize=True)

ax1.text(*left_null_space_basis.flatten()*2.2, 'N(A^T)', color='red', fontsize=14)

ax1.set_title('Output Space (R^3)')

ax1.set_xlim([-3, 3]); ax1.set_ylim([-3, 3]); ax1.set_zlim([-3, 3])



# Plotting Input Space (R^2)

# The row space is all of R^2

ax2.fill_between([-2, 2], -2, 2, color='lightgreen', alpha=0.3, label='Row Space C(A^T) = R^2')

# The null space is just the origin

ax2.plot(0, 0, 'mo', markersize=10, label='Null Space N(A) = {0}')

ax2.set_xlim(-2, 2); ax2.set_ylim(-2, 2); ax2.set_aspect('equal'); ax2.grid(True)

ax2.set_title('Input Space (R^2)'); ax2.legend()



plt.tight_layout(); plt.show()
sec("Visualizing a Matrix Transformation")



def plot_transformation(matrix, ax, title):

    i_hat, j_hat = np.array([1, 0]), np.array([0, 1])

    transformed_i, transformed_j = matrix @ i_hat, matrix @ j_hat

    ax.quiver(0, 0, *i_hat, color='gray', scale=1, scale_units='xy', angles='xy', label='$\hat{i}$')

    ax.quiver(0, 0, *j_hat, color='gray', scale=1, scale_units='xy', angles='xy', label='$\hat{j}$')

    ax.quiver(0, 0, *transformed_i, color='red', scale=1, scale_units='xy', angles='xy', label='$A\hat{i}$')

    ax.quiver(0, 0, *transformed_j, color='blue', scale=1, scale_units='xy', angles='xy', label='$A\hat{j}$')

    unit_square = np.array([[0,0], [1,0], [1,1], [0,1], [0,0]])

    ax.add_patch(Polygon((matrix @ unit_square.T).T, facecolor='lightblue', alpha=0.5))

    ax.set_xlim(-1, 4); ax.set_ylim(-1, 4); ax.set_aspect('equal', adjustable='box')

    ax.legend(); ax.grid(True); ax.set_title(f"{title}\nDeterminant = {np.linalg.det(matrix):.2f}")



fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

A_shear = np.array([[1, 1.5], [0, 1]])

A_rotate_scale = np.array([[2, 1], [1, 2]])

plot_transformation(A_shear, ax1, 'Shear Transformation')

plot_transformation(A_rotate_scale, ax2, 'Rotation and Scale')

plt.tight_layout(); plt.show()
sec("Solving the Leontief Input-Output Model")

# A: Technology Matrix (rows: input sector, cols: output sector)

# e.g., A[0,1] = 0.2 means Manuf needs 0.2 units from Ag for each unit of output

A = np.array([[0.1, 0.2, 0.4],  # Inputs from Agriculture

                [0.5, 0.1, 0.3],  # Inputs from Manufacturing

                [0.1, 0.6, 0.1]]) # Inputs from Services

I = np.eye(3)

L = I - A # The Leontief Matrix



# Decompose the Leontief matrix ONCE using lu_factor for efficiency.

lu_factors, piv = lu_factor(L)



note("The Leontief matrix (I - A) is LU-decomposed once for efficiency.")



def solve_leontief(d):

    """Solves the system for a given demand vector using the pre-computed LU factors."""

    return lu_solve((lu_factors, piv), d)



# Scenario 1: High demand for services

d1 = np.array([100, 200, 500])

x1 = solve_leontief(d1)

print(f"For demand d1 = {d1}, required gross output x1 = {x1}")



# Scenario 2: High demand for manufacturing

d2 = np.array([150, 600, 150])

x2 = solve_leontief(d2)

print(f"For demand d2 = {d2}, required gross output x2 = {x2}")
sec("Condition Number and Multicollinearity")

rng = np.random.default_rng(42)

n = 100

x1 = rng.standard_normal(n)



note("Case 1: Low correlation between x1 and x2")

x2_low_corr = 0.1 * x1 + rng.standard_normal(n) # Low correlation

X_low = np.c_[np.ones(n), x1, x2_low_corr]

cond_low = np.linalg.cond(X_low.T @ X_low)

print(f"Correlation: {np.corrcoef(x1, x2_low_corr)[0,1]:.2f}, Condition Number: {cond_low:.2f}")



note("Case 2: High correlation between x1 and x2")

x2_high_corr = 0.95 * x1 + 0.1 * rng.standard_normal(n) # High correlation

X_high = np.c_[np.ones(n), x1, x2_high_corr]

cond_high = np.linalg.cond(X_high.T @ X_high)

print(f"Correlation: {np.corrcoef(x1, x2_high_corr)[0,1]:.2f}, Condition Number: {cond_high:.2f}")

note("The extremely high condition number indicates that the OLS estimates will be very sensitive to small changes in the data.")
sec("Testing for Positive Definiteness")



note("A valid covariance matrix must be positive definite.")

valid_cov = np.array([[1, 0.5], [0.5, 1]])

try:

    # Cholesky decomposition only works for positive definite matrices

    cholesky(valid_cov)

    print("Matrix is positive definite (Cholesky succeeded).")

except np.linalg.LinAlgError:

    print("Matrix is not positive definite.")



note("An invalid covariance matrix is not positive definite.")

invalid_cov = np.array([[1, 1.1], [1.1, 1]]) # Correlation > 1

try:

    cholesky(invalid_cov)

    print("Matrix is positive definite.")

except np.linalg.LinAlgError as e:

    print(f"Matrix is not positive definite (Cholesky failed: {e})")
sec("Eigen-analysis of a 2D Dynamic System")



def plot_dynamics(A, ax, title):

    eigvals, _ = np.linalg.eig(A)

    ax.set_title(f"{title}\nEigenvalues: {eigvals[0]:.2f}, {eigvals[1]:.2f}", fontsize=10)

    ax.set_xlim(-5, 5); ax.set_ylim(-5, 5); ax.grid(True)



    for i in range(20):

        x0 = np.random.rand(2) * 4 - 2

        path = [x0]

        for t in range(15):

            x_next = A @ path[-1]

            path.append(x_next)

        path = np.array(path)

        ax.plot(path[:, 0], path[:, 1], '-o', markersize=2, alpha=0.7)



A_stable = np.array([[0.5, 0.2], [0.1, 0.7]])      # Both |lambda| < 1

A_unstable = np.array([[1.1, 0.2], [0.1, 1.3]])    # Both |lambda| > 1

A_saddle = np.array([[0.8, 0.3], [0.2, 1.2]])      # One |lambda| < 1, one |lambda| > 1



fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

plot_dynamics(A_stable, ax1, 'Stable System')

plot_dynamics(A_unstable, ax2, 'Unstable System')

plot_dynamics(A_saddle, ax3, 'Saddle-Path System')

plt.tight_layout()

plt.show()
sec("Dimensionality Reduction with SVD (PCA)")

rng = np.random.default_rng(123)

# Create correlated data

X_orig = rng.multivariate_normal([0, 0], [[1, 0.8], [0.8, 1]], size=200)



# 1. Center the data

X_centered = X_orig - X_orig.mean(axis=0)



# 2. Compute SVD

U, s, Vt = np.linalg.svd(X_centered)

V = Vt.T # V contains the principal components as columns



# 3. Project data onto the first principal component

X_projected = X_centered @ V[:, 0]



note("The first column of V is the direction of maximum variance.")

plt.figure(figsize=(8, 6))

plt.scatter(X_centered[:, 0], X_centered[:, 1], alpha=0.6, label='Original Centered Data')

# Plot the principal component vectors, scaled by singular values

plt.quiver(0, 0, V[0, 0]*s[0], V[1, 0]*s[0], color='r', scale=1, scale_units='xy', angles='xy', label='PC1')

plt.quiver(0, 0, V[0, 1]*s[1], V[1, 1]*s[1], color='g', scale=1, scale_units='xy', angles='xy', label='PC2')

plt.xlabel('X1'); plt.ylabel('X2'); plt.legend(); plt.axis('equal'); plt.grid(True)

plt.title('Principal Components via SVD')

plt.show()
sec("Memory and Speed of Sparse Matrices")

N = 10000

# Create a sparse matrix (e.g., a simple tridiagonal matrix)

diag = np.ones(N) * -2

off_diag = np.ones(N - 1)

diagonals = [diag, off_diag, off_diag]

offsets = [0, -1, 1]

A_sparse = csr_matrix((np.concatenate(diagonals), (np.concatenate([np.arange(N), np.arange(N-1), np.arange(1,N)]), np.concatenate([np.arange(N), np.arange(1,N), np.arange(N-1)]))), shape=(N, N))

A_dense = A_sparse.toarray()



note(f"Memory of dense {N}x{N} matrix: {A_dense.nbytes / 1e6:.2f} MB")

note(f"Memory of sparse matrix: {A_sparse.data.nbytes / 1e6:.2f} MB (plus overhead)")



# Solve Ax=b

b = np.random.rand(N)

note("Solving Ax=b using a sparse solver is much faster.")


note("Solving with a dense solver is slower.")


# --- Manual replacement for %timeit spsolve(A_sparse, b) ---
A_sparse_setup = '''
from __main__ import A_sparse, b
from scipy.sparse.linalg import spsolve
'''
A_sparse_stmt = '''
spsolve(A_sparse, b)
'''
spsolve_time = timeit.timeit(stmt=A_sparse_stmt, setup=A_sparse_setup, number=10)
print(f'Time for spsolve: {spsolve_time / 10 * 1e6:.2f} us per loop')

# --- Manual replacement for %timeit np.linalg.solve(A_dense, b) ---
A_dense_setup = '''
from __main__ import A_dense, b
import numpy as np
'''
A_dense_stmt = '''
np.linalg.solve(A_dense, b)
'''
dense_solve_time = timeit.timeit(stmt=A_dense_stmt, setup=A_dense_setup, number=10)
print(f'Time for dense solve: {dense_solve_time / 10 * 1e3:.2f} ms per loop')
