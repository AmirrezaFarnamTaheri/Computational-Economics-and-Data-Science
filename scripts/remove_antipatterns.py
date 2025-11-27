import nbformat
import re
import sys

def remove_antipatterns(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    modified = False

    for cell in nb.cells:
        if cell.cell_type == 'code':
            # Check for sec() and note() in code cells, which is where they usually live as custom functions
            # But the memory says they are custom functions used for headers and notes.
            # Often they are used like `sec("Title")` in a code cell which outputs a header.
            source = cell.source

            # Regex for sec("Title") or sec('Title')
            # We want to replace the whole cell if it only contains this, or replace the line.
            # Ideally, these should be markdown cells.

            # Case 1: sec("Title") -> ## Title (Markdown)
            # This is tricky because we are changing cell type from code to markdown if it's just a header.
            # Let's look for exact matches of single line calls first.

            if re.match(r'^\s*sec\s*\([\'"](.*)[\'"]\)\s*$', source.strip()):
                match = re.match(r'^\s*sec\s*\([\'"](.*)[\'"]\)\s*$', source.strip())
                title = match.group(1)
                cell.cell_type = 'markdown'
                cell.source = f"## {title}"
                modified = True
                continue

            # Case 2: note("Message") -> > **Note:** Message (Markdown)
            if re.match(r'^\s*note\s*\([\'"](.*)[\'"]\)\s*$', source.strip()):
                match = re.match(r'^\s*note\s*\([\'"](.*)[\'"]\)\s*$', source.strip())
                msg = match.group(1)
                cell.cell_type = 'markdown'
                cell.source = f"> **Note:** {msg}"
                modified = True
                continue

            # If they are embedded in other code, we might need a more complex approach,
            # but usually in these notebooks they are standalone "helper" calls.

    if modified:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print(f"Removed antipatterns in {notebook_path}")
    else:
        print(f"No antipatterns found in {notebook_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        remove_antipatterns(sys.argv[1])
    else:
        print("Usage: python remove_antipatterns.py <notebook_path>")
