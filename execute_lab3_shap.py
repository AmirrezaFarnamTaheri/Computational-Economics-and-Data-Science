# === Environment Setup ===
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import StandardScaler
import shap

# --- Configuration ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'font.size': 14, 'figure.figsize': (12, 7), 'figure.dpi': 150})
np.set_printoptions(suppress=True, linewidth=120, precision=4)

# --- Utility Functions ---
def sec(title): print(f"\\n{100*'='}\\n| {title.upper()} |\\n{100*'='}")

# --- Directories ---
IMG_DIR = 'images/07-Machine-Learning'
MODEL_DIR = 'models'
MODEL_PATH = f'{MODEL_DIR}/mlp_boston_housing.keras'

if not os.path.exists(MODEL_PATH):
    print(f"Error: Model file not found at {MODEL_PATH}. Please run execute_lab1_mlp.py first.")
else:
    # === Code Lab 3: Interpreting the MLP Regression Model with SHAP ===
    sec("Interpreting the MLP with SHAP using DeepExplainer")

    # 1. Load data
    (x_train, _), (x_test, _) = keras.datasets.boston_housing.load_data()
    feature_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']

    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    # 2. Load the pre-trained model
    model = keras.models.load_model(MODEL_PATH)
    print("Pre-trained MLP model loaded successfully.")

    # 3. Create a SHAP DeepExplainer
    explainer = shap.DeepExplainer(model, x_train_scaled[:100])

    # 4. Calculate SHAP values
    print("Calculating SHAP values with DeepExplainer...")
    shap_values = explainer.shap_values(x_test_scaled)
    print("SHAP value calculation complete.")

    # CORRECTIVE ACTION: Squeeze the extra dimension from the shap_values array
    # The model's single output creates a shape of (n_samples, n_features, 1),
    # but the plots expect (n_samples, n_features).
    if isinstance(shap_values, list) and len(shap_values) == 1:
        shap_values_squeezed = shap_values[0].squeeze()
    elif isinstance(shap_values, np.ndarray):
        shap_values_squeezed = shap_values.squeeze()
    else:
        shap_values_squeezed = shap_values # Fallback

    print(f"DEBUG: Shape of squeezed shap_values: {shap_values_squeezed.shape}")
    print(f"DEBUG: Shape of x_test_scaled: {x_test_scaled.shape}")

    # 5. Create and save the summary plot
    print("--- SHAP Summary Plot ---")
    shap.summary_plot(shap_values_squeezed, x_test_scaled, feature_names=feature_names, show=False)
    plt.savefig(f'{IMG_DIR}/shap_summary_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"SHAP summary plot saved to {IMG_DIR}/shap_summary_plot.png")

    # 6. Create and save the dependence plot
    print("--- SHAP Dependence Plot for 'LSTAT' ---")
    shap.dependence_plot("LSTAT", shap_values_squeezed, x_test_scaled, feature_names=feature_names, show=False)
    plt.savefig(f'{IMG_DIR}/shap_dependence_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"SHAP dependence plot saved to {IMG_DIR}/shap_dependence_plot.png")

print("\\nScript finished.")
