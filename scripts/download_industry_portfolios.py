"""Refresh the bundled 10-industry Fama-French portfolio table."""

from pathlib import Path

import pandas_datareader.data as web

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
START_DATE, END_DATE = "1963-07-01", "2023-12-31"


def main() -> int:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    try:
        print("Downloading 10 Industry Portfolios data...")
        industry_portfolios = web.DataReader(
            "10_Industry_Portfolios",
            "famafrench",
            start=START_DATE,
            end=END_DATE,
        )[0]
        if industry_portfolios.empty:
            raise ValueError("Fama-French provider returned no observations.")
        output_path = DATA_DIR / "10_industry_portfolios.csv"
        industry_portfolios.to_csv(output_path)
        print(f"Data downloaded and saved to {output_path.relative_to(ROOT)}")
    except Exception as exc:
        print(f"FAIL: industry portfolio refresh: {exc}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
