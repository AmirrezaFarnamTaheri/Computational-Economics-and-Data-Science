
import json

def fix_notebook_20_syntax_v5(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    for cell in notebook['cells']:
        if cell['cell_type'] == 'code':
            source = cell.get('source', [])
            new_source = []
            changed = False
            for line in source:
                if "ylabel='Spatially Lagged Log GDP per Capita (Neighbors\\' Average)'" in line:
                    # Simplify the string to avoid the apostrophe issue.
                    corrected_line = '    ax.set(xlabel=\'Log GDP per Capita (Standardized)\', ylabel="Spatially Lagged Log GDP per Capita")\n'
                    new_source.append(corrected_line)
                    changed = True
                else:
                    new_source.append(line)
            if changed:
                cell['source'] = new_source
                break

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)
    print("Fixed syntax error in notebook.")

if __name__ == '__main__':
    fix_notebook_20_syntax_v5('07-Machine-Learning/20_Geospatial_Data.ipynb')
