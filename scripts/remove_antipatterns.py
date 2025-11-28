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

    changed = False
    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = "".join(cell['source'])

            # Pattern: sec("Title")
            sec_match = re.match(r'^\s*sec\([\'"](.*)[\'"]\)\s*$', source)
            if sec_match:
                title = sec_match.group(1)
                cell['cell_type'] = 'markdown'
                cell['source'] = [f"## {title}"]
                cell['outputs'] = []
                if 'execution_count' in cell: del cell['execution_count']
                changed = True
                continue

            # Pattern: note("Message")
            note_match = re.match(r'^\s*note\([\'"](.*)[\'"]\)\s*$', source, re.DOTALL)
            if note_match:
                msg = note_match.group(1)
                cell['cell_type'] = 'markdown'
                cell['source'] = [f"> **Note:** {msg}"]
                cell['outputs'] = []
                if 'execution_count' in cell: del cell['execution_count']
                changed = True
                continue

    if changed:
        with open(filepath, 'w') as f:
            json.dump(nb, f, indent=1)
        print(f"Cleaned antipatterns in {filepath}")

if __name__ == "__main__":
    for filepath in glob.glob('**/*.ipynb', recursive=True):
        if 'checkpoint' not in filepath:
            remove_antipatterns(filepath)
