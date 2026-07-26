# Comprehensive Project Audit & Improvement Plan

> **Generated from deep one-by-one analysis of all 113 notebooks, 64 scripts, 13 data files, all docs, configs, and infrastructure files.**

---

## Part I: Cross-Cutting Audit Findings

### A. Notebook Structural Compliance Matrix

| Standard Element | Required By | Present In | Missing From | Gap |
|---|---|---|---|---|
| **The Lens** section | PEDAGOGY.md | 104/113 notebooks | ~9 | ~8% |
| **Learning Objectives** | PEDAGOGY.md | **12/113** | 101 | **89%** |
| **Prerequisites** | PEDAGOGY.md | **9/113** | 104 | **92%** |
| **Table of Contents** | PEDAGOGY.md | 99/113 | ~14 | ~12% |
| **Exercises** | PEDAGOGY.md (min 3) | 82/113 | ~31 | **27%** |
| **Summary / Key Takeaways** | PEDAGOGY.md | 112/113 | ~1 | ~1% |
| **References / Further Reading** | PEDAGOGY.md | **23/113** | 90 | **80%** |
| **Colab/Binder Badges** | FULL_ROADMAP.md | **0/113** | 113 | **100%** |
| **Standard Plot Style** (`seaborn-v0_8-whitegrid`) | CODE_STYLE.md | 110/113 | ~3 | ~3% |
| **Type Hints on Functions** | CODE_STYLE.md | **9/113** | 104 | **92%** |
| **`ipywidgets` Interactivity** | FULL_ROADMAP.md | 9/113 | 104 | 92% |

### B. Boilerplate / Template Remnant Contamination

**22 notebooks** (primarily in 09-Finance, 10-Specialized-Models, Appendix, high_performance_python) contain auto-generated template cells that do not belong:

- `"### Concept Overview: Iterative Control Flow"` — generic CS concept cards
- `"### Concept Overview: Object-Oriented Programming (Classes)"` — generic
- `"### Concept Overview: NumPy Arrays"` — generic
- `"### Concept Overview: Pandas DataFrame"` — generic
- `"### Concept Overview: Modular Functions"` — generic
- `"### Concept Overview: Linear Algebra Solvers"` — generic
- `"### Implementation Detail\nThe following code block implements..."` — boilerplate

**Affected files (22):**
- `09-Finance/01_Portfolio_Theory.ipynb` (12 instances)
- `09-Finance/02_Asset_Pricing.ipynb` (8 instances)
- `09-Finance/03_Option_Pricing.ipynb` (12 instances)
- `09-Finance/04_Continuous_Time_Finance.ipynb` (9 instances)
- `09-Finance/05_Credit_Risk.ipynb` (7 instances)
- `09-Finance/06_High_Frequency_Data.ipynb` (6 instances)
- `09-Finance/07_Financial_Frictions_BGG.ipynb` (8 instances)
- `10-Specialized-Models/01_Agent_Based_Models.ipynb` (11 instances)
- `10-Specialized-Models/02_General_Equilibrium_with_Heterogeneous_Agents.ipynb` (11 instances)
- `10-Specialized-Models/03_Network_Economics.ipynb` (9 instances)
- `Appendix/A1-Real-Analysis.ipynb` (8 instances)
- `Appendix/A2-Multivariate-Calculus.ipynb` (5 instances)
- `Appendix/A3-Probability-Theory.ipynb` (6 instances)
- `Appendix/A4-Linear-Algebra.ipynb` (4 instances)
- `Appendix/T1_Publishing_with_Quarto.ipynb` (3 instances)
- `Appendix/T2_Replication_Exercise_Chetty_2014.ipynb` (3 instances)
- `Appendix/T3_Autograding_with_Otter.ipynb` (3 instances)
- `high_performance_python/01_High_Performance_Computing.ipynb` (8 instances)
- `high_performance_python/02_Accelerating_Code_with_Numba.ipynb` (4 instances)
- `high_performance_python/03_Parallel_Computing_with_Dask.ipynb` (2 instances)
- `high_performance_python/04_GPU_Acceleration_with_CuPy.ipynb` (1 instance)

### C. Duplicate License Badge Problem

Multiple notebooks have the license badge block duplicated 2-3 times in cell 0:
- `05-Micro-Models/02_General_Equilibrium.ipynb` — 3x badges
- `06-Econometrics/03_Causal_Inference.ipynb` — 3x badges
- `07-Machine-Learning/06_Deep_Learning_Foundations.ipynb` — 3x badges
- `08-Time-Series/04A_VAR_Estimation_and_Granger.ipynb` — 3x badges
- Many others in modules 05-10

This likely resulted from running `scripts/standardize_headers.py` multiple times.

### D. Header Inconsistency

- **01-Foundations & 02-Numerical-Methods:** Consistent header format with `# XX Title` + badges + "The Lens" + Learning Objectives + Prerequisites
- **03-Economic-Modeling through 10:** Mixed formats. Some have `## Part N: Module Name` / `## Chapter N.X: Title` prefixes, others don't. Some have `# The Lens`, others `## The Lens`.
- **Module name in header cell:** Some notebooks redundantly include the module name (e.g., "# 01-Foundations") at the top.

### E. Import Style Inconsistencies

- **01-Foundations (24 notebooks):** Clean, standardized imports with individual lines
- **02-Numerical-Methods (8):** Clean, standardized
- **03 through 10:** Many use compressed imports: `import os, sys, math, time, random, json, textwrap, warnings`
- **Unnecessary imports:** Many notebooks import `os, sys, math, time, random, json, textwrap` even when unused
- **Missing `import math`:** The Vector class in `04_Python_Data_Model.ipynb` uses `math.sqrt` but imports `math` only in the setup cell, not where used

### F. Code Quality Issues

1. **Bare `except:` clause** in `scripts/audit_notebooks.py` line 67
2. **`except:` with bare pass** in `05-Micro-Models/02_General_Equilibrium.ipynb` (CGEModel.get_excess_demand_goods)
3. **Deprecated API usage:** `keras.datasets.boston_housing` in `07-Machine-Learning/06_Deep_Learning_Foundations.ipynb` (removed in sklearn 1.2+)
4. **`graphviz` imported but not guarded** in `07-Machine-Learning/06_Deep_Learning_Foundations.ipynb`
5. **`os.makedirs` in notebook code cells** (08-Time-Series/04) — image saving should not happen in notebooks
6. **Hardcoded relative paths** (`../scripts`, `../images`) — fragile, breaks on Colab/Binder

### G. TODO/FIXME Items Found in Code

| File | Issue |
|---|---|
| `03-Economic-Modeling/03A_Discrete_Choice_DP_Rust.ipynb` | 2 TODOs |
| `03-Economic-Modeling/04_Estimation_and_Calibration.ipynb` | 1 TODO |
| `04-Macro-Models/03B_RBC_Model_Solution.ipynb` | 1 TODO |
| `06-Econometrics/02A_MLE_Principles_and_Geometry.ipynb` | 1 TODO |
| `07-Machine-Learning/06_Deep_Learning_Foundations.ipynb` | 1 TODO |
| `08-Time-Series/04A_VAR_Estimation_and_Granger.ipynb` | 1 TODO |
| `01-Foundations/22A_Computational_Complexity_Foundations.ipynb` | 2 FutureWarning suppressions |

### H. Empty / Placeholder Content

- `06-Econometrics/03_Causal_Inference.ipynb` cell 2: `"(Introduction text to be added)"`
- `06-Econometrics/03_Causal_Inference.ipynb` cell 4: Table of Contents with only `"1. [Introduction](#Introduction)"` — incomplete
- Several notebooks in 06-Econometrics have `GRAPHVIZ_AVAILABLE = False` hardcoded

### I. Redundancies & Content Overlaps

A systematic cross-notebook search reveals **significant topic duplication** where the same concept is re-taught from scratch in multiple notebooks rather than building on prior coverage:

| Topic | Notebooks Where Re-Taught | Nature of Overlap |
|---|---|---|
| **OLS Regression** | `01-Foundations/12_NumPy` (manual), `01-Foundations/13_Pandas`, `02-Numerical-Methods/01_Linear_Algebra`, `06-Econometrics/01_Linear_Model_and_OLS`, `07-ML/01_Introduction_to_ML` | Re-derived 5 times; each re-explains the normal equations from scratch |
| **Contraction Mapping Theorem** | `01-Foundations/01_Introduction` (9 mentions), `02-Numerical-Methods/04_Root_Finding` (2), `03-Economic-Modeling/01_Dynamic_Programming` (7), `Appendix/A1-Real-Analysis` (6) | Proven or stated 4 separate times with no cross-referencing |
| **Newton-Raphson** | `01-Foundations/20_Introduction_to_SciPy` (4), `02-Numerical-Methods/03_Numerical_Differentiation` (5), `02-Numerical-Methods/04_Root_Finding` (9), `02-Numerical-Methods/05_Optimization` (1) | Explained and coded in 4 notebooks |
| **Tauchen Discretization** | `03-Economic-Modeling/01_DP` (6), `03-Economic-Modeling/02_DP_Continuous` (3), `03-Economic-Modeling/04_Estimation` (3), `04-Macro-Models/macro_vfi_utils.py` | Implemented 4 times across notebooks and utility file |
| **Bellman Equation** | `01-Foundations/01_Introduction`, `01-Foundations/22_Computational_Complexity`, `02-Numerical-Methods/06_Interpolation`, `03-Economic-Modeling/01-07`, `04-Macro-Models/01-03`, `07-ML/15_RL`, `09-Finance/05_Continuous_Time`, `10-Specialized/02_HANK` | Re-introduced in 14+ notebooks |
| **Monte Carlo Integration** | `02-Numerical-Methods/07_Numerical_Integration` (16), `09-Finance/04_Option_Pricing` (5), `high_performance_python/02` (3), `high_performance_python/04` (4) | Re-implemented from scratch 4 times |
| **VAR / Time Series Analysis** | `06-Econometrics/09_Classical_Time_Series_Analysis`, `08-Time-Series/04A_VAR_Estimation_and_Granger`, `08-Time-Series/04B_VAR_Identification_and_Structural_Shocks`, `08-Time-Series/04C_VAR_Impulse_Responses_and_FEVD` | Substantial content overlap between modules |
| **Propensity Score Matching** | `06-Econometrics/03_Causal_Inference` (8 mentions), `07-ML/17_Causal_ML` | PSM covered in both; the ML notebook should build on, not repeat, the Econometrics one |
| **Euler Equation** | `03-Economic-Modeling/02_DP_Continuous` (14), `04-Macro-Models/02_Neoclassical_Growth`, `04-Macro-Models/03_RBC`, `04-Macro-Models/05_NK`, `04-Macro-Models/07_Endogenous_Growth` | Derived from scratch in 5+ notebooks |
| **`solve_bgg_model.py` vs BGG notebook** | `scripts/solve_bgg_model.py`, `scripts/bgg_illustrative_solver.py`, `09-Finance/07_Financial_Frictions_BGG.ipynb` | Same model solved in 3 places |

**Impact:** Learners encounter the same derivation repeatedly without clear signposting ("we proved this in Notebook X; here we apply it"). This inflates content volume, creates maintenance burden, and obscures the pedagogical progression.

### J. Over-Engineering Audit

Several implementations are unnecessarily complex for their pedagogical purpose:

| Location | Issue | Simpler Alternative |
|---|---|---|
| `01-Foundations/04_Python_Data_Model.ipynb` | `ModelRegistryMeta` metaclass example — metaclasses are a niche topic that may confuse more than it teaches at this level | Move to an "Advanced Topics" box or Appendix |
| `02-Numerical-Methods/04_Root_Finding.ipynb` | `anderson_acceleration` function is incomplete (comment says "Ideally we would solve a least squares problem here") — half-implemented algorithm | Either complete it properly or remove and reference `scipy.optimize.fixed_point` |
| `09-Finance/07_Financial_Frictions_BGG.ipynb` | Full 8-variable QZ decomposition DSGE solver inline — extremely advanced for a finance notebook | Factor out to utility module (already partially done), simplify in-notebook to 3-var system |
| `05-Micro-Models/02_General_Equilibrium.ipynb` | `CGEModel.get_excess_demand_goods()` has nested `try/except` with bare pass and silent `np.nan` return | Clean error handling with informative messages |
| `10-Specialized-Models/01_Agent_Based_Models.ipynb` | `MacroABM` model is over-simplified to the point of not producing meaningful dynamics (GDP collapses immediately) | Calibrate properly or simplify further with clear caveat |
| `scripts/generate_images.py` setup_dirs | Creates 7 directories but only 3 generation functions — most directories remain empty | Only create directories that will be populated |
| Multiple notebooks | Import of 8+ unused modules (`os, sys, math, time, random, json, textwrap`) in every setup cell | Strip to actually-used imports per notebook |

### K. Writing Quality & Proofreading

Systematic proofreading has not been performed. Identified patterns:

| Category | Examples |
|---|---|
| **Typos** | `beijin_data.dta` (should be `beijing`); `my-research-env` in README (should be `computational-economics`); `pysinc` in `environment.yml` (non-existent package) |
| **Incomplete sentences** | `06-Econometrics/03_Causal_Inference.ipynb` cell 2: `"(Introduction text to be added)"` |
| **Inconsistent voice** | Some notebooks use first-person plural ("We will…"), others use second-person ("You will…"), others use passive voice ("It can be shown that…") — no consistent authorial voice |
| **Abrupt transitions** | Many notebooks jump from theory to code without a bridging sentence. E.g., in `02-Numerical-Methods/04_Root_Finding.ipynb`, the Anderson acceleration function (cell 1) appears before the import cell (cell 2) — broken narrative flow |
| **Dense walls of text** | Several theory cells exceed 500 words without a single equation, code example, or visual break. E.g., `02-Numerical-Methods/04_Root_Finding.ipynb` cell 4 has Bisection, Newton, Halley, Broyden, Anderson, and convergence proof all in one cell |
| **Undefined notation** | Variables used in equations without prior definition (e.g., $\xi$ in Newton convergence proof in `04_Root_Finding.ipynb` is introduced mid-proof without statement like "where $\xi \in [x_n, x^*]$") |
| **Missing motivation** | Several code cells lack a preceding markdown cell explaining *what* the code does and *why* — the reader sees a class definition with no context |

