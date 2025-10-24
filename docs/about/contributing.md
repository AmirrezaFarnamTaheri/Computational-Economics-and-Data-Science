# Contributing

Thank you for your interest in contributing to Computational Economics and Data Science! This guide will help you get started.

---

## Ways to Contribute

You don't need to be an expert to contribute! Here are many ways to help:

### 🐛 Report Bugs

Found an error? Help us fix it!

- Check if it's already reported in [GitHub Issues](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/issues)
- If not, [open a new issue](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/issues/new)
- Include: notebook name, cell number, error message, your setup

### 📝 Improve Documentation

- Fix typos and grammar
- Clarify confusing explanations
- Add missing docstrings
- Improve code comments

### 💡 Suggest Enhancements

- New topics or modules
- Additional examples
- Better visualizations
- Improved exercises

### 🔧 Fix Issues

- Browse [open issues](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/issues)
- Look for issues labeled `good first issue` or `help wanted`
- Comment on an issue you'd like to work on

### ✨ Add Features

- New notebook content
- Additional datasets
- Utility functions
- Interactive visualizations

---

## Getting Started

### 1. Fork the Repository

Click the "Fork" button on [GitHub](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science).

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR-USERNAME/Computational-Economics-and-Data-Science.git
cd Computational-Economics-and-Data-Science
```

### 3. Set Up Development Environment

```bash
# Create conda environment
conda env create -f environment.yml
conda activate computational-econ

