
import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import sys
import os

def run_notebook(notebook_path):
    """Executes a notebook and saves it in place."""
    try:
        # Check if the notebook exists
        if not os.path.exists(notebook_path):
            print(f"Error: Notebook not found at '{notebook_path}'")
            sys.exit(1)

        # Read the notebook
        with open(notebook_path, 'r') as f:
            nb = nbformat.read(f, as_version=4)

        # Configure the execution preprocessor
        # We can specify a kernel name if needed, otherwise it uses the default
        ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

        # Execute the notebook
        # The second argument is a dictionary for metadata, we can leave it empty
        ep.preprocess(nb, {'metadata': {'path': os.path.dirname(notebook_path) or '.'}})

        # Write the executed notebook back to the file
        with open(notebook_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)

        print(f"Notebook '{notebook_path}' executed successfully.")

    except Exception as e:
        print(f"An error occurred while running the notebook '{notebook_path}':")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python run_notebook.py <path_to_notebook>")
        sys.exit(1)

    notebook_to_run = sys.argv[1]
    run_notebook(notebook_to_run)
