
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor

def run_notebook(notebook_path):
    """
    Executes a notebook and raises an exception if any cell fails.
    """
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    proc = ExecutePreprocessor(timeout=600, kernel_name='python3')
    proc.preprocess(nb, {'metadata': {'path': '07-Machine-Learning/'}})

if __name__ == '__main__':
    try:
        run_notebook('07-Machine-Learning/03_Support_Vector_Machines.ipynb')
        print("Notebook executed successfully.")
    except Exception as e:
        print(f"Error executing notebook: {e}")
