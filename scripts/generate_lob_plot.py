import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def generate_lob_plot():
    """
    Generates and saves a visualization of a limit order book.
    """
    # --- Generate Synthetic LOB Data ---
    mid_price = 100.00
    best_bid = 99.99
    best_ask = 100.01

    # Bids (price descending)
    bid_prices = np.arange(best_bid, best_bid - 0.10, -0.01)
    bid_sizes = np.random.randint(100, 1000, len(bid_prices)) * np.exp(-np.arange(len(bid_prices)) * 0.5)
    bid_sizes = bid_sizes.astype(int)

    # Asks (price ascending)
    ask_prices = np.arange(best_ask, best_ask + 0.10, 0.01)
    ask_sizes = np.random.randint(100, 1000, len(ask_prices)) * np.exp(-np.arange(len(ask_prices)) * 0.5)
    ask_sizes = ask_sizes.astype(int)

    bid_df = pd.DataFrame({'price': bid_prices, 'volume': bid_sizes})
    ask_df = pd.DataFrame({'price': ask_prices, 'volume': ask_sizes})

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(12, 8))
    plt.style.use('seaborn-v0_8-whitegrid')

    # Plot Bids
    ax.barh(bid_df['price'], bid_df['volume'], color='red', alpha=0.6, height=0.008, label='Bid Orders')

    # Plot Asks
    ax.barh(ask_df['price'], ask_df['volume'], color='green', alpha=0.6, height=0.008, label='Ask Orders')

    # Annotations and Labels
    ax.axhline(best_bid, color='r', linestyle='--', lw=1.5, label=f'Best Bid: ${best_bid:.2f}')
    ax.axhline(best_ask, color='g', linestyle='--', lw=1.5, label=f'Best Ask: ${best_ask:.2f}')

    spread = best_ask - best_bid
    ax.annotate(f'Bid-Ask Spread: ${spread:.2f}',
                xy=(max(ask_df['volume'])*0.5, best_ask),
                xytext=(max(ask_df['volume'])*0.5, best_ask + 0.03),
                arrowprops=dict(facecolor='black', shrink=0.05),
                ha='center')

    ax.set_xlabel('Order Size (Volume)')
    ax.set_ylabel('Price ($)')
    ax.set_title('Snapshot of a Limit Order Book (LOB)', fontsize=18)
    ax.legend(loc='center right')
    ax.invert_xaxis() # Common convention for LOB plots
    ax.yaxis.set_major_formatter(plt.FormatStrFormatter('%.2f'))

    plt.tight_layout()

    # --- Save Figure ---
    import os
    save_dir = 'images/finance'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_path = os.path.join(save_dir, 'images\png\limit_order_book.png')
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"Plot saved to {save_path}")

if __name__ == '__main__':
    generate_lob_plot()