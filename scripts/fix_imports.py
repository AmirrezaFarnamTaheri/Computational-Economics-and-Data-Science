import nbformat
import os

def fix_imports():
    # 1. Fix 05_Optimization
    nb_opt_path = '02-Numerical-Methods/05_Optimization.ipynb'
    with open(nb_opt_path, 'r', encoding='utf-8') as f:
        nb_opt = nbformat.read(f, as_version=4)

    # Locate the visualization cell and add imports
    for cell in nb_opt.cells:
        if "rosen_2d" in cell.source and "minimize(rosen" in cell.source:
            if "from scipy.optimize import minimize, rosen" not in cell.source:
                cell.source = "from scipy.optimize import minimize, rosen\nimport numpy as np\nimport matplotlib.pyplot as plt\n" + cell.source
                print(f"Fixed imports in {nb_opt_path}")

    with open(nb_opt_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb_opt, f)

    # 2. Fix 01_Dynamic_Programming
    nb_dp_path = '03-Economic-Modeling/01_Dynamic_Programming.ipynb'
    with open(nb_dp_path, 'r', encoding='utf-8') as f:
        nb_dp = nbformat.read(f, as_version=4)

    for cell in nb_dp.cells:
        if "os.makedirs" in cell.source:
            if "import os" not in cell.source and "import os" not in nb_dp.cells[1].source: # Heuristic check setup cell
                 cell.source = "import os\nfrom IPython.display import Image, display\n" + cell.source
                 print(f"Fixed os import in {nb_dp_path}")
            elif "import os" not in cell.source:
                 # It might be in setup, but local import is safer for robustness
                 cell.source = "import os\n" + cell.source
                 print(f"Added local os import in {nb_dp_path}")

    with open(nb_dp_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb_dp, f)

    # 3. Fix 01_Job_Search
    nb_js_path = '04-Macro-Models/01_Job_Search.ipynb'
    with open(nb_js_path, 'r', encoding='utf-8') as f:
        nb_js = nbformat.read(f, as_version=4)

    for cell in nb_js.cells:
        if "os.makedirs" in cell.source:
             if "import os" not in cell.source:
                 cell.source = "import os\nfrom IPython.display import Image, display\n" + cell.source
                 print(f"Fixed os import in {nb_js_path}")

    with open(nb_js_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb_js, f)

if __name__ == "__main__":
    fix_imports()
