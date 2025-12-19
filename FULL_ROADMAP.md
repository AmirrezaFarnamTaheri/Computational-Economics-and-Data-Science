# Comprehensive Repository Roadmap

This document provides a surgical, detailed plan for upgrading every single notebook in the repository to meet the "Zero to Hero" standard. It serves as the master checklist for the renovation.

## Global Standards (Apply to All)
*   **Header:** Standard Title, Badges, "The Lens" (Economic Intuition), Learning Objectives, Prerequisites.
*   **Footer:** Summary, Key Takeaways, References.
*   **Navigation:** Clickable Table of Contents.
*   **Exercises:** At least 3 graded exercises (Conceptual, Applied, Challenge).
*   **Code:** Type hints, docstrings, vectorization where applicable.

---

## Module 01: Foundations
*Goal: Solidify the "Python for Economists" narrative.*

| Notebook | Status | Specific Action Items |
| :--- | :--- | :--- |
| `01_Introduction.ipynb` | **Completed** | (Reference implementation). |
| `02_Professional_Development_Environment.ipynb` | Good content | Add "The Lens". Add Exercise on setting up a virtual env. |
| `03_Python_Fundamentals_Data_Types.ipynb` | Needs Context | Add examples of `float` errors in financial calculations. |
| `04_Python_Data_Model.ipynb` | Advanced | Frame as "Building Economic Objects" (e.g., a `Consumer` class). |
| `05_Lists_and_Tuples.ipynb` | Standard | Add example: Storing time-series data in lists vs tuples. |
| `06_Advanced_String_Processing.ipynb` | Standard | Add example: Parsing central bank announcements. |
| `07_Dictionaries.ipynb` | Standard | Add example: Representing model parameters as dicts. |
| `08_Sets.ipynb` | Light | Add example: Unique set of traded assets. |
| `09_Control_Flow_and_Error_Handling.ipynb` | Standard | Add example: Robust simulation loops (catching non-convergence). |
| `10_Advanced_Functions.ipynb` | Advanced | Add example: Closures for defining utility functions with parameters. |
| `11_Object_Oriented_Programming.ipynb` | Vital | Refactor: Build a reusable `Market` class. |
| `12_NumPy.ipynb` | Vital | Add example: Matrix algebra for Input-Output models. |
| `13_Pandas.ipynb` | Vital | Use real GDP/Inflation data (via `pandas-datareader` or CSV). |
| `14_Introduction_to_Data_Acquisition.ipynb` | Good | Ensure API examples are secure. |
| `15_Accessing_Economic_Data_via_APIs.ipynb` | Good | Add FRED and World Bank API exercises. |
| `16_Data_Visualization.ipynb` | Standard | Add "The Lens" on communicating data. Replicate a famous Econ chart. |
| `17_Effective_Debugging.ipynb` | Vital | Create a "Bug Hunt" exercise with a broken model. |
| `18_Data_Acquisition_Web_Scraping.ipynb` | Advanced | Add warning on `robots.txt` compliance. |
| `19_Introduction_to_SQL.ipynb` | Light | Add a realistic schema (e.g., compustat-like). |
| `20_Introduction_to_SciPy.ipynb` | Vital | Frame `optimize` as "Rational Choice". |
| `21_Symbolic_Computation_with_SymPy.ipynb` | Niche | Use to derive FOCs for a utility function. |
| `22_Computational_Complexity.ipynb` | Theoretical | Link O(n) to simulation runtime in later modules. |
| `23_Profiling_and_Performance.ipynb` | Advanced | Profile a slow simulation from Module 10. |
| `24_Production_Code_Standards.ipynb` | Meta | Add pre-commit hook setup guide. |

---

## Module 02: Numerical Methods
*Goal: Connect abstract math to economic utility.*

