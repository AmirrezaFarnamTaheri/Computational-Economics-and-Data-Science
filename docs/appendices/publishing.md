# Publishing with Quarto

Learn to create professional publications from Jupyter notebooks using Quarto.

---

## Overview

This appendix teaches you how to transform Jupyter notebooks into publication-quality documents using Quarto, a modern scientific publishing system. You'll learn to create PDFs, HTML documents, presentations, and even entire websites from your computational work.

**Notebook:** `Appendix/01_Publishing_with_Quarto.ipynb`

---

## What is Quarto?

Quarto is an open-source scientific and technical publishing system built on Pandoc that enables:

- **Multi-format output**: PDF, HTML, Word, PowerPoint, reveal.js slides
- **Reproducible research**: Embed code, results, and narrative
- **Cross-referencing**: Figures, tables, equations, theorems
- **Citations**: BibTeX integration
- **Professional typography**: LaTeX-quality output
- **Collaboration**: Version control friendly

### Why Quarto for Economics?

1. **Reproducibility**: Code and output travel together
2. **Journal submissions**: Many journals accept PDF from LaTeX
3. **Working papers**: Professional-looking documents
4. **Presentations**: Code-driven slides with live execution
5. **Websites**: Course materials, project documentation
6. **Books**: Multi-chapter documents with cross-references

---

## Installation

### Basic Installation

```bash
# Install Quarto (one-time setup)
# Visit https://quarto.org/docs/get-started/
# Download and install for your OS

# Verify installation
quarto --version

# Install Python packages
pip install jupyter nbformat nbclient
```

### LaTeX for PDF Output

```bash
# For PDF output, install TinyTeX
quarto install tinytex

# Or use existing LaTeX distribution
# - TeX Live (Linux)
# - MacTeX (macOS)
# - MiKTeX (Windows)
```

---

## Quick Start

### From Jupyter Notebook

```bash
# Render notebook to HTML
quarto render my_analysis.ipynb

# Render to PDF
quarto render my_analysis.ipynb --to pdf

# Render to Word
quarto render my_analysis.ipynb --to docx

# Render presentation
quarto render my_slides.ipynb --to revealjs
```

### Live Preview

```bash
# Preview with auto-reload
quarto preview my_analysis.ipynb
```

---

## Document Structure

### YAML Header

Add metadata to your notebook's first cell (Raw NBConvert):

```yaml
---
title: "The Effect of Minimum Wage on Employment"
subtitle: "A Synthetic Control Approach"
author: "Your Name"
date: "2024-10-24"
format:
  pdf:
    documentclass: article
    geometry: margin=1in
    fontsize: 12pt
    number-sections: true
  html:
    toc: true
    toc-depth: 3
    code-fold: true
    theme: cosmo
bibliography: references.bib
csl: econometrica.csl
---
```

---

## Key Features

### 1. Code Execution Control

```python
#| echo: false
#| warning: false
#| message: false

# This code runs but doesn't appear in output
import pandas as pd
data = pd.read_csv('data.csv')
```

Common options:
- `echo: false` - Hide code, show output
- `eval: false` - Show code, don't execute
- `include: false` - Execute but hide everything
- `warning: false` - Suppress warnings
- `fig-cap: "Caption text"` - Figure caption

---

### 2. Cross-References

```markdown
See @fig-scatter for the relationship between variables.

```{python}
#| label: fig-scatter
#| fig-cap: "Wage vs. Experience"

plt.scatter(data['experience'], data['wage'])
plt.xlabel('Experience (years)')
plt.ylabel('Hourly Wage ($)')
plt.show()
```

Reference as @fig-scatter in text.
```

Similarly for tables (@tbl-summary), equations (@eq-regression), sections (@sec-intro).

---

### 3. Citations and Bibliography

```markdown
According to @card1994minimum, the effect of minimum wage is...

Multiple citations [@card1994minimum; @angrist2008mostly].

The DiD estimator is:
$$
\hat{\beta} = (\bar{Y}_{T,post} - \bar{Y}_{T,pre}) - (\bar{Y}_{C,post} - \bar{Y}_{C,pre})
$$ {#eq-did}

As shown in @eq-did, the DiD estimator...
```

Requires `references.bib`:
```bibtex
@article{card1994minimum,
  title={Minimum wages and employment: A case study},
  author={Card, David and Krueger, Alan B},
  journal={American Economic Review},
  volume={84},
  number={4},
  pages={772--793},
  year={1994}
}
```

---

### 4. LaTeX Math

Inline math: `$\alpha + \beta = \gamma$`

Display math:
```latex
$$
\max_{c_t, k_{t+1}} \sum_{t=0}^{\infty} \beta^t u(c_t)
$$ {#eq-bellman}

subject to:
$$
c_t + k_{t+1} = f(k_t) + (1-\delta)k_t
$$
```

---

### 5. Callout Blocks

