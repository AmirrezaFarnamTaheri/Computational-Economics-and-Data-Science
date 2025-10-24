# Module 8: Time Series Analysis

Master modern time series methods for economic and financial data.

---

## Overview

This module provides comprehensive coverage of time series econometrics, from classical ARMA models to modern volatility modeling and cointegration techniques. You'll learn to analyze, forecast, and understand temporal dynamics in economic data.

**Duration:** 4-5 weeks
**Difficulty:** Advanced
**Prerequisites:** Module 6 (Econometrics), probability theory, basic time series concepts

---

## Learning Objectives

By the end of this module, you will be able to:

- ✓ Model and forecast univariate time series
- ✓ Estimate ARMA and ARIMA models
- ✓ Test for stationarity and unit roots
- ✓ Analyze multivariate time series with VAR
- ✓ Model volatility using ARCH/GARCH
- ✓ Test for and model cointegration
- ✓ Apply error correction models
- ✓ Forecast economic and financial variables

---

## Topics Covered

### 1. Introduction to Time Series
**Notebook:** `01_Introduction_to_Time_Series.ipynb`

- Time series data characteristics
- Stationarity: strict vs. weak
- Autocovariance and autocorrelation functions
- Partial autocorrelation function (PACF)
- White noise and random walks
- Trends and seasonality
- Time series decomposition

**Fundamental Concepts:**
- Lag operator notation
- Difference operator
- Moving average representation
- Wold decomposition theorem

**Data Handling:**
- Date/time indexing in pandas
- Handling missing data
- Seasonal adjustment
- Frequency conversion

**Applications:**
- Exploratory time series analysis
- Identifying patterns in data
- Decomposing economic indicators

---

### 2. ARMA Models
**Notebook:** `02_ARMA_Models.ipynb`

- Autoregressive (AR) models
- Moving average (MA) models
- ARMA(p,q) specification
- Identification using ACF/PACF
- Maximum likelihood estimation
- Diagnostic checking
- Information criteria (AIC, BIC)

**AR Models:**
- AR(1) process and properties
- Higher-order AR processes
- Stationarity conditions
- Yule-Walker equations

**MA Models:**
- MA(1) process and properties
- Higher-order MA processes
- Invertibility conditions
- Identification challenges

**ARMA Estimation:**
- Method of moments
- Maximum likelihood
- Conditional sum of squares
- State space methods

**Applications:**
- Modeling economic growth
- Interest rate dynamics
- Inflation persistence

---

### 3. ARIMA and Forecasting
**Notebook:** `03_ARIMA_and_Forecasting.ipynb`

- Integrated processes and unit roots
- ARIMA(p,d,q) models
- Seasonal ARIMA (SARIMA)
- Model selection strategy (Box-Jenkins)
- Point forecasts and prediction intervals
- Rolling and recursive forecasting
- Forecast evaluation (RMSE, MAE, MAPE)

**Differencing:**
- First and higher-order differences
- Seasonal differencing
- Overdifferencing issues

**Unit Root Tests:**
- Augmented Dickey-Fuller (ADF) test
- Phillips-Perron (PP) test
- KPSS test
- Interpreting test results

**Forecasting:**
- One-step-ahead forecasts
- Multi-step-ahead forecasts
- Forecast intervals
- Forecast combination

**Applications:**
- GDP forecasting
- Unemployment rate prediction
- Sales forecasting

---

### 4. Vector Autoregression (VAR)
**Notebook:** `04_Vector_Autoregression.ipynb`

- VAR model specification
- OLS estimation of VAR
- Lag length selection
- Impulse response functions (IRFs)
- Forecast error variance decomposition (FEVD)
- Granger causality testing
- Structural VAR (SVAR) identification

**VAR Theory:**
- Reduced-form vs. structural VAR
- Stability conditions
- MA representation

**Identification:**
- Recursive (Cholesky) identification
- Short-run restrictions
- Long-run restrictions
- Sign restrictions

**Inference:**
- Bootstrap confidence intervals
- Asymptotic standard errors
- Bayesian VAR (BVAR)

**Applications:**
- Monetary policy analysis
- Fiscal policy effects
- Macro variable interactions
- Business cycle analysis

---

### 5. Volatility Modeling: ARCH/GARCH
**Notebook:** `05_Volatility_Modeling_ARCH_GARCH.ipynb`

- Stylized facts of financial returns
- Conditional heteroskedasticity
- ARCH models
- GARCH(p,q) specification
- Extensions: EGARCH, TGARCH, FIGARCH
- Volatility forecasting
- Risk management applications

**ARCH Models:**
- ARCH(1) and properties
- Estimation by MLE
- Testing for ARCH effects
- Ljung-Box test on squared residuals

**GARCH Models:**
- GARCH(1,1) - the workhorse model
- Variance targeting
- Persistence and half-life
- Forecasting volatility

**Advanced Models:**
- EGARCH (exponential GARCH)
- GJR-GARCH (threshold GARCH)
- Integrated GARCH (long memory)
- Multivariate GARCH

