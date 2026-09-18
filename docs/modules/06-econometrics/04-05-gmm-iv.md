# GMM & Instrumental Variables

> This page is synchronized from the authoritative notebooks. Use the generated reading view for searchable prose/code, or open the notebook for execution.

## Summary

**What problem are we solving?** OLS requires minimizing squared errors. MLE requires knowing the full probability distribution. What if we don't want to make such strong assumptions? **Generalized Method of Moments (GMM)** is a framework that encompasses OLS, IV, MLE, and more. It requires only that certain **moment conditions** hold in the population (e.g., $E[x \epsilon] = 0$). **Why this method?** GMM is incredib

[Read generated page](../../notebooks/06-Econometrics/04_GMM.md){ .md-button } [Open notebook](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/blob/main/06-Econometrics/04_GMM.ipynb){ .md-button }

## Summary

**What problem are we solving?** When $X$ is correlated with the error term $\epsilon$ (endogeneity), OLS is biased and inconsistent. * **Omitted Variable Bias:** Ability affects both education and wages. * **Reverse Causality:** Growth affects investment, and investment affects growth. **Instrumental Variables (IV)** provide a way to cut this link and isolate the causal variation in $X$. **Why this method?** We need

[Read generated page](../../notebooks/06-Econometrics/05_Instrumental_Variables.md){ .md-button } [Open notebook](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/blob/main/06-Econometrics/05_Instrumental_Variables.ipynb){ .md-button }
