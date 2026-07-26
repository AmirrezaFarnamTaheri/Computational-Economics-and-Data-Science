"""
Tests for `scripts/macro_utils.py` (`solve_qz`, Klein 2000).

For a saddle system x_{t+1} = M x_t with x = [k; u], the unique
non-explosive solution is fully determined by the stable eigenvectors of M:
stacking the stable eigenvectors as W = [W_k; W_u] (partitioned by
states/controls), the policy is u = W_u @ inv(W_k) @ k and the transition is
k' = W_k @ Lambda_s @ inv(W_k) @ k. Constructing M from chosen eigenvalues
and eigenvectors therefore gives exact closed-form benchmarks.

This suite exists because a subtle QZ-convention error (assuming y = Z x
instead of y = Z.T x) produces answers that are correct for scalar
state/control blocks but wrong — including sign flips — for any
multi-dimensional system. The multi-dimensional benchmark below guards
against that class of bug.
"""

import numpy as np
import pytest

from macro_utils import solve_qz


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def saddle_system(eigenvalues, eigenvectors):
    """Build M = V diag(lambda) V^-1 with prescribed eigen-structure."""
    V = np.asarray(eigenvectors, dtype=float)
    M = V @ np.diag(eigenvalues) @ np.linalg.inv(V)
    return M


def equilibrium_residual(AA, BB, policy, transition, k0):
    """Max residual of AA x' = BB x along the computed solution path."""
    x0 = np.concatenate([k0, policy @ k0])
    k1 = transition @ k0
    x1 = np.concatenate([k1, policy @ k1])
    return np.max(np.abs(AA @ x1 - BB @ x0))


# ---------------------------------------------------------------------------
# Closed-form benchmarks
# ---------------------------------------------------------------------------

class TestClosedForm:

    def test_scalar_saddle_path(self):
        """1 state, 1 control; stable eigvec [1, 0.4] => u = 0.4 k, k' = 0.5 k."""
        V = np.array([[1.0, 1.0],
                      [0.4, 1.5]])
        M = saddle_system([0.5, 2.0], V)
        result = solve_qz(np.eye(2), M, n_states=1)
        assert result['Policy'][0, 0] == pytest.approx(0.4, rel=1e-10)
        assert result['Transition'][0, 0] == pytest.approx(0.5, rel=1e-10)

    def test_scalar_saddle_path_negative_policy(self):
        """Sign of the policy must follow the stable eigenvector exactly."""
        V = np.array([[1.0, 0.3],
                      [-0.7, 1.2]])
        M = saddle_system([0.8, 1.6], V)
        result = solve_qz(np.eye(2), M, n_states=1)
        assert result['Policy'][0, 0] == pytest.approx(-0.7, rel=1e-10)
        assert result['Transition'][0, 0] == pytest.approx(0.8, rel=1e-10)

    def test_multidimensional_saddle_path(self):
        """2 states, 2 controls: Policy = W_u inv(W_k), Transition = W_k L inv(W_k).

        This is the regression test for the y = Z x vs y = Z.T x convention
        bug: scalar systems mask it, multi-dimensional ones do not."""
        rng = np.random.default_rng(42)
        eigenvalues = [0.5, 0.8, 1.5, 3.0]
        V = rng.normal(size=(4, 4))
        while abs(np.linalg.det(V)) < 0.5:
            V = rng.normal(size=(4, 4))
        M = saddle_system(eigenvalues, V)

        W = V[:, :2]           # stable eigenvectors
        W_k, W_u = W[:2], W[2:]
        policy_expected = W_u @ np.linalg.inv(W_k)
        transition_expected = W_k @ np.diag(eigenvalues[:2]) @ np.linalg.inv(W_k)

        result = solve_qz(np.eye(4), M, n_states=2)
        np.testing.assert_allclose(result['Policy'], policy_expected, atol=1e-10)
        np.testing.assert_allclose(result['Transition'], transition_expected,
                                   atol=1e-10)

    def test_pure_backward_looking_system(self):
        """All variables predetermined and stable: transition must equal BB."""
        BB = np.array([[0.9, 0.1],
                       [0.0, 0.5]])
        result = solve_qz(np.eye(2), BB, n_states=2)
        np.testing.assert_allclose(result['Transition'], BB, atol=1e-12)

    def test_nontrivial_AA_matrix(self):
        """AA != I: solve AA x' = BB x by reduction to x' = inv(AA) BB x."""
        rng = np.random.default_rng(3)
        AA = np.eye(3) + 0.1 * rng.normal(size=(3, 3))
        V = rng.normal(size=(3, 3))
        while abs(np.linalg.det(V)) < 0.3:
            V = rng.normal(size=(3, 3))
        M = saddle_system([0.6, 0.9, 1.8], V)   # 2 stable, 1 unstable
        BB = AA @ M                              # so that AA x' = BB x <=> x' = M x

        W = V[:, :2]
        W_k, W_u = W[:2], W[2:]
        policy_expected = W_u @ np.linalg.inv(W_k)

        result = solve_qz(AA, BB, n_states=2)
        np.testing.assert_allclose(result['Policy'], policy_expected, atol=1e-9)


