import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import io
import sys

def run_notebook(notebook_path):
    """
    Executes a notebook and returns the executed notebook object.
    """
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

    try:
        ep.preprocess(nb, {'metadata': {'path': '07-Machine-Learning/'}})
        print(f"Successfully executed {notebook_path}")
        return nb
    except Exception as e:
        print(f"Error executing notebook {notebook_path}:")
        print(e)
        raise

if __name__ == '__main__':
    if len(sys.argv) > 1:
        notebook_path = sys.argv[1]
        run_notebook(notebook_path)
    else:
        print("Please provide a notebook path to execute.")
