import nbformat
import glob
import re
import os

def fix_antipatterns(cell_source):
    """
    Replaces sec() and note() calls with Markdown.
    Returns (new_source, changed_boolean)
    """
    lines = cell_source.split('\n')
    new_lines = []
    changed = False

    # Regex for simple sec('Title') or sec("Title")
    # We assume these are on their own lines as per previous patterns
    sec_pattern = re.compile(r"^\s*sec\(['\"](.*?)['\"]\)\s*$")
    note_pattern = re.compile(r"^\s*note\(['\"](.*?)['\"]\)\s*$")

    for line in lines:
        sec_match = sec_pattern.match(line)
        note_match = note_pattern.match(line)

        if sec_match:
            title = sec_match.group(1)
            new_lines.append(f"### {title}")
            changed = True
        elif note_match:
            msg = note_match.group(1)
            new_lines.append(f"> **Note:** {msg}")
            changed = True
        else:
            new_lines.append(line)

    return '\n'.join(new_lines), changed

def fix_notebook(filepath):
    print(f"Processing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    except Exception as e:
        print(f"  Error reading {filepath}: {e}")
        return

    modified = False

    # 1. Fix Antipatterns (sec/note in code cells)
    # We need to split code cells that contain sec/note into Markdown cells
    new_cells = []
    for cell in nb.cells:
        if cell.cell_type == 'code':
            # Check if cell contains sec() or note()
            # If it does, we might need to split it
            source = cell.source
            if 'sec(' in source or 'note(' in source:
                # Simple strategy: If the cell is ONLY sec/note calls, convert to Markdown
                # If it mixes code and sec/note, it's harder.
                # Let's inspect the lines.
                lines = source.split('\n')
                current_block = []
                current_type = 'code' # Start as code

                # Helper to flush current block
                def flush(block, type_):
                    if not block: return
                    content = '\n'.join(block)
                    if type_ == 'code':
                        new_cells.append(nbformat.v4.new_code_cell(content))
                    else:
                        new_cells.append(nbformat.v4.new_markdown_cell(content))

                sec_pattern = re.compile(r"^\s*sec\(['\"](.*?)['\"]\)\s*$")
                note_pattern = re.compile(r"^\s*note\(['\"](.*?)['\"]\)\s*$")

                for line in lines:
                    sec_match = sec_pattern.match(line)
                    note_match = note_pattern.match(line)

                    if sec_match:
                        # Flush previous code
                        flush(current_block, 'code')
                        current_block = []
                        # Add markdown header
                        title = sec_match.group(1)
                        new_cells.append(nbformat.v4.new_markdown_cell(f"### {title}"))
                        modified = True
                    elif note_match:
                        # Flush previous code
                        flush(current_block, 'code')
                        current_block = []
                        # Add markdown note
                        msg = note_match.group(1)
                        new_cells.append(nbformat.v4.new_markdown_cell(f"> **Note:** {msg}"))
                        modified = True
                    else:
                        current_block.append(line)

                # Flush remaining
                flush(current_block, 'code')
            else:
                new_cells.append(cell)
        else:
            new_cells.append(cell)

    nb.cells = new_cells

    # 2. Check/Inject Headers
    # We want "Introduction" (Lens) and "Summary"
    # Logic: Look at first non-setup markdown cell. If it's not H1 Intro, prepend one.
    # Look at last markdown cell. If not H1 Summary, append one.

    # Simple check for existing H1 Intro
    has_intro = False
    for cell in nb.cells[:5]:
        if cell.cell_type == 'markdown':
            if cell.source.strip().startswith('# Introduction') or cell.source.strip().startswith('# The Lens'):
                has_intro = True
                break

    if not has_intro:
        # Find where to insert. After the title/license cell, before imports?
        # Usually cell 0 is title/license. Cell 1 is setup. Cell 2 should be Intro.
        intro_cell = nbformat.v4.new_markdown_cell("# Introduction\n\n(Introduction text to be added)")
        # Insert at index 2 (0, 1, 2) or earlier if fewer cells
        insert_idx = min(2, len(nb.cells))
        nb.cells.insert(insert_idx, intro_cell)
        modified = True
        print("  Inserted Introduction placeholder.")

    # Simple check for existing H1 Summary
    has_summary = False
    for cell in nb.cells[-5:]:
        if cell.cell_type == 'markdown':
            if cell.source.strip().startswith('# Summary') or cell.source.strip().startswith('# Conclusion'):
                has_summary = True
                break

    if not has_summary:
        summary_cell = nbformat.v4.new_markdown_cell("# Summary\n\n(Summary text to be added)")
        nb.cells.append(summary_cell)
        modified = True
        print("  Appended Summary placeholder.")

    # 3. Standard Setup Injection (Optional, but good for consistency)
    # Check if first code cell has the standard imports
    if nb.cells:
        first_code_idx = -1
        for i, cell in enumerate(nb.cells):
            if cell.cell_type == 'code':
                first_code_idx = i
                break

        if first_code_idx != -1:
            code_source = nb.cells[first_code_idx].source
            if 'plt.style.use' not in code_source and 'seaborn' in code_source:
                 # It might be an old setup cell. Let's just update the style line if possible
                 # Or just leave it for now to avoid breaking custom setups.
                 pass

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print("  Saved changes.")
    else:
        print("  No changes needed.")

def main():
    # Load the audit report to target specific files?
    # Or just run on everything?
    # Let's run on everything in 07, 08, and Appendix since they were the main offenders.

    target_dirs = [
        '07-Machine-Learning',
        '08-Time-Series',
        'Appendix'
    ]

    notebooks = []
    for d in target_dirs:
        notebooks.extend(glob.glob(f'{d}/*.ipynb'))

    # Filter checkpoints
    notebooks = [nb for nb in notebooks if '.ipynb_checkpoints' not in nb]

    print(f"Targeting {len(notebooks)} notebooks for standardization...")

    for nb_path in notebooks:
        fix_notebook(nb_path)

if __name__ == '__main__':
    main()
