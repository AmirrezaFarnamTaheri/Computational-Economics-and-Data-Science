import nbformat
import os

def enhance_dp_notebook():
    nb_path = '03-Economic-Modeling/01_Dynamic_Programming.ipynb'
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # 1. Update TOC (standardize)
    # The TOC was already decent but let's ensure H1 headers are linked properly if they changed.
    # The refactor script might have already updated headers but not the TOC links.
    # Let's trust the refactor script did its main job.

    # 2. Add LaTeX for Bellman Equation in Code (Comment or Docstring)
    # The notebook already has good Markdown math.
    # The main enhancement is ensuring the visual flow.

    # 3. Clean up the duplicate Summary (Refactor script might have appended one while another existed)
    summary_count = 0
    cells_to_remove = []
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'markdown' and "# Summary" in cell.source:
            summary_count += 1
            if summary_count > 1:
                cells_to_remove.append(i)

    # Remove redundant summaries (keep the last one which is likely the injected one)
    # Actually, the injected one is appended at the end. The old one might be in the middle.
    # We should keep the one at the end.
    if summary_count > 1:
        # Sort indices in descending order to avoid shifting issues
        for idx in sorted(cells_to_remove[:-1], reverse=True): # Keep the last one? No, remove earlier ones.
             # Wait, cells_to_remove contains ALL summary indices.
             # We want to keep the last one (most likely correct location) or the best content.
             # The injected one (last) has the good content.
             pass

    # Actually, let's just delete any summary that is NOT the last one.
    final_cells = []
    summary_indices = [i for i, c in enumerate(nb.cells) if c.cell_type=='markdown' and "# Summary" in c.source]

    if len(summary_indices) > 1:
        # keep the last one
        keep_idx = summary_indices[-1]
        for i, cell in enumerate(nb.cells):
            if i in summary_indices and i != keep_idx:
                continue
            final_cells.append(cell)
        nb.cells = final_cells
        print("Removed duplicate Summary cells.")

    # 4. Enhance the Cake Eating Plot
    # The existing plot code is good, but maybe we can make it prettier.
    # It saves to `../images/03-Economic-Modeling/cake_eating_solution.png`
    # Let's ensure the directory exists in the code cell.

    for cell in nb.cells:
        if "plt.savefig" in cell.source:
            if "os.makedirs" not in cell.source:
                # Add directory creation
                lines = cell.source.split('\n')
                new_lines = []
                for line in lines:
                    if "plt.savefig" in line:
                        indent = line[:len(line)-len(line.lstrip())]
                        new_lines.append(f"{indent}if not os.path.exists('../images/03-Economic-Modeling'):")
                        new_lines.append(f"{indent}    os.makedirs('../images/03-Economic-Modeling')")
                    new_lines.append(line)
                cell.source = "\n".join(new_lines)

    # Save
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    print(f"Enhanced {nb_path}")

if __name__ == "__main__":
    enhance_dp_notebook()
