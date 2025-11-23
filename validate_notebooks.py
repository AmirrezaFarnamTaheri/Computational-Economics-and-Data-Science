import os
import json
import re
from pathlib import Path

def validate_notebooks(root_dir="."):
    """
    Scans all .ipynb files in the repository and validates them.
    Checks for:
    1. Valid JSON structure.
    2. Existence of referenced images.
    """
    print("Starting notebook validation...")

    notebooks = []
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".ipynb") and ".ipynb_checkpoints" not in root:
                notebooks.append(os.path.join(root, file))

    all_passed = True

    for nb_path in notebooks:
        print(f"Checking {nb_path}...")
        try:
            with open(nb_path, 'r', encoding='utf-8') as f:
                nb_content = json.load(f)

            # Check for image references in markdown cells
            for cell in nb_content.get("cells", []):
                if cell.get("cell_type") == "markdown":
                    source = "".join(cell.get("source", []))
                    # Regex to find markdown image links: ![alt](path)
                    # and HTML img tags: <img src="path" ...>
                    md_images = re.findall(r'!\[.*?\]\((.*?)\)', source)
                    html_images = re.findall(r'<img.*?src=[\'"](.*?)[\'"]', source)

                    all_images = md_images + html_images

                    for img_path in all_images:
                        # Resolve relative paths
                        # Assumption: paths are relative to the notebook location
                        if img_path.startswith("http"):
                            continue # Skip external links

                        # Handle anchors or query params
                        img_path_clean = img_path.split('#')[0].split('?')[0]

                        nb_dir = os.path.dirname(nb_path)
                        full_img_path = os.path.normpath(os.path.join(nb_dir, img_path_clean))

                        if not os.path.exists(full_img_path):
                            print(f"  [ERROR] Missing image: {img_path} (resolved to {full_img_path})")
                            all_passed = False
                        else:
                            # print(f"  [OK] Found image: {img_path}")
                            pass

        except json.JSONDecodeError:
            print(f"  [ERROR] Invalid JSON in {nb_path}")
            all_passed = False
        except Exception as e:
            print(f"  [ERROR] Error processing {nb_path}: {str(e)}")
            all_passed = False

    if all_passed:
        print("\nValidation passed! All notebooks are valid and images exist.")
    else:
        print("\nValidation failed. See errors above.")
        exit(1)

if __name__ == "__main__":
    validate_notebooks()