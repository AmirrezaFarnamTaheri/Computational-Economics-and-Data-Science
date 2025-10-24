import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --- Setup Plot Style ---
sns.set_style("whitegrid")
plt.rcParams.update({'font.size': 12, 'figure.dpi': 150})

# --- Define parameters ---
mean = [0, 0]
n_samples = 1000
np.random.seed(42)

# Define different covariance matrices for different correlations
covariances = {
    r'$\rho = 0.9$': [[1.0, 0.9], [0.9, 1.0]],
    r'$\rho = 0.0$': [[1.0, 0.0], [0.0, 1.0]],
    r'$\rho = -0.7$': [[1.0, -0.7], [-0.7, 1.0]],
}

# --- Create the subplots ---
fig, axes = plt.subplots(1, 3, figsize=(15, 5))
fig.suptitle('Samples from Bivariate Normal Distributions', fontsize=18, y=1.02)

for ax, (title, cov) in zip(axes, covariances.items()):
    # Generate data
    x, y = np.random.multivariate_normal(mean, cov, n_samples).T

    # Create a scatter plot
    sns.scatterplot(x=x, y=y, ax=ax, alpha=0.6, s=20)

    # Create a density contour plot
    sns.kdeplot(x=x, y=y, ax=ax, levels=5, color='k', linewidths=1.0)

    # Formatting
    ax.set_title(title, fontsize=14)
    ax.set_xlabel('$X_1$')
    ax.set_ylabel('$X_2$')
    ax.set_aspect('equal', 'box')
    ax.set_xlim(-4, 4)
    ax.set_ylim(-4, 4)

plt.tight_layout(rect=[0, 0, 1, 0.96])

# --- Save the Figure ---
output_path = 'images/png/multivariate_normal_distribution.png'
plt.savefig(output_path)
print(f"Plot saved to {output_path}")