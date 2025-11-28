import os
import nbformat
import glob

def check_structure(notebook_path):
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    except Exception as e:
        return f"ERROR: Could not read file: {e}"

    has_lens = False
    lens_level = 0
    has_summary = False
    summary_level = 0

    lens_titles = ["introduction", "the lens", "lens"]
    summary_titles = ["summary", "conclusion", "chapter summary"]

    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            lines = cell.source.split('\n')
            for line in lines:
                line = line.strip()
                if line.startswith('#'):
                    # Count hashes
                    level = 0
                    for char in line:
                        if char == '#':
                            level += 1
                        else:
                            break

                    title = line.lstrip('#').strip().lower()

                    # Check for Lens
                    if any(t in title for t in lens_titles):
                        # Avoid matching "Introduction to Data Acquisition" if it's the main title
                        # But we want to catch "Introduction" section.
                        # Usually the main title is just the notebook name.
                        # We are looking for the narrative intro.
                        if not has_lens: # Only catch the first one
                            has_lens = True
                            lens_level = level

                    # Check for Summary
                    if any(t in title for t in summary_titles):
                        has_summary = True
                        summary_level = level

    return {
        'has_lens': has_lens,
        'lens_level': lens_level,
        'has_summary': has_summary,
        'summary_level': summary_level
    }

def main():
    notebooks = sorted(glob.glob("**/*.ipynb", recursive=True))
    print(f"{'Notebook':<60} | {'Lens':<10} | {'Summary':<10}")
    print("-" * 86)

    issues = []

    for nb_path in notebooks:
        if "checkpoints" in nb_path:
            continue

        result = check_structure(nb_path)

        if isinstance(result, str):
            print(f"{nb_path:<60} | {result}")
            continue

        lens_status = f"H{result['lens_level']}" if result['has_lens'] else "MISSING"
        summary_status = f"H{result['summary_level']}" if result['has_summary'] else "MISSING"

        # Flag issues: Missing or Wrong Level (Standard is H1 or H2, but H3 is definitely weak)
        # Actually, Gold Standard in 01_Introduction was H3 for "Introduction" but H1/H2 is preferred?
        # Let's check 01_Introduction again.
        # It had "### Introduction: Computation as Lens and Laboratory" (H3).
        # And "# Summary" (H1) or "### 11. Chapter Summary" (H3).
        # Wait, the read_file of 01_Introduction showed "### Introduction..." and "### Chapter Summary".
        # But the user Prompt said "Standardize headers".
        # The user roadmap says "# Introduction" or "# The Lens". So H1 is the goal.

        if result['has_lens'] and result['lens_level'] > 1:
             lens_status += " (Weak)"
        if result['has_summary'] and result['summary_level'] > 1:
             summary_status += " (Weak)"

        if "MISSING" in lens_status or "MISSING" in summary_status or "Weak" in lens_status or "Weak" in summary_status:
             print(f"{nb_path:<60} | {lens_status:<10} | {summary_status:<10}")
             issues.append(nb_path)

    print("-" * 86)
    print(f"Total notebooks with issues: {len(issues)}")

if __name__ == "__main__":
    main()