# ---------------------------------------------------------------------------
# Solution properties
# ---------------------------------------------------------------------------

class TestSolutionProperties:

    @pytest.mark.parametrize("seed", [0, 1, 2, 3])
    def test_solution_satisfies_equilibrium_conditions(self, seed):
        """AA x_{t+1} = BB x_t must hold exactly along the solved path."""
        rng = np.random.default_rng(seed)
        eigenvalues = [0.4, 0.7, 1.3, 2.5]
        V = rng.normal(size=(4, 4))
        while abs(np.linalg.det(V)) < 0.3:
            V = rng.normal(size=(4, 4))
        M = saddle_system(eigenvalues, V)

        result = solve_qz(np.eye(4), M, n_states=2)
        k0 = rng.normal(size=2)
        residual = equilibrium_residual(np.eye(4), M, result['Policy'],
                                        result['Transition'], k0)
        assert residual < 1e-9

    def test_transition_is_stable(self):
        """All eigenvalues of the transition matrix must lie inside the
        unit circle when Blanchard-Kahn holds."""
        rng = np.random.default_rng(5)
        V = rng.normal(size=(4, 4))
        while abs(np.linalg.det(V)) < 0.3:
            V = rng.normal(size=(4, 4))
        M = saddle_system([0.5, 0.95, 1.2, 4.0], V)
        result = solve_qz(np.eye(4), M, n_states=2)
        transition_eigenvalues = np.linalg.eigvals(result['Transition'])
        assert np.all(np.abs(transition_eigenvalues) < 1.0)
        # The transition's spectrum must be exactly the stable roots
        np.testing.assert_allclose(sorted(np.abs(transition_eigenvalues)),
                                   [0.5, 0.95], atol=1e-9)


# ---------------------------------------------------------------------------
# Blanchard-Kahn diagnostics
# ---------------------------------------------------------------------------

class TestBlanchardKahn:

    def test_warns_when_explosive(self):
        """0 stable roots but 1 state expected: no stable solution exists."""
        V = np.array([[1.0, 1.0],
                      [0.4, 1.5]])
        M = saddle_system([1.5, 2.0], V)
        with pytest.warns(UserWarning, match="Blanchard-Kahn"):
            solve_qz(np.eye(2), M, n_states=1)

    def test_warns_when_indeterminate(self):
        """2 stable roots but 1 state expected: multiple stable solutions."""
        V = np.array([[1.0, 1.0],
                      [0.4, 1.5]])
        M = saddle_system([0.5, 0.8], V)
        with pytest.warns(UserWarning, match="Blanchard-Kahn"):
            solve_qz(np.eye(2), M, n_states=1)

    def test_no_warning_when_saddle_path_stable(self):
        V = np.array([[1.0, 1.0],
                      [0.4, 1.5]])
        M = saddle_system([0.5, 2.0], V)
        with warnings_disabled_as_errors():
            solve_qz(np.eye(2), M, n_states=1)

    @pytest.mark.parametrize("scale", [1e-12, 1e-6, 1e6])
    def test_classification_invariant_to_pencil_rescaling(self, scale):
        """(c*AA, c*BB) is the same model: root classification and the
        solution must not depend on the common scale of the pencil."""
        V = np.array([[1.0, 1.0],
                      [0.4, 1.5]])
        M = saddle_system([0.5, 2.0], V)
        baseline = solve_qz(np.eye(2), M, n_states=1)
        with warnings_disabled_as_errors():
            scaled = solve_qz(scale * np.eye(2), scale * M, n_states=1)
        np.testing.assert_allclose(scaled['Policy'], baseline['Policy'],
                                   rtol=1e-9)
        np.testing.assert_allclose(scaled['Transition'], baseline['Transition'],
                                   rtol=1e-9)


class warnings_disabled_as_errors:
    """Context manager: escalate any warning to a test failure."""

    def __enter__(self):
        import warnings
        self._ctx = warnings.catch_warnings()
        self._ctx.__enter__()
        warnings.simplefilter("error")
        return self

    def __exit__(self, *exc):
        return self._ctx.__exit__(*exc)
