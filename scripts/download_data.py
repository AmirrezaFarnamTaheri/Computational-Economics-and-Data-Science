
import os
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf
from datetime import datetime
import time

def download_and_save(name, fetch_func, filename):
    print(f"Downloading {name}...")
    try:
        df = fetch_func()
        if df is not None and not df.empty:
            path = os.path.join("data", filename)
            df.to_csv(path)
            print(f"Saved {name} to {path}")
        else:
            print(f"Warning: {name} returned empty data.")
    except Exception as e:
        print(f"Error downloading {name}: {e}")

def fetch_sp500():
    # S&P 500 from Yahoo Finance
    end = datetime.now()
    start = datetime(2000, 1, 1)
    df = yf.download("^GSPC", start=start, end=end, progress=False)
    # yfinance returns MultiIndex columns sometimes, flatten if needed
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df

def fetch_fama_french():
    # Fama-French 3 Factors
    # Note: Requires connection to Kenneth French's data library
    # 'F-F_Research_Data_Factors' is the standard dataset
    try:
        ds = web.DataReader("F-F_Research_Data_Factors", "famafrench", start="2000-01-01")
        return ds[0] # Returns a dict, key 0 is monthly data
    except Exception as e:
        print(f"Fama-French download failed: {e}")
        return None

def fetch_us_macro():
    # GDP, CPI, Unemployment from FRED
    start = datetime(1960, 1, 1)
    end = datetime.now()
    series = ["GDPC1", "CPIAUCSL", "UNRATE", "FEDFUNDS"]
    try:
        df = web.DataReader(series, "fred", start, end)
        return df
    except Exception as e:
        print(f"FRED download failed: {e}")
        return None

def main():
    if not os.path.exists("data"):
        os.makedirs("data")

    download_and_save("S&P 500", fetch_sp500, "sp500.csv")
    download_and_save("Fama-French Factors", fetch_fama_french, "fama_french_factors.csv")
    download_and_save("US Macro Data", fetch_us_macro, "us_macro.csv")

    # California Housing is usually in sklearn, we can save it as CSV for consistency if needed
    # but the notebooks probably load it from sklearn.datasets.
    # We will skip it for now unless specific notebooks need it as CSV.

if __name__ == "__main__":
    main()
