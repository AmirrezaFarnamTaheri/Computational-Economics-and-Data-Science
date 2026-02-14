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
*Theme: The Pythonic Economist*
*Narrative Arc:* From "Hello World" to building complex economic objects and pipelines.

| Notebook | Status | Pedagogical Goal | Technical Spec | Data Source | Interactive Element |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `01_Introduction.ipynb` | **Completed** | Define the field & tooling. | Markdown polish. | N/A | Cobweb Model Sliders. |
| `02_Professional_Development_Environment.ipynb` | Good | Mastering the CLI/Git. | Shell commands. | N/A | Git graph visualizer. |
| `03_Python_Fundamentals_Data_Types.ipynb` | Needs Context | Numerical precision. | `decimal` vs `float`. | N/A | Floating point error demo. |
| `04_Python_Data_Model.ipynb` | Advanced | OOP for Economics. | `dataclasses`. | N/A | `Consumer` class builder. |
| `05_Lists_and_Tuples.ipynb` | Standard | Sequence efficiency. | Timeit profiling. | N/A | Memory usage comparator. |
| `06_Advanced_String_Processing.ipynb` | Standard | Regex for Econ text. | `re` module. | FOMC snippet. | Regex matcher widget. |
| `07_Dictionaries.ipynb` | Standard | Key-Value mappings. | Dict comprehensions. | N/A | Parameter sweep dict. |
| `08_Sets.ipynb` | Light | Set theory ops. | `frozenset`. | N/A | Venn diagram plotter. |
| `09_Control_Flow_and_Error_Handling.ipynb` | Standard | Robust simulation loops. | `try-except` blocks. | N/A | Error handling sandbox. |
| `10_Advanced_Functions.ipynb` | Advanced | Functional programming. | Closures, Decorators. | N/A | Utility function factory. |
| `11_Object_Oriented_Programming.ipynb` | Vital | Agent representation. | Inheritance/Composition. | N/A | Market simulation. |
| `12_NumPy.ipynb` | Vital | Linear Algebra foundation. | Vectorization. | N/A | Matrix mult visualizer. |
| `13_Pandas.ipynb` | Vital | Tidy Data principles. | Method chaining. | WDI/FRED. | Data filtering slider. |
| `14_Introduction_to_Data_Acquisition.ipynb` | Good | API vs Scraping. | `requests`. | JSON placeholder. | JSON viewer. |
| `15_Accessing_Economic_Data_via_APIs.ipynb` | Good | Remote data access. | `pandas-datareader`. | FRED/WorldBank. | Series fetcher widget. |
| `16_Data_Visualization.ipynb` | Standard | Communicating results. | `seaborn`, `altair`. | Gapminder. | Chart style picker. |
| `17_Effective_Debugging.ipynb` | Vital | Diagnosing model failure. | `pdb`, logging. | Buggy model code. | Interactive debugger. |
| `18_Data_Acquisition_Web_Scraping.ipynb` | Advanced | Unstructured data. | `beautifulsoup4`. | Mock website. | HTML parser. |
| `19_Introduction_to_SQL.ipynb` | Light | Relational databases. | `sqlite3`. | Dummy Firm DB. | SQL Query runner. |
| `20_Introduction_to_SciPy.ipynb` | Vital | Numerical toolbox. | `scipy.optimize`. | N/A | Root finding animator. |
| `21_Symbolic_Computation_with_SymPy.ipynb` | Niche | Analytical derivation. | `sympy`. | Utility func. | Derivative solver. |
| `22A_Computational_Complexity_Foundations.ipynb` | Theoretical | Algorithmic efficiency. | Big-O notation. | N/A | Complexity plotter. |
| `22B_Complexity_in_Economic_Applications.ipynb` | Applied | Economic feasibility. | Curse of dimensionality. | N/A | Scaling case study. |
| `23_Profiling_and_Performance.ipynb` | Advanced | Code optimization. | `cProfile`. | Slow sim code. | Flame graph viewer. |
| `24_Production_Code_Standards.ipynb` | Meta | Reproducibility. | `black`, `flake8`. | N/A | Linter check demo. |

**Ordering note:** For instructional flow, consider teaching `08_Sets` before `07_Dictionaries`, and moving `17_Effective_Debugging` earlier (right after `09_Control_Flow_and_Error_Handling`).

---

