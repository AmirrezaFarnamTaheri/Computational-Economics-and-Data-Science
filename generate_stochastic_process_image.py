import numpy as np
import matplotlib.pyplot as plt

# --- Configuration ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'font.size': 14, 'figure.figsize': (12, 8), 'figure.dpi': 150})

# --- Generate Data ---
np.random.seed(42)
n_realizations = 5
n_steps = 100
ar_param = 0.9
process = np.zeros((n_steps, n_realizations))

for i in range(n_realizations):
    for t in range(1, n_steps):
        process[t, i] = ar_param * process[t-1, i] + np.random.normal()

# --- Plotting ---
plt.figure()
plt.plot(process)
plt.title('Five Realizations of a Stationary AR(1) Process')
plt.xlabel('Time')
plt.ylabel('Value')
plt.legend([f'Realization {i+1}' for i in range(n_realizations)], loc='upper left')

# --- Save Figure ---
plt.savefig('images/08-Time-Series/stochastic_process_realizations.png', dpi=300, bbox_inches='tight')
plt.close()

print("Image 'stochastic_process_realizations.png' generated successfully.")
