#!/usr/bin/env python3
"""Audit image provenance without treating unknown origin as permission to publish."""

from __future__ import annotations

import argparse

try:
    from scripts.image_provenance import (
        iter_assets,
        metadata,
        provenance_for,
        source_references,
    )
except ImportError:
    from image_provenance import (
        ROOT,
        iter_assets,
        metadata,
        provenance_for,
        source_references,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    assets = set(iter_assets())
    entries = metadata()
    refs = source_references()

    blocking: list[str] = []
    warnings: list[str] = []

    for path in sorted(entries):
        if path not in assets:
            blocking.append(f"metadata points to missing asset: {path}")

    for asset in sorted(assets):
        p = provenance_for(asset)
        if p.status == "verified-generated":
            if not p.license:
                blocking.append(f"generated asset missing license: {asset}")
        elif p.status == "verified-external":
            entry = entries.get(asset, {})
            required = ("source_url", "creator", "license", "attribution", "retrieved_at")
            missing = [key for key in required if not str(entry.get(key, "")).strip()]
            if missing:
                blocking.append(
                    f"verified external asset has incomplete provenance: {asset} ({', '.join(missing)})"
                )
        elif p.status == "unverified":
            if asset in refs:
                warnings.append(
                    f"referenced asset is publication-blocked until provenance is verified: {asset}"
                )
        else:
            blocking.append(f"unknown provenance status {p.status!r}: {asset}")

    print(
        f"Image provenance: {len(assets)} assets; "
        f"{sum(provenance_for(a).publishable for a in assets)} publishable; "
        f"{sum(provenance_for(a).status == 'unverified' for a in assets)} unverified."
    )
    if warnings:
        print(f"Publication-blocked referenced assets: {len(warnings)}")
        for item in warnings[:50]:
            print(f"WARNING: {item}")
    if blocking:
        print(f"Blocking provenance-schema findings: {len(blocking)}")
        for item in blocking:
            print(f"ERROR: {item}")

    return 1 if args.strict and blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
