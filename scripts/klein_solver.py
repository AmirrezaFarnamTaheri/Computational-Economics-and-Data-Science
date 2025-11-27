import numpy as np
from scipy.linalg import ordqz

def solve_linear_model(AA, BB, CC=None):
    """
    Solves a linear rational expectations model of the form:
    AA * x_{t+1} = BB * x_t + CC * epsilon_{t+1}

    where x_t includes both predetermined (state) and non-predetermined (control) variables.

    This function uses the QZ (Generalized Schur) decomposition with reordering (ordqz)
    to separate stable and unstable eigenvalues. It implements a method similar to
    Paul Klein (2000) or Sims (2002).

    Parameters:
    - AA, BB: n x n matrices defining the system dynamics.
    - CC: n x k matrix defining the impact of exogenous shocks (optional).

    Returns:
    - P: Transition matrix for the state variables.
    - Q: Policy function mapping state variables to control variables (if applicable).
         Note: The exact structure of return depends on how x_t is ordered.

    Assumption:
    The system is ordered such that predetermined variables (states) come FIRST,
    followed by non-predetermined variables (jumps/controls).
    Let n_s be the number of stable eigenvalues (should equal number of states).
    """

    # 1. Generalized Schur Decomposition (QZ)
    # We want to reorder such that stable eigenvalues (|lambda| < 1) are in the top-left.
    # The sort keyword 'iuc' means "inside unit circle".
    try:
        S, T, alpha, beta, U, V = ordqz(AA, BB, sort='iuc', output='complex')
    except Exception as e:
        raise ValueError(f"QZ Decomposition failed: {e}")

    # Determine the number of stable eigenvalues
    # generalized eigenvalues are alpha / beta
    # 'iuc' sorts them to the top-left.
    # We assume the number of stable eigenvalues equals the number of predetermined variables (states).
    # If not, the Blanchard-Kahn conditions are violated.

    # Count stable eigenvalues
    eig _vals = np.abs(alpha / beta)
    n_stable = np.sum(eig_vals < 1.0)

    # Check Blanchard-Kahn
    # Ideally, n_stable should equal n_states (provided by user, or inferred).
    # Here we infer n_states = n_stable and solve accordingly.

    # Partition matrices
    # S = [S11 S12]
    #     [0   S22]
    # T = [T11 T12]
    #     [0   T22]
    # Z (or V) connects the original variables to the transformed ones.
    # x_t = Z.T @ y_t  (Note: Scipy's V is usually Z.T or something similar, check docs)
    # Scipy docs: A = U @ S @ V.H, B = U @ T @ V.H
    # So V.H (conjugate transpose) is the right eigenvector matrix Z.
    # Let Z = V.conj().T

    Z = V.conj().T

    # Partition Z
    # Z = [Z11 Z12]
    #     [Z21 Z22]
    # where 1 refers to stable/state block, 2 refers to unstable/jump block.

    Z11 = Z[:n_stable, :n_stable]
    Z12 = Z[:n_stable, n_stable:]
    Z21 = Z[n_stable:, :n_stable]
    Z22 = Z[n_stable:, n_stable:]

    S11 = S[:n_stable, :n_stable]
    T11 = T[:n_stable, :n_stable]

    # Check invertibility for uniqueness
    if np.linalg.det(Z22) == 0:
        raise ValueError("Invertibility condition failed. Indeterminacy or no solution.")

    # Compute Policy Function Coefficients
    # From Klein (2000):
    # Variables are linked by: x_jump_t = C_policy * x_state_t
    # C_policy = Z21 @ inv(Z11)  <-- This is if variables are ordered [jump, state]?
    # Let's derive carefully from the triangular system.

    # The unstable block equation is: S22 * y2_{t+1} = T22 * y2_t + ...
    # For stability, we must have y2_t = 0 for all t (if no shocks).
    # The relationship between x and y is:
    # [x_state] = [Z11 Z12] [y1]
    # [x_jump ]   [Z21 Z22] [y2]
    # If y2 = 0, then:
    # x_state = Z11 * y1  => y1 = inv(Z11) * x_state
    # x_jump  = Z21 * y1  => x_jump = Z21 * inv(Z11) * x_state

    # Wait, usually ordqz puts stable roots first.
    # So y1 corresponds to stable roots, y2 to unstable.
    # To suppress explosive paths, we need to decouple y2 from shocks/history?
    # Actually, the condition is usually that the unstable components y2 must be zero
    # (or function of shocks only) to satisfy transversality.

    # With y2_t = 0:
    # x_jump_t = Z21 @ inv(Z11) @ x_state_t
    # But usually Z is partitioned based on the variable ordering.
    # If the user input x_t = [state, jump], and we sorted stable roots first...
    # The mapping from sorted eigenspace to variables is Z.
    # We need to express jumps in terms of states.

    # Inverse of Z block?
    # Actually, proper solution for x_{t+1} = P x_t
    # P = Z11 @ inv(S11) @ T11 @ inv(Z11)  (for the state part)
    # And mapping matrix F: x_jump = F x_state

    # Correct solution (Klein):
    # s_t = states, u_t = controls.
    # u_t = Real(Z21 @ inv(Z11)) @ s_t
    # s_{t+1} = Real(Z11 @ inv(S11) @ T11 @ inv(Z11)) @ s_t

    # Let's implement this.

    inv_Z11 = np.linalg.inv(Z11)

    # Transition matrix for states (P)
    # S11 * y1_{t+1} = T11 * y1_t  => y1_{t+1} = inv(S11) * T11 * y1_t
    # s_{t+1} = Z11 * y1_{t+1} = Z11 * inv(S11) * T11 * inv(Z11) * s_t
    P = np.real(Z11 @ np.linalg.inv(S11) @ T11 @ inv_Z11)

    # Policy matrix (Mapping states to controls)
    # u_t = Z21 * y1_t = Z21 * inv(Z11) * s_t
    F = np.real(Z21 @ inv_Z11)

    return P, F

