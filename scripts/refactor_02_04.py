import nbformat
import os

def refactor_notebook_root_finding():
    nb_path = '02-Numerical-Methods/04_Root_Finding.ipynb'
    try:
        with open(nb_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    except FileNotFoundError:
        print(f"File not found: {nb_path}")
        return

    # 1. Update TOC (Remove old header levels if present in links, ensure clean structure)
    # Since I don't see the exact TOC content, I'll update it to a standard one based on typical structure if I can infer it,
    # or just fix the cell if it exists.
    # Let's write a generic TOC update or just fix the headers first.

    # 2. Update Headers
    lens_found = False
    summary_found = False

    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            lines = cell.source.split('\n')
            new_lines = []
            for line in lines:
                if "The Lens" in line or "Introduction" in line:
                    if line.strip().startswith("###"):
                        line = line.replace("###", "#", 1) # Promote to H1
                        lens_found = True
                if "Summary" in line or "Conclusion" in line:
                    # Avoid updating TOC lines
                    if not ("[" in line and "]" in line):
                        if line.strip().startswith("###"):
                            line = line.replace("###", "#", 1) # Promote to H1
                            summary_found = True
                new_lines.append(line)
            cell.source = "\n".join(new_lines)

    # 3. Enhance Content - Add "Lens" text if it's weak or missing
    # I'll overwrite the Lens cell with a strong one.

    new_lens = """# The Lens: Finding Balance in a Complex World

**What problem are we solving?**
In economics, equilibrium is everything. A market clears when supply equals demand ($S(p) - D(p) = 0$). A firm maximizes profit where marginal revenue equals marginal cost ($MR(q) - MC(q) = 0$). A macroeconomy is in steady state when capital accumulation ceases ($s f(k) - \delta k = 0$). All of these are **root-finding problems**. We are looking for the value of a variable $x$ that makes a function $f(x)$ equal to zero.

**Why this method?**
Analytical solutions (like the quadratic formula) are rare. For most realistic economic models—which involve non-linear production functions, utility functions, and tax codes—we must find the root numerically.
*   **Bisection** gives us safety (guaranteed convergence).
*   **Newton-Raphson** gives us speed (quadratic convergence).
*   **Brent's Method** gives us the best of both worlds.

This notebook explores how to solve these equations efficiently and robustly, a skill that is the prerequisite for solving almost any equilibrium model."""

    # Inject/Replace Lens
    # Heuristic: Find the first cell with "Lens" or insert after TOC
    lens_cell_index = -1
    for i, cell in enumerate(nb.cells):
        if "The Lens" in cell.source:
            lens_cell_index = i
            break

    if lens_cell_index != -1:
        nb.cells[lens_cell_index].source = new_lens
    else:
        # Insert after the first few cells (usually header, imports, TOC)
        # Let's assume index 3
        new_cell = nbformat.v4.new_markdown_cell(new_lens)
        nb.cells.insert(3, new_cell)

    # 4. Enhance Summary
    new_summary = """# Summary

Root finding is the computational equivalent of finding an economic equilibrium.

**Key Takeaways:**
*   **No Free Lunch:** There is a trade-off between robustness (Bisection) and speed (Newton-Raphson).
*   **Differentiation Matters:** Newton's method requires the derivative $f'(x)$. If calculating it is expensive or impossible, use the Secant method.
*   **Good Guesses are Gold:** All solvers perform better with a good initial guess. Use economic intuition to bound your search.
*   **The Gold Standard:** `scipy.optimize.brentq` is the industry standard for scalar root finding. It combines the safety of bisection with the speed of advanced methods. Use it."""

    # Replace Summary
    summary_cell_index = -1
    for i, cell in enumerate(nb.cells):
        if "Summary" in cell.source and cell.cell_type == 'markdown':
            # Check if it's the header cell
            if cell.source.strip().startswith("#"):
                 summary_cell_index = i
                 break

    if summary_cell_index != -1:
        nb.cells[summary_cell_index].source = new_summary

    # Save
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    print(f"Successfully refactored {nb_path}")

if __name__ == "__main__":
    refactor_notebook_root_finding()