## Module 02: Numerical Methods
*Theme: The Engine of Computation*
*Narrative Arc:* Converting economic equilibrium conditions into solvable numerical problems.

| Notebook | Status | Pedagogical Goal | Technical Spec | Data Source | Interactive Element |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `01_Linear_Algebra.ipynb` | Vital | Systems of equations. | `numpy.linalg`. | I-O Tables. | Eigenvalue animator. |
| `02_Numerical_Preliminaries.ipynb` | Theoretical | Stability & Condition. | FP64 vs FP32. | N/A | Error propagation plot. |
| `03_Numerical_Differentiation.ipynb` | Standard | Gradients & Hessians. | `jax` vs Finite Diff. | N/A | Derivative comparison. |
| `04_Root_Finding.ipynb` | Vital | Equilibrium Finding. | Newton-Raphson. | Supply/Demand. | Convergence stepper. |
| `05_Optimization.ipynb` | Vital | Rational Choice. | `scipy.optimize`. | Utility Surface. | 3D Hill climbing. |
| `06_Interpolation_and_Approximation.ipynb` | Advanced | Function Approx. | Chebyshev, Splines. | N/A | Approx error plot. |
| `07_Numerical_Integration.ipynb` | Standard | Expectations. | Gaussian Quad. | Normal Dist. | Area under curve. |
| `08_Differential_Equations.ipynb` | Advanced | Dynamics. | `scipy.integrate`. | Solow Model. | Phase diagram plotter. |

---

## Module 03: Economic Modeling
*Theme: Dynamic Programming & Structural Estimation*
*Narrative Arc:* Solving for optimal policies in dynamic environments.

| Notebook | Status | Pedagogical Goal | Technical Spec | Data Source | Interactive Element |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `01_Dynamic_Programming.ipynb` | Core | Bellman Equation. | VFI (Numba). | N/A | VFI convergence GIF. |
| `02_DP_with_Continuous_States.ipynb` | Advanced | Curse of Dimensionality. | Interpolation + VFI. | N/A | Value func surface. |
| `03A_Discrete_Choice_DP_Rust.ipynb` | Advanced | Discrete choice DP. | Rust replacement. | Bus data. | Policy threshold plot. |
| `03B_Continuous_State_DP_Interpolation.ipynb` | Advanced | Continuous state DP. | Interpolation VFI. | N/A | Policy function plot. |
| `04_Estimation_and_Calibration.ipynb` | Light | Model-Data matching. | MSM (Method of Moments). | Simulated panel. | Parameter fit slider. |
| `05_Optimal_Stopping_Problems.ipynb` | Standard | Option Value. | McCall Search. | Wage offer dist. | Reservation wage plot. |
| `06_Robust_Control.ipynb` | Niche | Ambiguity Aversion. | Min-Max Bellman. | N/A | Worst-case dist. |
| `07_Structural_Estimation.ipynb` | Advanced | Identification. | Nested Fixed Point. | Rust Bus Data. | Likelihood surface. |

---

## Module 04: Macro Models
*Theme: From Solow to HANK*
*Narrative Arc:* Adding layers of realism: Dynamics -> Microfoundations -> Heterogeneity.

| Notebook | Status | Pedagogical Goal | Technical Spec | Data Source | Interactive Element |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `01_Job_Search.ipynb` | Core | Labor Frictions. | DMP Model. | Beveridge Curve data. | DMP equilibrium plot. |
| `02_Neoclassical_Growth.ipynb` | Core | Convergence. | Ramsey-Cass-Koopmans. | PWT (Penn World Table). | Phase diagram slider. |
| `03A_RBC_Model_Foundations.ipynb` | Light | Business Cycles. | Equilibrium conditions. | FRED (GDP/Cons). | Steady-state solver. |
| `03B_RBC_Model_Solution.ipynb` | Light | Business Cycles. | Log-linearization + QZ. | FRED (GDP/Cons). | Solution diagnostics. |
| `03C_RBC_Dynamics_and_Surprise_Shocks.ipynb` | Light | Business Cycles. | Surprise shocks. | FRED (GDP/Cons). | IRF plotter. |
| `03D_RBC_News_Shocks_and_Expectations.ipynb` | Light | Business Cycles. | News shocks + expectations. | FRED (GDP/Cons). | Expectation dynamics plot. |
| `04_OLG_Models.ipynb` | Standard | Intergenerational equity. | Auerbach-Kotlikoff. | Demographics. | Transition path plot. |
| `05_New_Keynesian_Models.ipynb` | Core | Nominal Rigidities. | 3-Eq NK Model. | Inflation/Output Gap. | Taylor Rule slider. |
| `06_Heterogeneous_Agent_Models.ipynb` | Capstone | Inequality in Macro. | Aiyagari/HANK. | Wealth Dist. | Gini coeff dynamic. |
| `08_Endogenous_Growth.ipynb` | Standard | R&D and Innovation. | Romer Model. | Patent data. | Growth path sim. |

