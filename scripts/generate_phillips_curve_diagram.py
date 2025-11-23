import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime
import os

# Set the start and end dates for the data
start = datetime.datetime(1960, 1, 1)
end = datetime.datetime(1985, 1, 1)

try:
    # Download inflation and unemployment data from FRED
    inflation = web.DataReader('CPIAUCNS', 'fred', start, end)
    unemployment = web.DataReader('UNRATE', 'fred', start, end)

    # Resample to annual data, taking the last value of the year for inflation
    # and the average for unemployment
    inflation_annual = inflation.resample('YE').last().pct_change(12) * 100
    unemployment_annual = unemployment.resample('YE').mean()

    # Create a DataFrame with the two series
    df = pd.DataFrame({'inflation': inflation_annual['CPIAUCNS'],
                       'unemployment': unemployment_annual['UNRATE']})
    df = df.dropna()

except Exception as e:
    print(f"Could not download data from FRED: {e}")
    print("Using hardcoded representative data for illustration.")
    # Representative data points for 1960-1979
    data = {
        'year': range(1960, 1980),
        'unemployment': [5.5, 6.7, 5.5, 5.7, 5.2, 4.5, 3.8, 3.8, 3.6, 3.5, # 60s
                         4.9, 5.9, 5.6, 4.9, 5.6, 8.5, 7.7, 7.1, 6.1, 5.8], # 70s
        'inflation': [1.4, 0.7, 1.3, 1.6, 1.0, 1.9, 3.5, 3.0, 4.7, 6.2, # 60s
                      5.5, 3.3, 3.4, 8.7, 12.3, 7.0, 4.9, 6.7, 9.0, 13.3] # 70s
    }
    df = pd.DataFrame(data).set_index(pd.to_datetime([f"{y}-12-31" for y in data['year']]))

# Create the plot
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the 1960s
ax.plot(df['unemployment'][df.index.year < 1970], df['inflation'][df.index.year < 1970], 'o-', label='1960s')

# Plot the 1970s
ax.plot(df['unemployment'][df.index.year >= 1970], df['inflation'][df.index.year >= 1970], 'o-', label='1970s', color='orange')

# Add labels and title
ax.set_xlabel('Unemployment Rate (%)')
ax.set_ylabel('Inflation Rate (%)')
ax.set_title('The Phillips Curve Breakdown (1960-1979)', fontsize=16)
ax.legend()
ax.grid(True)

# Annotate some points
for date, row in df.iterrows():
    year = date.year
    if year % 2 == 0:
        ax.annotate(str(year)[-2:],
                    (row['unemployment'], row['inflation']),
                    textcoords="offset points",
                    xytext=(0,5),
                    ha='center')


# Create the directory if it doesn't exist
# Using relative path that assumes script is run from repo root
os.makedirs('images/png', exist_ok=True)

# Save the figure
plt.savefig('images/png/1.1-phillips-curve-breakdown.png', dpi=300, bbox_inches='tight')

print("Phillips Curve breakdown diagram created successfully.")
