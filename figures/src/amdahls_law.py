#!/usr/bin/env python3
"""Amdahl's law: speedup bound as a function of parallel fraction and cores.

Target lecture: high_performance_python/01_High_Performance_Computing.ipynb
(Amdahl's Law section).
Run:  python figures/src/amdahls_law.py
  ->  images/high_performance_python/amdahls_law.png

Pure mathematics (S(n) = 1 / ((1-p) + p/n)); no timing data involved.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = (
    Path(__file__).resolve().parents[2]
    / "images"
    / "high_performance_python"
    / "amdahls_law.png"
)


def main() -> None:
    n = np.arange(1, 65)
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    for p, color in ((0.95, "#2e7d32"), (0.90, "#48688a"), (0.75, "#b03a2e")):
        speedup = 1.0 / ((1 - p) + p / n)
        ax.plot(n, speedup, lw=2.0, color=color, label=f"parallel share p = {p:.2f}")
        ax.axhline(1 / (1 - p), color=color, lw=0.8, ls=":", alpha=0.6)
    ax.set_xlabel("number of cores $n$")
    ax.set_ylabel("speedup $S(n)$")
    ax.set_xlim(1, 64)
    ax.set_ylim(0, 21)
    ax.set_title("Amdahl's law: the serial fraction caps the speedup")
    ax.legend(frameon=False, loc="upper left", fontsize=9)
    fig.tight_layout()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=150)
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
