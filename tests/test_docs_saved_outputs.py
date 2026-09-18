"""Regression coverage for saved notebook outputs in generated docs."""

import base64
import json

import scripts.notebooks_to_docs as generator


def test_convert_preserves_saved_text_markdown_and_image_outputs():
    notebook = generator.ROOT / "01-Foundations" / "saved_output_probe.ipynb"
    png = base64.b64encode(b"not-a-real-png-but-valid-base64").decode("ascii")
    payload = {
        "cells": [
            {
                "cell_type": "code",
                "id": "probe-cell",
                "metadata": {},
                "execution_count": 1,
                "source": ["print('estimate')\n"],
                "outputs": [
                    {
                        "output_type": "stream",
                        "name": "stdout",
                        "text": ["estimate = 1.25\n"],
                    },
                    {
                        "output_type": "display_data",
                        "metadata": {},
                        "data": {"text/markdown": ["**diagnostic:** passed"]},
                    },
                    {
                        "output_type": "display_data",
                        "metadata": {},
                        "data": {"image/png": png},
                    },
                ],
            }
        ],
        "metadata": {},
        "nbformat": 4,
        "nbformat_minor": 5,
    }
    notebook.write_text(json.dumps(payload), encoding="utf-8")
    try:
        page = generator.convert(notebook)
        assert "estimate = 1.25" in page
        assert "**diagnostic:** passed" in page
        assert f"data:image/png;base64,{png}" in page
        assert 'alt="Saved output from cell probe-cell, result 3"' in page
        assert "outputs are intentionally omitted" not in page
    finally:
        notebook.unlink()


def test_error_output_keeps_diagnostic_without_terminal_escape_codes():
    output = {
        "output_type": "error",
        "ename": "ValueError",
        "evalue": "bad value",
        "traceback": ["\u001b[31mValueError\u001b[0m: bad value"],
    }
    rendered = "\n".join(generator.render_saved_output(output, "cell-a", 0))
    assert "ValueError" in rendered
    assert "bad value" in rendered
    assert "\u001b[" not in rendered
