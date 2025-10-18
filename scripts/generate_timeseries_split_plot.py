import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import TimeSeriesSplit

# --- Configuration ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'font.size': 14, 'figure.figsize': (14, 10), 'figure.dpi': 150})

# --- Generate Synthetic Data ---
np.random.seed(101)
n_points = 150
t = np.arange(n_points)
# A series with trend, seasonality, and noise
y = 0.5 * t + 20 * np.sin(t * 2 * np.pi / 30) + np.random.randn(n_points) * 5 + 50
series = pd.Series(y, index=pd.date_range('2020-01-01', periods=n_points, freq='D'))

# --- Setup TimeSeriesSplit ---
n_splits = 5
tscv = TimeSeriesSplit(n_splits=n_splits)

# --- Create the Plot ---
fig, axes = plt.subplots(n_splits, 1, figsize=(12, 10), sharex=True)
fig.suptitle('Expanding Window Cross-Validation (TimeSeriesSplit)', fontsize=18, y=0.93)

for i, (train_index, test_index) in enumerate(tscv.split(series)):
    ax = axes[i]

    # Plot the full series in grey
    ax.plot(series.index, series.values, color='gray', alpha=0.5, label='Full Series')

    # Plot the training data for this fold
    train_series = series.iloc[train_index]
    ax.plot(train_series.index, train_series.values, color='blue', lw=2.5, label='Train Data')

    # Plot the testing data for this fold
    test_series = series.iloc[test_index]
    ax.plot(test_series.index, test_series.values, color='red', lw=2.5, linestyle='--', marker='o', markersize=5, label='Test Data')

    ax.set_ylabel(f'Fold {i+1}')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

axes[-1].set_xlabel('Time')
handles, labels = axes[0].get_legend_handles_labels()
fig.legend(handles, labels, loc='upper right', bbox_to_anchor=(0.95, 0.9))

plt.tight_layout(rect=[0, 0, 1, 0.9])
output_path = 'images/timeseries_split_visualization.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')

print(f"Plot saved to {output_path}")