# This script combines all code labs from the notebook for validation.

# === Environment Setup (from Cell 1) ===
import os, sys, math, time, random, json, textwrap, warnings
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import graphviz
try:
    import tensorflow as tf
    from tensorflow import keras
    from tensorflow.keras import layers
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    import shap
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

# --- Configuration ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'font.size': 14, 'figure.figsize': (12, 7), 'figure.dpi': 150})
np.set_printoptions(suppress=True, linewidth=120, precision=4)

# --- Utility Functions ---
def sec(title): print(f"\\n{100*'='}\\n| {title.upper()} |\\n{100*'='}")

# Create image directory if it doesn't exist
IMG_DIR = 'images/07-Machine-Learning'
if not os.path.exists(IMG_DIR):
    os.makedirs(IMG_DIR)

if not TENSORFLOW_AVAILABLE:
    print("TensorFlow/Keras or SHAP is not installed. Skipping code labs.")
else:
    # === Code Lab 1: Regression with an MLP (from Cell 21) ===
    sec("Predicting House Prices with a Regularized MLP")

    # 1. Load and preprocess data
    (x_train, y_train), (x_test, y_test) = keras.datasets.boston_housing.load_data()
    feature_names = ['CRIM', 'ZN', 'INDUS', 'CHAS', 'NOX', 'RM', 'AGE', 'DIS', 'RAD', 'TAX', 'PTRATIO', 'B', 'LSTAT']
    scaler = StandardScaler()
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    # 2. Define the model architecture
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=[x_train.shape[1]]),
        layers.Dropout(0.2),
        layers.Dense(64, activation='relu'),
        layers.Dropout(0.2),
        layers.Dense(1)
    ])

    # 3. Compile and train
    model.compile(optimizer='adam', loss='mean_squared_error')
    model.fit(x_train_scaled, y_train, epochs=150, validation_split=0.2, verbose=0)
    print("MLP Model training complete.")

    # 4. Evaluate
    loss = model.evaluate(x_test_scaled, y_test, verbose=0)
    print(f"--- Model Performance on Test Set ---\nMean Squared Error: {loss:.2f}\n")

    # === Code Lab 2: Image Classification with a CNN (from Cell 24) ===
    sec("Image Classification with a CNN")

    # 1. Load and preprocess image data
    (x_train_img, y_train_img), (x_test_img, y_test_img) = keras.datasets.mnist.load_data()
    x_train_img = x_train_img.astype("float32") / 255.0
    x_test_img = x_test_img.astype("float32") / 255.0
    x_train_img = np.expand_dims(x_train_img, -1)
    x_test_img = np.expand_dims(x_test_img, -1)

    # 2. Define the CNN architecture
    cnn_model = keras.Sequential([
        keras.Input(shape=(28, 28, 1)),
        layers.Conv2D(32, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
        layers.MaxPooling2D(pool_size=(2, 2)),
        layers.Flatten(),
        layers.Dropout(0.5),
        layers.Dense(10, activation="softmax")
    ])

    # 3. Compile and train
    cnn_model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
    cnn_model.fit(x_train_img, y_train_img, batch_size=128, epochs=5, validation_split=0.1, verbose=1)
    print("CNN model training complete.")

    # 4. Evaluate
    score = cnn_model.evaluate(x_test_img, y_test_img, verbose=0)
    print(f"--- CNN Performance on Test Set ---\nTest loss: {score[0]:.4f}\nTest accuracy: {score[1]:.4f}\n")

    # === Code Lab 3: Interpreting the MLP Regression Model with SHAP (from Cell 35) ===
    sec("Interpreting the MLP with SHAP")

    # 1. Create a SHAP explainer object
    explainer = shap.KernelExplainer(model.predict, x_train_scaled[:100])

    # 2. Calculate SHAP values
    shap_values = explainer.shap_values(x_test_scaled)
    print("SHAP value calculation complete.")

    # 3. Create and save the summary plot
    print("--- SHAP Summary Plot ---")
    shap.summary_plot(shap_values, x_test_scaled, feature_names=feature_names, show=False)
    plt.savefig(f'{IMG_DIR}/shap_summary_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"SHAP summary plot saved to {IMG_DIR}/shap_summary_plot.png")

    # 4. Create and save the dependence plot
    print("--- SHAP Dependence Plot for 'LSTAT' ---")
    shap.dependence_plot("LSTAT", shap_values[0], x_test, feature_names=feature_names, show=False)
    plt.savefig(f'{IMG_DIR}/shap_dependence_plot.png', dpi=300, bbox_inches='tight')
    plt.close()
    print(f"SHAP dependence plot saved to {IMG_DIR}/shap_dependence_plot.png")

print("\\nScript finished.")
