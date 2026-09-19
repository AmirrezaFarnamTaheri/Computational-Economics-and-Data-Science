#!/usr/bin/env python3
"""Regenerate the image catalog from repository truth."""

try:
    from scripts.image_provenance import ROOT, catalog_markdown
except ImportError:
    from image_provenance import ROOT, catalog_markdown

TARGET = ROOT / "docs" / "IMAGE_CATALOG.md"


def main() -> int:
    TARGET.write_text(catalog_markdown(), encoding="utf-8", newline="\n")
    print(f"Wrote {TARGET.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
