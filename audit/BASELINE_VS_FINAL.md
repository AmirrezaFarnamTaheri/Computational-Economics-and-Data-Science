# Baseline vs Final Curriculum Quality

The baseline is the user-provided ZIP as received. The final column is the improved tree at release-audit time.

| Metric | Baseline | Final |
|---|---:|---:|
| Notebook count | 121 | 129 |
| Standard `## The Lens` heading | 36 | 129 |
| Learning Objectives | 117 | 129 |
| Prerequisites | 117 | 129 |
| Table of Contents | 121 | 129 |
| Exercises | 84 | 129 |
| Summary/Key Takeaways | 107 | 129 |
| References/Further Reading | 4 | 129 |
| Exercise tier: Conceptual | 15 | 129 |
| Exercise tier: Applied | 29 | 129 |
| Exercise tier: Challenge | 36 | 129 |
| Colab badges | 0 | 129 |
| Binder badges | 0 | 129 |
| Notebooks with duplicate cell IDs | 2 | 0 |
| Notebooks with missing cell IDs | 1 | 0 |
| Notebooks with strong placeholders | 1 | 0 |
| Notebooks with blanket warning suppression | 11 | 0 |
| Notebooks with Python/IPython syntax errors | 2 | 0 |
| Broken local Markdown image references | 8 | 0 |
| Broken code Image(filename=...) references | 13 | 0 |
| Zero-byte image assets | 0 | 0 |
| Blocking notebooks under strict audit | 121 | 0 |

Strict structural compliance is intentionally stronger in the final audit than the historical planning documents: every notebook must expose all three exercise tiers, stable cell IDs, valid local asset references, and parseable Python/IPython code.
