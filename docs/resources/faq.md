# Frequently Asked Questions

Find answers to common questions about the course.

---

## Getting Started

### Do I need prior programming experience?

No! Module 1 starts from the basics. If you've never programmed before, you'll learn everything you need. However, familiarity with computers and willingness to practice is essential.

### What mathematics background do I need?

**Minimum:**
- Calculus (single and multivariable)
- Linear algebra (matrices, vectors)
- Probability and statistics

**Recommended:**
- Real analysis
- Optimization theory
- Stochastic processes

The appendices provide mathematical reviews if you need a refresher.

### What economics background is required?

**Minimum:**
- Intermediate microeconomics
- Intermediate macroeconomics
- Basic econometrics

**Helpful but not required:**
- Graduate-level micro/macro
- Dynamic optimization
- Game theory

---

## Installation & Setup

### Which installation method should I use: conda or pip?

**Conda (recommended):**
- ✓ Better dependency management
- ✓ Handles non-Python packages
- ✓ Isolated environments
- ✓ Better for data science

**Pip:**
- ✓ Lighter weight
- ✓ More packages available
- ✓ Faster for small installs

For this course, **conda is strongly recommended** due to complex scientific packages.

### The installation is taking forever. Is this normal?

Yes! The full environment includes:
- 50+ Python packages
- 2-3 GB of downloads
- Complex dependency resolution

**Tips:**
- Use a fast, stable internet connection
- Consider `mamba` for faster installation: `conda install mamba -c conda-forge`
- Install in stages if needed

### I'm getting package conflicts. What should I do?

Try these steps:

1. **Update conda:**
   ```bash
   conda update conda
   ```

2. **Clear cache:**
   ```bash
   conda clean --all
   ```

3. **Create fresh environment:**
   ```bash
   conda env remove -n computational-econ
   conda env create -f environment.yml
   ```

4. **Use mamba (faster solver):**
   ```bash
   conda install mamba -c conda-forge
   mamba env create -f environment.yml
   ```

### Can I use Google Colab instead of installing locally?

Yes, but with limitations:

**Pros:**
- No local installation needed
- Free GPU access
- Works on any device

**Cons:**
- Session timeouts
- No persistent storage
- Limited memory
- Missing some packages

**Verdict:** Good for getting started, but local installation recommended for serious work.

---

## Using the Course

### In what order should I complete the modules?

**Recommended sequence:**
1. Module 1: Foundations (required for all others)
2. Module 2: Numerical Methods (required for most others)
3. Module 3: Economic Modeling (foundation for macro/micro)
4. Then choose based on interest:
   - Macro track: Modules 4 → 10
   - Micro track: Modules 5 → 10
   - Empirical track: Modules 6 → 7 → 8
   - Finance track: Modules 6 → 8 → 9

See the [Course Structure](../getting-started/structure.md) for details.

### How long does it take to complete the course?

**Full-time study (40 hrs/week):**
- Fast track: 12-16 weeks
- Comfortable pace: 20-24 weeks

**Part-time study (10-15 hrs/week):**
- 6-12 months

**Factors affecting speed:**
- Prior programming experience
- Mathematics background
- Time spent on exercises
- Depth of exploration

### Can I skip modules?

It depends:

**Can skip if you already know:**
- Python basics (but review Module 1 highlights)
- Specific topics you're not interested in

**Cannot skip:**
- Module 1 (unless strong Python background)
- Module 2 (needed for almost everything)
- Module 3 (needed for modules 4-5, 9-10)

### Are there solutions to the exercises?

Many notebooks include:
- Worked examples with full solutions
- Code cells with expected outputs
- Hints and tips

For open-ended exercises:
- Multiple valid approaches exist
- Focus on understanding concepts
- Compare your approach to course code

### Can I use this course for teaching?

**Yes!** The course is open-source and free to use.

**Licensing:**
- Code: MIT License (use freely)
- Content: CC BY 4.0 (attribution required)

Please:
- Provide attribution
- Share improvements back
- See [License](../about/license.md) for details

---

## Technical Issues

### Jupyter is not starting. What should I do?

1. **Verify installation:**
   ```bash
   conda activate computational-econ
   jupyter lab --version
   ```

2. **Try classic Jupyter:**
   ```bash
   jupyter notebook
   ```

3. **Check port conflicts:**
   ```bash
   jupyter lab --port=8889
   ```

4. **Reinstall Jupyter:**
   ```bash
   conda install -c conda-forge jupyterlab --force-reinstall
   ```

### A notebook is giving import errors. Help!

**Check these:**

1. **Correct kernel selected?**
   - Kernel → Change Kernel → computational-econ

2. **Environment activated?**
   ```bash
   conda activate computational-econ
   ```

3. **Package installed?**
   ```bash
   conda list | grep package-name
   ```

