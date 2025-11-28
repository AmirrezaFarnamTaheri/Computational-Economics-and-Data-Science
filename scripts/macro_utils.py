import numpy as np
from scipy.linalg import ordqz
import pandas as pd
import warnings

def solve_qz(AA, BB, n_states):
    """
    Solves a linear rational expectations model of the form:
    AA * E_t[x_{t+1}] = BB * x_t + Exogenous_Shocks

    Using the QZ decomposition (Klein, 2000).

    Parameters:
    -----------
    AA, BB : np.ndarray
        Square matrices (n x n) describing the system.
    n_states : int
        Number of predetermined (state) variables.
        The state vector x_t must be ordered as [states; controls].

    Returns:
    --------
    dict with keys:
        'Policy': Matrix P such that u_t = P * k_t
        'Transition': Matrix Q such that k_{t+1} = Q * k_t
        'Z': The QZ unitary matrix Z (useful for debugging)
    """

    # 1. QZ Decomposition
    # Sort such that stable eigenvalues (|lambda| < 1) are in the top-left (indices 0 to n_states-1)
    def sort_stable(alpha, beta):
        return np.abs(alpha) < np.abs(beta)

    S, T, alpha, beta, Q, Z = ordqz(AA, BB, sort=sort_stable, output='real')

    # Z from scipy satisfies: Q @ AA @ Z.T = S
    # Meaning AA = Q.T @ S @ Z
    # AA * x = Q.T @ S @ Z @ x
    # System: Q.T @ S @ Z @ x_{t+1} = Q.T @ T @ Z @ x_t
    # Multiply by Q: S @ (Z @ x_{t+1}) = T @ (Z @ x_t)
    # Let y_t = Z @ x_t.
    # S @ y_{t+1} = T @ y_t

    # Partition Z
    # Z has shape (n, n).
    # x_t has first n_states as k_t, rest as u_t.
    # y_t = [y1_t; y2_t] where y1 has size n_states (stable).
    # Z = [[Z11, Z12], [Z21, Z22]]

    Z11 = Z[:n_states, :n_states]
    Z12 = Z[:n_states, n_states:]
    Z21 = Z[n_states:, :n_states]
    Z22 = Z[n_states:, n_states:]

    # 2. Check Blanchard-Kahn
    # We need exactly n_states stable eigenvalues.
    n_stable = np.sum(sort_stable(alpha, beta))
    if n_stable != n_states:
        warnings.warn(f"Blanchard-Kahn condition warning: Expected {n_states} stable roots, found {n_stable}. System may be indeterminate or explosive.")

    # 3. Solve for Controls: u_t = Policy * k_t
    # Stability requires y2_t = 0 (assuming no shocks in the unstable block yet)
    # y2_t = Z21 * k_t + Z22 * u_t = 0
    # => u_t = - inv(Z22) * Z21 * k_t

    if np.linalg.det(Z22) == 0:
        raise ValueError("Indeterminacy: Z22 is singular. Rank condition failed.")

    Policy = -np.linalg.solve(Z22, Z21)

    # 4. Solve for Transitions: k_{t+1} = Transition * k_t
    # y1_t = Z11 * k_t + Z12 * u_t = (Z11 + Z12 * Policy) * k_t
    # S11 * y1_{t+1} = T11 * y1_t
    # S11 * (Z11 + Z12 * P) * k_{t+1} = T11 * (Z11 + Z12 * P) * k_t
    # Let H = Z11 + Z12 * P
    # k_{t+1} = inv(S11 @ H) @ (T11 @ H) * k_t

    S11 = S[:n_states, :n_states]
    T11 = T[:n_states, :n_states]
    H = Z11 + Z12 @ Policy

    Transition = np.linalg.solve(S11 @ H, T11 @ H)

    return {'Policy': Policy, 'Transition': Transition, 'Z': Z}
