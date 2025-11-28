import nbformat
import os

# Dictionary containing the "Gold Standard" content for each notebook
CONTENT_MAP = {
    # --- Module 03: Economic Modeling ---
    '01_Dynamic_Programming.ipynb': {
        'lens': """# The Lens: The Recursive Structure of Choice

**What problem are we solving?**
Most economic decisions are not one-off events; they are sequences of choices made over time. A firm decides investment today, tomorrow, and next year. A worker decides whether to accept a job offer or keep searching. A central bank sets interest rates month after month.
To optimize a sequence of decisions, we must account for how today's choice affects tomorrow's possibilities. This is the realm of **Dynamic Programming**.

**Why this method?**
Solving an infinite-horizon problem directly (choosing an infinite sequence of actions) is mathematically impossible. Dynamic Programming breaks this impossible problem into two manageable parts:
1.  **Current Reward:** What do I get today?
2.  **Continuation Value:** What is the value of the state I leave for tomorrow?
The **Bellman Equation** formalizes this recursive logic:
$$ V(x) = \max_{a} \{ u(x, a) + \beta V(x') \} $$
By finding the **fixed point** of this equation, we solve the entire infinite-horizon problem at once.

This notebook introduces the machinery of DP: the Bellman Operator, Value Function Iteration, and the Contraction Mapping Theorem.""",
        'summary': """# Summary

Dynamic Programming is the grammar of modern macroeconomics.

**Key Takeaways:**
*   **Recursive Thinking:** Don't solve for a sequence; solve for a rule (policy function).
*   **The Bellman Operator:** It maps a guess of the value function to a better guess. Iterating it leads to the truth.
*   **The Curse of Dimensionality:** As the number of state variables increases, the computational burden grows exponentially. This is the main limit of standard DP methods."""
    },
    '02_DP_with_Continuous_States.ipynb': {
        'lens': """# The Lens: Approximating the Continuum

**What problem are we solving?**
In the basic DP model, we often assume states (like capital or wealth) are discrete. But in reality, capital is a continuous variable. If we restrict an agent to choose from a grid of 100 points, we introduce artificial friction. How do we solve the Bellman equation when the state space is continuous?

**Why this method?**
We cannot store a function $V(k)$ for every possible real number $k$. We must **approximate** it.
*   **Interpolation:** We solve for $V(k)$ at specific nodes and use interpolation (linear, cubic, etc.) to evaluate it in between.
*   **Fitted Value Iteration:** We guess a functional form (like a polynomial) and find the coefficients that best fit the Bellman equation.

This notebook extends our DP toolkit to handle the continuous nature of economic variables.""",
        'summary': """# Summary

Continuous state spaces require us to blend optimization with approximation.

**Key Takeaways:**
*   **Interpolation is Key:** The choice of interpolation scheme (linear vs. cubic vs. Chebyshev) determines the accuracy and stability of your solution.
*   **Standard vs. Fitted VFI:** Standard VFI updates values on a grid. Fitted VFI updates the coefficients of an approximating function.
*   **Speed-Accuracy Trade-off:** More grid points mean higher accuracy but slower convergence. Smart grid choice (e.g., concentrating points where curvature is high) is essential."""
    },
    '03_Discrete_Continuous_DP.ipynb': {
        'lens': """# The Lens: Mixed Decisions

**What problem are we solving?**
Many economic problems involve both **discrete choices** (e.g., work/retire, buy/rent, default/repay) and **continuous choices** (e.g., how much to consume, how much to save). These "discrete-continuous" problems are ubiquitous in labor economics and corporate finance.

**Why this method?**
The presence of discrete choices introduces \"kinks\" or non-concavities in the value function, breaking standard derivative-based optimization methods. We need a specialized approach:
1.  **Conditional Value Functions:** Calculate the value of *each* discrete choice (e.g., $V_{work}$ and $V_{retire}$) assuming optimal continuous choices.
2.  **Upper Envelope:** The true value function is the maximum of these conditional values: $V(x) = \max(V_{work}(x), V_{retire}(x))$.

This notebook demonstrates how to handle these non-standard but critical optimization landscapes.""",
        'summary': """# Summary

Discrete-continuous problems model the most important decisions in life: career, housing, and default.

**Key Takeaways:**
*   **Conditional Maximization:** Solve the continuous problem for *each* discrete option first, then compare them.
*   **Non-Concavity:** Discrete choices destroy the global concavity of the value function. We must be careful with local optimizers.
*   **Thresholds:** The solution is often characterized by threshold values (e.g., a reservation wage or a default threshold) where the optimal discrete choice switches."""
    },
    '04_Estimation_and_Calibration.ipynb': {
        'lens': """# The Lens: From Theory to Reality

**What problem are we solving?**
A model without data is just a parable. To make economic models useful for policy analysis—whether it's predicting the effect of a tax cut or understanding inequality—we must choose their parameters so that they behave like the real world. This is the challenge of **Estimation and Calibration**.

In simple linear models, we can use Ordinary Least Squares (OLS). But modern dynamic models (like the Aiyagari model) are highly non-linear and have no closed-form solution, making standard econometric techniques impossible.

**Why this method?**
The solution is the **Simulated Method of Moments (SMM)**. If we can't derive the likelihood function, we can at least *simulate* the model. SMM asks: "What parameters make the simulated data look most like the real data?"

This notebook teaches you how to bridge the gap between elegant theory and messy data.""",
        'summary': """# Summary

Estimation transforms a theoretical toy into an empirical tool.

**Key Takeaways:**
*   **Calibration vs. Estimation:** Calibration often sets parameters based on external evidence (e.g., labor share from NIPA). Estimation picks parameters to minimize the distance between model and data moments.
*   **Identification:** You can only estimate a parameter if it actually changes the moments you are matching. Always check the "identification surface."
*   **Computational Cost:** Estimation requires solving the model hundreds of times. Efficient code (JIT, parallelization) is not optional; it is a requirement."""
    },
    '05_Optimal_Stopping_Problems.ipynb': {
        'lens': """# The Lens: The Economics of Waiting

**What problem are we solving?**
Timing is everything.
*   When should I sell this stock?
*   When should I accept a job offer?
*   When should a firm invest in a new factory?
These are **Optimal Stopping Problems**. The core trade-off is between the **current payoff** (taking the deal now) and the **option value of waiting** (the chance that a better deal comes along tomorrow).

**Why this method?**
These problems are a special class of dynamic programming where the choice is binary: Stop or Continue. The solution is characterized by a **reservation value** or threshold. If the state exceeds this threshold, you act; otherwise, you wait.
We will study the famous **McCall Search Model** and the theory of **Real Options**, which revolutionized corporate finance by treating investment opportunities as financial options.

This notebook quantifies the value of patience and the cost of uncertainty.""",
        'summary': """# Summary

Optimal stopping theory explains why hesitation can be rational.

**Key Takeaways:**
*   **Option Value:** Uncertainty creates value. The ability to wait and see is a "real option" that is lost once an irreversible decision is made.
*   **Reservation Rule:** The optimal policy is almost always a threshold rule (e.g., accept any wage $w > w^*$).
*   **Volatility:** Paradoxically, higher uncertainty often *increases* the value of waiting, delaying investment and prolonging unemployment."""
    },
    '06_Robust_Control.ipynb': {
        'lens': """# The Lens: Decision Making Under Deep Uncertainty

**What problem are we solving?**
Standard economics assumes agents know the true probability distribution of shocks (Rational Expectations). But in reality, agents face **ambiguity** or **Knightian Uncertainty**—they don't know the true model. They fear their model might be wrong.
How should a prudent central bank or investor act when they suspect their model is misspecified?

**Why this method?**
**Robust Control**, pioneered by Hansen and Sargent, models agents who assume the \"worst-case scenario.\" They play a game against a malevolent \"Nature\" that tries to twist the shocks to hurt them. The agent chooses a policy to maximize utility, while Nature chooses a perturbation to minimize it ($\max \min$).
This framework explains why agents might be cautious, hold excess precautionary savings, or demand high risk premiums, even if the "true" risk is low.

This notebook introduces the mathematics of fear and robustness.""",
        'summary': """# Summary

Robust control models agents who are not just risk-averse, but model-averse.

**Key Takeaways:**
*   **Risk vs. Ambiguity:** Risk is not knowing the outcome (rolling a die). Ambiguity is not knowing the odds (rolling a loaded die).
*   **Max-Min Utility:** Robust agents maximize their utility under the worst-case distortion of the model.
*   **Observational Equivalence:** Robustness often looks like high risk aversion. It provides an alternative explanation for the Equity Premium Puzzle."""
    },
    '07_Structural_Estimation.ipynb': {
        'lens': """# The Lens: Inferring the Unobservable

**What problem are we solving?**
We observe agents' choices (e.g., how many cars they buy), but we care about their underlying preferences (e.g., price elasticity, brand loyalty). **Structural Estimation** uses an economic model to infer these unobservable parameters from observed behavior. Unlike "reduced-form" econometrics which seeks correlations, structural estimation seeks the "deep parameters" that are invariant to policy changes (addressing the Lucas Critique).

**Why this method?**
We construct a model of the agent's decision-making process and estimate the parameters that maximize the likelihood of observing the actual choices in the data.
*   **Rust's Engine Replacement Model:** A classic example of estimating a dynamic discrete choice model.
*   **BLP (Berry-Levinsohn-Pakes):** The industry standard for estimating demand in differentiated product markets.

This notebook shows how to reverse-engineer the agent's mind from their actions.""",
        'summary': """# Summary

Structural estimation recovers the "deep" parameters of preferences and technology.

**Key Takeaways:**
*   **Policy Counterfactuals:** Only structural models can predict the effects of policies that have never been tried before (e.g., a merger between two specific firms).
*   **Computational Burden:** Structural estimation involves nested loops: an outer optimization loop for parameters and an inner fixed-point loop for the model solution.
*   **The Lucas Critique:** By estimating parameters that are invariant to policy (like utility functions), we avoid the pitfalls of reduced-form correlations."""
    },

    # --- Module 04: Macro Models ---
    '01_Job_Search.ipynb': {
        'lens': """# The Lens: Frictions in the Labor Market

**What problem are we solving?**
In a frictionless supply-and-demand model, there is no unemployment; wages adjust instantly to clear the market. But in the real world, finding a job takes time and effort. Workers are unemployed not because there are no jobs, but because it takes time to find the *right* job.
This is the domain of **Search and Matching Theory**, which won the Nobel Prize for Diamond, Mortensen, and Pissarides.

**Why this method?**
We model unemployment as a productive activity: searching for a better match.
*   **McCall Model:** A single worker searching for a wage.
*   **DMP Model:** Firms and workers searching for each other, with wages determined by bargaining.
These models explain the "Beveridge Curve" (the relationship between unemployment and vacancies) and the dynamics of the labor market over the business cycle.

This notebook builds the micro-foundations of unemployment.""",
        'summary': """# Summary

Unemployment is a dynamic equilibrium phenomenon, not just a market failure.

**Key Takeaways:**
*   **Reservation Wage:** The central decision rule. Workers accept jobs that pay more than their reservation wage and reject others.
*   **Frictions Matter:** Higher unemployment benefits or lower search efficiency increase the reservation wage, raising the equilibrium unemployment rate.
*   **Flows vs. Stocks:** The unemployment rate is a stock determined by the flows into and out of unemployment (job separation and job finding rates)."""
    },
    '02_Neoclassical_Growth.ipynb': {
        'lens': """# The Lens: The Long Run

**What problem are we solving?**
Why are some countries rich and others poor? Why do economies grow over time?
The **Neoclassical Growth Model** (Solow-Swan and Ramsey-Cass-Koopmans) provides the foundational framework for answering these questions. It strips the economy down to its barest essentials: capital accumulation, population growth, and technological progress.

**Why this method?**
This model serves as the benchmark for all modern macroeconomics. It teaches us:
*   **Capital Deepening:** How saving leads to more capital per worker.
*   **Steady State:** The long-run equilibrium where investment equals depreciation.
*   **Convergence:** Why poor countries should theoretically grow faster than rich ones (and why they sometimes don't).

This notebook explores the mechanics of growth and the transition to the steady state.""",
        'summary': """# Summary

Growth comes from accumulation in the short run, but only from innovation in the long run.

**Key Takeaways:**
*   **Diminishing Returns:** Capital accumulation cannot sustain growth forever. Eventually, the return on new capital falls to zero (in net terms).
*   **Technology is Key:** Long-run improvements in living standards must come from technological progress (Total Factor Productivity).
*   **The Golden Rule:** There is an optimal savings rate that maximizes consumption. Saving too much is just as bad as saving too little (Dynamic Inefficiency)."""
    },
    '03_RBC_Models.ipynb': {
        'lens': """# The Lens: Microfoundations of Aggregates

**What problem are we solving?**
Business cycles—the boom and bust of the economy—were traditionally analyzed using ad-hoc aggregate relationships (like IS-LM). The **Real Business Cycle (RBC)** revolution changed everything. It asked: "Can we explain recessions as the optimal response of rational agents to productivity shocks?"
RBC models build the macroeconomy from the ground up, starting with utility-maximizing households and profit-maximizing firms.

**Why this method?**
This is the first true **DSGE** (Dynamic Stochastic General Equilibrium) model.
*   **Dynamic:** Agents care about the future.
*   **Stochastic:** The economy is hit by random shocks.
*   **General Equilibrium:** All markets (labor, capital, goods) clear simultaneously.
Even if you disagree with the RBC premise (that recessions are efficient), the *methodology* is the standard language of modern macroeconomics.

This notebook builds, solves, and simulates the canonical RBC model.""",
        'summary': """# Summary

The RBC model established the methodology of modern macroeconomics: DSGE.

**Key Takeaways:**
*   **Propagation:** Even small, temporary shocks can have long-lasting effects due to capital accumulation.
*   **Comovement:** The model successfully explains why consumption, investment, and hours worked move together over the business cycle.
*   **The Limits:** The standard RBC model struggles to explain the volatility of hours worked and asset prices, motivating the addition of frictions (New Keynesian models)."""
    },
    '04_OLG_Models.ipynb': {
        'lens': """# The Lens: Generations and the Life Cycle

**What problem are we solving?**
The standard Ramsey model assumes an infinitely lived "representative agent." But in reality, people are born, work, retire, and die. Different generations coexist and trade with each other.
**Overlapping Generations (OLG)** models capture this life-cycle structure. They are essential for studying issues like Social Security, public debt, and demographic change.

**Why this method?**
OLG models reveal phenomena that infinite-horizon models miss:
*   **Dynamic Inefficiency:** The competitive equilibrium might have *too much* capital, because current generations don't care about the infinite future.
*   **The Role of Money:** In some OLG settings, fiat money can have positive value as a store of value between generations.
*   **Intergenerational Conflict:** Policy changes (like cutting pensions) create winners and losers across generations.

This notebook introduces the Diamond-Mortensen-Pissarides style OLG framework.""",
        'summary': """# Summary

OLG models remind us that the "long run" is made up of a sequence of short lives.

**Key Takeaways:**
*   **Life-Cycle Savings:** The primary motive for saving is to finance consumption in retirement.
*   **Breakdown of Ricardian Equivalence:** Government debt matters in OLG models. It can crowd out private capital accumulation.
*   **Bubbles:** OLG models provide a theoretical foundation for rational asset bubbles."""
    },
    '05_New_Keynesian_Models.ipynb': {
        'lens': """# The Lens: Prices, Frictions, and Monetary Policy

**What problem are we solving?**
The RBC model assumes prices adjust instantly. This implies monetary policy (printing money) has no effect on the real economy ("money neutrality").
But in the real world, central banks *do* affect output and employment. To capture this, **New Keynesian (NK)** models introduce **nominal rigidities**—sticky prices and wages.
Firms want to change prices, but they can't do so every day (e.g., due to "menu costs"). This friction gives monetary policy traction.

**Why this method?**
The NK model is the primary framework used by central banks around the world. It boils down to three equations:
1.  **IS Curve:** Euler equation (Demand).
2.  **Phillips Curve:** Inflation dynamics (Supply).
3.  **Taylor Rule:** Central bank policy rule.

This notebook builds the 3-equation NK model and analyzes the transmission of monetary shocks.""",
        'summary': """# Summary

New Keynesian models bridge the gap between flexible-price theory and sticky-price reality.

**Key Takeaways:**
*   **Non-Neutrality:** Because prices are sticky, changes in the nominal interest rate affect the real interest rate, driving consumption and investment.
*   **The Taylor Principle:** To stabilize the economy, the central bank must raise interest rates *more than one-for-one* with inflation.
*   **The Phillips Curve:** Inflation depends on *expected* future inflation and the output gap (marginal cost)."""
    },
    '06_Heterogeneous_Agent_Models.ipynb': {
        'lens': """# The Lens: Inequality in Macroeconomics

**What problem are we solving?**
Representative agent models (like RBC or NK) assume everyone is the same. They cannot talk about inequality, poverty, or the distribution of wealth.
**Heterogeneous Agent** models (like **Aiyagari-Bewley-Huggett**) populate the macroeconomy with millions of different households, each facing their own idiosyncratic income shocks (getting a raise, losing a job) and making their own saving decisions.

**Why this method?**
This framework allows us to ask distributional questions:
*   How does wealth inequality evolve?
*   Who suffers most from a recession?
*   Why are interest rates so low? (Precautionary savings).
The "state" of the economy is no longer just a few variables (K, L), but the entire **distribution** of wealth across the population.

This notebook implements the Aiyagari model, the workhorse of modern quantitative macroeconomics.""",
        'summary': """# Summary

Heterogeneity matters. The aggregate economy behaves differently when agents face uninsurable risk.

**Key Takeaways:**
*   **Precautionary Savings:** Agents save more than the standard model predicts to buffer against bad luck. This pushes the equilibrium interest rate down.
*   **Wealth Inequality:** Even if everyone has the same preferences, luck alone generates significant wealth inequality.
*   **Smoothing:** Aggregate consumption is smoother than individual consumption, but idiosyncratic risk breaks the "representative agent" logic."""
    },
    '08_Endogenous_Growth.ipynb': {
        'lens': """# The Lens: The Engines of Prosperity

**What problem are we solving?**
The Solow model predicts that growth stops in the long run (without exogenous magic). **Endogenous Growth Theory** seeks to explain growth from *within* the model.
It argues that economic policy (taxes, subsidies, R&D) can permanently affect the rate of growth, not just the level of income.

**Why this method?**
We explore two main engines of endogenous growth:
1.  **Human Capital (Lucas):** Education and skills accumulation.
2.  **Ideas and R&D (Romer):** The creation of new blueprints and technologies.
The key insight is **non-rivalry**: an idea can be used by everyone simultaneously without being depleted. This leads to increasing returns to scale, the secret sauce of sustained growth.

This notebook models the economics of ideas.""",
        'summary': """# Summary

Ideas are not like other goods. Their non-rivalry is the ultimate source of long-run growth.

**Key Takeaways:**
*   **Spillovers:** Knowledge creation has positive externalities. The private return to R&D is lower than the social return, justifying government subsidies.
*   **Scale Effects:** Larger economies (more researchers) should theoretically grow faster.
*   **Creative Destruction:** Growth often involves the replacement of old firms/technologies by new ones (Schumpeterian growth)."""
    }
}

