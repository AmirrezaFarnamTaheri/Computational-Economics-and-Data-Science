#!/usr/bin/env python3
"""Validate the mathematical-review evidence ledger.

The ledger prevents structural proof scans and numerical regression tests from
being mislabeled as independent mathematical review.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "ci" / "mathematical_claims.json"

REVIEW_STATUSES = {
    "not-claimed",
    "independent-signoff-required",
    "reviewed",
}
NUMERICAL_STATUSES = {
    "not-applicable",
    "not-validated",
    "validated",
}
RELEASE_LABELS = {
    "structure-complete",
    "mathematically-reviewed",
    "numerically-validated",
}


def load_ledger() -> dict:
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def source_cell_exists(source: Path, cell_id: str) -> bool:
    notebook = json.loads(source.read_text(encoding="utf-8"))
    return any(cell.get("id") == cell_id for cell in notebook.get("cells", []))


def validate_claim(claim: dict) -> list[str]:
    errors: list[str] = []
    claim_id = claim.get("id", "<missing-id>")
    prefix = f"{claim_id}: "

    source_text = claim.get("source")
    if not source_text:
        errors.append(prefix + "missing source")
        return errors

    source = ROOT / source_text
    if not source.is_file():
        errors.append(prefix + f"source does not exist: {source_text}")
    elif claim.get("source_cell"):
        if source.suffix != ".ipynb":
            errors.append(prefix + "source_cell is only valid for notebooks")
        elif not source_cell_exists(source, str(claim["source_cell"])):
            errors.append(
                prefix
                + f"source cell {claim['source_cell']!r} is absent from {source_text}"
            )

    if not isinstance(claim.get("structure_complete"), bool):
        errors.append(prefix + "structure_complete must be boolean")

    review = claim.get("mathematical_review") or {}
    review_status = review.get("status")
    if review_status not in REVIEW_STATUSES:
        errors.append(prefix + f"invalid mathematical_review status: {review_status}")
    if review_status == "reviewed":
        if not review.get("reviewer") or not review.get("evidence"):
            errors.append(
                prefix
                + "reviewed status requires both reviewer identity and review evidence"
            )

    numerical = claim.get("numerical_validation") or {}
    numerical_status = numerical.get("status")
    if numerical_status not in NUMERICAL_STATUSES:
        errors.append(prefix + f"invalid numerical_validation status: {numerical_status}")
    if numerical_status == "validated":
        evidence = numerical.get("evidence")
        selector = numerical.get("selector")
        if not evidence or not (ROOT / evidence).is_file():
            errors.append(prefix + f"numerical evidence does not exist: {evidence}")
        if not selector:
            errors.append(prefix + "validated numerical claim requires a test selector")

    labels = claim.get("release_labels")
    if not isinstance(labels, list) or not labels:
        errors.append(prefix + "release_labels must be a non-empty list")
        labels = []
    unknown = sorted(set(labels) - RELEASE_LABELS)
    if unknown:
        errors.append(prefix + f"unknown release labels: {unknown}")

    if "mathematically-reviewed" in labels and review_status != "reviewed":
        errors.append(
            prefix
            + "mathematically-reviewed label requires independent review status=reviewed"
        )
    if "numerically-validated" in labels and numerical_status != "validated":
        errors.append(
            prefix + "numerically-validated label requires numerical status=validated"
        )
    if "structure-complete" in labels and claim.get("structure_complete") is not True:
        errors.append(
            prefix + "structure-complete label requires structure_complete=true"
        )

    return errors


def main() -> int:
    ledger = load_ledger()
    policy = ledger.get("policy_document")
    errors: list[str] = []
    if ledger.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if not policy or not (ROOT / policy).is_file():
        errors.append(f"policy document does not exist: {policy}")

    claims = ledger.get("claims")
    if not isinstance(claims, list) or not claims:
        errors.append("claims must be a non-empty list")
        claims = []

    ids = [claim.get("id") for claim in claims]
    if None in ids or len(ids) != len(set(ids)):
        errors.append("claim ids must be present and unique")

    for claim in claims:
        errors.extend(validate_claim(claim))

    reviewed = sum(
        (claim.get("mathematical_review") or {}).get("status") == "reviewed"
        for claim in claims
    )
    numerically_validated = sum(
        (claim.get("numerical_validation") or {}).get("status") == "validated"
        for claim in claims
    )
    print(
        f"Mathematical claim ledger: {len(claims)} claims; "
        f"{reviewed} independently reviewed; "
        f"{numerically_validated} numerically validated."
    )
    if errors:
        print("Ledger errors:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(
        "Evidence labels are internally consistent. "
        "No independent mathematical review is inferred from CI."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
