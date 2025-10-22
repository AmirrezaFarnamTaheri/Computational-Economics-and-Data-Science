# === Environment Setup ===
import os, sys, math, time, random, json, textwrap, warnings
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import graphviz
try:
    print("Attempting to import TensorFlow...")
    import tensorflow as tf
    print("TensorFlow imported successfully.")
    from tensorflow import keras
    from tensorflow.keras import layers
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    print("Attempting to import SHAP...")
    import shap
    print("SHAP imported successfully.")
    TENSORFLOW_AVAILABLE = True
except ImportError as e:
    print(f"ImportError: {e}")
    TENSORFLOW_AVAILABLE = False
# from IPython.display import display, Markdown # This will fail in a script

# --- Configuration ---\n",
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'font.size': 14, 'figure.figsize': (12, 7), 'figure.dpi': 150})
np.set_printoptions(suppress=True, linewidth=120, precision=4)

# --- Utility Functions ---\n",
# def note(msg, **kwargs): display(Markdown(f\"<div class='alert alert-block alert-info'>📝 **Note:** {msg}</div>\"))
def sec(title): print(f"\\n{100*'='}\\n| {title.upper()} |\\n{100*'='}")

if not TENSORFLOW_AVAILABLE:
    # note(\"TensorFlow/Keras or SHAP is not installed. Skipping code labs. Run `pip install tensorflow shap`.\")
    print("TensorFlow/Keras or SHAP is not installed.")

# note(f\"Environment initialized. TensorFlow/SHAP available: {TENSORFLOW_AVAILABLE}\")"
print(f"Environment initialized. TensorFlow/SHAP available: {TENSORFLOW_AVAILABLE}")
