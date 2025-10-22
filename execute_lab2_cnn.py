# === Environment Setup ===
import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# --- Utility Functions ---
def sec(title): print(f"\\n{100*'='}\\n| {title.upper()} |\\n{100*'='}")

# === Code Lab 2: Image Classification with a CNN ===
sec("Image Classification with a CNN")

# 1. Load and preprocess image data
(x_train_img, y_train_img), (x_test_img, y_test_img) = keras.datasets.mnist.load_data()
# Normalize pixel values to [0, 1] and add a channel dimension
x_train_img = x_train_img.astype("float32") / 255.0
x_test_img = x_test_img.astype("float32") / 255.0
x_train_img = np.expand_dims(x_train_img, -1)
x_test_img = np.expand_dims(x_test_img, -1)

# 2. Define the CNN architecture
cnn_model = keras.Sequential([
    keras.Input(shape=(28, 28, 1)),
    layers.Conv2D(32, kernel_size=(3, 3), activation="relu"), # 32 filters, 3x3 kernel
    layers.MaxPooling2D(pool_size=(2, 2)), # Downsample by taking max value in 2x2 patch
    layers.Conv2D(64, kernel_size=(3, 3), activation="relu"),
    layers.MaxPooling2D(pool_size=(2, 2)),
    layers.Flatten(), # Flatten the 2D feature map to a 1D vector
    layers.Dropout(0.5),
    layers.Dense(10, activation="softmax") # Output layer for 10-class classification
])

# 3. Compile and train
cnn_model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
cnn_model.fit(x_train_img, y_train_img, batch_size=128, epochs=5, validation_split=0.1, verbose=1)
print("CNN model training complete.")

# 4. Evaluate
score = cnn_model.evaluate(x_test_img, y_test_img, verbose=0)
print(f"--- CNN Performance on Test Set ---\nTest loss: {score[0]:.4f}\nTest accuracy: {score[1]:.4f}\n")

print("\\nScript finished.")
