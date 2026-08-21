#!/usr/bin/env python3
"""Add narrowly scoped theory-summary blocks identified by the final audit.

The script is intentionally idempotent: each inserted block has a stable heading/marker
and is added only when absent. It supplements existing derivations; it does not replace
or claim to mechanically verify them.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BLOCKS: dict[str, list[str]] = {
    "02-Numerical-Methods/01_Linear_Algebra.ipynb": [
        """## Economic Interpretation: Why conditioning is an economic issue\n\nIn an estimated equilibrium system, a large condition number means that small sampling, calibration, or rounding errors in moments and coefficients can produce economically large changes in the recovered prices, quantities, or policy coefficients. Decompositions such as QR and SVD are therefore not only numerical conveniences: they diagnose weakly identified directions and distinguish economically meaningful variation from nearly redundant equations.""",
    ],
    "02-Numerical-Methods/06_Interpolation_and_Approximation.ipynb": [
        """## Economic Interpretation: Approximation error becomes policy error\n\nApproximation quality matters because value functions, policy rules, and equilibrium maps are repeatedly evaluated inside solvers. A small local interpolation error can alter an argmax, shift a simulated distribution, and then feed back into market clearing. Chebyshev nodes and sparse grids are useful precisely because they allocate approximation capacity where global polynomial error would otherwise become economically consequential.""",
    ],
    "02-Numerical-Methods/07_Numerical_Integration.ipynb": [
        """## Assumptions Behind the Quadrature Rules\n\nThe convergence statements in this notebook assume the integrand is finite on the integration domain and has the smoothness required by the chosen rule. Gaussian quadrature additionally assumes the weighted moments exist; Monte Carlo estimators require an integrable target and finite variance for the usual $N^{-1/2}$ error characterization. Heavy tails or singular endpoints therefore require transformation, specialized weights, or robust simulation rather than blind application of a textbook rule.""",
        """## Key Equations\n\n- **Generic expectation:** $\\mathbb{E}[g(X)] = \\int g(x) f(x)\\,dx$.\n- **Gauss quadrature:** $\\int_a^b f(x)w(x)\\,dx \\approx \\sum_{i=1}^{n} w_i f(x_i)$.\n- **Monte Carlo:** $\\hat I_N = N^{-1}\\sum_{i=1}^N g(X_i)$ with sampling error $O_p(N^{-1/2})$ under finite variance.\n- **Gauss-Hermite mapping:** use Hermite nodes and weights after transforming a Gaussian expectation to the $e^{-x^2}$ weight.""",
    ],
    "01-Foundations/22B_Complexity_in_Economic_Applications.ipynb": [
        """## Derivation: Why tensor-product state spaces explode\n\nSuppose each of $d$ state variables is discretized with $m$ grid points. A full tensor grid contains\n\n$$N(d,m)=m^d.$$\n\nIncreasing the dimension from $d$ to $d+1$ multiplies storage and one full-grid pass by $m$:\n\n$$\\frac{N(d+1,m)}{N(d,m)}=m.$$\n\nThus even an $O(N)$ Bellman update becomes $O(m^d)$ in the primitive resolution parameter. This is the computational form of the curse of dimensionality and explains why sparse grids, endogenous grids, simulation, and function approximation can change the feasible economic question rather than merely accelerate the same calculation.""",
    ],
    "04-Macro-Models/03B_RBC_Model_Solution.ipynb": [
        """## Key Equations\n\n- **Linear rational-expectations system:** $A\\,\\mathbb{E}_t x_{t+1}=B x_t + C\\varepsilon_{t+1}$.\n- **Generalized Schur form:** $Q^*AZ=S$, $Q^*BZ=T$, with generalized eigenvalues $\\lambda_i=T_{ii}/S_{ii}$.\n- **Blanchard-Kahn criterion:** the number of unstable generalized eigenvalues must equal the number of non-predetermined (jump) variables for a unique stable solution.\n- **Policy representation:** once stable/unstable blocks are separated, jump variables are linear functions of the predetermined state.""",
    ],
    "04-Macro-Models/04_OLG_Models.ipynb": [
        """## Key Equations\n\n- **Young household budget:** $c_{1,t}+s_t=w_t$.\n- **Old-age consumption:** $c_{2,t+1}=(1+r_{t+1})s_t$.\n- **Euler condition:** $u'(c_{1,t})=\\beta(1+r_{t+1})u'(c_{2,t+1})$.\n- **Capital accumulation:** next period's capital per worker is pinned down by current saving and cohort growth.\n- **Dynamic efficiency diagnostic:** over-accumulation is associated with a return on capital below the economy's relevant growth rate under the model's assumptions.""",
    ],
    "05-Micro-Models/01_Consumer_and_Producer_Theory.ipynb": [
        """## Key Equations\n\n- **Consumer problem:** $\\max_x u(x)$ subject to $p\\cdot x\\le m$.\n- **Marshallian demand FOC:** $\\nabla u(x^*)=\\lambda p$ for an interior optimum.\n- **Slutsky decomposition:** $\\partial x_i/\\partial p_j = \\partial h_i/\\partial p_j - x_j\\,\\partial x_i/\\partial m$.\n- **Roy's identity:** $x_i(p,m)=-V_{p_i}(p,m)/V_m(p,m)$.\n- **Shephard's lemma:** $h_i(p,u)=\\partial e(p,u)/\\partial p_i$.""",
    ],
    "05-Micro-Models/03_Game_Theory_and_Auctions.ipynb": [
        """## Key Equations\n\n- **Best response:** $BR_i(a_{-i})=\\arg\\max_{a_i} u_i(a_i,a_{-i})$.\n- **Nash equilibrium:** $a_i^*\\in BR_i(a_{-i}^*)$ for every player $i$.\n- **Mixed equilibrium:** each action in the support yields the same expected payoff.\n- **First-price symmetric bidding:** the equilibrium bid is obtained by trading off a higher winning probability against the lower surplus conditional on winning.\n- **Revenue equivalence:** under the standard independent-private-values assumptions, allocation-equivalent mechanisms with the same zero type yield the same expected revenue.""",
    ],
    "05-Micro-Models/05_Principal_Agent_Models.ipynb": [
        """## Key Equations\n\n- **Participation constraint:** expected agent utility under the contract must weakly exceed the outside option.\n- **Incentive compatibility:** the recommended action must maximize the agent's expected utility among feasible actions.\n- **Principal objective:** maximize expected output net of compensation subject to participation and incentive constraints.\n- **Risk-incentive trade-off:** stronger performance pay improves incentives but transfers more risk to a risk-averse agent.""",
    ],
    "05-Micro-Models/06_Information_Economics.ipynb": [
        """## Key Equations\n\n- **Bayes' rule:** $P(\\theta\\mid s)=P(s\\mid\\theta)P(\\theta)/P(s)$.\n- **Expected utility under information:** choose the action maximizing posterior expected payoff $\\mathbb{E}[u(a,\\theta)\\mid s]$.\n- **Value of information:** compare optimized expected utility with and without the signal; under free disposal of information the value is weakly non-negative.\n- **Screening/separation:** incentive constraints determine which types voluntarily select which contracts or signals.""",
    ],
    "06-Econometrics/01_Linear_Model_and_OLS.ipynb": [
        """## Key Equations\n\n- **Linear model:** $y=X\\beta+u$.\n- **OLS estimator:** $\\hat\\beta=(X'X)^{-1}X'y$ when $X$ has full column rank.\n- **Projection:** $\\hat y=P_Xy$ with $P_X=X(X'X)^{-1}X'$.\n- **FWL residualization:** the coefficient on a regressor block can be obtained by regressing residualized $y$ on residualized regressors.\n- **HC covariance:** sandwich estimators replace homoskedastic $\\sigma^2I$ with residual-based diagonal weighting.""",
    ],
    "06-Econometrics/02A_MLE_Principles_and_Geometry.ipynb": [
        """## Key Equations\n\n- **Likelihood:** $L(\\theta;y)=\\prod_i f(y_i\\mid\\theta)$.\n- **Log-likelihood:** $\\ell(\\theta)=\\sum_i \\log f(y_i\\mid\\theta)$.\n- **Score:** $s(\\theta)=\\nabla_\\theta\\ell(\\theta)$.\n- **Observed information:** $-\\nabla_\\theta^2\\ell(\\theta)$.\n- **Asymptotic normality:** under regularity conditions, $\\sqrt{n}(\\hat\\theta-\\theta_0)$ converges to a centered normal distribution with covariance equal to the inverse Fisher information.""",
    ],
    "06-Econometrics/07_Synthetic_Control_Methods.ipynb": [
        """## Key Equations\n\n- **Synthetic counterfactual:** $\\hat Y_{1t}(0)=\\sum_{j=2}^{J+1} w_jY_{jt}$ for post-treatment $t$.\n- **Convex donor weights:** $w_j\\ge0$ and $\\sum_j w_j=1$.\n- **Pre-treatment fit:** choose $w$ to minimize the discrepancy between treated and synthetic predictors/outcomes over the pre-period.\n- **Estimated effect:** $\\hat\\tau_t=Y_{1t}-\\hat Y_{1t}(0)$.\n- **Placebo inference:** compare the treated unit's post/pre gap ratio or trajectory with analogous reassignments to donor units.""",
    ],
    "06-Econometrics/13_Modern_Causal_Frontiers_SDID.ipynb": [
        """## Economic Interpretation: Balancing units and time\n\nSynthetic Difference-in-Differences treats identification as a two-sided balancing problem. Unit weights construct a control combination that resembles treated units before treatment, while time weights emphasize pre-periods that best predict the post-period contrast. Economically, the estimator relaxes the idea that one untreated average or one uniform pre-period trend must represent the counterfactual; it instead asks which comparison units and which historical periods carry the most credible counterfactual information under the maintained design assumptions.""",
    ],
    "07-Machine-Learning/17_Causal_ML.ipynb": [
        """## Key Equations\n\n- **Partially linear model:** $Y=\\theta_0 D+g_0(X)+\\varepsilon$, $D=m_0(X)+v$.\n- **Orthogonal score:** $\\psi(W;\\theta,\\eta)=(D-m(X))[Y-g(X)-\\theta(D-m(X))]$.\n- **Neyman orthogonality:** the first-order derivative of the population moment with respect to nuisance perturbations vanishes at the truth.\n- **Cross-fitting:** nuisance functions are learned out of fold so the score for each observation is evaluated using models that did not train on that observation.""",
    ],
    "07-Machine-Learning/18_Natural_Language_Processing.ipynb": [
        """## Key Equations\n\n- **TF-IDF:** $\\operatorname{tfidf}(t,d)=\\operatorname{tf}(t,d)\\log(N/\\operatorname{df}(t))$.\n- **Skip-gram idea:** embeddings are learned so words predict nearby context words.\n- **Cosine similarity:** $\\cos(x,y)=x'y/(\\|x\\|\\,\\|y\\|)$.\n- **Text prediction:** an economic target can be modeled from document representations only with a time-aware train/test split when the intended use is forecasting.""",
    ],
    "08-Time-Series/07_Nonlinear_Time_Series_and_Particle_Filters.ipynb": [
        """## Economic Interpretation: Filtering is real-time inference\n\nA particle filter converts a nonlinear state-space model into a sequence of empirical posterior distributions. In macro and finance the latent state can represent volatility, a regime, productivity, or another economically meaningful object that is never observed directly. The resampling step concentrates computational effort on state paths that remain plausible after new data arrive, so filtering uncertainty is part of the economic inference rather than a numerical nuisance to hide.""",
    ],
    "09-Finance/06_High_Frequency_Data.ipynb": [
        """## Key Equations\n\n- **Log return:** $r_{t,i}=\\log P_{t,i}-\\log P_{t,i-1}$.\n- **Realized variance:** $RV_t=\\sum_i r_{t,i}^2$ over intraday intervals.\n- **Bid-ask spread:** quoted spread is ask minus bid; effective spread uses the trade price relative to the prevailing midpoint.\n- **Microstructure caution:** as sampling becomes too fine, bid-ask bounce and price discreteness contaminate naive realized-variance estimates.""",
    ],
    "09-Finance/07_Financial_Frictions_BGG.ipynb": [
        """## Key Equations\n\n- **External finance premium:** the borrowing rate exceeds the risk-free rate by a spread that rises as borrower net worth falls.\n- **Net-worth feedback:** adverse shocks reduce entrepreneurial net worth, widen financing spreads, compress investment, and amplify the original shock.\n- **Linearized equilibrium system:** the BGG block is solved jointly with aggregate dynamics, so stability is a generalized-eigenvalue problem rather than an isolated spread equation.""",
    ],
    "10-Specialized-Models/04_Climate_Macro_Integrated_Assessment_DICE.ipynb": [
        """## Economic Interpretation: The carbon price is an intertemporal shadow value\n\nIn an integrated assessment model, an additional unit of emissions raises future atmospheric carbon, temperature, and damages while current abatement uses resources today. The social cost of carbon is therefore a shadow value that prices the discounted marginal welfare damage of emissions along the model's transition path. Its magnitude is jointly determined by climate dynamics, damages, preferences, growth, and the assumed policy instrument; it is not a universal physical constant.""",
    ],
    "Appendix/T4_Replication_Card_Krueger_1994.ipynb": [
        """## Key Equations\n\n- **Two-by-two DiD:** $\\widehat{ATT}=(\\bar Y_{NJ,post}-\\bar Y_{NJ,pre})-(\\bar Y_{PA,post}-\\bar Y_{PA,pre})$.\n- **Regression form:** $Y_{it}=\\alpha+\\beta NJ_i+\\gamma Post_t+\\delta(NJ_i\\times Post_t)+u_{it}$, where $\\delta$ equals the two-by-two DiD in the saturated group-time design.\n- **Identification:** the causal reading of $\\delta$ requires a credible parallel-trends counterfactual; two waves alone cannot test pre-treatment trend equality.""",
    ],
    "Appendix/T5_Replication_Fama_French_Five_Factor.ipynb": [
        """## Key Equations\n\n- **Five-factor regression:** $R_{i,t}-R_{f,t}=\\alpha_i+\\beta_M MKT_t+\\beta_S SMB_t+\\beta_H HML_t+\\beta_R RMW_t+\\beta_C CMA_t+\\varepsilon_{i,t}$.\n- **Pricing diagnostic:** an economically small and statistically weak $\\alpha_i$ is consistent with the factors spanning that portfolio's average excess return over the evaluated sample.\n- **Scope:** this lab uses the bundled 2015–2022 overlap and is a reproduction of the factor-model workflow, not the exact sample of Fama and French (2015).""",
    ],
}


