import os
import json
import re
import pandas as pd

def audit_notebooks(root_dir="."):
    results = []

    print(f"Starting audit of {root_dir}...")

    for root, dirs, files in os.walk(root_dir):
        if ".ipynb_checkpoints" in root:
            continue

        for file in files:
            if file.endswith(".ipynb"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        nb = json.load(f)
                except Exception as e:
                    print(f"Error reading {filepath}: {e}")
                    continue

                content = json.dumps(nb)
                cells = nb.get("cells", [])

                # Checks
                has_license = False
                if cells and cells[0]["cell_type"] == "markdown":
                    if "License" in "".join(cells[0]["source"]):
                        has_license = True

                has_sec = "def sec(" in content
                has_note = "def note(" in content
                has_pip = "!pip" in content or "%pip" in content
                has_pdr = "pandas_datareader" in content

                # Check for summary
                has_summary = False
                for cell in cells:
                    if cell["cell_type"] == "markdown":
                        src = "".join(cell["source"]).lower()
                        if "# summary" in src or "## conclusion" in src or "### summary" in src:
                            has_summary = True
                            break

                # Check for hardcoded RBC solution (heuristic)
                has_hardcoded_rbc = "P_sol =" in content and "Q_sol =" in content

                results.append({
                    "module": os.path.basename(root),
                    "filename": file,
                    "has_license_header": has_license,
                    "has_sec_antipattern": has_sec,
                    "has_note_antipattern": has_note,
                    "has_pip_install": has_pip,
                    "has_pandas_datareader": has_pdr,
                    "has_summary": has_summary,
                    "has_hardcoded_rbc": has_hardcoded_rbc
                })

    df = pd.DataFrame(results)

    # Analysis
    print(f"\nTotal Notebooks: {len(df)}")
    print(f"Missing Header: {len(df[~df['has_license_header']])}")
    print(f"Using 'sec()' helper: {len(df[df['has_sec_antipattern']])}")
    print(f"Using 'note()' helper: {len(df[df['has_note_antipattern']])}")
    print(f"Inline Pip Installs: {len(df[df['has_pip_install']])}")
    print(f"Pandas Datareader Use: {len(df[df['has_pandas_datareader']])}")
    print(f"Missing Summary: {len(df[~df['has_summary']])}")

    # Save detail to file for inspection
    df.to_csv("notebook_audit_report.csv", index=False)
    print("\nDetailed report saved to notebook_audit_report.csv")

    # Print breakdown by module for the user
    print("\nBreakdown by Module (Anti-patterns):")
    print(df.groupby("module")[['has_sec_antipattern', 'has_note_antipattern']].sum())

if __name__ == "__main__":
    audit_notebooks()
