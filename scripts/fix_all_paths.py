#!/usr/bin/env python3
"""
Fix all Windows-style backslashes in paths to forward slashes for cross-platform compatibility.
This script fixes:
1. image_path_mapping.json
2. All Python scripts with path strings
"""

import json
import os
import re
from pathlib import Path

def fix_json_paths():
    """Fix Windows backslashes in image_path_mapping.json"""
    json_path = Path(__file__).parent.parent / "image_path_mapping.json"

    if not json_path.exists():
        print(f"⚠ {json_path} not found, skipping")
        return

    print(f"Fixing paths in {json_path}...")

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Convert all backslashes to forward slashes
    fixed_data = {}
    changes = 0
    for key, value in data.items():
        new_key = key.replace('\\\\', '/').replace('\\', '/')
        new_value = value.replace('\\\\', '/').replace('\\', '/')
        fixed_data[new_key] = new_value
        if new_key != key or new_value != value:
            changes += 1

    # Write back
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(fixed_data, f, indent=2, ensure_ascii=False)

    print(f"✓ Fixed {changes} path entries in image_path_mapping.json")

def fix_python_file_paths(file_path):
    """Fix Windows backslashes in a single Python file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Pattern to find strings with Windows paths like "images\png\file.png"
    # Match strings containing backslashes that look like paths
    def replace_path(match):
        quote = match.group(1)
        path = match.group(2)
        # Only replace if it looks like a file path (contains image, data, etc.)
        if any(keyword in path.lower() for keyword in ['image', 'png', 'jpg', 'data', 'csv', 'models']):
            fixed_path = path.replace('\\\\', '/').replace('\\', '/')
            return f'{quote}{fixed_path}{quote}'
        return match.group(0)

    # Match both single and double quoted strings
    content = re.sub(r'(["\'])([^"\']*\\[^"\']*)\1', replace_path, content)

    if content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def fix_all_python_paths():
    """Fix paths in all Python scripts"""
    scripts_dir = Path(__file__).parent
    root_dir = scripts_dir.parent

    python_files = list(scripts_dir.glob("*.py")) + list(root_dir.glob("*.py"))

    fixed_count = 0
    for py_file in python_files:
        if py_file.name == "fix_all_paths.py":  # Skip this script
            continue
        try:
            if fix_python_file_paths(py_file):
                print(f"✓ Fixed paths in {py_file.name}")
                fixed_count += 1
        except Exception as e:
            print(f"⚠ Error fixing {py_file.name}: {e}")

    print(f"\n✓ Fixed {fixed_count} Python files")

if __name__ == "__main__":
    print("=" * 70)
    print("Fixing all Windows-style paths to Unix-style paths")
    print("=" * 70)
    print()

    fix_json_paths()
    print()
    fix_all_python_paths()

    print()
    print("=" * 70)
    print("✓ All path fixes complete!")
    print("=" * 70)
