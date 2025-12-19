import os
import nbformat
import json

def get_notebook_outline(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    except Exception as e:
        return f"Error reading {filepath}: {e}"

    outline = []

    # Check sections
    sections = {
        "Introduction": False,
        "Theorems": [],
        "Proofs": [],
        "Examples": [],
        "Exercises": []
    }

    file_features = {
        "widgets": False,
        "theorems": False,
        "examples": False,
        "codes": 0,
        "history": False,
        "concepts": False
    }

    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            source = cell.source
            # Simple header extraction
            for line in source.split('\n'):
                if line.strip().startswith('#'):
                    outline.append(line.strip())

                    # Check for sections
                    lower_line = line.lower()
                    if "introduction" in lower_line:
                        sections["Introduction"] = True
                    if "theorem" in lower_line:
                        sections["Theorems"].append(line.strip())
                        file_features["theorems"] = True
                    if "proof" in lower_line:
                        sections["Proofs"].append(line.strip())
                    if "example" in lower_line:
                        sections["Examples"].append(line.strip())
                        file_features["examples"] = True
                    if "exercise" in lower_line:
                        sections["Exercises"].append(line.strip())
                    if "history" in lower_line or "historical" in lower_line:
                        file_features["history"] = True
                    if "concept" in lower_line:
                        file_features["concepts"] = True

            if "ipywidgets" in source or "interactive" in source: # Very basic check
                 file_features["widgets"] = True

        elif cell.cell_type == 'code':
            file_features["codes"] += 1
            if "ipywidgets" in cell.source or "interactive" in cell.source:
                file_features["widgets"] = True

    return {
        "filepath": filepath,
        "outline": outline,
        "sections": sections,
        "features": file_features
    }

def main():
    root_dir = "."
    report = []

    # Walk through directories
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d != 'site']

        for file in files:
            if file.endswith(".ipynb"):
                filepath = os.path.join(root, file)
                print(f"Processing {filepath}...")
                data = get_notebook_outline(filepath)
                report.append(data)

    # Write report
    with open("notebook_structure_report.json", "w") as f:
        json.dump(report, f, indent=2)

    # Also create a readable markdown version
    with open("notebook_structure.md", "w") as f:
        f.write("# Notebook Structure Report\n\n")
        for item in report:
            f.write(f"## {item['filepath']}\n")

            f.write("### Features\n")
            feat = item['features']
            f.write(f"- **Code Cells**: {feat['codes']}\n")
            f.write(f"- **Widgets**: {feat['widgets']}\n")
            f.write(f"- **Theorems**: {feat['theorems']}\n")
            f.write(f"- **Examples**: {feat['examples']}\n")
            f.write(f"- **History**: {feat['history']}\n")

            f.write("\n### Outline\n")
            for line in item['outline']:
                f.write(f"{line}\n")
            f.write("\n---\n")

if __name__ == "__main__":
    main()
