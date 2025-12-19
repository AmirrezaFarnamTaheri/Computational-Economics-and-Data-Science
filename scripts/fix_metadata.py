import json
import os

files_to_fix = [
    "06-Econometrics/03_Causal_Inference.ipynb",
    "06-Econometrics/05_Instrumental_Variables.ipynb",
    "06-Econometrics/09_Classical_Time_Series_Analysis.ipynb",
    "07-Machine-Learning/12_Self_Supervised_Learning.ipynb",
    "07-Machine-Learning/22_Style_Transfer_and_Advanced_Vision.ipynb"
]

new_metadata = {
    "kernelspec": {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
    },
    "language_info": {
        "codemirror_mode": {
            "name": "ipython",
            "version": 3
        },
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.10.0"
    }
}

for filepath in files_to_fix:
    if os.path.exists(filepath):
        print(f"Fixing metadata for {filepath}...")
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                notebook = json.load(f)

            notebook['metadata'] = new_metadata

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=1)

            print(f"Success: {filepath}")
        except Exception as e:
            print(f"Error fixing {filepath}: {e}")
    else:
        print(f"File not found: {filepath}")
