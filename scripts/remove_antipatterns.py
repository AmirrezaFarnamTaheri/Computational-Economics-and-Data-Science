import os
import json
import glob
import re

def remove_antipatterns(filepath):
    with open(filepath, 'r') as f:
        try:
            nb = json.load(f)
        except json.JSONDecodeError:
            print(f"Error reading {filepath}")
            return

    new_cells = []
    changed = False

    for cell in nb['cells']:
        if cell['cell_type'] != 'code':
            new_cells.append(cell)
            continue

        source_lines = cell['source']
        if not source_lines:
            new_cells.append(cell)
            continue

        current_buffer = []
        cell_split = False

        for line in source_lines:
            # Check for sec() - strictly start of line (no indentation)
            # Regex matches string start, so it enforces no leading characters other than what's matched.
            # But if line starts with space, regex won't match `^sec`.
            sec_match = re.match(r'^sec\([\'"](.*)[\'"]\)\s*$', line)

            # Check for note()
            note_match = re.match(r'^note\([\'"](.*)[\'"]\)\s*$', line)

            if sec_match:
                # Flush buffer if any
                if any(l.strip() for l in current_buffer):
                    # Clean buffer edges
                    while current_buffer and not current_buffer[0].strip(): current_buffer.pop(0)
                    while current_buffer and not current_buffer[-1].strip(): current_buffer.pop()
                    if current_buffer:
                        new_code_cell = {
                            "cell_type": "code",
                            "execution_count": None,
                            "metadata": {},
                            "outputs": [],
                            "source": current_buffer
                        }
                        new_cells.append(new_code_cell)

                # Add Markdown header
                title = sec_match.group(1)
                new_cells.append({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [f"### {title}"]
                })
                current_buffer = [] # Reset
                cell_split = True
                changed = True

            elif note_match:
                 # Flush buffer if any
                if any(l.strip() for l in current_buffer):
                    while current_buffer and not current_buffer[0].strip(): current_buffer.pop(0)
                    while current_buffer and not current_buffer[-1].strip(): current_buffer.pop()
                    if current_buffer:
                        new_code_cell = {
                            "cell_type": "code",
                            "execution_count": None,
                            "metadata": {},
                            "outputs": [],
                            "source": current_buffer
                        }
                        new_cells.append(new_code_cell)

                # Add Note
                msg = note_match.group(1)
                new_cells.append({
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [f"> **Note:** {msg}"]
                })
                current_buffer = [] # Reset
                cell_split = True
                changed = True

            else:
                current_buffer.append(line)

        # Flush remaining buffer
        if current_buffer:
            if cell_split:
                # If we split, we need to clean the last chunk too
                if any(l.strip() for l in current_buffer):
                    while current_buffer and not current_buffer[0].strip(): current_buffer.pop(0)
                    while current_buffer and not current_buffer[-1].strip(): current_buffer.pop()
                    if current_buffer:
                        new_code_cell = {
                            "cell_type": "code",
                            "execution_count": None,
                            "metadata": {},
                            "outputs": [],
                            "source": current_buffer
                        }
                        new_cells.append(new_code_cell)
            else:
                # No split, keep original cell
                new_cells.append(cell)
        elif cell_split:
             # Buffer empty but we split (e.g. sec() was last line)
             pass

    if changed:
        nb['cells'] = new_cells
        with open(filepath, 'w') as f:
            json.dump(nb, f, indent=1)
        print(f"Cleaned antipatterns in {filepath}")

if __name__ == "__main__":
    for filepath in glob.glob('**/*.ipynb', recursive=True):
        if 'checkpoint' not in filepath and '_executed' not in filepath:
            remove_antipatterns(filepath)
