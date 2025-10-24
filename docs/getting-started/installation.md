# Installation Guide

This guide will help you set up the complete environment for the Computational Economics and Data Science course.

---

## System Requirements

!!! info "Minimum Requirements"
    - **OS**: Windows 10+, macOS 10.14+, or Linux
    - **RAM**: 8 GB minimum, 16 GB recommended
    - **Storage**: 5 GB free space
    - **Python**: 3.10 or higher

!!! tip "Recommended Setup"
    - 16+ GB RAM for machine learning modules
    - SSD for faster data processing
    - GPU (NVIDIA) for deep learning acceleration (optional)

---

## Installation Methods

Choose the method that works best for you:

=== "Conda (Recommended)"

    ### Using Conda

    [Conda](https://docs.conda.io/) is the recommended package manager for data science projects.

    #### 1. Install Miniconda or Anaconda

    **Option A: Miniconda** (lightweight, recommended)
    ```bash
    # Download and install from:
    # https://docs.conda.io/en/latest/miniconda.html
    ```

    **Option B: Anaconda** (includes GUI and extra packages)
    ```bash
    # Download and install from:
    # https://www.anaconda.com/download
    ```

    #### 2. Clone the Repository
    ```bash
    git clone https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science.git
    cd Computational-Economics-and-Data-Science
    ```

    #### 3. Create the Environment
    ```bash
    conda env create -f environment.yml
    ```

    #### 4. Activate the Environment
    ```bash
    conda activate computational-econ
    ```

    #### 5. Verify Installation
    ```bash
    python --version  # Should be 3.10+
    jupyter lab --version
    ```

=== "pip (Alternative)"

    ### Using pip

    If you prefer using pip, follow these steps:

    #### 1. Ensure Python 3.10+ is Installed
    ```bash
    python --version  # Should output 3.10.0 or higher
    ```

    #### 2. Clone the Repository
    ```bash
    git clone https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science.git
    cd Computational-Economics-and-Data-Science
    ```

    #### 3. Create Virtual Environment (Optional but Recommended)
    ```bash
    python -m venv venv

    # Activate on macOS/Linux:
    source venv/bin/activate

    # Activate on Windows:
    venv\Scripts\activate
    ```

    #### 4. Install Dependencies
    ```bash
    pip install -r requirements.txt
    ```

    !!! warning "Large Installation"
        This will download about 2-3 GB of packages. Ensure you have a stable internet connection.

---

## Package Overview

The course requires the following major packages:

### Core Scientific Computing
- **NumPy** ≥ 2.0 - Numerical arrays and linear algebra
- **SciPy** ≥ 1.11 - Scientific computing
- **Pandas** ≥ 2.0 - Data manipulation
- **Matplotlib** ≥ 3.8 - Data visualization
- **Seaborn** ≥ 0.13 - Statistical visualization

### Machine Learning
- **scikit-learn** ≥ 1.4 - Classical ML algorithms
- **TensorFlow** ≥ 2.15 - Deep learning
- **PyTorch** ≥ 2.1 - Deep learning (alternative)
- **XGBoost** ≥ 2.0 - Gradient boosting

### Econometrics
- **statsmodels** ≥ 0.14 - Statistical models
- **quantecon** ≥ 0.7 - Quantitative economics
- **arch** ≥ 6.0 - ARCH/GARCH models
- **pymc** ≥ 5.10 - Bayesian inference

### Interactive Computing
- **JupyterLab** ≥ 4.0 - Interactive notebooks
- **IPython** ≥ 8.20 - Enhanced Python shell

---

## Verifying Your Installation

Run this Python script to verify all packages are installed correctly:

```python
import sys
print(f"Python version: {sys.version}")

# Test core packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy

print(f"✓ NumPy {np.__version__}")
print(f"✓ Pandas {pd.__version__}")
print(f"✓ Matplotlib {matplotlib.__version__}")
print(f"✓ SciPy {scipy.__version__}")

# Test ML packages
try:
    import sklearn
    print(f"✓ scikit-learn {sklearn.__version__}")
except ImportError:
    print("✗ scikit-learn not installed")

try:
    import tensorflow as tf
    print(f"✓ TensorFlow {tf.__version__}")
except ImportError:
    print("⚠ TensorFlow not installed (optional)")

try:
    import torch
    print(f"✓ PyTorch {torch.__version__}")
except ImportError:
    print("⚠ PyTorch not installed (optional)")

# Test econometrics packages
try:
    import statsmodels.api as sm
    print(f"✓ statsmodels {sm.__version__}")
except ImportError:
    print("✗ statsmodels not installed")

try:
    import quantecon as qe
    print(f"✓ QuantEcon {qe.__version__}")
except ImportError:
    print("✗ QuantEcon not installed")

print("\n✓ All core packages installed successfully!")
```

---

## Launching Jupyter Lab

After installation, start Jupyter Lab:

```bash
# Make sure you're in the course directory and environment is activated
jupyter lab
```

This will open Jupyter Lab in your default web browser at `http://localhost:8888`.

---

## Optional: GPU Support

For deep learning with GPU acceleration:

### NVIDIA GPU (CUDA)

1. **Check GPU compatibility**: NVIDIA GPU with CUDA Compute Capability 3.5+

2. **Install CUDA Toolkit** (version 12.x):
    ```bash
    # Download from: https://developer.nvidia.com/cuda-downloads
    ```

3. **Install cuDNN**:
    ```bash
    # Download from: https://developer.nvidia.com/cudnn
    ```

4. **Install GPU-enabled packages**:
    === "TensorFlow"
        ```bash
        pip install tensorflow[and-cuda]
        ```

    === "PyTorch"
        ```bash
        # Visit https://pytorch.org/get-started/locally/
        # for platform-specific instructions
        ```

    === "CuPy"
        ```bash
        pip install cupy-cuda12x
        ```

5. **Verify GPU is detected**:
    ```python
    # TensorFlow
    import tensorflow as tf
    print("GPUs:", tf.config.list_physical_devices('GPU'))

    # PyTorch
    import torch
    print("CUDA available:", torch.cuda.is_available())
    print("GPU count:", torch.cuda.device_count())
    ```

---

## Troubleshooting

### Common Issues

!!! question "Package conflicts or installation errors?"
    ```bash
    # Clear conda cache
    conda clean --all

    # Try creating environment again
    conda env remove -n computational-econ
    conda env create -f environment.yml
    ```

!!! question "Jupyter kernel not found?"
    ```bash
    # Install IPython kernel
    python -m ipykernel install --user --name computational-econ
    ```

!!! question "Import errors in Jupyter notebooks?"
    Make sure you've selected the correct kernel:
    - Click "Kernel" → "Change Kernel" → "computational-econ"

!!! question "Out of memory errors?"
    - Close other applications
    - Restart Jupyter kernel
    - Consider using a machine with more RAM

### Getting Help

If you encounter issues:

1. Check the [FAQ](../resources/faq.md)
2. Search [GitHub Issues](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/issues)
3. Create a new issue with:
    - Your OS and Python version
    - Full error message
    - Steps to reproduce

---

## Next Steps

Once installation is complete:

1. [:material-rocket-launch: Complete the Quick Start tutorial](quickstart.md)
2. [:material-book-open-variant: Review the Course Structure](structure.md)
3. [:material-school: Begin Module 1: Foundations](../modules/01-foundations/index.md)

---

!!! success "Installation Complete!"
    Congratulations! You're now ready to begin the course. Head to the [Quick Start guide](quickstart.md) to run your first notebook.