```markdown
::: {.callout-note}
## Note
This is important context for readers.
:::

::: {.callout-warning}
The parallel trends assumption may not hold.
:::

::: {.callout-tip}
## Pro Tip
Use robust standard errors for clustered data.
:::
```

---

## Output Formats

### PDF (Academic Papers)

```yaml
---
title: "My Paper"
format:
  pdf:
    documentclass: article
    classoption: [12pt, twoside]
    geometry:
      - margin=1in
    number-sections: true
    colorlinks: true
    keep-tex: true  # Save intermediate .tex file
---
```

### HTML (Web Reports)

```yaml
---
title: "Analysis Report"
format:
  html:
    toc: true
    toc-location: left
    code-fold: true
    code-tools: true
    theme: cosmo
    grid:
      sidebar-width: 300px
    css: custom.css
---
```

### Presentations (reveal.js)

```yaml
---
title: "Research Presentation"
format:
  revealjs:
    theme: simple
    slide-number: true
    chalkboard: true
    preview-links: auto
    controls: true
---
```

Use `##` for new slides.

### Word Documents

```yaml
---
title: "Report"
format:
  docx:
    reference-doc: template.docx
    toc: true
    number-sections: true
---
```

---

## Advanced Features

### Conditional Content

```markdown
::: {.content-visible when-format="html"}
This appears only in HTML output.
[Interactive Plotly visualization]
:::

::: {.content-visible when-format="pdf"}
This appears only in PDF.
[Static matplotlib figure]
:::
```

### Multi-Column Layouts

```markdown
:::: {.columns}

::: {.column width="50%"}
Content for left column
:::

::: {.column width="50%"}
Content for right column
:::

::::
```

### Tabsets

```markdown
::: {.panel-tabset}

## Estimation Results
[Show regression table]

## Robustness Checks
[Show alternative specifications]

## Diagnostic Plots
[Show residual plots]

:::
```

### Theorem Environments

```markdown
::: {#thm-efficiency}
## Gauss-Markov Theorem
Under assumptions 1-5, OLS is BLUE.
:::

By @thm-efficiency, we know that...
```

---

## Best Practices

### 1. Project Organization

```
project/
├── analysis.qmd or .ipynb
├── _quarto.yml           # Project config
├── references.bib        # Bibliography
├── data/
│   └── dataset.csv
├── scripts/
│   └── utils.py
├── output/
│   ├── analysis.pdf
│   └── analysis.html
└── figures/
    └── saved_plots.png
```

### 2. Reproducibility

```python
#| label: setup
#| include: false

# Set random seed
import numpy as np
np.random.seed(42)

# Record package versions
import sys
print(f"Python: {sys.version}")
print(f"NumPy: {np.__version__}")
```

### 3. Code Organization

- **Setup cell**: Imports and configuration
- **Data loading**: Separate from analysis
- **Helper functions**: In separate script or early cells
- **Main analysis**: Clear logical flow
- **Robustness checks**: Well-organized sections

### 4. Figure Quality

```python
#| label: fig-quality
#| fig-width: 8
#| fig-height: 6
#| fig-dpi: 300
#| fig-cap: "High-resolution figure"

import matplotlib.pyplot as plt
plt.figure(figsize=(8, 6), dpi=300)
# ... plotting code ...
plt.savefig('figure.png', dpi=300, bbox_inches='tight')
```

---

## Academic Workflow

### Working Paper

1. **Draft in Jupyter**: Interactive analysis
2. **Add YAML**: Metadata and format options
3. **Render to PDF**: `quarto render paper.ipynb --to pdf`
4. **Iterate**: Refine analysis and narrative
5. **Version control**: Git-friendly plain text

### Journal Submission

```yaml
---
format:
  pdf:
    documentclass: article
    keep-tex: true        # Submit .tex to journal
    cite-method: natbib   # Or biblatex
---
```

Many journals provide Quarto templates.

### Presentations

```yaml
---
format:
  revealjs:
    theme: [default, custom.scss]
    logo: university_logo.png
    footer: "Author Name | Conference 2024"
    incremental: true   # Bullet points appear one-by-one
---
```

---

## Websites and Blogs

### Create a Website

```yaml
# _quarto.yml
project:
  type: website

website:
  title: "My Research"
  navbar:
    left:
      - href: index.qmd
        text: Home
      - href: research.qmd
        text: Research
      - href: teaching.qmd
        text: Teaching
```

Render: `quarto render`

### Publish to GitHub Pages

```bash
quarto publish gh-pages
```

---

## Books and Course Notes

```yaml
# _quarto.yml
project:
  type: book

book:
  title: "Computational Economics"
  author: "Your Name"
  chapters:
    - index.qmd
    - intro.qmd
    - part: "Part I: Foundations"
      chapters:
        - ch01-python.qmd
        - ch02-numpy.qmd
    - references.qmd
```

---

## Integration with LaTeX

### Custom LaTeX Commands

