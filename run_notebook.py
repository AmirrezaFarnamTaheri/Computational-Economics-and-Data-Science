import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os
import sys

# Set the notebook path from the command-line argument
if len(sys.argv) < 2:
    print("Usage: python run_notebook.py <path_to_notebook>")
    sys.exit(1)
notebook_filename = sys.argv[1]
notebook_path = os.path.dirname(notebook_filename)

# Read the notebook
with open(notebook_filename, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# Configure the preprocessor
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

# Execute the notebook
try:
    # The second argument is a dictionary for metadata, which can be empty
    ep.preprocess(nb, {'metadata': {'path': notebook_path}})
    print(f"Successfully executed {notebook_filename}")
except Exception as e:
    print(f"Error executing {notebook_filename}:")
    print(e)

# You can optionally save the executed notebook
# with open('path/to/executed_notebook.ipynb', 'w', encoding='utf-8') as f:
#     nbformat.write(nb, f)