### L. Content Gaps & Missing Depth

Areas where the content is too shallow, proofs are missing, or key topics are absent:

| Location | Gap | What's Needed |
|---|---|---|
| **01-Foundations/22_Computational_Complexity** | No formal Big-O definition (only informal); no $\Omega$, $\Theta$ notation; no P vs NP discussion | Add rigorous definitions; add P/NP and implications for economic optimization |
| **02-Numerical-Methods/04_Root_Finding** | Halley's method stated twice (duplicate text in same cell); no convergence proof for Bisection; Brent's method has no explanation of *how* it hybridizes | Deduplicate; add Bisection convergence rate derivation; expand Brent's explanation |
| **03-Economic-Modeling/01_DP** | Bellman equation stated but Principle of Optimality not formally proved | Add proof sketch or intuitive derivation of the Principle of Optimality |
| **04-Macro-Models/02_Neoclassical_Growth** | Euler equation stated but derivation from Lagrangian not shown | Show full Lagrangian / Hamiltonian derivation step by step |
| **05-Micro-Models/02_General_Equilibrium** | No Edgeworth Box, no First/Second Welfare Theorems, no proof of existence via Brouwer | Add these foundational GE results |
| **06-Econometrics/03_Causal_Inference** | DAGs discussed but no `graphviz` rendering (hardcoded `GRAPHVIZ_AVAILABLE = False`); no formal d-separation definition | Enable graphviz; add d-separation; add do-calculus introduction |
| **06-Econometrics (whole module)** | No notebook on Panel Data fixed/random effects derivation from first principles | Expand `12_Panel_Data_Methods` with within-estimator derivation |
| **07-ML/06_Deep_Learning** | Universal Approximation Theorem mentioned but not stated or proved | Add formal statement + intuitive proof sketch |
| **08-Time-Series (whole module)** | No unit root testing notebook (ADF, PP, KPSS) as standalone topic | Either expand `01_Introduction` or add a dedicated notebook |
| **09-Finance/04_Option_Pricing** | Black-Scholes formula stated but no derivation from Itô's Lemma | Add step-by-step derivation or cross-reference to `05_Continuous_Time_Finance` |
| **Appendix A1-A4** | Math appendices contaminated with boilerplate; proofs are stated but many lack step-by-step working | Expand every theorem/proof with intermediate steps |
| **All modules** | No "Key Equations" summary box at the end of theory-heavy notebooks | Add consolidated equation reference at the end |

### M. Ordering & Sequencing Issues

| Issue | Detail |
|---|---|
| **Cell ordering bug** | `02-Numerical-Methods/04_Root_Finding.ipynb`: `anderson_acceleration` function (cell 1) placed before the imports cell (cell 2) — code cannot execute |
| **Module numbering gaps** | Resolved: `high_performance_python/` now uses contiguous 01–04 naming |
| **Appendix dual numbering** | Resolved: math appendices use `A1`–`A4`; tooling uses `T1`–`T3` |
| **Cross-module dependency ambiguity** | `04-Macro-Models/01_Job_Search` uses VFI but `03-Economic-Modeling/01_DP` teaches VFI — no explicit prerequisite link |
| **Within-module progression unclear** | In `01-Foundations`, notebooks 05-08 (data structures) could be reordered: Sets (08) before Dictionaries (07) would be more natural since sets are simpler |
| **Late introduction of tools** | `01-Foundations/17_Effective_Debugging` comes after 16 notebooks that could have benefited from debugging skills. `02_Professional_Development_Environment` teaches Git but is notebook #2, not #1 |
| **Topic split across modules** | Time series concepts split between `06-Econometrics/09_Classical_Time_Series_Analysis` and the dedicated `08-Time-Series` module with no clear boundary |
| **Finance module internal order** | Resolved in Phase 13.1: reordered to start with `01_Portfolio_Theory`, `02_Asset_Pricing`, and `03_Option_Pricing`, with BGG moved to the end |

### N. Coherence & Cohesiveness

| Dimension | Current State | Target |
|---|---|---|
| **Narrative thread** | No "Previously on…" or "Coming up next…" links between notebooks | Every notebook should open with "Building on [Notebook X]…" and close with "In the next notebook, we will…" |
| **Notation consistency** | Discount factor: $\beta$ in most notebooks, but $\delta$ in some macro notebooks. Interest rate: $r$, $R$, $i$, $i_{nom}$ used interchangeably without mapping | Create a project-wide notation glossary (`docs/resources/notation.md`); enforce within each module |
| **Variable naming** | `n_states` in `dp_solver.py`, `n` in `macro_vfi_utils.py`, `N` in ABM notebooks — no convention for count variables | Standardize: `n_<thing>` for counts, document in code style guide |
| **Terminology** | "Value Function Iteration" vs "VFI" vs "value iteration" used inconsistently | First use: full name + abbreviation. Subsequent: abbreviation only |
| **Tone** | Module 01-02: tutorial, warm, explanatory. Module 03-04: research-paper terse. Module 09-10: template-generated generic. | Standardize to a consistent "graduate textbook" tone throughout |
| **"The Lens" depth** | Module 02 (Numerical Methods): Excellent — each Lens deeply connects to economics. Module 09 (Finance): Some Lens sections are 2 sentences | All Lens sections should be 150-300 words with a specific economic question |
| **Exercise difficulty** | Module 01: Exercises vary from trivial to challenging. Module 06-08: Most exercises are at the same difficulty level | Adopt the 3-tier system consistently: Conceptual / Applied / Challenge |

### O. Legacy Remnants (Beyond Boilerplate)

Items beyond the "Concept Overview" template cells that are stale or from earlier project iterations:

| Remnant | Location | Issue |
|---|---|---|
| **`## Part N: Module Name` / `## Chapter N.X: Title` headers** | Scattered in modules 03-10 | Leftover from a textbook-style numbering scheme that was abandoned. Some notebooks have it, most don't |
| **`> **Note:** Environment initialized…` print statements** | Nearly every notebook's setup cell | Legacy print confirmation — unnecessary clutter; should be silent or use a single standard message |
| **`%config InlineBackend.figure_format = 'retina'`** | Only in some notebooks (01-Foundations consistently, others sporadically) | Either include everywhere or nowhere |
| **`plt.rcParams` inconsistency** | `figure.figsize` varies: (10,6), (12,7), (12,8), (14,8) across notebooks; `font.size` varies: 12, 14; `figure.dpi` varies: 100, 120, 130, 150 | Standardize to one rcParams block project-wide |
| **`np.set_printoptions` inconsistency** | `precision` varies: 4, 6. `linewidth` varies: 100, 120. Present in some notebooks, absent in others | Standardize |
| **Stale `FULL_ROADMAP.md`, `IMPROVEMENT_PLAN.md`, `INFRASTRUCTURE.md`, `PEDAGOGY.md`, `PREP_WORK_SUMMARY.md`** | Root directory | 5 planning documents from earlier phases, now superseded by this audit. Should be archived or consolidated |
| **`notebook_structure.md` (148 KB) + `notebook_structure_report.json` (372 KB)** | Root directory | Auto-generated audit artifacts cluttering root |
| **`debug_rbc.py`, `debug_rbc_reduced.py`** | Root directory | Debug scripts that should not be in root |
| **`models/mlp_boston_housing.keras`** | `models/` | Trained on deprecated Boston Housing dataset; should be regenerated or removed |
| **`image_path_mapping.json`** | Root directory | Build artifact; should be in `scripts/` or `.gitignore` |
| **`GRAPHVIZ_AVAILABLE = False` hardcoded** | Multiple econometrics notebooks | Legacy workaround — should be dynamic `try/except` |

### P. Convention Inconsistencies

Beyond code style (covered in F/E), there are pedagogical and formatting conventions that vary across the project:

| Convention | Variants Found | Recommended Standard |
|---|---|---|
| **Heading for economic motivation** | `# The Lens`, `## The Lens`, `### The Lens: <subtitle>` | `## The Lens: <Subtitle>` everywhere |
| **Heading level for sections** | `##` in some notebooks, `###` in others for the same logical level | `##` for major sections, `###` for subsections, `####` for sub-subsections |
| **Exercise format** | Some use numbered lists, some use `### Exercise N:`, some use `#### N. Title` | `### Exercises` section with `**N. Title (Difficulty):**` format |
| **Code cell output** | Some notebooks show all output (including training logs), others suppress | Suppress verbose output; show only final results and plots |
| **Theorem/Definition boxes** | Some use `> **Theorem (Name):**`, others use plain markdown, others use nothing | Use consistent `> **Theorem N (Name):**` blockquote style |
| **Mathematical notation rendering** | Some use `$...$` for inline, others use `$$...$$` for display. Some use `\text{}` for words in equations, others don't | `$...$` inline, `$$...$$` display, always `\text{}` for words |
| **Figure captions** | Some figures have `plt.title()`, some have `ax.set_title()`, some have neither. No consistent caption style | Always use `ax.set_title()` with `fontsize=14, fontweight='bold'` |
| **Data generation** | Some notebooks use `np.random.seed(42)` (legacy), others use `np.random.default_rng(42)` (modern) | Standardize to `rng = np.random.default_rng(42)` everywhere |
| **`display(Markdown(...))` vs `print()`** | Some notebooks use `display(Markdown(f"> **Note:** ..."))`, others use `print(f"> **Note:** ...")` | Standardize to `display(Markdown(...))` for formatted notes |

---

## Part I-B: Second-Pass Deep Investigation Findings

*These findings were uncovered by a broader, more extensive re-investigation of every file in the project.*

### Q. Broken (Zero-Byte) Image Files — **CRITICAL**

**57 out of 310 image files (18.4%) are 0-byte empty files** that will render as broken images in notebooks.

| Directory | # Broken Files | Examples |
|---|---|---|
| `images/01-Foundations/` | 13 | `1.1-eniac-programmers.gif`, `1.1-ibm-system360.jpg`, `1.1-robert-lucas.jpg`, `1.1-william-petty.jpg`, `1.3-data-model-translation.png` |
| `images/02-Numerical-Methods/` | 9 | ALL files are 0-byte: `2.0-fundamental-subspaces.png`, `2.2-computational-graph.png`, `2.3-bisection-method.png`, `2.3-newton-method.png`, `2.3-secant-method.png`, `2.4-gradient-descent-step.png`, `2.4-newton-method-step.png`, `2.5-chebyshev-nodes.png`, `2.6-quadrature-rules.png` |
| `images/03-Economic-Modeling/` | 4 | ALL files are 0-byte: `3.1-bellman-operator.png`, `3.2-stochastic-expectation.png`, `3.3-chebyshev-nodes.png`, `3.4-binomial-tree.png` |
| `images/04-Macro-Models/` | 4 | ALL files are 0-byte: `4.2-rbc-labor-market.png`, `4.3-olg-cobweb.png`, `4.4-nk-transmission-mechanism.png`, `4.5-beveridge-curve.png` |
| `images/05-Micro-Models/` | 2 | ALL files are 0-byte: `5.1.1-warp-violation.png`, `5.2-tatonnement-process.png` |
| `images/06-Econometrics/` | 5 | `.keep`, `6.2-fisher.jpg`, `6.2-holy_trinity.png`, `iv_diagram.png`, `ols_geometry.png` |
| `images/gif/` | 1 | `1.1-eniac-programmers.gif` |
| `images/jpg/` | 5 | `1.1-ibm-system360.jpg`, `1.1-robert-lucas.jpg`, `1.1-wassily-leontief.jpg`, `1.1-william-petty.jpg`, `fisher.jpg`, `john_snow.jpg` |
| `images/png/` | 10 | `1.1-quesnay-tableau.png`, `bellman_equation.png`, `confounding_diagram.png`, `holy_trinity.png`, `law_of_large_numbers.png`, `nfxp_diagram.png`, `ra_vs_ha.png`, `sml_cml.png`, `system_models.png`, `vector_vs_raster.png` |
| `images/svg/` | 3 | `bayes_rule_visual.svg`, `kalman_filter_model.svg`, `rl_loop.svg` |

**Impact:** 41 notebooks reference images via `![...](../images/...)` markdown. Many of these references point to 0-byte files, producing broken image displays. Entire module image directories (02, 03, 04, 05) have **zero valid files**.

Additionally, there are **duplicate image directory structures**: `images/jpg/`, `images/png/`, `images/gif/`, `images/svg/` contain duplicates of files already in the module-specific directories — all are 0-byte. This suggests a failed migration or download process.

### R. Placeholder "The Lens" and "Summary" Template Cells — **CRITICAL**

Previously, only "Concept Overview" and "Implementation Detail" boilerplate was identified. A deeper sweep reveals a **much larger contamination** with unfilled template cells:

| Template Pattern | # Notebooks Affected | Files |
|---|---|---|
| **Unfilled "The Lens"** (`"Provide a brief overview of the economic context..."`) | **19** | All of 07-ML/02-05,07-15,17,19,21; 08-TS/02,03,06 |
| **Unfilled "Summary"** (`"Key takeaway 1 / Key takeaway 2 / Synthesize the main lesson"`) | **25** | All of 07-ML/02-22; 08-TS/02,03,05,06; 09-Finance/02 |
| **`"(Introduction text to be added)"`** | **12** | 06-Econometrics/03,05,06,08,10,12; 07-ML/18,19,22; Appendix/01_Quarto,01_Chetty,02_Otter |

