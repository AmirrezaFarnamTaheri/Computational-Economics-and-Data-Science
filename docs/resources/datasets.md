# Datasets

Economic datasets used throughout the course.

---

## Included Datasets

### FRED Economic Data

**Source:** Federal Reserve Economic Data (FRED)

**Files:**
- `GDPC1.csv` - Real GDP
- `CPIAUCSL.csv` - Consumer Price Index
- `UNRATE.csv` - Unemployment Rate
- `FEDFUNDS.csv` - Federal Funds Rate
- `DPIC96.csv` - Disposable Personal Income
- `PCECC96.csv` - Personal Consumption
- `INDPRO.csv` - Industrial Production

**API:** Use `pandas-datareader` to download updated data

```python
from pandas_datareader import data
gdp = data.get_data_fred('GDPC1', start='2000')
```

### Finance Data

- `SP500.csv` - S&P 500 returns
- `10_industry_portfolios.csv` - Industry portfolio returns
- `fama_french_5_factors.csv` - Fama-French factors

### Research Data

- `beijin_data.dta` - Beijing housing data (Stata format)
- `SEntFiN.csv` - Sentiment/Financial data

---

## External Data Sources

### Economic Data

- [FRED](https://fred.stlouisfed.org/) - Federal Reserve data
- [World Bank](https://data.worldbank.org/) - Global development data
- [IMF](https://www.imf.org/en/Data) - International financial data
- [OECD](https://data.oecd.org/) - OECD statistics

### Financial Data

- [Yahoo Finance](https://finance.yahoo.com/) - Stock market data
- [Quandl](https://www.quandl.com/) - Financial and economic data
- [Alpha Vantage](https://www.alphavantage.co/) - Market data API

### Research Data

- [NBER](https://www.nber.org/data) - Economic research data
- [Opportunity Insights](https://opportunityinsights.org/) - Social mobility data
- [IPUMS](https://ipums.org/) - Census and survey data

---

[:material-arrow-left: Back to Resources](index.md){ .md-button }
