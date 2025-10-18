import numpy as np
import pandas as pd

def get_bgg_solution_matrices(chi=0.05):
    """
    Constructs the illustrative solution matrices for the BGG model.

    This function returns the matrices P and Q for the reduced-form solution:
    x_t = P * x_{t-1} + Q * z_t

    The state vector is x_t = [y_t, pi_t, k_t, n_t]'
    (Output, Inflation, Capital, Net Worth)

    The matrices are illustrative and calibrated to show the financial
    accelerator mechanism. They are composed of a baseline 'frictionless'
    part and a part that depends on the financial friction parameter 'chi'.
    """

    # Base dynamics (represents a standard frictionless New Keynesian model)
    P_base = np.array([
        # y_t,  pi_t,   k_t,   n_t  <- x_{t-1}
        [0.95,  0.1,  0.05,  0.0], # y_t equation
        [0.05,  0.85,  0.1,  0.0], # pi_t equation
        [0.1,   0.0,   0.9,   0.0], # k_t equation
        [0.0,   0.0,   0.0,   0.0]  # n_t equation (no role in frictionless model)
    ])

    # Accelerator dynamics (captures the effect of the financial friction)
    # This matrix multiplies 'chi'
    P_accel = np.array([
        # y_t,  pi_t,   k_t,   n_t  <- x_{t-1}
        [0.0,   0.0,   0.1,   0.2], # y_t is boosted by higher past net worth
        [0.0,   0.0,  0.05,   0.1], # pi_t also sees a boost
        [0.1,   0.1,  0.05,   0.3], # k_t is strongly boosted by higher net worth
        [0.2,   0.1,   0.3,  0.85]  # n_t is persistent and depends on past econ activity
    ])

    # The final policy matrix P is the sum of the base and the friction effect
    P = P_base + chi * P_accel

    # Shock matrix Q (represents a 1-std-dev technology shock, z_t)
    # The shock hits all variables, especially output, capital, and net worth
    Q = np.array([1.0, 0.2, 1.2, 0.8]).reshape(4, 1)

    return P, Q

def generate_irfs_from_solution(P, Q, T=40):
    """Generates IRFs from a solved model x_t = P*x_{t-1} + Q*z_t"""
    n_vars = P.shape[0]
    irfs = np.zeros((n_vars, T))
    irfs[:, 0] = Q.flatten()

    for t in range(1, T):
        irfs[:, t] = P @ irfs[:, t-1]

    irf_df = pd.DataFrame(irfs.T, columns=['Output', 'Inflation', 'Capital', 'Net Worth'])

    # Derive investment from the capital series for plotting
    delta = 0.025 # Capital depreciation rate
    irf_df['Investment'] = irf_df['Capital'] - (1 - delta) * irf_df['Capital'].shift(1).fillna(0)

    return irf_df