import numpy as np
from scipy.stats import norm

# Note: @njit decorator removed due to incompatibility with scipy.stats.norm
# For performance-critical applications, consider implementing a custom
# norm.cdf approximation that is compatible with Numba
# Or use the quantecon library: from quantecon import tauchen

def tauchen(rho, sigma_e, n_states=7, m=3):
    """
    Implements Tauchen's (1986) method for discretizing an AR(1) process.

    Parameters
    ----------
    rho : float
        The persistence parameter of the AR(1) process.
    sigma_e : float
        The standard deviation of the innovation term.
    n_states : int, optional
        The number of states to use in the discretized Markov chain.
    m : float, optional
        The number of standard deviations of the unconditional distribution
        to use for the grid boundaries.

    Returns
    -------
    z_grid : np.ndarray
        The grid for the discretized state variable.
    P : np.ndarray
        The transition matrix for the discretized Markov chain.
    """
    sigma_z = sigma_e / np.sqrt(1 - rho**2)
    z_max = m * sigma_z
    z_grid = np.linspace(-z_max, z_max, n_states)
    step = z_grid[1] - z_grid[0]

    P = np.zeros((n_states, n_states))
    for i in range(n_states):
        cond_mean = rho * z_grid[i]
        P[i, 0] = norm.cdf((z_grid[0] - cond_mean + step / 2) / sigma_e)
        P[i, -1] = 1 - norm.cdf((z_grid[-1] - cond_mean - step / 2) / sigma_e)
        for j in range(1, n_states - 1):
            P[i, j] = norm.cdf((z_grid[j] - cond_mean + step / 2) / sigma_e) - norm.cdf(
                (z_grid[j] - cond_mean - step / 2) / sigma_e
            )
    return z_grid, P
