"""
Tests for `04-Macro-Models/macro_vfi_utils.py` (Tauchen 1986 discretization).

The discretized chain approximates the AR(1) process

    z' = rho * z + eps,   eps ~ N(0, sigma_e^2)

with unconditional standard deviation sigma_z = sigma_e / sqrt(1 - rho^2).
The suite checks:

1. **Structural invariants** — the transition matrix is row-stochastic and
   the grid spans exactly [-m*sigma_z, +m*sigma_z] symmetrically.
2. **Exact probabilities in the i.i.d. case** — for rho = 0 every row must
   equal the N(0, sigma_e) mass of each grid bin, computable in closed form.
3. **Moment matching** — the chain's conditional means, stationary mean,
   and implied first-order autocorrelation must reproduce the AR(1)
   parameters on a fine grid.
"""

import numpy as np
import pytest
from macro_vfi_utils import tauchen
from scipy.stats import norm


def stationary_distribution(P: np.ndarray) -> np.ndarray:
    """Left Perron eigenvector of a row-stochastic matrix, normalized to 1."""
    eigenvalues, eigenvectors = np.linalg.eig(P.T)
    idx = np.argmin(np.abs(eigenvalues - 1.0))
    pi = np.real(eigenvectors[:, idx])
    return pi / pi.sum()


# ---------------------------------------------------------------------------
# Structural invariants
# ---------------------------------------------------------------------------


class TestStructure:

    @pytest.mark.parametrize(
        "rho,sigma_e,n,m",
        [
            (0.0, 1.0, 5, 3),
            (0.5, 0.1, 7, 3),
            (0.9, 0.02, 11, 3),
            (0.95, 0.007, 21, 2.5),
        ],
    )
    def test_rows_sum_to_one(self, rho, sigma_e, n, m):
        _, P = tauchen(rho, sigma_e, n_states=n, m=m)
        np.testing.assert_allclose(P.sum(axis=1), np.ones(n), atol=1e-12)

    def test_probabilities_are_valid(self):
        _, P = tauchen(0.9, 0.02, n_states=9)
        assert np.all(P >= 0.0)
        assert np.all(P <= 1.0)

    def test_grid_is_symmetric_with_correct_bounds(self):
        rho, sigma_e, m, n = 0.8, 0.1, 3, 7
        z_grid, _ = tauchen(rho, sigma_e, n_states=n, m=m)
        sigma_z = sigma_e / np.sqrt(1 - rho**2)
        assert z_grid[0] == pytest.approx(-m * sigma_z, rel=1e-12)
        assert z_grid[-1] == pytest.approx(m * sigma_z, rel=1e-12)
        # Symmetry: grid is its own negation reversed
        np.testing.assert_allclose(z_grid, -z_grid[::-1], atol=1e-12)
        # Uniform spacing
        np.testing.assert_allclose(
            np.diff(z_grid), np.full(n - 1, z_grid[1] - z_grid[0]), atol=1e-12
        )

    def test_output_shapes(self):
        z_grid, P = tauchen(0.9, 0.02, n_states=13)
        assert z_grid.shape == (13,)
        assert P.shape == (13, 13)

    def test_deterministic(self):
        z1, P1 = tauchen(0.9, 0.02, n_states=9)
        z2, P2 = tauchen(0.9, 0.02, n_states=9)
        np.testing.assert_array_equal(z1, z2)
        np.testing.assert_array_equal(P1, P2)


# ---------------------------------------------------------------------------
# Exact closed-form check: rho = 0 (i.i.d. case)
# ---------------------------------------------------------------------------


class TestIIDCase:

    def test_rows_identical_when_rho_zero(self):
        """With rho = 0 the next-period draw ignores the current state."""
        _, P = tauchen(0.0, 1.0, n_states=7, m=3)
        for i in range(1, 7):
            np.testing.assert_allclose(P[i], P[0], atol=1e-14)

    def test_rows_match_exact_gaussian_bin_masses(self):
        """Each row must equal the N(0, sigma_e) probability of each bin,
        with the outer bins absorbing the tails (Tauchen's construction)."""
        sigma_e, n, m = 1.0, 7, 3
        z_grid, P = tauchen(0.0, sigma_e, n_states=n, m=m)
        step = z_grid[1] - z_grid[0]

        expected = np.zeros(n)
        expected[0] = norm.cdf((z_grid[0] + step / 2) / sigma_e)
        expected[-1] = 1 - norm.cdf((z_grid[-1] - step / 2) / sigma_e)
        for j in range(1, n - 1):
            expected[j] = norm.cdf((z_grid[j] + step / 2) / sigma_e) - norm.cdf(
                (z_grid[j] - step / 2) / sigma_e
            )

        np.testing.assert_allclose(P[0], expected, atol=1e-14)


# ---------------------------------------------------------------------------
# Moment matching against the underlying AR(1)
# ---------------------------------------------------------------------------


class TestMomentMatching:

    # A fine grid keeps the discretization error well below the tolerances.
    RHO, SIGMA_E, N, M = 0.9, 0.02, 101, 3.5

    @pytest.fixture(scope="class")
    def chain(self):
        z_grid, P = tauchen(self.RHO, self.SIGMA_E, n_states=self.N, m=self.M)
        return z_grid, P, stationary_distribution(P)

    def test_conditional_means_track_rho_z(self, chain):
        """E[z' | z_i] must be close to rho * z_i for interior states."""
        z_grid, P, _ = chain
        conditional_means = P @ z_grid
        interior = slice(self.N // 4, 3 * self.N // 4)
        np.testing.assert_allclose(
            conditional_means[interior], self.RHO * z_grid[interior], atol=1e-4
        )

    def test_stationary_mean_is_zero(self, chain):
        z_grid, _, pi = chain
        assert pi @ z_grid == pytest.approx(0.0, abs=1e-10)

    def test_stationary_variance_matches_ar1(self, chain):
        z_grid, _, pi = chain
        sigma_z2 = self.SIGMA_E**2 / (1 - self.RHO**2)
        variance = pi @ z_grid**2
        assert variance == pytest.approx(sigma_z2, rel=0.02)

    def test_implied_autocorrelation_matches_rho(self, chain):
        """corr(z_t, z_{t+1}) under the stationary law must approximate rho."""
        z_grid, P, pi = chain
        variance = pi @ z_grid**2
        autocovariance = z_grid @ (np.diag(pi) @ P) @ z_grid
        assert autocovariance / variance == pytest.approx(self.RHO, abs=5e-3)

    def test_higher_persistence_concentrates_diagonal_mass(self):
        """More persistent processes must put more mass on staying in place."""
        _, P_low = tauchen(0.3, 0.1, n_states=9)
        _, P_high = tauchen(0.95, 0.1, n_states=9)
        middle = 4
        assert P_high[middle, middle] > P_low[middle, middle]
