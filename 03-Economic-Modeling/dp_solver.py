import numpy as np
from typing import Tuple, List


class DiscreteDP:
    """
    A class to represent and solve discrete dynamic programming models.

    It is designed to solve problems of the form:
    V(s) = max_a { R(s, a) + beta * sum_{s'} Q(s, a, s') * V(s') }

    Parameters
    ----------
    R : np.ndarray
        The reward array of shape (n_states, n_actions). R[s, a] is the
        reward for taking action a in state s.
    Q : np.ndarray
        The transition probability matrix of shape (n_states, n_actions, n_states).
        Q[s, a, s'] is the probability of transitioning to state s' from state s
        when taking action a.
    beta : float
        The discount factor, must be in (0, 1).

    Attributes
    ----------
    R, Q, beta : See Parameters.
    n_states : int
        The number of states.
    n_actions : int
        The number of actions.
    """

    def __init__(self, R: np.ndarray, Q: np.ndarray, beta: float):
        self.R = np.asarray(R)
        self.Q = np.asarray(Q)
        self.beta = beta
        if not (0 < self.beta < 1):
            raise ValueError("beta must be in (0, 1).")

        self.n_states, self.n_actions = self.R.shape
        if self.Q.shape != (self.n_states, self.n_actions, self.n_states):
            raise ValueError("The shape of Q is not compatible with R.")

    def bellman_operator(self, V: np.ndarray) -> np.ndarray:
        """
        The Bellman operator, which computes the right-hand side of the
        Bellman equation. T(V) = max_a { R + beta * Q @ V }.

        Parameters
        ----------
        V : np.ndarray
            A candidate value function, array of shape (n_states,).

        Returns
        -------
        np.ndarray
            The updated value function, array of shape (n_states,).
        """
        # self.Q is (n, m, n). V is (n,). Q @ V gives (n, m)
        expected_V = self.Q @ V
        return np.max(self.R + self.beta * expected_V, axis=1)

    def compute_greedy(self, V: np.ndarray) -> np.ndarray:
        """
        Computes the greedy policy given a value function V.

        Parameters
        ----------
        V : np.ndarray
            A candidate value function, array of shape (n_states,).

        Returns
        -------
        np.ndarray
            The optimal policy, an array of shape (n_states,) containing
            the index of the optimal action for each state.
        """
        expected_V = self.Q @ V
        return np.argmax(self.R + self.beta * expected_V, axis=1)

    def solve_vfi(
        self, tol: float = 1e-7, max_iter: int = 2000, track_history: bool = False
    ) -> Tuple[np.ndarray, np.ndarray, List[np.ndarray]]:
        """
        Solves the model using Value Function Iteration (VFI).

        Parameters
        ----------
        tol : float, optional
            The tolerance for convergence.
        max_iter : int, optional
            The maximum number of iterations.
        track_history : bool, optional
            If True, stores the value function at each iteration.

        Returns
        -------
        V : np.ndarray
            The converged value function.
        policy : np.ndarray
            The optimal policy corresponding to V.
        history : list
            A list of value functions at each iteration (if track_history is True).
        """
        V = np.zeros(self.n_states)  # Initial guess
        history = [V] if track_history else None

        for i in range(max_iter):
            V_new = self.bellman_operator(V)
            if np.max(np.abs(V - V_new)) < tol:
                print(f"VFI converged in {i} iterations.")
                policy = self.compute_greedy(V_new)
                return V_new, policy, history
            V = V_new
            if track_history:
                history.append(V)

        print("VFI failed to converge.")
        policy = self.compute_greedy(V)
        return V, policy, history

    def policy_evaluation(self, policy: np.ndarray) -> np.ndarray:
        """
        Computes the value of a given policy using matrix inversion.
        V_pi = (I - beta * P_pi)^-1 * R_pi

        Parameters
        ----------
        policy : np.ndarray
            A policy, array of shape (n_states,) specifying the action
            to take in each state.

        Returns
        -------
        np.ndarray
            The value function V_pi for the given policy.
        """
        # Get rewards and transition probabilities for the given policy
        R_pi = self.R[np.arange(self.n_states), policy]
        Q_pi = self.Q[np.arange(self.n_states), policy, :]

        # Solve the linear system (I - beta * Q_pi) * V = R_pi
        identity_matrix = np.identity(self.n_states)
        V_pi = np.linalg.solve(identity_matrix - self.beta * Q_pi, R_pi)
        return V_pi

    def solve_pfi(self, max_iter: int = 500) -> Tuple[np.ndarray, np.ndarray]:
        """
        Solves the model using Policy Function Iteration (PFI).

        Parameters
        ----------
        max_iter : int, optional
            The maximum number of iterations.

        Returns
        -------
        V : np.ndarray
            The converged value function.
        policy : np.ndarray
            The optimal policy.
        """
        policy = np.zeros(self.n_states, dtype=int)  # Start with an arbitrary policy

        for i in range(max_iter):
            # 1. Policy Evaluation
            V_pi = self.policy_evaluation(policy)

            # 2. Policy Improvement
            new_policy = self.compute_greedy(V_pi)

            if np.array_equal(new_policy, policy):
                print(f"PFI converged in {i} iterations.")
                return V_pi, new_policy

            policy = new_policy

        print("PFI failed to converge.")
        V = self.policy_evaluation(policy)
        return V, policy