def refactor_notebook(module_dir, filename, content):
    filepath = os.path.join(module_dir, filename)
    if not os.path.exists(filepath):
        print(f"Skipping {filename}: File not found in {module_dir}.")
        return

    print(f"Processing {filepath}...")
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            nb = nbformat.read(f, as_version=4)
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return

    # 1. Update TOC (Generic clean up)

    # 2. Inject Lens
    lens_injected = False
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            # Check for existing Lens/Intro
            if any(x in cell.source for x in ["# The Lens", "# Introduction", "### The Lens", "### Introduction"]):
                if "Table of Contents" not in cell.source:
                    cell.source = content['lens']
                    lens_injected = True
                    break

    if not lens_injected:
        # Insert after imports usually
        insert_idx = 2
        if insert_idx < len(nb.cells) and nb.cells[insert_idx].cell_type == 'code':
            insert_idx += 1
        nb.cells.insert(insert_idx, nbformat.v4.new_markdown_cell(content['lens']))

    # 3. Inject Summary
    summary_injected = False
    for cell in nb.cells:
        if cell.cell_type == 'markdown':
            if any(x in cell.source for x in ["# Summary", "### Summary", "## Summary", "### Conclusion"]):
                 if "[" not in cell.source:
                     cell.source = content['summary']
                     summary_injected = True
                     break

    if not summary_injected:
        nb.cells.append(nbformat.v4.new_markdown_cell(content['summary']))

    # 4. Standardize Headers
    for cell in nb.cells:
        if cell.cell_type == 'markdown' and "Exercises" in cell.source:
             if cell.source.strip().startswith("###"):
                 cell.source = cell.source.replace("###", "#", 1)

    # Save
    with open(filepath, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"  -> Success.")

def main():
    # Module 03
    for filename, content in CONTENT_MAP.items():
        if filename in [
            '01_Dynamic_Programming.ipynb',
            '02_DP_with_Continuous_States.ipynb',
            '03_Discrete_Continuous_DP.ipynb',
            '04_Estimation_and_Calibration.ipynb',
            '05_Optimal_Stopping_Problems.ipynb',
            '06_Robust_Control.ipynb',
            '07_Structural_Estimation.ipynb'
        ]:
            refactor_notebook('03-Economic-Modeling', filename, content)

        # Module 04
        if filename in [
            '01_Job_Search.ipynb',
            '02_Neoclassical_Growth.ipynb',
            '03_RBC_Models.ipynb',
            '04_OLG_Models.ipynb',
            '05_New_Keynesian_Models.ipynb',
            '06_Heterogeneous_Agent_Models.ipynb',
            '08_Endogenous_Growth.ipynb'
        ]:
            refactor_notebook('04-Macro-Models', filename, content)

if __name__ == "__main__":
    main()