---

## Module 05: Micro Models
*Theme: Strategic Interaction*
*Narrative Arc:* Agents interacting in markets, games, and under information asymmetry.

| Notebook | Status | Pedagogical Goal | Technical Spec | Data Source | Interactive Element |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `01_Consumer_and_Producer_Theory.ipynb` | Core | Duality. | Slutsky decomp. | Expenditure data. | Indifference curves. |
| `02_General_Equilibrium.ipynb` | Light | Market Clearing. | Edgeworth Box. | N/A | 2-Good Exchange box. |
| `03_Game_Theory_and_Auctions.ipynb` | Core | Nash Equilibrium. | `nashpy`. | Auction logs. | Payoff matrix editor. |
| `04_Discrete_Choice_Models.ipynb` | Standard | Random Utility. | Logit/Probit. | Transport choices. | Probability curve. |
| `05_Principal_Agent_Models.ipynb` | Standard | Asymmetric Info. | Contract Theory. | N/A | Contract menu plot. |
| `06_Information_Economics.ipynb` | Light | Signaling. | Spence Model. | Education/Wage. | Separating equilib. |

---

## Module 06: Econometrics
*Theme: The Causal Revolution*
*Narrative Arc:* From correlation to causation using modern identification strategies.

| Notebook | Status | Pedagogical Goal | Technical Spec | Data Source | Interactive Element |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `01_Linear_Model_and_OLS.ipynb` | Core | Gauss-Markov. | Matrix OLS. | wage/educ. | Regression line dragger. |
| `02A_MLE_Principles_and_Geometry.ipynb` | Standard | MLE Intuition. | Likelihood geometry. | Binary outcome. | Likelihood func plot. |
| `02B_MLE_Optimization_and_Applications.ipynb` | Standard | Numerical MLE. | Optimization + Probit. | Synthetic binary. | LL surface contour. |
| `03_Causal_Inference.ipynb` | Vital | Identification Strat. | DAGs (`networkx`). | N/A | DAG builder/viewer. |
| `04_GMM.ipynb` | Advanced | Moment Conditions. | 2-step GMM. | Asset returns. | J-stat visualizer. |
| `05_Instrumental_Variables.ipynb` | Vital | Endogeneity fix. | 2SLS manual. | Card (1995) data. | First-stage fit plot. |
| `06_Regression_Discontinuity.ipynb` | Standard | Local Randomization. | `rdrobust` equivalent. | Test scores. | Discontinuity plot. |
| `07_Synthetic_Control_Methods.ipynb` | Advanced | Case Studies. | Convex Hull. | Prop 99 (Tobacco). | Counterfactual plot. |
| `08_Difference_in_Differences.ipynb` | Core | Parallel Trends. | TWFE / CS (2021). | Minimum Wage. | Event study plot. |
| `09_Classical_Time_Series_Analysis.ipynb` | Vital | Stationarity. | ADF / KPSS tests. | GDP/CPI. | ACF/PACF viewer. |
| `10_Vector_Autoregression.ipynb` | Standard | Multivariate Dynamics. | VAR / SVAR. | Macro aggregates. | Impulse Response visual. |
| `11_Bayesian_Econometrics.ipynb` | Advanced | Posterior updating. | `PyMC`. | N/A | Posterior dist plot. |
| `12_Panel_Data_Methods.ipynb` | Standard | Unobserved Heterogeneity.| FE / RE. | Penn World Table. | Within/Between variation. |

---

## Module 07: Machine Learning
*Theme: Prediction & High-Dimensional Inference*
*Narrative Arc:* Adapting ML tools for economic forecasting and causal inference.

