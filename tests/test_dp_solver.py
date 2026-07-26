"""
Tests for `03-Economic-Modeling/dp_solver.py` (the `DiscreteDP` class).

The suite verifies the solver against three kinds of ground truth:

1. **Closed-form solutions** — models small enough that the value function
   can be computed by hand (geometric series, 2x2 linear systems).
2. **Mathematical properties** — the Bellman operator must be a
   beta-contraction in the sup norm and monotone; the converged value
   function must be a fixed point.
3. **Cross-method agreement** — VFI and PFI must converge to the same value
   function and policy on randomly generated MDPs.
"""

import numpy as np
import pytest

from dp_solver import DiscreteDP


# ---------------------------------------------------------------------------
# Helpers: constructed MDPs with known solutions
# ---------------------------------------------------------------------------

def single_state_dp(reward: float = 1.0, beta: float = 0.95) -> DiscreteDP:
    """One state, one action. V* = reward / (1 - beta) exactly."""
    R = np.array([[reward]])
    Q = np.array([[[1.0]]])
    return DiscreteDP(R, Q, beta)


def two_state_dp(beta: float = 0.9) -> tuple:
    """
    Two states, two actions, deterministic transitions.

    Action 0 = "stay", action 1 = "switch" (move to the other state).
        R[0] = [stay: 0, switch: -0.5]   (state 0 is the bad state)
        R[1] = [stay: 1, switch: -0.5]   (state 1 is the good state)

    Optimal policy: switch out of state 0, stay in state 1.
    Solving the Bellman system by hand for that policy:
        V(1) = 1 + beta * V(1)          =>  V(1) = 1 / (1 - beta)
        V(0) = -0.5 + beta * V(1)       =>  V(0) = -0.5 + beta / (1 - beta)
    """
    R = np.array([
        [0.0, -0.5],
        [1.0, -0.5],
    ])
    stay = np.eye(2)
    switch = np.array([[0.0, 1.0], [1.0, 0.0]])
    # Q[s, a, s'] : stack the transition rows per action
    Q = np.stack([stay, switch], axis=1)
    V1 = 1.0 / (1.0 - beta)
    V0 = -0.5 + beta * V1
    V_expected = np.array([V0, V1])
    policy_expected = np.array([1, 0])
    return DiscreteDP(R, Q, beta), V_expected, policy_expected


def random_dp(rng: np.random.Generator, n_states: int = 8, n_actions: int = 4,
              beta: float = 0.92) -> DiscreteDP:
    """A random MDP with valid (row-stochastic) transition kernels."""
    R = rng.normal(size=(n_states, n_actions))
    Q = rng.random((n_states, n_actions, n_states))
    Q = Q / Q.sum(axis=2, keepdims=True)
    return DiscreteDP(R, Q, beta)


# ---------------------------------------------------------------------------
# Input validation
# ---------------------------------------------------------------------------

class TestValidation:

    def test_rejects_beta_of_one(self):
        with pytest.raises(ValueError, match="beta"):
            DiscreteDP(np.ones((2, 2)), np.full((2, 2, 2), 0.5), beta=1.0)

    def test_rejects_beta_of_zero(self):
        with pytest.raises(ValueError, match="beta"):
            DiscreteDP(np.ones((2, 2)), np.full((2, 2, 2), 0.5), beta=0.0)

    def test_rejects_negative_beta(self):
        with pytest.raises(ValueError, match="beta"):
            DiscreteDP(np.ones((2, 2)), np.full((2, 2, 2), 0.5), beta=-0.5)

    def test_rejects_incompatible_q_shape(self):
        R = np.ones((3, 2))
        Q_bad = np.full((2, 2, 2), 0.5)  # should be (3, 2, 3)
        with pytest.raises(ValueError, match="shape of Q"):
            DiscreteDP(R, Q_bad, beta=0.9)

    def test_dimensions_inferred_from_reward_array(self):
        dp = random_dp(np.random.default_rng(0), n_states=5, n_actions=3)
        assert dp.n_states == 5
        assert dp.n_actions == 3


# ---------------------------------------------------------------------------
# Closed-form benchmarks
# ---------------------------------------------------------------------------

