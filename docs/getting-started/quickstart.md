# Quick Start

Get up and running in 10 minutes and run your first economic analysis!

---

## Prerequisites

Before starting, make sure you have:

- [x] Completed the [Installation](installation.md)
- [x] Activated the conda environment
- [x] Basic familiarity with Jupyter notebooks (optional)

---

## Step 1: Launch Jupyter Lab

Open a terminal and navigate to the course directory:

```bash
# Navigate to course folder
cd Computational-Economics-and-Data-Science

# Activate environment
conda activate computational-econ

# Start Jupyter Lab
jupyter lab
```

Your browser will open at `http://localhost:8888` showing the Jupyter Lab interface.

!!! tip "First Time Using Jupyter?"
    Jupyter Lab is an interactive development environment. The left sidebar shows your files, and you can create/open notebooks in the main area.

---

## Step 2: Open Your First Notebook

1. In the left sidebar, navigate to `01-Foundations/`
2. Double-click `01_Introduction.ipynb`

The notebook will open in a new tab.

---

## Step 3: Run Your First Cells

### Understanding Notebooks

Jupyter notebooks consist of **cells** that can contain:
- **Code** (Python code to execute)
- **Markdown** (formatted text, like this guide)

### Running Cells

Click on the first code cell and:

=== "Keyboard Shortcut"
    Press `Shift + Enter` to run the cell

=== "Mouse"
    Click the ▶️ button in the toolbar

The cell will execute and show output below.

### Try This: Simple Calculation

Find a cell with Python code like this:

```python
# Simple calculation
2 + 2
```

Run it with `Shift + Enter`. You should see:

```
4
```

Congratulations! You've run your first Python code! 🎉

---

## Step 4: Your First Economic Analysis

Let's do something more interesting. Navigate to:

`01-Foundations/15_Accessing_Economic_Data_via_APIs.ipynb`

### Example: Downloading US GDP Data

Find and run these cells:

```python
# Import libraries
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt

# Download real GDP data from FRED
gdp = pdr.get_data_fred('GDPC1', start='2000')

# Plot
plt.figure(figsize=(12, 6))
plt.plot(gdp.index, gdp.values)
plt.title('US Real GDP (Billions of Chained 2012 Dollars)', fontsize=14)
plt.xlabel('Year')
plt.ylabel('GDP')
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
```

You should see a plot of US GDP over time! 📈

### What Just Happened?

You:
1. Imported Python libraries for data analysis
2. Downloaded real economic data from FRED (Federal Reserve)
3. Created a publication-quality plot

This is the power of computational economics!

---

## Step 5: Explore the Course Structure

### Module Organization

The course is organized in numbered folders:

```
01-Foundations/          ← Start here
02-Numerical-Methods/
03-Economic-Modeling/
04-Macro-Models/
... and more!
```

### Within Each Module

Each module contains:

- **Numbered notebooks** (e.g., `01_Topic.ipynb`, `02_Topic.ipynb`)
- **Supporting Python files** (utility functions)
- **README** (if present)

!!! tip "Recommended Path"
    Work through notebooks in numerical order within each module.

---

## Step 6: Your First Challenge

Ready for a small challenge? Try this:

### Challenge: Unemployment Rate Analysis

1. Open a new notebook: **File → New → Notebook**
2. Select the **Python 3 (ipykernel)** kernel
3. Copy and modify the GDP code to download unemployment data
4. The FRED series code for unemployment is: `'UNRATE'`

??? hint "Need Help?"
    ```python
    import pandas as pd
    from pandas_datareader import data as pdr
    import matplotlib.pyplot as plt

    # Download unemployment rate
    unemployment = pdr.get_data_fred('UNRATE', start='2000')

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(unemployment.index, unemployment.values)
    plt.title('US Unemployment Rate (%)', fontsize=14)
    plt.xlabel('Year')
    plt.ylabel('Unemployment Rate (%)')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
    ```

??? success "Solution"
    Run the code above! You should see the unemployment rate over time, clearly showing recessions (2008-2009, 2020).

---

## Essential Jupyter Skills

