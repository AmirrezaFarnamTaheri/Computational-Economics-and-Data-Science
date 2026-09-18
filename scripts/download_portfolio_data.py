import pandas as pd
import pandas_datareader.data as web
import yfinance as yf

# --- Tickers and Date Range ---
tickers = ["AAPL", "MSFT", "AMZN", "JPM", "XOM", "SPY"]
start_date, end_date = "2015-01-01", "2022-12-31"

# --- Download Stock Prices ---
try:
    print(f"Downloading price data for: {', '.join(tickers)}")
    # Keep the price definition explicit. yfinance has changed the default
    # auto_adjust behavior across releases; this course expects the distinct
    # "Adj Close" field so historical splits/dividends are incorporated once.
    prices = yf.download(
        tickers,
        start=start_date,
        end=end_date,
        auto_adjust=False,
        actions=False,
        progress=False,
    )

    if prices.empty:
        raise ValueError("yfinance returned no price observations.")

    # Select adjusted close and verify that every requested ticker is present.
    if isinstance(prices.columns, pd.MultiIndex):
        if "Adj Close" not in prices.columns.get_level_values(0):
            raise ValueError("Expected an 'Adj Close' field from yfinance.")
        adj_close = prices["Adj Close"].copy()
        missing_tickers = sorted(set(tickers) - set(adj_close.columns))
        if missing_tickers:
            raise ValueError(f"Missing requested tickers: {missing_tickers}")
    else:
        if "Adj Close" not in prices.columns:
            raise ValueError("Expected an 'Adj Close' field from yfinance.")
        adj_close = prices[["Adj Close"]].copy()

    if adj_close.dropna(how="all").empty:
        raise ValueError("Adjusted-close data contains no usable observations.")

    adj_close.to_csv("data/portfolio_prices.csv")
    print("Price data saved to data/portfolio_prices.csv")

except Exception as e:
    print(f"An error occurred during price download: {e}")

# --- Download Fama-French Factors ---
try:
    print("Downloading Fama-French 5-factor data...")
    # The [0] selects the monthly data table
    ff_factors = web.DataReader(
        "F-F_Research_Data_5_Factors_2x3", "famafrench", start=start_date, end=end_date
    )[0]
    ff_factors.to_csv("data/fama_french_5_factors.csv")
    print("Fama-French data saved to data/fama_french_5_factors.csv")

except Exception as e:
    print(f"An error occurred during Fama-French download: {e}")
