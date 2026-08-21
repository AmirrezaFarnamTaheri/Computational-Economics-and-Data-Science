# Causal Directed Acyclic Graph: Collider Conditioning Bias

Illustration of Berkson's Paradox and induced spurious correlation when conditioning on common collider.

```mermaid
flowchart LR
    X["Talent / Ability $$X$$"] -->|Causes| C["Academic Admission $$C$$<br/>(Collider)"]
    Y["Motivation / Effort $$Y$$"] -->|Causes| C
    
    subgraph Conditioned ["Conditioning on Collider ($$C = 1$$)"]
        X -.->|"Induced Spurious Correlation $$\rho < 0$$"| Y
    end

    classDef root fill:#EFF6FF,stroke:#3B82F6,stroke-width:2px,color:#1E3A8A;
    classDef collider fill:#FEF3C7,stroke:#F59E0B,stroke-width:2px,color:#92400E;
    class X,Y root;
    class C collider;
```
