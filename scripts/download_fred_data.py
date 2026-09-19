"""
Download FRED economic data series used in the course.

Fetches the 6 FRED CSV files (CPIAUCSL, DPIC96, FEDFUNDS, GDPC1, INDPRO, PCECC96)
using pandas-datareader and saves them to the data/ directory.

Usage: python scripts/download_fred_data.py [--start 1919-01-01] [--end 2024-12-31]

Every output is normalized to the stable schema
``observation_date,<SERIES_ID>``, which is the contract consumed by the
offline notebook fallbacks. The default start date intentionally preserves the
historical depth of the oldest bundled series (INDPRO).

Requires: pandas-datareader (`pip install pandas-datareader`)
"""

import argparse
import sys
from pathlib import Path

import pandas as pd

try:
    from pandas_datareader import data as pdr
except ImportError:
    print(
        "Error: pandas-datareader is required. Install with: pip install pandas-datareader"
    )
    sys.exit(1)

DATA_DIR = Path(__file__).parent.parent / "data"
DEFAULT_START = "1919-01-01"
DEFAULT_END = "2024-12-31"

# Downstream notebooks rely on the normalized two-column CSV contract:
# observation_date,<SERIES_ID>. Keep that contract independent of the exact
# index name returned by pandas-datareader.
SERIES = {
    "GDPC1": "Real Gross Domestic Product",
    "CPIAUCSL": "Consumer Price Index for All Urban Consumers",
    "FEDFUNDS": "Effective Federal Funds Rate",
    "DPIC96": "Real Disposable Personal Income",
    "PCECC96": "Real Personal Consumption Expenditures",
    "INDPRO": "Industrial Production Index",
}


def normalize_fred_frame(df, series_id):
    """Return a validated frame matching the bundled FRED CSV contract."""
    if df.empty:
        raise ValueError("provider returned no observations")
    if list(df.columns) != [series_id]:
        raise ValueError(
            f"expected exactly column {series_id!r}, got {list(df.columns)!r}"
        )

    normalized = df.copy()
    dates = pd.to_datetime(normalized.index, errors="coerce")
    values = pd.to_numeric(normalized[series_id], errors="coerce")
    valid = dates.notna() & values.notna()
    normalized = pd.DataFrame(
        {series_id: values.loc[valid].to_numpy()},
        index=pd.DatetimeIndex(dates[valid], name="observation_date"),
    )
    normalized = normalized[~normalized.index.duplicated(keep="last")].sort_index()
    if normalized.empty:
        raise ValueError("no valid dated numeric observations after normalization")
    return normalized


def download_series(series_id, description, start, end):
    """Download, validate, and save one FRED series using the shared CSV schema."""
    output_path = DATA_DIR / f"{series_id}.csv"
    try:
        raw = pdr.get_data_fred(series_id, start=start, end=end)
        df = normalize_fred_frame(raw, series_id)
        df.to_csv(output_path, index_label="observation_date")
        # Read back the artifact so a serialization/schema regression fails the refresh.
        check = pd.read_csv(output_path, nrows=5)
        if list(check.columns) != ["observation_date", series_id]:
            raise ValueError(f"serialized schema mismatch: {list(check.columns)!r}")
        print(
            f"  OK: {series_id} ({description}) -> {output_path.name} "
            f"({len(df)} obs, {df.index.min().date()} to {df.index.max().date()})"
        )
        return True
    except Exception as e:
        print(f"  FAIL: {series_id} -> {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Download FRED data for the course")
    parser.add_argument(
        "--start",
        default=DEFAULT_START,
        help=f"Start date (default: {DEFAULT_START}; preserves the oldest bundled series)",
    )
    parser.add_argument(
        "--end",
        default=DEFAULT_END,
        help=f"End date (default: {DEFAULT_END})",
    )
    args = parser.parse_args()

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {len(SERIES)} FRED series ({args.start} to {args.end})...\n")

    ok = 0
    for series_id, description in SERIES.items():
        if download_series(series_id, description, args.start, args.end):
            ok += 1

    print(f"\nDone: {ok}/{len(SERIES)} series downloaded to {DATA_DIR}")
    return 0 if ok == len(SERIES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
