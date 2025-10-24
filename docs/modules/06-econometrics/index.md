# Module 6: Econometrics

Master modern econometric methods for causal inference and statistical modeling.

---

## Overview

This module provides comprehensive coverage of econometric methods, from classical linear models to modern causal inference techniques. You'll learn both the theory and practical implementation of methods used in applied economic research.

**Duration:** 8-10 weeks
**Difficulty:** Advanced
**Prerequisites:** Modules 1-2, Probability & Statistics, Linear Algebra

---

## Learning Objectives

By the end of this module, you will be able to:

- ✓ Implement and interpret linear regression models
- ✓ Use maximum likelihood estimation effectively
- ✓ Apply modern causal inference methods
- ✓ Estimate models using GMM and instrumental variables
- ✓ Conduct rigorous difference-in-differences analysis
- ✓ Implement synthetic control methods
- ✓ Perform regression discontinuity designs
- ✓ Analyze time series and panel data
- ✓ Apply Bayesian econometric methods

---

## Topics Covered

### 1. Linear Model and OLS
**Notebook:** `01_Linear_Model_and_OLS.ipynb`

- Ordinary Least Squares (OLS) estimation
- Gauss-Markov theorem
- Statistical inference (standard errors, t-tests, F-tests)
- Heteroskedasticity and robust inference
- Weighted least squares
- Generalized least squares (GLS)

**Key Concepts:**
- Assumptions of the classical linear model
- BLUE (Best Linear Unbiased Estimator)
- Hypothesis testing
- Confidence intervals

**Applications:**
- Wage regressions
- Returns to education
- Production function estimation

---

### 2. Maximum Likelihood Estimation
**Notebook:** `02_Maximum_Likelihood.ipynb`

- Likelihood function and log-likelihood
- MLE properties (consistency, asymptotic normality)
- Information matrix and Cramér-Rao bound
- Likelihood ratio, Wald, and Lagrange multiplier tests
- Quasi-maximum likelihood
- Numerical optimization for MLE

**Advanced Topics:**
- Profile likelihood
- Concentrated likelihood
- EM algorithm

**Applications:**
- Probit and logit models
- Tobit models
- Count data models (Poisson, negative binomial)

---

### 3. Causal Inference
**Notebook:** `03_Causal_Inference.ipynb`

- Potential outcomes framework (Rubin causal model)
- Treatment effects (ATE, ATT, LATE)
- Selection bias and confounding
- Randomized controlled trials (RCTs)
- Observational studies and identification
- Matching methods (exact, propensity score)
- Sensitivity analysis

**Fundamental Concepts:**
- Counterfactuals
- Conditional independence assumption (CIA)
- Common support
- Parallel trends

**Applications:**
- Program evaluation
- Policy impact assessment
- Treatment effect heterogeneity

---

### 4. Generalized Method of Moments (GMM)
**Notebook:** `04_GMM.ipynb`

