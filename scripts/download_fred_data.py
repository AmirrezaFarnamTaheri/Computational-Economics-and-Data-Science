"""
Download FRED economic data series used in the course.

Fetches the 6 FRED CSV files (CPIAUCSL, DPIC96, FEDFUNDS, GDPC1, INDPRO, PCECC96)
using pandas-datareader and saves them to the data/ directory.

Usage: python scripts/download_fred_data.py [--start 2000-01-01] [--end 2024-12-31]

Requires: pandas-datareader (`pip install pandas-datareader`)
"""

import argparse
import sys
from pathlib import Path

try:
    from pandas_datareader import data as pdr
except ImportError:
    print(
        "Error: pandas-datareader is required. Install with: pip install pandas-datareader"
    )
    sys.exit(1)

DATA_DIR = Path(__file__).parent.parent / "data"

SERIES = {
    "GDPC1": "Real Gross Domestic Product",
    "CPIAUCSL": "Consumer Price Index for All Urban Consumers",
    "FEDFUNDS": "Effective Federal Funds Rate",
    "DPIC96": "Real Disposable Personal Income",
    "PCECC96": "Real Personal Consumption Expenditures",
    "INDPRO": "Industrial Production Index",
}


def download_series(series_id, description, start, end):
    """Download a single FRED series and save to CSV."""
    output_path = DATA_DIR / f"{series_id}.csv"
    try:
        df = pdr.get_data_fred(series_id, start=start, end=end)
        df.to_csv(output_path)
        print(
            f"  OK: {series_id} ({description}) -> {output_path.name} ({len(df)} obs)"
        )
        return True
    except Exception as e:
        print(f"  FAIL: {series_id} -> {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Download FRED data for the course")
    parser.add_argument(
        "--start", default="2000-01-01", help="Start date (default: 2000-01-01)"
    )
    parser.add_argument(
        "--end", default="2024-12-31", help="End date (default: 2024-12-31)"
    )
    args = parser.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {len(SERIES)} FRED series ({args.start} to {args.end})...\n")

    ok = 0
    for series_id, description in SERIES.items():
        if download_series(series_id, description, args.start, args.end):
            ok += 1

    print(f"\nDone: {ok}/{len(SERIES)} series downloaded to {DATA_DIR}")


if __name__ == "__main__":
    main()
