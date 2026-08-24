#!/usr/bin/env python3
"""Create executable real-data replication labs supported by bundled datasets."""

from __future__ import annotations

from pathlib import Path

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "Appendix"


def md(text: str):
    return nbf.v4.new_markdown_cell(text.strip() + "\n")


def code(text: str):
    return nbf.v4.new_code_cell(text.strip() + "\n")


def write_if_missing(path: Path, cells: list) -> bool:
    if path.exists():
        return False
    nb = nbf.v4.new_notebook(cells=cells)
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3",
    }
    nb.metadata["language_info"] = {"name": "python", "version": "3.11"}
    nbf.write(nb, path)
    return True


def card_krueger() -> bool:
    path = APP / "T4_Replication_Card_Krueger_1994.ipynb"
    cells = [
        md(r"""
# T4 Replication Lab: Card & Krueger (1994) Minimum Wage and Employment

## The Lens: A Policy Change as a Natural Experiment
New Jersey raised its minimum wage while neighboring eastern Pennsylvania did not. The empirical question is whether fast-food employment changed differently in New Jersey after the policy. The two-wave restaurant panel makes the canonical difference-in-differences (DiD) estimand transparent: compare the before/after change in the treated state with the same change in the control state.

### Learning Objectives
- Reconstruct the two-by-two DiD estimand from group means.
- Estimate the same interaction coefficient by OLS with heteroskedasticity-robust uncertainty.
- Add chain/ownership/region controls without changing the target estimand.
- State what a two-wave design can and cannot reveal about parallel trends.

### Prerequisites
- `../06-Econometrics/08_Difference_in_Differences.ipynb`
- `../06-Econometrics/01_Linear_Model_and_OLS.ipynb`

### Table of Contents
1. Data provenance and validation
2. Two-by-two DiD
3. Regression representation
4. Controlled specification and diagnostics
5. Interpretation and identification limits
6. Exercises
7. Summary and references
"""),
        code(r"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf


def locate(relative: str) -> Path:
    candidates = [Path(relative), Path("..") / relative]
    path = next((p for p in candidates if p.exists()), None)
    if path is None:
        raise FileNotFoundError(f"Could not locate {relative} from repository root or Appendix/")
    return path

DATA = locate("data/replications/card_krueger_1994_njmin3.csv")
df = pd.read_csv(DATA)
required = {"nj", "d", "d_nj", "fte", "bk", "kfc", "roys", "wendys", "co_owned", "centralj", "southj", "pa1", "pa2"}
missing = required.difference(df.columns)
assert not missing, f"Missing required columns: {sorted(missing)}"
assert set(df["nj"].dropna().unique()) <= {0, 1}
assert set(df["d"].dropna().unique()) <= {0, 1}
print(f"Loaded {len(df):,} restaurant-wave observations from {DATA}.")
"""),
        md(r"""
## 1. Data Provenance and Estimand
The bundled file is a long-form version of the Card–Krueger fast-food survey: `nj=1` identifies New Jersey, `d=1` identifies the post-policy wave, `d_nj = nj × d`, and `fte` is full-time-equivalent employment. The DiD estimand is

$$
\widehat{\tau}_{DiD} = (\bar Y_{NJ,post}-\bar Y_{NJ,pre})-(\bar Y_{PA,post}-\bar Y_{PA,pre}).
$$

With only one pre-treatment wave, this dataset cannot empirically validate a pre-trend. Parallel trends remains an identifying assumption that must be defended institutionally and with external evidence.
"""),
        code(r"""
means = df.groupby(["nj", "d"], observed=True)["fte"].agg(["count", "mean"])
display(means)
pa_pre = means.loc[(0, 0), "mean"]
pa_post = means.loc[(0, 1), "mean"]
nj_pre = means.loc[(1, 0), "mean"]
nj_post = means.loc[(1, 1), "mean"]
did = (nj_post - nj_pre) - (pa_post - pa_pre)
print(f"Two-by-two DiD estimate: {did:.4f} FTE workers per restaurant")

plot = means["mean"].unstack("d").rename(columns={0: "Pre", 1: "Post"})
ax = plot.T.plot(marker="o", figsize=(8, 5))
ax.set(title="Mean FTE Employment by State and Survey Wave", xlabel="Survey wave", ylabel="FTE employment")
ax.legend(["Pennsylvania", "New Jersey"], title="Group")
plt.show()
"""),
        md(r"""
## 2. Regression Representation
The saturated two-by-two regression is

$$
Y_{it}=\alpha+\gamma NJ_i+\lambda Post_t+\tau(NJ_i\times Post_t)+\varepsilon_{it}.
$$

In this design, the interaction coefficient $\tau$ is algebraically identical to the four-cell DiD above. Robust standard errors address heteroskedasticity, but they do not repair violations of parallel trends or other identification assumptions.
"""),
        code(r"""
base = smf.ols("fte ~ nj + d + d_nj", data=df).fit(cov_type="HC1")
print(base.summary().tables[1])
assert np.isclose(base.params["d_nj"], did, atol=1e-10)
print(f"Interaction equals manual DiD: {base.params['d_nj']:.4f}")
"""),
        md(r"""
## 3. Controlled Specification and Diagnostics
Controls can absorb residual composition differences across restaurant chains, ownership, and regions. They should not be chosen because they make the treatment coefficient more attractive. The estimand remains the post-policy differential change associated with New Jersey.
"""),
        code(r"""
formula = "fte ~ nj + d + d_nj + bk + kfc + roys + co_owned + centralj + southj + pa1 + pa2"
controlled = smf.ols(formula, data=df).fit(cov_type="HC1")
comparison = pd.DataFrame({
    "estimate": [base.params["d_nj"], controlled.params["d_nj"]],
    "robust_se": [base.bse["d_nj"], controlled.bse["d_nj"]],
}, index=["Two-by-two", "With controls"])
display(comparison)
print(f"Complete-case N in controlled model: {int(controlled.nobs)}")
"""),
        md(r"""
## 4. Interpretation and Identification Limits
A positive DiD coefficient means New Jersey employment rose relative to the Pennsylvania comparison group over the two survey waves. That is a statement about the observed design, not a universal claim that minimum-wage increases always raise employment. With one pre-period, the notebook cannot test differential pre-trends; survey measurement, spillovers, compositional changes, and treatment anticipation remain substantive concerns.

## Exercises
**1. Design logic (Conceptual):** Derive why the OLS interaction coefficient equals the four-cell DiD. Which assumption gives the coefficient a causal interpretation?

**2. Robustness (Applied):** Re-estimate the coefficient using alternative FTE constructions if the source variables are available, and compare robust uncertainty and sample size.

**3. Identification stress test (Challenge):** Simulate a differential pre-trend that continues into the post period. Show how the DiD coefficient mixes the policy effect with the trend violation.

## Summary & Key Takeaways
- The manual four-cell calculation and OLS interaction target the same DiD estimand.
- Robust standard errors address variance estimation, not identification.
- A two-wave design makes institutional reasoning about parallel trends especially important.

## References & Further Reading
- Card, D. & Krueger, A. B. (1994). Minimum Wages and Employment: A Case Study of the Fast-Food Industry in New Jersey and Pennsylvania. *American Economic Review*, 84(4), 772–793.
- Angrist, J. D. & Pischke, J.-S. (2009). *Mostly Harmless Econometrics*. Princeton University Press.
"""),
    ]
    return write_if_missing(path, cells)


def fama_french() -> bool:
    path = APP / "T5_Replication_Fama_French_Five_Factor.ipynb"
    cells = [
        md(r"""
# T5 Replication Lab: Fama–French Five-Factor Model

## The Lens: Do Common Risk Factors Explain Industry Returns?
The five-factor model augments the market factor with size, value, profitability, and investment factors. This lab uses the repository's bundled monthly factor file and 10-industry portfolio returns to estimate time-series factor regressions. The local five-factor snapshot spans 2015–2022, so this is a **replication-style reproduction on a later sample**, not a reconstruction of every table in Fama and French (2015).

### Learning Objectives
- Align return and factor datasets by month without look-ahead operations.
- Estimate industry excess-return regressions on MKT, SMB, HML, RMW, and CMA.
- Interpret factor loadings, intercepts, and adjusted $R^2$.
- Distinguish a later-sample reproduction from an exact historical replication.

### Prerequisites
- `../09-Finance/01_Portfolio_Theory.ipynb`
- `../09-Finance/02_Asset_Pricing.ipynb`
- `../06-Econometrics/01_Linear_Model_and_OLS.ipynb`

### Table of Contents
1. Data alignment and provenance
2. Five-factor regression
3. Cross-industry diagnostic panel
4. Interpretation and limits
5. Exercises
6. Summary and references
"""),
        code(r"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm


def locate(relative: str) -> Path:
    candidates = [Path(relative), Path("..") / relative]
    path = next((p for p in candidates if p.exists()), None)
    if path is None:
        raise FileNotFoundError(relative)
    return path

factor_path = locate("data/fama_french_5_factors.csv")
industry_path = locate("data/10_industry_portfolios.csv")
factors = pd.read_csv(factor_path)
industries = pd.read_csv(industry_path)
for frame in (factors, industries):
    frame["Date"] = pd.PeriodIndex(frame["Date"], freq="M")
panel = industries.merge(factors, on="Date", how="inner", validate="one_to_one")
assert not panel.empty
print(f"Overlap: {panel['Date'].min()} to {panel['Date'].max()} ({len(panel)} months)")
"""),
        md(r"""
## 1. Time-Series Five-Factor Regression
For industry portfolio $i$,

$$
R_{it}-R_{ft}=\alpha_i+\beta_{MKT,i}(R_{Mt}-R_{ft})+\beta_{SMB,i}SMB_t+\beta_{HML,i}HML_t+\beta_{RMW,i}RMW_t+\beta_{CMA,i}CMA_t+\varepsilon_{it}.
$$

All bundled returns are percentages per month. We keep that unit for estimation, so an intercept of `0.10` means 0.10 percentage points per month.
"""),
        code(r"""
factor_cols = ["Mkt-RF", "SMB", "HML", "RMW", "CMA"]
industry_cols = [c for c in industries.columns if c != "Date"]
X = sm.add_constant(panel[factor_cols])
results = {}
rows = []
for industry in industry_cols:
    y = panel[industry] - panel["RF"]
    fit = sm.OLS(y, X).fit(cov_type="HC1")
    results[industry] = fit
    rows.append({
        "industry": industry,
        "alpha_monthly_pct": fit.params["const"],
        "alpha_annualized_pct": 12 * fit.params["const"],
        "alpha_pvalue": fit.pvalues["const"],
        "adj_r2": fit.rsquared_adj,
        **{f"beta_{name}": fit.params[name] for name in factor_cols},
    })
summary = pd.DataFrame(rows).set_index("industry")
display(summary.round(4))
"""),
        md(r"""
## 2. One Industry in Detail
The coefficient vector is an empirical description of how that industry's excess returns co-move with the five factor portfolios. The intercept is often used as a pricing diagnostic, but statistical insignificance is not proof that the model is structurally correct.
"""),
        code(r"""
example = "HiTec"
print(results[example].summary())

fig, axes = plt.subplots(1, 2, figsize=(13, 5))
summary["alpha_annualized_pct"].sort_values().plot.barh(ax=axes[0])
axes[0].set(title="Annualized Five-Factor Alpha by Industry", xlabel="percentage points/year")
summary["adj_r2"].sort_values().plot.barh(ax=axes[1])
axes[1].set(title="Adjusted $R^2$ by Industry", xlabel="adjusted $R^2$")
plt.tight_layout()
plt.show()
"""),
        md(r"""
## 3. Interpretation and Replication Boundary
The exercise uses real bundled factor and industry-portfolio data, but the five-factor file starts in 2015. Fama and French (2015) evaluate a much longer historical sample and a broader set of test portfolios. Therefore differences from the published paper are expected and should not be labeled replication failures. This notebook is designed to reproduce the **econometric mechanism and diagnostics** on a transparent local sample.

## Exercises
**1. Factor meaning (Conceptual):** Explain the economic interpretation of each of SMB, HML, RMW, and CMA. Why can a high $R^2$ coexist with a nonzero intercept?

**2. Model comparison (Applied):** Re-estimate every industry using only the market factor and compare adjusted $R^2$, alphas, and residual volatility with the five-factor specification.

**3. Stability (Challenge):** Split the 2015–2022 sample into two subperiods. Quantify which factor loadings are least stable and discuss whether the shift is economic, statistical, or both.

## Summary & Key Takeaways
- Alignment by calendar month is part of the econometric specification, not clerical preprocessing.
- Industry factor loadings differ meaningfully; intercepts and residual diagnostics remain necessary.
- A later-sample reproduction must be clearly separated from an exact paper replication.

## References & Further Reading
- Fama, E. F. & French, K. R. (2015). A five-factor asset pricing model. *Journal of Financial Economics*, 116(1), 1–22.
- Cochrane, J. H. (2005). *Asset Pricing*. Princeton University Press.
"""),
    ]
    return write_if_missing(path, cells)


def main() -> None:
    created = []
    if card_krueger():
        created.append("Card-Krueger")
    if fama_french():
        created.append("Fama-French")
    print(
        f"Created {len(created)} replication notebooks: {', '.join(created) if created else 'none (already present)'}"
    )


if __name__ == "__main__":
    main()
