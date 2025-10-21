import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm

class MLEstimator:
    """
    A class to perform Maximum Likelihood Estimation for a given model.
    """
    def __init__(self, loglike, data, param_names=None):
        self.loglike = loglike
        self.data = data
        self.param_names = param_names if param_names is not None else []
        self.n_params = len(self.param_names)
        self.mle_params = None
        self.vcov = None
        self.max_loglike = None

    def fit(self, start_params):
        """
        Fits the model using numerical optimization.
        """
        result = minimize(self.loglike, start_params, args=(self.data['y'], self.data['X']),
                          method='BFGS', options={'disp': False})

        self.mle_params = result.x
        self.vcov = result.hess_inv
        self.max_loglike = -result.fun

    def summary(self):
        """
        Prints a summary of the estimation results.
        """
        if self.mle_params is None:
            print("Model has not been fitted yet.")
            return

        std_errors = np.sqrt(np.diag(self.vcov))
        z_scores = self.mle_params / std_errors
        p_values = 2 * (1 - norm.cdf(np.abs(z_scores)))

        results_df = pd.DataFrame({
            'Coefficient': self.mle_params,
            'Std. Error': std_errors,
            'z-value': z_scores,
            'P>|z|': p_values
        }, index=self.param_names)

        print("\\n" + "="*80)
        print("Maximum Likelihood Estimation Results")
        print("="*80)
        print(f"Log-Likelihood: {self.max_loglike:.4f}")
        print(f"Number of Observations: {len(self.data['y'])}")
        print(f"Number of Parameters: {self.n_params}")
        print("-"*80)
        print(results_df.round(4))
        print("="*80)
