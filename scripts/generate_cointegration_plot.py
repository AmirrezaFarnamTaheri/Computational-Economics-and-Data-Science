import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- Configuration ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'font.size': 14, 'figure.figsize': (14, 10), 'figure.dpi': 150})

# --- Generate Cointegrated Series ---
np.random.seed(123)
n_obs = 300
# 1. Create a common stochastic trend (a random walk)
common_trend = np.random.normal(size=n_obs, scale=0.5).cumsum() + 20

# 2. Create two I(1) series that share this common trend
# They are cointegrated because their difference will be stationary
y1 = common_trend + np.random.normal(size=n_obs, scale=1)
y2 = common_trend + np.random.normal(size=n_obs, scale=1)

# 3. Calculate the error (the deviation from the long-run relationship)
# In this simple case, the cointegrating vector is (1, -1)
error = y1 - y2

# --- Create the Plot ---
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
fig.suptitle('Visualization of Cointegration', fontsize=18)

# Plot the two I(1) series
ax1.plot(y1, label='$y_1$ (I(1) Series)')
ax1.plot(y2, label='$y_2$ (I(1) Series)')
ax1.set_title('Two Non-Stationary (I(1)) Series')
ax1.legend()
ax1.text(0, 4, 'The series share a common stochastic trend and never drift too far apart.', fontsize=12, style='italic')

# Plot the stationary linear combination (the error)
ax2.plot(error, label='Error Term ($u_t = y_{1,t} - y_{2,t}$)', color='green')
ax2.axhline(np.mean(error), color='r', linestyle='--', label='Mean of Error')
ax2.set_title('The Error Term ($u_t$) is Stationary (I(0))')
ax2.legend()
ax2.set_xlabel('Time')

plt.tight_layout(rect=[0, 0, 1, 0.95])
output_path = 'images/png/cointegration_visualization.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight')

print(f"Plot saved to {output_path}")