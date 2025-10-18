import pytest
from finance_utils import calculate_pv


def test_calculate_pv():
    """Tests the PV calculation for a standard case."""
    # Use pytest.approx for floating-point comparisons
    assert calculate_pv(fv=110, r=0.1, n=2) == pytest.approx(90.90909)
