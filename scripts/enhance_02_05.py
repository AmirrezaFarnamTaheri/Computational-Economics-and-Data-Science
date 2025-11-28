import nbformat
import os

def enhance_optimization_notebook():
    nb_path = '02-Numerical-Methods/05_Optimization.ipynb'
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # We want to add a comparison of Newton's Method vs Gradient Descent vs Nelder-Mead
    # This visualizes "The Search Party" concept in the Lens.

    comparison_code = """# --- Visualizing the "Search Party" ---\n# Let's visualize how different algorithms traverse a cost surface (the Rosenbrock function).\n\ndef rosen_2d(x, y):\n    return (1 - x)**2 + 100 * (y - x**2)**2\n\n# Create the mesh\nx = np.linspace(-2, 2, 250)\ny = np.linspace(-1, 3, 250)\nX, Y = np.meshgrid(x, y)\nZ = rosen_2d(X, Y)\n\n# Solve with different methods to track the path\nmethods = ['Nelder-Mead', 'BFGS']\npaths = {}\n\nfor method in methods:\n    path = []\n    def callback(xk):\n        path.append(xk)\n    \n    x0 = np.array([-1.5, 1.5])\n    res = minimize(rosen, x0, method=method, callback=callback)\n    paths[method] = np.array(path)\n\n# Plot\nfig, ax = plt.subplots(figsize=(10, 7))\n# Contour plot (log scale for visibility)\nax.contourf(X, Y, np.log(Z), levels=30, cmap='viridis', alpha=0.6)\n\n# Plot paths\ncolors = {'Nelder-Mead': 'white', 'BFGS': 'red'}\nmarkers = {'Nelder-Mead': 'o', 'BFGS': 'x'}\n\nfor method, path in paths.items():\n    if len(path) > 0:\n        ax.plot(path[:, 0], path[:, 1], color=colors[method], label=f'{method} ({len(path)} steps)', marker=markers[method], markersize=4, lw=1.5)\n        # Plot start and end\n        ax.plot(path[0, 0], path[0, 1], 'ks', label='Start' if method == 'Nelder-Mead' else None) # Only label once\n        ax.plot(path[-1, 0], path[-1, 1], 'k*', markersize=12, label='Optimum' if method == 'Nelder-Mead' else None)\n\nax.set_title("Optimization Paths: Derivative-Free (Nelder-Mead) vs. Gradient-Based (BFGS)")\nax.set_xlabel("x")\nax.set_ylabel("y")\nax.legend()\nplt.show()\n\nprint("Observation: BFGS (Gradient-based) takes a direct, efficient curved path exploiting curvature information.")\nprint("Observation: Nelder-Mead (Derivative-free) 'walks' down the valley, taking many more steps.")"""

    new_cell = nbformat.v4.new_code_cell(comparison_code)

    # Insert after section 1.2 (Quasi-Newton Methods)
    # Finding the index
    insert_idx = -1
    for i, cell in enumerate(nb.cells):
        if "![Optimizer Paths" in cell.source:
             insert_idx = i # Replace the static image placeholder
             break

    if insert_idx != -1:
        # Replace the static image cell with the live code cell
        nb.cells[insert_idx] = new_cell
    else:
        # Fallback: find section 1.2
        for i, cell in enumerate(nb.cells):
            if "1.2 Quasi-Newton Methods" in cell.source:
                nb.cells.insert(i + 1, new_cell)
                break

    # Save
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    print(f"Enhanced {nb_path} with live visualization.")

if __name__ == "__main__":
    enhance_optimization_notebook()
