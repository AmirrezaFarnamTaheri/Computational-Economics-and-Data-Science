import os
import json
import re
import sys

# --- Configuration ---
LICENSE_BADGES = """[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](../LICENSE)
[![Content License: CC BY 4.0](https://img.shields.io/badge/Content%20License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)"""

MATPLOTLIB_STYLE = """import matplotlib.pyplot as plt
import seaborn as sns
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'figure.figsize': (10, 6), 'font.size': 12})"""

# --- Helpers ---
def fix_header(cells, filename):
    """Ensures the first markdown cell has the correct license badges."""
    if not cells:
        return

    first_cell = cells[0]
    if first_cell["cell_type"] != "markdown":
        # Insert a new header cell if the first one isn't markdown
        new_header = {
            "cell_type": "markdown",
            "metadata": {},
            "source": [f"# {filename.replace('.ipynb', '').replace('_', ' ')}\n", "\n", LICENSE_BADGES]
        }
        cells.insert(0, new_header)
        return

    source = "".join(first_cell["source"])
    if "Code License-MIT" not in source:
        # Append badges if missing
        first_cell["source"].append("\n\n" + LICENSE_BADGES)

def process_notebook(filepath):
    changed = False
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return

    cells = nb.get("cells", [])

    # 1. Fix Header
    fix_header(cells, os.path.basename(filepath))

    # 2. Iterate through cells
    for i, cell in enumerate(cells):
        if cell["cell_type"] == "code":
            new_source = []
            source_changed = False
            for line in cell["source"]:
                # Check for anti-patterns in code cells (definition cells)
                if "def sec(" in line or "def note(" in line:
                    new_source.append(f"# {line}")
                    source_changed = True
                else:
                    new_source.append(line)

            if source_changed:
                cell["source"] = new_source
                changed = True

            # 3. Inject Matplotlib Style
            src_text = "".join(cell["source"])
            if "import matplotlib.pyplot" in src_text and "plt.style.use" not in src_text:
                cell["source"].append("\n" + MATPLOTLIB_STYLE)
                changed = True

    # SAVE
    # Always save to ensure header updates are applied even if no code changed
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(nb, f, indent=1)
        print(f"Processed: {filepath}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/standardize_notebooks.py <directory>")
        sys.exit(1)

    target_dir = sys.argv[1]
    print(f"Standardizing notebooks in {target_dir}...")

    for root, dirs, files in os.walk(target_dir):
        if ".ipynb_checkpoints" in root:
            continue
        for file in files:
            if file.endswith(".ipynb"):
                process_notebook(os.path.join(root, file))
    print("Done.")

if __name__ == "__main__":
    main()
