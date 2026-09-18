# High-Performance Python Cheat Sheet

> Quick reference for the High-Performance Python module. Details: [High Performance Computing](../notebooks/high_performance_python/01_High_Performance_Computing.md) (notebook).

## Core objects & dimensions

| Object | Notation | Cost model |
|---|---|---|
| Vectorized op | `np.dot`, `+`, `exp` | $O(n)$ flops at C speed |
| BLAS level 1/2/3 | axpy / gemv / gemm | $O(n)$ / $O(n^2)$ / $O(n^3)$ |
| Memory traffic | — | bandwidth-bound vs compute-bound |
| Parallel fraction | $p \in [0, 1]$ | scalar |

## Rules of thumb

- **Amdahl**: $S(n) = \dfrac{1}{(1-p) + p/n}$ — the serial fraction caps speedup at $1/(1-p)$ regardless of cores.
- Vectorize before parallelizing: NumPy elementwise beats Python loops by 10–100× with zero threading risk.
- `numba @njit`: first call pays LLVM compile cost (cache it); loops then run at C speed. Type-stable inputs required.
- Memory layout: row-major (C order): vary the last index (columns within a row) in the innermost loop; `np.ascontiguousarray` before hot loops.
- Chunking (Dask): pick chunks that fit comfortably in RAM (~100 MB) so workers never swap.
- Profile first (`cProfile`, `line_profiler`): optimize the 3% of code taking 97% of time.

## Decision ladder

1. Better algorithm (drop $O(n^2)$ to $O(n \log n)$) →
2. Vectorize with NumPy/pandas →
3. JIT-compile hot loops (`numba`) →
4. Parallelize across cores (`joblib`, `dask`) →
5. Only then reach for GPUs/clusters.

## Complexity quick table

| Pattern | Naive Python | Vectorized/Numba |
|---|---|---|
| Elementwise math on $n$ floats | $O(n)$, huge constant | $O(n)$, small constant |
| Pairwise distances | $O(n^2 d)$ loops | $O(n^2 d)$ BLAS |
| Rolling statistic | $O(nw)$ loop | $O(n)$ sliding tricks |
| Monte Carlo $N$ paths | embarrassingly parallel | batch by array |
