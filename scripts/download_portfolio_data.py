"""Refresh the bundled portfolio-price and Fama-French inputs.

The command is intentionally fail-fast for automation: if either upstream
refresh fails, the process exits non-zero instead of leaving a partial refresh
that looks successful.
"""

from pathlib import Path

import pandas as pd
import pandas_datareader.data as web
import yfinance as yf

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
TICKERS = ["AAPL", "MSFT", "AMZN", "JPM", "XOM", "SPY"]
START_DATE, END_DATE = "2015-01-01", "2022-12-31"


def download_prices() -> Path:
    """Download adjusted closes with an explicit yfinance adjustment policy."""
    print(f"Downloading price data for: {', '.join(TICKERS)}")
    prices = yf.download(
        TICKERS,
        start=START_DATE,
        end=END_DATE,
        auto_adjust=False,
        actions=False,
        progress=False,
    )
    if prices.empty:
        raise ValueError("yfinance returned no price observations.")

    if isinstance(prices.columns, pd.MultiIndex):
        if "Adj Close" not in prices.columns.get_level_values(0):
            raise ValueError("Expected an 'Adj Close' field from yfinance.")
        adj_close = prices["Adj Close"].copy()
        missing_tickers = sorted(set(TICKERS) - set(adj_close.columns))
        if missing_tickers:
            raise ValueError(f"Missing requested tickers: {missing_tickers}")
    else:
        if "Adj Close" not in prices.columns:
            raise ValueError("Expected an 'Adj Close' field from yfinance.")
        adj_close = prices[["Adj Close"]].copy()

    if adj_close.dropna(how="all").empty:
        raise ValueError("Adjusted-close data contains no usable observations.")

    output = DATA_DIR / "portfolio_prices.csv"
    adj_close.to_csv(output)
    print(f"Price data saved to {output.relative_to(ROOT)}")
    return output


def download_fama_french() -> Path:
    """Download the monthly Fama-French five-factor table."""
    print("Downloading Fama-French 5-factor data...")
    ff_factors = web.DataReader(
        "F-F_Research_Data_5_Factors_2x3",
        "famafrench",
        start=START_DATE,
        end=END_DATE,
    )[0]
    if ff_factors.empty:
        raise ValueError("Fama-French provider returned no observations.")
    output = DATA_DIR / "fama_french_5_factors.csv"
    ff_factors.to_csv(output)
    print(f"Fama-French data saved to {output.relative_to(ROOT)}")
    return output


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    for label, loader in (
        ("portfolio prices", download_prices),
        ("Fama-French factors", download_fama_french),
    ):
        try:
            loader()
        except Exception as exc:
            failures.append(f"{label}: {exc}")
            print(f"FAIL: {label}: {exc}")

    if failures:
        print(f"Refresh incomplete: {len(failures)} source(s) failed.")
        return 1
    print("Refresh complete: all portfolio inputs downloaded successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
