import pandas as pd
import pandas_datareader.data as web
import matplotlib.pyplot as plt
import datetime

# Set the start and end dates for the data
start = datetime.datetime(1960, 1, 1)
end = datetime.datetime(1985, 1, 1)

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

# Create the plot
plt.style.use('seaborn-v0_8-whitegrid')
fig, ax = plt.subplots(figsize=(12, 8))

# Plot the 1960s
ax.plot(df.loc['1960':'1969', 'unemployment'], df.loc['1960':'1969', 'inflation'], 'o-', label='1960s')

# Plot the 1970s
ax.plot(df.loc['1970':'1979', 'unemployment'], df.loc['1970':'1979', 'inflation'], 'o-', label='1970s', color='orange')

# Add labels and title
ax.set_xlabel('Unemployment Rate (%)')
ax.set_ylabel('Inflation Rate (%)')
ax.set_title('The Phillips Curve Breakdown (1960-1979)', fontsize=16)
ax.legend()
ax.grid(True)

# Annotate some points
for year_end, row in df.loc['1960':'1979'].iterrows():
    year = year_end.year
    if year % 2 == 0:
        ax.annotate(str(year)[-2:],
                    (row['unemployment'], row['inflation']),
                    textcoords="offset points",
                    xytext=(0,5),
                    ha='center')


import os

# Create the directory if it doesn't exist
os.makedirs('../images/png', exist_ok=True)

# Save the figure
plt.savefig('../images/png/phillips_curve_breakdown.png', dpi=300, bbox_inches='tight')

print("Phillips Curve breakdown diagram created successfully.")