| Notebook | Status | Specific Action Items |
| :--- | :--- | :--- |
| `01_Linear_Algebra.ipynb` | Vital | Add "The Lens": Equilibrium as a system of equations. Add Markov Chain example. |
| `02_Numerical_Preliminaries.ipynb` | Theoretical | Explain machine epsilon relevance in iterative solvers. |
| `03_Numerical_Differentiation.ipynb` | Standard | Compare Finite Differences vs JAX auto-diff for marginal utility. |
| `04_Root_Finding.ipynb` | Vital | Frame as "Market Clearing" ($S(p) - D(p) = 0$). |
| `05_Optimization.ipynb` | Vital | Frame as "Utility Maximization". Add 3D hill-climbing plot. |
| `06_Interpolation_and_Approximation.ipynb` | Advanced | Explain why we need this for Value Functions (continuous state). |
| `07_Numerical_Integration.ipynb` | Standard | Frame as "Calculating Expectations" (Expected Utility). |
| `08_Differential_Equations.ipynb` | Advanced | Solve Solow/Ramsey growth path numerically. |

---

## Module 03: Economic Modeling
*Goal: Standardize Dynamic Programming (DP).*

| Notebook | Status | Specific Action Items |
| :--- | :--- | :--- |
| `01_Dynamic_Programming.ipynb` | Core | Standardize notation ($V, \beta$). Visualize VFI convergence. |
| `02_DP_with_Continuous_States.ipynb` | Advanced | Implement Collocation method clearly. |
| `03_Discrete_Continuous_DP.ipynb` | Light | Expand. Implement a basic Rust Bus Engine model. |
| `04_Estimation_and_Calibration.ipynb` | Light | Expand significantly. Calibration vs Estimation. |
| `05_Optimal_Stopping_Problems.ipynb` | Standard | Frame as "Option Value of Waiting" (Job Search). |
| `06_Robust_Control.ipynb` | Niche | Explain "Knightian Uncertainty" clearly in The Lens. |
| `07_Structural_Estimation.ipynb` | Advanced | Explain the link to "Counterfactual Policy Analysis". |

---

## Module 04: Macro Models
*Goal: Create a clear historical progression.*

| Notebook | Status | Specific Action Items |
| :--- | :--- | :--- |
| `01_Job_Search.ipynb` | Core | Link to `03-05` (Optimal Stopping). Add DMP model viz. |
| `02_Neoclassical_Growth.ipynb` | Core | Compare Solow (exogenous) vs Ramsey (endogenous savings). |
| `03_RBC_Models.ipynb` | Light | Expand. Explicitly compare Real vs Monetary shocks. |
| `04_OLG_Models.ipynb` | Standard | Add visual of "intergenerational transfer". |
| `05_New_Keynesian_Models.ipynb` | Core | Add Impulse Response Functions (IRFs) for interest rate shock. |
| `06_Heterogeneous_Agent_Models.ipynb` | Capstone | Frame as HANK. Show wealth distribution histogram. |
| `08_Endogenous_Growth.ipynb` | Standard | Renumber to `07`. Add Romer model simulation. |

---

## Module 05: Micro Models
*Goal: Connect Game Theory and Information.*

| Notebook | Status | Specific Action Items |
| :--- | :--- | :--- |
| `01_Consumer_and_Producer_Theory.ipynb` | Core | Add Slutsky Matrix visualization. |
| `02_General_Equilibrium.ipynb` | Light | Expand significantly. Build an Edgeworth Box. |
| `03_Game_Theory_and_Auctions.ipynb` | Core | Use `nashpy`. Visualize payoff matrices. |
| `04_Discrete_Choice_Models.ipynb` | Standard | Link to Logit/Probit in Econometrics. |
| `05_Principal_Agent_Models.ipynb` | Standard | Add "Moral Hazard" interactive parameter widget. |
| `06_Information_Economics.ipynb` | Light | Add "Signaling Game" simulation (Spence). |

---

## Module 06: Econometrics
*Goal: Focus on Causal Inference.*

