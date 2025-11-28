import nbformat
import os

def enhance_ols_notebook():
    nb_path = '06-Econometrics/01_Linear_Model_and_OLS.ipynb'
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # 1. Visualization of OLS Geometry (Minimizing Squared Errors)
    # We create a 3D plot showing a plane fitting points

    viz_code = """# --- Visualizing the Geometry of OLS ---
# OLS finds the plane that minimizes the sum of squared vertical distances (residuals).

# Generate synthetic data
n_viz = 50
x1_viz = np.random.uniform(0, 10, n_viz)
x2_viz = np.random.uniform(0, 10, n_viz)
y_viz = 2 + 0.5 * x1_viz + 1.5 * x2_viz + np.random.normal(0, 2, n_viz)

# Fit model
X_viz = pd.DataFrame({'const': 1, 'x1': x1_viz, 'x2': x2_viz})
model_viz = sm.OLS(y_viz, X_viz).fit()

# Create meshgrid for plane
x1_grid, x2_grid = np.meshgrid(np.linspace(0, 10, 20), np.linspace(0, 10, 20))
y_pred_grid = model_viz.params['const'] + model_viz.params['x1'] * x1_grid + model_viz.params['x2'] * x2_grid

# Plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Plot points
ax.scatter(x1_viz, x2_viz, y_viz, c='r', marker='o', label='Data Points')

# Plot plane
ax.plot_surface(x1_grid, x2_grid, y_pred_grid, alpha=0.3, color='blue')

# Draw residual lines
for i in range(n_viz):
    x1_i, x2_i, y_i = x1_viz[i], x2_viz[i], y_viz[i]
    y_pred_i = model_viz.predict([1, x1_i, x2_i])[0]
    ax.plot([x1_i, x1_i], [x2_i, x2_i], [y_i, y_pred_i], 'k-', lw=0.5, alpha=0.5)

ax.set_xlabel('X1')
ax.set_ylabel('X2')
ax.set_zlabel('Y')
ax.set_title('OLS Geometry: Minimizing Squared Vertical Residuals')
ax.legend()

if not os.path.exists('../images/06-Econometrics'):
    os.makedirs('../images/06-Econometrics')
plt.savefig('../images/06-Econometrics/ols_geometry_3d.png')
plt.show()"""

    new_cell = nbformat.v4.new_code_cell(viz_code)

    # Insert after section 1.1 (Geometric Interpretation)
    insert_idx = -1
    for i, cell in enumerate(nb.cells):
        if "1.1 The Geometric Interpretation of OLS" in cell.source:
            insert_idx = i + 1
            break

    if insert_idx != -1:
        nb.cells.insert(insert_idx, new_cell)

    # 2. Fix the LASSO plot save
    for cell in nb.cells:
        if "LASSO for Variable Selection" in cell.source:
            if "plt.savefig" not in cell.source:
                lines = cell.source.split('\n')
                new_lines = []
                for line in lines:
                    if "plt.show()" in line:
                        indent = line[:len(line)-len(line.lstrip())]
                        new_lines.append(f"{indent}if not os.path.exists('../images/06-Econometrics'):")
                        new_lines.append(f"{indent}    os.makedirs('../images/06-Econometrics')")
                        new_lines.append(f"{indent}plt.savefig('../images/06-Econometrics/lasso_selection.png')")
                        new_lines.append(f"{indent}plt.close()")
                        new_lines.append(f"{indent}display(Image(filename='../images/06-Econometrics/lasso_selection.png'))")
                    else:
                        new_lines.append(line)
                cell.source = "\n".join(new_lines)

    # 3. Import Check (IPython.display.Image)
    # Ensure Image is imported in setup or locally
    # It is imported in the setup cell (index 1), but let's be safe for the new cell.
    # The new cell uses `display` which is standard IPython but `Image` needs import.
    # We'll add `from IPython.display import Image` to the new cell just in case.
    new_cell.source = "from IPython.display import Image\n" + new_cell.source

    # Save
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    print(f"Enhanced {nb_path} with OLS Geometry visualization.")

if __name__ == "__main__":
    enhance_ols_notebook()
