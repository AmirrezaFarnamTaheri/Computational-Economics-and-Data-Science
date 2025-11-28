import os
import json
import glob

HEADER_CELL = {
   "cell_type": "markdown",
   "metadata": {},
   "source": [
    "# === Notebook Title ===\n",
    "\n",
    "[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](../LICENSE)\n",
    "[![Content License: CC BY 4.0](https://img.shields.io/badge/Content%20License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)"
   ]
}

def fix_header(filepath):
    with open(filepath, 'r') as f:
        try:
            nb = json.load(f)
        except json.JSONDecodeError:
            print(f"Error reading {filepath}")
            return

    # Check first cell
    if nb['cells'] and nb['cells'][0]['cell_type'] == 'markdown':
        src = "".join(nb['cells'][0]['source'])
        if "License" in src:
            print(f"Skipping {filepath}, header likely present.")
            # Optionally update it strictly, but for now skip
            return

    # Insert header
    # We need to guess the title from the filename or existing first cell
    filename = os.path.basename(filepath)
    title = filename.replace('.ipynb', '').replace('_', ' ').title()

    new_header = HEADER_CELL.copy()
    new_header['source'] = [f"# {title}\n\n"] + HEADER_CELL['source'][2:]

    nb['cells'].insert(0, new_header)

    with open(filepath, 'w') as f:
        json.dump(nb, f, indent=1)
    print(f"Fixed header in {filepath}")

if __name__ == "__main__":
    for filepath in glob.glob('**/*.ipynb', recursive=True):
        if 'checkpoint' not in filepath:
            fix_header(filepath)