| Notebook | Status | Pedagogical Goal | Technical Spec | Data Source | Interactive Element |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `01_Introduction_to_ML_for_Economists.ipynb` | Good | Bias-Variance Tradeoff. | `sklearn`. | Housing prices. | Complexity slider. |
| `02_Gradient_Boosting_Machines.ipynb` | Light | Tree Ensembles. | `xgboost`. | Credit default. | Tree visualizer. |
| `03_Support_Vector_Machines.ipynb` | Light | Margin Maximization. | `sklearn.svm`. | Classification. | Decision boundary. |
| `04_Ensemble_Methods.ipynb` | Light | Model Averaging. | Bagging/Stacking. | N/A | Voting visualizer. |
| `05_Dimensionality_Reduction_and_Clustering.ipynb` | Standard | Unsupervised Learning. | PCA / K-Means. | Fed speeches (TFIDF). | PCA scatter plot. |
| `06_Deep_Learning_Foundations.ipynb` | Standard | Backpropagation. | `pytorch` / `tensorflow`. | MNIST. | Neural net graph. |
| `07_Convolutional_Neural_Networks.ipynb` | Light | Spatial Structure. | CNN. | Satellite Night Lights. | Feature map viewer. |
| `08_Recurrent_Neural_Networks.ipynb` | Standard | Sequence Memory. | RNN. | Time series. | Hidden state heat. |
| `09_LSTMs_and_GRUs.ipynb` | Standard | Gating Mechanisms. | LSTM. | Text generation. | Gate activation plot. |
| `10_Transformers.ipynb` | Duplicate | Attention Mechanism. | Transformer. | Translation. | Attention weights. |
| `11_Autoencoders.ipynb` | Light | Representation Learning.| VAE. | Yield curves. | Latent space walk. |
| `12_Self_Supervised_Learning.ipynb` | Unknown Kernel | Pre-training. | Contrastive Loss. | Unlabeled data. | Embedding plot. |
| `13_Generative_Models.ipynb` | Standard | Distribution Learning. | GAN. | Synthetic data. | Generator output. |
| `14_Multi_modal_Fusion.ipynb` | Light | Data Integration. | Fusion Arch. | Text + Tabular. | Fusion weights. |
| `15_Reinforcement_Learning.ipynb` | Advanced | Optimal Control. | Q-Learning. | Grid world / Econ. | Policy map. |
| `16_Advanced_Deep_RL.ipynb` | Advanced | Policy Gradients. | PPO / A2C. | AI Economist. | Reward curve. |
| `17_Causal_ML.ipynb` | Vital | High-dim Confounding. | `DoubleML`. | 401(k) data. | CATE histogram. |
| `18_Natural_Language_Processing.ipynb` | Standard | Text as Data. | Word2Vec / BERT. | FOMC Minutes. | Word cloud /TSNE. |
| `19_Graph_Neural_Networks.ipynb` | Light | Network effects. | GCN. | Supply Chains. | Graph propagation. |
| `20_Geospatial_Data.ipynb` | Standard | Spatial Econometrics. | `geopandas`. | Census tracts. | Choropleth map. |
| `21_ML_for_Macro_Forecasting.ipynb` | Light | Nowcasting. | Factor Models / ML. | FRED-MD. | Forecast comparison. |
| `22_Style_Transfer_and_Advanced_Vision.ipynb` | Unknown Kernel | Fun / Niche. | CNN optimization. | Images. | Style transfer. |

---

## Module 08: Time Series
*Theme: Forecasting*
*Narrative Arc:* Modeling the temporal dependence of data to predict the future.

| Notebook | Status | Pedagogical Goal | Technical Spec | Data Source | Interactive Element |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `01_Introduction_to_Time_Series.ipynb` | Core | Serial Correlation. | Autocorrelation plots. | Stock returns. | Lag plot viewer. |
| `02_ARMA_Models.ipynb` | Standard | Linear Dynamics. | `statsmodels.tsa`. | Simulated ARMA. | Param stability check. |
| `03_ARIMA_and_Forecasting.ipynb` | Standard | Integration/Trends. | Box-Jenkins. | GDP. | Forecast fan chart. |
| `04A_VAR_Estimation_and_Granger.ipynb` | Core | Multi-equation dynamics.| VAR. | Macro vars. | Lag order diagnostics. |
| `04B_VAR_Identification_and_Structural_Shocks.ipynb` | Core | Identification assumptions. | Cholesky ordering. | Macro vars. | Ordering sensitivity check. |
| `04C_VAR_Impulse_Responses_and_FEVD.ipynb` | Core | Shock propagation. | IRF/FEVD. | Macro vars. | IRF/FEVD plot. |
| `05_Volatility_Modeling_ARCH_GARCH.ipynb` | Light | Heteroskedasticity. | `arch`. | S&P 500 Vol. | Volatility clustering. |
| `06_Cointegration_and_Error_Correction_Models.ipynb` | Advanced | Long-run relationships.| VECM / Engle-Granger. | Pairs trading. | Spread plot. |

