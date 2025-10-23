import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

# Set the notebook path
notebook_filename = '08-Time-Series/01_Introduction_to_Time_Series.ipynb'

# Read the notebook
with open(notebook_filename, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# Configure the preprocessor
ep = ExecutePreprocessor(timeout=600, kernel_name='python3')

# Execute the notebook
try:
    # The second argument is a dictionary for metadata, which can be empty
    ep.preprocess(nb, {'metadata': {'path': '08-Time-Series/'}})
    print(f"Successfully executed {notebook_filename}")
except Exception as e:
    print(f"Error executing {notebook_filename}:")
    print(e)

# You can optionally save the executed notebook
# with open('path/to/executed_notebook.ipynb', 'w', encoding='utf-8') as f:
#     nbformat.write(nb, f)
