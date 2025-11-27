import numpy as np
import pandas as pd
from scipy.optimize import minimize
from scipy.stats import norm
from IPython.display import display


class MLEstimator:
    """
    A class to perform Maximum Likelihood Estimation for a given model.

    This class is designed to be a general-purpose tool for estimating parameters
    of any model for which a log-likelihood function can be specified.
    """

    def __init__(self, loglike_func, data, param_names=None):
        """
        Initializes the MLEstimator.

        Parameters
        ----------
        loglike_func : callable
            The log-likelihood function. Must take two arguments: `params` (a
            NumPy array of parameters) and `data` (the data used for estimation).
            It should return the total log-likelihood value.
        data : object
            The data to be used in estimation. The format is flexible and should
            be handled by the user-provided loglike_func.
        param_names : list of str, optional
            A list of names for the parameters being estimated. If None, generic
            names like 'theta_0', 'theta_1', etc., will be used.
        """
        self.loglike = loglike_func
        self.data = data
        self.param_names = param_names  # Initialize unconditionally to avoid AttributeError
        self.results = None

    def fit(self, start_params):
        """
        Fit the model using a numerical optimizer to find the MLE.

        Parameters
        ----------
        start_params : np.ndarray
            An array of starting values for the optimization. The length must
            match the number of parameters.

        Returns
        -------
        self
            Returns the instance of the estimator.
        """
        if self.param_names is None:
            self.param_names = [f"theta_{i}" for i in range(len(start_params))]

        # The objective function is the *negative* of the log-likelihood,
        # because scipy.optimize performs minimization.
        def objective(params):
            return -self.loglike(params, self.data)

        # Use the BFGS algorithm to find the minimum of the negative log-likelihood
        res = minimize(objective, start_params, method="BFGS", options={"disp": False})

        # Store results
        self.mle_params = res.x
        # The inverse of the Hessian matrix is a consistent estimator of the
        # variance-covariance matrix of the parameters.
        self.vcov = res.hess_inv
        self.std_errs = np.sqrt(np.diag(self.vcov))
        self.loglike_val = -res.fun
        self.results = res
        return self

    def summary(self):
        """
        Display a summary table of the estimation results, similar to those
        produced by standard econometric software.
        """
        if self.results is None:
            print("Model has not been fitted yet.")
            return

        # Calculate z-scores and p-values for hypothesis tests
        z_scores = self.mle_params / self.std_errs
        p_values = norm.sf(np.abs(z_scores)) * 2

        # Calculate 95% confidence intervals
        ci_lower = self.mle_params - 1.96 * self.std_errs
        ci_upper = self.mle_params + 1.96 * self.std_errs

        # Create a pandas DataFrame for a nicely formatted table
        summary_df = pd.DataFrame(
            {
                "Coefficient": self.mle_params,
                "Std. Error": self.std_errs,
                "z-score": z_scores,
                "p-value": p_values,
                "[0.025": ci_lower,
                "0.975]": ci_upper,
            },
            index=self.param_names,
        )

        print(f"Maximum Log-Likelihood: {self.loglike_val:.4f}")
        try:
            print(f"Number of Observations: {len(self.data[0])}")
        except TypeError:
            print(f"Number of Observations: {len(self.data)}")

        display(summary_df.round(4))
        return summary_df


class MCMCSampler:
    """
    A class to perform Markov Chain Monte Carlo (MCMC) sampling using the
    Metropolis-Hastings algorithm.
    """

    def __init__(self, log_posterior_func, data):
        """
        Initializes the MCMC Sampler.

        Parameters
        ----------
        log_posterior_func : callable
            A function that computes the log of the posterior probability.
            It must take `params` and `data` as arguments.
        data : object
            The data to be used in estimation.
        """
        self.log_posterior = log_posterior_func
        self.data = data
        self.samples = None

    def sample(self, start_params, num_samples=10000, burn_in=1000, step_size=0.1):
        """
        Draw samples from the posterior distribution.

        Parameters
        ----------
        start_params : np.ndarray
            Starting values for the parameters.
        num_samples : int
            Number of samples to generate.
        burn_in : int
            Number of initial samples to discard.
        step_size : float or np.ndarray
            Standard deviation of the proposal distribution.
        """
        current_params = np.asarray(start_params)
        samples = [current_params]

        current_log_post = self.log_posterior(current_params, self.data)

        for i in range(num_samples + burn_in):
            # Propose a new set of parameters
            proposal = np.random.normal(current_params, step_size)

            # Calculate log posterior at the proposal
            proposal_log_post = self.log_posterior(proposal, self.data)

            # Acceptance probability
            log_alpha = proposal_log_post - current_log_post
            if np.log(np.random.rand()) < log_alpha:
                # Accept the proposal
                current_params = proposal
                current_log_post = proposal_log_post

            samples.append(current_params)

        self.samples = np.array(samples[burn_in:])
        return self

    def summary(self):
        """
        Display a summary of the posterior samples.
        """
        if self.samples is None:
            print("No samples generated yet.")
            return

        summary_df = pd.DataFrame(
            {
                "Mean": np.mean(self.samples, axis=0),
                "Std. Dev.": np.std(self.samples, axis=0),
                "2.5%": np.percentile(self.samples, 2.5, axis=0),
                "97.5%": np.percentile(self.samples, 97.5, axis=0),
            }
        )
        display(summary_df)
        return summary_df