4. **Reinstall if needed:**
   ```bash
   conda install package-name
   ```

### My code is running very slowly. Is this normal?

**Common causes:**

1. **Not using vectorization**
   - ❌ Bad: `for` loops over arrays
   - ✓ Good: NumPy vectorized operations

2. **Large dataset in memory**
   - Use chunks for very large data
   - Consider Dask for out-of-core computation

3. **Inefficient algorithm**
   - Review Module 23: Performance Optimization
   - Use profiling to find bottlenecks

4. **No GPU for deep learning**
   - Consider Google Colab for free GPU
   - Or install CUDA locally

### I'm getting "Kernel died" errors

**Possible causes:**

1. **Out of memory**
   - Close other applications
   - Restart kernel
   - Use smaller datasets for practice

2. **Infinite loop**
   - Check for while loops without exit condition
   - Add iteration limits

3. **Segmentation fault**
   - Usually from C extensions
   - Restart kernel and try again

---

## Content Questions

### Why don't you cover topic X?

The course focuses on:
- Core computational methods
- Widely-used techniques
- Foundation for frontier research

**Topics not covered (and why):**
- Distributed systems → Out of scope
- Quantum computing → Too specialized
- Specific software (Stata, Matlab) → Python-focused
- Web development → Not core to economics

That said, contributions are welcome! See [Contributing](../about/contributing.md).

### The math is too hard. Where can I get help?

**Resources:**

1. **Course appendices** - Math reviews included
2. **Khan Academy** - Free calculus and linear algebra
3. **3Blue1Brown** - Excellent YouTube series on math
4. **MIT OpenCourseWare** - Free university courses

**Strategy:**
- Don't get stuck on math details
- Focus on intuition first
- Come back to proofs later
- Practice with code helps understanding

### The code is too hard. What should I do?

**Learning strategies:**

1. **Type code yourself** - Don't just read
2. **Run each cell** - See what happens
3. **Modify and experiment** - Change parameters
4. **Break down complex code** - One line at a time
5. **Use debugger** - Step through execution
6. **Add print statements** - See intermediate values

**Resources:**
- Module 17: Effective Debugging
- [Python Tutor](http://pythontutor.com/) - Visualize execution
- [Real Python](https://realpython.com/) - Tutorials

---

## GPU & Performance

### Do I need a GPU for this course?

**Not required, but helpful for:**
- Module 7: Machine Learning (deep learning sections)
- Large-scale simulations
- Training neural networks

**Alternatives if no GPU:**
- Google Colab (free GPU)
- Use smaller examples
- Pre-trained models
- CPU is fine for learning

### How do I enable GPU support?

**For NVIDIA GPUs:**

1. **Install CUDA Toolkit** (version 12.x)
2. **Install cuDNN**
3. **Install GPU packages:**
   ```bash
   pip install tensorflow[and-cuda]
   pip install torch --index-url https://download.pytorch.org/whl/cu121
   ```

4. **Verify:**
   ```python
   import tensorflow as tf
   print("GPUs:", tf.config.list_physical_devices('GPU'))
   ```

See [Installation Guide](../getting-started/installation.md) for details.

---

## Career & Applications

### Will this course prepare me for a job in data science?

**Yes, with caveats:**

**Strengths:**
- Strong programming foundation
- Statistical/econometric methods
- Machine learning skills
- Real-world applications

**Also needed (not covered as much):**
- Software engineering
- Databases and SQL
- Cloud computing
- Communication skills

**Verdict:** Excellent foundation; supplement with applied projects and internships.

### Can I use this for my research?

**Absolutely!** The course covers:
- Modern econometric methods
- Computational modeling
- Data analysis techniques
- Machine learning for economics

Many notebooks can be adapted for research projects.

### What jobs can this prepare me for?

**Roles:**
- Economic researcher
- Data scientist (economics/finance)
- Quantitative analyst
- Policy analyst
- Computational economist
- Economic consultant
- Central bank researcher
- Academic economist

**Skills employers value:**
- Python programming
- Statistical analysis
- Economic modeling
- Machine learning
- Data visualization

---

## Contributing

### I found an error. How do I report it?

**GitHub Issues:**
1. Go to [GitHub repository](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/issues)
2. Click "New Issue"
3. Provide:
   - Notebook name and cell number
   - Description of error
   - Expected vs actual behavior
   - Your setup (OS, Python version)

### Can I contribute improvements?

**Yes! Contributions welcome:**

1. **Fork repository**
2. **Make improvements**
3. **Submit pull request**

See [Contributing Guide](../about/contributing.md).

**Good contributions:**
- Bug fixes
- Clarifications
- Additional examples
- New exercises
- Better visualizations

---

## Still Have Questions?

- :material-github: [GitHub Discussions](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/discussions)
- :material-github: [GitHub Issues](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/issues)
- :material-email: Email: [Contact](../about/contact.md)
