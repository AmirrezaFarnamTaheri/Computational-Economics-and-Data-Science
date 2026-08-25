# Machine Learning Cheat Sheet

> Quick reference for Module 07. Details: [ML for Economists](../modules/07-machine-learning/01-intro.md), [Deep Learning](../modules/07-machine-learning/06-deep-learning.md), [Transformers](../modules/07-machine-learning/10-transformers.md), [Causal ML](../modules/07-machine-learning/17-causal-ml.md).

## Core objects & dimensions

| Object | Notation | Dimensions |
|---|---|---|
| Feature matrix / target | $X \in \mathbb{R}^{n \times p}$, $\mathbf{y} \in \mathbb{R}^n$ | $n$ obs, $p$ features |
| Fitted model | $\hat{f}: \mathbb{R}^p \to \mathbb{R}$ (or classes) | — |
| Parameters | $\theta \in \mathbb{R}^{P}$ | model-dependent |
| Latent dim (AE/VAE) | $\mathbf{z} \in \mathbb{R}^{d_z}$ | $d_z \ll p$ |

## Decompositions & losses

- **Bias-variance**: $E[(y_0 - \hat{f}(x_0))^2] = \mathrm{Bias}^2 + \mathrm{Variance} + \sigma_\epsilon^2$ (all scalars).
- Ridge: $\hat{\beta} = (X'X + \lambda I_p)^{-1} X'\mathbf{y}$ — closed form; Lasso: no closed form (coordinate descent), sparse $\hat{\beta}$.
- Log loss: $-\frac{1}{n}\sum_i [y_i \ln \hat{p}_i + (1-y_i)\ln(1-\hat{p}_i)]$.
- VAE ELBO: $\ln p(x) \ge \underbrace{E_{q}[\ln p(x|z)]}_{\text{reconstruction}} - \underbrace{D_{KL}(q(z|x)\,\|\,p(z))}_{\text{regularizer}}$, both scalars.

## Algorithms & complexity

| Method | Train | Predict | Notes |
|---|---|---|---|
| kNN | O(1) | $O(nd)$ per query | curse of dimensionality |
| Random forest | $O(T \cdot n d \log n)$ | $O(T \cdot \text{depth})$ | $T$ trees |
| GBM / XGBoost | $O(M \cdot n d)$ (histogram: $n \cdot \text{bins}$) | $O(M \cdot \text{depth})$ | early stopping on validation |
| NN (1 epoch) | $O(n \cdot W)$ fwd+bwd | $O(W)$ | $W$ = weight count |
| Attention layer | $O(T^2 d)$ | — | $T$ tokens, $d$ model dim |

## Discipline

1. Fit preprocessing **inside** the pipeline on train folds only (no leakage).
2. Time-ordered data → expanding-window CV, never random splits.
3. Tune via nested CV; touch the test set once.
4. Deep RL: target networks + replay (deadly triad); report distributions over seeds.

## Causal ML

Double/ debiased ML: $\hat{\theta} = \frac{\sum_i \tilde{Y}_i \tilde{D}_i}{\sum_i \tilde{D}_i^2}$ with cross-fitted residuals $\tilde{Y}, \tilde{D}$; CATE forests estimate heterogeneous effects, not ATEs alone.
