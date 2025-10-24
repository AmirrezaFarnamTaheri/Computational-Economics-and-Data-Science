from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import numpy as np
from numba import jit
import os

# Assuming the AiyagariModel class and its helper functions are defined in a file named aiyagari_solver.py
# To make this script self-contained, we will redefine the necessary components here.

# --- Jitted Helper Functions ---
@jit(nopython=True)
def utility(c, gamma):
    return (c**(1 - gamma)) / (1 - gamma) if c > 0 else -1e12

@jit(nopython=True)
def solve_household_problem_vfi(V, a_grid, y_grid, r, beta, gamma, y_trans):
    n_a, n_y = len(a_grid), len(y_grid)
    V_new, g_star = np.zeros_like(V), np.zeros_like(V, dtype=np.int64)
    for i_y in range(n_y):
        for i_a in range(n_a):
            max_val, best_i_ap = -1e12, 0
            budget = (1 + r) * a_grid[i_a] + y_grid[i_y]
            for i_ap in range(n_a):
                c = budget - a_grid[i_ap]
                if c > 0:
                    expected_V_next = np.sum(y_trans[i_y, :] * V[i_ap, :])
                    val = utility(c, gamma) + beta * expected_V_next
                    if val > max_val:
                        max_val, best_i_ap = val, i_ap
            V_new[i_a, i_y], g_star[i_a, i_y] = max_val, best_i_ap
    return V_new, g_star

# --- Animation Function ---
def animate_and_save_distribution(g_star, y_trans, a_grid, n_a, n_y, output_path, n_frames=100):
    fig, ax = plt.subplots(figsize=(10, 7))
    dist = np.zeros((n_a, n_y))
    dist[0, :] = 0.5 / n_y # Start all agents at a=0, split by income state

    def update(frame):
        nonlocal dist
        ax.clear()
        dist_new = np.zeros_like(dist)
        for i_a in range(n_a):
            for i_y in range(n_y):
                if dist[i_a, i_y] > 1e-9: # If there's mass at this point
                    i_ap = g_star[i_a, i_y]
                    for i_yp in range(n_y):
                        dist_new[i_ap, i_yp] += dist[i_a, i_y] * y_trans[i_y, i_yp]
        dist = dist_new / np.sum(dist_new)

        ax.bar(a_grid, dist[:, 0], width=a_grid[1]-a_grid[0], label='Low Income', alpha=0.7)
        ax.bar(a_grid, dist[:, 1], width=a_grid[1]-a_grid[0], bottom=dist[:, 0], label='High Income', alpha=0.7)
        ax.set_title(f'Evolution of Wealth Distribution (Time Step: {frame+1})')
        ax.set_xlabel('Asset Level'); ax.set_ylabel('Mass of Households')
        ax.legend(); ax.set_ylim(0, 0.15)
        ax.grid(True)

    anim = FuncAnimation(fig, update, frames=n_frames, interval=100, repeat=False)
    print(f"Saving animation to {output_path}...")
    anim.save(output_path, writer='imagemagick', fps=10)
    plt.close(fig)
    print("Animation saved.")

if __name__ == "__main__":
    # --- Simplified Model Setup to get g_star ---
    # In a real application, you would solve the full Aiyagari model first.
    # Here we just get a plausible policy function for demonstration.
    BETA, GAMMA = 0.96, 2.0
    R_STAR = 0.025 # Assume an equilibrium rate
    N_A, A_MAX = 200, 50
    a_grid = np.linspace(0, A_MAX, N_A)
    y_grid = np.array([0.1, 1.0])
    y_trans = np.array([[0.5, 0.5], [0.1, 0.9]])

    # Solve for the policy function
    V = np.zeros((N_A, len(y_grid)))
    for i in range(500):
        V_new, g_star = solve_household_problem_vfi(V, a_grid, y_grid, R_STAR, BETA, GAMMA, y_trans)
        if np.max(np.abs(V_new - V)) < 1e-6:
            print(f"VFI converged in {i+1} iterations.")
            break
        V = V_new

    # --- Generate and Save Animation ---
    output_dir = 'images/10-Specialized-Models'
    output_path = os.path.join(output_dir, 'aiyagari_wealth_distribution.gif')
    if not os.path.exists(output_path):
        animate_and_save_distribution(g_star, y_trans, a_grid, N_A, len(y_grid), output_path)
    else:
        print(f"Animation already exists at {output_path}.")
