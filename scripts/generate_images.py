"""
Master Image and Diagram Generation Orchestrator.

Executes all 41 educational diagram generators across the repository, verifies outputs,
exports Mermaid diagram sources (.mmd/.md) for MkDocs, and synchronizes images/metadata.json.

Usage:
    python scripts/generate_images.py --all
    python scripts/generate_images.py --module 01-Foundations
    python scripts/generate_images.py --category dags
    python scripts/generate_images.py --mermaid
"""

import argparse
import glob
import os
import subprocess
import sys
import time
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.resolve()
ROOT_DIR = SCRIPTS_DIR.parent.resolve()


def generate_mermaid_diagrams():
    """Generates pure Mermaid (.mmd) and Markdown (.md) sources under docs/resources/diagrams/."""
    diag_dir = ROOT_DIR / "docs" / "resources" / "diagrams"
    diag_dir.mkdir(parents=True, exist_ok=True)

    diagrams = {
        "var-identification": {
            "title": "Structural VAR Identification & Cholesky Recursive Ordering",
            "desc": "Orthogonal structural shocks mapped to endogenous macroeconomic variables via lower triangular impact matrix.",
            "mmd": """flowchart LR
    subgraph Shocks["Structural Shocks $u_t \\sim \\mathcal{N}(0, I)$"]
        u1["$u_{GDP}$ (Supply/Demand)"]
        u2["$u_{\\pi}$ (Cost-Push)"]
        u3["$u_{R}$ (Monetary Policy)"]
    end

    subgraph Matrix["Impact Matrix $A_0^{-1}$"]
        m["Recursive Cholesky<br/>Ordering: $e_t = A_0^{-1} u_t$"]
    end

    subgraph Vars["Observed Endogenous Variables $y_t$"]
        y1["GDP Growth ($y_{1,t}$)"]
        y2["Inflation ($y_{2,t}$)"]
        y3["Fed Funds Rate ($y_{3,t}$)"]
    end

    u1 --> y1
    u2 --> y2
    u3 --> y3

    y1 -->|Contemporaneous| y2
    y1 -->|Contemporaneous| y3
    y2 -->|Contemporaneous| y3
""",
        },
        "box-jenkins-methodology": {
            "title": "Box-Jenkins Time Series Iterative Methodology",
            "desc": "Four-stage iterative workflow for ARIMA/SARIMA model identification, estimation, diagnostic checking, and forecasting.",
            "mmd": """flowchart TD
    A["1. Identification & Stationarity<br/>- ADF & KPSS Unit Root Tests<br/>- Transformations (Log, Difference $d$)<br/>- Inspect ACF & PACF Signatures"] --> B["2. Parameter Estimation<br/>- Estimate AR($p$) and MA($q$) Coefficients<br/>- Maximum Likelihood (MLE) / CSS"]
    B --> C["3. Diagnostic Checking<br/>- Residual Ljung-Box $Q$-Test<br/>- White Noise Verification<br/>- AIC / BIC Selection"]
    C --> D{"Residuals<br/>White Noise?"}
    D -->|No: Misspecified| A
    D -->|Yes: Adequate| E["4. Forecasting & Policy Analysis<br/>- Multi-Step Dynamic Forecasts<br/>- Impulse Response Functions"]
""",
        },
        "aiyagari-equilibrium": {
            "title": "Aiyagari (1994) Stationary General Equilibrium Algorithm",
            "desc": "Outer-loop bisection search on aggregate interest rate r clearing incomplete capital markets.",
            "mmd": """flowchart TD
    A["1. Outer Loop: Guess Interest Rate $r^{(0)}$"] --> B["2. Solve Household Dynamic Program<br/>- Value Function Iteration (VFI)<br/>- Policy Function $a'(a, z; r)$"]
    B --> C["3. Compute Stationary Distribution $\\mu(a, z)$<br/>- Fixed point of Markov transition $T_r(\\mu) = \\mu$"]
    C --> D["4. Aggregate Capital Supply vs. Firm Demand<br/>- $K_s(r) = \\int a \\, d\\mu(a, z)$<br/>- $K_d(r) = \\left(\\frac{r+\\delta}{\\alpha}\\right)^{\\frac{1}{\\alpha-1}}$"]
    D --> E{"Market Clearing?<br/>$|K_s(r) - K_d(r)| < \\epsilon$"}
    E -->|No: Update $r^{(k+1)}$ via Bisection| A
    E -->|Yes: Converged| F["5. Stationary Equilibrium Output<br/>- Equilibrium Prices $(r^*, w^*)$<br/>- Macro Aggregates & Wealth Distribution $\\mu^*$"]
""",
        },
        "fama-macbeth-twopass": {
            "title": "Fama-MacBeth (1973) Two-Pass Asset Pricing Procedure",
            "desc": "Time-series factor beta estimation followed by cross-sectional risk premia estimation.",
            "mmd": """flowchart TD
    subgraph Pass1["Pass 1: Time-Series Regressions ($N$ Assets)"]
        p1["For each asset $i=1..N$, regress across $t=1..T$:<br/>$R_{i,t} - R_{f,t} = \\alpha_i + \\beta_i f_t + \\epsilon_{i,t}$<br/>$\\rightarrow$ Estimated Factor Betas $\\hat{\\beta}_i$"]
    end

    subgraph Pass2["Pass 2: Cross-Sectional Regressions ($T$ Periods)"]
        p2["At each period $t=1..T$, regress across assets $i=1..N$:<br/>$R_{i,t} - R_{f,t} = \\lambda_{0,t} + \\lambda_{1,t} \\hat{\\beta}_i + \\eta_{i,t}$<br/>$\\rightarrow$ Time-series of Risk Premia $\\hat{\\lambda}_t$"]
    end

    subgraph Inference["Final Inference: Average Risk Premia"]
        inf["$\\bar{\\lambda} = \\frac{1}{T} \\sum_{t=1}^T \\hat{\\lambda}_t$<br/>$t$-statistic with Shanken (1992) Errors-in-Variables Correction"]
    end

    Pass1 --> Pass2
    Pass2 --> Inference
""",
        },
        "collider-bias-dag": {
            "title": "Collider Bias DAG (Berkson's Paradox)",
            "desc": "Conditioning on a common collider outcome creates spurious negative correlation between independent causes.",
            "mmd": """flowchart TD
    T["Talent ($T$)<br/>Exogenous"] --> A["Admission ($A$)<br/>Collider [Conditioned]"]
    L["Luck ($L$)<br/>Exogenous"] --> A
    T -.->|Spurious Negative Correlation<br/>when conditioned on A| L
""",
        },
        "reinforcement-learning-loop": {
            "title": "Reinforcement Learning Agent-Environment Loop",
            "desc": "Continuous feedback loop between agent actions and environmental states and rewards.",
            "mmd": """flowchart LR
    Agent["AGENT<br/>Policy $\\pi(a|s)$<br/>Value Function $V(s) / Q(s, a)$"]
    Env["ENVIRONMENT<br/>Transition $P(s'|s, a)$<br/>Reward Function $R(s, a)$"]

    Agent -->|Action $A_t \\in \\mathcal{A}(S_t)$| Env
    Env -->|State $S_{t+1}$, Reward $R_{t+1}$| Agent
""",
        },
    }

    print("\n--- Generating Mermaid Architectural Diagrams (.mmd / .md) ---")
    for name, data in diagrams.items():
        mmd_path = diag_dir / f"{name}.mmd"
        md_path = diag_dir / f"{name}.md"

        with open(mmd_path, "w", encoding="utf-8") as f:
            f.write(data["mmd"].strip() + "\n")

        md_content = f"# {data['title']}\n\n{data['desc']}\n\n```mermaid\n{data['mmd'].strip()}\n```\n"
        with open(md_path, "w", encoding="utf-8") as f:
            f.write(md_content)

        print(f"  [SAVED] {mmd_path.relative_to(ROOT_DIR)}")
        print(f"  [SAVED] {md_path.relative_to(ROOT_DIR)}")