def text(cell: dict) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else str(source)


def stable_id(path: str, block: str) -> str:
    return hashlib.sha1(f"{path}\n{block}".encode()).hexdigest()[:8]


def insertion_index(cells: list[dict]) -> int:
    for i, cell in enumerate(cells):
        if cell.get("cell_type") != "markdown":
            continue
        if re.search(r"^#{1,4}\s+(?:Summary|Summary & Key Takeaways|References|Further Reading)\b", text(cell), re.I | re.M):
            return i
    return len(cells)


def main() -> int:
    changed = 0
    added = 0
    for rel, blocks in BLOCKS.items():
        path = ROOT / rel
        nb = json.loads(path.read_text(encoding="utf-8"))
        cells = nb.get("cells", [])
        joined = "\n\n".join(text(c) for c in cells if c.get("cell_type") == "markdown")
        new_blocks: list[dict] = []
        for block in blocks:
            heading = block.splitlines()[0].strip()
            if heading in joined:
                continue
            new_blocks.append({
                "cell_type": "markdown",
                "id": stable_id(rel, heading),
                "metadata": {},
                "source": [line + "\n" for line in block.splitlines()],
            })
        if not new_blocks:
            continue
        idx = insertion_index(cells)
        cells[idx:idx] = new_blocks
        path.write_text(json.dumps(nb, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
        changed += 1
        added += len(new_blocks)
    print(f"Enriched {changed} notebooks with {added} audit-targeted theory blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
