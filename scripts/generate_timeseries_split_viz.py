import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import TimeSeriesSplit

def plot_time_series_split():
    """
    Generates and saves a visualization of the TimeSeriesSplit cross-validator.
    """
    X = np.arange(20)
    n_splits = 4
    tscv = TimeSeriesSplit(n_splits=n_splits)

    fig, ax = plt.subplots(figsize=(10, 6))

    # Plot the splits
    for i, (train_index, test_index) in enumerate(tscv.split(X)):
        # Plot training data
        ax.fill_betweenx([i, i+0.8], train_index[0], train_index[-1], color='lightblue', label='Training Set' if i == 0 else "")
        ax.scatter(train_index, np.full_like(train_index, i + 0.4), marker='_', s=50, color='blue')

        # Plot testing data
        ax.fill_betweenx([i, i+0.8], test_index[0], test_index[-1], color='lightcoral', alpha=0.8, label='Test Set' if i == 0 else "")
        ax.scatter(test_index, np.full_like(test_index, i + 0.4), marker='_', s=50, color='red')

    ax.set_yticks(np.arange(n_splits))
    ax.set_yticklabels([f'Fold {i+1}' for i in range(n_splits)])
    ax.set_xlabel('Data Index')
    ax.set_ylabel('CV Iteration')
    ax.set_title('Expanding Window Cross-Validation (TimeSeriesSplit)')
    ax.legend(loc='upper left')
    ax.set_ylim(-0.5, n_splits)
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)

    plt.tight_layout()

    # --- Save Figure ---
    import os
    if not os.path.exists('images'):
        os.makedirs('images')

    save_path = 'images/png/timeseries_split_visualization.png'
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Plot saved to {save_path}")

if __name__ == '__main__':
    plot_time_series_split()