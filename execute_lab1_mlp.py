# === Environment Setup ===
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import StandardScaler

# --- Configuration ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'font.size': 14, 'figure.figsize': (12, 7), 'figure.dpi': 150})
np.set_printoptions(suppress=True, linewidth=120, precision=4)

# --- Utility Functions ---
def sec(title): print(f"\\n{100*'='}\\n| {title.upper()} |\\n{100*'='}")

# === Code Lab 1: Regression with an MLP (Functional API) ===
sec("Training and Saving the MLP Model (Functional API)")

# 1. Load and preprocess data
(x_train, y_train), (x_test, y_test) = keras.datasets.boston_housing.load_data()
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

# 2. Define the model architecture using the Keras Functional API
inputs = keras.Input(shape=(x_train.shape[1],), name="input_layer")
x = layers.Dense(64, activation='relu')(inputs)
x = layers.Dropout(0.2)(x)
x = layers.Dense(64, activation='relu')(x)
x = layers.Dropout(0.2)(x)
outputs = layers.Dense(1)(x)
model = keras.Model(inputs=inputs, outputs=outputs, name="boston_housing_model")

model.summary() # Print model summary to verify structure

# 3. Compile and train
model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(x_train_scaled, y_train, epochs=150, validation_split=0.2, verbose=1)
print("MLP Model training complete.")

# 4. Evaluate
loss = model.evaluate(x_test_scaled, y_test, verbose=0)
print(f"--- Model Performance on Test Set ---\nMean Squared Error: {loss:.2f}\n")

# 5. Save the trained model
MODEL_DIR = 'models'
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)
model.save(f'{MODEL_DIR}/mlp_boston_housing.keras')
print(f"Model saved to {MODEL_DIR}/mlp_boston_housing.keras")

print("\\nScript finished.")
