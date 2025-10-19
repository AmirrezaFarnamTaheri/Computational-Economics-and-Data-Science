import os
import nbformat
import json

def find_notebooks(directory):
    notebooks = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".ipynb") and not file.endswith(".nbconvert.ipynb"):
                notebooks.append(os.path.join(root, file))
    return notebooks

def validate_notebook_json(notebook_path):
    try:
        with open(notebook_path, 'r', encoding='utf-8') as f:
            nbformat.read(f, as_version=4)
        print(f"  PASSED: {notebook_path}")
        return True
    except (json.decoder.JSONDecodeError, nbformat.reader.NotJSONError) as e:
        print(f"  FAILED: {notebook_path} - Invalid JSON format.")
        print(f"    Error: {e}")
        return False
    except Exception as e:
        print(f"  FAILED: {notebook_path} - An unexpected error occurred.")
        print(f"    Error: {e}")
        return False

if __name__ == "__main__":
    all_notebooks = []
    for module in [
        "01-Foundations",
        "02-Numerical-Methods",
        "03-Economic-Modeling",
        "04-Macro-Models",
        "05-Micro-Models",
        "06-Econometrics",
        "07-Machine-Learning",
        "08-Time-Series",
        "09-Finance",
        "10-Specialized-Models",
        "Appendix",
        "high_performance_python",
    ]:
        all_notebooks.extend(find_notebooks(module))

    all_valid = True
    for notebook in all_notebooks:
        if not validate_notebook_json(notebook):
            all_valid = False

    if all_valid:
        print("\nAll notebooks validated successfully!")
    else:
        print("\nSome notebooks failed validation.")