### Keyboard Shortcuts

Master these shortcuts to work faster:

| Shortcut | Action |
|----------|--------|
| `Shift + Enter` | Run cell and move to next |
| `Ctrl + Enter` | Run cell and stay |
| `A` | Insert cell above |
| `B` | Insert cell below |
| `D D` (press twice) | Delete cell |
| `M` | Convert to Markdown |
| `Y` | Convert to Code |
| `Ctrl + S` | Save notebook |

### Cell Types

- **Code cells**: Python code (blue left border)
- **Markdown cells**: Text and formatting (no left border)

### Running Multiple Cells

- **Run All**: Cell → Run All Cells
- **Run Above**: Cell → Run All Above
- **Restart Kernel**: Kernel → Restart Kernel

!!! warning "Kernel Restart"
    Restarting the kernel clears all variables. You'll need to run cells again from the top.

---

## Next Steps

Now that you're set up, here's what to do next:

### 1. Complete Module 1: Foundations

Work through the notebooks in order:

- [ ] 01_Introduction.ipynb
- [ ] 02_Professional_Development_Environment.ipynb
- [ ] 03_Python_Fundamentals_Data_Types.ipynb
- [ ] ... continue through all 24 notebooks

### 2. Practice, Practice, Practice

For each notebook:

1. **Read** the explanations
2. **Run** all code cells
3. **Modify** code and experiment
4. **Complete** exercises (if present)
5. **Take notes** in markdown cells

### 3. Build Something

After Module 1, try a mini-project:

- Download and analyze economic data
- Create visualizations
- Replicate a simple economic model
- Share your work on GitHub

---

## Common Issues

### Kernel is Busy

**Symptom:** Cell has `[*]` and won't finish

**Solutions:**
- Wait (might be running complex code)
- Interrupt: Kernel → Interrupt Kernel
- Restart: Kernel → Restart Kernel

### Import Error

**Symptom:** `ModuleNotFoundError: No module named 'package'`

**Solutions:**
1. Check environment is activated: `conda list`
2. Install missing package: `conda install package-name`
3. Restart Jupyter after installing

### Can't Save Notebook

**Symptom:** Save icon greyed out or error message

**Solutions:**
- Check file permissions
- Save a copy: File → Save Notebook As
- Close and reopen Jupyter

---

## Learning Resources

### While You Learn

Keep these open in browser tabs:

- [Official Python Docs](https://docs.python.org/3/)
- [NumPy Documentation](https://numpy.org/doc/)
- [Pandas Documentation](https://pandas.pydata.org/docs/)
- [Stack Overflow](https://stackoverflow.com/) (for questions)

### If You Get Stuck

1. **Read error messages carefully** - They're helpful!
2. **Google the error** - Someone has likely solved it
3. **Check the FAQ** - [Course FAQ](../resources/faq.md)
4. **Ask for help** - [GitHub Discussions](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/discussions)

---

## Tips for Success

### 1. Type Code Yourself

❌ **Don't**: Copy-paste code
✅ **Do**: Type it out manually

**Why:** You learn by doing. Typing helps you remember syntax and catch mistakes.

### 2. Experiment Freely

- Change parameters
- Try different data
- Break things (in a copy!)
- See what happens

### 3. Use Version Control

Save your progress with Git:

```bash
# Make changes to notebooks
git add .
git commit -m "Completed Module 1.3"
git push
```

### 4. Take Breaks

- Complex material takes time
- Don't rush
- Sleep on difficult concepts
- Come back refreshed

### 5. Join the Community

- Share your progress
- Ask questions
- Help others
- Build your network

---

## You're Ready! 🚀

You now know how to:

- ✅ Launch Jupyter Lab
- ✅ Run notebook cells
- ✅ Download economic data
- ✅ Create visualizations
- ✅ Navigate the course

Time to dive deep into computational economics!

[:material-school: Start Module 1](../modules/01-foundations/index.md){ .md-button .md-button--primary }
[:material-help: Get Help](../resources/faq.md){ .md-button }

---

!!! quote "Remember"
    "The best way to learn programming is to program. Don't just read – code!"
