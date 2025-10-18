import yfinance as yf
import pandas as pd
import pandas_datareader.data as web

# --- Tickers and Date Range ---
tickers = ['AAPL', 'MSFT', 'AMZN', 'JPM', 'XOM', 'SPY']
start_date, end_date = '2015-01-01', '2022-12-31'

# --- Download Stock Prices ---
try:
    print(f"Downloading price data for: {', '.join(tickers)}")
    prices = yf.download(tickers, start=start_date, end=end_date)

    # Select 'Adj Close' and save
    if isinstance(prices.columns, pd.MultiIndex):
        adj_close = prices['Adj Close']
    else:
        # If only one ticker is downloaded, the columns are not multi-level
        adj_close = prices[['Adj Close']]

    adj_close.to_csv('data/portfolio_prices.csv')
    print("Price data saved to data/portfolio_prices.csv")

except Exception as e:
    print(f"An error occurred during price download: {e}")

# --- Download Fama-French Factors ---
try:
    print("Downloading Fama-French 5-factor data...")
    # The [0] selects the monthly data table
    ff_factors = web.DataReader('F-F_Research_Data_5_Factors_2x3', 'famafrench', start=start_date, end=end_date)[0]
    ff_factors.to_csv('data/fama_french_5_factors.csv')
    print("Fama-French data saved to data/fama_french_5_factors.csv")

except Exception as e:
    print(f"An error occurred during Fama-French download: {e}")