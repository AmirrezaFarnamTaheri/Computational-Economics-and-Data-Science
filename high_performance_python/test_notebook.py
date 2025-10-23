# === Environment Setup ===
import os, sys, math, time, random, json, textwrap, warnings, timeit
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
try:
    from numba import njit, prange, vectorize
    NUMBA_AVAILABLE = True
except ImportError:
    def njit(func=None, **kwargs): return func if func else lambda f: f
    def prange(*args, **kwargs): return range(*args, **kwargs)
    def vectorize(func=None, **kwargs): return np.vectorize(func) if func else lambda f: np.vectorize(f)
    NUMBA_AVAILABLE = False
try:
    import dask
    from dask import delayed
    DASK_AVAILABLE = True
except ImportError:
    DASK_AVAILABLE = False
import multiprocessing as mp
from IPython.display import display, Markdown

# --- Configuration ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'font.size': 14, 'figure.figsize': (12, 8), 'figure.dpi': 150})
np.set_printoptions(suppress=True, linewidth=120, precision=4)

# --- Utility Functions ---
def note(msg): print(f"Note: {msg}")
def sec(title): print(f"\\n{80*'='}\\n| {title.upper()} |\\n{80*'='}")

note("Environment initialized for High-Performance Computing.")

sec("Numba for Accelerating Loops: A Monte Carlo Example")

def monte_carlo_pi_python(n_samples):
    acc = 0
    for i in range(n_samples):
        x, y = random.random(), random.random()
        if x**2 + y**2 < 1.0: acc += 1
    return 4.0 * acc / n_samples

@njit(parallel=True, cache=True)
def monte_carlo_pi_numba(n_samples):
    acc = 0
    for i in prange(n_samples):
        x, y = np.random.rand(), np.random.rand()
        if x**2 + y**2 < 1.0: acc += 1
    return 4.0 * acc / n_samples

n = 10_000_000
if NUMBA_AVAILABLE:
    py_time = timeit.timeit(lambda: monte_carlo_pi_python(n), number=1)
    # Warm up Numba
    monte_carlo_pi_numba(1)
    numba_time = timeit.timeit(lambda: monte_carlo_pi_numba(n), number=1)
    note(f"Numba provides a {py_time / numba_time:.1f}x speedup over pure Python for this task.")

sec("Parallelism with Multiprocessing")

# This function must be defined at the top level of the module to be pickleable
def run_simulation(params):
    sim_id, alpha, beta = params
    result = 0
    for i in range(1_000_000): result += np.sin(i * alpha) * np.cos(i * beta)
    return sim_id, result

if __name__ == '__main__':
    param_grid = [(i, alpha, beta) for i, (alpha, beta) in enumerate(np.random.rand(8, 2))]
    note(f"Running a parameter sweep with {len(param_grid)} simulations...")

    start_time = time.time()
    with mp.Pool(processes=4) as pool:
        results = pool.map(run_simulation, param_grid)
    end_time = time.time()
    note(f"Multiprocessing execution time: {end_time - start_time:.2f}s")

sec("GPU Acceleration Example: NumPy vs. CuPy")
try:
    import cupy as cp
    CUPY_AVAILABLE = True
except ImportError:
    CUPY_AVAILABLE = False

if CUPY_AVAILABLE:
    # Create large random matrices on both CPU (NumPy) and GPU (CuPy)
    size = 4000
    np_A, np_B = np.random.rand(size, size), np.random.rand(size, size)
    cp_A, cp_B = cp.asarray(np_A), cp.asarray(np_B)

    note(f"Timing matrix multiplication for a {size}x{size} matrix...")
    # Time NumPy
    numpy_time = timeit.timeit(lambda: np_A @ np_B, number=10)
    # Time CuPy (after a warm-up)
    cp.cuda.runtime.deviceSynchronize() # Synchronize to get accurate timing
    cupy_time = timeit.timeit(lambda: cp_A @ cp_B, number=10)
    cp.cuda.runtime.deviceSynchronize()

    print(f"NumPy (CPU) time: {numpy_time:.4f} seconds")
    print(f"CuPy (GPU) time:  {cupy_time:.4f} seconds")
    print(f"GPU Speedup:      {numpy_time / cupy_time:.1f}x")
else:
    note("CuPy is not installed or no compatible GPU is found. Skipping GPU example.")

sec("Profiling with cProfile")
import cProfile, pstats

# Define two functions to simulate a workflow
def slow_function():
    # This function is deliberately slow
    time.sleep(0.1)
    [math.sqrt(i) for i in range(10**4)]

def fast_function():
    # This function is fast
    pass

def main_workflow():
    for _ in range(5):
        slow_function()
    for _ in range(100):
        fast_function()

# Create a profiler object and run it on our main function
profiler = cProfile.Profile()
profiler.enable()
main_workflow()
profiler.disable()

# Print the stats
stats = pstats.Stats(profiler).sort_stats('cumulative')
stats.print_stats(10) # Print the top 10 offenders
note("The profiler output clearly shows that nearly all the execution time is spent inside `slow_function`, making it the obvious target for optimization efforts.")
