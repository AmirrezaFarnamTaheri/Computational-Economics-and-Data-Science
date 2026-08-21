import warnings

import numpy as np
from scipy.linalg import ordqz


def solve_qz(AA, BB, n_states):
    """
    Solves a linear rational expectations model of the form:

        AA @ E_t[x_{t+1}] = BB @ x_t

    using the QZ (generalized Schur) decomposition, following Klein (2000).

    The state vector must be ordered as x_t = [k_t; u_t], where k_t are the
    n_states predetermined (state) variables and u_t are the jump (control)
    variables.

    Method
    ------
    scipy's ``ordqz(AA, BB)`` returns orthogonal Q, Z and quasi-triangular
    S, T such that

        AA = Q @ S @ Z.T   and   BB = Q @ T @ Z.T.

    Substituting into the system and premultiplying by Q.T gives

        S @ (Z.T @ x_{t+1}) = T @ (Z.T @ x_t),

    so the auxiliary variable is y_t = Z.T @ x_t, equivalently x_t = Z @ y_t.
    Generalized eigenvalues are lambda_i = T_ii / S_ii; with scipy's
    (alpha, beta) output, lambda_i = beta_i / alpha_i, so a root is stable
    (|lambda| < 1) when |beta| < |alpha|. We sort stable roots into the
    top-left block.

    Partitioning y_t = [y1_t; y2_t] (stable/unstable) and Z conformably,
    saddle-path stability requires y2_t = 0, so

        x_t = Z[:, :n_states] @ y1_t
        =>  k_t = Z11 @ y1_t,   u_t = Z21 @ y1_t
        =>  u_t = Z21 @ inv(Z11) @ k_t                    (Policy)

    and from the stable block S11 @ y1_{t+1} = T11 @ y1_t:

        k_{t+1} = Z11 @ inv(S11) @ T11 @ inv(Z11) @ k_t   (Transition)

    Parameters
    ----------
    AA, BB : np.ndarray
        Square matrices (n x n) describing the system AA @ x' = BB @ x.
    n_states : int
        Number of predetermined (state) variables. The state vector x_t
        must be ordered as [states; controls].

    Returns
    -------
    dict with keys:
        'Policy': Matrix P such that u_t = P @ k_t
        'Transition': Matrix M such that k_{t+1} = M @ k_t
        'Z': The QZ orthogonal matrix Z (useful for debugging)

    References
    ----------
    Klein, P. (2000). "Using the generalized Schur form to solve a
    multivariate linear rational expectations model." Journal of Economic
    Dynamics and Control, 24(10), 1405-1423.
    """

    # 1. QZ decomposition, sorted so stable roots (|beta| < |alpha|) come first.
    def sort_stable(alpha, beta):
        # Stable roots satisfy |lambda| = |beta/alpha| < 1, i.e. |beta| < |alpha|.
        # An infinite root (alpha = 0) can never satisfy this, so no separate
        # finiteness cutoff is needed — and unlike an absolute threshold, the
        # comparison is invariant to a common rescaling of (AA, BB).
        return np.abs(beta) < np.abs(alpha)

    S, T, alpha, beta, Q, Z = ordqz(AA, BB, sort=sort_stable, output="real")

    # 2. Blanchard-Kahn check: saddle-path uniqueness needs exactly
    # n_states stable roots.
    n_stable = np.sum(sort_stable(alpha, beta))
    if n_stable != n_states:
        warnings.warn(
            f"Blanchard-Kahn condition warning: Expected {n_states} stable "
            f"roots, found {n_stable}. System may be indeterminate or explosive."
        )

    # 3. Partition Z conformably with y = [stable; unstable] and x = [k; u]
    Z11 = Z[:n_states, :n_states]
    Z21 = Z[n_states:, :n_states]
    S11 = S[:n_states, :n_states]
    T11 = T[:n_states, :n_states]

    # Klein's rank condition: Z11 must be invertible for k_t to pin down y1_t.
    if n_states > 0 and 1.0 / np.linalg.cond(Z11) < 1e-12:
        raise ValueError(
            "Rank condition failed: Z11 is (numerically) singular. "
            "The states do not span the stable subspace."
        )

    # Compute X @ inv(Z11) as solve(Z11.T, X.T).T — solving the linear
    # system is better conditioned than forming the inverse explicitly.

    # 4. Policy: u_t = Z21 @ inv(Z11) @ k_t
    Policy = np.linalg.solve(Z11.T, Z21.T).T

    # 5. Transition: k_{t+1} = Z11 @ inv(S11) @ T11 @ inv(Z11) @ k_t
    stable_dynamics = np.linalg.solve(S11, T11)
    Transition = np.linalg.solve(Z11.T, (Z11 @ stable_dynamics).T).T

    return {"Policy": Policy, "Transition": Transition, "Z": Z}
