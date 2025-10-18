import pandas as pd
import pandas_datareader.data as web
import yfinance as yf

# --- Download S&P 500 data ---
# yfinance is generally more reliable than stooq
output_path = 'data/SP500.csv'
try:
    print("Attempting to download S&P 500 data using yfinance...")
    # The ticker for S&P 500 in Yahoo Finance is ^GSPC
    sp500 = yf.download('^GSPC', start='2000-01-01', end='2022-12-31')

    if sp500.empty:
        raise ValueError("Downloaded data is empty. Trying stooq.")

    # Save the data to a CSV file
    sp500.to_csv(output_path)
    print(f"Data downloaded and saved to {output_path}")

except Exception as e:
    print(f"yfinance failed: {e}")
    print("Falling back to pandas_datareader with stooq...")
    try:
        # The ticker for S&P 500 in Stooq is ^SPX
        sp500 = web.DataReader('^SPX', 'stooq', start='2000-01-01', end='2022-12-31')
        sp500.to_csv(output_path)
        print(f"Data downloaded from stooq and saved to {output_path}")
    except Exception as e2:
        print(f"Stooq also failed: {e2}")
        print("Could not download S&P 500 data.")