**Applications:**
- Stock return volatility
- Exchange rate volatility
- Value-at-Risk (VaR) calculation
- Option pricing inputs
- Portfolio risk management

---

### 6. Cointegration and Error Correction Models
**Notebook:** `06_Cointegration_and_Error_Correction_Models.ipynb`

- Spurious regression problem
- Concept of cointegration
- Engle-Granger two-step method
- Johansen cointegration test
- Vector error correction model (VECM)
- Long-run and short-run dynamics
- Testing restrictions on cointegrating vectors

**Theory:**
- I(1) processes
- Common stochastic trends
- Granger representation theorem
- Cointegration rank

**Testing:**
- Engle-Granger test
- Johansen trace and max eigenvalue tests
- Determining cointegration rank

**VECM:**
- Specification and estimation
- Loading coefficients
- Adjustment speeds
- Impulse responses in VECM

**Applications:**
- Purchasing power parity (PPP)
- Interest rate parity
- Consumption and income relationships
- Money demand functions
- Term structure of interest rates

---

## Prerequisites

### Required Knowledge

**Statistics:**
- Probability theory
- Statistical inference
- Hypothesis testing
- Maximum likelihood estimation

**Mathematics:**
- Linear algebra
- Complex numbers (for AR roots)
- Calculus and optimization

**Programming:**
- Module 1 (Python foundations)
- Module 6 (Econometrics basics)
- pandas for time series

**Economics:**
- Basic macro concepts
- Financial markets knowledge helpful

---

## Key Libraries

- **Statsmodels**: Comprehensive time series tools
  - `statsmodels.tsa.arima.model.ARIMA`
  - `statsmodels.tsa.statespace.sarimax.SARIMAX`
  - `statsmodels.tsa.vector_ar.var_model.VAR`
  - `statsmodels.tsa.stattools` (unit root tests)

- **Arch**: Volatility modeling
  - `arch.univariate` (ARCH/GARCH)
  - `arch.bootstrap` (inference)

- **Pandas**: Time series data structures
- **NumPy**: Numerical operations
- **Matplotlib/Seaborn**: Visualization

---

## Learning Path

### Week 1: Foundations
- Complete notebooks 01-02
- Master stationarity concepts
- Fit ARMA models

### Week 2: Forecasting
- Complete notebook 03
- Learn Box-Jenkins methodology
- Implement ARIMA forecasting

### Week 3: Multivariate Models
- Complete notebook 04
- Estimate VAR models
- Compute impulse responses

### Week 4: Volatility
- Complete notebook 05
- Model conditional heteroskedasticity
- Forecast volatility

### Week 5: Cointegration
- Complete notebook 06
- Test for cointegration
- Estimate VECM

---

## Practice Exercises

Key exercises throughout the module:

1. **ACF/PACF Analysis**: Identify appropriate ARMA orders for GDP growth
2. **Unit Root Testing**: Test various economic series for stationarity
3. **ARIMA Forecasting**: Build forecasting model for unemployment
4. **VAR Analysis**: Analyze monetary policy shocks with 3-variable VAR
5. **GARCH Estimation**: Model S&P 500 return volatility
6. **VaR Calculation**: Compute 1-day ahead Value-at-Risk using GARCH
7. **Cointegration Test**: Test PPP for exchange rates
8. **VECM Estimation**: Model consumption-income relationship with VECM

---

## Computational Challenges

### Challenge: Model Selection
**Solutions:**
- Use information criteria (AIC, BIC)
- Cross-validation for forecasting
- Diagnostic checking of residuals
- Compare out-of-sample performance

### Challenge: Non-Convergence in MLE
**Solutions:**
- Try different starting values
- Simplify model (reduce parameters)
- Check for identification issues
- Use method of moments for initial values

### Challenge: High-Dimensional VAR
**Solutions:**
- Apply dimension reduction
- Use Bayesian VAR with shrinkage priors
- Factor-augmented VAR (FAVAR)
- Sparse VAR methods

### Challenge: Structural Breaks
**Solutions:**
- Test for breaks (Chow test, Quandt-Andrews)
- Use rolling/recursive estimation
- Allow for time-varying parameters
- Robust forecasting methods

---

## Common Pitfalls

### Pitfall: Spurious Regression
**Issue**: Regressing non-stationary variables gives misleading results

**Solution**:
- Test for unit roots first
- Difference data or test for cointegration
- Use appropriate specification (VECM if cointegrated)

### Pitfall: Overfitting
**Issue**: Too many parameters, poor out-of-sample performance

**Solution**:
- Use information criteria
- Validate on holdout data
- Prefer parsimonious models

### Pitfall: Ignoring Structural Breaks
**Issue**: Parameters change over time

**Solution**:
- Plot data and residuals
- Formal break tests
- Use robust methods

### Pitfall: Misinterpreting Granger Causality
**Issue**: Granger causality ≠ true causality

**Solution**:
- Careful interpretation
- Consider economic theory
- Use with other evidence

---

## Real-World Applications

