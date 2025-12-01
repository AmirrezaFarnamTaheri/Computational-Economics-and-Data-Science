import os
import json
import glob
import re
import sys

def check_notebook(filepath):
    issues = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except json.JSONDecodeError:
        return ["Invalid JSON structure"]
    except Exception as e:
        return [f"Could not read file: {str(e)}"]

    cells = nb.get('cells', [])
    if not cells:
        return ["Notebook is empty"]

    # 1. Structure Check: Introduction (Lens) and Summary
    has_intro = False
    has_summary = False

    # Check first few markdown cells for Introduction
    for cell in cells[:5]:
        if cell['cell_type'] == 'markdown':
            src = ''.join(cell['source']).strip()
            if src.startswith('# Introduction') or src.startswith('# The Lens'):
                has_intro = True
                break

    # Check last few markdown cells for Summary
    for cell in cells[-5:]:
        if cell['cell_type'] == 'markdown':
            src = ''.join(cell['source']).strip()
            if src.startswith('# Summary') or src.startswith('# Conclusion'):
                has_summary = True
                break

    if not has_intro:
        issues.append("Missing '# Introduction' or '# The Lens' (H1) at the beginning")
    if not has_summary:
        issues.append("Missing '# Summary' or '# Conclusion' (H1) at the end")

    # 2. Plot Style Check
    first_code_found = False
    for cell in cells:
        if cell['cell_type'] == 'code':
            src = ''.join(cell['source'])
            if not first_code_found:
                if "plt.style.use" not in src and "seaborn" in src:
                    # Soft check
                    if "plt.style.use" not in src:
                         issues.append("First code cell missing 'plt.style.use(...)'")
                first_code_found = True

            # 3. Anti-patterns Check
            # Ignore indentation, just look for usage
            # But if it's display(Markdown(...)) it shouldn't trigger.
            # So we check for 'note(' NOT preceded by 'def '
            # And 'sec(' NOT preceded by 'def '

            # Simple regex matches note( anywhere.
            # We want to catch note("...")
            # If we replaced it with display(Markdown(f'> **Note:** ...')), 'note(' is gone.
            # So simplistic check works.

            if re.search(r'(?<!def )\bnote\(', src):
                 issues.append("Found 'note(...)' anti-pattern in code cell")
            if re.search(r'(?<!def )\bsec\(', src):
                 issues.append("Found 'sec(...)' anti-pattern in code cell")

            # 4. Pip Install Check
            # Ignore commented lines
            # Check line by line
            for line in src.split('\n'):
                if "!pip install" in line:
                    if not line.strip().startswith('#'):
                        issues.append("Found '!pip install' in code cell")

            # 5. Data Access Check (simple heuristic)
            if "pandas_datareader" in src or "yfinance" in src:
                if "try:" not in src and "except" not in src:
                     pass # Hard to detect reliably with simple regex across cells.

    return issues

def main():
    notebooks = glob.glob("**/*.ipynb", recursive=True)
    # Ignore checkpoints and executed copies if any remain
    notebooks = [nb for nb in notebooks if ".ipynb_checkpoints" not in nb and "_executed" not in nb]

    print(f"Auditing {len(notebooks)} notebooks...")

    error_count = 0
    passed_count = 0

    for nb_path in sorted(notebooks):
        issues = check_notebook(nb_path)
        if issues:
            print(f"\n[FAIL] {nb_path}")
            for issue in issues:
                print(f"  - {issue}")
            error_count += 1
        else:
            passed_count += 1

    print(f"\nSummary: {passed_count} passed, {error_count} failed.")

    if error_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
