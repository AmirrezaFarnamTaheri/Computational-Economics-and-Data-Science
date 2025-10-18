import os
import numpy as np
import matplotlib.pyplot as plt
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

def generate_bias_variance_tradeoff_image():
    """
    Generates and saves a plot illustrating the bias-variance trade-off.
    """
    output_dir = "images/ml_intro"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "figure1_bias_variance_tradeoff.png")

    # Define the true function
    def true_function(X):
        return np.cos(1.5 * np.pi * X)

    # Function to generate data with noise
    def generate_data(n_samples=40, noise=0.3, random_state=0):
        rng = np.random.default_rng(random_state)
        X = np.sort(rng.random((n_samples, 1)), axis=0)
        y = true_function(X).ravel() + rng.normal(0, noise, n_samples)
        return X, y

    n_simulations = 100
    max_degree = 12
    degrees = np.arange(1, max_degree + 1)

    # Test data is fixed across all simulations
    X_test = np.linspace(0, 1, 100).reshape(-1, 1)
    y_test_true = true_function(X_test).ravel()
    noise_variance = 0.3**2

    avg_expected_prediction_error = np.zeros(max_degree)
    avg_bias_sq = np.zeros(max_degree)
    avg_variance = np.zeros(max_degree)

    for degree in degrees:
        # Store predictions for each simulation at this degree
        y_test_predictions = np.zeros((n_simulations, len(X_test)))

        for i in range(n_simulations):
            X_train, y_train = generate_data(random_state=i)
            model = make_pipeline(PolynomialFeatures(degree), LinearRegression())
            model.fit(X_train, y_train)
            y_test_predictions[i, :] = model.predict(X_test)

        # Calculate bias, variance, and MSE
        avg_prediction = np.mean(y_test_predictions, axis=0)
        avg_bias_sq[degree-1] = np.mean((avg_prediction - y_test_true)**2)
        avg_variance[degree-1] = np.mean(np.var(y_test_predictions, axis=0))
        avg_expected_prediction_error[degree-1] = np.mean(np.mean((y_test_predictions - y_test_true)**2, axis=1))

    # Plotting
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(degrees, avg_bias_sq, 'o-', color='skyblue', lw=2, label='Squared Bias')
    ax.plot(degrees, avg_variance, 'o-', color='sandybrown', lw=2, label='Variance')
    ax.plot(degrees, avg_expected_prediction_error, 'o-', color='red', lw=3, label='Total Test Error (MSE)')
    ax.axhline(noise_variance, color='gray', ls='--', lw=2, label='Irreducible Error ($\\sigma^2_{\\epsilon}$)')

    ax.set_xlabel('Model Complexity (Polynomial Degree)', fontsize=14)
    ax.set_ylabel('Error', fontsize=14)
    ax.set_title('The Bias-Variance Trade-off', fontsize=18)
    ax.set_ylim(0, 0.5)
    ax.set_xticks(degrees)
    ax.tick_params(axis='both', which='major', labelsize=12)

    best_degree = degrees[np.argmin(avg_expected_prediction_error)]
    ax.axvline(best_degree, color='k', ls=':', lw=2, label=f'Optimal Complexity (Degree={best_degree})')

    ax.legend(loc='upper center', fontsize=12)
    plt.tight_layout()

    # Save the figure
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Image saved to {output_path}")

def generate_lasso_ridge_geometry_image():
    """
    Generates and saves a plot illustrating the geometric intuition behind
    Lasso (L1) and Ridge (L2) regularization.
    """
    output_dir = "images/ml_intro"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "figure2_lasso_ridge_geometry.png")

    # Create a grid for plotting
    b1 = np.linspace(-1, 1, 400)
    b2 = np.linspace(-1, 1, 400)
    B1, B2 = np.meshgrid(b1, b2)

    # OLS loss function (elliptical contours)
    # Assume OLS solution is at (0.5, 0.5)
    ols_loss = (B1 - 0.5)**2 + (B2 - 0.5)**2

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7.5))
    plt.style.use('seaborn-v0_8-whitegrid')

    # --- Ridge Plot ---
    ax1.contour(B1, B2, ols_loss, levels=np.logspace(-1, 1, 10), cmap='viridis_r')
    ax1.plot(0.5, 0.5, 'ro', markersize=10, label='OLS Solution')

    # L2 constraint (circle)
    l2_constraint = B1**2 + B2**2
    ax1.contour(B1, B2, l2_constraint, levels=[0.25], colors='red', linewidths=3)

    ax1.set_title('Ridge ($L_2$) Regularization', fontsize=18)
    ax1.set_xlabel('$\\beta_1$', fontsize=14)
    ax1.set_ylabel('$\\beta_2$', fontsize=14)
    ax1.text(0.3, 0.3, 'Ridge\nSolution', ha='center',
             bbox=dict(facecolor='white', alpha=0.6), color='red', fontsize=12)
    ax1.plot([0.353], [0.353], 'r*', markersize=20) # Approx tangent point
    ax1.axhline(0, color='grey', lw=0.5)
    ax1.axvline(0, color='grey', lw=0.5)
    ax1.set_aspect('equal', adjustable='box')
    ax1.tick_params(axis='both', which='major', labelsize=12)


    # --- Lasso Plot ---
    ax2.contour(B1, B2, ols_loss, levels=np.logspace(-1, 1, 10), cmap='viridis_r')
    ax2.plot(0.5, 0.5, 'ro', markersize=10, label='OLS Solution')

    # L1 constraint (diamond)
    l1_constraint = np.abs(B1) + np.abs(B2)
    ax2.contour(B1, B2, l1_constraint, levels=[0.5], colors='blue', linewidths=3)

    ax2.set_title('Lasso ($L_1$) Regularization', fontsize=18)
    ax2.set_xlabel('$\\beta_1$', fontsize=14)
    ax2.set_ylabel('$\\beta_2$', fontsize=14)
    ax2.text(0.5, 0.1, 'Lasso\nSolution', ha='center',
             bbox=dict(facecolor='white', alpha=0.6), color='blue', fontsize=12)
    ax2.plot([0.5], [0], 'b*', markersize=20) # Tangent point
    ax2.axhline(0, color='grey', lw=0.5)
    ax2.axvline(0, color='grey', lw=0.5)
    ax2.set_aspect('equal', adjustable='box')
    ax2.tick_params(axis='both', which='major', labelsize=12)

    fig.suptitle('Geometric Intuition: Why Lasso Creates Sparsity', fontsize=22, y=1.02)
    plt.tight_layout(rect=[0, 0, 1, 0.98])

    # Save the figure
    plt.savefig(output_path, dpi=150)
    plt.close()
    print(f"Image saved to {output_path}")

if __name__ == "__main__":
    generate_bias_variance_tradeoff_image()
    generate_lasso_ridge_geometry_image()