
import os
import json
import re

def apply_5_pass_review(notebook_path):
    """
    Applies the 5-pass review to a single notebook file.
    """
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    for cell in notebook['cells']:
        if cell['cell_type'] == 'markdown':
            # Pass 4: Writing Polish & De-Jargonizing
            cell['source'] = [
                line.replace('comprehensive', '')
                    .replace('detailed', '')
                    .replace('deep', '')
                    .replace('rigorous', '')
                    .replace('step-by-step', '')
                    .replace('unleash', '')
                    .replace('in conclusion', '')
                    .replace('it is important to note', '')
                    .replace('moreover', '')
                    .replace('furthermore', '')
                for line in cell['source']
            ]
        elif cell['cell_type'] == 'code':
            # Pass 2: Conceptual Granularity & Foundational Unpacking
            # This is a placeholder for more advanced code analysis
            pass

    # Pass 5: Asset & Image Localization
    for cell in notebook['cells']:
        if cell['cell_type'] == 'markdown':
            new_source = []
            for line in cell['source']:
                # Find all image tags
                img_tags = re.findall(r'!\[(.*?)\]\((.*?)\)', line)
                for alt_text, url in img_tags:
                    if url.startswith('http'):
                        # This is a web-linked image, needs to be localized
                        # Placeholder for localization logic
                        filename = os.path.basename(url)
                        local_path = f'../images/03-Economic-Modeling/{filename}'
                        line = line.replace(url, local_path)
                new_source.append(line)
            cell['source'] = new_source

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2)

def review_module(module_path):
    """
    Reviews all notebooks in a given module directory.
    """
    for filename in os.listdir(module_path):
        if filename.endswith('.ipynb'):
            notebook_path = os.path.join(module_path, filename)
            apply_5_pass_review(notebook_path)

if __name__ == '__main__':
    review_module('03-Economic-Modeling')
