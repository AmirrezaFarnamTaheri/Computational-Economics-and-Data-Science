"""
Master Data Downloader Script
-----------------------------
This script ensures the 'data/' directory is populated with all necessary datasets
for the notebooks to run offline ("Batteries Included").

It handles:
1. S&P 500 Data (Yahoo Finance / Stooq)
2. Fama-French Factors (Ken French Library)
3. US Macro Data (FRED)
4. Portfolio Assets (Yahoo Finance)
5. Machine Learning Datasets (California Housing, etc.)

Usage:
    python scripts/download_data.py [--force]
"""

import os
import sys
import argparse
import pandas as pd
import pandas_datareader.data as web
import yfinance as yf
from pathlib import Path

# Constants
DATA_DIR = Path("data")
START_DATE = "1960-01-01"
END_DATE = "2023-12-31"

def ensure_data_dir():
    if not DATA_DIR.exists():
        print(f"Creating directory: {DATA_DIR}")
        DATA_DIR.mkdir(parents=True, exist_ok=True)

def download_sp500(force=False):
    path = DATA_DIR / "SP500.csv"
    if path.exists() and not force:
        print(f"Skipping S&P 500 (exists): {path}")
        return

    print("Downloading S&P 500 data (Yahoo Finance)...")
    try:
        # auto_adjust=True means 'Close' is already adjusted.
        df = yf.download("^GSPC", start="2000-01-01", end=END_DATE, progress=False, auto_adjust=True)
        if df.empty:
            raise ValueError("Empty dataframe from Yahoo")

        # Handle multi-index columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df = df['Close']
        elif 'Close' in df.columns:
            df = df['Close']

        df.to_csv(path)
        print(f"Saved: {path}")
    except Exception as e:
        print(f"Yahoo failed ({e}). Trying Stooq...")
        try:
            df = web.DataReader("^SPX", "stooq", start="2000-01-01", end=END_DATE)
            df.to_csv(path)
            print(f"Saved: {path}")
        except Exception as e2:
            print(f"Failed to download S&P 500: {e2}")

def download_fama_french(force=False):
    path = DATA_DIR / "fama_french_5_factors.csv"
    if path.exists() and not force:
        print(f"Skipping Fama-French (exists): {path}")
        return

    print("Downloading Fama-French 5 Factors...")
    try:
        # returns a dict of dataframes, [0] is the monthly data
        ds = web.DataReader("F-F_Research_Data_5_Factors_2x3", "famafrench", start=START_DATE, end=END_DATE)
        df = ds[0]
        df.to_csv(path)
        print(f"Saved: {path}")
    except Exception as e:
        print(f"Failed to download Fama-French data: {e}")

def download_macro_data(force=False):
    path = DATA_DIR / "us_macro_quarterly.csv"
    if path.exists() and not force:
        print(f"Skipping Macro Data (exists): {path}")
        return

    print("Downloading US Macro Data (FRED)...")
    tickers = {
        'GDPC1': 'Real_GDP',
        'CPIAUCSL': 'CPI',
        'FEDFUNDS': 'Fed_Funds_Rate',
        'UNRATE': 'Unemployment_Rate'
    }
    try:
        df = web.DataReader(list(tickers.keys()), "fred", start=START_DATE, end=END_DATE)
        df.rename(columns=tickers, inplace=True)
        df.to_csv(path)
        print(f"Saved: {path}")
    except Exception as e:
        print(f"Failed to download FRED data: {e}")

def download_portfolio_assets(force=False):
    path = DATA_DIR / "portfolio_prices.csv"
    if path.exists() and not force:
        print(f"Skipping Portfolio Assets (exists): {path}")
        return

    tickers = ['AAPL', 'MSFT', 'AMZN', 'JPM', 'XOM', 'SPY']
    print(f"Downloading Portfolio Assets: {tickers}...")
    try:
        # auto_adjust=True is the new default. Returns 'Close' which is adjusted.
        df = yf.download(tickers, start="2015-01-01", end=END_DATE, progress=False, auto_adjust=True)

        # yfinance returns a MultiIndex DataFrame (Price, Ticker) or just (Ticker) depending on version
        # If 'Close' is in the top level:
        if 'Close' in df.columns:
            df = df['Close']

        df.to_csv(path)
        print(f"Saved: {path}")
    except Exception as e:
        print(f"Failed to download portfolio assets: {e}")

def main():
    parser = argparse.ArgumentParser(description="Download external datasets for the project.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    args = parser.parse_args()

    ensure_data_dir()

    print("=== Starting Data Download ===")
    download_sp500(args.force)
    download_fama_french(args.force)
    download_macro_data(args.force)
    download_portfolio_assets(args.force)
    print("=== Download Complete ===")

if __name__ == "__main__":
    main()
