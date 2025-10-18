import pandas_datareader.data as web
import pandas as pd

# --- Date Range ---
start_date, end_date = '1963-07-01', '2023-12-31'

# --- Download 10 Industry Portfolios ---
try:
    print("Downloading 10 Industry Portfolios data...")
    # The [0] selects the value-weighted monthly returns
    industry_portfolios = web.DataReader('10_Industry_Portfolios', 'famafrench', start=start_date, end=end_date)[0]

    output_path = 'data/10_industry_portfolios.csv'
    industry_portfolios.to_csv(output_path)
    print(f"Data downloaded and saved to {output_path}")

except Exception as e:
    print(f"An error occurred during data download: {e}")