---

## Module 09: Finance
*Theme: Pricing & Risk*
*Narrative Arc:* Valuing assets in uncertain environments using no-arbitrage conditions.

| Notebook | Status | Pedagogical Goal | Technical Spec | Data Source | Interactive Element |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `01_Portfolio_Theory.ipynb` | Standard | Diversification. | Mean-Variance Opt. | Asset returns. | Efficient frontier. |
| `02_Asset_Pricing.ipynb` | Core | Risk Premia. | CAPM / Fama-French. | F-F Factors. | Security Market Line. |
| `03_Option_Pricing.ipynb` | Core | Arbitrage Pricing. | Black-Scholes / Binomial. | Option chain. | Greeks visualizer. |
| `04_Continuous_Time_Finance.ipynb` | Advanced | Stochastic Calculus. | Ito's Lemma sim. | Brownian Motion. | Path simulation. |
| `05_Credit_Risk.ipynb` | Standard | Default Probability. | Merton Structural Model. | Corporate bond data. | Distance-to-default. |
| `06_High_Frequency_Data.ipynb` | Standard | Microstructure. | TAQ data format. | LOB snapshot. | Order book depth. |
| `07_Financial_Frictions_BGG.ipynb` | Advanced | Credit Constraints. | Bernanke-Gertler-Gilchrist. | N/A | External finance premium. |

---

## Module 10: Specialized Models
*Theme: Complexity & Networks*
*Narrative Arc:* Moving beyond the representative agent to emergent phenomena.

| Notebook | Status | Pedagogical Goal | Technical Spec | Data Source | Interactive Element |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `01_Agent_Based_Models.ipynb` | Vital | Emergence. | Schelling / Vectorized. | N/A | Grid animation. |
| `02_General_Equilibrium_with_Heterogeneous_Agents.ipynb`| Advanced | Distributional Macro. | Aiyagari / EGM. | N/A | Wealth dist evolution. |
| `03_Network_Economics.ipynb` | Standard | Connectivity. | Network Centrality. | Trade flows. | Force-directed graph. |

---

## Appendix & High Performance
*Theme: Tooling & Math*
*Narrative Arc:* The foundational skills required to build the models above.

| Notebook | Status | Pedagogical Goal | Technical Spec | Data Source | Interactive Element |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `T1_Publishing_with_Quarto.ipynb` | Tooling | Scientific Comm. | Quarto CLI. | N/A | Rendered output. |
| `T2_Replication_Exercise_Chetty_2014.ipynb` | Capstone | Replication. | OLS / Visuals. | Chetty Data. | Mobility map. |
| `T3_Autograding_with_Otter.ipynb` | Tooling | Assessment. | `otter-grader`. | N/A | Autograder demo. |
| `A1-Real-Analysis.ipynb` | Math | Rigor. | LaTeX Proofs. | N/A | Sequence convergence. |
| `A2-Multivariate-Calculus.ipynb` | Math | Optimization Math. | Jacobians. | N/A | Gradient field. |
| `A3-Probability-Theory.ipynb` | Math | Uncertainty Math. | Distributions. | N/A | PDF/CDF interactive. |
| `A4-Linear-Algebra.ipynb` | Math | Matrix Math. | Eigen decomp. | N/A | Transformation visual. |
| `high_performance_python/01_High_Performance_Computing.ipynb` | Advanced | Speed. | `numba`. | Pi Monte Carlo. | Speedup bar chart. |
| `high_performance_python/02_Accelerating_Code_with_Numba.ipynb`| Standard | JIT Compilation. | `@jit`. | Loops. | Runtime comparison. |
| `high_performance_python/03_Parallel_Computing_with_Dask.ipynb`| Standard | Out-of-core. | `dask`. | Big CSV. | Task graph. |
| `high_performance_python/04_GPU_Acceleration_with_CuPy.ipynb` | Niche | Hardware Accel. | `cupy`. | Matrix ops. | GPU vs CPU time. |
