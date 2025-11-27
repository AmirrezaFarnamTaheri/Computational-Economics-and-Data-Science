import os
import json
import nbformat

def fix_header(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    header_source = [
        "# Foundations\n",
        "## Chapter X.X: Title\n",
        "\n",
        "[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](../LICENSE)\n",
        "[![Content License: CC BY 4.0](https://img.shields.io/badge/Content%20License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)"
    ]

    # Check if the first cell is a header
    if nb.cells and nb.cells[0].cell_type == 'markdown':
        content = nb.cells[0].source
        if "License" in content:
            # It seems to have a header, but let's standardize it if needed
            # For now, we assume if it has License, it might be okay, but the user wants standardization.
            # However, replacing it blindly might remove the specific Chapter title.
            # So we will try to preserve the title if possible.
            lines = content.split('\n')
            title_line = ""
            for line in lines:
                if line.strip().startswith("#"):
                    title_line = line
                    break

            # If we found a title, use it, otherwise use a placeholder
            if not title_line:
                 title_line = "## Chapter Title Placeholder"

            new_source = [
                 "# " + notebook_path.split('/')[-2] + "\n", # Module Name roughly
                 title_line + "\n",
                 "\n",
                 "[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](../LICENSE)\n",
                 "[![Content License: CC BY 4.0](https://img.shields.io/badge/Content%20License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)"
            ]
            nb.cells[0].source = "\n".join(new_source)
        else:
             # Insert new header
             nb.cells.insert(0, nbformat.v4.new_markdown_cell("\n".join(header_source)))
    else:
        nb.cells.insert(0, nbformat.v4.new_markdown_cell("\n".join(header_source)))

    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"Fixed header for {notebook_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        fix_header(sys.argv[1])
    else:
        print("Usage: python fix_headers.py <notebook_path>")
