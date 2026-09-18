"""Anchor and image fidelity of generated notebook documentation pages."""

from pathlib import Path

import scripts.notebooks_to_docs as generator


def test_markdown_heading_slug_matches_mkdocs_toc_permalink():
    """GitHub-style Jupyter anchors are rewritten to MkDocs slugs."""
    text = (
        "## 3.1 Probability Spaces\n\n"
        "Jump to [details](#3.1-Probability-Spaces) or [summary](#Summary)."
    )
    converted = generator.convert_headings_and_anchors(text)
    assert "#31-probability-spaces" in converted
    assert "toc-anchor" not in converted
    # The original Jupyter spelling must not survive anywhere.
    assert "#3.1-Probability-Spaces" not in converted


def test_block_formula_ids_survive_slug_conversion():
    """Manual HTML ids for display equations keep working after conversion."""
    text = '<a id="eq-budget"></a>\n\nSee [the budget equation](#eq-budget).'
    converted = generator.convert_headings_and_anchors(text)
    assert converted.count('id="eq-budget"') == 1
    assert converted.count("#eq-budget") == 1


def test_relative_images_resolve_inside_repository():
    class FakeNotebook:
        parent = Path(
            "D:/GitHub/Computational-Economics-and-Data-Science/01-Foundations"
        )

    html = generator.rewrite_links("![fig](../images/foo/plot.png)", FakeNotebook())
    assert html.startswith("![fig](")
    assert "/images/foo/plot.png)" in html
