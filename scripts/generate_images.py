#!/usr/bin/env python3
"""
Image Generation Script for Computational Economics Course
Generates all educational diagrams and saves them to the images/ folder
"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Configuration
IMAGE_BASE = Path(__file__).parent.parent / "images"
DPI = 300
FIGSIZE = (10, 7)
plt.style.use('seaborn-v0_8-whitegrid')

def setup_dirs():
    """Create all necessary image directories"""
    dirs = [
        "foundations/git",
        "foundations/sets",
        "foundations/complexity",
        "numerical_methods/phase_diagrams",
        "numerical_methods/optimization",
        "numerical_methods/integration",
        "machine_learning/architectures",
        "machine_learning/rl",
        "machine_learning/concepts",
        "finance/options",
        "finance/portfolio",
        "finance/risk",
        "econometrics/causal",
        "econometrics/time_series",
        "micro_macro/micro",
        "micro_macro/macro"
    ]
    for d in dirs:
        (IMAGE_BASE / d).mkdir(parents=True, exist_ok=True)
    print(f"✓ Created {len(dirs)} directories")

# ============================================================================
# PHASE DIAGRAMS
# ============================================================================

def generate_phase_diagrams():
    """Generate enhanced phase diagrams with color-coded manifolds"""
    print("Generating phase diagrams...")

    # Lotka-Volterra Predator-Prey
    fig, ax = plt.subplots(figsize=FIGSIZE)

    a, b, c, d = 1.5, 0.1, 3.0, 0.1
    R_star, F_star = c/d, a/b

    R_grid = np.linspace(0, 60, 30)
    F_grid = np.linspace(0, 40, 30)
    R, F = np.meshgrid(R_grid, F_grid)

    R_dot = a*R - b*R*F
    F_dot = -c*F + d*R*F

    # Streamplot with velocity coloring
    velocity = np.sqrt(R_dot**2 + F_dot**2)
    ax.streamplot(R, F, R_dot, F_dot, color=velocity,
                 cmap='viridis', density=1.5, linewidth=1.2)

    # Nullclines
    ax.axhline(F_star, color='red', ls='--', lw=2.5,
              label='R-nullcline ($\\dot{R}=0$)', alpha=0.8)
    ax.axvline(R_star, color='blue', ls='--', lw=2.5,
              label='F-nullcline ($\\dot{F}=0$)', alpha=0.8)

    # Steady state
    ax.plot(R_star, F_star, 'ko', markersize=15,
           markeredgewidth=2, markeredgecolor='white',
           label='Steady State', zorder=10)

    ax.set_xlabel('Prey Population (R)', fontsize=12)
    ax.set_ylabel('Predator Population (F)', fontsize=12)
    ax.set_title('Lotka-Volterra Predator-Prey Dynamics',
                fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(IMAGE_BASE / "images\png\lotka_volterra.png",
               dpi=DPI, bbox_inches='tight')
    plt.close()

    # RCK Model with Saddle Path
    fig, ax = plt.subplots(figsize=FIGSIZE)

    # Parameters
    alpha, delta, rho, n, g = 0.3, 0.05, 0.02, 0.01, 0.02
    k_star = ((rho + delta) / alpha)**(1/(alpha-1))
    c_star = k_star**alpha - (n + g + delta)*k_star

    k_grid = np.linspace(0.1, k_star*1.5, 30)
    c_grid = np.linspace(0.1, c_star*1.5, 30)
    K, C = np.meshgrid(k_grid, c_grid)

    # System dynamics
    K_dot = K**alpha - C - (n + g + delta)*K
    C_dot = (C/rho) * (alpha * K**(alpha-1) - delta - rho)

    velocity = np.sqrt(K_dot**2 + C_dot**2)
    ax.streamplot(K, C, K_dot, C_dot, color=velocity,
                 cmap='plasma', density=1.3, linewidth=1.2)

    # k-nullcline
    c_nullcline = k_grid**alpha - (n + g + delta)*k_grid
    ax.plot(k_grid, c_nullcline, 'b-', lw=2.5,
           label='$\\dot{k}=0$ nullcline', alpha=0.8)

    # c-nullcline
    ax.axvline(k_star, color='r', ls='--', lw=2.5,
              label='$\\dot{c}=0$ nullcline', alpha=0.8)

    # Saddle path (approximation)
    k_saddle = np.linspace(k_star*0.3, k_star*1.2, 100)
    c_saddle = c_star * (k_saddle/k_star)**0.5  # Simplified saddle path
    ax.plot(k_saddle, c_saddle, 'g-', lw=3.5,
           label='Stable Manifold (Saddle Path)',
           alpha=0.9, zorder=10)

    # Unstable paths
    for offset in [-0.1, 0.1]:
        c_unstable = c_saddle + offset*c_star
        c_unstable = np.clip(c_unstable, 0, c_star*1.5)
        ax.plot(k_saddle, c_unstable, 'm--', lw=2,
               alpha=0.6, label='Unstable Path' if offset==-0.1 else '')

    # Steady state
    ax.plot(k_star, c_star, 'ko', markersize=15,
           markeredgewidth=2, markeredgecolor='white',
           label='Steady State', zorder=10)

    ax.set_xlabel('Capital per Capita (k)', fontsize=12)
    ax.set_ylabel('Consumption per Capita (c)', fontsize=12)
    ax.set_title('Ramsey-Cass-Koopmans Model Phase Diagram',
                fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=9)
    ax.set_xlim([0, k_star*1.5])
    ax.set_ylim([0, c_star*1.5])
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(IMAGE_BASE / "images\png\rck_model.png",
               dpi=DPI, bbox_inches='tight')
    plt.close()

    print("  ✓ Generated 2 phase diagrams")

# ============================================================================
# OPTION PAYOFFS
# ============================================================================

def generate_option_diagrams():
    """Generate professional option payoff diagrams"""
    print("Generating option diagrams...")

    K = 100  # Strike price
    S_range = np.linspace(50, 150, 200)

    # Call and Put Payoffs
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Call Option
    call_payoff = np.maximum(S_range - K, 0)
    premium = 5
    call_profit = call_payoff - premium

    ax1.fill_between(S_range, 0, call_profit, where=(call_profit>=0),
                     alpha=0.3, color='green', label='Profit Zone')
    ax1.fill_between(S_range, call_profit, 0, where=(call_profit<0),
                     alpha=0.3, color='red', label='Loss Zone')
    ax1.plot(S_range, call_profit, 'b-', lw=2.5, label='P&L')
    ax1.axhline(0, color='black', lw=1, ls='--', alpha=0.5)
    ax1.axvline(K, color='gray', lw=1.5, ls='--',
               label=f'Strike K={K}', alpha=0.7)

    ax1.set_xlabel('Stock Price at Expiration ($S_T$)', fontsize=11)
    ax1.set_ylabel('Profit/Loss', fontsize=11)
    ax1.set_title('Long Call Option', fontsize=13, fontweight='bold')
    ax1.legend(loc='upper left', fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Put Option
    put_payoff = np.maximum(K - S_range, 0)
    put_profit = put_payoff - premium

    ax2.fill_between(S_range, 0, put_profit, where=(put_profit>=0),
                     alpha=0.3, color='green', label='Profit Zone')
    ax2.fill_between(S_range, put_profit, 0, where=(put_profit<0),
                     alpha=0.3, color='red', label='Loss Zone')
    ax2.plot(S_range, put_profit, 'darkorange', lw=2.5, label='P&L')
    ax2.axhline(0, color='black', lw=1, ls='--', alpha=0.5)
    ax2.axvline(K, color='gray', lw=1.5, ls='--',
               label=f'Strike K={K}', alpha=0.7)

    ax2.set_xlabel('Stock Price at Expiration ($S_T$)', fontsize=11)
    ax2.set_ylabel('Profit/Loss', fontsize=11)
    ax2.set_title('Long Put Option', fontsize=13, fontweight='bold')
    ax2.legend(loc='upper right', fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(IMAGE_BASE / "images\png\call_put_payoffs.png",
               dpi=DPI, bbox_inches='tight')
    plt.close()

    # Iron Condor
    fig, ax = plt.subplots(figsize=(12, 7))

    K1, K2, K3, K4 = 90, 95, 105, 110
    P1, P2, P3, P4 = 2, 4, 4, 2

    put1 = np.maximum(K1 - S_range, 0) - P1  # Short put
    put2 = -(np.maximum(K2 - S_range, 0) - P2)  # Long put
    call1 = -(np.maximum(S_range - K3, 0) - P3)  # Long call
    call2 = np.maximum(S_range - K4, 0) - P4  # Short call

    total = put1 + put2 + call1 + call2

    ax.fill_between(S_range, 0, total, where=(total>=0),
                    alpha=0.3, color='green', label='Profit Zone')
    ax.fill_between(S_range, total, 0, where=(total<0),
                    alpha=0.3, color='red', label='Loss Zone')
    ax.plot(S_range, total, 'purple', lw=3, label='Iron Condor P&L')
    ax.axhline(0, color='black', lw=1, ls='--', alpha=0.5)

    for K, label in [(K1, 'K1'), (K2, 'K2'), (K3, 'K3'), (K4, 'K4')]:
        ax.axvline(K, color='gray', lw=1, ls=':', alpha=0.6)
        ax.text(K, ax.get_ylim()[1]*0.9, label, ha='center', fontsize=9)

    ax.set_xlabel('Stock Price at Expiration', fontsize=12)
    ax.set_ylabel('Profit/Loss', fontsize=12)
    ax.set_title('Iron Condor Strategy', fontsize=14, fontweight='bold')
    ax.legend(loc='upper right', fontsize=10)
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(IMAGE_BASE / "images\png\iron_condor.png",
               dpi=DPI, bbox_inches='tight')
    plt.close()

    print("  ✓ Generated 2 option diagrams")

# ============================================================================
# BIG-O COMPLEXITY
# ============================================================================

def generate_complexity_charts():
    """Generate Big-O complexity comparison charts"""
    print("Generating complexity charts...")

    fig, ax = plt.subplots(figsize=(12, 8))

    n = np.linspace(1, 100, 500)

    complexities = {
        'O(1)': np.ones_like(n),
        'O(log n)': np.log2(n),
        'O(n)': n,
        'O(n log n)': n * np.log2(n),
        'O(n²)': n**2,
        'O(2ⁿ)': 2**np.minimum(n/10, 10)  # Scale down for visibility
    }

    colors = ['green', 'lime', 'yellow', 'orange', 'red', 'darkred']

    for (name, values), color in zip(complexities.items(), colors):
        ax.plot(n, values, label=name, lw=2.5, color=color, alpha=0.8)

    ax.set_xlabel('Input Size (n)', fontsize=13)
    ax.set_ylabel('Operations', fontsize=13)
    ax.set_title('Algorithm Complexity Comparison (Big-O Notation)',
                fontsize=15, fontweight='bold')
    ax.legend(loc='upper left', fontsize=11, framealpha=0.9)
    ax.set_ylim([0, 200])
    ax.grid(True, alpha=0.3, which='both', ls='-', linewidth=0.5)
    ax.set_axisbelow(True)

    # Add background color zones
    ax.axhspan(0, 50, alpha=0.1, color='green', zorder=0)
    ax.axhspan(50, 100, alpha=0.1, color='yellow', zorder=0)
    ax.axhspan(100, 200, alpha=0.1, color='red', zorder=0)

    ax.text(95, 25, 'Good', fontsize=10, ha='right',
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.7))
    ax.text(95, 75, 'Fair', fontsize=10, ha='right',
           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
    ax.text(95, 150, 'Poor', fontsize=10, ha='right',
           bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.7))

    plt.tight_layout()
    plt.savefig(IMAGE_BASE / "images\png\big_o_chart.png",
               dpi=DPI, bbox_inches='tight')
    plt.close()

    print("  ✓ Generated complexity chart")

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    print("\\n" + "="*70)
    print("IMAGE GENERATION SCRIPT FOR COMPUTATIONAL ECONOMICS")
    print("="*70 + "\\n")

    setup_dirs()
    print()

    generate_phase_diagrams()
    generate_option_diagrams()
    generate_complexity_charts()

    print("\\n" + "="*70)
    print("✓ All images generated successfully!")
    print(f"✓ Images saved to: {IMAGE_BASE}")
    print("="*70 + "\\n")

if __name__ == "__main__":
    main()