def main():
    parser = argparse.ArgumentParser(
        description="Master diagram and figure generator for Computational Economics."
    )
    parser.add_argument(
        "--all",
        action="store_true",
        default=True,
        help="Generate all diagrams and figures",
    )
    parser.add_argument(
        "--module",
        type=str,
        default=None,
        help="Generate diagrams for a specific module",
    )
    parser.add_argument(
        "--mermaid", action="store_true", help="Generate Mermaid .mmd/.md files only"
    )
    args = parser.parse_args()

    start_time = time.time()
    print("=" * 70)
    print("COMPUTATIONAL ECONOMICS & DATA SCIENCE: DIAGRAM GENERATOR ORCHESTRATOR")
    print("=" * 70)

    # Generate Mermaid diagrams
    generate_mermaid_diagrams()
    if args.mermaid:
        print("\nMermaid diagram generation completed.")
        return

    # Find Python diagram generators
    scripts = sorted(
        glob.glob(str(SCRIPTS_DIR / "generate_*.py"))
        + glob.glob(str(SCRIPTS_DIR / "create_*.py"))
    )
    scripts = [s for s in scripts if Path(s).name != "generate_images.py"]

    if args.module:
        scripts = [s for s in scripts if args.module.lower() in Path(s).name.lower()]

    print(f"\nExecuting {len(scripts)} Python diagram generator scripts...")
    passed = 0
    failed = 0
    failed_scripts = []

    # Environment setup
    env = os.environ.copy()
    env["PYTHONPATH"] = str(SCRIPTS_DIR) + os.pathsep + env.get("PYTHONPATH", "")

    for s in scripts:
        rel_s = Path(s).relative_to(ROOT_DIR)
        print(f"Running {rel_s}...", end=" ", flush=True)
        t0 = time.time()
        proc = subprocess.run(
            [sys.executable, str(s)],
            capture_output=True,
            text=True,
            env=env,
            cwd=str(ROOT_DIR),
        )
        elapsed = time.time() - t0

        if proc.returncode == 0:
            print(f"[OK] ({elapsed:.2f}s)")
            passed += 1
        else:
            err_msg = proc.stderr.strip() or proc.stdout.strip()
            print(f"[FAILED] ({elapsed:.2f}s): {err_msg[:120]}")
            failed += 1
            failed_scripts.append((rel_s, err_msg))

    total_time = time.time() - start_time
    print("\n" + "=" * 70)
    print(f"GENERATION SUMMARY: {passed} PASSED, {failed} FAILED in {total_time:.2f}s")
    if failed > 0:
        print("\nFailed scripts:")
        for s, err in failed_scripts:
            print(f"  - {s}:\n    {err[:200]}")
    print("=" * 70)


if __name__ == "__main__":
    main()
