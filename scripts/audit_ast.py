import os
import json
import ast
import pandas as pd

def audit_ast(root_dir="."):
    results = []
    print(f"Starting AST audit of {root_dir}...")

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

                # Metrics
                num_cells = 0
                num_code_cells = 0
                num_markdown_cells = 0
                has_plot_labels = True # Assume true, disprove if plot calls exist without setters
                plot_calls = 0
                labeled_plot_calls = 0
                imports = set()
                classes_defined = 0
                functions_defined = 0
                magic_numbers = 0

                for cell in nb.get("cells", []):
                    num_cells += 1
                    if cell["cell_type"] == "markdown":
                        num_markdown_cells += 1
                    elif cell["cell_type"] == "code":
                        num_code_cells += 1
                        source = "".join(cell["source"])
                        if not source.strip(): continue

                        # Ignore ipython magics for parsing
                        source_clean = "\n".join([line for line in source.splitlines() if not line.startswith("%") and not line.startswith("!")])

                        try:
                            tree = ast.parse(source_clean)
                        except SyntaxError:
                            continue # Skip cells with syntax errors (e.g. partial code)

                        for node in ast.walk(tree):
                            # Imports
                            if isinstance(node, ast.Import):
                                for n in node.names: imports.add(n.name.split('.')[0])
                            elif isinstance(node, ast.ImportFrom):
                                if node.module: imports.add(node.module.split('.')[0])

                            # Structure
                            if isinstance(node, ast.ClassDef):
                                classes_defined += 1
                            if isinstance(node, ast.FunctionDef):
                                functions_defined += 1

                            # Visuals (Heuristic)
                            if isinstance(node, ast.Call):
                                if hasattr(node.func, 'attr'):
                                    name = node.func.attr
                                    if name in ['plot', 'scatter', 'bar', 'hist']:
                                        plot_calls += 1
                                    if name in ['set_title', 'set_xlabel', 'set_ylabel', 'title', 'xlabel', 'ylabel']:
                                        labeled_plot_calls += 1

                            # Magic Numbers (Heuristic: numbers not 0 or 1 in assignments)
                            if isinstance(node, ast.Assign):
                                if isinstance(node.value, ast.Constant) and isinstance(node.value.value, (int, float)):
                                    if node.value.value not in [0, 1, -1, 0.0, 1.0]:
                                        magic_numbers += 1

                # Plotting Score
                if plot_calls > 0:
                    visual_score = labeled_plot_calls / (plot_calls * 3) # Expect title, xlabel, ylabel
                    if visual_score > 1: visual_score = 1
                else:
                    visual_score = 1.0 # N/A

                results.append({
                    "module": os.path.basename(root),
                    "filename": file,
                    "total_cells": num_cells,
                    "markdown_ratio": num_markdown_cells / max(1, num_cells),
                    "classes": classes_defined,
                    "functions": functions_defined,
                    "magic_numbers": magic_numbers,
                    "visual_score": visual_score,
                    "imports": list(imports)
                })

    df = pd.DataFrame(results)
    df.to_csv("notebook_ast_audit.csv", index=False)
    print("\nAST Audit Complete. Saved to notebook_ast_audit.csv")

    # Summary
    print(f"\nTotal Files Scanned: {len(df)}")
    print(f"Avg Markdown Ratio: {df['markdown_ratio'].mean():.2f}")
    print(f"Total Classes Defined: {df['classes'].sum()}")
    print(f"Total Functions Defined: {df['functions'].sum()}")
    print(f"Avg Visual Score (where plots exist): {df[df['visual_score'] < 1]['visual_score'].mean():.2f}")

if __name__ == "__main__":
    audit_ast()
