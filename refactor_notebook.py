
import json
import sys
import os

def refactor_notebook(notebook_path, util_path):
    """
    Refactors a Jupyter notebook to make it self-contained.
    - Embeds a class from a utility file.
    - Removes the import statement for the utility file.
    - Replaces custom sec() and note() calls with standard Markdown.
    """
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        with open(util_path, 'r', encoding='utf-8') as f:
            util_content = f.read()
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading files: {e}", file=sys.stderr)
        sys.exit(1)

    # --- Prepare the MLEstimator class definition for injection ---
    mle_class_def_lines = []
    in_class = False
    for line in util_content.splitlines(True):
        if line.strip().startswith('class MLEstimator:'):
            in_class = True
        if in_class:
            if line.strip().startswith('class MCMCSampler:'):
                break
            # Replace IPython display() with standard print()
            mle_class_def_lines.append(line.replace('display(summary_df.round(4))', 'print(summary_df.round(4))'))
    mle_class_definition = "".join(mle_class_def_lines)

    # --- Task 1: Remove external utility import ---
    if notebook['cells'] and notebook['cells'][0].get('cell_type') == 'code':
        notebook['cells'][0]['source'] = [
            line for line in notebook['cells'][0].get('source', [])
            if "from econometrics_utils import MLEstimator" not in line
        ]

    # --- Task 2: Inject the MLEstimator class definition ---
    insertion_index = -1
    for i, cell in enumerate(notebook['cells']):
        if cell.get('cell_type') == 'markdown' and any("A Reusable `MLEstimator` Class" in line for line in cell.get('source', [])):
            cell['source'] = [
                line.replace(
                    'in the `econometrics_utils.py` file',
                    'in the code cell below'
                ) for line in cell['source']
            ]
            insertion_index = i + 1
            break

    if insertion_index != -1 and mle_class_definition:
        class_cell = {
            'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [],
            'source': mle_class_definition.splitlines(True)
        }
        notebook['cells'].insert(insertion_index, class_cell)

    # --- Task 3: Replace sec() and note() calls with Markdown cells ---
    final_cells = []
    for cell in notebook['cells']:
        if cell.get('cell_type') == 'code' and any('sec(' in line or 'note(' in line for line in cell.get('source', [])):
            title, note, code_lines = "", "", []
            for line in cell['source']:
                stripped_line = line.strip()
                if stripped_line.startswith('sec('):
                    title = stripped_line.split('sec("', 1)[1].rsplit('")', 1)[0]
                elif stripped_line.startswith('note('):
                    note = stripped_line.split('note("', 1)[1].rsplit('")', 1)[0]
                else:
                    code_lines.append(line)

            if title:
                final_cells.append({'cell_type': 'markdown', 'metadata': {}, 'source': [f"### {title}\\n"]})
            if note:
                final_cells.append({'cell_type': 'markdown', 'metadata': {}, 'source': [f"<div class='alert alert-info'>{note}</div>\\n"]})
            if any(line.strip() for line in code_lines):
                final_cells.append({'cell_type': 'code', 'execution_count': None, 'metadata': {}, 'outputs': [], 'source': code_lines})
        else:
            final_cells.append(cell)
    notebook['cells'] = final_cells

    # --- Write the modified notebook back to the file ---
    try:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=1)
        print(f"Successfully refactored {notebook_path}")
    except IOError as e:
        print(f"Error writing to file: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python refactor_notebook.py <notebook_path> <util_path>", file=sys.stderr)
        sys.exit(1)
    refactor_notebook(sys.argv[1], sys.argv[2])
