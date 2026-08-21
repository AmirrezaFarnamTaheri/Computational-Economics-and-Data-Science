# Fama-MacBeth Two-Pass Cross-Sectional Regression

Standard empirical asset pricing methodology decomposing asset return betas and risk premia lambdas across time.

```mermaid
flowchart TD
    A["Panel of Asset Returns $$R_{i,t}$$ & Factor Returns $$F_t$$"] --> B["Pass 1: Time-Series Regressions (for each asset $$i$$)<br/>$$R_{i,t} - R_{f,t} = \alpha_i + \beta_i' F_t + \epsilon_{i,t}$$"]
    B --> C["Estimated Risk Exposures (Factor Betas $$\hat{\beta}_i$$)"]
    C --> D["Pass 2: Cross-Sectional Regressions (for each time $$t$$)<br/>$$R_{i,t} - R_{f,t} = \gamma_{0,t} + \hat{\beta}_i' \lambda_t + \eta_{i,t}$$"]
    D --> E["Time Series of Risk Premia Estimates $$\hat{\lambda}_t$$"]
    E --> F["Time-Series Averaging & Standard Error Inference<br/>$$\hat{\lambda} = \frac{1}{T} \sum_{t=1}^T \hat{\lambda}_t, \quad \text{SE}(\hat{\lambda}) = \frac{\hat{\sigma}_{\lambda}}{\sqrt{T}}$$"]
    F --> G["Asset Pricing Test: Shanken (1992) Correction & $$t$$-stats"]

    classDef step fill:#F8FAFC,stroke:#64748B,stroke-width:1.5px,color:#0F172A;
    classDef pass fill:#EFF6FF,stroke:#3B82F6,stroke-width:2px,color:#1E3A8A;
    classDef result fill:#ECFDF5,stroke:#10B981,stroke-width:2px,color:#065F46;
    class A,C,E step;
    class B,D pass;
    class F,G result;
```
