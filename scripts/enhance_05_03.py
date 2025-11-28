import nbformat
import os

def enhance_game_theory_notebook():
    nb_path = '05-Micro-Models/03_Game_Theory_and_Auctions.ipynb'
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # 1. Visualization of Best Response Functions
    # We will replace the text-only output of "Battle of the Sexes" or augment it with a plot.

    viz_code = """# --- Visualizing Best Response: Battle of the Sexes ---
# We can visualize the mixed-strategy Nash equilibrium by plotting the best response functions.
# Let p be the probability A plays 'Opera' and q be the probability B plays 'Opera'.

# A's Payoffs: (3, 1) vs (0, 2)
# E[u_A(Opera)] = 3q + 0(1-q) = 3q
# E[u_A(Football)] = 1q + 2(1-q) = 2 - q
# A plays Opera if 3q > 2 - q => 4q > 2 => q > 0.5

# B's Payoffs: (2, 1) vs (0, 3)
# E[u_B(Opera)] = 2p + 0(1-p) = 2p
# E[u_B(Football)] = 1p + 3(1-p) = 3 - 2p
# B plays Opera if 2p > 3 - 2p => 4p > 3 => p > 0.75

fig, ax = plt.subplots(figsize=(8, 8))

# A's Best Response (p as function of q)
# If q < 0.5, A plays Football (p=0). If q > 0.5, A plays Opera (p=1).
q_vals = np.linspace(0, 1, 100)
p_response_A = np.where(q_vals < 0.5, 0, np.where(q_vals > 0.5, 1, 0.5))
# Note: At q=0.5, A is indifferent, so p can be anything [0, 1]. We denote this with a vertical line.

# B's Best Response (q as function of p)
# If p < 0.75, B plays Football (q=0). If p > 0.75, B plays Opera (q=1).
p_vals = np.linspace(0, 1, 100)
q_response_B = np.where(p_vals < 0.75, 0, np.where(p_vals > 0.75, 1, 0.5))

# Plotting lines
ax.plot(p_response_A, q_vals, 'b-', label="Player A's Best Response", lw=2)
ax.vlines(0, 0, 0.5, colors='b', lw=2)
ax.vlines(1, 0.5, 1, colors='b', lw=2)
ax.hlines(0.5, 0, 1, colors='b', lw=2, linestyles='--') # Indifference zone

ax.plot(p_vals, q_response_B, 'r-', label="Player B's Best Response", lw=2)
ax.hlines(0, 0, 0.75, colors='r', lw=2)
ax.hlines(1, 0.75, 1, colors='r', lw=2)
ax.vlines(0.75, 0, 1, colors='r', lw=2, linestyles='--') # Indifference zone

# Intersections
ax.plot(0, 0, 'ko', markersize=10, label='Pure NE (F, F)')
ax.plot(1, 1, 'ko', markersize=10, label='Pure NE (O, O)')
ax.plot(0.75, 0.5, 'g*', markersize=15, label='Mixed NE')

ax.set_title("Nash Equilibria: Intersection of Best Response Functions")
ax.set_xlabel("Prob. Player A plays Opera (p)")
ax.set_ylabel("Prob. Player B plays Opera (q)")
ax.set_xlim(-0.05, 1.05); ax.set_ylim(-0.05, 1.05)
ax.legend(loc='center right')
ax.grid(True, alpha=0.3)

if not os.path.exists('../images/05-Micro-Models'):
    os.makedirs('../images/05-Micro-Models')
plt.savefig('../images/05-Micro-Models/nash_best_response.png')
plt.close()
display(Image(filename='../images/05-Micro-Models/nash_best_response.png'))"""

    new_cell = nbformat.v4.new_code_cell(viz_code)

    # Insert after the Nashpy cell (Section 1)
    insert_idx = -1
    for i, cell in enumerate(nb.cells):
        if "Finding Nash Equilibria with nashpy" in cell.source:
            insert_idx = i + 1
            break

    if insert_idx != -1:
        nb.cells.insert(insert_idx, new_cell)

    # 2. Clean up Summary (remove duplicate if exists)
    final_cells = []
    summary_indices = [i for i, c in enumerate(nb.cells) if c.cell_type=='markdown' and "# Summary" in c.source]
    if len(summary_indices) > 1:
        keep_idx = summary_indices[-1]
        for i, cell in enumerate(nb.cells):
            if i in summary_indices and i != keep_idx:
                continue
            final_cells.append(cell)
        nb.cells = final_cells

    # Save
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    print(f"Enhanced {nb_path} with Best Response visualization.")

if __name__ == "__main__":
    enhance_game_theory_notebook()
