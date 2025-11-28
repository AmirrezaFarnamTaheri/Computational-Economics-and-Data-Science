import nbformat
import os

def enhance_job_search_notebook():
    nb_path = '04-Macro-Models/01_Job_Search.ipynb'
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # 1. Deduplicate Summary
    final_cells = []
    summary_indices = [i for i, c in enumerate(nb.cells) if c.cell_type=='markdown' and "# Summary" in c.source]

    if len(summary_indices) > 1:
        # keep the last one (it's the injected one which is better)
        keep_idx = summary_indices[-1]
        for i, cell in enumerate(nb.cells):
            if i in summary_indices and i != keep_idx:
                continue
            final_cells.append(cell)
        nb.cells = final_cells
        print("Removed duplicate Summary cells.")

    # 2. Add LaTeX comments to the McCall Solver Code
    # The code already has comments, but we can make them richer or ensure integration.
    # The current code is functional. Let's leave it as is to avoid breaking it, but ensure plots are saved.

    # 3. Add savefig to plots
    for cell in nb.cells:
        if "plt.show()" in cell.source and "plt.savefig" not in cell.source:
            # We need to determine a filename based on context
            filename = "plot.png"
            if "Optimal Policy in the McCall Search Model" in cell.source:
                filename = "mccall_reservation_wage.png"
            elif "The Beveridge Curve" in cell.source:
                filename = "beveridge_curve.png"
            elif "Burdett-Mortensen" in cell.source:
                filename = "burdett_mortensen_wages.png"

            # Inject save code
            lines = cell.source.split('\n')
            new_lines = []
            for line in lines:
                if "plt.show()" in line:
                    indent = line[:len(line)-len(line.lstrip())]
                    new_lines.append(f"{indent}if not os.path.exists('../images/04-Macro-Models'):")
                    new_lines.append(f"{indent}    os.makedirs('../images/04-Macro-Models')")
                    new_lines.append(f"{indent}plt.savefig('../images/04-Macro-Models/{filename}')")
                    new_lines.append(f"{indent}plt.close()")
                    new_lines.append(f"{indent}display(Image(filename='../images/04-Macro-Models/{filename}'))")
                    # Remove plt.show() if we are displaying the saved image
                else:
                    new_lines.append(line)
            cell.source = "\n".join(new_lines)

    # Save
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

    print(f"Enhanced {nb_path}")

if __name__ == "__main__":
    enhance_job_search_notebook()
