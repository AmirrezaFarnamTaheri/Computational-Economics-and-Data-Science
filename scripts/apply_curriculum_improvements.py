"""One-time, idempotent curriculum normalization and repair pass.

This script applies the repository-wide invariants agreed in the reconciled 2026
curriculum plan. It intentionally limits broad automated edits to changes that are
mechanical and reviewable: metadata/badges, section presence, learning-path links,
reference blocks, equation review boxes, cell IDs, and a small set of confirmed
broken code cells. Content-heavy frontier additions live in
``scripts/create_frontier_notebooks.py``.
"""
from __future__ import annotations

import hashlib
import re
from pathlib import Path
from urllib.parse import quote

import nbformat
from nbformat.v4 import new_markdown_cell

ROOT = Path(__file__).resolve().parents[1]
REPO = "AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science"

MODULE_LABELS = {
    "01-Foundations": "Foundations",
    "02-Numerical-Methods": "Numerical Methods",
    "03-Economic-Modeling": "Economic Modeling",
    "04-Macro-Models": "Macroeconomic Models",
    "05-Micro-Models": "Microeconomic Models",
    "06-Econometrics": "Econometrics",
    "07-Machine-Learning": "Machine Learning",
    "08-Time-Series": "Time Series",
    "09-Finance": "Finance",
    "10-Specialized-Models": "Specialized Models",
    "Appendix": "Mathematical & Tooling Appendix",
    "high_performance_python": "High-Performance Python",
}

MODULE_REFERENCES = {
    "01-Foundations": [
        "Python Software Foundation. *Python 3 Documentation*.",
        "Harris, C. R. et al. (2020). Array programming with NumPy. *Nature*, 585, 357–362.",
        "McKinney, W. (2022). *Python for Data Analysis* (3rd ed.). O'Reilly.",
    ],
    "02-Numerical-Methods": [
        "Judd, K. L. (1998). *Numerical Methods in Economics*. MIT Press.",
        "Miranda, M. J. & Fackler, P. L. (2002). *Applied Computational Economics and Finance*. MIT Press.",
        "Nocedal, J. & Wright, S. J. (2006). *Numerical Optimization* (2nd ed.). Springer.",
    ],
    "03-Economic-Modeling": [
        "Stokey, N. L., Lucas, R. E. Jr. & Prescott, E. C. (1989). *Recursive Methods in Economic Dynamics*. Harvard University Press.",
        "Ljungqvist, L. & Sargent, T. J. (2018). *Recursive Macroeconomic Theory* (4th ed.). MIT Press.",
        "Rust, J. (1987). Optimal replacement of GMC bus engines: An empirical model of Harold Zurcher. *Econometrica*, 55(5), 999–1033.",
    ],
    "04-Macro-Models": [
        "Ljungqvist, L. & Sargent, T. J. (2018). *Recursive Macroeconomic Theory* (4th ed.). MIT Press.",
        "Galí, J. (2015). *Monetary Policy, Inflation, and the Business Cycle* (2nd ed.). Princeton University Press.",
        "Aiyagari, S. R. (1994). Uninsured idiosyncratic risk and aggregate saving. *Quarterly Journal of Economics*, 109(3), 659–684.",
    ],
    "05-Micro-Models": [
        "Mas-Colell, A., Whinston, M. D. & Green, J. R. (1995). *Microeconomic Theory*. Oxford University Press.",
        "Osborne, M. J. & Rubinstein, A. (1994). *A Course in Game Theory*. MIT Press.",
        "Train, K. E. (2009). *Discrete Choice Methods with Simulation* (2nd ed.). Cambridge University Press.",
    ],
    "06-Econometrics": [
        "Wooldridge, J. M. (2010). *Econometric Analysis of Cross Section and Panel Data* (2nd ed.). MIT Press.",
        "Angrist, J. D. & Pischke, J.-S. (2009). *Mostly Harmless Econometrics*. Princeton University Press.",
        "Imbens, G. W. & Rubin, D. B. (2015). *Causal Inference for Statistics, Social, and Biomedical Sciences*. Cambridge University Press.",
    ],
    "07-Machine-Learning": [
        "Hastie, T., Tibshirani, R. & Friedman, J. (2009). *The Elements of Statistical Learning* (2nd ed.). Springer.",
        "James, G., Witten, D., Hastie, T., Tibshirani, R. & Taylor, J. (2023). *An Introduction to Statistical Learning with Applications in Python*. Springer.",
        "Goodfellow, I., Bengio, Y. & Courville, A. (2016). *Deep Learning*. MIT Press.",
    ],
    "08-Time-Series": [
        "Hamilton, J. D. (1994). *Time Series Analysis*. Princeton University Press.",
        "Lütkepohl, H. (2005). *New Introduction to Multiple Time Series Analysis*. Springer.",
        "Hyndman, R. J. & Athanasopoulos, G. *Forecasting: Principles and Practice* (3rd ed.). OTexts.",
    ],
    "09-Finance": [
        "Cochrane, J. H. (2005). *Asset Pricing* (rev. ed.). Princeton University Press.",
        "Campbell, J. Y., Lo, A. W. & MacKinlay, A. C. (1997). *The Econometrics of Financial Markets*. Princeton University Press.",
        "Shreve, S. E. (2004). *Stochastic Calculus for Finance II*. Springer.",
    ],
    "10-Specialized-Models": [
        "Tesfatsion, L. & Judd, K. L. (eds.) (2006). *Handbook of Computational Economics, Vol. 2: Agent-Based Computational Economics*. Elsevier.",
        "Jackson, M. O. (2008). *Social and Economic Networks*. Princeton University Press.",
        "Acemoglu, D., Ozdaglar, A. & Tahbaz-Salehi, A. (2015). Systemic risk and stability in financial networks. *American Economic Review*, 105(2), 564–608.",
    ],
    "Appendix": [
        "Rudin, W. (1976). *Principles of Mathematical Analysis* (3rd ed.). McGraw-Hill.",
        "Axler, S. (2015). *Linear Algebra Done Right* (3rd ed.). Springer.",
        "Boyd, S. & Vandenberghe, L. (2004). *Convex Optimization*. Cambridge University Press.",
    ],
    "high_performance_python": [
        "Gorelick, M. & Ozsvald, I. (2020). *High Performance Python* (2nd ed.). O'Reilly.",
        "Numba project. *Numba Documentation*.",
        "Dask Development Team. *Dask Documentation*; CuPy Developers. *CuPy Documentation*.",
    ],
}

