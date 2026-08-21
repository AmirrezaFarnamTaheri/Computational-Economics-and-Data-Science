# Structural VAR Identification & Cholesky Decomposition

Causal flow of contemporaneous structural shocks into endogenous macroeconomic observables via lower-triangular Cholesky factor matrix.

```mermaid
flowchart TD
    subgraph Shocks ["Structural Shocks (Orthogonal White Noise)"]
        ugdp["$$u_{\text{GDP}} \sim \mathcal{N}(0, 1)$$<br/>Supply Shock"]
        upi["$$u_{\pi} \sim \mathcal{N}(0, 1)$$<br/>Cost-Push Shock"]
        ur["$$u_R \sim \mathcal{N}(0, 1)$$<br/>Monetary Policy Shock"]
    end

    subgraph Observables ["Endogenous Macroeconomic Variables"]
        ygdp["$$\Delta \ln \text{GDP}_t$$<br/>GDP Growth"]
        ypi["$$\pi_t$$<br/>Inflation Rate"]
        yr["$$R_t$$<br/>Federal Funds Rate"]
    end

    ugdp -->|$$a_{11}$$ (Instantaneous)| ygdp
    ugdp -->|$$a_{21}$$ (Spillover)| ypi
    ugdp -->|$$a_{31}$$ (Spillover)| yr

    upi -->|$$a_{22}$$ (Instantaneous)| ypi
    upi -->|$$a_{32}$$ (Spillover)| yr

    ur -->|$$a_{33}$$ (Policy Shock)| yr

    ygdp -.->|Recursion| ypi
    ypi -.->|Recursion| yr

    classDef shock fill:#EFF6FF,stroke:#3B82F6,stroke-width:2px,color:#1E3A8A;
    classDef obs fill:#ECFDF5,stroke:#10B981,stroke-width:2px,color:#065F46;
    class ugdp,upi,ur shock;
    class ygdp,ypi,yr obs;
```
