# Foundations Cheat Sheet

> Quick reference for Module 01. Formulas follow the [notation glossary](../resources/notation.md); every object carries its dimensions. Details: [Python Fundamentals](../modules/01-foundations/03-python-fundamentals.md), [NumPy & Pandas](../modules/01-foundations/12-13-numpy-pandas.md).

## Core objects & dimensions

| Object | Notation | Dimensions / cost |
|---|---|---|
| NumPy array | `A` | shape `(n_1, ..., n_d)`; contiguous C-order |
| Vector | $\mathbf{x}$ | shape `(n,)` — neither row nor column |
| Matrix | $\mathbf{X}$ | shape `(n, k)` |
| `list` | — | append O(1); insert/delete at 0 O(n) |
| `dict` / `set` | — | avg lookup/insert O(1); worst O(n) collisions |
| `tuple` | — | immutable, hashable if contents are |

## Key facts & formulas

- **Machine epsilon**: $\varepsilon_{mach} = 2^{-52} \approx 2.22\times 10^{-16}$ (float64). Never test float equality: use `math.isclose(a, b, rel_tol=...)`.
- **Integer overflow**: NumPy ints wrap silently; pandas ints upcast to float on `NaN` (use nullable `Int64`).
- **Views vs copies**: basic slicing returns a *view* (mutating it mutates the base); fancy indexing returns a *copy*.
- **Broadcasting**: shapes align right; dims match if equal or one of them is 1. `(n,) + (n,1) -> (n,n)` — usually a bug.
- **Aliasing**: `b = a` copies the *reference*; `copy.deepcopy` for nested structures.
- **Closures bind late**: `[lambda: i for i in range(3)]` all see the final `i`; fix with `lambda i=i: i`.

## Vectorization & complexity

| Operation | Cost | Notes |
|---|---|---|
| Python loop over $10^7$ floats | seconds | interpreter overhead dominates |
| NumPy elementwise on same data | ~10–100× faster | single pass in C |
| `df.iterrows()` | O(n) with huge constant | avoid; use vectorized column ops |
| `df.merge` | O(n + m) hash | beware many-to-many row explosion |

## Gotcha checklist

1. `==` on floats; 2. `is` on values; 3. mutable default arguments; 4. chained indexing assignment; 5. mutating a list/dict while iterating.