```yaml
---
format:
  pdf:
    include-in-header:
      text: |
        \newcommand{\E}{\mathbb{E}}
        \newcommand{\Var}{\text{Var}}
        \newcommand{\Cov}{\text{Cov}}
---
```

Use in markdown: `$\E[X]$`, `$\Var(Y)$`

### Theorem Environments

```yaml
---
format:
  pdf:
    include-in-header:
      text: |
        \newtheorem{theorem}{Theorem}
        \newtheorem{lemma}{Lemma}
        \newtheorem{proposition}{Proposition}
---
```

---

## Troubleshooting

### Common Issues

**Issue**: PDF rendering fails
```bash
# Check LaTeX installation
quarto check

# Install missing packages
quarto install tinytex
```

**Issue**: Code doesn't execute
- Check Python environment
- Verify kernel in Jupyter
- Add `#| eval: true`

**Issue**: References not resolving
- Check `references.bib` path
- Verify citation keys
- Use `@citekey` syntax

**Issue**: Figures not appearing
- Check file paths
- Verify `fig-cap` labels
- Ensure code executes

---

## Resources

### Documentation
- [Quarto Official Guide](https://quarto.org/docs/guide/)
- [Quarto Gallery](https://quarto.org/docs/gallery/) - Examples
- [Quarto Journal Templates](https://quarto.org/docs/journals/)

### Tutorials
- [Get Started with Quarto](https://quarto.org/docs/get-started/)
- [Quarto for Academics](https://quarto.org/docs/blog/posts/2022-03-15-quarto-for-academics/)

### Citation Styles
- [Zotero Style Repository](https://www.zotero.org/styles) - Download .csl files
- Common economics styles: econometrica.csl, apa.csl, chicago.csl

### Templates
- [Quarto Journal Articles](https://quarto.org/docs/journals/templates.html)
- [Awesome Quarto](https://github.com/mcanouil/awesome-quarto) - Community resources

---

## Comparison with Alternatives

### Quarto vs. Jupyter Book
- **Quarto**: Single-file notebooks, multi-format, simpler
- **Jupyter Book**: Better for complex books, more customization

### Quarto vs. R Markdown
- **Quarto**: Language-agnostic (Python, R, Julia), newer
- **R Markdown**: R-centric, mature ecosystem

### Quarto vs. LaTeX Directly
- **Quarto**: Easier, reproducible, multi-format
- **LaTeX**: More control, traditional academic workflow

---

## Example Workflow: Research Paper

### Step 1: Analysis Notebook
Create `analysis.ipynb` with:
- Data loading and cleaning
- Descriptive statistics
- Main analysis
- Robustness checks

### Step 2: Add YAML

```yaml
---
title: "Effect of Policy X on Outcome Y"
author: "Your Name"
date: today
format:
  pdf:
    number-sections: true
    colorlinks: true
bibliography: refs.bib
---
```

### Step 3: Structure Sections

```markdown
# Introduction
Background and motivation...

# Data
Description of dataset...

## Summary Statistics
[Code for Table 1]

# Empirical Strategy
Our identification strategy...

# Results
Main findings...

# Robustness
Alternative specifications...

# Conclusion
Summary and implications...

# References {.unnumbered}
::: {#refs}
:::
```

### Step 4: Render

```bash
quarto render analysis.ipynb --to pdf
```

### Step 5: Iterate
- Refine analysis
- Update narrative
- Improve figures
- Re-render

---

## Tips for Success

1. **Start Simple**: Basic YAML, then add features
2. **Preview Often**: `quarto preview` for live updates
3. **Version Control**: Commit `.ipynb` and `.qmd` files
4. **Separate Concerns**: Data processing ≠ presentation
5. **Reusable Code**: Functions in external `.py` files
6. **Document Early**: Write narrative alongside code
7. **Backup**: Cloud storage for important work

---

## Assessment

After completing this appendix, you should be able to:

- [ ] Install and configure Quarto
- [ ] Render notebooks to PDF, HTML, and presentations
- [ ] Use cross-references for figures, tables, and equations
- [ ] Manage citations with BibTeX
- [ ] Create multi-format output from single source
- [ ] Publish websites with Quarto
- [ ] Integrate code, results, and narrative professionally

---

## Practice Exercises

1. **Basic Report**: Render a simple analysis to PDF and HTML
2. **Citations**: Add bibliography and cite 5+ papers
3. **Cross-References**: Create document with numbered figures and tables
4. **Presentation**: Convert analysis to reveal.js slides
5. **Website**: Create personal academic website
6. **Full Paper**: Write complete working paper with Quarto

---

## Need Help?

- Work through `Appendix/01_Publishing_with_Quarto.ipynb`
- Check [Quarto Documentation](https://quarto.org/docs/guide/)
- Visit [Quarto Discussions](https://github.com/quarto-dev/quarto-cli/discussions)
- Ask in [Course Discussions](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/discussions)

---

**Master professional publishing and make your research reproducible and accessible!**
