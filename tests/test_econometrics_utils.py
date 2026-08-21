from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "06-Econometrics" / "econometrics_utils.py"
spec = importlib.util.spec_from_file_location("econometrics_utils", PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
MCMCSampler = module.MCMCSampler


def test_mh_recovers_normal_mean():
    def log_posterior(x):
        return -0.5 * float(x) ** 2

    sampler = MCMCSampler(log_posterior, random_seed=7)
    draws = sampler.sample([0.5], num_samples=6000, burn_in=1000, step_size=0.8)
    assert draws.shape == (6000, 1)
    assert abs(float(draws.mean())) < 0.12
    assert 0.2 < sampler.acceptance_rate < 0.9


def test_invalid_start_is_rejected():
    sampler = MCMCSampler(lambda x: -np.inf)
    try:
        sampler.sample([0.0], num_samples=10)
    except ValueError as exc:
        assert "finite posterior" in str(exc)
    else:
        raise AssertionError("invalid initial state should fail")
