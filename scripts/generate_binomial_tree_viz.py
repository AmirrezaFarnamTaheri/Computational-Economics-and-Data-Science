import numpy as np
import graphviz

def generate_binomial_tree_viz(n_steps=3, S0=100, K=100, T=1.0, r=0.05, sigma=0.2, option_type='call'):
    """
    Generates a visualization of a binomial tree for option pricing.
    """
    dot = graphviz.Digraph('Binomial_Tree', comment='Binomial Option Pricing Tree')
    dot.attr('node', shape='record', style='rounded', fontname='Helvetica', fontsize='10')
    dot.attr(rankdir='LR')

    dt = T / n_steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)

    # 1. Generate asset prices at each node
    prices = {}
    for i in range(n_steps + 1):
        for j in range(i + 1):
            price = S0 * (u**j) * (d**(i-j))
            prices[(i, j)] = price
            node_name = f'node_{i}_{j}'
            dot.node(node_name, f'{{S={price:.2f} | C=?}}')

    # 2. Calculate option values at expiration
    option_values = {}
    for j in range(n_steps + 1):
        price = prices[(n_steps, j)]
        if option_type == 'call':
            value = max(0, price - K)
        else:
            value = max(0, K - price)
        option_values[(n_steps, j)] = value
        node_name = f'node_{n_steps}_{j}'
        dot.node(node_name, f'{{S={price:.2f} | C={value:.2f}}}')

    # 3. Work backwards to price the option
    for i in range(n_steps - 1, -1, -1):
        for j in range(i + 1):
            val_up = option_values[(i + 1, j + 1)]
            val_down = option_values[(i + 1, j)]
            value = np.exp(-r * dt) * (p * val_up + (1 - p) * val_down)
            option_values[(i, j)] = value
            node_name = f'node_{i}_{j}'
            price = prices[(i,j)]
            dot.node(node_name, f'{{S={price:.2f} | C={value:.2f}}}')

    # 4. Create edges
    for i in range(n_steps):
        for j in range(i + 1):
            dot.edge(f'node_{i}_{j}', f'node_{i+1}_{j+1}', label=f'p={p:.2f}')
            dot.edge(f'node_{i}_{j}', f'node_{i+1}_{j}', label=f'1-p={(1-p):.2f}')

    # Render and save
    import os
    save_dir = 'images/finance/options'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_path = os.path.join(save_dir, 'binomial_tree_viz')
    dot.render(save_path, format='png', view=False, cleanup=True)
    print(f"Plot saved to {save_path}.png")


if __name__ == '__main__':
    generate_binomial_tree_viz()