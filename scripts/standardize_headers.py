import os
import nbformat
import sys

def standardize_headers(target_dir):
    if not os.path.exists(target_dir):
        print(f"Directory {target_dir} does not exist.")
        return

    license_badge = '[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](LICENSE) [![Content License: CC BY 4.0](https://img.shields.io/badge/Content%20License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)'

    files = [f for f in os.listdir(target_dir) if f.endswith('.ipynb')]

    for filename in files:
        filepath = os.path.join(target_dir, filename)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                nb = nbformat.read(f, as_version=4)

            # Check first cell
            if nb.cells:
                first_cell = nb.cells[0]
                if first_cell.cell_type == 'markdown':
                    source = first_cell.source
                    # If it doesn't have the badge, add it
                    if 'Code License-MIT' not in source:
                        lines = source.split('\n')
                        if lines[0].startswith('# '):
                            # Insert badges after title
                            lines.insert(1, "")
                            lines.insert(2, license_badge)
                            nb.cells[0].source = '\n'.join(lines)
                            print(f"Added badges to {filepath}")
                        else:
                            nb.cells[0].source = license_badge + "\n\n" + source
                            print(f"Added badges to {filepath}")
                else:
                    # First cell is code. Insert markdown cell.
                    new_cell = nbformat.v4.new_markdown_cell(license_badge)
                    nb.cells.insert(0, new_cell)
                    print(f"Inserted badge cell in {filepath}")

            with open(filepath, 'w', encoding='utf-8') as f:
                nbformat.write(nb, f)

        except Exception as e:
            print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        standardize_headers(sys.argv[1])
    else:
        print("Please provide a directory.")
