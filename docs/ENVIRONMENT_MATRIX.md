# Environment and Capability Matrix

This repository intentionally has more than one execution surface. The files below are **not interchangeable lockfiles**; each serves a different scope.

| Surface | Python | Dependency source | CI coverage | Intended use |
|---|---:|---|---|---|
| Deterministic core | 3.13 | `environment.lock.yml` | `deterministic-execution` | Dependency-light notebooks that must execute top-to-bottom, offline, on every PR. |
| Test suite | 3.13 | `requirements-test.txt` | `test` | Repository tests and audit fixtures; deliberately excludes heavy curriculum stacks. |
| Static quality/docs | 3.11 | CI-installed Ruff/Black/MkDocs tools | `lint`, `validate-notebooks`, `docs-strict` | Formatting, static notebook audits, generated-page parity, documentation build. |
| Full local curriculum | 3.13 | `environment.yml` | installation surface is documented; individual optional stacks are guarded/smoke-tested rather than all executed in one CI image | Broadest supported local course environment. |
| pip-oriented full curriculum | >=3.11, with 3.13 the reference release environment | `requirements.txt` | dependency compatibility is checked through targeted jobs rather than a single monolithic run | Users who prefer pip/venv to Conda. |
| Hardware/provider-specific lessons | varies within the supported Python range | notebook-specific optional dependencies | capability manifest / optional smoke checks; GPU work requires a compatible runner | GPU, network-service, large-data, or provider-specific demonstrations. |

## Canonical rules

1. **`environment.lock.yml` is the deterministic CI contract.** It pins direct dependencies for the offline execution lane. It does not claim to be a fully resolved transitive lock for the entire curriculum.
2. **`requirements-test.txt` is intentionally smaller.** Passing the test suite does not imply TensorFlow, PyTorch, geospatial, Prophet, GPU, or provider-specific lessons are installed.
3. **`environment.yml` is the recommended full local environment.** It includes the broad optional stacks needed by the curriculum and is the default setup documented in the README.
4. **`requirements.txt` is the pip alternative.** It is intentionally broader and less tightly pinned than the deterministic lane because many heavy packages have platform-specific wheels and constraints.
5. **Notebook capability is explicit.** A lesson that needs an optional library, external service, GPU, or dataset must guard that dependency, state the requirement, and must not silently reinterpret a skipped demonstration as a successful empirical result.
6. **Offline deterministic notebooks must not acquire data at runtime.** They use committed datasets or small deterministic teaching fixtures.
7. **Framework reproducibility is scoped.** Seeds control supported stochastic boundaries; they do not promise bit-for-bit equality across different hardware, BLAS libraries, GPU kernels, or package versions.

## Installation paths

### Recommended full course environment

```bash
mamba env create -f environment.yml
conda activate computational-economics
jupyter lab
```

### Deterministic CI-compatible core

```bash
conda env create -f environment.lock.yml
conda activate computational-economics-lock
```

### pip alternative

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## What “supported” means

A capability is **verified** only to the level of its owning lane. Static validation, a successful import smoke test, top-to-bottom notebook execution, a saved-output publishing check, and a GPU benchmark are different levels of evidence. The CI names and notebook capability inventory should therefore be read literally rather than collapsed into a single “everything works everywhere” claim.