TOPIC_REFERENCES: list[tuple[str, str]] = [
    ("difference_in_differences", "Callaway, B. & Sant'Anna, P. H. C. (2021). Difference-in-differences with multiple time periods. *Journal of Econometrics*, 225(2), 200–230."),
    ("difference_in_differences", "Sun, L. & Abraham, S. (2021). Estimating dynamic treatment effects in event studies with heterogeneous treatment effects. *Journal of Econometrics*, 225(2), 175–199."),
    ("causal_ml", "Chernozhukov, V. et al. (2018). Double/debiased machine learning for treatment and structural parameters. *The Econometrics Journal*, 21(1), C1–C68."),
    ("portfolio", "Ledoit, O. & Wolf, M. (2004). A well-conditioned estimator for large-dimensional covariance matrices. *Journal of Multivariate Analysis*, 88(2), 365–411."),
    ("option", "Carr, P. & Madan, D. (1999). Option valuation using the fast Fourier transform. *Journal of Computational Finance*, 2(4), 61–73."),
    ("structural_estimation", "Hotz, V. J. & Miller, R. A. (1993). Conditional choice probabilities and the estimation of dynamic models. *Review of Economic Studies*, 60(3), 497–529."),
    ("continuous_states", "Carroll, C. D. (2006). The method of endogenous gridpoints for solving dynamic stochastic optimization problems. *Economics Letters*, 91(3), 312–320."),
    ("heterogeneous_agent", "Auclert, A., Bardóczy, B., Rognlie, M. & Straub, L. (2021). Using the sequence-space Jacobian to solve and estimate heterogeneous-agent models. *Econometrica*, 89(5), 2375–2408."),
]


def text(cell) -> str:
    return cell.source if isinstance(cell.source, str) else "".join(cell.source)


def set_text(cell, value: str) -> None:
    cell.source = value.rstrip() + "\n"


def title_of(nb) -> str:
    for cell in nb.cells:
        if cell.cell_type == "markdown":
            match = re.search(r"(?m)^#\s+(.+?)\s*$", text(cell))
            if match:
                return re.sub(r"<.*?>", "", match.group(1)).strip()
    return "Untitled Notebook"


def module_of(path: Path) -> str:
    return path.relative_to(ROOT).parts[0]


def notebook_key(path: Path) -> str:
    return path.stem.lower().replace("-", "_")


