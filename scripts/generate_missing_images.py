"""Generate missing finance and econometrics diagrams."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle
import numpy as np

# Set style
plt.style.use('seaborn-v0_8-darkgrid')

def create_bgg_accelerator():
    """Create BGG accelerator diagram."""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # Title
    ax.text(5, 9.5, 'Bernanke-Gertler-Gilchrist Financial Accelerator',
            ha='center', fontsize=16, fontweight='bold')

    # Boxes
    boxes = [
        ('Technology\nShock', 5, 7.5, 'lightblue'),
        ('Output ↑', 2, 6, 'lightgreen'),
        ('Firm Net Worth ↑', 8, 6, 'lightgreen'),
        ('External Finance\nPremium ↓', 5, 4.5, 'yellow'),
        ('Investment ↑', 2, 3, 'lightcoral'),
        ('Capital ↑', 8, 3, 'lightcoral'),
        ('Amplification', 5, 1.5, 'orange'),
    ]

    for text, x, y, color in boxes:
        box = FancyBboxPatch((x-0.8, y-0.3), 1.6, 0.6,
                              boxstyle="round,pad=0.1",
                              edgecolor='black', facecolor=color, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=10, fontweight='bold')

    # Arrows
    arrows = [
        (5, 7.2, 2.5, 6.3), (5, 7.2, 7.5, 6.3),
        (2.5, 5.7, 2.5, 3.3), (7.5, 5.7, 7.5, 3.3),
        (2.8, 6, 4.2, 4.8), (7.2, 6, 5.8, 4.8),
        (2.5, 2.7, 4.2, 1.8), (7.5, 2.7, 5.8, 1.8),
    ]

    for x1, y1, x2, y2 in arrows:
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                arrowstyle='->', mutation_scale=20,
                                linewidth=2, color='darkblue')
        ax.add_patch(arrow)

    plt.tight_layout()
    plt.savefig('images/png/bgg_accelerator.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Created bgg_accelerator.png')

def create_cml_sml_distinction():
    """Create CML vs SML diagram."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # CML
    sigma = np.linspace(0, 0.3, 100)
    rf = 0.02
    mu_m = 0.10
    sigma_m = 0.20
    cml = rf + (mu_m - rf) / sigma_m * sigma

    ax1.plot(sigma, cml, 'b-', linewidth=2, label='CML')
    ax1.scatter([0, sigma_m], [rf, mu_m], c='red', s=100, zorder=5)
    ax1.text(0, rf-0.01, 'Rf', ha='center')
    ax1.text(sigma_m, mu_m+0.01, 'Market', ha='center')
    ax1.set_xlabel('Portfolio Standard Deviation (σ)', fontsize=12)
    ax1.set_ylabel('Expected Return E(R)', fontsize=12)
    ax1.set_title('Capital Market Line (CML)', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # SML
    beta = np.linspace(0, 2, 100)
    sml = rf + (mu_m - rf) * beta

    ax2.plot(beta, sml, 'r-', linewidth=2, label='SML')
    ax2.scatter([0, 1], [rf, mu_m], c='blue', s=100, zorder=5)
    ax2.text(0, rf-0.01, 'Rf', ha='center')
    ax2.text(1, mu_m+0.01, 'Market', ha='center')
    ax2.set_xlabel('Beta (β)', fontsize=12)
    ax2.set_ylabel('Expected Return E(R)', fontsize=12)
    ax2.set_title('Security Market Line (SML)', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('images/png/cml_sml_distinction.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Created cml_sml_distinction.png')

def create_cointegration_visualization():
    """Create cointegration visualization."""
    np.random.seed(42)
    t = np.arange(0, 100)
    trend = 0.5 * t
    noise1 = np.cumsum(np.random.randn(100) * 0.5)
    noise2 = np.cumsum(np.random.randn(100) * 0.5)

    x = trend + noise1
    y = trend + noise2  # Cointegrated with x

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

    # Time series
    ax1.plot(t, x, label='Series X', linewidth=2)
    ax1.plot(t, y, label='Series Y', linewidth=2)
    ax1.set_xlabel('Time', fontsize=12)
    ax1.set_ylabel('Value', fontsize=12)
    ax1.set_title('Cointegrated Time Series', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Spread (stationary)
    spread = x - y
    ax2.plot(t, spread, linewidth=2, color='green')
    ax2.axhline(y=0, color='red', linestyle='--', label='Mean')
    ax2.fill_between(t, spread, alpha=0.3, color='green')
    ax2.set_xlabel('Time', fontsize=12)
    ax2.set_ylabel('Spread (X - Y)', fontsize=12)
    ax2.set_title('Cointegration Spread (Stationary)', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('images/png/cointegration_visualization.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Created cointegration_visualization.png')

def create_fama_macbeth_procedure():
    """Create Fama-MacBeth procedure flowchart."""
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 12)

    ax.text(5, 11.5, 'Fama-MacBeth Two-Step Procedure',
            ha='center', fontsize=16, fontweight='bold')

    steps = [
        ('Step 1: Cross-Sectional Regressions', 5, 10, 'lightblue'),
        ('For each time period t:\nRᵢ,ₜ = γ₀,ₜ + γ₁,ₜβᵢ + εᵢ,ₜ', 5, 8.5, 'lightyellow'),
        ('Estimate risk premium γ₁,ₜ\nfor each period', 5, 7, 'lightgreen'),
        ('Step 2: Time-Series Analysis', 5, 5.5, 'lightblue'),
        ('Average risk premiums:\nγ̄₁ = (1/T)Σₜ γ₁,ₜ', 5, 4, 'lightyellow'),
        ('Test significance using\ntime-series standard errors', 5, 2.5, 'lightgreen'),
        ('Result: Risk Premium Estimate\nwith Robust Standard Errors', 5, 1, 'lightcoral'),
    ]

    y_pos = 10
    for text, x, y, color in steps:
        box = FancyBboxPatch((x-1.5, y-0.4), 3, 0.8,
                              boxstyle="round,pad=0.1",
                              edgecolor='black', facecolor=color, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=10)

        if y > 1.5:
            arrow = FancyArrowPatch((x, y-0.5), (x, y-1.1),
                                    arrowstyle='->', mutation_scale=20,
                                    linewidth=2, color='darkblue')
            ax.add_patch(arrow)

    plt.tight_layout()
    plt.savefig('images/png/fama_macbeth_procedure.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Created fama_macbeth_procedure.png')

def create_binomial_tree():
    """Create binomial tree for option pricing."""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    ax.text(5, 9.5, 'Binomial Tree for Option Pricing',
            ha='center', fontsize=16, fontweight='bold')

    # Parameters
    S0 = 100
    u = 1.1
    d = 0.9

    # Tree nodes
    nodes = [
        (1, 5, S0),
        (3, 7, S0*u),
        (3, 3, S0*d),
        (5, 8.5, S0*u*u),
        (5, 5, S0*u*d),
        (5, 1.5, S0*d*d),
    ]

    for x, y, price in nodes:
        circle = plt.Circle((x, y), 0.4, color='lightblue', ec='black', linewidth=2)
        ax.add_patch(circle)
        ax.text(x, y, f'${price:.1f}', ha='center', va='center', fontweight='bold')

    # Edges
    edges = [
        (1.4, 5.3, 2.6, 6.7, 'u'),
        (1.4, 4.7, 2.6, 3.3, 'd'),
        (3.4, 7.3, 4.6, 8.2, 'u'),
        (3.4, 6.7, 4.6, 5.3, 'd'),
        (3.4, 3.3, 4.6, 4.7, 'u'),
        (3.4, 2.7, 4.6, 1.8, 'd'),
    ]

    for x1, y1, x2, y2, label in edges:
        ax.plot([x1, x2], [y1, y2], 'k-', linewidth=2)
        mid_x, mid_y = (x1+x2)/2, (y1+y2)/2
        offset = 0.2 if label == 'u' else -0.2
        ax.text(mid_x, mid_y+offset, label, fontsize=10, style='italic')

    # Add time labels
    ax.text(1, 0.5, 't=0', ha='center', fontsize=12)
    ax.text(3, 0.5, 't=1', ha='center', fontsize=12)
    ax.text(5, 0.5, 't=2', ha='center', fontsize=12)

    plt.tight_layout()
    plt.savefig('images/png/binomial_tree_viz.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Created binomial_tree_viz.png')

def create_option_payoffs():
    """Create call and put option payoff diagrams."""
    S = np.linspace(50, 150, 100)
    K = 100

    call_payoff = np.maximum(S - K, 0)
    put_payoff = np.maximum(K - S, 0)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    # Call option
    ax1.plot(S, call_payoff, 'b-', linewidth=3, label='Call Payoff')
    ax1.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax1.axvline(x=K, color='r', linestyle='--', label=f'Strike K={K}')
    ax1.fill_between(S, call_payoff, alpha=0.3)
    ax1.set_xlabel('Stock Price at Expiration (S)', fontsize=12)
    ax1.set_ylabel('Payoff', fontsize=12)
    ax1.set_title('Call Option Payoff', fontsize=14, fontweight='bold')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Put option
    ax2.plot(S, put_payoff, 'r-', linewidth=3, label='Put Payoff')
    ax2.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
    ax2.axvline(x=K, color='b', linestyle='--', label=f'Strike K={K}')
    ax2.fill_between(S, put_payoff, alpha=0.3, color='red')
    ax2.set_xlabel('Stock Price at Expiration (S)', fontsize=12)
    ax2.set_ylabel('Payoff', fontsize=12)
    ax2.set_title('Put Option Payoff', fontsize=14, fontweight='bold')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('images/png/call_put_payoffs.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Created call_put_payoffs.png')

def create_var_identification():
    """Create VAR identification diagram."""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.axis('off')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    ax.text(5, 9.5, 'VAR Identification Strategies',
            ha='center', fontsize=16, fontweight='bold')

    boxes = [
        ('Reduced Form VAR\nYₜ = A₁Yₜ₋₁ + ... + AₚYₜ₋ₚ + uₜ', 5, 8, 'lightblue', 2),
        ('Choleski\nDecomposition', 2, 6, 'lightgreen', 1.2),
        ('Structural\nRestrictions', 5, 6, 'yellow', 1.2),
        ('Sign\nRestrictions', 8, 6, 'lightcoral', 1.2),
        ('Recursive\nOrdering', 2, 4, 'lightyellow', 1.2),
        ('Long-run\nRestrictions', 5, 4, 'lightyellow', 1.2),
        ('Economic\nTheory', 8, 4, 'lightyellow', 1.2),
        ('Identified\nStructural Shocks', 5, 2, 'orange', 2),
        ('Impulse Response\nFunctions', 5, 0.5, 'lightgreen', 2),
    ]

    for text, x, y, color, width in boxes:
        box = FancyBboxPatch((x-width/2, y-0.4), width, 0.8,
                              boxstyle="round,pad=0.1",
                              edgecolor='black', facecolor=color, linewidth=2)
        ax.add_patch(box)
        ax.text(x, y, text, ha='center', va='center', fontsize=9)

    # Arrows
    arrows = [
        (5, 7.6, 2.5, 6.4),
        (5, 7.6, 5, 6.4),
        (5, 7.6, 7.5, 6.4),
        (2, 5.6, 2, 4.4),
        (5, 5.6, 5, 4.4),
        (8, 5.6, 8, 4.4),
        (2, 3.6, 4, 2.4),
        (5, 3.6, 5, 2.4),
        (8, 3.6, 6, 2.4),
        (5, 1.6, 5, 0.9),
    ]

    for x1, y1, x2, y2 in arrows:
        arrow = FancyArrowPatch((x1, y1), (x2, y2),
                                arrowstyle='->', mutation_scale=15,
                                linewidth=1.5, color='darkblue')
        ax.add_patch(arrow)

    plt.tight_layout()
    plt.savefig('images/png/var_identification_diagram.png', dpi=150, bbox_inches='tight')
    plt.close()
    print('✓ Created var_identification_diagram.png')

# Create all missing images
if __name__ == '__main__':
    print('Generating missing images...')
    create_bgg_accelerator()
    create_cml_sml_distinction()
    create_cointegration_visualization()
    create_fama_macbeth_procedure()
    create_binomial_tree()
    create_option_payoffs()
    create_var_identification()
    print('\n✓ All missing images created successfully!')
