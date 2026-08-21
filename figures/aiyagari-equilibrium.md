# Aiyagari (1994) Stationary General Equilibrium

Two-layer nested loop computation: Outer interest rate bisection and inner dynamic programming with distribution invariant tracking.

```mermaid
flowchart TD
    subgraph OuterLoop ["Outer General Equilibrium Loop"]
        guess["Guess Interest Rate $$r^{(0)} \in (0, 1/\beta - 1)$$"]
        factor["Compute Wage Rate: $$w = (1-\alpha) k^\alpha$$"]
        clearing{"Capital Market Clearing<br/>$$|K_s(r) - K_d(r)| < \epsilon$$"}
        update["Update Interest Rate $$r^{(k+1)}$$<br/>via Bisection / Anderson Acceleration"]
        eq["Stationary General Equilibrium<br/>$$(r^*, w^*, K^*, \mu^*)$$"]
    end

    subgraph InnerLoop ["Inner Microeconomic Solvers"]
        vfi["Solve Household Bellman Equation<br/>$$V(a, z; r) = \max \left\{ u(c) + \beta \mathbb{E}[V(a', z')] \right\}$$"]
        policy["Extract Optimal Asset Policy: $$a'(a, z; r)$$"]
        dist["Compute Invariant Stationary Distribution<br/>$$T_r(\mu) = \mu$$"]
        agg["Aggregate Capital Supply:<br/>$$K_s(r) = \int a \, d\mu(a, z)$$"]
    end

    guess --> factor
    factor --> vfi
    vfi --> policy
    policy --> dist
    dist --> agg
    agg --> clearing
    clearing -->|No| update
    update --> factor
    clearing -->|Yes| eq

    classDef outer fill:#EFF6FF,stroke:#3B82F6,stroke-width:1.8px,color:#1E3A8A;
    classDef inner fill:#F8FAFC,stroke:#64748B,stroke-width:1.5px,color:#0F172A;
    classDef dec fill:#FEF3C7,stroke:#F59E0B,stroke-width:2px,color:#92400E;
    classDef success fill:#ECFDF5,stroke:#10B981,stroke-width:2px,color:#065F46;
    class guess,factor,update outer;
    class vfi,policy,dist,agg inner;
    class clearing dec;
    class eq success;
```