def badges(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    encoded_path = quote(rel)
    colab = f"https://colab.research.google.com/github/{REPO}/blob/main/{encoded_path}"
    binder = f"https://mybinder.org/v2/gh/{REPO}/main?filepath={encoded_path}"
    return (
        f"[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)]({colab}) "
        f"[![Launch Binder](https://mybinder.org/badge_logo.svg)]({binder}) "
        "[![Code License: MIT](https://img.shields.io/badge/Code%20License-MIT-yellow.svg)](../LICENSE) "
        "[![Content License: CC BY 4.0](https://img.shields.io/badge/Content%20License-CC%20BY%204.0-blue.svg)](https://creativecommons.org/licenses/by/4.0/)"
    )


def ensure_badges(nb, path: Path) -> None:
    first_md = next((c for c in nb.cells if c.cell_type == "markdown"), None)
    if first_md is None:
        return
    lines = text(first_md).splitlines()
    badge_markers = (
        "Open in Colab",
        "Launch Binder",
        "Code License: MIT",
        "Content License: CC BY 4.0",
    )
    lines = [line for line in lines if not any(marker in line for marker in badge_markers)]
    title_idx = next((i for i, line in enumerate(lines) if re.match(r"^#\s+\S", line)), 0)
    before = lines[: title_idx + 1]
    after = lines[title_idx + 1 :]
    while after and not after[0].strip():
        after.pop(0)
    canonical = before + ["", badges(path)]
    if after:
        canonical += [""] + after
    # Collapse accidental runs of blank lines without touching prose.
    normalized: list[str] = []
    for line in canonical:
        if not line.strip() and normalized and not normalized[-1].strip():
            continue
        normalized.append(line)
    set_text(first_md, "\n".join(normalized))


def dedupe_finance_lens(nb) -> None:
    lens_indices = [
        i
        for i, c in enumerate(nb.cells)
        if c.cell_type == "markdown"
        and re.search(r"(?im)^\s*#{1,4}\s+The Lens\b", text(c))
    ]
    if len(lens_indices) <= 1:
        return
    # Prefer the richer Lens that includes objectives/prerequisites.
    keep = max(
        lens_indices,
        key=lambda i: (
            "Learning Objectives" in text(nb.cells[i]),
            "Prerequisites" in text(nb.cells[i]),
            len(text(nb.cells[i])),
        ),
    )
    for idx in reversed(lens_indices):
        if idx != keep:
            del nb.cells[idx]


def framing_for(module: str, title: str) -> str:
    frames = {
        "01-Foundations": (
            "The economic value of this topic is not the syntax itself but the reliability of the research workflow it enables. "
            "Small implementation choices determine whether a result can be reproduced, scaled to a panel or simulation, and audited by another researcher. "
            "As you work through the examples, ask which representation makes the economic object easiest to validate and which failure modes would silently change a quantitative conclusion."
        ),
        "02-Numerical-Methods": (
            "In economic computation, an algorithm is part of the model: convergence tolerances, conditioning, discretization, and stopping rules can alter the apparent equilibrium. "
            "The central question is therefore not merely whether a routine returns a number, but whether that number is stable under tighter tolerances, alternative initial conditions, and an independent method. "
            "Treat every numerical result as an approximation with a measurable error budget."
        ),
        "03-Economic-Modeling": (
            "Dynamic models convert economic incentives into a recursive computational object. The practical question is how an agent's current choice changes both today's payoff and tomorrow's feasible states. "
            "A trustworthy solution should make that mechanism visible through the Bellman equation, the policy rule, and a diagnostic such as a residual or Euler-equation error. "
            "Keep the economic state, control, transition law, and numerical approximation conceptually separate."
        ),
        "04-Macro-Models": (
            "Macroeconomic models are useful when their equilibrium restrictions can be traced from household and firm decisions to aggregate dynamics. "
            "The key question is which mechanism moves consumption, investment, employment, prices, or distributions after a shock or policy change—and which assumptions are responsible for that response. "
            "Comparative statics and impulse responses should therefore be read as disciplined counterfactuals, not as decorative plots."
        ),
        "05-Micro-Models": (
            "Microeconomic computation makes equilibrium and incentive constraints operational. "
            "The useful question is how preferences, technologies, information, or strategic beliefs map into choices and welfare, and whether the computed solution respects feasibility, optimality, and equilibrium conditions. "
            "Whenever multiple equilibria or corner solutions are possible, the numerical method should expose rather than hide that economic structure."
        ),
        "06-Econometrics": (
            "The computational task only has economic meaning after the estimand and identifying assumptions are explicit. "
            "Ask what variation identifies the parameter, which observations act as the comparison group, and what data-generating process would make the estimator fail. "
            "A good empirical workflow pairs the point estimate with diagnostics, uncertainty, and at least one falsification or sensitivity check so that precision is not confused with identification."
        ),
        "07-Machine-Learning": (
            "For economists, predictive performance is useful but not sufficient. The model must be evaluated against the decision or forecasting problem, the information set available at prediction time, and the cost of distribution shift or leakage. "
            "Ask what inductive bias the method introduces, how tuning choices are validated out of sample, and which errors matter economically. "
            "When the goal is causal or structural, prediction should be treated as a nuisance component rather than evidence of identification by itself."
        ),
        "08-Time-Series": (
            "Time-series methods exploit dependence across dates, so chronology is part of the data-generating process rather than a nuisance index. "
            "The central question is what can be learned from persistence, innovations, and cross-variable dynamics without leaking future information into the past. "
            "Model adequacy must therefore be judged through residual diagnostics, stability, and genuinely out-of-sample forecasting or structural restrictions."
        ),
        "09-Finance": (
            "Financial models connect prices to risk, timing, and no-arbitrage restrictions. "
            "The economic question is which states of the world make a payoff valuable, how risk is transferred or hedged, and how sensitive the valuation is to assumptions about dynamics and market completeness. "
            "A numerical price is credible only when it respects basic bounds, limiting cases, and an independent replication or hedging argument."
        ),
        "10-Specialized-Models": (
            "Complex systems are valuable precisely when aggregate behavior cannot be read off from a representative agent. "
            "The question is how local rules, network structure, heterogeneity, or feedback create macro-level patterns and whether those patterns are robust to alternative micro assumptions. "
            "Simulation should therefore be paired with mechanism tests, sensitivity analysis, and statistics that distinguish genuine emergence from a coding artifact."
        ),
        "Appendix": (
            "This mathematical result earns its place in the curriculum because later economic arguments rely on its hypotheses, not only its conclusion. "
            "As you read each derivation, track which assumption licenses each step and construct a counterexample when an assumption is removed. "
            "The objective is to make the theorem usable as a diagnostic tool in optimization, probability, econometrics, or dynamic models rather than a formula to memorize."
        ),
        "high_performance_python": (
            "Performance matters when computation changes which economic questions are feasible to ask. "
            "The relevant objective is not a synthetic speedup alone but lower time-to-solution at fixed numerical accuracy and reproducibility. "
            "Benchmark with representative problem sizes, separate compilation or transfer overhead from steady-state work, and verify that the optimized implementation agrees with a clear reference calculation."
        ),
    }
    return (
        f"\n\n**Economic question.** In *{title}*, what must remain economically invariant when the computational representation changes? "
        + frames[module]
    )


def standardize_and_expand_lens(nb, path: Path) -> None:
    module = module_of(path)
    title = title_of(nb)
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue
        src = text(cell)
        m = re.search(r"(?im)^\s*#{1,4}\s+The Lens(?::\s*([^\n]+))?\s*$", src)
        if not m:
            continue
        subtitle = (m.group(1) or title).strip()
        src = src[: m.start()] + f"## The Lens: {subtitle}" + src[m.end() :]
        # Measure only the prose before objectives/prerequisites/next major section.
        lens_start = re.search(r"(?im)^## The Lens:[^\n]*\n", src)
        if lens_start:
            tail = src[lens_start.end() :]
            stop = re.search(r"(?im)^#{2,3}\s+(?:Learning Objectives|Prerequisites|Table of Contents|\d+\.)", tail)
            lens_body = tail[: stop.start()] if stop else tail
            words = re.findall(r"\b[\w'-]+\b", re.sub(r"[$*_>`#]", " ", lens_body))
            if len(words) < 150 and "**Economic question.**" not in lens_body:
                insertion = framing_for(module, title)
                if stop:
                    tail = tail[: stop.start()] + insertion + "\n\n" + tail[stop.start() :]
                else:
                    tail += insertion
                src = src[: lens_start.end()] + tail
        set_text(cell, src)
        break


def add_hpp_objectives_prereqs(nb, path: Path) -> None:
    if module_of(path) != "high_performance_python":
        return
    md = "\n".join(text(c) for c in nb.cells if c.cell_type == "markdown")
    if re.search(r"(?im)^#{2,4}\s+Learning Objectives\b", md):
        return
    title = title_of(nb)
    lens = next(
        (c for c in nb.cells if c.cell_type == "markdown" and "The Lens" in text(c)),
        None,
    )
    if lens is None:
        return
    block = f"""

### Learning Objectives
- **Measure** the performance bottleneck in {title} before optimizing it.
- **Implement** a faster version while preserving a simple reference implementation.
- **Separate** setup/compilation/transfer overhead from steady-state execution time.
- **Validate** numerical equivalence and explain when the optimization is economically worthwhile.

### Prerequisites
- **`../01-Foundations/12_NumPy.ipynb`**: vectorized arrays, broadcasting, and memory layout.
- **`../01-Foundations/23_Profiling_and_Performance.ipynb`**: profiling and benchmark discipline.
- Familiarity with functions, NumPy, and reproducible timing experiments.
"""
    set_text(lens, text(lens).rstrip() + block)


def ensure_learning_path(nb, path: Path, prev_path: Path | None, next_path: Path | None) -> None:
    if any("**Learning path:**" in text(c) for c in nb.cells if c.cell_type == "markdown"):
        return
    parts = []
    if prev_path:
        parts.append(f"Building on [`{prev_path.name}`]({prev_path.name})")
    else:
        parts.append("This notebook is the entry point for this track")
    if next_path:
        parts.append(f"next continue with [`{next_path.name}`]({next_path.name})")
    else:
        parts.append("this notebook closes the current track")
    note = "> **Learning path:** " + "; ".join(parts) + "."
    # Put after the Lens/objectives/prerequisites cell so it is visible before the body.
    lens_idx = next(
        (
            i
            for i, c in enumerate(nb.cells)
            if c.cell_type == "markdown" and re.search(r"(?im)^## The Lens\b", text(c))
        ),
        None,
    )
    if lens_idx is not None:
        nb.cells.insert(lens_idx + 1, new_markdown_cell(note))


def ensure_filename_prerequisite(nb, path: Path, prev_path: Path | None) -> None:
    if prev_path is None:
        return
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue
        src = text(cell)
        if re.search(r"(?im)^#{2,4}\s+Prerequisites\b", src):
            if prev_path.name not in src:
                src = src.rstrip() + f"\n* **Learning-path prerequisite:** [`{prev_path.name}`]({prev_path.name})\n"
                set_text(cell, src)
            return


def exercise_block(module: str, title: str, topics: list[str]) -> str:
    focus = ", ".join(topics[:2]) if topics else title
    if module in {"03-Economic-Modeling", "04-Macro-Models"}:
        qs = [
            f"State the equilibrium/optimality condition that organizes **{title}**. Explain which assumption guarantees existence, uniqueness, or stability, and identify a limiting case where that argument weakens.",
            f"Reproduce one quantitative result from the sections on {focus}. Change one economically meaningful parameter over a defensible grid, report the policy/value/equilibrium response, and verify convergence with a residual or tighter tolerance.",
            "Design a policy or shock counterfactual that changes one mechanism at a time. Compare welfare or transition dynamics against the baseline and explain which conclusion is structural versus calibration-specific.",
        ]
    elif module == "05-Micro-Models":
        qs = [
            f"Write the optimization or equilibrium problem underlying **{title}** and derive its first-order, incentive, or market-clearing conditions. Discuss any relevant corner solution.",
            f"Construct a small numerical example using {focus}. Verify feasibility and optimality/equilibrium conditions numerically rather than relying only on the solver status.",
            "Relax one substantive assumption—information, convexity, symmetry, commitment, or market completeness—and predict how equilibrium or welfare changes before computing the extension.",
        ]
    elif module == "06-Econometrics":
        qs = [
            f"Define the estimand in **{title}**, list the identifying assumptions, and give a concrete data-generating process that violates one assumption while leaving the others intact.",
            f"Implement or reproduce the estimator using the material on {focus}. Report uncertainty and at least two diagnostics; then compare with an alternative specification that targets the same estimand.",
            "Run a Monte Carlo or sensitivity exercise that varies the most fragile identifying condition. Quantify bias/coverage or the range of estimates and state what evidence would change your substantive conclusion.",
        ]
    elif module == "07-Machine-Learning":
        qs = [
            f"Explain the loss/objective and inductive bias of **{title}**. Distinguish optimization error, estimation error, and generalization error in the economic use case.",
            f"Build a leakage-safe validation experiment using {focus}. Compare a simple baseline with the featured method using an economically relevant metric and report uncertainty across folds or seeds.",
            "Stress-test the model under temporal, subgroup, or covariate distribution shift. Identify which performance degradation matters for the downstream economic decision and propose one mitigation without using the test set for tuning.",
        ]
    elif module == "08-Time-Series":
        qs = [
            f"For **{title}**, identify the stochastic assumptions that make the model estimable and state how stationarity, invertibility, or identification can be checked from the fitted object.",
            f"Fit the method covered in {focus} to a time-ordered series. Diagnose residual dependence and stability, then evaluate a rolling or expanding-window out-of-sample forecast against a naive baseline.",
            "Alter one structural restriction, lag/order choice, or innovation distribution. Explain how impulse responses, forecasts, or uncertainty change and whether the conclusion survives the alternative specification.",
        ]
    elif module == "09-Finance":
        qs = [
            f"Derive the no-arbitrage, optimality, or risk-pricing relation central to **{title}** and verify that it satisfies at least two economically meaningful limiting cases or bounds.",
            f"Reproduce a calculation from {focus} with transparent inputs. Perturb volatility, discounting, risk aversion, transaction costs, or another key parameter and explain the sensitivity in economic terms.",
            "Construct a stress scenario outside the calibration sample. Compare two valuation/risk methods and explain which discrepancy reflects model risk rather than numerical error.",
        ]
    elif module == "Appendix":
        qs = [
            f"Restate one theorem used in **{title}** with every hypothesis explicit. Prove one non-trivial step that is often skipped and explain where that step is used later in the curriculum.",
            f"Work a concrete example from {focus} by hand and verify it computationally. Show the intermediate algebra, not only the final result.",
            "Remove one hypothesis and construct a counterexample or boundary case. Explain exactly which line of the original proof fails and what weaker conclusion, if any, remains.",
        ]
    elif module == "high_performance_python":
        qs = [
            f"Build a baseline for **{title}** and predict its time and memory complexity before benchmarking. State which measurement would falsify your performance hypothesis.",
            f"Optimize the workload using {focus}. Report warm-up separately from steady-state timing, use multiple repetitions, and verify numerical equivalence to the baseline.",
            "Scale the workload until the bottleneck changes (compute, memory bandwidth, serialization, transfer, or scheduler overhead). Identify the crossover point and recommend when the optimization should not be used.",
        ]
    else:
        qs = [
            f"Explain the central computational idea in **{title}** and connect it to one explicit economic object or research workflow.",
            f"Reproduce an example involving {focus}, then change one input and explain the result before running the code.",
            "Extend the example to a larger or less convenient case and document the correctness and performance checks needed before trusting the result.",
        ]
    return (
        "## Exercises\n\n"
        f"**1. Mechanism and assumptions (Conceptual):** {qs[0]}\n\n"
        f"**2. Reproduce and diagnose (Applied):** {qs[1]}\n\n"
        f"**3. Robust extension (Challenge):** {qs[2]}\n\n"
        "<details>\n<summary>Solution guidance</summary>\n\n"
        "A strong solution states assumptions before computation, includes an independent diagnostic or limiting-case check, and interprets the result in the units of the economic problem. For the challenge, separate changes caused by the economic assumption from changes caused by numerical approximation or tuning.\n\n"
        "</details>"
    )


def headings(nb) -> list[str]:
    out = []
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue
        for line in text(cell).splitlines():
            m = re.match(r"^#{2,4}\s+(.+)$", line.strip())
            if not m:
                continue
            h = re.sub(r"<.*?>", "", m.group(1)).strip()
            if not re.search(r"lens|learning objectives|prereq|table of contents|summary|exercise|reference", h, re.I):
                out.append(h)
    return out


def has_heading(nb, pattern: str) -> bool:
    return any(
        c.cell_type == "markdown" and re.search(pattern, text(c), re.I | re.M)
        for c in nb.cells
    )


def insert_before_end_sections(nb, cell) -> None:
    idx = len(nb.cells)
    for i, c in enumerate(nb.cells):
        if c.cell_type != "markdown":
            continue
        if re.search(r"(?im)^\s*#{1,4}\s+.*(?:Summary|Key Takeaways|Exercises|Problem Set|References|Further Reading)\b", text(c)):
            idx = i
            break
    nb.cells.insert(idx, cell)


def cleanup_generated_exercise_duplicates(nb) -> None:
    marker = "**1. Mechanism and assumptions (Conceptual):**"
    generated = [
        i
        for i, c in enumerate(nb.cells)
        if c.cell_type == "markdown"
        and marker in text(c)
        and re.search(r"(?im)^\s*##\s+Exercises\b", text(c))
    ]
    if not generated:
        return
    other = [
        i
        for i, c in enumerate(nb.cells)
        if c.cell_type == "markdown"
        and marker not in text(c)
        and re.search(r"(?im)^\s*#{1,4}\s+.*(?:Exercises?|Problem Sets?)\b", text(c))
    ]
    if other:
        remove = set(generated)
    else:
        remove = set(generated[1:])
    nb.cells = [c for i, c in enumerate(nb.cells) if i not in remove]


def ensure_exercises(nb, path: Path) -> None:
    if has_heading(nb, r"^\s*#{1,4}\s+.*(?:Exercises?|Problem Sets?)\b"):
        return
    insert_before_end_sections(
        nb,
        new_markdown_cell(exercise_block(module_of(path), title_of(nb), headings(nb))),
    )


def ensure_exercise_tiers(nb, path: Path) -> None:
    """Ensure every lecture exposes an explicit Conceptual/Applied/Challenge ladder.

    Existing exercises are preserved. When their labels do not make the three-tier
    progression explicit, append a short, notebook-specific ladder before the
    summary instead of rewriting instructor-authored problems.
    """
    markdown = "\n".join(text(c) for c in nb.cells if c.cell_type == "markdown")
    if all(re.search(rf"\b{label}\b", markdown, re.I) for label in ("Conceptual", "Applied", "Challenge")):
        return
    generated = exercise_block(module_of(path), title_of(nb), headings(nb))
    body = generated.split("\n\n", 1)[1]
    body = body.split("<details>", 1)[0].rstrip()
    block = (
        "### Three-Tier Practice Ladder\n\n"
        + body
        + "\n\n> Use the existing exercises above when they target the same skill; this ladder makes the intended progression explicit rather than replacing instructor-authored problems."
    )
    insert_before_end_sections(nb, new_markdown_cell(block))


def summary_block(module: str, title: str, topics: list[str]) -> str:
    topic_text = ", ".join(topics[:3]) if topics else "the central method"
    return f"""## Summary & Key Takeaways

- **Object:** *{title}* turns an economic or statistical question into an explicit mathematical/computational object rather than a black-box routine.
- **Mechanism:** The core sections on {topic_text} should be read as a chain from assumptions to equations to executable implementation.
- **Verification:** A computed answer is not sufficient; use residuals, diagnostics, limiting cases, out-of-sample checks, or an independent method as appropriate to this module.
- **Interpretation:** Report results in economic units and distinguish changes in the model's mechanism from changes caused by tuning, discretization, or numerical tolerance.
- **Reproducibility:** Keep seeds, data provenance, software requirements, and parameter choices explicit enough for another reader to reproduce the result.
"""


def ensure_summary(nb, path: Path) -> None:
    if has_heading(nb, r"^\s*#{1,4}\s+.*(?:Summary|Key Takeaways)\b"):
        return
    # Before references if present; otherwise append after exercises.
    idx = len(nb.cells)
    for i, c in enumerate(nb.cells):
        if c.cell_type == "markdown" and re.search(r"(?im)^\s*#{1,4}\s+.*(?:References|Further Reading)\b", text(c)):
            idx = i
            break
    nb.cells.insert(idx, new_markdown_cell(summary_block(module_of(path), title_of(nb), headings(nb))))


def refs_for(path: Path) -> list[str]:
    module = module_of(path)
    refs = list(MODULE_REFERENCES[module])
    key = notebook_key(path)
    for marker, ref in TOPIC_REFERENCES:
        if marker in key:
            refs.append(ref)
    return refs


def ensure_references(nb, path: Path) -> None:
    if has_heading(nb, r"^\s*#{1,4}\s+.*(?:References|Further Reading)\b"):
        return
    refs = refs_for(path)
    block = "## References & Further Reading\n\n" + "\n".join(f"- {r}" for r in refs)
    nb.cells.append(new_markdown_cell(block))


def display_equations(nb) -> list[str]:
    equations: list[str] = []
    seen = set()
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue
        for eq in re.findall(r"\$\$(.+?)\$\$", text(cell), flags=re.S):
            eq = re.sub(r"\s+", " ", eq.strip())
            if 12 <= len(eq) <= 500 and eq not in seen and "begin{aligned}" not in eq:
                seen.add(eq)
                equations.append(eq)
    return equations


def ensure_key_equations(nb, path: Path) -> None:
    module = module_of(path)
    if module in {"01-Foundations", "high_performance_python"}:
        return
    if module == "Appendix" and not path.name.startswith("A"):
        return
    if has_heading(nb, r"^\s*#{1,4}\s+Key Equations\b"):
        return
    eqs = display_equations(nb)[:4]
    if len(eqs) < 3:
        return
    block = [
        "## Key Equations",
        "",
        "These relations are collected from the derivations above as a review map. Their assumptions and derivations remain part of the result; this box is not a substitute for them.",
        "",
    ]
    for i, eq in enumerate(eqs, 1):
        block.extend([f"**{i}. Core relation**", "", f"$${eq}$$", ""])
    insert_before_end_sections(nb, new_markdown_cell("\n".join(block)))


def remove_blanket_warning_suppression(nb) -> None:
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        src = text(cell)
        new = re.sub(
            r"(?m)^\s*warnings\.filterwarnings\(\s*['\"]ignore['\"]\s*\)\s*\n?",
            "",
            src,
        )
        if new != src:
            set_text(cell, new)


def replace_source_matching(nb, needle: str, replacement: str) -> None:
    for cell in nb.cells:
        if cell.cell_type == "code" and needle in text(cell):
            set_text(cell, replacement)
            return
    return False


def confirmed_code_repairs(nb, path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "03-Economic-Modeling/01_Dynamic_Programming.ipynb":
        replacement = '''@njit\ndef policy_function_iteration(R, Q, beta, tol=1e-8, max_iter=100):\n    """Solve the discrete DP by exact policy evaluation and improvement.\n\n    The state is ``(asset_index, exogenous_state)`` and an action selects the\n    next asset index. ``Q[0, :, 0, :]`` contains the exogenous transition\n    matrix used throughout this notebook. Policy evaluation solves\n    ``(I - beta P_pi) V_pi = r_pi`` exactly, then the greedy step improves the\n    policy.\n    """\n    n_a, n_y, _, _ = Q.shape\n    n_states = n_a * n_y\n    P_trans = Q[0, :, 0, :]\n    policy = np.zeros((n_a, n_y), dtype=np.int32)\n    V = np.zeros((n_a, n_y))\n\n    for _ in range(max_iter):\n        # Exact policy evaluation.\n        transition = np.zeros((n_states, n_states))\n        rewards = np.empty(n_states)\n        for a_now in range(n_a):\n            for y_now in range(n_y):\n                row = a_now * n_y + y_now\n                a_next = policy[a_now, y_now]\n                rewards[row] = R[a_now, y_now, a_next]\n                for y_next in range(n_y):\n                    col = a_next * n_y + y_next\n                    transition[row, col] = P_trans[y_now, y_next]\n\n        lhs = np.eye(n_states) - beta * transition\n        V_new = np.linalg.solve(lhs, rewards).reshape((n_a, n_y))\n\n        # Greedy policy improvement.\n        expected_value = V_new @ P_trans.T\n        policy_new = np.empty_like(policy)\n        for a_now in range(n_a):\n            for y_now in range(n_y):\n                q_values = R[a_now, y_now, :] + beta * expected_value[:, y_now]\n                policy_new[a_now, y_now] = np.argmax(q_values)\n\n        value_change = np.max(np.abs(V_new - V))\n        stable = np.array_equal(policy_new, policy)\n        V = V_new\n        policy = policy_new\n        if stable and value_change < tol:\n            break\n\n    return V, policy\n\nprint("Exact policy-function iteration algorithm compiled.")'''
        replace_source_matching(nb, "# ... (Implementation would go here)", replacement)

    elif rel == "06-Econometrics/02A_MLE_Principles_and_Geometry.ipynb":
        for cell in nb.cells:
            if cell.cell_type == "code" and text(cell).lstrip().startswith("## Implementation Note"):
                cell.cell_type = "markdown"
                cell.pop("execution_count", None)
                cell.pop("outputs", None)
                break

    elif rel == "06-Econometrics/02B_MLE_Optimization_and_Applications.ipynb":
        for cell in nb.cells:
            if cell.cell_type == "code" and "except:\n            pass" in text(cell):
                src = text(cell).replace(
                    "        except:\n            pass",
                    "        except (TypeError, AttributeError, IndexError):\n"
                    "            display(Markdown(\"> **Note:** Observation count is unavailable for this data container.\"))",
                )
                set_text(cell, src)

    elif rel == "07-Machine-Learning/06_Deep_Learning_Foundations.ipynb":
        for cell in nb.cells:
            if cell.cell_type != "code" or "# === Environment Setup ===" not in text(cell):
                continue
            src = text(cell)
            src = re.sub(
                r"try:\n\s+import graphviz\n\s+GRAPHVIZ_AVAILABLE = True\nexcept ImportError:\n\s+try:\n\s+import graphviz\n\s+GRAPHVIZ_AVAILABLE = True\n\s+except ImportError:\n\s+GRAPHVIZ_AVAILABLE = False",
                "try:\n    import graphviz\n    GRAPHVIZ_AVAILABLE = True\nexcept ImportError:\n    GRAPHVIZ_AVAILABLE = False",
                src,
            )
            src = re.sub(r"\nelse:\s*$", "\n", src)
            set_text(cell, src)

    elif rel == "07-Machine-Learning/17_Causal_ML.ipynb":
        nb.cells = [
            c
            for c in nb.cells
            if not (
                c.cell_type == "code"
                and "if ECONML_AVAILABLE:" in text(c)
                and "# 1. Data Generation" in text(c)
                and re.search(r"(?m)^\s*pass\s*$", text(c))
            )
        ]

    elif rel == "07-Machine-Learning/18_Natural_Language_Processing.ipynb":
        nb.cells = [
            c
            for c in nb.cells
            if not (
                c.cell_type == "code"
                and "if GENSIM_AVAILABLE and NLTK_AVAILABLE:" in text(c)
                and re.search(r"(?m)^\s*pass\s*$", text(c))
            )
        ]
        replacement_load = '''glove_vectors = None\nif GENSIM_AVAILABLE:\n    try:\n        # The first call downloads and caches the model through gensim-data.\n        glove_vectors = api.load("glove-wiki-gigaword-100")\n        display(Markdown("> **Note:** GloVe vectors loaded and cached successfully."))\n    except (OSError, ValueError, RuntimeError) as exc:\n        display(Markdown(f"> **Note:** GloVe vectors are unavailable in this environment: `{exc}`"))\nelse:\n    display(Markdown("> **Note:** `gensim` is not installed; skipping the pretrained-embedding lab."))'''
        replace_source_matching(nb, "glove_vectors = api.load('glove-wiki-gigaword-100')", replacement_load)
        replacement_sim = '''if glove_vectors is not None:\n    query_word = "finance"\n    if query_word in glove_vectors.key_to_index:\n        neighbors = glove_vectors.most_similar(query_word, topn=8)\n        similarity_table = pd.DataFrame(neighbors, columns=["word", "cosine_similarity"])\n        display(similarity_table)\n\n        analogy = glove_vectors.most_similar(positive=["bank", "money"], negative=["river"], topn=5)\n        display(Markdown("**A simple vector-arithmetic probe (`bank + money - river`):**"))\n        display(pd.DataFrame(analogy, columns=["word", "cosine_similarity"]))\n    else:\n        display(Markdown(f"> **Note:** `{query_word}` is not present in the selected vocabulary."))'''
        replace_source_matching(nb, "# 2. Explore Semantic Similarities", replacement_sim)

    elif rel == "08-Time-Series/03_ARIMA_and_Forecasting.ipynb":
        nb.cells = [
            c
            for c in nb.cells
            if not (
                c.cell_type == "code"
                and "# 1. Load and plot the data" in text(c)
                and re.search(r"(?m)^\s*pass\s*$", text(c))
            )
        ]
        loader = '''from pathlib import Path\n\ndef _load_indpro(start="1980-01-01", end="2022-12-31"):\n    """Load INDPRO from FRED when available, otherwise from the bundled CSV."""\n    if PDR_AVAILABLE:\n        try:\n            downloaded = web.DataReader("INDPRO", "fred", start, end)\n            downloaded.index = pd.DatetimeIndex(downloaded.index)\n            return downloaded, "FRED"\n        except (OSError, ValueError, KeyError) as exc:\n            display(Markdown(f"> **Note:** FRED download failed (`{exc}`); using the bundled snapshot."))\n\n    candidates = [Path("data/INDPRO.csv"), Path("../data/INDPRO.csv")]\n    local_path = next((candidate for candidate in candidates if candidate.exists()), None)\n    if local_path is None:\n        raise FileNotFoundError("Bundled INDPRO.csv was not found from the repository root or notebook directory.")\n    local = pd.read_csv(local_path, index_col="observation_date", parse_dates=True)\n    return local.loc[start:end], f"local snapshot: {local_path}"\n\nindpro, indpro_source = _load_indpro()\nlog_indpro = np.log(indpro["INDPRO"].astype(float))\ndisplay(Markdown(f"> **Data source:** {indpro_source}; {len(log_indpro):,} monthly observations."))'''
        replace_source_matching(nb, "indpro = web.DataReader('INDPRO'", loader)
        nb.cells = [
            c
            for c in nb.cells
            if not (
                c.cell_type == "code"
                and "if not PDR_AVAILABLE:" in text(c)
                and "INDPRO.csv" in text(c)
            )
        ]

    elif rel == "08-Time-Series/06_Cointegration_and_Error_Correction_Models.ipynb":
        nb.cells = [
            c
            for c in nb.cells
            if not (
                c.cell_type == "code"
                and "series_to_load" in text(c)
                and re.search(r"(?m)^\s*pass\s*$", text(c))
            )
        ]
        loader = '''from pathlib import Path\n\nseries_to_load = {"PCECC96": "LogCons", "DPIC96": "LogInc"}\nstart, end = "1960-01-01", "2019-12-31"\n\ndef _load_consumption_income():\n    if PDR_AVAILABLE:\n        try:\n            downloaded = web.DataReader(list(series_to_load), "fred", start, end)\n            return downloaded, "FRED"\n        except (OSError, ValueError, KeyError) as exc:\n            display(Markdown(f"> **Note:** FRED download failed (`{exc}`); using bundled snapshots."))\n\n    def locate(filename):\n        candidates = [Path("data") / filename, Path("../data") / filename]\n        path = next((candidate for candidate in candidates if candidate.exists()), None)\n        if path is None:\n            raise FileNotFoundError(f"Bundled {filename} was not found.")\n        return path\n\n    cons_path, inc_path = locate("PCECC96.csv"), locate("DPIC96.csv")\n    cons = pd.read_csv(cons_path, index_col="observation_date", parse_dates=True)\n    inc = pd.read_csv(inc_path, index_col="observation_date", parse_dates=True)\n    return pd.concat([cons, inc], axis=1), f"local snapshots: {cons_path}, {inc_path}"\n\ndata_raw, macro_source = _load_consumption_income()\ndf = np.log(data_raw[list(series_to_load)].astype(float)).dropna()\ndf.columns = list(series_to_load.values())\ndf = df.loc[start:end]\ndisplay(Markdown(f"> **Data source:** {macro_source}; {len(df):,} aligned observations."))\ndf.plot(title="Log Real Consumption and Disposable Income")\nplt.show()\n\n# Engle-Granger cointegration test\nscore, p_value, _ = coint(df["LogCons"], df["LogInc"])\ncointegrated = bool(p_value < 0.05)\nconclusion = "reject" if cointegrated else "do not reject"\ndisplay(Markdown(\n    f"> **Engle-Granger result:** p-value = {p_value:.4f}; {conclusion} the null of no cointegration at the 5% level."\n))'''
        replace_source_matching(nb, "data_raw = web.DataReader(list(series_to_load.keys())", loader)
        # Remove the obsolete fallback/test/result fragments now consolidated above.
        obsolete_markers = [
            "if not PDR_AVAILABLE:",
            "score, p_value, _ = coint",
            "Cointegration test p-value",
            "if p_value < 0.05:",
        ]
        kept = []
        for c in nb.cells:
            src = text(c)
            if c.cell_type == "code" and any(marker in src for marker in obsolete_markers):
                # Keep our newly consolidated cell (it contains coint but also macro_source).
                if "macro_source" in src and "_load_consumption_income" in src:
                    kept.append(c)
                continue
            if c.cell_type == "markdown" and (
                "Data downloaded successfully" in src
                or "pandas_datareader not available" in src
                or "p-value is less than 0.05" in src
            ):
                continue
            kept.append(c)
        nb.cells = kept

    elif rel == "high_performance_python/01_High_Performance_Computing.ipynb":
        for cell in nb.cells:
            if cell.cell_type == "code" and "def fast_function():" in text(cell):
                src = re.sub(
                    r"def fast_function\(\):\n\s+pass",
                    'def fast_function():\n    """Reference no-op used to isolate profiler overhead."""\n    return None',
                    text(cell),
                )
                set_text(cell, src)


def repair_optional_import_passes(nb, path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    for cell in nb.cells:
        if cell.cell_type != "code":
            continue
        src = text(cell)
        if rel == "07-Machine-Learning/05_Dimensionality_Reduction_and_Clustering.ipynb" and "import yfinance as yf" in src and "except Exception:\n    pass" in src:
            src = src.replace(
                "try:\n    import yfinance as yf\nexcept Exception:\n    pass",
                "try:\n    import yfinance as yf\n    YFINANCE_AVAILABLE = True\nexcept ImportError:\n    yf = None\n    YFINANCE_AVAILABLE = False",
            )
        if rel == "07-Machine-Learning/09_LSTMs_and_GRUs.ipynb" and "import pandas_datareader.data as web" in src and "except Exception:\n    pass" in src:
            src = src.replace(
                "try:\n    import pandas_datareader.data as web\nexcept Exception:\n    pass",
                "try:\n    import pandas_datareader.data as web\n    PDR_AVAILABLE = True\nexcept ImportError:\n    web = None\n    PDR_AVAILABLE = False",
            )
        set_text(cell, src)


def repair_broken_image_references(nb, path: Path) -> None:
    rel = path.relative_to(ROOT).as_posix()
    replacements = {
        "../images/01-Foundations/1.1-eniac-programmers.gif": "../images/01-Foundations/1.1-eniac-programmers.jpg",
        "../images/01-Foundations/1.4.1-list-internal-structure.png": "../images/01-Foundations/1.5-list-internals.png",
        "../images/01-Foundations/1.3-data-model-translation.png": "../images/01-Foundations/1.3-data-model-translation.svg",
    }
    missing_historical = {
        "../images/01-Foundations/1.1-william-petty.jpg",
        "../images/01-Foundations/1.1-quesnay-tableau.png",
        "../images/01-Foundations/1.1-ibm-system360.jpg",
        "../images/01-Foundations/1.1-wassily-leontief.jpg",
        "../images/01-Foundations/1.1-robert-lucas.jpg",
    }
    for cell in nb.cells:
        if cell.cell_type != "markdown":
            continue
        src = text(cell)
        for old, new in replacements.items():
            src = src.replace(old, new)
        for target in missing_historical:
            # Remove only the broken image markup, retaining the surrounding historical narrative.
            src = re.sub(rf"!?\[[^\]]*\]\({re.escape(target)}\)\s*", "", src)
        set_text(cell, src)


def ensure_ids(nb, path: Path) -> None:
    used: set[str] = set()
    rel = path.relative_to(ROOT).as_posix()
    for i, cell in enumerate(nb.cells):
        cid = cell.get("id")
        if not cid or cid in used:
            digest = hashlib.sha1(f"{rel}:{i}:{text(cell)[:160]}".encode()).hexdigest()[:12]
            cid = f"cell-{digest}"
            counter = 1
            while cid in used:
                cid = f"cell-{digest[:8]}-{counter}"
                counter += 1
            cell["id"] = cid
        used.add(cid)


def write_supporting_svg() -> None:
    out = ROOT / "images/01-Foundations/1.3-data-model-translation.svg"
    out.write_text(
        '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="520" viewBox="0 0 1200 520" role="img" aria-labelledby="title desc">
<title id="title">From economic concept to Python data representation</title>
<desc id="desc">A four-stage diagram linking an economic concept to mathematical representation, Python type, and validation checks.</desc>
<rect width="1200" height="520" fill="#f8fafc"/>
<g font-family="Arial, sans-serif" text-anchor="middle">
  <text x="600" y="55" font-size="30" font-weight="700" fill="#0f172a">Economic object → representation → Python type → validation</text>
  <g font-size="20">
    <rect x="55" y="150" rx="18" width="230" height="180" fill="#e0f2fe" stroke="#0369a1" stroke-width="3"/>
    <text x="170" y="210" font-weight="700" fill="#075985">Economic object</text><text x="170" y="250" fill="#0f172a">price, income, state,</text><text x="170" y="282" fill="#0f172a">choice, parameter</text>
    <rect x="335" y="150" rx="18" width="230" height="180" fill="#ecfccb" stroke="#4d7c0f" stroke-width="3"/>
    <text x="450" y="210" font-weight="700" fill="#3f6212">Mathematical form</text><text x="450" y="250" fill="#0f172a">scalar, vector, matrix,</text><text x="450" y="282" fill="#0f172a">mapping, probability</text>
    <rect x="615" y="150" rx="18" width="230" height="180" fill="#fef3c7" stroke="#b45309" stroke-width="3"/>
    <text x="730" y="210" font-weight="700" fill="#92400e">Python form</text><text x="730" y="250" fill="#0f172a">float, ndarray, dict,</text><text x="730" y="282" fill="#0f172a">Series, dataclass</text>
    <rect x="895" y="150" rx="18" width="250" height="180" fill="#f3e8ff" stroke="#7e22ce" stroke-width="3"/>
    <text x="1020" y="210" font-weight="700" fill="#6b21a8">Validation</text><text x="1020" y="250" fill="#0f172a">units · shape · domain</text><text x="1020" y="282" fill="#0f172a">missingness · invariants</text>
  </g>
  <g stroke="#475569" stroke-width="4" fill="none"><path d="M285 240 H330"/><path d="M565 240 H610"/><path d="M845 240 H890"/></g>
  <g fill="#475569"><path d="M330 240 l-14 -9 v18z"/><path d="M610 240 l-14 -9 v18z"/><path d="M890 240 l-14 -9 v18z"/></g>
  <text x="600" y="410" font-size="21" fill="#334155">Choose a representation that preserves the economic invariant you need to test.</text>
</g></svg>''',
        encoding="utf-8",
    )


def notebook_groups(paths: list[Path]) -> dict[str, list[Path]]:
    groups: dict[str, list[Path]] = {}
    for path in paths:
        groups.setdefault(module_of(path), []).append(path)
    for values in groups.values():
        values.sort()
    return groups


def main() -> None:
    write_supporting_svg()
    paths = sorted(ROOT.glob("**/*.ipynb"))
    paths = [p for p in paths if ".ipynb_checkpoints" not in p.parts]
    groups = notebook_groups(paths)
    changed = 0
    for path in paths:
        nb = nbformat.read(path, as_version=4)
        before = nbformat.writes(nb)
        dedupe_finance_lens(nb)
        ensure_badges(nb, path)
        standardize_and_expand_lens(nb, path)
        add_hpp_objectives_prereqs(nb, path)
        group = groups[module_of(path)]
        pos = group.index(path)
        prev_path = group[pos - 1] if pos > 0 else None
        next_path = group[pos + 1] if pos + 1 < len(group) else None
        ensure_learning_path(nb, path, prev_path, next_path)
        ensure_filename_prerequisite(nb, path, prev_path)
        confirmed_code_repairs(nb, path)
        repair_optional_import_passes(nb, path)
        remove_blanket_warning_suppression(nb)
        repair_broken_image_references(nb, path)
        ensure_key_equations(nb, path)
        cleanup_generated_exercise_duplicates(nb)
        ensure_exercises(nb, path)
        ensure_exercise_tiers(nb, path)
        ensure_summary(nb, path)
        ensure_references(nb, path)
        ensure_ids(nb, path)
        after = nbformat.writes(nb)
        if after != before:
            nbformat.write(nb, path)
            changed += 1
    print(f"Normalized {len(paths)} notebooks; {changed} files changed.")


if __name__ == "__main__":
    main()
