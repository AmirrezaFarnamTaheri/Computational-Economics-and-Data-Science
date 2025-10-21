# -*- coding: utf-8 -*-
# === Environment Setup ===
import os, sys, math, time, random, json, textwrap, warnings
import numpy as np, pandas as pd, matplotlib.pyplot as plt
import statsmodels.api as sm
import statsmodels.formula.api as smf
from linearmodels.iv import IV2SLS
import seaborn as sns

# --- Configuration ---
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({'font.size': 14, 'figure.figsize': (12, 8), 'figure.dpi': 150})
np.set_printoptions(suppress=True, linewidth=120, precision=4)

# --- Utility Functions ---
def note(msg, **kwargs):
    print(f"📝 {textwrap.fill(msg, width=100)}")
def sec(title):
    print(f"\n{100*'='}\\n| {title.upper()} |\n{100*'='}")

# --- Simulation Function ---
def run_weak_iv_sim(instrument_strength=0.1, n_sims=1000):
    true_beta = 0.8; ols_estimates, iv_estimates = [], []
    for _ in range(n_sims):
        n = 200; ability = np.random.normal(0, 1, n); instrument = np.random.normal(0, 1, n)
        education = instrument_strength * instrument + 1.2 * ability + np.random.normal(0, 1, n)
        log_wage = true_beta * education + 1.0 * ability + np.random.normal(0, 1, n)
        df = pd.DataFrame({'log_wage':log_wage, 'educ':education, 'instr':instrument})
        ols = smf.ols('log_wage ~ educ', data=df).fit()
        iv = IV2SLS.from_formula('log_wage ~ 1 + [educ ~ instr]', df).fit()
        ols_estimates.append(ols.params['educ']); iv_estimates.append(iv.params['educ'])

    plt.figure(figsize=(12, 6))
    sns.kdeplot(ols_estimates, label=f'OLS Estimates (Mean={np.mean(ols_estimates):.2f})', fill=True)
    sns.kdeplot(iv_estimates, label=f'IV Estimates (Mean={np.mean(iv_estimates):.2f})', fill=True)
    plt.axvline(true_beta, color='k', ls='--', label=f'True Beta = {true_beta}')
    plt.title(f'Distribution of OLS vs. IV Estimates (Instrument Strength: {instrument_strength})')
    plt.legend(); plt.xlabel("Beta Estimate"); plt.ylabel("Density")
    plt.savefig('weak_instrument.png')
    print("Weak instrument plot saved.")
    note(f"With instrument strength = {instrument_strength}, the IV estimator's distribution is wide and biased towards the OLS estimate.")

note("Environment initialized for Advanced Instrumental Variables.")

# Case Study with Substitute Dataset
sec("Case Study: Substitute Dataset for Instrumental Variables")
card_df = None
try:
    note("Using the 'card' dataset from 'wooldridge' to validate the IV logic.")
    card_data = sm.datasets.get_rdataset('card', 'wooldridge')
    card_df = card_data.data
    note(f"Loaded 'card' dataset. Shape: {card_df.shape}")

    card_df.rename(columns={'lwage': 'log_wage', 'educ': 'education', 'nearc4': 'instrument'}, inplace=True)
    card_df = card_df[['log_wage', 'education', 'instrument']].dropna()

    ols_model = smf.ols('log_wage ~ education', data=card_df).fit()
    iv_model = IV2SLS.from_formula('log_wage ~ 1 + [education ~ instrument]', data=card_df).fit()

    print("--- OLS Results (using 'card' data) ---"); print(ols_model.summary().tables[1])
    print("\n--- IV (2SLS) Results (using 'card' data) ---"); print(iv_model)

    f_stat_series = iv_model.first_stage.diagnostics['f.stat']
    f_stat_value = f_stat_series.iloc[0] # Extract the float value from the Series
    note(f"First-stage F-statistic: {f_stat_value:.2f}. A common rule of thumb is that an F-statistic > 10 suggests instruments are not weak.")

except Exception as e:
    note(f"An error occurred during the case study. Error: {e}")

# Weak Instrument Problem
sec("Interactive: The Weak Instrument Problem")
run_weak_iv_sim(instrument_strength=0.05)

# Control Function
sec("Control Function Example and Endogeneity Test")
if card_df is not None:
    try:
        # 1. First Stage
        first_stage = smf.ols('education ~ instrument', data=card_df).fit()
        card_df['resid'] = first_stage.resid

        # 2. Second Stage
        control_fn_model = smf.ols('log_wage ~ education + resid', data=card_df).fit()

        print(control_fn_model.summary().tables[1])
        p_value_resid = control_fn_model.pvalues['resid']
        note(f"The coefficient on 'education' is the control function estimate. The p-value for the residual term is {p_value_resid:.3f}. If this p-value is < 0.05, we reject the null of exogeneity.")
    except Exception as e:
        note(f"An error occurred during the control function section. Error: {e}")
else:
    note("Dataset not available for Control Function example.")