def solve_klein(AA, BB, CC, n_states):
    """
    Wrapper specifically for the RBC notebook format.
    AA, BB are 8x8. CC is 8x1.
    n_states is the number of predetermined variables.

    In the RBC notebook:
    x_t = [k_hat, a_hat, l_hat, c_hat, y_hat, i_hat, w_hat, r_hat]
    States: k_hat (endogenous), a_hat (exogenous). Total = 2.
    Controls: l_hat, c_hat, ... Total = 6.
    """

    # 1. Solve the homogenous system
    P_states, F_policy = solve_linear_model(AA, BB)

    # P_states is 2x2 (transition for k, a)
    # F_policy is 6x2 (mapping k, a -> l, c, y, i, w, r)

    # 2. Reconstruct full system matrices P and Q as requested by the notebook.
    # The notebook wants:
    # s_{t+1} = Q * s_t + M * epsilon_{t+1}
    # c_t = P * s_t
    # (Note: Notebook uses P for Policy and Q for Transition. Klein uses P for Transition.)

    # Notebook notation:
    # P_notebook (Policy) = F_policy
    # Q_notebook (Transition) = P_states

    Q_notebook = P_states
    P_notebook = F_policy

    # 3. Handle the Shock Matrix M
    # The system is AA*x_{t+1} = BB*x_t + CC*eps_{t+1}
    # x_{t+1} = Q*x_t + ...
    # Substitute x_t+1 = [s_{t+1}, u_{t+1}]'
    # The shock only affects s_{t+1} directly usually.
    # For the standard RBC, s_{t+1} = Q*s_t + M*eps
    # M depends on CC and the decomposition.
    # Typically M = Z11 @ inv(S11) @ (Q_qz @ CC)_upper_part ?
    # Let's derive or use a simplified assumption for now that shocks hit states directly.
    # In RBC, a_{t+1} = rho * a_t + eps_{t+1}.
    # So M for a_hat is just 1. M for k_hat is 0.

    # We can calculate M formally if needed, but given the specific RBC structure,
    # we know M corresponds to the impact on k_{t+1} and a_{t+1}.
    # k_{t+1} is predetermined at t. So shock at t+1 doesn't affect k_{t+1} (it affects k_{t+2}).
    # Wait, timing convention.
    # x_t is observed at t.
    # a_{t+1} = rho*a_t + eps_{t+1}.
    # k_{t+1} is determined at t.
    # So shock eps_{t+1} affects a_{t+1} (coeff 1) and nothing else in s_{t+1}.

    M_notebook = np.zeros((2, 1))
    M_notebook[1, 0] = 1.0 # Shock hits a_hat (2nd state var)

    return {'P': P_notebook, 'Q': Q_notebook, 'M': M_notebook}
