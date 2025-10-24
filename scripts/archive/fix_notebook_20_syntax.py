
import json

def fix_notebook_20_syntax(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            source_code = ''.join(cell['source'])
            if "ax.set(xlabel='Log GDP per Capita (Standardized)', ylabel='Spatially Lagged Log GDP per Capita (Neighbors\\\\' Average)')" in source_code:
                cell['source'] = [line.replace("Neighbors\\\\' Average", "Neighbors' Average") for line in cell['source']]
                break

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)

if __name__ == '__main__':
    fix_notebook_20_syntax('07-Machine-Learning/20_Geospatial_Data.ipynb')
