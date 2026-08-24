# Time Series Econometrics

> This page is synchronized from the authoritative notebooks. Use the generated reading view for searchable prose/code, or open the notebook for execution.

## Summary

**What problem are we solving?** Time series data is different. Observations are not independent; today depends on yesterday. * GDP growth is persistent. * Stock returns display volatility clustering. We need models that capture this temporal dependence to forecast the future and understand dynamic responses. **Why this method?** **ARMA (AutoRegressive Moving Average)** models describe the autocorrelation structure o

[Read generated page](../../notebooks/06-Econometrics/09_Classical_Time_Series_Analysis.md){ .md-button } [Open notebook](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/blob/main/06-Econometrics/09_Classical_Time_Series_Analysis.ipynb){ .md-button }

## Summary

**What problem are we solving?** Macroeconomic variables are endogenous. GDP affects Interest Rates, and Interest Rates affect GDP. Single-equation models cannot capture this feedback loop. **Vector Autoregression (VAR)** models treat all variables as endogenous. It is a system of equations where every variable depends on the past values of every variable. **Why this method?** VARs allow us to analyze dynamics withou

[Read generated page](../../notebooks/06-Econometrics/10_Vector_Autoregression.md){ .md-button } [Open notebook](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/blob/main/06-Econometrics/10_Vector_Autoregression.ipynb){ .md-button }