**Impact:** These 25 notebooks have **two Summary sections** — one with real content and one with empty template text. The 19 notebooks with unfilled "The Lens" have the template cell alongside (in some cases) a real Lens section, creating confusing duplication. The 12 notebooks with "(Introduction text to be added)" have missing introductory content.

### S. Security Vulnerability — **CRITICAL**

**`polyfill.io` CDN reference in `mkdocs.yml` line 130:**
```yaml
- https://polyfill.io/v3/polyfill.min.js?features=es6
```

The `polyfill.io` domain was **compromised in June 2024** and began serving malicious JavaScript to visitors. It is now a known supply-chain attack vector. MathJax v3 no longer requires this polyfill. **This line must be removed immediately.**

### T. Missing Documentation Pages — **CRITICAL**

The `mkdocs.yml` navigation references **45+ markdown files that do not exist** in `docs/`:

| Missing Directory | # Missing Pages | Examples |
|---|---|---|
| `docs/modules/` | 37 | `modules/index.md`, `modules/01-foundations/index.md`, `modules/01-foundations/01-introduction.md`, etc. (all 10 module index pages + ~27 content pages) |
| `docs/appendices/` | 4 | `appendices/index.md`, `appendices/mathematics.md`, `appendices/publishing.md`, `appendices/autograding.md` |

**Only 19 of ~64 referenced docs pages exist.** The docs site build will produce broken navigation with 404 links for ~70% of entries.

Additionally:
- `docs/getting-started/structure.md` is a 20-line stub with no real content
- `docs/resources/datasets.md` references `UNRATE.csv` which doesn't exist in `data/`
- `docs/about/contributing.md` references `scripts/validate_notebooks.py` which doesn't exist

### U. Dependency Gap Analysis — **CRITICAL**

Complete matrix of packages **imported in notebooks but missing from both `environment.yml` and `requirements.txt`**:

| Package | # Notebooks Using It | In `environment.yml`? | In `requirements.txt`? |
|---|---|---|---|
| **tensorflow / keras** | 11 (all 07-ML deep learning) | ❌ No | ❌ No |
| **torch / pytorch** | 2 (07-ML/11,16) | ❌ No | ❌ No |
| **xgboost** | 1 (07-ML/02) | ❌ No | ❌ No |
| **networkx** | 4 (06,07,10) | ❌ No | ❌ No |
| **numba** | 11 (01,03,04,10,HPP) | ❌ No | ❌ No |
| **ipywidgets** | 9 (01,04,05,06,10) | ❌ No | ❌ No |
| **graphviz** | 4 (03,07) | ❌ No | ❌ No |
| **shap** | 3 (07,10) | ❌ No | ❌ No |
| **sympy** | 4 (01,02,05,09) | ❌ No | ❌ No |
| **dask** | 2 (HPP) | ❌ No | ❌ No |
| **cupy** | 2 (HPP) | ❌ No | ❌ No |
| **doubleml / econml** | 1 (07-ML/17) | ❌ No | ❌ No |
| **pymc** | 1 (05-Micro/04) | ❌ No | ❌ No |
| **emcee** | 1 (06-Econometrics/11) | ❌ No | ❌ No |
| **otter-grader** | 1 (Appendix/02) | ❌ No | ❌ No |
| **fredapi** | 1 (01-Foundations/15) | ❌ No | ❌ No |
| **jupyterlab / notebook** | All | ❌ No | ❌ No |

Also: `pyportfolioopt` is in `environment.yml` but **never imported in any notebook**. `pysinc` (non-existent package) is still listed.

The `requirements.txt` is also missing: `scikit-learn`, `statsmodels`, `arch`, `linearmodels`, `nashpy`, `prophet`, `pysal`, `geopandas`, `gymnasium`, `cvxpy`, `joblib` — all present in `environment.yml` but not in `requirements.txt`.

### V. `plt.savefig` Inside Notebooks — Anti-Pattern

**16 notebooks** contain `plt.savefig()` calls that write files to disk when executed:

| Module | # Notebooks | Issue |
|---|---|---|
| 03-Economic-Modeling | 1 | `01_DP` — 4 savefig calls |
| 04-Macro-Models | 2 | `01_Job_Search` (3), `02_Neoclassical_Growth` (1) |
| 05-Micro-Models | 2 | `03_Game_Theory` (2), `06_Information_Econ` (1) |
| 06-Econometrics | 3 | `01_OLS` (3), `05_IV` (1), `08_DiD` (1) |
| 07-Machine-Learning | 4 | `02_GBM` (2), `03_SVM` (1), `11_Autoencoders` (1), `21_ML_Macro` (1) |
| 08-Time-Series | 1 | `04_VAR` (1) |
| 09-Finance | 2 | `02_Portfolio` (1), `06_Credit_Risk` (1) |
| Appendix | 1 | `01_Publishing_Quarto` (1) |

**Impact:** Running notebooks creates files in `images/` that clutter the working directory and may cause unintended git changes. Notebooks should display plots inline only; image generation should be in `scripts/`.

### W. Data File Inconsistencies

| Issue | Detail |
|---|---|
| **Case mismatch** | `data/sp500.csv` exists but GARCH notebook references `SP500.csv` (different case — works on Windows, fails on Linux/macOS) |
| **Missing referenced file** | `docs/resources/datasets.md` lists `UNRATE.csv` but no such file exists in `data/` |
| **`us_macro.csv`** | Undocumented in datasets.md — no provenance, source, or description |
| **`fama_french_factors.csv` vs `fama_french_5_factors.csv`** | Two Fama-French files with unclear distinction; datasets.md only mentions one generically |
| **No `data/README.md`** | No documentation of data provenance, licenses, or download dates |

### X. Duplicate Image Directories

The `images/` folder has **overlapping organizational schemes**:

1. **Module-based:** `images/01-Foundations/`, `images/07-Machine-Learning/`, etc.
2. **Format-based:** `images/jpg/`, `images/png/`, `images/gif/`, `images/svg/`
3. **Topic-based:** `images/machine_learning/`, `images/micro_macro/`
4. **A metadata file:** `images/metadata.json` (56 KB)

Files like `1.1-robert-lucas.jpg` appear in both `images/01-Foundations/` and `images/jpg/` — all duplicates are 0-byte. This suggests a broken image migration script. The format-based and topic-based directories should be removed, and all images consolidated into module-based directories.

### Y. Mixed Deep Learning Frameworks

The project uses **both TensorFlow/Keras and PyTorch** without clear rationale:
- **TensorFlow/Keras:** 07-ML notebooks 06-10, 12-15, 22 (11 notebooks)
- **PyTorch:** 07-ML notebooks 11 (Autoencoders) and 16 (Advanced Deep RL)

This creates a confusing learning experience and doubles the dependency burden. The project should either standardize on one framework or explicitly document the rationale and provide setup instructions for both.

### Z. `warnings.filterwarnings('ignore')` Overuse

**32 notebooks** suppress all warnings globally with `warnings.filterwarnings('ignore')`. This hides:
- DeprecationWarning for APIs that will break in future versions
- FutureWarning for upcoming behavioral changes
- RuntimeWarning for numerical issues (overflow, divide-by-zero)

**Recommendation:** Remove blanket suppression. Use targeted `warnings.filterwarnings('ignore', category=..., module=...)` only where specific expected warnings are noisy.

---

## Part II: Infrastructure & Configuration Audit

### A. Environment & Dependencies

| Issue | Severity | Detail |
|---|---|---|
| **README env name mismatch** | Critical | README says `my-research-env`, `environment.yml` says `computational-economics` |
| **`tqdm` listed twice** | Medium | Duplicate in `environment.yml` |
| **`pysinc` package** | Medium | Likely typo/non-existent package in `environment.yml` |
| **Missing packages** | Critical | `tensorflow`, `pytorch`, `jax`, `numba`, `ipywidgets`, `networkx`, `pymc`, `doubleml`, `graphviz`, `shap`, `rdrobust`, `otter-grader` are used in notebooks but absent from deps |
| **No conda version pins** | High | Only pip packages are pinned in `requirements.txt`; conda packages are unpinned |
| **`requirements.txt` incomplete** | High | Missing ~15 packages present in `environment.yml` (statsmodels, scikit-learn, arch, linearmodels, nashpy, prophet, pysal, geopandas, gymnasium, cvxpy, pyportfolioopt, etc.) |
| **No `pyproject.toml`** | Medium | No centralized project configuration |

### B. Documentation Site

| Issue | Severity | Detail |
|---|---|---|
| **`docs/modules/` directory missing** | Critical | `mkdocs.yml` nav references ~40+ markdown files that don't exist |
| **`docs/appendices/` directory missing** | Critical | Nav references `appendices/index.md`, `mathematics.md`, etc. |
| **No conversion script** | Critical | No `.ipynb` → `.md` script exists (acknowledged in PREP_WORK_SUMMARY.md) |
| **CI installs packages individually** | Medium | `deploy-docs.yml` should use `pip install -r requirements-docs.txt` |
| **`contributing.md` references non-existent script** | High | References `scripts/validate_notebooks.py` which doesn't exist (3 times); also says `conda activate computational-econ` (wrong name — should be `computational-economics`) |
| **`docs/IMAGE_CATALOG.md` is stale** | Medium | References paths like `foundations/git/three_states.png` that don't match actual `images/` directory structure; only 5 images cataloged out of 300+ |
| **`docs/CODE_STYLE.md` (16KB) duplicates `docs/resources/code-style.md` (2KB)** | Low | The resources version is a thin summary linking to the full version; the full version is not in mkdocs.yml nav — only accessible via direct GitHub link |
| **`docs/getting-started/prerequisites.md`** | Low | Only 678 bytes — likely a stub |
| **`docs/getting-started/structure.md`** | Low | Only 471 bytes — likely a stub |
| **`docs/resources/references.md`** | Low | Only 1512 bytes — very thin |
| **`docs/resources/datasets.md`** | Low | Only 1748 bytes — incomplete; references `UNRATE.csv` which doesn't exist; lists `SP500.csv` (uppercase) but file is `sp500.csv`; missing `us_macro.csv` and `fama_french_factors.csv` entries |

### C. CI/CD

| Issue | Severity | Detail |
|---|---|---|
| **No CI for tests** | High | No GitHub Actions workflow for pytest, nbval, or linting |
| **No CI for notebook validation** | High | Notebooks are never tested in CI |
| **Deploy workflow fragile** | Medium | Doesn't fail on missing module pages |
| **Outdated GitHub Actions versions** | Medium | `actions/cache@v3` → should be `v4`; `peaceiris/actions-gh-pages@v3` → should be `v4` |
| **3 mkdocs plugins installed but not configured** | Low | `mkdocs-redirects`, `mkdocs-glightbox`, `mkdocs-minify-plugin` are `pip install`ed in CI but not listed in `mkdocs.yml` plugins section — wasted install |
| **`mike` version provider configured but not installed** | Low | `mkdocs.yml` has `version.provider: mike` but `mike` is not in `requirements-docs.txt` or CI |
| **Google Analytics env var unlikely set** | Low | `!ENV GOOGLE_ANALYTICS_KEY` will silently produce no analytics if env var not configured |

### D. Pre-commit

| Issue | Severity | Detail |
|---|---|---|
| **`.pre-commit-config.yaml` does not exist** | High | INFRASTRUCTURE.md references pre-commit hooks, but the config file was never created. Need to create from scratch with black, ruff, isort |

### E. Testing

| Issue | Severity | Detail |
|---|---|---|
| **Only 1 test file** | Critical | `01-Foundations/test_finance_utils.py` — tests a 5-line function |
| **No `conftest.py`** | High | No shared test fixtures |
| **No `pyproject.toml` / `pytest.ini`** | High | No test configuration |
| **No `nbval` setup** | High | No notebook execution testing |
| **No test for `dp_solver.py`** | High | 181-line solver module with zero tests |
| **No test for `macro_utils.py`** | High | QZ decomposition solver — critical code, zero tests |
| **No test for `macro_vfi_utils.py`** | High | Tauchen discretization — zero tests |

### F. Licensing

| Issue | Severity | Detail |
|---|---|---|
| **No CC BY 4.0 license file** | Medium | Dual license claimed but only MIT `LICENSE` exists |
| **No `images/LICENSE.txt`** | Low | README references per-directory licenses — none exist |

### G. Data Directory

| Issue | Severity | Detail |
|---|---|---|
| **`beijin_data.dta` typo** | Low | Should be `beijing_data.dta` |
| **No `data/README.md`** | Medium | No documentation of dataset provenance, sources, licenses |
| **Large files in git** | Medium | `SEntFiN.csv` (1.1 MB), `beijin_data.dta` (2.7 MB), `sp500.csv` (597 KB) — should consider Git LFS |
| **`models/mlp_boston_housing.keras`** | Low | 94 KB model artifact — should be regenerable |

### H. Root Directory Clutter

| File | Issue | Action |
|---|---|---|
| `debug_rbc.py` | Debug artifact | Move to `scripts/debug/` or delete |
| `debug_rbc_reduced.py` | Debug artifact | Move to `scripts/debug/` or delete |
| `notebook_structure.md` (148 KB) | Generated audit report | Move to `.reports/` or `.gitignore` |
| `notebook_structure_report.json` (372 KB) | Generated audit report | Move to `.reports/` or `.gitignore` |
| `image_path_mapping.json` (16 KB) | Build artifact | Move to `scripts/` |
| `FULL_ROADMAP.md` | Planning doc | Consolidate into `docs/internal/` |
| `IMPROVEMENT_PLAN.md` | Planning doc | Consolidate into `docs/internal/` |
| `INFRASTRUCTURE.md` | Planning doc | Consolidate into `docs/internal/` |
| `PEDAGOGY.md` | Planning doc | Consolidate into `docs/internal/` |
| `PREP_WORK_SUMMARY.md` | Planning doc | Consolidate into `docs/internal/` |
| `01-Foundations/__pycache__/` | Committed cache | Delete; **no `.gitignore` file exists** — must also create `.gitignore` |