| Notebook | Status | Specific Action Items |
| :--- | :--- | :--- |
| `01_Linear_Model_and_OLS.ipynb` | Core | Derive OLS geometrically. |
| `02_Maximum_Likelihood.ipynb` | Standard | Link to `02-05` (Optimization). |
| `03_Causal_Inference.ipynb` | Vital | Fix Unknown Kernel. Explain DAGs vs Potential Outcomes. |
| `04_GMM.ipynb` | Advanced | Frame as generalized method for structural estimation. |
| `05_Instrumental_Variables.ipynb` | Vital | Fix Unknown Kernel. Add 2SLS manual implementation. |
| `06_Regression_Discontinuity.ipynb` | Standard | Add sharp vs fuzzy RDD visual. |
| `07_Synthetic_Control_Methods.ipynb` | Advanced | Add "Placebo Test" exercise. |
| `08_Difference_in_Differences.ipynb` | Core | Discuss "Staggered Adoption" risks. |
| `09_Classical_Time_Series_Analysis.ipynb` | Vital | Fix Unknown Kernel. Differentiate from Module 08. |
| `10_Vector_Autoregression.ipynb` | Standard | Merge/Link with `08-04`. Focus on identification here. |
| `11_Bayesian_Econometrics.ipynb` | Advanced | Use `PyMC` for a simple linear model. |
| `12_Panel_Data_Methods.ipynb` | Standard | Fixed vs Random Effects intuition. |

---

## Module 07: Machine Learning
*Goal: Deepen "ML for Economics".*

| Notebook | Status | Specific Action Items |
| :--- | :--- | :--- |
| `01_Introduction_to_ML_for_Economists.ipynb` | Good | Explain Bias-Variance in econ forecasting context. |
| `02_Gradient_Boosting_Machines.ipynb` | Light | Use `xgboost` on credit default data. |
| `03_Support_Vector_Machines.ipynb` | Light | Briefly cover, note lower relevance in modern econ. |
| `04_Ensemble_Methods.ipynb` | Light | Explain "Wisdom of Crowds". |
| `05_Dimensionality_Reduction_and_Clustering.ipynb` | Standard | PCA for "Factor Models" in finance. |
| `06_Deep_Learning_Foundations.ipynb` | Standard | Neural Networks as "Universal Approximators". |
| `07_Convolutional_Neural_Networks.ipynb` | Light | Expand. Application: Night lights -> GDP. |
| `08_Recurrent_Neural_Networks.ipynb` | Standard | Time-series forecasting application. |
| `09_LSTMs_and_GRUs.ipynb` | Standard | Compare with standard ARIMA. |
| `10_Transformers.ipynb` | Duplicate | Merge with `10_Transformers_executed.ipynb`. |
| `10_Transformers_executed.ipynb` | Duplicate | Merge into `10_Transformers.ipynb`. |
| `11_Autoencoders.ipynb` | Light | Application: Denoising financial data. |
| `12_Self_Supervised_Learning.ipynb` | Unknown Kernel | Fix Kernel. Explain usefulness for unlabeled econ data. |
| `13_Generative_Models.ipynb` | Standard | Generating synthetic economic scenarios. |
| `14_Multi_modal_Fusion.ipynb` | Light | Text + Time Series for forecasting. |
| `15_Reinforcement_Learning.ipynb` | Advanced | Link to Dynamic Programming (Bellman Eq). |
| `16_Advanced_Deep_RL.ipynb` | Advanced | AI Economist example (tax policy). |
| `17_Causal_ML.ipynb` | Vital | `DoubleML` deep dive. Heterogeneous Treatment Effects. |
| `18_Natural_Language_Processing.ipynb` | Standard | Sentiment Analysis of Fed Minutes. |
| `19_Graph_Neural_Networks.ipynb` | Light | Supply chain contagion application. |
| `20_Geospatial_Data.ipynb` | Standard | Housing price heatmaps. |
| `21_ML_for_Macro_Forecasting.ipynb` | Light | Nowcasting GDP. |
| `22_Style_Transfer_and_Advanced_Vision.ipynb` | Unknown Kernel | Fix Kernel. Low priority, keep as fun example. |