# Add upstream remote
git remote add upstream https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science.git
```

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

**Branch naming:**
- `feature/` for new features
- `fix/` for bug fixes
- `docs/` for documentation
- `refactor/` for code refactoring

---

## Making Changes

### Code Style

Follow the project's [Code Style Guide](../resources/code-style.md):

**Python:**
- PEP 8 style
- NumPy-style docstrings
- Type hints where appropriate
- Meaningful variable names

**Notebooks:**
- Clear markdown explanations
- One concept per cell
- Output visible (run all cells)
- Kernel restarted before committing

**Example:**

```python
def calculate_present_value(future_value: float, rate: float, periods: int) -> float:
    """
    Calculate present value using the discount formula.

    Parameters
    ----------
    future_value : float
        Future cash flow value
    rate : float
        Discount rate (annual)
    periods : int
        Number of periods

    Returns
    -------
    float
        Present value

    Examples
    --------
    >>> calculate_present_value(110, 0.10, 1)
    100.0
    ```

### Testing

Run existing tests before submitting:

```bash
# Run Python tests
pytest

# Validate notebooks
python scripts/validate_notebooks.py

# Check code style
flake8 scripts/
```

### Commit Messages

Write clear, descriptive commit messages:

**Good:**
```
Fix: Correct discount factor formula in Module 3

The formula in cell 15 was using addition instead of multiplication.
Also updated the docstring to clarify the discount_factor parameter.

Fixes #123
```

**Bad:**
```
fixed stuff
```

**Format:**
```
<type>: <short summary>

<detailed description>

<issue reference>
```

**Types:**
- `Fix:` Bug fixes
- `Feat:` New features
- `Docs:` Documentation changes
- `Style:` Code style improvements
- `Refactor:` Code refactoring
- `Test:` Test additions/changes
- `Chore:` Maintenance tasks

---

## Submitting Changes

### 1. Push to Your Fork

```bash
git add .
git commit -m "Fix: your change description"
git push origin feature/your-feature-name
```

### 2. Create Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your branch
4. Fill out the template:
   - **Description:** What does this PR do?
   - **Motivation:** Why is this change needed?
   - **Testing:** How did you test it?
   - **Screenshots:** If applicable

### 3. Wait for Review

- Maintainers will review your PR
- Address any requested changes
- Once approved, it will be merged!

---

## Contribution Guidelines

### What We're Looking For

✅ **We love:**
- Bug fixes
- Improved explanations
- Additional examples
- Better visualizations
- Test additions
- Documentation improvements

⚠️ **Please discuss first:**
- Major new features
- New modules or topics
- Significant restructuring
- Breaking changes

❌ **Please don't:**
- Add unnecessary dependencies
- Change code style without discussion
- Submit AI-generated content without review
- Remove working features without reason

### Quality Standards

All contributions should:

- **Work correctly** - Test your changes
- **Follow style guide** - Consistent with existing code
- **Include documentation** - Explain what and why
- **Be self-contained** - Don't break other features
- **Add value** - Improve the course meaningfully

---

## Types of Contributions

### Documentation Improvements

**Examples:**
- Fix typos
- Clarify confusing sections
- Add missing explanations
- Improve formatting

**How to contribute:**
1. Edit markdown or notebook cells
2. Ensure clarity and correctness
3. Preview changes locally
4. Submit PR

### Code Improvements

**Examples:**
- Fix bugs
- Optimize performance
- Add error handling
- Improve readability

**How to contribute:**
1. Identify issue
2. Write fix
3. Test thoroughly
4. Add tests if applicable
5. Submit PR

### New Content

**Examples:**
- Additional exercises
- New examples
- Extended explanations
- New datasets

**How to contribute:**
1. Discuss in issue first
2. Follow existing structure
3. Ensure high quality
4. Include documentation
5. Submit PR

### Translations

**Interested in translating?**

1. Open an issue to discuss
2. Follow translation guidelines
3. Maintain technical accuracy
4. Keep formatting consistent

---

## Development Workflow

### Daily Development

```bash
# Start of day: Get latest changes
git checkout main
git pull upstream main

# Create feature branch
git checkout -b feature/my-feature

# Make changes...
# ... edit files ...

# Test changes
pytest
python scripts/validate_notebooks.py

# Commit
git add .
git commit -m "Feat: add new feature"

# Push to your fork
git push origin feature/my-feature
```

### Before Submitting PR

```bash
# Update from upstream
git fetch upstream
git rebase upstream/main

# Run all checks
pytest
flake8
python scripts/validate_notebooks.py

# Push
git push origin feature/my-feature --force-with-lease
```

---

## Code Review Process

### What Reviewers Look For

1. **Correctness** - Does it work?
2. **Quality** - Is it well-written?
3. **Style** - Does it match project standards?
4. **Documentation** - Is it explained?
5. **Tests** - Is it tested?
6. **Impact** - Does it improve the course?

### Addressing Feedback

- Be open to suggestions
- Ask questions if unclear
- Make requested changes promptly
- Don't take it personally - we're all learning!

### Approval Process

1. **Automated checks** must pass
2. **At least one review** from maintainer
3. **All discussions** resolved
4. **Squash and merge** to main branch

---

## Community Guidelines

### Be Respectful

- Use welcoming and inclusive language
- Respect differing viewpoints
- Accept constructive criticism gracefully
- Focus on what's best for the community

### Be Professional

- Provide constructive feedback
- Help newcomers
- Give credit where due
- Follow code of conduct

### Be Patient

- Reviewers are volunteers
- Response may take a few days
- Be understanding of timelines
- Follow up politely if needed

---

## Recognition

### Contributors

All contributors are recognized in:
- GitHub contributors page
- Release notes
- Project documentation

### Major Contributors

Significant contributors may be:
- Listed in README
- Invited as collaborators
- Consulted on major decisions

---

## Getting Help

### Questions About Contributing?

- **General questions:** [GitHub Discussions](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/discussions)
- **Specific issues:** Comment on the issue
- **Private concerns:** [Contact us](contact.md)

### Resources

- [Code Style Guide](../resources/code-style.md)
- [GitHub Flow Guide](https://guides.github.com/introduction/flow/)
- [How to Write Good Commit Messages](https://chris.beams.io/posts/git-commit/)

---

## Thank You!

Every contribution, no matter how small, makes this course better for everyone. Thank you for being part of our community!

---

[:material-github: View on GitHub](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science){ .md-button .md-button--primary }
[:material-bug: Report Issue](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/issues){ .md-button }
[:material-chat: Join Discussion](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/discussions){ .md-button }
