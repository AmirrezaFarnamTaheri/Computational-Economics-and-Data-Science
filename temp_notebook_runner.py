
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def run_notebook(notebook_path):
    """
    Executes a notebook and raises an exception if any cell fails.
    """
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    # The ipython kernel is required for this to run
    proc = ExecutePreprocessor(timeout=600, kernel_name='python3')
    proc.preprocess(nb, {'metadata': {'path': '03-Economic-Modeling/'}})

if __name__ == '__main__':
    try:
        run_notebook('03-Economic-Modeling/01_Dynamic_Programming.ipynb')
        print("Notebook executed successfully.")
    except Exception as e:
        print(f"Error executing notebook: {e}")
