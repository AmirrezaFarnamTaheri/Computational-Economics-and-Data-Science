# Data Directory

This directory contains datasets used throughout the course notebooks.

## FRED Economic Data

Downloaded from [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/).

| File | Series | Description |
|------|--------|-------------|
| `GDPC1.csv` | GDPC1 | Real Gross Domestic Product (billions of chained 2017 dollars) |
| `CPIAUCSL.csv` | CPIAUCSL | Consumer Price Index for All Urban Consumers |
| `FEDFUNDS.csv` | FEDFUNDS | Effective Federal Funds Rate |
| `DPIC96.csv` | DPIC96 | Real Disposable Personal Income |
| `PCECC96.csv` | PCECC96 | Real Personal Consumption Expenditures |
| `INDPRO.csv` | INDPRO | Industrial Production Index |

## Finance Data

| File | Source | Description |
|------|--------|-------------|
| `sp500.csv` | Yahoo Finance (`^GSPC`) | S&P 500 daily price data (Open, High, Low, Close, Volume) |
| `10_industry_portfolios.csv` | Kenneth French Data Library | Value-weighted returns for 10 industry portfolios |
| `fama_french_5_factors.csv` | Kenneth French Data Library | Fama-French 5-factor model data (Mkt-RF, SMB, HML, RMW, CMA, RF) |
| `fama_french_factors.csv` | Kenneth French Data Library | Fama-French 3-factor model data (Mkt-RF, SMB, HML, RF) |

## Research Data

| File | Source | Description |
|------|--------|-------------|
| `beijing_data.dta` | Academic dataset (Stata format) | Beijing housing market data for hedonic regression exercises |
| `SEntFiN.csv` | Academic dataset | Financial sentiment analysis data |
| `us_macro.csv` | FRED / compiled | U.S. macroeconomic indicators panel (GDP, unemployment, inflation, etc.) |

## Downloading / Updating Data

Several scripts in `scripts/` can refresh these datasets:

- `scripts/download_sp500.py` — Downloads S&P 500 data via `yfinance`
- `scripts/download_portfolio_data.py` — Downloads stock and Fama-French factor data
- `scripts/download_industry_portfolios.py` — Downloads industry portfolio returns

FRED data can also be fetched programmatically:

```python
from pandas_datareader import data
gdp = data.get_data_fred('GDPC1', start='2000')
```

## License

FRED data is public domain. Kenneth French data is freely available for academic use.
Other datasets retain their original licenses as noted in their source publications.