class TestClosedForm:

    def test_single_state_geometric_series(self):
        """With one state and reward r, V* = r / (1 - beta) exactly."""
        beta, r = 0.95, 2.0
        dp = single_state_dp(reward=r, beta=beta)
        V, policy, _ = dp.solve_vfi(tol=1e-12, verbose=False)
        assert V[0] == pytest.approx(r / (1 - beta), rel=1e-8)
        assert policy[0] == 0

    def test_two_state_analytic_value_function_vfi(self):
        dp, V_expected, policy_expected = two_state_dp(beta=0.9)
        V, policy, _ = dp.solve_vfi(tol=1e-12, verbose=False)
        np.testing.assert_allclose(V, V_expected, rtol=1e-8)
        np.testing.assert_array_equal(policy, policy_expected)

    def test_two_state_analytic_value_function_pfi(self):
        dp, V_expected, policy_expected = two_state_dp(beta=0.9)
        V, policy = dp.solve_pfi(verbose=False)
        # PFI evaluates policies exactly (matrix inversion), so the value
        # of the optimal policy should be exact to machine precision.
        np.testing.assert_allclose(V, V_expected, rtol=1e-12)
        np.testing.assert_array_equal(policy, policy_expected)

    def test_policy_evaluation_matches_geometric_sum(self):
        """V_pi from matrix inversion must match the truncated series
        sum_t beta^t (Q_pi^t R_pi)."""
        rng = np.random.default_rng(7)
        dp = random_dp(rng, n_states=6, n_actions=3, beta=0.9)
        policy = rng.integers(0, dp.n_actions, size=dp.n_states)

        V_pi = dp.policy_evaluation(policy)

        R_pi = dp.R[np.arange(dp.n_states), policy]
        Q_pi = dp.Q[np.arange(dp.n_states), policy, :]
        V_series = np.zeros(dp.n_states)
        discounted_kernel = np.eye(dp.n_states)
        for _ in range(800):  # beta^800 ~ 3e-37: series has fully converged
            V_series += discounted_kernel @ R_pi
            discounted_kernel = dp.beta * discounted_kernel @ Q_pi
        np.testing.assert_allclose(V_pi, V_series, rtol=1e-10)


# ---------------------------------------------------------------------------
# Bellman operator properties
# ---------------------------------------------------------------------------

class TestBellmanOperator:

    def test_contraction_in_sup_norm(self):
        """||T(V1) - T(V2)||_inf <= beta * ||V1 - V2||_inf."""
        rng = np.random.default_rng(11)
        dp = random_dp(rng, beta=0.92)
        for _ in range(20):
            V1 = rng.normal(scale=10.0, size=dp.n_states)
            V2 = rng.normal(scale=10.0, size=dp.n_states)
            lhs = np.max(np.abs(dp.bellman_operator(V1) - dp.bellman_operator(V2)))
            rhs = dp.beta * np.max(np.abs(V1 - V2))
            assert lhs <= rhs + 1e-12

    def test_monotonicity(self):
        """V1 <= V2 (elementwise) implies T(V1) <= T(V2)."""
        rng = np.random.default_rng(13)
        dp = random_dp(rng)
        for _ in range(20):
            V1 = rng.normal(size=dp.n_states)
            V2 = V1 + rng.random(dp.n_states)  # V2 >= V1
            assert np.all(dp.bellman_operator(V1) <= dp.bellman_operator(V2) + 1e-12)

    def test_converged_value_is_fixed_point(self):
        """At the solution, T(V*) = V*."""
        rng = np.random.default_rng(17)
        dp = random_dp(rng)
        V, _, _ = dp.solve_vfi(tol=1e-12, verbose=False)
        np.testing.assert_allclose(dp.bellman_operator(V), V, atol=1e-9)

    def test_greedy_policy_attains_bellman_max(self):
        """The greedy policy's action values must equal max_a of the RHS."""
        rng = np.random.default_rng(19)
        dp = random_dp(rng)
        V = rng.normal(size=dp.n_states)
        policy = dp.compute_greedy(V)
        action_values = dp.R + dp.beta * (dp.Q @ V)
        chosen = action_values[np.arange(dp.n_states), policy]
        np.testing.assert_allclose(chosen, action_values.max(axis=1), rtol=1e-12)


# ---------------------------------------------------------------------------
# Cross-method agreement and convergence behavior
# ---------------------------------------------------------------------------

class TestSolverAgreement:

    @pytest.mark.parametrize("seed", [0, 1, 2, 3, 4])
    def test_vfi_and_pfi_agree(self, seed):
        dp = random_dp(np.random.default_rng(seed))
        V_vfi, policy_vfi, _ = dp.solve_vfi(tol=1e-11, verbose=False)
        V_pfi, policy_pfi = dp.solve_pfi(verbose=False)
        np.testing.assert_allclose(V_vfi, V_pfi, rtol=1e-6, atol=1e-6)
        np.testing.assert_array_equal(policy_vfi, policy_pfi)

    def test_vfi_history_tracks_monotone_error_decay(self):
        """Successive VFI errors must shrink at least geometrically (rate beta)."""
        dp = random_dp(np.random.default_rng(23), beta=0.9)
        _, _, history = dp.solve_vfi(tol=1e-10, track_history=True, verbose=False)
        assert history is not None and len(history) > 3
        errors = [np.max(np.abs(history[i + 1] - history[i]))
                  for i in range(len(history) - 1)]
        for e_next, e_prev in zip(errors[1:], errors[:-1]):
            assert e_next <= dp.beta * e_prev + 1e-12

    def test_vfi_history_disabled_by_default(self):
        dp = random_dp(np.random.default_rng(29))
        _, _, history = dp.solve_vfi(verbose=False)
        assert history is None
