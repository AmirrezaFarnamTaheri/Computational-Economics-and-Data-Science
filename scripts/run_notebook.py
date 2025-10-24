import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import sys

def run_notebook(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)

    preprocessor = ExecutePreprocessor(timeout=600, kernel_name='python3')

    try:
        preprocessor.preprocess(nb, {'metadata': {'path': './'}})
    except Exception as e:
        print(f"Error executing the notebook: {e}")
        # Re-raise exception to prevent saving corrupted notebooks
        raise e

    # Only save if execution was successful
    with open(notebook_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_notebook(sys.argv[1])
