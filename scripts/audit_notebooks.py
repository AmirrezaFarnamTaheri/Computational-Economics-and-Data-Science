import ast
import json
import os
import re

import nbformat


def analyze_markdown_cell(source):
    words = len(source.split())
    # Regex for equations might need to be robust but simple is fine for audit
    equations = len(
        re.findall(r"(?<!\\)\$.*?(?<!\\)\$", source, re.DOTALL)
    )  # Simple inline
    # Block equations
    equations += len(re.findall(r"(?<!\\)\$\$.*?(?<!\\)\$\$", source, re.DOTALL))

    links = len(re.findall(r"\[.*?\]\(.*?\)", source))
    images = len(re.findall(r"!\[.*?\]\(.*?\)", source))
    images += len(re.findall(r"<img.*?>", source))

    todos = len(re.findall(r"(?i)\b(todo|fixme)\b", source))

    headers = []
    in_code_block = False

    for line in source.split("\n"):
        stripped_line = line.strip()

        # Toggle code block state
        if stripped_line.startswith("```"):
            in_code_block = not in_code_block
            continue

        # Skip lines inside code blocks
        if in_code_block:
            continue

        if line.lstrip().startswith("#"):
            # Count the number of hash characters
            hashes = len(line) - len(line.lstrip("#"))
            text = line.lstrip("#").strip()
            if text:  # Ignore empty headers
                headers.append({"level": hashes, "text": text})

    return {
        "words": words,
        "equations": equations,
        "links": links,
        "images": images,
        "todos": todos,
        "headers": headers,
    }


def analyze_code_cell(source):
    lines = len(source.split("\n"))
    imports = set()
    # Remove magic commands for AST parsing
    clean_source = "\n".join(
        [
            line if not line.strip().startswith(("%", "!")) else f"# {line}"
            for line in source.split("\n")
        ]
    )

    try:
        tree = ast.parse(clean_source)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imports.add(node.module.split(".")[0])
    except (SyntaxError, ValueError):
        pass
    return {"lines": lines, "imports": list(imports)}