- Moment conditions and identification
- One-step and two-step GMM
- Optimal weighting matrix
- Overidentification tests (Hansen's J-test)
- GMM with weakly identified parameters
- Bootstrap inference

**Computational Implementation:**
- Defining moment functions
- Computing optimal weights
- Handling nonlinear restrictions

**Applications:**
- Asset pricing models
- Euler equation estimation
- Dynamic panel data

---

### 5. Instrumental Variables (IV)
**Notebook:** `05_Instrumental_Variables.ipynb`

- Endogeneity and omitted variable bias
- Two-stage least squares (2SLS)
- Instrument validity (relevance and exogeneity)
- Weak instruments problem
- Limited information maximum likelihood (LIML)
- Control function approach

**Testing:**
- First-stage F-statistic
- Sargan-Hansen test of overidentifying restrictions
- Durbin-Wu-Hausman endogeneity test

**Applications:**
- Returns to schooling with family background instruments
- Supply and demand estimation
- Peer effects

---

### 6. Regression Discontinuity Design (RDD)
**Notebook:** `06_Regression_Discontinuity.ipynb`

- Sharp vs. fuzzy RD
- Continuity-based identification
- Bandwidth selection
- Local polynomial regression
- Inference and robust standard errors
- Validation tests (density, placebo, covariate balance)

**Implementation:**
- Choosing kernel and bandwidth
- Sensitivity to specification
- Graphical analysis

**Applications:**
- School entry age effects
- Electoral competition
- Policy thresholds

---

### 7. Synthetic Control Methods
**Notebook:** `07_Synthetic_Control_Methods.ipynb`

- Synthetic control construction
- Donor pool selection
- Optimization for weights
- Inference via placebo tests
- Augmented synthetic control
- Matrix completion methods

**Recent Extensions:**
- Synthetic difference-in-differences
- Multiple treated units
- Time-varying treatments

**Applications:**
- State policy evaluation (California tobacco control)
- Country-level studies
- Firm-level interventions

---

### 8. Difference-in-Differences (DiD)
**Notebook:** `08_Difference_in_Differences.ipynb`

- Classical 2×2 DiD
- Parallel trends assumption
- Multiple time periods and groups
- Two-way fixed effects (TWFE)
- Recent advances (staggered adoption, heterogeneous treatment)
- Event study designs
- Triple differences

**Modern DiD Methods:**
- Callaway-Sant'Anna estimator
- Sun-Abraham interaction-weighted estimator
- Stacked DiD

**Applications:**
- Minimum wage effects
- Medicaid expansion
- Environmental policy

---

### 9. Classical Time Series Analysis
**Notebook:** `09_Classical_Time_Series_Analysis.ipynb`

- Stationarity and unit root tests
- Autocorrelation and partial autocorrelation
- ARMA models
- Model selection (AIC, BIC)
- Forecasting
- Structural breaks

**Testing:**
- Augmented Dickey-Fuller test
- Phillips-Perron test
- KPSS test

**Applications:**
- GDP forecasting
- Inflation persistence
- Interest rate dynamics

---

### 10. Vector Autoregression (VAR)
**Notebook:** `10_Vector_Autoregression.ipynb`

- VAR specification and estimation
- Impulse response functions (IRFs)
- Forecast error variance decomposition
- Structural VAR (SVAR)
- Identification through short-run/long-run restrictions
- Sign restrictions
- Granger causality

**Computational Methods:**
- Bootstrap confidence intervals for IRFs
- Recursive vs. rolling estimation
- Optimal lag selection

**Applications:**
- Monetary policy shocks
- Fiscal multipliers
- Oil price effects

---

### 11. Bayesian Econometrics
**Notebook:** `11_Bayesian_Econometrics.ipynb`

- Bayesian inference basics
- Prior, likelihood, and posterior
- Conjugate priors
- Markov Chain Monte Carlo (MCMC)
- Gibbs sampling
- Metropolis-Hastings algorithm
- Bayesian model comparison (Bayes factors, DIC)

**Practical Implementation:**
- PyMC for Bayesian modeling
- Convergence diagnostics
- Posterior predictive checks

**Applications:**
- Bayesian linear regression
- Hierarchical models
- Time-varying parameter models

---

### 12. Panel Data Methods
**Notebook:** `12_Panel_Data_Methods.ipynb`

- Fixed effects (within estimator)
- Random effects (GLS estimator)
- Hausman test
- First differences
- Dynamic panel data (Arellano-Bond, Blundell-Bond)
- Correlated random effects
- Clustered standard errors

**Advanced Topics:**
- Unbalanced panels
- Nonlinear panel models
- Interactive fixed effects

**Applications:**
- Firm productivity
- Individual wage dynamics
- International trade

---

## Prerequisites

### Required Knowledge

**Statistics:**
- Probability theory
- Statistical inference
- Hypothesis testing
- Asymptotic theory basics

**Mathematics:**
- Linear algebra (matrices, eigenvalues)
- Calculus (derivatives, optimization)
- Basic real analysis

**Programming:**
- Modules 1-2 completed
- Data manipulation with pandas
- NumPy proficiency

---

## Key Libraries

- **Statsmodels**: Comprehensive econometric models
- **Linearmodels**: Panel data and IV estimation
- **PyMC**: Bayesian statistical modeling
- **CausalML**: Causal inference methods
- **Scikit-learn**: Machine learning for causal inference
- **Pandas**: Data manipulation
- **Matplotlib/Seaborn**: Visualization

---

## Learning Path

### Week 1-2: Linear Models
- Complete notebooks 01-02
- Master OLS and MLE
- Understand asymptotic theory

### Week 3: Causal Inference Foundations
- Complete notebook 03
- Grasp potential outcomes framework
- Learn matching methods

### Week 4: GMM and IV
- Complete notebooks 04-05
- Solve endogeneity problems
- Implement IV estimators

### Week 5-6: Quasi-Experimental Methods
- Complete notebooks 06-08
- Master RDD, synthetic control, DiD
- Apply to policy evaluation

### Week 7-8: Time Series
- Complete notebooks 09-10
- Analyze temporal data
- Compute impulse responses

### Week 9: Bayesian Methods
- Complete notebook 11
- Implement MCMC
- Bayesian model comparison

### Week 10: Panel Data
- Complete notebook 12
- Fixed and random effects
- Dynamic panels

---

## Practice Exercises

Key exercises throughout the module:

1. **Wage Regression**: Estimate returns to education, test for heteroskedasticity
2. **Binary Choice**: Estimate labor force participation using probit/logit
3. **Matching**: Evaluate job training program with propensity score matching
4. **IV Estimation**: Estimate demand elasticity with cost shifters as instruments
5. **RDD Analysis**: Evaluate effect of class size on student achievement
6. **Synthetic Control**: Replicate California tobacco control study
7. **DiD**: Estimate minimum wage effects on employment
8. **VAR Analysis**: Compute monetary policy shock effects
9. **Bayesian Regression**: Implement Bayesian linear model with PyMC
10. **Panel FE**: Estimate production function with firm fixed effects

---

## Computational Challenges

### Challenge: Large Datasets
**Solutions:**
- Use sparse matrices
- Apply Dask for out-of-core computation
- Optimize pandas operations
- Consider sampling strategies

### Challenge: Bootstrap Inference
**Solutions:**
- Vectorize bootstrap loops
- Use parallel processing
- Apply wild bootstrap for clusters
- Block bootstrap for time series

### Challenge: Weak Identification
**Solutions:**
- Test instrument strength
- Use LIML or GMM-CUE
- Report robust confidence intervals
- Consider alternative identification

---

## Real-World Applications

Econometric methods are essential for:

**Academic Research:**
- Labor economics
- Public economics
- Development economics
- Industrial organization
- Macroeconomics

**Policy Analysis:**
- Program evaluation
- Cost-benefit analysis
- Impact assessment
- Forecasting

**Industry:**
- Marketing attribution
- A/B testing at scale
- Demand estimation
- Pricing strategy

---

## Key Debates

Modern econometrics features ongoing discussions:

1. **Design vs. Structure**: Reduced-form causal inference vs. structural modeling
2. **Inference**: Classical vs. Bayesian approaches
3. **Machine Learning**: Prediction vs. causal identification
4. **Credibility Revolution**: What makes research convincing?

Understanding these debates helps you:
- Choose appropriate methods
- Communicate research effectively
- Navigate literature critically

---

## Resources

### Essential Reading

**Textbooks:**
- Wooldridge, J. (2020). *Econometric Analysis of Cross Section and Panel Data*, 2nd ed.
- Angrist, J. & Pischke, J.-S. (2008). *Mostly Harmless Econometrics*
- Cameron, A. C. & Trivedi, P. K. (2005). *Microeconometrics*
- Hamilton, J. (1994). *Time Series Analysis*
- Hayashi, F. (2000). *Econometrics*

**Key Papers:**
- Rubin, D. (1974). "Estimating Causal Effects of Treatments"
- Hahn, J., Todd, P., & Van der Klaauw, W. (2001). "Identification and Estimation of Treatment Effects with RDD"
- Abadie, A., Diamond, A., & Hainmueller, J. (2010). "Synthetic Control Methods"
- Callaway, B. & Sant'Anna, P. (2021). "Difference-in-Differences with Multiple Time Periods"

### Online Resources
- [Mixtape Sessions](https://mixtape.scunning.com/) - Causal inference
- [Metrics Monday](https://thelittledataset.com/metrics-mondays/) - Econometric concepts
- [Nick Huntington-Klein's YouTube](https://www.youtube.com/@NickHuntingtonKlein) - Econometrics videos

---

## Software and Tools

- **Stata**: Industry standard (not covered, but principles transfer)
- **R**: Strong econometric packages (fixest, did, tidyverse)
- **Python**: Growing ecosystem (statsmodels, linearmodels, PyMC)

This course focuses on Python, but concepts apply across platforms.

---

## Assessment

Master these skills:

- [ ] Estimate and interpret regression models
- [ ] Conduct proper statistical inference
- [ ] Apply causal inference methods appropriately
- [ ] Diagnose and address endogeneity
- [ ] Implement quasi-experimental designs
- [ ] Analyze time series data
- [ ] Use panel data methods
- [ ] Perform Bayesian analysis
- [ ] Communicate results effectively

---

## Next Steps

After this module:

1. **Module 7: Machine Learning** - Complement causal methods with prediction
2. **Module 8: Time Series** - Deepen time series knowledge
3. **Real Research**: Apply methods to original research questions

---

## Tips for Success

1. **Understand Identification**: Always ask "What identifies the parameter?"
2. **Check Assumptions**: Test assumptions, don't just assume them
3. **Robust Inference**: Use robust/clustered standard errors appropriately
4. **Visualize**: Plot data before and after estimation
5. **Replicate**: Reproduce published results for practice
6. **Report Thoroughly**: Document all specification choices

---

## Common Pitfalls

### Pitfall: Interpreting Correlation as Causation
**Solution**: Use causal inference framework, identify assumptions explicitly

### Pitfall: p-Hacking and Specification Search
**Solution**: Pre-register analyses, report robustness checks

### Pitfall: Ignoring Clustered Dependence
**Solution**: Use clustered standard errors at appropriate level

### Pitfall: Weak Instruments
**Solution**: Test instrument strength, report robust confidence intervals

---

## Need Help?

- Review [Numerical Methods](../02-numerical-methods/index.md) for optimization
- Check [FAQ](../../resources/faq.md)
- See [References](../../resources/references.md)
- Join [Discussions](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/discussions)

---

**Ready to master econometrics?** Start with `01_Linear_Model_and_OLS.ipynb`!
