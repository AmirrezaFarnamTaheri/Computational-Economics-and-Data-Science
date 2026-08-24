"""Small, teaching-oriented econometrics utilities shared by Module 06 notebooks."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass

import numpy as np

Array = np.ndarray


@dataclass
class MCMCSampler:
    """Random-walk Metropolis-Hastings sampler with deterministic RNG support.

    The class deliberately keeps the algorithm transparent for teaching. Production
    Bayesian work should generally use PyMC/Stan/NUTS, but a from-scratch sampler is
    useful for validating posterior geometry against analytical examples.
    """

    log_posterior: Callable[..., float]
    data: object | None = None
    random_seed: int = 42

    def __post_init__(self) -> None:
        self.rng = np.random.default_rng(self.random_seed)
        self.samples: Array = np.empty((0, 0), dtype=float)
        self.acceptance_rate: float = float("nan")

    def _evaluate(self, params: Array) -> float:
        argument: float | Array = float(params[0]) if params.size == 1 else params
        value = (
            self.log_posterior(argument, self.data)
            if self.data is not None
            else self.log_posterior(argument)
        )
        value = float(value)
        return value if np.isfinite(value) else -np.inf

    def sample(
        self,
        start_params: list[float] | Array,
        *,
        num_samples: int = 10_000,
        burn_in: int = 1_000,
        step_size: float | Array = 0.1,
    ) -> Array:
        """Draw posterior samples with a Gaussian random-walk proposal."""
        if num_samples <= 0 or burn_in < 0:
            raise ValueError("num_samples must be positive and burn_in nonnegative")
        current = np.atleast_1d(np.asarray(start_params, dtype=float)).copy()
        scale = np.broadcast_to(np.asarray(step_size, dtype=float), current.shape)
        if np.any(scale <= 0):
            raise ValueError("step_size must be strictly positive")
        current_lp = self._evaluate(current)
        if not np.isfinite(current_lp):
            raise ValueError("start_params must have finite posterior density")

        total = burn_in + num_samples
        draws = np.empty((num_samples, current.size), dtype=float)
        accepted = 0
        stored = 0
        for iteration in range(total):
            proposal = current + self.rng.normal(scale=scale, size=current.shape)
            proposal_lp = self._evaluate(proposal)
            log_acceptance = proposal_lp - current_lp
            if np.log(self.rng.random()) < min(0.0, log_acceptance):
                current, current_lp = proposal, proposal_lp
                if iteration >= burn_in:
                    accepted += 1
            if iteration >= burn_in:
                draws[stored] = current
                stored += 1

        self.samples = draws
        self.acceptance_rate = accepted / num_samples
        return draws

    def summary(self) -> dict[str, Array | float]:
        """Print and return compact posterior diagnostics."""
        if self.samples.size == 0:
            raise RuntimeError("sample() must be called before summary()")
        result = {
            "mean": self.samples.mean(axis=0),
            "std": self.samples.std(axis=0, ddof=1),
            "q05": np.quantile(self.samples, 0.05, axis=0),
            "median": np.quantile(self.samples, 0.50, axis=0),
            "q95": np.quantile(self.samples, 0.95, axis=0),
            "acceptance_rate": self.acceptance_rate,
        }
        print(f"Acceptance rate: {self.acceptance_rate:.3f}")
        for key in ("mean", "std", "q05", "median", "q95"):
            print(f"{key:>6}: {np.asarray(result[key])}")
        return result
