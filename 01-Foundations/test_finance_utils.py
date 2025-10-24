"""
Comprehensive test suite for finance_utils module.

Tests present value calculations with various inputs including
edge cases, boundary conditions, and error handling.
"""

import pytest
import numpy as np
from finance_utils import calculate_pv


class TestCalculatePV:
    """Test suite for the calculate_pv function."""

    def test_standard_case(self):
        """Tests the PV calculation for a standard case."""
        assert calculate_pv(fv=110, r=0.1, n=2) == pytest.approx(90.90909, rel=1e-4)

    def test_zero_periods(self):
        """Test with n=0 (no time period) - should return fv."""
        assert calculate_pv(fv=100, r=0.1, n=0) == pytest.approx(100.0)

    def test_zero_rate(self):
        """Test with r=0 (no discount) - should return fv."""
        assert calculate_pv(fv=100, r=0.0, n=5) == pytest.approx(100.0)

    def test_one_period(self):
        """Test with n=1 (single period discounting)."""
        assert calculate_pv(fv=110, r=0.1, n=1) == pytest.approx(100.0)

    def test_high_interest_rate(self):
        """Test with high interest rate."""
        # At 100% interest rate, PV should be fv / 2^n
        assert calculate_pv(fv=100, r=1.0, n=2) == pytest.approx(25.0)

    def test_low_interest_rate(self):
        """Test with very low interest rate."""
        # At 1% interest rate
        assert calculate_pv(fv=100, r=0.01, n=1) == pytest.approx(99.00990099)

    def test_negative_future_value(self):
        """Test with negative future value (e.g., future payment)."""
        # PV of a future payment should also be negative
        assert calculate_pv(fv=-100, r=0.1, n=1) == pytest.approx(-90.90909, rel=1e-4)

    def test_large_n(self):
        """Test with large number of periods."""
        # After 100 periods at 10% discount, PV should be very small
        pv = calculate_pv(fv=1000, r=0.1, n=100)
        assert pv < 0.01  # Should be close to zero
        assert pv > 0     # But positive

    def test_small_n(self):
        """Test with fractional periods."""
        # 0.5 periods (half year)
        assert calculate_pv(fv=100, r=0.1, n=0.5) == pytest.approx(95.346, rel=1e-3)

    def test_negative_rate(self):
        """Test with negative interest rate (e.g., storage costs)."""
        # With negative rates, PV > FV
        pv = calculate_pv(fv=100, r=-0.05, n=1)
        assert pv > 100
        assert pv == pytest.approx(105.2631, rel=1e-3)

    def test_numerical_precision(self):
        """Test numerical precision with very small discount rates."""
        # Test that function handles small rates correctly
        pv = calculate_pv(fv=1000, r=0.0001, n=10)
        expected = 1000 / (1.0001 ** 10)
        assert pv == pytest.approx(expected, rel=1e-10)

    def test_multiple_values(self):
        """Test with multiple different parameter combinations."""
        test_cases = [
            (100, 0.05, 1, 95.238),
            (1000, 0.08, 5, 680.583),
            (500, 0.12, 3, 355.889),
            (250, 0.15, 2, 189.036),
        ]
        for fv, r, n, expected_pv in test_cases:
            assert calculate_pv(fv, r, n) == pytest.approx(expected_pv, rel=1e-3)

    def test_array_inputs(self):
        """Test with numpy array inputs (if function supports vectorization)."""
        # Note: Current implementation may not support arrays
        # This test documents expected behavior for future enhancement
        try:
            fv_array = np.array([100, 200, 300])
            r = 0.1
            n = 1
            result = calculate_pv(fv_array, r, n)
            expected = np.array([90.90909, 181.81818, 272.72727])
            np.testing.assert_array_almost_equal(result, expected, decimal=4)
        except TypeError:
            # If function doesn't support arrays, that's okay
            pytest.skip("Function doesn't support array inputs yet")

    def test_consistency_with_financial_formulas(self):
        """Test consistency with known financial calculations."""
        # Present value of $1000 in 5 years at 8% should be $680.58
        assert calculate_pv(1000, 0.08, 5) == pytest.approx(680.583, rel=1e-3)

        # Present value of $10,000 in 10 years at 5% should be $6139.13
        assert calculate_pv(10000, 0.05, 10) == pytest.approx(6139.13, rel=1e-4)

    @pytest.mark.parametrize("fv,r,n,expected", [
        (100, 0.1, 1, 90.90909),
        (1000, 0.05, 2, 907.029),
        (500, 0.08, 3, 396.918),
        (250, 0.12, 4, 158.935),
        (750, 0.06, 5, 560.395),
    ])
    def test_parametrized_cases(self, fv, r, n, expected):
        """Parametrized test cases for various PV calculations."""
        assert calculate_pv(fv, r, n) == pytest.approx(expected, rel=1e-3)


class TestEdgeCases:
    """Test edge cases and potential error conditions."""

    def test_very_large_fv(self):
        """Test with very large future value."""
        fv = 1e15  # 1 quadrillion
        pv = calculate_pv(fv, 0.05, 10)
        assert pv > 0
        assert pv < fv

    def test_very_small_fv(self):
        """Test with very small future value."""
        fv = 0.01
        pv = calculate_pv(fv, 0.05, 1)
        assert pv == pytest.approx(0.00952, rel=1e-4)

    def test_extreme_rate(self):
        """Test with very high interest rate."""
        # At 1000% interest rate
        pv = calculate_pv(100, 10.0, 2)
        assert pv == pytest.approx(0.826, rel=1e-2)

    def test_many_periods(self):
        """Test with very many periods."""
        # 1000 periods should make PV very small
        pv = calculate_pv(1000, 0.05, 1000)
        assert pv < 1e-10  # Should be essentially zero


class TestReturnTypes:
    """Test that function returns expected types."""

    def test_returns_float(self):
        """Test that function returns a float."""
        result = calculate_pv(100, 0.1, 1)
        assert isinstance(result, (float, np.floating, int, np.integer))

    def test_returns_finite(self):
        """Test that result is finite (not inf or nan)."""
        result = calculate_pv(100, 0.1, 1)
        assert np.isfinite(result)


# Additional integration tests
def test_compound_discounting():
    """Test that the function correctly applies compound discounting."""
    # Manually calculate compound discounting
    fv = 100
    r = 0.1
    n = 3

    # Manual calculation
    expected = fv / ((1 + r) * (1 + r) * (1 + r))

    # Function calculation
    result = calculate_pv(fv, r, n)

    assert result == pytest.approx(expected, rel=1e-10)


def test_inverse_relationship():
    """Test inverse relationship between PV and periods."""
    # As n increases, PV should decrease (for positive r)
    fv = 100
    r = 0.1

    pv_1 = calculate_pv(fv, r, 1)
    pv_2 = calculate_pv(fv, r, 2)
    pv_3 = calculate_pv(fv, r, 3)

    assert pv_1 > pv_2 > pv_3


if __name__ == "__main__":
    # Run tests with verbose output
    pytest.main([__file__, "-v", "--tb=short"])
