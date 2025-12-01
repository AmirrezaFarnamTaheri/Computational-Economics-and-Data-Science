import nbformat
import glob
import re
import os

def fix_notebook(filepath):
    print(f"Processing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    except Exception as e:
        print(f"  Error reading {filepath}: {e}")
        return

    modified = False

    note_pattern = re.compile(r"^(.*?)note\((?:[fr])?(['\"])(.*?)\2\)(.*)$")
    sec_pattern = re.compile(r"^(\s*)sec\((?:[fr])?(['\"])(.*?)\2\)\s*$")
    pip_pattern = re.compile(r"^\s*!pip install")

    # 1. Fix Antipatterns in Code Cells
    new_cells = []
    for cell in nb.cells:
        if cell.cell_type == 'code':
            source = cell.source

            # Remove definitions
            if "def note(msg" in source or "def sec(title):" in source:
                lines = source.split('\n')
                new_lines = []
                for line in lines:
                    if "def note(" in line or "def sec(" in line:
                        modified = True
                        continue
                    if "display(Markdown" in line and "alert-info" in line:
                        modified = True
                        continue
                    if "print" in line and "title.upper()" in line:
                         modified = True
                         continue
                    new_lines.append(line)
                source = '\n'.join(new_lines)
                cell.source = source

            # Handle usages
            if 'note(' in source or 'sec(' in source or '!pip' in source:
                lines = source.split('\n')
                current_block = []

                def flush_code(block):
                    if not block: return
                    content = '\n'.join(block)
                    if content.strip():
                        new_cells.append(nbformat.v4.new_code_cell(content))

                for line in lines:
                    if pip_pattern.match(line):
                        modified = True
                        continue # Remove pip

                    note_match = note_pattern.match(line)
                    sec_match = sec_pattern.match(line)

                    if note_match:
                        prefix = note_match.group(1)
                        content = note_match.group(3)
                        suffix = note_match.group(4)

                        if not prefix.strip():
                            indent = prefix
                            if not suffix.strip() or suffix.strip().startswith('#'):
                                # Top level note
                                if len(indent) == 0:
                                    flush_code(current_block)
                                    current_block = []
                                    new_cells.append(nbformat.v4.new_markdown_cell(f"> **Note:** {content}"))
                                    modified = True
                                else:
                                    safe_content = content.replace('"', '\\"')
                                    new_line = f"{indent}display(Markdown(f\"> **Note:** {safe_content}\"))"
                                    if suffix.strip(): new_line += f" {suffix}"
                                    current_block.append(new_line)
                                    modified = True
                            else:
                                safe_content = content.replace('"', '\\"')
                                new_line = f"{prefix}display(Markdown(f\"> **Note:** {safe_content}\")){suffix}"
                                current_block.append(new_line)
                                modified = True
                        else:
                            safe_content = content.replace('"', '\\"')
                            new_line = f"{prefix}display(Markdown(f\"> **Note:** {safe_content}\")){suffix}"
                            current_block.append(new_line)
                            modified = True

                    elif sec_match:
                         indent = sec_match.group(1)
                         content = sec_match.group(3)

                         if len(indent) == 0:
                             flush_code(current_block)
                             current_block = []
                             new_cells.append(nbformat.v4.new_markdown_cell(f"### {content}"))
                             modified = True
                         else:
                             new_line = f"{indent}display(Markdown(f'### {content}'))"
                             current_block.append(new_line)
                             modified = True
                    else:
                        current_block.append(line)

                flush_code(current_block)
            else:
                new_cells.append(cell)
        else:
            new_cells.append(cell)

    nb.cells = new_cells

    # 2. Add Guard for Pysinc
    if "pysinc" in filepath.lower():
        has_guard = False
        for cell in nb.cells:
             if "PYSINC_AVAILABLE" in cell.source:
                 has_guard = True
                 break

        if not has_guard:
            guard_cell = nbformat.v4.new_code_cell("""try:
    from pysinc.Sinc import Sinc
    PYSINC_AVAILABLE = True
except ImportError:
    PYSINC_AVAILABLE = False
    from IPython.display import display, Markdown
    display(Markdown("> **Note:** `pysinc` not found. Please install via `pip install pysinc` or check environment."))""")

            insert_idx = 0
            for i, cell in enumerate(nb.cells):
                if cell.cell_type == 'code' and "import" in cell.source:
                    insert_idx = i + 1
                    break

            nb.cells.insert(insert_idx, guard_cell)
            modified = True
            print("  Inserted Pysinc guard.")

    # 3. Check/Inject Headers (Intro/Summary)
    has_intro = False
    for cell in nb.cells[:5]:
        if cell.cell_type == 'markdown':
            if cell.source.strip().startswith('# Introduction') or cell.source.strip().startswith('# The Lens'):
                has_intro = True
                break

    if not has_intro:
        insert_idx = 0
        if len(nb.cells) > 0 and '# ' in nb.cells[0].source:
             insert_idx = 1
        if len(nb.cells) > 1 and 'import' in nb.cells[1].source:
             insert_idx = 2

        intro_text = "# Introduction\n\nThis notebook explores the topic using computational methods. (Content to be added)"
        nb.cells.insert(min(insert_idx, len(nb.cells)), nbformat.v4.new_markdown_cell(intro_text))
        modified = True
        print("  Inserted Introduction.")

    has_summary = False
    for cell in nb.cells[-5:]:
        if cell.cell_type == 'markdown':
            if cell.source.strip().startswith('# Summary') or cell.source.strip().startswith('# Conclusion'):
                has_summary = True
                break

    if not has_summary:
        nb.cells.append(nbformat.v4.new_markdown_cell("# Summary\n\nKey takeaways from this notebook."))
        modified = True
        print("  Appended Summary.")

    # 4. Inject Plot Style
    if nb.cells:
        for cell in nb.cells:
            if cell.cell_type == 'code':
                if 'matplotlib' in cell.source or 'plt.' in cell.source:
                    if "plt.style.use('seaborn-v0_8-whitegrid')" not in cell.source:
                        lines = cell.source.split('\n')
                        import_idx = -1
                        for i, line in enumerate(lines):
                            if 'import' in line and 'matplotlib' in line:
                                import_idx = i

                        if import_idx != -1:
                            lines.insert(import_idx + 1, "plt.style.use('seaborn-v0_8-whitegrid')")
                            cell.source = '\n'.join(lines)
                            modified = True
                            print("  Injected plot style.")
                break # Only check first code cell

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print("  Saved changes.")
    else:
        print("  No changes needed.")

def main():
    # Target ALL potential notebook directories
    target_dirs = [
        '01-Foundations',
        '02-Numerical-Methods',
        '03-Economic-Modeling',
        '04-Macro-Models',
        '05-Micro-Models',
        '06-Econometrics',
        '07-Machine-Learning',
        '08-Time-Series',
        '09-Finance',
        '10-Specialized-Models',
        'high_performance_python',
        'Appendix'
    ]

    notebooks = []
    for d in target_dirs:
        notebooks.extend(glob.glob(f'{d}/*.ipynb'))

    # Filter checkpoints and executed
    notebooks = [nb for nb in notebooks if '.ipynb_checkpoints' not in nb and '_executed' not in nb]

    print(f"Fixing {len(notebooks)} notebooks...")
    for nb_path in notebooks:
        fix_notebook(nb_path)

if __name__ == '__main__':
    main()
