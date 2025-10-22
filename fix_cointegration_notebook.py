
import json
import nbformat

notebook_path = '08-Time-Series/06_Cointegration_and_Error_Correction_Models.ipynb'
old_markdown_substring = "![Visualization of Cointegration](images\\png\\cointegration_visualization.png)"
new_markdown_line = "![Visualization of Cointegration](../images/08-Time-Series/cointegration_visualization.png)\\n"

# Read the notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# Find the target cell and replace its source
cell_found_and_fixed = False
for cell in nb.cells:
    if cell.cell_type == 'markdown':
        # Check each line in the cell's source
        new_source = []
        source_changed = False
        for line in cell.source:
            if old_markdown_substring in line:
                new_source.append(new_markdown_line)
                source_changed = True
            else:
                new_source.append(line)

        if source_changed:
            cell.source = "".join(new_source)
            cell_found_and_fixed = True
            print(f"Found and fixed the image path in {notebook_path}.")
            break # Exit the outer loop once the cell is fixed

if not cell_found_and_fixed:
    print(f"ERROR: Could not find the target markdown cell in {notebook_path}.")
else:
    # Write the corrected notebook back to the file
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"Successfully updated the notebook file.")
