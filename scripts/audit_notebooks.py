import os
import json
import nbformat
import glob
import re

def audit_notebook(filepath):
    """
    Audits a single notebook for compliance with the Gold Standard.
    Returns a dictionary of issues.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    except Exception as e:
        return {'status': 'error', 'message': f'Failed to read notebook: {str(e)}'}

    issues = []

    # Check for 'The Lens' or 'Introduction'
    has_lens = False
    has_summary = False

    # Check headers in the first few cells
    for cell in nb.cells[:5]:
        if cell.cell_type == 'markdown':
            source = cell.source.strip()
            if source.startswith('# Introduction') or source.startswith('# The Lens'):
                has_lens = True
                break

    # Check headers in the last few cells
    for cell in nb.cells[-5:]:
        if cell.cell_type == 'markdown':
            source = cell.source.strip()
            if source.startswith('# Summary') or source.startswith('# Conclusion'):
                has_summary = True
                break

    if not has_lens:
        issues.append('Missing "The Lens" or "Introduction" (H1) at start.')
    if not has_summary:
        issues.append('Missing "Summary" or "Conclusion" (H1) at end.')

    # Check for antipatterns
    for i, cell in enumerate(nb.cells):
        if cell.cell_type == 'code':
            if 'sec(' in cell.source:
                issues.append(f'Cell {i}: Found "sec()" antipattern.')
            if 'note(' in cell.source:
                issues.append(f'Cell {i}: Found "note()" antipattern.')

    status = 'pass' if not issues else 'fail'
    return {'status': status, 'issues': issues}

def main():
    notebooks = sorted(glob.glob('**/*.ipynb', recursive=True))
    # Filter out checkpoints
    notebooks = [nb for nb in notebooks if '.ipynb_checkpoints' not in nb]

    report = {}

    print(f"Auditing {len(notebooks)} notebooks...")

    for nb_path in notebooks:
        result = audit_notebook(nb_path)
        if result['status'] != 'pass':
            report[nb_path] = result['issues']
            print(f"❌ {nb_path}")
            for issue in result['issues']:
                print(f"  - {issue}")
        else:
            # print(f"✅ {nb_path}")
            pass

    print(f"\nAudit complete. {len(report)} notebooks require attention.")

    with open('audit_report.json', 'w') as f:
        json.dump(report, f, indent=2)

if __name__ == '__main__':
    main()
