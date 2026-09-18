# Real Business Cycle Models

> This page is synchronized from the authoritative notebooks. Use the generated reading view for searchable prose/code, or open the notebook for execution.

## Summary

**What problem are we solving?** Business cycles—the boom and bust of the economy—were traditionally analyzed using ad-hoc aggregate relationships (like IS-LM). The **Real Business Cycle (RBC)** revolution grounded fluctuations in micro-level optimization. This notebook builds the structural core: equilibrium conditions and the planner's problem that define the model. **Why this method?** We build a dynamic stochasti

[Read generated page](../../notebooks/04-Macro-Models/03A_RBC_Model_Foundations.md){ .md-button } [Open notebook](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/blob/main/04-Macro-Models/03A_RBC_Model_Foundations.ipynb){ .md-button }

## Summary

**What problem are we solving?** Once the RBC equilibrium conditions are established, we need a practical way to compute decision rules and simulate the economy under shocks. The key challenge is transforming a nonlinear system into a solvable linear representation and then interpreting the resulting dynamics. **Why this method?** Log-linearization and the QZ (generalized Schur) decomposition provide a stable, transp

[Read generated page](../../notebooks/04-Macro-Models/03B_RBC_Model_Solution.md){ .md-button } [Open notebook](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/blob/main/04-Macro-Models/03B_RBC_Model_Solution.ipynb){ .md-button }

## Summary

**What problem are we solving?** Once we solve the RBC model, we need to understand how the economy responds to *unexpected* productivity shocks. **Why this method?** Impulse-response style simulations translate the linearized solution into time paths for output, consumption, investment, and labor. **Economic question.** In *03C Real Business Cycle (RBC) Models: Dynamics and Surprise Shocks*, what must remain economi

[Read generated page](../../notebooks/04-Macro-Models/03C_RBC_Dynamics_and_Surprise_Shocks.md){ .md-button } [Open notebook](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/blob/main/04-Macro-Models/03C_RBC_Dynamics_and_Surprise_Shocks.ipynb){ .md-button }

## Summary

**What problem are we solving?** Expectations about future productivity can move the economy today, even before productivity changes. **Why this method?** News shocks require extending the RBC state space to capture anticipated future changes and their effects on current decisions. **Economic question.** In *03D Real Business Cycle (RBC) Models: News Shocks and Expectations*, what must remain economically invariant w

[Read generated page](../../notebooks/04-Macro-Models/03D_RBC_News_Shocks_and_Expectations.md){ .md-button } [Open notebook](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/blob/main/04-Macro-Models/03D_RBC_News_Shocks_and_Expectations.ipynb){ .md-button }
