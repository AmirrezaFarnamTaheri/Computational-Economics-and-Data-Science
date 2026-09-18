"""Anchor and image fidelity of generated notebook documentation pages."""

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
    """A repository-relative image becomes the raw GitHub URL.

    The fake notebook parent is built from ``generator.ROOT`` rather than a
    hard-coded Windows path: on the Linux CI runner the hard-coded path is not
    under ROOT, ``rewrite_links`` takes its not-inside-repository branch, and
    the input is returned unchanged -- so the assertions still passed while
    testing nothing (the unmodified input already satisfies them).
    """
    track_dir = generator.ROOT / "01-Foundations"
    images_dir = generator.ROOT / "images" / "foo"
    images_dir.mkdir(parents=True, exist_ok=True)
    stub = images_dir / "plot.png"
    stub.write_bytes(b"stub")
    try:

        class FakeNotebook:
            parent = track_dir

        html = generator.rewrite_links("![fig](../images/foo/plot.png)", FakeNotebook())
        expected = f"{generator.RAW}/images/foo/plot.png"
        assert html == f"![fig]({expected})", html
    finally:
        # The stub is test scaffolding, not a committed asset; leaving it in the
        # working tree would show up as an untracked file and could be committed
        # by accident.
        stub.unlink()
        images_dir.rmdir()


def test_repository_file_links_resolve_to_raw_urls():
    """Non-image repository files (LICENSE, README) are rewritten, not copied.

    This is the defect behind the 129 unresolved ``../LICENSE`` links MkDocs
    warned about while audit_docs reported zero findings: a relative file link
    is valid from the notebook but points at a nonexistent path once copied
    into docs/notebooks/<track>/.
    """
    track_dir = generator.ROOT / "01-Foundations"
    nb = track_dir / "link_probe.ipynb"
    nb.write_text("{}", encoding="utf-8")
    try:
        badge = (
            "[![Code License: MIT]"
            "(https://img.shields.io/badge/Code%20License-MIT-yellow.svg)]"
            "(../LICENSE)"
        )
        out = generator.rewrite_links(badge, nb)
        assert f"{generator.RAW}/LICENSE)" in out, out
        # The badge image itself is untouched (external URL).
        assert "img.shields.io/badge/Code%20License-MIT-yellow.svg" in out
    finally:
        nb.unlink()


def test_links_outside_repository_are_left_alone():
    """A link to a nonexistent file is a notebook defect, and must survive
    verbatim so the docs audit can report it rather than being silently
    rewritten to a raw URL that does not exist either.
    """
    track_dir = generator.ROOT / "01-Foundations"
    nb = track_dir / "absent_probe.ipynb"
    nb.write_text("{}", encoding="utf-8")
    try:
        out = generator.rewrite_links("[nope](../does_not_exist.txt)", nb)
        assert out == "[nope](../does_not_exist.txt)", out
    finally:
        nb.unlink()
