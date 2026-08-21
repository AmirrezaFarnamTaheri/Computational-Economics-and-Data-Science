### 2026-08-21 — Klein QZ Solver Rank Condition & Notebook License URLs
- **Symptom:** Potential division by zero / singularity when Z11 is non-invertible in Klein QZ solver; notebook badges in subdirectories breaking with relative LICENSE instead of ../LICENSE.
- **Wrong approach:** Blindly inverting Z11 without checking condition number; using top-level relative paths in subfolder notebooks.
- **Do:** Use condition number checks (1.0 / np.linalg.cond(Z11) < 1e-12) and np.linalg.solve(Z11.T, ...).T; use ../LICENSE in module notebooks.
- **Don't:** Allow singular state-blocks to fail silently or emit uncaught NaN policies.
- **Evidence:** tests/test_macro_utils.py::TestBlanchardKahn::test_raises_when_states_do_not_span_stable_subspace