---

## Module 08: Time Series
*Goal: Focus on Forecasting and Dynamics.*

| Notebook | Status | Specific Action Items |
| :--- | :--- | :--- |
| `01_Introduction_to_Time_Series.ipynb` | Core | Stationarity and Unit Roots visual explainer. |
| `02_ARMA_Models.ipynb` | Standard | Build intuition for AR vs MA processes. |
| `03_ARIMA_and_Forecasting.ipynb` | Standard | Add `Prophet` or modern library comparison. |
| `04_Vector_Autoregression.ipynb` | Core | Focus on IRFs and Variance Decomposition. |
| `05_Volatility_Modeling_ARCH_GARCH.ipynb` | Light | Expand. Use real financial returns data. |
| `06_Cointegration_and_Error_Correction_Models.ipynb` | Advanced | Pairs trading strategy example. |

---

## Module 09: Finance
*Goal: Unify notation and rigorous derivations.*

| Notebook | Status | Specific Action Items |
| :--- | :--- | :--- |
| `01_Financial_Frictions_BGG.ipynb` | Advanced | Explain "Costly State Verification" simply. |
| `02_Portfolio_Theory.ipynb` | Standard | Efficient Frontier visualization. |
| `03_Asset_Pricing.ipynb` | Core | SDF (Stochastic Discount Factor) framework unification. |
| `04_Option_Pricing.ipynb` | Core | Black-Scholes derivation from Heat Equation. |
| `05_Continuous_Time_Finance.ipynb` | Advanced | Intuitive intro to Ito's Lemma. |
| `06_Credit_Risk.ipynb` | Standard | Merton Model for default probability. |
| `07_High_Frequency_Data.ipynb` | Standard | Limit Order Book visualization. |

---

## Module 10: Specialized Models
*Goal: Frontier complexity methods.*

| Notebook | Status | Specific Action Items |
| :--- | :--- | :--- |
| `01_Agent_Based_Models.ipynb` | Vital | Optimize Schelling code (vectorize). Add Tipping Point exercise. |
| `02_General_Equilibrium_with_Heterogeneous_Agents.ipynb` | Advanced | Ensure distinction from Module 04 HANK. Focus on implementation. |
| `03_Network_Economics.ipynb` | Standard | Network centrality measures in production networks. |

---

## Appendix & High Performance
*Goal: Supporting resources.*

| Notebook | Status | Specific Action Items |
| :--- | :--- | :--- |
| `01_Publishing_with_Quarto.ipynb` | Tooling | Update for latest Quarto version. |
| `01_Replication_Exercise_Chetty_2014.ipynb` | Capstone | Ensure data access is clear/working. |
| `02_Autograding_with_Otter.ipynb` | Tooling | Verify `otter-grader` config. |
| `A1-Real-Analysis.ipynb` | Math | Self-contained refresher. |
| `A2-Multivariate-Calculus.ipynb` | Math | Jacobian/Hessian intuition. |
| `A3-Probability-Theory.ipynb` | Math | CLT and LLN visualizations. |
| `A4-Linear-Algebra.ipynb` | Math | Eigenvalues in dynamic systems context. |
| `high_performance_python/02_High_Performance_Computing.ipynb` | Advanced | Numba vs Cython speedup comparison. |
| `high_performance_python/04_Accelerating_Code_with_Numba.ipynb` | Standard | Monte Carlo simulation optimization. |
| `high_performance_python/05_Parallel_Computing_with_Dask.ipynb` | Standard | Large dataframe processing example. |
| `high_performance_python/06_GPU_Acceleration_with_CuPy.ipynb` | Niche | Matrix multiplication on GPU. |