---

## Part III: Module-by-Module Deep Findings

### Module 01: Foundations (24 notebooks)

**Strengths:**
- Most standardized module. Consistent headers, ToC, exercises, summaries
- Rich pedagogical content with economic motivation in every notebook
- Good use of `ipywidgets` in `01_Introduction.ipynb`
- `finance_utils.py` has a comprehensive test suite (198 lines, parametrized)
- NumPy notebook (12) is exceptionally thorough: strides, einsum, profiling

**Issues:**
- **Learning Objectives** only in `01_Introduction.ipynb`
- **Prerequisites** only in `01_Introduction.ipynb`
- **References/Further Reading** in only 6/24 notebooks
- `__pycache__/` committed to git
- Header cell has module name prefix `# 01-Foundations` before title — redundant

### Module 02: Numerical Methods (8 notebooks)

**Strengths:**
- **Best standardized module.** All 8 have: Learning Objectives, Prerequisites, The Lens, ToC, Exercises, Summary
- Clean, professional structure throughout
- Root-finding notebook has excellent content: fixed-point theory, Newton fractal, homotopy continuation, Anderson acceleration

**Issues:**
- No References/Further Reading in any of the 8 notebooks
- `04_Root_Finding.ipynb` has `anderson_acceleration` function placed before the import cell (cell 1 before cell 2)
- All 8 empty image directories — generation scripts not yet run

### Module 03: Economic Modeling (7 notebooks + `dp_solver.py`)

**Strengths:**
- `dp_solver.py` is well-written: NumPy-style docstrings, type hints, validation, VFI + PFI
- Good ToC in all notebooks

**Issues:**
- 2 TODO markers in `03A_Discrete_Choice_DP_Rust.ipynb`
- 1 TODO in `04_Estimation_and_Calibration.ipynb`
- No Learning Objectives or Prerequisites in any notebook
- No unit tests for `dp_solver.py`
- Notebooks 03 (214 KB) and 04 (120 KB) are very large — candidates for splitting

### Module 04: Macro Models (7 notebooks + `macro_vfi_utils.py`)

**Strengths:**
- `macro_vfi_utils.py`: Clean Tauchen implementation with NumPy-style docstrings
- Good economic content depth

**Issues:**
- `macro_vfi_utils.py` has note about Numba incompatibility — performance limitation
- 1 TODO in `03B_RBC_Model_Solution.ipynb`
- Notebook 03 split into 03A/03B/03C
- `07_Endogenous_Growth.ipynb` numbered 07 but FULL_ROADMAP says 08
- No tests for `macro_vfi_utils.py`
- No Learning Objectives or Prerequisites

### Module 05: Micro Models (6 notebooks)

**Strengths:**
- `02_General_Equilibrium.ipynb` has solid CGE implementation with Heckscher-Ohlin trade model

**Issues:**
- Triple license badges in `02_General_Equilibrium.ipynb`
- Bare `except:` in CGE code
- `02_General_Equilibrium.ipynb` marked as "Light" in FULL_ROADMAP — needs Edgeworth Box, welfare theorems
- Missing `nashpy` integration in `03_Game_Theory_and_Auctions.ipynb`

### Module 06: Econometrics (12 notebooks)

**Strengths:**
- Causal inference notebook has good DAG discussion, Potential Outcomes framework, PSM implementation
- Wide topic coverage: OLS, MLE, Causal Inference, GMM, IV, RD, Synth Control, DiD, Time Series, Panel, Bayesian

**Issues:**
- `03_Causal_Inference.ipynb` has placeholder text: `"(Introduction text to be added)"`
- `03_Causal_Inference.ipynb` has incomplete ToC
- Triple license badges in `03_Causal_Inference.ipynb`
- `GRAPHVIZ_AVAILABLE = False` hardcoded in several notebooks
- 1 TODO in `02A_MLE_Principles_and_Geometry.ipynb`
- Notebook 02A/02B split completed (original 145 KB)
- Overlap with `08-Time-Series` module (VAR appears in both `09_Classical_Time_Series_Analysis` and `08-Time-Series/04`)

### Module 07: Machine Learning (22 notebooks)

**Strengths:**
- Largest module with comprehensive coverage
- From classical (SVMs, ensemble) to deep learning (CNN, RNN, LSTM, Transformers, GANs, RL, GNNs, Causal ML)

**Issues:**
- `06_Deep_Learning_Foundations.ipynb` uses deprecated `boston_housing` dataset
- `06_Deep_Learning_Foundations.ipynb` imports `graphviz` without try/except guard
- 1 TODO in `06_Deep_Learning_Foundations.ipynb`
- Some notebooks marked "Unknown Kernel" or "Duplicate" in FULL_ROADMAP
- TensorFlow not in dependencies — many notebooks will fail on fresh install
- Triple license badges in several notebooks
- No `shap` in dependencies (used in deep learning notebook)

### Module 08: Time Series (6 notebooks)

**Strengths:**
- VAR notebook has excellent theory: Sims, Lucas critique, Cholesky identification, FEVD
- Good synthetic data generation for demonstrations

**Issues:**
- 1 TODO in `04A_VAR_Estimation_and_Granger.ipynb`
- Triple license badges in `04A_VAR_Estimation_and_Granger.ipynb`
- Notebook 04A saves images from within the notebook (`plt.savefig`) — anti-pattern
- Overlap with Module 06 econometrics time series content
- Notebook 04A/04B split completed; check if IRF notebook still oversized

### Module 09: Finance (7 notebooks)

**Strengths:**
- BGG Financial Accelerator model is a serious graduate-level implementation using QZ decomposition
- Uses `scripts/macro_utils.py` properly

**Issues:**
- **Most contaminated module:** All 7 notebooks contain "Concept Overview" and "Implementation Detail" boilerplate cells (62+ instances total)
- Triple license badges in several notebooks
- `sys.path.append` for importing `macro_utils` — fragile

### Module 10: Specialized Models (3 notebooks)

**Strengths:**
- ABM notebook is exceptionally rich: Schelling, Axelrod, Kirman ants, artificial stock market, macro ABM
- Good use of `ipywidgets` for interactive exploration
- Good use of `dataclass` for agent definitions
- ODD protocol documentation for ABMs

**Issues:**
- All 3 notebooks contaminated with "Concept Overview" boilerplate (31+ instances)
- Thinnest module — only 3 notebooks. FULL_ROADMAP suggests this is complete, but could benefit from 1-2 more (computational auctions, climate-economy)

### Appendix (7 notebooks)

**Issues:**
- Numbering scheme normalized: math appendices `A1`–`A4`, tooling `T1`–`T3`
- All 7 notebooks contaminated with boilerplate cells
- Math notebooks (A1-A4) should be self-contained reference material

### high_performance_python (4 notebooks)

**Issues:**
- Numbering gaps: Files are `02_`, `04_`, `05_`, `06_` — missing `01_` and `03_`
- 4 notebooks contaminated with boilerplate cells
- Not integrated into main module flow or mkdocs navigation

---

## Part IV: Scripts Deep Analysis (64 files)

### Utility Scripts (4)
| Script | Lines | Quality | Issues |
|---|---|---|---|
| `macro_utils.py` | 107 | Good | Missing type hints on return; `np.linalg.det(Z22) == 0` should use tolerance |
| `audit_notebooks.py` | 264 | Fair | **Bare `except:` on line 67**; generates large artifacts at root |
| `standardize_headers.py` | 54 | Fair | Bare `except Exception`; caused duplicate badge insertion; only adds badges, not Learning Objectives/Prerequisites |
| `fix_metadata.py` | 49 | Fair | No `__name__` guard; hardcodes Python `3.10.0`; hardcodes 5 specific notebook paths; one-off script — should be deleted after use |

### Image Generation Scripts — Deep Audit (53 `generate_*` scripts + 1 `create_*`)

#### Overview
- **53 `generate_*` scripts** + `create_causal_tree_diagram.py` = **54 total image scripts**
- Scripts use two rendering backends: **matplotlib** (34 scripts) and **graphviz** (20 scripts)
- **3 scripts** generate GIF animations requiring external `imagemagick`

#### A. MASSIVE DUPLICATION — **CRITICAL** (18 duplicate clusters)

Many images are generated by **2-4 independent scripts** that each produce slightly different versions of the same diagram, saving to different (often conflicting) paths:

| Image | # Duplicate Scripts | Scripts |
|---|---|---|
| **BGG Accelerator** | **4** | `generate_bgg_accelerator_diagram.py`, `generate_bgg_accelerator_flowchart.py`, `generate_diagram.py`, `generate_missing_images.py` |
| **Option Payoffs (Call/Put)** | **4** | `generate_option_payoff_diagram.py`, `generate_option_payoffs.py`, `generate_missing_images.py`, `generate_images.py` |
| **CML/SML Distinction** | **3** | `generate_cml_sml_diagram.py`, `generate_cml_sml_plot.py`, `generate_missing_images.py` |
| **Causal Tree Split** | **3** | `create_causal_tree_diagram.py`, `generate_causal_ml_images.py`, `generate_causal_tree_split_image.py` |
| **Cointegration** | **3** | `generate_cointegration_plot.py`, `generate_cointegration_viz.py`, `generate_missing_images.py` |
| **Gradient Field** | **3** | `generate_gradient_field_plot.py`, `generate_gradient_plot.py`, `generate_appendix_images.py` |
| **Convergence Rates** | **2** | `generate_convergence_plot.py`, `generate_appendix_images.py` |
| **CLT Dice Plots** | **2** | `generate_clt_plots.py`, `generate_appendix_images.py` |
| **Convex/Non-Convex Sets** | **2** | `generate_convex_plots.py`, `generate_appendix_images.py` |
| **Eigenvectors** | **2** | `generate_eigenvector_plot.py`, `generate_appendix_images.py` |
| **Jensen's Inequality** | **2** | `generate_jensen_plot.py`, `generate_appendix_images.py` |
| **Martingale Paths** | **2** | `generate_martingale_plot.py`, `generate_appendix_images.py` |
| **Multivariate Normal** | **2** | `generate_multivariate_normal_plot.py`, `generate_appendix_images.py` |
| **Normal PDF/CDF** | **2** | `generate_normal_dist_plots.py`, `generate_appendix_images.py` |
| **Comparative Statics** | **2** | `generate_comparative_statics_plot.py`, `generate_appendix_images.py` |
| **Aiyagari Loop** | **2** | `generate_aiyagari_diagram.py`, `generate_aiyagari_loop_diagram.py` |
| **Box-Jenkins** | **2** | `generate_box_jenkins_diagram.py`, `generate_box_jenkins_flowchart.py` |
| **Fama-MacBeth** | **2** | `generate_fama_macbeth_diagram.py`, `generate_missing_images.py` |
| **Merton Model** | **2** | `generate_merton_model_diagram.py`, `generate_merton_payoffs_diagram.py` |
| **Stochastic Process** | **2** | `generate_stochastic_plot.py`, `generate_stochastic_process_plot.py` — both save to `images/png/stochastic_process_realizations.png`; the latter has no `__name__` guard |
| **Time Series Split** | **2** | `generate_timeseries_split_plot.py`, `generate_timeseries_split_viz.py` — both save to `images/png/timeseries_split_visualization.png`; the former has no `__name__` guard and requires `sklearn` |
| **VAR Identification** | **2** | `generate_var_diagram.py`, `generate_var_identification_diagram.py` — different layouts of the same VAR identification concept; the former saves to correct module dir, the latter saves to root `images/` |

**Impact:** ~38 of 54 scripts are redundant. Only ~16 unique scripts are actually needed. The duplicate scripts often produce subtly different output (different DPI, style, labels) making it unclear which version is "canonical."

*Note: `generate_taylor_plot.py` (Taylor series sin(x) approximation) and `generate_stochastic_process_plot.py` also lack `__name__` guards and save to `images/png/` (legacy directory).*

#### B. BROKEN OUTPUT PATHS — **CRITICAL** (5 scripts)

These scripts construct save paths by joining a directory with a path that already starts with `images/`, creating deeply nested broken directories:

| Script | Broken Path Created | Intended Path |
|---|---|---|
| `generate_ml_intro_images.py` line 14 | `images/ml_intro/images/png/figure1_...` | `images/07-Machine-Learning/figure1_...` |
| `generate_option_payoffs.py` line 61 | `images/finance/options/images/png/call_put_payoffs.png` | `images/09-Finance/call_put_payoffs.png` |
| `generate_merton_payoffs_diagram.py` line 61 | `images/images/png/merton_model_payoffs.png` | `images/09-Finance/merton_model_payoffs.png` |
| `generate_ito_lemma_viz.py` line 78 | `images/finance/images/png/ito_lemma_intuition.png` | `images/09-Finance/ito_lemma_intuition.png` |
| `generate_lob_plot.py` line 63 | `images/finance/images/png/limit_order_book.png` | `images/09-Finance/limit_order_book.png` |

#### C. BUGS IN SCRIPTS — **HIGH**

| Script | Bug | Impact |
|---|---|---|
| `generate_box_jenkins_diagram.py` line 10 | Uses `/n` instead of `\n` in node text | Literal `/n` rendered in diagram instead of newlines |
| `generate_box_jenkins_flowchart.py` line 13 | Uses `/n` instead of `\n` in node text | Same issue |
| `generate_diagram.py` line 34 | `os.rename()` on a file graphviz already created with `.png` extension | `FileExistsError` on second run |
| `generate_appendix_images.py` line 63 | `save_plot(fig, "images/png/convergence_rates.png")` ignores its own `OUTPUT_DIR = "images/appendix"` | Images save to wrong directory |

#### D. INCONSISTENT OUTPUT DIRECTORIES — **HIGH**

Scripts save to **14+ different directory schemes** instead of a uniform module-based structure:

| Directory Pattern | # Scripts | Examples |
|---|---|---|
| `images/png/` (legacy catch-all) | ~20 | Most standalone scripts |
| `images/<module>/` (correct) | ~10 | `generate_rl_loop_diagram.py`, `generate_centrality_diagram.py` |
| `images/` root level | ~5 | `generate_bgg_accelerator_diagram.py`, `generate_box_jenkins_diagram.py` |
| `images/finance/` | 2 | `generate_ito_lemma_viz.py`, `generate_lob_plot.py` |
| `images/finance/options/` | 2 | `generate_binomial_tree_viz.py`, `generate_option_payoffs.py` |
| `images/ml_intro/` | 1 | `generate_ml_intro_images.py` |
| `images/causal_ml/` | 1 | `generate_causal_ml_images.py` |
| `images/appendix/` | 1 | `generate_appendix_images.py` (but doesn't actually save there) |

#### E. MISSING `if __name__ == '__main__'` GUARD — **MEDIUM** (7 scripts)

These scripts execute on import, which breaks any attempt to use them as modules:
- `generate_clt_plots.py`
- `generate_cml_sml_diagram.py`
- `generate_comparative_statics_plot.py`
- `generate_convergence_plot.py`
- `generate_eigenvector_plot.py`
- `generate_merton_model_diagram.py`
- `generate_box_jenkins_diagram.py`

#### F. STYLE INCONSISTENCIES — **MEDIUM**

| Issue | Scripts Affected |
|---|---|
| `plt.style.use('seaborn-v0_8-whitegrid')` vs `sns.set_style("whitegrid")` | Mixed across all |
| DPI varies: 150 vs 300 | Mixed (some have no DPI setting at all) |
| `np.random.seed()` (legacy) vs `np.random.default_rng()` | Mixed |
| Font sizes vary: 10, 12, 14, 16 for same element types | All |
| Some use function wrapping, some are top-level scripts | ~15 top-level |
| Some have docstrings, most don't | ~30 missing |

#### G. DEPENDENCY GAPS — **HIGH**

| Dependency | # Scripts Needing It | In `environment.yml`? |
|---|---|---|
| **graphviz** (Python + system binary) | 18 | ❌ No |
| **networkx** | 2 (`generate_animation.py`, `generate_contagion_animation.py`) | ❌ No |
| **numba** | 1 (`generate_aiyagari_animation.py`) | ❌ No |
| **imagemagick** (external) | 3 (animation scripts) | ❌ No (system dependency) |
| **scikit-learn** | 1 (`generate_ml_intro_images.py`) | In env.yml but not requirements.txt |
| **pandas_datareader** | 1 (`generate_phillips_curve_diagram.py`) | ❌ Not imported but in source |

#### H. SCRIPTS THAT ARE WELL-WRITTEN (keep as canonical)

| Script | Quality | Notes |
|---|---|---|
| `generate_images.py` | Good | Well-structured orchestrator, but only covers 3 modules |
| `generate_appendix_images.py` | Good | Has helper functions `setup_plot`/`save_plot`, good code quality (but saves to wrong dirs) |
| `generate_phillips_curve_diagram.py` | Good | Includes metadata tracking, clean code |
| `generate_centrality_diagram.py` | Good | Clean graphviz diagram |
| `generate_emergence_diagram.py` | Good | Clean graphviz diagram |
| `generate_ordered_dict_diagram.py` | Good | Well-documented |
| `generate_rl_loop_diagram.py` | Good | Clean, simple |
| `generate_ml_intro_images.py` | Fair | Good content (bias-variance, lasso/ridge geometry) but broken save path |
| `generate_contagion_animation.py` | Fair | Solid financial contagion simulation, needs dep fixes |

#### Recommended Action: Consolidation Plan

1. **Delete ~38 redundant scripts** — keep only the best version from each of the 18 duplicate clusters
2. **Fix 5 broken save paths** — use consistent `images/<module>/` pattern
3. **Fix 4 code bugs** — `/n` → `\n`, rename race condition, wrong output dir
4. **Add `__name__` guards** to 7 scripts
5. **Create `scripts/generate_all_images.py`** — unified runner that imports and calls all canonical scripts
6. **Standardize style** — uniform DPI (300), `plt.style.use('seaborn-v0_8-whitegrid')`, `rng = np.random.default_rng(42)`
7. **Add `graphviz` and `imagemagick`** to dependencies and README setup instructions
8. **Target: reduce from 54 scripts to ~15-18 canonical scripts**

### Data Download Scripts (4)
| Script | Purpose | Issues |
|---|---|---|
| `download_images.py` | Downloads historical images | Hardcoded URLs; only 2 images in manifest; saves to `images/png/` (legacy dir) |
| `download_industry_portfolios.py` | Fama-French data | Requires `pandas_datareader`; no `__name__` guard; no caching |
| `download_portfolio_data.py` | Portfolio + FF factors | Requires `yfinance` + `pandas_datareader`; no `__name__` guard |
| `download_sp500.py` | S&P 500 data | **Saves as `SP500.csv` (uppercase)** — root cause of the case mismatch bug; requires `yfinance` + `pandas_datareader`; no `__name__` guard |

**Gap:** No download script exists for the 6 FRED CSV files (`CPIAUCSL.csv`, `DPIC96.csv`, `FEDFUNDS.csv`, `GDPC1.csv`, `INDPRO.csv`, `PCECC96.csv`). These were presumably downloaded manually or via the `fredapi` library used in `01-Foundations/15_APIs_and_Data_Sources.ipynb`. No provenance tracking.

### Model Solution Scripts (2)
| Script | Purpose | Issues |
|---|---|---|
| `solve_bgg_model.py` | Standalone BGG solver | **NON-FUNCTIONAL**: returns empty DataFrame on line 74 with warning "DSGE solver not configured". Lines 76-98 are **unreachable code** after `return`. References non-existent `pysnowdrop` library in error message (line 96). Entire script is a placeholder/template |
| `bgg_illustrative_solver.py` | Simplified BGG with handcrafted matrices | Works correctly; uses illustrative calibration. Could be merged with notebook import |

### One-Off / Maintenance Scripts (1)
| Script | Purpose | Issues |
|---|---|---|
| `fix_metadata.py` | Fixes kernel metadata for 5 specific notebooks | No `__name__` guard; hardcodes Python `3.10.0`; hardcodes specific notebook paths; one-off script that should be deleted after use |

---

## Part V: Comprehensive Improvement Plan

### Phase 0: Emergency Fixes (Estimated: 5-8 hours) — ✅ COMPLETED

All 15 tasks implemented. `.gitignore`, `.pre-commit-config.yaml`, and `.gitattributes` were found to already exist (hidden dotfiles missed by initial scan).

| # | Task | Files | Priority |
|---|---|---|---|
| 0.1 | **🔴 SECURITY: Remove `polyfill.io` CDN** — compromised domain serving malware since June 2024. MathJax v3 does not need it. Delete line 130 from `mkdocs.yml` | `mkdocs.yml` | **CRITICAL — SECURITY** |
| 0.2 | Fix README env name `my-research-env` → `computational-economics` | `README.md` | **Critical** |
| 0.3 | Remove duplicate `tqdm` from `environment.yml` | `environment.yml` | Critical |
| 0.4 | Remove/fix `pysinc` from `environment.yml` (non-existent package) | `environment.yml` | Critical |
| 0.5 | **Add ALL 17 missing packages** to `environment.yml` and `requirements.txt`: `tensorflow`, `torch`, `xgboost`, `networkx`, `numba`, `ipywidgets`, `graphviz`, `shap`, `sympy`, `dask`, `cupy`, `doubleml`, `econml`, `pymc`, `emcee`, `fredapi`, `otter-grader` | `environment.yml`, `requirements.txt` | **Critical** |
| 0.6 | **Sync `requirements.txt`** — add 11 packages present in `environment.yml` but missing: `scikit-learn`, `statsmodels`, `arch`, `linearmodels`, `nashpy`, `prophet`, `pysal`, `geopandas`, `gymnasium`, `cvxpy`, `joblib` | `requirements.txt` | **Critical** |
| 0.7 | Remove unused `pyportfolioopt` from `environment.yml` (never imported) | `environment.yml` | Low |
| 0.8 | ~~Delete committed `01-Foundations/__pycache__/`~~ ✅ **DONE** — `.gitignore` already existed (235 lines, hidden dotfile missed by scan) | `01-Foundations/`, root | **Critical** |
| 0.9 | Fix bare `except:` in `scripts/audit_notebooks.py` line 67 → `except (SyntaxError, ValueError):` | `scripts/audit_notebooks.py` | Medium |
| 0.10 | Fix bare `except:` in `05-Micro-Models/02_General_Equilibrium.ipynb` | Notebook | Medium |
| 0.11 | **Fix `SP500.csv` case mismatch** — rename reference in GARCH notebook to `sp500.csv` (Linux/macOS will fail) | `08-Time-Series/05_Volatility_Modeling_ARCH_GARCH.ipynb` | High |
| 0.12 | **Fix cell ordering bug** — `02-NM/04_Root_Finding.ipynb` has code cell before imports cell | Notebook | High |
| 0.13 | **Fix `contributing.md` env name** — says `conda activate computational-econ` but should be `computational-economics` | `docs/about/contributing.md` | Medium |
| 0.14 | **Remove `playwright` from `requirements.txt`** — browser automation tool, development artifact not needed for course | `requirements.txt` | Low |
| 0.15 | **Fix `download_sp500.py`** — saves as `SP500.csv` (uppercase), root cause of case mismatch; change to `sp500.csv` | `scripts/download_sp500.py` | High |

### Phase 1: Boilerplate & Placeholder Cleanup (Estimated: 8-12 hours) — ✅ PARTIALLY COMPLETED

**196 boilerplate cells removed** from 44+ notebooks via `scripts/cleanup_boilerplate.py`:
- All "Concept Overview" cells removed
- All "Implementation Detail" cells removed
- All unfilled "Summary" template cells removed
- All unfilled "The Lens" template cells removed
- All "(Introduction text to be added)" placeholder cells removed

Remaining: 1.6 (badge dedup), 1.7 (header standardization), 1.9 (plt.savefig removal), 1.10 (os.makedirs removal)

| # | Task | Files | Priority |
|---|---|---|---|
| 1.1 | **Remove all "Concept Overview" boilerplate cells** from 22 contaminated notebooks | 22 notebooks in 09-Finance, 10-Specialized, Appendix, high_performance_python | **Critical** |
| 1.2 | **Remove all "Implementation Detail" boilerplate cells** | Same 22 notebooks | **Critical** |
| 1.3 | **Remove all unfilled "The Lens" template cells** (`"Provide a brief overview of the economic context..."`) | **19 notebooks** in 07-ML, 08-TS | **Critical** |
| 1.4 | **Remove all unfilled "Summary" template cells** (`"Key takeaway 1 / Key takeaway 2"`) | **25 notebooks** in 07-ML, 08-TS, 09-Finance | **Critical** |
| 1.5 | **Fill all `"(Introduction text to be added)"` placeholders** with real introductory content | **12 notebooks** in 06-Econometrics, 07-ML, Appendix | **Critical** |
| 1.6 | ~~**De-duplicate license badges**~~ ✅ **DONE** — final 3 notebooks (04-Macro `03B`/`03C`/`03D`) merged to the single-line badge convention; `test_no_duplicate_badges` now passes project-wide | ~20+ notebooks in modules 05-10 | High |
| 1.7 | **Standardize header format** — remove redundant module name prefix from cell 0 | All notebooks | Medium |
| 1.8 | Complete incomplete ToC in `06-Econometrics/03_Causal_Inference.ipynb` | 1 notebook | High |
| 1.9 | **Remove `plt.savefig()` calls** from all 16 notebooks that write to disk. Keep inline `plt.show()` only | 16 notebooks across 7 modules | High |
| 1.10 | **Remove `os.makedirs` for image dirs** from notebook code cells | 15 notebooks | High |

### Phase 2: Structural Standardization (Estimated: 8-12 hours)

Apply the PEDAGOGY.md "The Lens" structure to all notebooks:

| # | Task | Files | Priority |
|---|---|---|---|
| 2.1 | **Add Learning Objectives** to all 101 notebooks missing them | 101 notebooks | **High** |
| 2.2 | **Add Prerequisites** to all 104 notebooks missing them | 104 notebooks | **High** |
| 2.3 | **Add References / Further Reading** to all 90 notebooks missing them | 90 notebooks | High |
| 2.4 | **Add Exercises** to the ~31 notebooks missing them (min 3 per notebook: Conceptual, Applied, Challenge) | ~31 notebooks | High |
| 2.5 | **Add Colab badges** to all 113 notebooks | All notebooks | Medium |
| 2.6 | **Add Binder badges** to all 113 notebooks | All notebooks | Medium |
| 2.7 | **Upgrade `standardize_headers.py`** to handle all structural elements (Objectives, Prerequisites, badges) and prevent duplicate insertion | `scripts/standardize_headers.py` | High |

### Phase 3: Infrastructure Repair (Estimated: 8-12 hours) — ✅ PARTIALLY COMPLETED

Completed: CI actions updated to v4, 3 mkdocs plugins configured, `.pre-commit-config.yaml` updated (already existed), `requirements-docs.txt` already existed, `pyproject.toml` created, `ci.yml` workflow created, 57 docs stub pages created, `contributing.md` linter refs fixed, `datasets.md` corrected, `structure.md` expanded.

| # | Task | Priority |
|---|---|---|
| 3.1 | **Create `scripts/build_docs.py`** — notebook-to-markdown conversion script using `nbconvert`, outputting to `docs/modules/` structure matching `mkdocs.yml` | **Critical** |
| 3.0a | ~~**Create all 45+ missing docs pages**~~ ✅ **DONE** — 57 stub pages created via `scripts/create_docs_stubs.py` | **Critical** |
| 3.0b | ~~**Remove `polyfill.io` from `mkdocs.yml`**~~ ✅ **DONE** — verified absent; was already removed in Phase 0 | **Critical** |
| 3.0c | ~~**Fix `docs/about/contributing.md`**~~ ✅ **DONE** — `validate_notebooks.py` refs were actually `audit_notebooks.py` (correct); replaced `flake8` with `ruff`/`black` | High |
| 3.0d | ~~**Fix `docs/resources/datasets.md`**~~ ✅ **DONE** — removed non-existent `UNRATE.csv`, added `us_macro.csv` + `fama_french_factors.csv`, fixed `SP500.csv` → `sp500.csv` | High |
| 3.0e | ~~**Expand `docs/getting-started/structure.md`**~~ ✅ **DONE** — expanded from 20 lines to 85 lines with module tables, learning paths, repo layout | Medium |
| 3.2 | **Generate all missing `docs/modules/` pages** — create index files and converted content | **Critical** |
| 3.3 | **Generate missing `docs/appendices/` pages** | **Critical** |
| 3.4 | **Fix CI deploy workflow** — use `requirements-docs.txt`, add conversion step | High |
| 3.5 | ~~**Create `pyproject.toml`**~~ ✅ **DONE** — created with black, ruff, pytest config | High |
| 3.6 | ~~**Create `.pre-commit-config.yaml`**~~ ✅ **DONE** — file already existed; updated versions to pre-commit-hooks v5.0, black 24.10, ruff v0.8 | High |
| 3.7 | ~~**Add CI workflow for linting + tests**~~ ✅ **DONE** — created `.github/workflows/ci.yml` with lint, test, and validate-notebooks jobs | High |
| 3.7a | ~~**Update CI action versions**~~ ✅ **DONE** — `actions/cache@v3` → `v4`, `peaceiris/actions-gh-pages@v3` → `v4` | Medium |
| 3.7b | ~~**Clean up CI plugin installs**~~ ✅ **DONE** — configured `minify`, `glightbox`, `redirects` in `mkdocs.yml`; CI now uses `requirements-docs.txt` | Low |
| 3.8 | **Add CI workflow for notebook validation** — `pytest --nbval-lax` | Medium |
| 3.9 | **Create Binder configuration** — `binder/` with `environment.yml` and `postBuild` | Medium |
| 3.10 | ~~**Add CC BY 4.0 license file**~~ ✅ **ALREADY EXISTS** — `LICENSE` contains both MIT + CC BY 4.0 full text | Medium |
| 3.11 | ~~**Fill `docs/getting-started/prerequisites.md`**~~ ✅ **DONE** — expanded from 40 to 103 lines with self-assessment, module-level requirements table | Low |
| 3.12 | ~~**Fill `docs/getting-started/structure.md`**~~ ✅ **DONE** (see 3.0e) | Low |
| 3.13 | ~~**Expand `docs/resources/datasets.md`**~~ ✅ **DONE** — all 13 data files documented with sources; also created `data/README.md` with full provenance table | Medium |

### Phase 4: Testing Infrastructure (Estimated: 4-6 hours) — ✅ PARTIALLY COMPLETED

Completed: `tests/conftest.py` with shared fixtures, `tests/test_notebooks.py` with 4 regression tests, plus analytic test suites for the three core numerical modules (52 tests, all passing).

> **🔴 Bug found and fixed by 4.3:** `solve_qz` in `scripts/macro_utils.py` derived the
> policy as `-inv(Z22) @ Z21`, based on the premise `y = Z x`. scipy's `ordqz`
> convention (`AA = Q S Zᵀ`) implies `y = Zᵀ x`, so the correct Klein (2000)
> formulas are `Policy = Z21 @ inv(Z11)` and `Transition = Z11 @ inv(S11) @ T11 @ inv(Z11)`.
> The error is invisible for scalar state/control blocks but wrong — including
> sign flips — for multi-dimensional systems: on the course's own RBC model the
> old policy was `[-0.58, -0.34]` vs the correct `[0.55, 0.39]`, with an
> equilibrium-condition residual of 0.18 (vs machine epsilon after the fix).
> The four affected notebooks (04-Macro `03B`/`03C`/`03D`, 09-Finance `07_BGG`)
> were re-executed with the corrected solver.

| # | Task | Priority |
|---|---|---|
| 4.1 | ~~**Create `conftest.py`**~~ ✅ **DONE** — shared fixtures for paths, tolerances, sample data, notebook discovery | High |
| 4.2 | ~~**Write tests for `dp_solver.py`**~~ ✅ **DONE** — closed-form benchmarks (geometric series, hand-solved 2-state MDP), contraction/monotonicity/fixed-point properties, VFI-PFI agreement, input validation (`tests/test_dp_solver.py`, 20 tests) | High |
| 4.3 | ~~**Write tests for `macro_utils.py`**~~ ✅ **DONE** — analytic saddle-path benchmarks incl. multi-dimensional eigenvector ground truth, equilibrium residuals, transition spectrum, Blanchard-Kahn warnings (`tests/test_macro_utils.py`, 13 tests). **Found and fixed a real solver bug — see note above** | High |
| 4.4 | ~~**Write tests for `macro_vfi_utils.py`**~~ ✅ **DONE** — row-stochasticity, grid bounds/symmetry, exact i.i.d. bin masses, stationary mean/variance and implied autocorrelation vs the underlying AR(1) (`tests/test_macro_vfi_utils.py`, 15 tests) | High |
| 4.5 | **Add smoke tests** for key models: BGG model, Schelling convergence, CES equilibrium | Medium |
| 4.6 | **Add `nbval` config** for lightweight notebook execution testing | Medium |

### Phase 5: Data & File Organization (Estimated: 3-5 hours) — ✅ PARTIALLY COMPLETED

Completed: data file rename, `data/README.md`, debug file moves, artifact moves, `.gitattributes` enhanced, FRED download script created, `fix_metadata.py` and `solve_bgg_model.py` deleted.

| # | Task | Priority |
|---|---|---|
| 5.1 | ~~**Rename `beijin_data.dta` → `beijing_data.dta`**~~ ✅ **DONE** — renamed + updated `datasets.md` | Low |
| 5.2 | ~~**Create `data/README.md`**~~ ✅ **DONE** — documents all 13 datasets with sources | Medium |
| 5.3 | ~~**Move debug files**~~ ✅ **DONE** — moved to `scripts/` | Medium |
| 5.4 | ~~**Move/gitignore audit artifacts**~~ ✅ **DONE** — `notebook_structure.md`, `notebook_structure_report.json` moved to `scripts/` | Medium |
| 5.5 | ~~**Move `image_path_mapping.json`**~~ ✅ **DONE** — moved to `scripts/` | Low |
| 5.6 | **Consolidate planning docs** into `docs/internal/` or archive | Low |
| 5.7 | **Evaluate Git LFS** for `SEntFiN.csv` (1.1MB), `beijin_data.dta` (2.7MB), `sp500.csv` (597KB) | Low |
| 5.8 | ~~**Create `.gitattributes`**~~ ✅ **DONE** — file already existed (1 line); enhanced with notebook diff, LF enforcement, binary markers | Medium |
| 5.9 | ~~**Create FRED download script**~~ ✅ **DONE** — created `scripts/download_fred_data.py` using `pandas-datareader` | Medium |
| 5.10 | ~~**Delete or archive `fix_metadata.py`**~~ ✅ **DONE** — deleted | Low |
| 5.11 | ~~**Delete or archive `solve_bgg_model.py`**~~ ✅ **DONE** — deleted | Low |
| 5.12 | **Update `docs/IMAGE_CATALOG.md`** — stale; only 5 of 300+ images cataloged; paths don't match actual directory structure | Low |

### Phase 6: Image Pipeline Overhaul & Broken Image Repair (Estimated: 10-16 hours) — ✅ PARTIALLY COMPLETED

Completed: 6.1 (57 zero-byte images deleted), 6.2 (5 empty/legacy dirs removed, eigenvectors.gif relocated), 6.7 (12 redundant scripts deleted, reduced from 53 to 41), 6.8 (5 broken save paths), 6.9 (4 code bugs), 6.10 (4 `__name__` guards), 6.12 (19 scripts redirected from `images/png/` to module dirs). Also fixed invalid JSON escapes in 2 notebooks.

**Sub-phase 6A: Broken Image Cleanup**

| # | Task | Priority |
|---|---|---|
| 6.1 | ~~**Delete all 57 zero-byte image files**~~ ✅ **DONE** — all 57 removed | **Critical** |
| 6.2 | ~~**Delete duplicate image directory schemes**~~ ✅ **PARTIALLY DONE** — removed `gif/`, `machine_learning/`, `micro_macro/`, 3 empty module dirs; `jpg/`, `png/`, `svg/` retained (contain real content needing notebook ref updates) | **Critical** |
| 6.3 | **Regenerate/source all broken module images** — modules 02, 03, 04, 05 have zero valid images. Either generate via scripts or source from appropriate references | **High** |
| 6.4 | **Source historical photos** — `1.1-eniac-programmers`, `1.1-robert-lucas`, `1.1-william-petty`, etc. are 0-byte. Re-download or replace with public domain alternatives | High |
| 6.5 | **Cross-reference audit** — verify all 85 notebook image references point to existing, non-empty files | High |
| 6.6 | **Clean up `images/metadata.json`** (56 KB) — determine if still needed or stale | Low |

**Sub-phase 6B: Script Consolidation (see Part IV §A-H for full details)**

| # | Task | Priority |
|---|---|---|
| 6.7 | ~~**Delete redundant image scripts**~~ ✅ **PARTIALLY DONE** — 12 scripts deleted (stochastic_plot, cml_sml_diagram, timeseries_split_viz, bgg_accelerator_diagram/flowchart, box_jenkins_flowchart, aiyagari_loop_diagram, merton_model_diagram, option_payoff_diagram, cointegration_plot, missing_images, images); reduced from 53 to 41 | **Critical** |
| 6.8 | ~~**Fix 5 broken save paths**~~ ✅ **DONE** — all 5 scripts corrected to save in module-based directories | **Critical** |
| 6.9 | ~~**Fix 4 code bugs**~~ ✅ **DONE** — `/n`→`\n` in 2 box-jenkins scripts, `os.rename` race removed, `OUTPUT_DIR` casing fixed | **High** |
| 6.10 | ~~**Add `if __name__ == '__main__'` guards**~~ ✅ **DONE** — 4 critical module-level scripts wrapped (box_jenkins_diagram, stochastic_process_plot, taylor_plot, timeseries_split_plot) | High |
| 6.11 | **Standardize all remaining scripts** — uniform DPI (300), `plt.style.use('seaborn-v0_8-whitegrid')`, `rng = np.random.default_rng(42)`, consistent font sizes | Medium |
| 6.12 | ~~**Redirect all output paths to module-based directories**~~ ✅ **DONE** — 19 scripts + 2 download manifest entries redirected from `images/png/` to module-based dirs | High |
| 6.13 | **Create `scripts/generate_all_images.py`** — unified runner that imports and calls all ~15 canonical scripts | High |
| 6.14 | **Add `graphviz` (Python package + system binary) and `imagemagick`** to dependencies and README setup instructions | High |
| 6.15 | **Add docstrings** to all remaining canonical image scripts | Low |

**Target: reduce from 54 image scripts to ~15-18 canonical scripts**

### Phase 7: Code Quality Pass (Estimated: 8-12 hours) — ✅ PARTIALLY COMPLETED

Completed: 7.3 (deprecated boston_housing replaced), 7.4 (sys.path.append fixed), 7.5 (no TODO/FIXME items in source), 7.7 (10 ML notebooks import-guarded).

| # | Task | Scope | Priority |
|---|---|---|---|
| 7.1 | **Add type hints** to all major functions in all notebooks | 104 notebooks lacking them | Medium |
| 7.2 | **Add NumPy-style docstrings** to all public functions | All notebooks | Medium |
| 7.3 | ~~**Replace deprecated APIs**~~ ✅ **DONE** — `boston_housing` → `fetch_california_housing` in `06_Deep_Learning_Foundations.ipynb` | ML notebooks | High |
| 7.4 | ~~**Fix `sys.path.append` usage**~~ ✅ **DONE** — converted to `sys.path.insert(0, ...)` + added try/except in `03B_RBC_Model_Solution.ipynb` and `07_Financial_Frictions_BGG.ipynb` | 09-Finance, 04-Macro | Medium |
| 7.5 | ~~**Resolve TODO/FIXME items**~~ ✅ **DONE** — verified 0 TODO/FIXME items in any notebook source cell (original 7 were in output blobs, not code) | 7 notebooks | Medium |
| 7.6 | **Vectorization audit** — replace explicit loops with NumPy operations where possible | Focus on 10-Specialized-Models ABMs | Medium |
| 7.7 | ~~**Add `try/except ImportError` guards**~~ ✅ **DONE** — 10 ML notebooks wrapped with `try/except` + `TENSORFLOW_AVAILABLE` flag via `scripts/add_import_guards.py` | All notebooks using optional deps | High |

### Phase 8: Content Enhancement (Estimated: 20-30 hours)

| # | Task | Module | Priority |
|---|---|---|---|
| 8.1 | **Split oversized notebooks** (>150 KB): RBC (split into 03A/03B/03C), Discrete-Continuous DP (split into 03A/03B), VAR (160 KB), MLE (145 KB) | 03, 04, 06, 08 | High |
| 8.2 | ~~**Expand `02_General_Equilibrium.ipynb`**~~ ✅ **DONE** — see 12.5; adds the Edgeworth box, both welfare theorems, and a computed contract curve with the equilibrium, budget line, and tangent indifference curves plotted | 05 | High |
| 8.3 | **Add `ipywidgets` interactivity** to at least 1 notebook per module (currently only 9/113 have it) | All modules | Medium |
| 8.4 | **Add staggered adoption / Callaway-Sant'Anna** to DiD notebook | 06 | Medium |
| 8.5 | **Integrate `nashpy`** in Game Theory notebook | 05 | Medium |
| 8.6 | **Deepen Causal ML** with `DoubleML` | 07 | Medium |
| 8.7 | **Fix numbering in Appendix** — resolve two "01" files | Appendix | Low |
| 8.8 | **Fix numbering in high_performance_python** — fill gaps (01, 03) | HPP | Low |
| 8.9 | **Cross-reference links** between related notebooks ("Red Thread") | All modules | Low |
| 8.10 | **Create `scripts/data_loader.py`** — unified data fetching with caching per INFRASTRUCTURE.md | scripts/ | Medium |

### Phase 9: Advanced & Polish (Estimated: 10-15 hours)

| # | Task | Priority |
|---|---|---|
| 9.1 | **Create `_quarto.yml`** for Quarto book rendering | Medium |
| 9.2 | **Math-Code Parity audit** — ensure LaTeX equations immediately precede code; variable names match notation | Medium |
| 9.3 | **Plot style standardization** — consistent colorblind-safe palettes across all notebooks | Low |
| 9.4 | **Ensure Colab compatibility** — no hard-coded local paths, add `!pip install` cells where needed | Medium |
| 9.5 | **Add otter-grader integration** for autograding exercises | Low |
| 9.6 | **Consolidate planning docs** — merge FULL_ROADMAP, IMPROVEMENT_PLAN, INFRASTRUCTURE, PEDAGOGY into a single DEVELOPMENT_GUIDE.md | Low |

### Phase 10: Redundancy & Overlap Resolution (Estimated: 12-16 hours)

Addresses audit findings §I. For each overlap, designate one **canonical notebook** as the authoritative source and convert all other occurrences to brief recaps with cross-reference links.

| # | Task | Priority |
|---|---|---|
| 10.1 | **OLS overlap** — canonical: `06-Econometrics/01`. In 01-Foundations/12_NumPy and 02-NM/01_Linear_Algebra, replace full derivations with 2-line recap + link. In 07-ML/01, reference back | High |
| 10.2 | **Contraction Mapping** — canonical: `Appendix/A1-Real-Analysis` (full proof). In 01-Intro and 02-NM/04, use statement-only + link. In 03-EM/01, recall + apply | High |
| 10.3 | **Newton-Raphson** — canonical: `02-NM/04_Root_Finding`. Remove redundant re-derivations from 01-Foundations/20_SciPy and 02-NM/03_Differentiation | High |
| 10.4 | **Tauchen discretization** — canonical: `04-Macro-Models/macro_vfi_utils.py`. All notebooks import from utility; remove inline re-implementations | High |
| 10.5 | **Bellman equation** — canonical: `03-EM/01_Dynamic_Programming`. All subsequent uses reference back; only re-state the specific variant needed | High |
| 10.6 | **Monte Carlo** — canonical: `02-NM/07_Numerical_Integration`. Finance/HPC notebooks import or recap, not re-derive | Medium |
| 10.7 | **VAR overlap** — merge or clearly delineate `06-Econometrics/09` (estimation focus) vs `08-TS/04` (IRF/structural focus). Add cross-links | High |
| 10.8 | **PSM overlap** — `06-Econometrics/03` owns PSM theory. `07-ML/17_Causal_ML` references back and focuses on DML/forests | Medium |
| 10.9 | **Euler equation** — canonical derivation in `03-EM/02_DP_Continuous`. Macro notebooks recall + specialize | Medium |
| 10.10 | **BGG scripts** — merge `solve_bgg_model.py` and `bgg_illustrative_solver.py` into one; notebook imports it | Medium |

### Phase 11: Writing Quality & Proofreading (Estimated: 15-20 hours)

Addresses audit findings §K. Systematic pass over all 113 notebooks.

| # | Task | Priority |
|---|---|---|
| 11.1 | **Spelling & grammar pass** — every markdown cell in all 113 notebooks | High |
| 11.2 | **Standardize authorial voice** — adopt first-person plural ("We derive…") consistently across all notebooks | High |
| 11.3 | **Break dense text walls** — split any markdown cell >300 words into smaller cells with equations, bullet lists, or diagrams between paragraphs | High |
| 11.4 | **Add bridging sentences** — every code cell must be preceded by a markdown cell stating what the code does and why | High |
| 11.5 | **Define all notation** — audit every equation; ensure every symbol is defined before or immediately after first use (e.g., "where $\xi \in [x_n, x^*]$ by the Mean Value Theorem") | High |
| 11.6 | **Eliminate placeholder text** — fill all `"(to be added)"` stubs with real content | Critical |
| 11.7 | **Fix cell ordering** — ensure imports always precede code that uses them (e.g., `04_Root_Finding.ipynb` cell 1/2 swap) | Critical |

### Phase 12: Content Deepening — Proofs, Derivations & Rigor (Estimated: 25-35 hours)

Addresses audit findings §L. Expand shallow content into graduate-level depth.

| # | Task | Priority |
|---|---|---|
| 12.1 | ~~**Add formal Big-O definition** + $\Omega$/$\Theta$ + P vs NP discussion~~ ✅ **DONE** (in `22A_Computational_Complexity_Foundations`) — formal $O$/$\Omega$/$\Theta$ definitions with a worked proof from the definition, the tightness trap ($3n^2 = O(n^3)$ is true), worst/average/best-case as an orthogonal axis, the P/NP/NP-hard/NP-complete definitions and class chain, and a table of NP-hard problems in economics (combinatorial auctions, PPAD-complete Nash, matching) closing with complexity as the formal backbone of bounded rationality | Medium |
| 12.2 | ~~**Deduplicate Halley's method**~~ ✅ **DONE** — removed the duplicated Halley block; added a complete convergence-rate derivation for Bisection ($n \ge \log_2((b-a)/\varepsilon)-1$), a full proof of Newton's local quadratic convergence (Taylor + Lagrange remainder, stated as a theorem), and a from-scratch derivation of Halley's update from the 2nd-order Taylor expansion; expanded Brent's method with the IQI formula, the accept/reject safeguards, and the convergence-order rationale for the hybrid | High |
| 12.3 | ~~**Add Principle of Optimality proof**~~ ✅ **DONE** — full proof (two-inequality sandwich argument) that the sequence-problem value function satisfies the Bellman equation, a converse verification theorem establishing uniqueness among bounded functions, and the one-line stochastic extension via the law of iterated expectations; cross-referenced to the Contraction Mapping Theorem in `Appendix/A1-Real-Analysis` | High |
| 12.4 | ~~**Add full Lagrangian/Hamiltonian Euler equation derivation**~~ ✅ **DONE** — complete continuous-time derivation (current-value Hamiltonian → Keynes-Ramsey rule, with the CRRA algebra spelled out) matching the `RCKModel.system_dynamics` code line-for-line, plus the discrete-time sequential-Lagrangian derivation of the Euler equation used by Section 3's stochastic VFI code | High |
| 12.5 | ~~**Add Edgeworth Box, Welfare Theorems, Brouwer existence proof**~~ ✅ **DONE** — new §1 with the Edgeworth box and a closed-form contract curve derived from the tangency condition, Walras' Law with proof (and why solvers search $N-1$ prices), the First Welfare Theorem proved by contradiction, the Second via separating hyperplanes with the role of convexity made explicit, and existence via Brouwer applied to the Gale-Nikaido price map — including the sum-of-squares argument showing a fixed point clears every market. Paired with an executed Edgeworth-box figure whose assertions verify the First Welfare Theorem numerically (the equilibrium lands on the contract curve) | High |
| 12.6 | ~~**Enable graphviz DAGs** + add d-separation + do-calculus intro~~ ✅ **DONE** — added §2.3 with the formal d-separation definition, the chain/fork/collider blocking table, the precisely-restated backdoor criterion, the do-operator's observational-vs-interventional distinction, and the Backdoor Adjustment Formula derived via truncated factorization — closing the loop to why Propensity Score Matching (§3) is justified. (Graphviz was already dynamically `try/except`-guarded, not hardcoded `False`) | High |
| 12.7 | ~~**Add within-estimator derivation**~~ ✅ **DONE** — added §2.1 deriving the within estimator from the annihilator matrix $Q$ (with its symmetry/idempotency/constant-killing properties proved), the closed-form estimator and its consistency under strict exogeneity, why time-invariant regressors are *not identified* rather than merely imprecise, the FWL equivalence to LSDV, the degrees-of-freedom trap that makes manual demeaning + generic OLS understate variance, and random effects as quasi-demeaning with FE as the $\theta \to 1$ limit | Medium |
| 12.8 | ~~**Add Universal Approximation Theorem** statement + proof sketch~~ ✅ **DONE** — added the missing §1.1 "Theoretical Foundations" section (which the ToC already linked to but did not exist): formal Cybenko/Hornik statement, constructive 4-step proof sketch (sigmoid→step→bump→staircase, closed by uniform continuity), a caveats table separating what the theorem does and does not guarantee, the depth-vs-width separation results, and the economist's reading as a non-parametric estimator | Medium |
| 12.9 | ~~**Add unit root testing** (ADF, PP, KPSS)~~ ✅ **DONE** (in `08-Time-Series/01_Introduction`) — added §3 deriving the Dickey-Fuller reparameterization, explaining why the critical values are non-standard (super-consistency and the Brownian-functional limit) and why a $t$-table over-rejects, the three deterministic specifications, the ADF augmentation and lag-selection trade-off, Phillips-Perron contrasted in a table, KPSS's reversed null, and the four-outcome ADF×KPSS decision table that exposes inconclusive and contradictory cases a single test would hide | Medium |
| 12.10 | ~~**Add Black-Scholes derivation** from Itô's Lemma~~ ✅ **DONE** (in `09-Finance/03_Option_Pricing`) — added an Itô's Lemma section (statement, the $(dW)^2 = dt$ multiplication table, and the Taylor-expansion derivation explaining why the second-order term survives), then completed the previously-missing step from PDE to closed form: Feynman-Kac, the risk-neutral lognormal expectation, and the explicit integral evaluation (splitting at the exercise boundary, completing the square) that *derives* $d_1$ and $d_2$ rather than asserting them | High |
| 12.11 | **Expand Appendix A1-A4 proofs** — add intermediate steps to every theorem | Medium |
| 12.12 | **Add "Key Equations" summary boxes** at end of every theory-heavy notebook | Medium |

### Phase 13: Flow, Ordering & Sequencing (Estimated: 8-10 hours)

Addresses audit findings §M.

| # | Task | Priority |
|---|---|---|
| 13.1 | **Reorder Finance module** — move `02_Portfolio_Theory` to position 01; move BGG to position 05+ | High |
| 13.2 | **Fix high_performance_python numbering** — renumber to 01-04 contiguously | Medium |
| 13.3 | **Fix Appendix numbering** — separate tools (Publishing, Autograding, Replication) from math (A1-A4) with clear prefix scheme | Medium |
| 13.4 | **Add explicit prerequisite chains** — every notebook's Prerequisites section must list specific notebook filenames, not just topic names | High |
| 13.5 | **Delineate 06-Econometrics/09 vs 08-Time-Series boundary** — 06/09 covers classical TS econometrics (stationarity, unit roots); 08 covers modern forecasting and multivariate. Add scope note to each | High |
| 13.6 | **Evaluate reordering 01-Foundations** — consider moving Debugging (17) earlier; consider Sets (08) before Dictionaries (07) | Low |
| 13.7 | **Split oversized notebooks** per Phase 8.1 to improve within-notebook flow | High |

### Phase 14: Coherence, Cohesiveness & Convention Standardization (Estimated: 15-20 hours)

Addresses audit findings §N, §O, §P.

| # | Task | Priority |
|---|---|---|
| 14.1 | ~~**Create `docs/resources/notation.md`**~~ ✅ **DONE** — project-wide glossary covering core conventions, per-domain symbol tables with math↔code mapping, interest-rate convention ($r$/$R$/$i$), and a symbol-collision table; wired into `mkdocs.yml` nav and `resources/index.md` | High |
| 14.2 | **Standardize "The Lens" heading** to `## The Lens: <Subtitle>` in all 113 notebooks | High |
| 14.3 | **Standardize heading levels** — `##` major sections, `###` subsections, `####` sub-sub | High |
| 14.4 | **Standardize exercise format** — `### Exercises` with `**N. Title (Difficulty):**` | High |
| 14.5 | **Standardize theorem/definition boxes** — `> **Theorem N (Name):**` blockquote style | High |
| 14.6 | **Standardize random seed** — replace all `np.random.seed()` with `rng = np.random.default_rng()` | Medium |
| 14.7 | **Standardize `plt.rcParams`** — create one canonical setup block; apply to all 113 notebooks | High |
| 14.8 | **Standardize `np.set_printoptions`** — one canonical config across all notebooks | Medium |
| 14.9 | **Add narrative thread** — "Building on [X]…" opener + "Next, we will…" closer in every notebook | High |
| 14.10 | **Standardize `display(Markdown())` vs `print()`** — use `display(Markdown())` for formatted notes | Medium |
| 14.11 | **Standardize "The Lens" depth** — expand any Lens section <100 words to 150-300 words with a specific economic question | High |
| 14.12 | **Enforce consistent terminology** — first use: full name + abbreviation; subsequent: abbreviation only | Medium |

### Phase 15: Legacy Purge & Consolidation (Estimated: 6-8 hours)

Addresses audit findings §O. Wipe out all remnants of previous iterations.

| # | Task | Priority |
|---|---|---|
| 15.1 | **Remove all `## Part N` / `## Chapter N.X` legacy headers** from modules 03-10 | High |
| 15.2 | **Remove/silence "Environment initialized" print statements** — replace with silent setup or single `display(Markdown("✓ Ready"))` | Medium |
| 15.3 | **Standardize `%config InlineBackend.figure_format = 'retina'`** — add to all or remove from all | Medium |
| 15.4 | **Strip unused imports** — remove `os, sys, math, time, random, json, textwrap` where not actually used | High |
| 15.5 | **Archive stale planning docs** — move FULL_ROADMAP, IMPROVEMENT_PLAN, INFRASTRUCTURE, PEDAGOGY, PREP_WORK_SUMMARY to `docs/internal/archive/` | Medium |
| 15.6 | **Delete root-level artifacts** — `notebook_structure.md`, `notebook_structure_report.json`, `image_path_mapping.json`, `debug_rbc*.py` | Medium |
| 15.7 | **Delete/regenerate `models/mlp_boston_housing.keras`** — trained on deprecated dataset | Low |
| 15.8 | **Replace hardcoded `GRAPHVIZ_AVAILABLE = False`** with dynamic `try/except` in all affected notebooks | High |
| 15.9 | **Consolidate BGG scripts** — merge `solve_bgg_model.py` + `bgg_illustrative_solver.py` into single `scripts/bgg_solver.py` | Medium |
| 15.10 | **Simplify over-engineered code** per audit §J — metaclass to Appendix, complete Anderson accel or remove, clean CGE error handling | Medium |

---

## Part VI: Summary Statistics

| Metric | Count | Severity |
|---|---|---|
| **Total notebooks analyzed** | 113 | — |
| **Total scripts analyzed** | 64 | — |
| **Total image files** | 310 | — |
| **Total data files** | 13 | — |
| **Total docs pages (existing)** | 19 | — |
| | | |
| **CRITICAL — SECURITY** | | |
| `polyfill.io` supply-chain vulnerability in mkdocs.yml | 1 | 🔴 |
| | | |
| **CRITICAL — BROKEN CONTENT** | | |
| Zero-byte (broken) image files | **57** (18.4% of all images) | 🔴 |
| Image directories with ALL files broken | 4 (modules 02, 03, 04, 05) | 🔴 |
| Notebooks with unfilled "Summary" template | **25** | 🔴 |
| Notebooks with unfilled "The Lens" template | **19** | 🔴 |
| Notebooks with "(Introduction text to be added)" | **12** | 🔴 |
| Missing docs pages referenced in mkdocs.yml | **45+** (~70% of nav) | 🔴 |
| Packages imported but missing from dependencies | **17** | 🔴 |
| Packages in env.yml but missing from requirements.txt | **11** | 🔴 |
| | | |
| **HIGH — STRUCTURAL** | | |
| Notebooks with "Concept Overview" boilerplate | 22 | 🟠 |
| Notebooks with duplicate license badges | ~20+ | 🟠 |
| Notebooks missing Learning Objectives | 101 | 🟠 |
| Notebooks missing Prerequisites | 104 | 🟠 |
| Notebooks missing References | 90 | 🟠 |
| Notebooks missing Exercises | ~31 | 🟠 |
| Notebooks missing Colab/Binder badges | 113 | 🟠 |
| Notebooks with `plt.savefig()` (writing to disk) | 16 | 🟠 |
| Notebooks with `warnings.filterwarnings('ignore')` | 32 | 🟠 |
| Notebooks using legacy `np.random.seed()` | 19 | 🟠 |
| Notebooks with `sys.path.append` | 2 | 🟠 |
| | | |
| **MEDIUM — QUALITY** | | |
| Notebooks with type hints on functions | 9 (of 113) | 🟡 |
| Major content overlaps (topic clusters) | 10 | 🟡 |
| Over-engineered implementations | 7 | 🟡 |
| Convention inconsistencies (categories) | 9 | 🟡 |
| Content gaps (missing proofs/derivations) | 12+ | 🟡 |
| Ordering/sequencing issues | 8 | 🟡 |
| Legacy remnants (beyond boilerplate) | 11 types | 🟡 |
| Notebooks needing proofreading | 113 (0 proofread) | 🟡 |
| Notebooks missing narrative thread | ~113 | 🟡 |
| Mixed DL frameworks (TF + PyTorch) | 2 frameworks | 🟡 |
| Duplicate image directory schemes | 4 schemes | 🟡 |
| | | |
| **HIGH — IMAGE SCRIPT ISSUES** | | |
| Total image generation scripts | 54 | — |
| Redundant duplicate scripts (18 clusters) | **~38** (70% of all scripts) | 🔴 |
| Scripts with broken output paths (nested `images/`) | **5** | 🔴 |
| Scripts with code bugs (`/n`, rename race, wrong dir) | **4** | 🟠 |
| Scripts missing `__name__` guard (execute on import) | **7** | 🟠 |
| Inconsistent output directory schemes | **14+** patterns | 🟠 |
| Scripts requiring `graphviz` (not in deps) | **18** | 🟠 |
| Scripts requiring `networkx` (not in deps) | **2** | 🟠 |
| Scripts requiring `imagemagick` (external, not documented) | **3** | 🟠 |
| | | |
| **LOW — HOUSEKEEPING** | | |
| Test files (excluding notebooks) | 1 | 🔵 |
| Oversized notebooks (>100 KB) | 6+ | 🔵 |
| Open TODO/FIXME items | 9 | 🔵 |
| Unused package in deps (`pyportfolioopt`) | 1 | 🔵 |
| Root-level clutter files | 7 | 🔵 |
| Data files with no documentation | 13 (0 have provenance) | 🔵 |

---

## Part VII: Recommended Execution Order

```
═══════════════════════════════════════════════════════════════════════
 TIER 1 — FOUNDATION (must be done first, unblocks everything else)
═══════════════════════════════════════════════════════════════════════

Phase 0  (Emergency & Security Fixes)      ←  5-8 hours   ← INCLUDES SECURITY FIX + .gitignore creation
Phase 15 (Legacy Purge & Consolidation)    ←  6-8 hours
Phase 1  (Boilerplate & Placeholder Clean) ←  8-12 hours  ← EXPANDED: 25 summaries, 19 Lens, 12 intros
  ↓
═══════════════════════════════════════════════════════════════════════
 TIER 2 — STRUCTURAL (skeleton and infrastructure)
═══════════════════════════════════════════════════════════════════════

Phase 13 (Flow, Ordering & Sequencing)     ←  8-10 hours  ← reorder before adding content
Phase 2  (Structural Standards)            ←  8-12 hours
Phase 3  (Infrastructure Repair)           ←  8-12 hours  ← EXPANDED: 45+ missing docs pages
Phase 4  (Testing)                         ←  4-6 hours
  ↓
═══════════════════════════════════════════════════════════════════════
 TIER 3 — CONTENT (the intellectual core of the upgrade)
═══════════════════════════════════════════════════════════════════════

Phase 10 (Redundancy & Overlap Resolution) ← 12-16 hours  ← before deepening
Phase 12 (Content Deepening — Proofs)      ← 25-35 hours
Phase 11 (Writing Quality & Proofreading)  ← 15-20 hours  ← after content is final
  ↓
═══════════════════════════════════════════════════════════════════════
 TIER 4 — POLISH & COHERENCE (final quality pass)
═══════════════════════════════════════════════════════════════════════

Phase 14 (Coherence & Convention Standard.)← 15-20 hours
Phase 7  (Code Quality)                    ←  8-12 hours
Phase 5  (File Organization)               ←  3-5 hours   ← EXPANDED: FRED scripts, stale script cleanup
Phase 6  (Image Pipeline Overhaul)         ← 10-16 hours  ← 57 broken images + 38 redundant scripts to consolidate
  ↓
═══════════════════════════════════════════════════════════════════════
 TIER 5 — ADVANCED (optional enhancements)
═══════════════════════════════════════════════════════════════════════

Phase 8  (Content Enhancement)             ← 20-30 hours
Phase 9  (Advanced & Polish)               ← 10-15 hours
```

**Total estimated effort: 182-257 hours**

| Tier | Phases | Hours | Focus |
|---|---|---|---|
| **Tier 1** | 0, 15, 1 | 19-28 | Clean slate: security fix, .gitignore, bugs, legacy purge, boilerplate & placeholder removal |
| **Tier 2** | 13, 2, 3, 4 | 28-40 | Structure: ordering, standards, infra (45+ missing docs pages), tests |
| **Tier 3** | 10, 12, 11 | 52-71 | Content: deduplicate, deepen, proofread |
| **Tier 4** | 14, 7, 5, 6 | 36-53 | Polish: coherence, code quality, organization (12 tasks), 57 broken images, 38 redundant scripts |
| **Tier 5** | 8, 9 | 30-45 | Advanced: new features, Quarto, interactivity |

---

## Part VIII: Key Findings Summary (Multi-Pass Investigation)

The second-pass and final-pass investigations uncovered **significant additional issues** not found in the first pass:

1. **🔴 SECURITY:** `polyfill.io` CDN reference in `mkdocs.yml` — compromised supply-chain attack vector (§S)
2. **🔴 57 broken images** (18.4% of all image files are 0-byte) — 4 entire module image directories have zero working files (§Q)
3. **🔴 25 notebooks with unfilled "Summary" templates** and **19 with unfilled "The Lens" templates** — a much larger contamination than the 22 "Concept Overview" boilerplate notebooks identified in the first pass (§R)
4. **🔴 12 notebooks with "(Introduction text to be added)"** placeholder text (§R)
5. **🔴 45+ missing docs pages** referenced in `mkdocs.yml` — 70% of navigation links are broken (§T)
6. **🔴 17 packages imported in notebooks but missing from all dependency files** — no notebook in ML module will run on fresh install (§U)
7. **🔴 11 packages in `environment.yml` but missing from `requirements.txt`** — pip-only installs will fail (§U)
8. **🟠 16 notebooks with `plt.savefig()`** writing files to disk — anti-pattern causing unintended git changes (§V)
9. **🟠 32 notebooks with blanket `warnings.filterwarnings('ignore')`** — hiding deprecation and runtime warnings (§Z)
10. **🟠 Mixed TensorFlow + PyTorch** without rationale or dual setup instructions (§Y)
11. **🟠 Duplicate/conflicting image directory schemes** — module-based, format-based, and topic-based coexist (§X)
12. **🟠 Data file issues** — case-sensitive path mismatch (`SP500.csv` vs `sp500.csv`), missing referenced files, undocumented datasets (§W)
13. **🔴 ~38 of 54 image scripts are redundant duplicates** — 18 duplicate clusters found where 2-4 scripts each generate the same image with different styles/paths (Part IV §A)
14. **🔴 5 image scripts have broken save paths** — they nest `images/` inside `images/`, writing to deeply nested broken directories (Part IV §B)
15. **🟠 4 image scripts contain bugs** — `/n` instead of `\n` in graphviz labels, `os.rename` race condition, wrong output directory (Part IV §C)
16. **🟠 7 image scripts execute on import** — missing `if __name__ == '__main__'` guard (Part IV §E)
17. **🟠 18 image scripts require `graphviz`** which is not in any dependency file (Part IV §G)
18. **🔴 `.gitignore` does not exist** — committed `__pycache__/` directory, no protection against future cache/artifact commits (Final Pass)
19. **🟠 `.pre-commit-config.yaml` does not exist** — INFRASTRUCTURE.md references pre-commit hooks but the config file was never created (Final Pass)
20. **🟠 `.gitattributes` does not exist** — no ipynb diff/merge settings, no line-ending enforcement (Final Pass)
21. **🟠 `solve_bgg_model.py` is non-functional** — placeholder that returns empty DataFrame; lines 76-98 are unreachable code after `return`; references non-existent `pysnowdrop` library (Final Pass)
22. **🟠 6 FRED CSV data files have no download script** — CPIAUCSL, DPIC96, FEDFUNDS, GDPC1, INDPRO, PCECC96 were presumably manually downloaded with zero provenance tracking (Final Pass)
23. **🟠 `contributing.md` has wrong env name** — says `conda activate computational-econ` but correct name is `computational-economics`; also references `scripts/validate_notebooks.py` 3 times (doesn't exist) (Final Pass)
24. **🟡 CI uses outdated GitHub Actions** — `actions/cache@v3` and `peaceiris/actions-gh-pages@v3` should be `v4` (Final Pass)
25. **🟡 3 mkdocs plugins installed but never configured** — `mkdocs-redirects`, `mkdocs-glightbox`, `mkdocs-minify-plugin` are pip-installed in CI but missing from `mkdocs.yml` plugins section (Final Pass)
26. **🟡 `docs/IMAGE_CATALOG.md` is stale** — only 5 of 300+ images cataloged; paths don't match actual directory structure (Final Pass)
27. **🟡 `requirements.txt` contains `playwright`** — browser automation dev artifact, not needed for course (Final Pass)

---

*This audit was produced through three passes of systematic investigation: (1) one-by-one reading of every notebook, script, config file, documentation page, and data file in the repository, combined with automated pattern analysis across all 113 notebooks; (2) a broader second-pass deep investigation focusing on broken assets, placeholder contamination, security vulnerabilities, dependency completeness, and cross-file consistency; and (3) a final comprehensive sweep re-examining every script, config file, docs page, CI workflow, and root-level artifact to verify factual accuracy of all claims in this document and uncover any remaining gaps (findings #18-27). Corrections from the final pass include: `.gitignore`, `.pre-commit-config.yaml`, and `.gitattributes` were erroneously described as existing—they do not; `solve_bgg_model.py` is a non-functional placeholder; 6 FRED data files lack download scripts; CI actions are outdated; 3 mkdocs plugins are installed but never configured. The plan covers 16 phases across 5 tiers: security fixes, dependency synchronization, legacy purge, boilerplate removal, structural standardization, infrastructure repair (45+ missing docs pages), testing, redundancy resolution, content deepening, proofreading, convention standardization, code quality, file organization, image pipeline overhaul (57 broken images + 35 redundant scripts), and advanced enhancements.*