def audit_notebook(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            nb = nbformat.read(f, as_version=4)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

    # Metadata
    kernelspec = nb.metadata.get("kernelspec", {}).get("display_name", "Unknown")
    language = nb.metadata.get("kernelspec", {}).get("language", "Unknown")

    # Counters
    stats = {
        "cells": {"markdown": 0, "code": 0, "raw": 0},
        "content": {
            "words": 0,
            "code_lines": 0,
            "equations": 0,
            "images": 0,
            "links": 0,
            "todos": 0,
        },
        "features": {
            "widgets": False,
            "theorems": False,
            "proofs": False,
            "examples": False,
            "exercises": False,
            "history": False,
            "concepts": False,
        },
    }

    all_headers = []
    all_imports = set()

    sections = {
        "Introduction": False,
        "Theorems": [],
        "Proofs": [],
        "Examples": [],
        "Exercises": [],
    }

    for cell in nb.cells:
        if cell.cell_type == "markdown":
            stats["cells"]["markdown"] += 1
            md_analysis = analyze_markdown_cell(cell.source)

            stats["content"]["words"] += md_analysis["words"]
            stats["content"]["equations"] += md_analysis["equations"]
            stats["content"]["links"] += md_analysis["links"]
            stats["content"]["images"] += md_analysis["images"]
            stats["content"]["todos"] += md_analysis["todos"]

            all_headers.extend(md_analysis["headers"])

            # Feature detection in markdown
            lower_source = cell.source.lower()
            if "ipywidgets" in lower_source or "interactive" in lower_source:
                stats["features"]["widgets"] = True

            # Section detection
            for header_obj in md_analysis["headers"]:
                header_text = header_obj["text"]
                lower_header = header_text.lower()

                if "introduction" in lower_header:
                    sections["Introduction"] = True
                if "theorem" in lower_header:
                    sections["Theorems"].append(header_text)
                    stats["features"]["theorems"] = True
                if "proof" in lower_header:
                    sections["Proofs"].append(header_text)
                    stats["features"]["proofs"] = True
                if "example" in lower_header:
                    sections["Examples"].append(header_text)
                    stats["features"]["examples"] = True
                if "exercise" in lower_header:
                    sections["Exercises"].append(header_text)
                    stats["features"]["exercises"] = True

            if "history" in lower_source or "historical" in lower_source:
                stats["features"]["history"] = True
            if "concept" in lower_source:
                stats["features"]["concepts"] = True

        elif cell.cell_type == "code":
            stats["cells"]["code"] += 1
            code_analysis = analyze_code_cell(cell.source)
            stats["content"]["code_lines"] += code_analysis["lines"]
            all_imports.update(code_analysis["imports"])

            if "ipywidgets" in cell.source or "interactive" in cell.source:
                stats["features"]["widgets"] = True

        elif cell.cell_type == "raw":
            stats["cells"]["raw"] += 1

    return {
        "filepath": filepath,
        "metadata": {"kernel": kernelspec, "language": language},
        "stats": stats,
        "outline": all_headers,
        "sections": sections,
        "imports": sorted(list(all_imports)),
    }


def main():
    root_dir = "."
    report = []

    # Collect all notebooks
    notebook_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories
        dirs[:] = [d for d in dirs if not d.startswith(".") and d != "site"]

        for file in files:
            if file.endswith(".ipynb"):
                notebook_files.append(os.path.join(root, file))

    # Sort files to ensure order
    notebook_files.sort()

    print(f"Found {len(notebook_files)} notebooks. Starting audit...")

    for filepath in notebook_files:
        print(f"Auditing {filepath}...")
        audit_data = audit_notebook(filepath)
        if audit_data:
            report.append(audit_data)

    # Write JSON report
    with open("notebook_structure_report.json", "w") as f:
        json.dump(report, f, indent=2)

    # Write Markdown report
    with open("notebook_structure.md", "w") as f:
        f.write("# Notebook Audit Report\n\n")
        f.write(f"Total Notebooks: {len(report)}\n\n")

        for item in report:
            f.write(f"## {item['filepath']}\n")

            # Metadata & Stats Summary
            f.write("### Overview\n")
            f.write(f"- **Kernel**: {item['metadata']['kernel']}\n")
            f.write(
                f"- **Cells**: {item['stats']['cells']['code']} Code, {item['stats']['cells']['markdown']} Markdown\n"
            )
            f.write(
                f"- **Content**: {item['stats']['content']['words']} words, {item['stats']['content']['code_lines']} lines of code\n"
            )
            f.write(
                f"- **Richness**: {item['stats']['content']['equations']} equations, {item['stats']['content']['images']} images, {item['stats']['content']['links']} links\n"
            )

            # Features
            f.write("\n### Features\n")
            feat = item["stats"]["features"]
            features_list = []
            if feat["widgets"]:
                features_list.append("Widgets")
            if feat["theorems"]:
                features_list.append("Theorems")
            if feat["proofs"]:
                features_list.append("Proofs")
            if feat["examples"]:
                features_list.append("Examples")
            if feat["exercises"]:
                features_list.append("Exercises")
            if feat["history"]:
                features_list.append("History")
            if feat["concepts"]:
                features_list.append("Concepts")

            if features_list:
                f.write(", ".join(features_list) + "\n")
            else:
                f.write("None detected\n")

            # Imports
            if item["imports"]:
                f.write(f"\n**Libraries**: {', '.join(item['imports'])}\n")

            # TODOs
            if item["stats"]["content"]["todos"] > 0:
                f.write(f"\n**TODOs**: {item['stats']['content']['todos']}\n")

            # Outline with indentation
            if item["outline"]:
                f.write("\n### Outline\n")
                for header in item["outline"]:
                    level = header["level"]
                    text = header["text"]
                    # Indent based on level.
                    # Level 1 headings (#) are top level.
                    # Indent 2 spaces per level beyond 1.
                    indent = "  " * (level - 1)
                    f.write(f"{indent}- {text}\n")

            f.write("\n---\n")


if __name__ == "__main__":
    main()
