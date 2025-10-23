import random
import numpy as np
from numba import njit, prange
import timeit

def monte_carlo_pi_python(num_samples):
    acc = 0
    for _ in range(num_samples):
        x = random.random()
        y = random.random()
        if (x**2 + y**2) < 1.0:
            acc += 1
    return 4.0 * acc / num_samples

@njit
def monte_carlo_pi_numba(num_samples):
    acc = 0
    for _ in range(num_samples):
        x = random.random()
        y = random.random()
        if (x**2 + y**2) < 1.0:
            acc += 1
    return 4.0 * acc / num_samples

def sum_of_squares_python(arr):
    total = 0.0
    for i in range(arr.shape[0]):
        total += arr[i] ** 2
    return total

@njit
def sum_of_squares_numba(arr):
    total = 0.0
    for i in range(arr.shape[0]):
        total += arr[i] ** 2
    return total

@njit(parallel=True)
def sum_of_squares_parallel(arr):
    total = 0.0
    # prange indicates this loop can be parallelized
    for i in prange(arr.shape[0]):
        total += arr[i] ** 2
    return total

num_samples = 10_000_000
my_array = np.random.randn(10_000_000)

print("--- Benchmarking Monte Carlo Pi ---")
py_time = timeit.timeit(lambda: monte_carlo_pi_python(num_samples), number=1)
print(f"Python time: {py_time:.4f}s")

# The first run compiles the function
monte_carlo_pi_numba(1)
numba_time = timeit.timeit(lambda: monte_carlo_pi_numba(num_samples), number=1)
print(f"Numba time: {numba_time:.4f}s")
print(f"Speedup: {py_time / numba_time:.1f}x")

print("\\n--- Benchmarking Sum of Squares ---")
py_time = timeit.timeit(lambda: sum_of_squares_python(my_array), number=1)
print(f"Python time: {py_time:.4f}s")

sum_of_squares_numba(my_array) # Warm-up
numba_time = timeit.timeit(lambda: sum_of_squares_numba(my_array), number=100)
print(f"Numba time: {numba_time / 100:.4f}s")
print(f"Speedup: {py_time / (numba_time / 100):.1f}x")

sum_of_squares_parallel(my_array) # Warm-up
parallel_time = timeit.timeit(lambda: sum_of_squares_parallel(my_array), number=100)
print(f"Parallel Numba time: {parallel_time / 100:.4f}s")
print(f"Speedup vs. Python: {(py_time / (parallel_time / 100)):.1f}x")
