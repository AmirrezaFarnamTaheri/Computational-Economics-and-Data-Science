import nbformat
import glob
import re
import os

def refix_notebook(filepath):
    print(f"Processing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    except Exception as e:
        print(f"  Error reading {filepath}: {e}")
        return

    modified = False

    new_cells = []
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            source = cell.source.strip()
            # Detect Markdown cells that look like notes with f-string variables
            # Pattern: > **Note:** ... {var} ...
            if source.startswith('> **Note:**') and '{' in source and '}' in source:
                # Check if it looks like a variable interpolation
                # Simple check: Are the braces balanced and containing something?
                # This heuristic is reasonable for this codebase.

                # We need to convert this BACK to a code cell
                # display(Markdown(f"..."))

                # Extract content
                # source is "> **Note:** content"
                # content = source[len("> **Note:**"):].strip()
                # But we want the whole thing wrapped.

                # We need to escape any existing double quotes to put it inside f"..."
                safe_source = source.replace('"', '\\"')

                # Construct code
                code_source = f"display(Markdown(f\"{safe_source}\"))"

                new_cells.append(nbformat.v4.new_code_cell(code_source))
                modified = True
                print(f"  Reverted dynamic note to code: {source[:30]}...")
            else:
                new_cells.append(cell)
        else:
            new_cells.append(cell)

    nb.cells = new_cells

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print("  Saved changes.")
    else:
        print("  No changes needed.")

def main():
    notebooks = glob.glob("**/*.ipynb", recursive=True)
    notebooks = [nb for nb in notebooks if ".ipynb_checkpoints" not in nb]

    print(f"Refixing {len(notebooks)} notebooks...")
    for nb_path in notebooks:
        refix_notebook(nb_path)

if __name__ == '__main__':
    main()
