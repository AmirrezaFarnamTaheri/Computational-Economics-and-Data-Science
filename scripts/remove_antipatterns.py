import nbformat
import re
import sys
import os

def process_notebook(notebook_path):
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    except Exception as e:
        print(f"Error reading {notebook_path}: {e}")
        return

    modified = False

    for cell in nb.cells:
        if cell.cell_type == 'code':
            source = cell.source

            # Case 1: sec("Title") -> ## Title (Markdown)
            match_sec = re.match(r'^\s*sec\s*\([\'"](.*)[\'"]\)\s*$', source.strip())
            if match_sec:
                title = match_sec.group(1)
                cell.cell_type = 'markdown'
                cell.source = f"## {title}"
                modified = True
                continue

            # Case 2: note("Message") -> > **Note:** Message (Markdown)
            match_note = re.match(r'^\s*note\s*\([\'"](.*)[\'"]\)\s*$', source.strip())
            if match_note:
                msg = match_note.group(1)
                cell.cell_type = 'markdown'
                cell.source = f"> **Note:** {msg}"
                modified = True
                continue

            # Case 3: Mixed content or definitions.
            # If we find `def sec(title):` or `def note(msg):`, we should comment them out or remove them
            # as they are no longer needed if we replace usages.
            if "def sec(" in source or "def note(" in source:
                # We comment them out to be safe, or we could delete.
                # Let's comment out for now to avoid breaking if there are missed usages.
                lines = source.split('\n')
                new_lines = []
                for line in lines:
                    if "def sec(" in line or "def note(" in line:
                         new_lines.append(f"# {line} # Deprecated")
                    else:
                        new_lines.append(line)
                cell.source = "\n".join(new_lines)
                modified = True

    if modified:
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print(f"Fixed antipatterns: {notebook_path}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python scripts/remove_antipatterns.py <directory_or_file>")
        sys.exit(1)

    target = sys.argv[1]

    if os.path.isfile(target):
         if target.endswith(".ipynb"):
             process_notebook(target)
    elif os.path.isdir(target):
        print(f"Scanning {target} for antipatterns...")
        for root, dirs, files in os.walk(target):
            if ".ipynb_checkpoints" in root:
                continue
            for file in files:
                if file.endswith(".ipynb"):
                    process_notebook(os.path.join(root, file))
    else:
        print(f"Invalid path: {target}")

if __name__ == "__main__":
    main()
