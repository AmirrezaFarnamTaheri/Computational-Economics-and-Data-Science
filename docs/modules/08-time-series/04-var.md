# Vector Autoregression

> This page is synchronized from the authoritative notebooks. Use the generated reading view for searchable prose/code, or open the notebook for execution.

## Summary

**What economic problem are we solving?** The economy is a deeply interconnected system. A hike in interest rates doesn't just lower inflation; it might also slow GDP growth, increase unemployment, and strengthen the currency. These variables feed back into each other over time: lower growth might eventually lower inflation further, prompting the central bank to cut rates. Single-equation models (like ARIMA) ignore t

[Read generated page](../../notebooks/08-Time-Series/04A_VAR_Estimation_and_Granger.md){ .md-button } [Open notebook](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/blob/main/08-Time-Series/04A_VAR_Estimation_and_Granger.ipynb){ .md-button }

## Summary

**What problem are we solving?** A reduced-form VAR captures comovements, but policy analysis requires **structural shocks**. We must decide how to interpret contemporaneous correlations in the residuals. **Why this method?** Identification schemes (like Cholesky ordering) impose economic structure on the reduced-form system so impulse responses can be interpreted as causal shocks. **Scope note:** This notebook conti

[Read generated page](../../notebooks/08-Time-Series/04B_VAR_Identification_and_Structural_Shocks.md){ .md-button } [Open notebook](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/blob/main/08-Time-Series/04B_VAR_Identification_and_Structural_Shocks.ipynb){ .md-button }

## Summary

**What problem are we solving?** Once shocks are identified, we need to trace how they ripple through the economy over time. **Why this method?** Impulse responses (IRFs) and forecast error variance decompositions (FEVDs) translate a VAR into interpretable dynamic effects and quantify which shocks drive each variable. **Scope note:** This notebook focuses on multivariate dynamics and forecast decomposition. Classical

[Read generated page](../../notebooks/08-Time-Series/04C_VAR_Impulse_Responses_and_FEVD.md){ .md-button } [Open notebook](https://github.com/AmirrezaFarnamTaheri/Computational-Economics-and-Data-Science/blob/main/08-Time-Series/04C_VAR_Impulse_Responses_and_FEVD.ipynb){ .md-button }