Time series methods are essential for:

**Central Banks:**
- Inflation forecasting
- Monetary policy analysis
- Nowcasting GDP
- Financial stability monitoring

**Finance:**
- Asset return modeling
- Volatility forecasting
- Risk management
- Trading strategies

**Businesses:**
- Demand forecasting
- Inventory management
- Revenue projection
- Capacity planning

**Government:**
- Economic forecasting
- Budget projections
- Policy impact analysis

**Academia:**
- Business cycle research
- Macro empirics
- Financial econometrics

---

## Model Selection Guide

### Choose ARMA when:
- Data is stationary
- Need to model short-term dynamics
- Interested in autocorrelation structure

### Choose ARIMA when:
- Data has unit roots
- Need to forecast non-stationary series
- Dealing with trending data

### Choose VAR when:
- Multiple related time series
- Interested in dynamic interactions
- Want impulse response analysis

### Choose GARCH when:
- Modeling financial returns
- Volatility clustering present
- Risk management applications

### Choose VECM when:
- Variables are cointegrated
- Modeling long-run relationships
- Separating short-run and long-run dynamics

---

## Resources

### Essential Reading

**Textbooks:**
- Hamilton, J. (1994). *Time Series Analysis*. Princeton
- Lütkepohl, H. (2005). *New Introduction to Multiple Time Series Analysis*
- Tsay, R. (2010). *Analysis of Financial Time Series*, 3rd ed.
- Enders, W. (2014). *Applied Econometric Time Series*, 4th ed.

**Papers:**
- Engle, R. (1982). "Autoregressive Conditional Heteroskedasticity"
- Bollerslev, T. (1986). "Generalized Autoregressive Conditional Heteroskedasticity"
- Johansen, S. (1988). "Statistical Analysis of Cointegration Vectors"
- Sims, C. (1980). "Macroeconomics and Reality"

### Online Resources
- [Statsmodels Time Series](https://www.statsmodels.org/stable/tsa.html)
- [NBER Time Series Analysis](https://www.nber.org/econometrics_minicourse_2014/2014si_timeseries.pdf)
- [Penn State Time Series Course](https://online.stat.psu.edu/stat510/)

---

## Datasets

Practice with real economic data:

**Sources:**
- [FRED](https://fred.stlouisfed.org/) - US economic data
- [Yahoo Finance](https://finance.yahoo.com/) - Financial data
- [Quandl](https://www.quandl.com/) - Multiple data sources
- [World Bank](https://data.worldbank.org/) - International data
- [ECB Statistical Data Warehouse](https://sdw.ecb.europa.eu/) - European data

**Recommended Series:**
- GDP, unemployment, inflation (macro)
- Stock indices, exchange rates (finance)
- Interest rates (money markets)
- Commodity prices

---

## Assessment

To master this module, demonstrate ability to:

- [ ] Test for stationarity and understand implications
- [ ] Identify and estimate ARMA/ARIMA models
- [ ] Produce and evaluate forecasts
- [ ] Estimate and interpret VAR models
- [ ] Compute impulse response functions
- [ ] Model volatility with ARCH/GARCH
- [ ] Test for and model cointegration
- [ ] Estimate and interpret VECM
- [ ] Choose appropriate models for different contexts
- [ ] Communicate results effectively

---

## Next Steps

After completing this module:

1. **Module 7: Machine Learning** - Modern forecasting with ML
2. **Module 9: Finance** - Apply to asset pricing and portfolio theory
3. **Research**: Use time series methods in applied work
4. **Advanced Topics**: State space models, Bayesian methods, high-frequency data

---

## Tips for Success

1. **Visualize First**: Always plot your data before modeling
2. **Check Stationarity**: Test for unit roots before proceeding
3. **Diagnostic Checking**: Examine residuals carefully
4. **Out-of-Sample Testing**: Validate forecasts on holdout data
5. **Economic Intuition**: Models should make economic sense
6. **Start Simple**: Begin with parsimonious models
7. **Compare Models**: Multiple approaches often useful
8. **Document Choices**: Keep track of specification decisions

---

## Software Tips

### Efficient Workflow
```python
# Load data with datetime index
import pandas as pd
data = pd.read_csv('data.csv', index_col=0, parse_dates=True)

# Quick diagnostics
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
plot_acf(data)
plot_pacf(data)

# Fit ARIMA efficiently
from statsmodels.tsa.arima.model import ARIMA
model = ARIMA(data, order=(1,1,1))
results = model.fit()
print(results.summary())

# Forecast
forecast = results.forecast(steps=12)
```

---

## Need Help?

- Review [Econometrics](../06-econometrics/index.md) for statistical foundations
- Check [Numerical Methods](../02-numerical-methods/index.md) for optimization
- See [FAQ](../../resources/faq.md)
- Join [Discussions](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/discussions)
- Visit [Statsmodels Community](https://groups.google.com/forum/#!forum/pystatsmodels)

---

**Ready to analyze time series?** Start with `01_Introduction_to_Time_Series.ipynb`!
