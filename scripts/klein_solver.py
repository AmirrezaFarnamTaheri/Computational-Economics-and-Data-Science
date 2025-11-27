import numpy as np
from scipy.linalg import ordqz

def solve_klein(A, B, n_states):
    """
    Solves a linear rational expectations model of the form:
    A * E_t[x_{t+1}] = B * x_t + C * epsilon_{t+1}

    Using the QZ decomposition (Klein, 2000).

    Parameters:
    - A, B: Square matrices (n x n) linking current and future variables.
    - n_states: Number of predetermined (state) variables.

    Returns:
    - P: Coefficient matrix for the state transition: k_{t+1} = P * k_t
    - F: Coefficient matrix for the policy function: u_t = F * k_t
    """

    # 1. QZ Decomposition with reordering
    # We want to sort the generalized eigenvalues (alpha/beta) such that
    # stable eigenvalues (|lambda| < 1) are in the top-left.

    def sort_stable(alpha, beta):
        # Handle cases where beta is close to zero (infinite eigenvalue)
        # We consider infinite eigenvalues as unstable (should be at bottom-right)
        return np.abs(alpha) < np.abs(beta)

    S, T, alpha, beta, Q, Z = ordqz(A, B, sort=sort_stable, output='real')

    # 2. Check Blanchard-Kahn conditions
    # We expect exactly n_states stable eigenvalues.
    n_stable = np.sum(sort_stable(alpha, beta))
    if n_stable != n_states:
        raise ValueError(f"Blanchard-Kahn condition failed. Expected {n_states} stable eigenvalues, found {n_stable}.")

    # 3. Partition matrices
    # Variables are x_t = [k_t, u_t]' where k_t are states, u_t are controls.
    # The QZ decomposition reorders the system.
    # Z.T * x_t = y_t
    # We need to relate the original variables to the transformed variables.

    # Z is orthogonal, so Z^T is Z inverse.
    # Z = [Z11 Z12]
    #     [Z21 Z22]
    # where Z11 is (n_states x n_states)

    Z = Z.T # Scipy returns Z such that Q*A*Z^T = S. So the transformation is x = Z * y.
    # Wait, let's verify scipy docs.
    # "Q, Z: Unitary matrices. Q @ A @ Z.T = S, Q @ B @ Z.T = T"
    # So A = Q.T @ S @ Z
    # A * x_{t+1} = B * x_t
    # Q.T * S * Z * x_{t+1} = Q.T * T * Z * x_t
    # S * (Z * x_{t+1}) = T * (Z * x_t)
    # Let y_t = Z * x_t.
    # S * y_{t+1} = T * y_t.
    # Since S, T are upper triangular and sorted, the system decouples.
    # The bottom block (unstable) must be zero for stability in forward solution.

    Z11 = Z[:n_states, :n_states]
    Z12 = Z[:n_states, n_states:]
    Z21 = Z[n_states:, :n_states]
    Z22 = Z[n_states:, n_states:]

    S11 = S[:n_states, :n_states]
    T11 = T[:n_states, :n_states]

    # 4. Compute solution matrices
    # If the Blanchard-Kahn condition holds, Z21 is invertible (typically).
    # Wait, usually it involves inverting Z22 or similar for controls.

    # From Klein (2000):
    # State transition: k_{t+1} = P * k_t
    # Controls: u_t = F * k_t

    # If Z is partitioned as Z_k and Z_u columns?
    # Let's stick to the method derived from S * y = T * y

    # Stable block: S11 * y1_{t+1} + S12 * y2_{t+1} = T11 * y1_t + T12 * y2_t
    # Unstable block: S22 * y2_{t+1} = T22 * y2_t  => y2_t = 0 for stability (if no shocks in this block)

    # So y2_t = 0.
    # Then y1_{t+1} = S11^{-1} * T11 * y1_t

    # We have y_t = Z * x_t = [Z11 Z12; Z21 Z22] * [k_t; u_t]
    # y1_t = Z11 * k_t + Z12 * u_t
    # y2_t = Z21 * k_t + Z22 * u_t = 0

    # From y2_t = 0, we get: Z21 * k_t + Z22 * u_t = 0
    # => u_t = - Z22^{-1} * Z21 * k_t
    # So F = - inv(Z22) * Z21

    if np.linalg.det(Z22) == 0:
         raise ValueError("Z22 is singular. Model may not have a unique solution.")

    F = -np.linalg.solve(Z22, Z21)

    # Now for state transition P:
    # y1_t = Z11 * k_t + Z12 * F * k_t = (Z11 + Z12 * F) * k_t
    # y1_{t+1} = S11^{-1} * T11 * y1_t
    # (Z11 + Z12 * F) * k_{t+1} = S11^{-1} * T11 * (Z11 + Z12 * F) * k_t

    # Let M = (Z11 + Z12 * F)
    # k_{t+1} = M^{-1} * S11^{-1} * T11 * M * k_t

    # Alternatively, direct substitution:
    # S11 * y1_{t+1} = T11 * y1_t
    # y1_{t+1} = Z11 * k_{t+1} + Z12 * u_{t+1} = (Z11 + Z12*F) * k_{t+1}
    # y1_t = (Z11 + Z12*F) * k_t

    # So S11 * (Z11 + Z12*F) * k_{t+1} = T11 * (Z11 + Z12*F) * k_t
    # Let H = Z11 + Z12 * F
    # k_{t+1} = inv(S11 @ H) @ (T11 @ H) * k_t

    # Note: Depending on Z definition (row vs col vectors), indices might swap.
    # Scipy ordqz returns Z such that x = Z^T * y ? No.
    # "Q, Z: Unitary matrices. Q @ A @ Z.T = S"
    # This implies A = Q.H @ S @ Z.
    # A x = B x
    # Q.H S Z x = Q.H T Z x
    # S (Z x) = T (Z x)
    # Let y = Z x.
    # The previous derivation holds.

    return -np.linalg.solve(Z22, Z21), np.linalg.solve(S11 @ (Z11 + Z12 @ F), T11 @ (Z11 + Z12 @ F))

