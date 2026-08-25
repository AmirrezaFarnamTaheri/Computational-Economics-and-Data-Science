"""WP-15: stub-function inventory guard (K-02 triage).

Every function whose body is a bare ``...`` / ``pass`` /
``raise NotImplementedError`` anywhere in the curriculum's notebooks is
classified exactly once, here. A new stub fails this test until it is added
to the inventory with a triage decision (LEGIT interface declaration vs FIX).

Current inventory (all LEGIT - interface declarations in the OOP lecture's
ABC-vs-Protocol lesson, each implemented concretely in the same notebook and
exercised by tests/test_notebook_solution_functions.py):

- 11_Object_Oriented_Programming.ipynb cell 15:
    AbstractValuationModel.calculate_npv   (ABC abstractmethod)
    ValuationProtocol.calculate_npv        (Protocol interface)
- 11_Object_Oriented_Programming.ipynb cell 17:
    ProductionFunction.produce             (Protocol interface)
    UtilityFunction.calculate_utility      (Protocol interface)
"""

from __future__ import annotations

import ast
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# (notebook, cell, qualified name) -> triage decision
INVENTORY = {
    (
        "01-Foundations/11_Object_Oriented_Programming.ipynb",
        15,
        "AbstractValuationModel.calculate_npv",
    ): "LEGIT",
    (
        "01-Foundations/11_Object_Oriented_Programming.ipynb",
        15,
        "ValuationProtocol.calculate_npv",
    ): "LEGIT",
    (
        "01-Foundations/11_Object_Oriented_Programming.ipynb",
        17,
        "ProductionFunction.produce",
    ): "LEGIT",
    (
        "01-Foundations/11_Object_Oriented_Programming.ipynb",
        17,
        "UtilityFunction.calculate_utility",
    ): "LEGIT",
}


def stub_kind(fn: ast.FunctionDef) -> str | None:
    if len(fn.body) != 1:
        return None
    node = fn.body[0]
    if isinstance(node, ast.Pass):
        return "pass"
    if (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and node.value.value is ...
    ):
        return "ellipsis"
    if isinstance(node, ast.Raise) and "NotImplementedError" in ast.dump(node):
        return "not-implemented"
    if (
        isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Constant)
        and isinstance(node.value.value, str)
    ):
        return "docstring-only"
    return None


def notebook_stubs() -> dict:
    """{(notebook, cell, qualified name): kind} for every stub in the repo."""
    found: dict = {}
    files = sorted(
        set(
            list(ROOT.glob("*/*.ipynb"))
            + list(ROOT.glob("Appendix/*.ipynb"))
            + list(ROOT.glob("high_performance_python/*.ipynb"))
        )
    )
    for f in files:
        rel = f.relative_to(ROOT).as_posix()
        nb = json.loads(f.read_text(encoding="utf-8"))
        for i, cell in enumerate(nb["cells"]):
            if cell.get("cell_type") != "code":
                continue
            src = cell["source"]
            src = "".join(src) if isinstance(src, list) else src
            try:
                tree = ast.parse(src)
            except SyntaxError:
                continue
            # structured traversal: top-level functions and class methods
            # (one level deep - the curriculum has no deeper nesting)
            for node in tree.body:
                if isinstance(node, ast.ClassDef):
                    for sub in node.body:
                        if isinstance(sub, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            kind = stub_kind(sub)
                            if kind:
                                found[(rel, i, f"{node.name}.{sub.name}")] = kind
                elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    kind = stub_kind(node)
                    if kind:
                        found[(rel, i, node.name)] = kind
    return found


def test_stub_inventory_matches_triage():
    found = notebook_stubs()
    found_keys = set(found)
    inventory_keys = set(INVENTORY)
    unclassified = found_keys - inventory_keys
    stale = inventory_keys - found_keys
    assert not unclassified, (
        "New untriaged stub(s) found - add them to the INVENTORY in "
        f"tests/test_stub_inventory.py with a LEGIT/FIX decision: {sorted(unclassified)}"
    )
    assert not stale, (
        "Inventory entries no longer exist (stubs were implemented or "
        f"removed) - update the INVENTORY: {sorted(stale)}"
    )


def test_all_inventory_entries_are_triaged():
    decisions = set(INVENTORY.values())
    assert decisions <= {"LEGIT", "FIX"}, f"unknown triage decisions: {decisions}"
    fix_entries = [k for k, v in INVENTORY.items() if v == "FIX"]
    assert not fix_entries, f"FIX-decision stubs remain unimplemented: {fix_entries}"
