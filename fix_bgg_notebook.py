
import json
import nbformat

notebook_path = '09-Finance/01_Financial_Frictions_BGG.ipynb'
old_markdown_substring = "![The BGG Financial Accelerator Loop](images\\png\\bgg_accelerator.png)"
new_markdown_line = "![The BGG Financial Accelerator Loop](../images/09-Finance/bgg_accelerator.png)\\n"

# Read the notebook
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# Find the target cell and replace its source
cell_found_and_fixed = False
for cell in nb.cells:
    if cell.cell_type == 'markdown':
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
            break

if not cell_found_and_fixed:
    print(f"ERROR: Could not find the target markdown cell in {notebook_path}.")
else:
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"Successfully updated the notebook file.")
