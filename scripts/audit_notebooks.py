import os
import json
import re
import pandas as pd

def analyze_notebook(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            nb = json.load(f)
    except Exception as e:
        return {"error": str(e)}

    content_str = json.dumps(nb)
    cells = nb.get("cells", [])

    # --- Structural Checks ---
    has_license = False
    has_intro = False
    has_summary = False

    if cells and cells[0]["cell_type"] == "markdown":
        src0 = "".join(cells[0]["source"]).lower()
        if "license" in src0 and "badge" in src0:
            has_license = True

    for cell in cells:
        if cell["cell_type"] == "markdown":
            src = "".join(cell["source"]).lower()
            if any(x in src for x in ["# introduction", "## introduction", "### introduction", "overview", "motivation"]):
                has_intro = True
            if any(x in src for x in ["# summary", "## summary", "### summary", "## conclusion", "# conclusion"]):
                has_summary = True

    # --- Anti-Patterns & Code Quality ---
    has_sec = "def sec(" in content_str
    has_note = "def note(" in content_str
    has_pip = "!pip" in content_str or "%pip" in content_str
    has_pdr = "pandas_datareader" in content_str
    has_inv = "inv(" in content_str or "linalg.inv" in content_str

    # Heuristic for hardcoding: looking for large array literals often indicates hardcoded solutions
    # or searching for specific known bad variables
    has_hardcoded = "P_sol =" in content_str or "Q_sol =" in content_str

    # --- Visuals ---
    # Check if plotting is happening inline (looking for plt.plot without a script reference is tricky,
    # but we can check for import matplotlib and lack of 'from scripts import')
    has_plotting = "matplotlib.pyplot" in content_str or "plt.plot" in content_str
    uses_scripts = "from scripts" in content_str or "import scripts" in content_str

    return {
        "filepath": filepath,
        "module": os.path.dirname(filepath).split("/")[-1],
        "filename": os.path.basename(filepath),
        "has_license": has_license,
        "has_intro": has_intro,
        "has_summary": has_summary,
        "anti_sec": has_sec,
        "anti_note": has_note,
        "anti_pip": has_pip,
        "risk_pdr": has_pdr,
        "risk_inv": has_inv,
        "risk_hardcode": has_hardcoded,
        "has_plotting": has_plotting,
        "uses_scripts": uses_scripts
    }

def audit_notebooks(root_dir="."):
    results = []
    print(f"Starting comprehensive audit of {root_dir}...")

    for root, dirs, files in os.walk(root_dir):
        if ".ipynb_checkpoints" in root:
            continue
        for file in files:
            if file.endswith(".ipynb"):
                filepath = os.path.join(root, file)
                results.append(analyze_notebook(filepath))

    df = pd.DataFrame(results)

    # Calculate Scores (Simplified)
    # Score = 100 - penalties
    def calc_score(row):
        penalties = 0
        if not row['has_license']: penalties += 10
        if not row['has_summary']: penalties += 10
        if row['anti_sec']: penalties += 5
        if row['anti_note']: penalties += 5
        if row['anti_pip']: penalties += 20
        if row['risk_hardcode']: penalties += 20
        return max(0, 100 - penalties)

    df['score'] = df.apply(calc_score, axis=1)

    # Save full report
    df.to_csv("notebook_audit_detailed.csv", index=False)
    print("\nAudit Complete. Saved to notebook_audit_detailed.csv")

    # Summaries for the user
    print(f"\nTotal Notebooks: {len(df)}")
    print(f"Perfect Score (100): {len(df[df['score'] == 100])}")
    print(f"Needs Work (<80): {len(df[df['score'] < 80])}")
    print(f"Critical (<50): {len(df[df['score'] < 50])}")

    print("\nTop 10 'Dirtiest' Notebooks:")
    print(df.sort_values("score").head(10)[['module', 'filename', 'score']])

    print("\nAnti-Pattern Prevalence:")
    print(f"  - 'def sec/note': {len(df[df['anti_sec'] | df['anti_note']])}")
    print(f"  - Inline Pip: {len(df[df['anti_pip']])}")
    print(f"  - Hardcoded Logic: {len(df[df['risk_hardcode']])}")
    print(f"  - Missing Summary: {len(df[~df['has_summary']])}")

if __name__ == "__main__":
    audit_notebooks()
