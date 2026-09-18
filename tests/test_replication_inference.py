"""Regression coverage for the two replication-notebook defects found in the
PR #58 review round:

1. The Card-Krueger extract has one row per restaurant-wave and no restaurant
   id, so HC1 treated 820 observations as independent. The notebook now
   reconstructs the panel pairing by row order within wave, *validates* it
   against the extract's own ``demp`` (change in employment) column, and
   clusters by restaurant. This test asserts the validation identity holds so
   the clustering can never silently pair the wrong stores.

2. The controlled specification's dummy sets are perfectly collinear with the
   intercept (bk+kfc+roys+wendys == 1 and nj+pa1+pa2 == 1 for every row),
   which made the design matrix singular. This test asserts the restricted
   formula is full rank.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = ROOT / "Appendix" / "T4_Replication_Card_Krueger_1994.ipynb"
DATA = ROOT / "data" / "replications" / "card_krueger_1994_njmin3.csv"


@pytest.fixture(scope="module")
def panel():
    import pandas as pd

    df = pd.read_csv(DATA)
    df = df.sort_values(["d"], kind="stable").reset_index(drop=True)
    df["restaurant"] = df.groupby("d").cumcount()
    return df


def test_extract_rows_pair_by_row_order(panel):
    """demp (recorded change) == post - pre for every complete pair.

    This is the identity that makes the reconstructed restaurant id
    trustworthy. If the extract's row order ever changes so the waves are no
    longer aligned, clustering by the id would pair unrelated stores and this
    test fails instead of silently mis-reporting uncertainty.
    """
    waves = {w: part.reset_index(drop=True) for w, part in panel.groupby("d")}
    pre, post = waves[0], waves[1]
    both = ~(pre["fte"].isna() | post["fte"].isna())
    assert both.sum() > 300, "expected ~384 complete restaurant pairs"
    implied = post.loc[both, "fte"] - pre.loc[both, "fte"]
    assert np.allclose(implied.values, post.loc[both, "demp"].values)


def test_each_restaurant_appears_at_most_twice(panel):
    """The panel is two waves; no id may collect more than two observations."""
    counts = panel.groupby("restaurant")["d"].nunique()
    assert counts.max() <= 2
    assert panel["restaurant"].nunique() == 410


def test_controlled_design_matrix_is_full_rank(panel):
    """The restricted dummy formula must not be singular.

    The unrestricted specification included all four chain dummies and all
    three state/region dummies alongside an intercept; each set sums to 1, so
    the design matrix was rank-deficient and the clustered covariance was
    garbage (SE ~1e5) rather than merely imprecise.
    """
    cols = [
        "fte",
        "nj",
        "d",
        "d_nj",
        "kfc",
        "roys",
        "wendys",
        "co_owned",
        "centralj",
        "southj",
        "pa1",
    ]
    design = panel[cols].dropna()
    m = np.column_stack([np.ones(len(design)), design[cols].values])
    assert np.linalg.matrix_rank(m) == m.shape[1], (
        "controlled specification is rank-deficient; a dummy set is "
        "collinear with the intercept"
    )


def test_notebook_uses_clustered_inference():
    """The notebook must cluster by restaurant, not use HC1."""
    nb = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    code = "\n".join(
        "".join(c["source"]) for c in nb["cells"] if c.get("cell_type") == "code"
    )
    assert 'cov_type="cluster"' in code
    assert "restaurant" in code
    # The validation guard must be present so a mis-ordered extract fails loudly.
    assert "demp" in code
