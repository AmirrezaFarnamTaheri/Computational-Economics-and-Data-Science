from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import os

def setup_financial_network(n_banks=100, m=3, seed=42):
    G = nx.DiGraph(nx.barabasi_albert_graph(n=n_banks, m=m, seed=seed))
    rng = np.random.default_rng(seed)
    for node in G.nodes():
        G.nodes[node]['capital'] = 10.0
        G.nodes[node]['status'] = 'solvent'
    for u, v in G.edges():
        G.edges[u, v]['weight'] = rng.uniform(3, 7)
    return G

def animate_and_save_contagion(graph, initial_shock_nodes, output_path):
    G = graph.copy()
    pos = nx.spring_layout(G, seed=42)
    fig, ax = plt.subplots(figsize=(10, 8))

    history = []
    for node in initial_shock_nodes:
        if G.has_node(node): G.nodes[node]['status'] = 'initially_failed'
    history.append(G.copy())

    newly_failed_in_round = list(initial_shock_nodes)
    while newly_failed_in_round:
        failing_now = newly_failed_in_round
        newly_failed_in_round = []
        # Create a copy to iterate over while modifying the original
        G_current_round = G.copy()
        for failing_node in failing_now:
            # G.in_edges gets the creditors
            for creditor, _ in G_current_round.in_edges(failing_node):
                if G.nodes[creditor]['status'] == 'solvent':
                    G.nodes[creditor]['capital'] -= G_current_round.edges[creditor, failing_node]['weight']
                    if G.nodes[creditor]['capital'] <= 0:
                        G.nodes[creditor]['status'] = 'failed_in_cascade'
                        if creditor not in newly_failed_in_round:
                             newly_failed_in_round.append(creditor)
        if newly_failed_in_round:
            history.append(G.copy())

    def update(frame):
        ax.clear()
        G_t = history[frame]
        status_map = {'solvent': 'skyblue', 'initially_failed': 'orange', 'failed_in_cascade': 'red'}
        colors = [status_map[G_t.nodes[n]['status']] for n in G_t.nodes()]
        nx.draw(G_t, pos, ax=ax, node_color=colors, node_size=120, width=0.6, edge_color='gray', arrows=False)
        n_failed = sum(1 for n in G_t.nodes() if G_t.nodes[n]['status'] != 'solvent')
        ax.set_title(f'Financial Contagion - Round: {frame} | Total Failures: {n_failed}', fontsize=16)

    anim = FuncAnimation(fig, update, frames=len(history), interval=800, repeat=False)
    print(f"Saving animation to {output_path}...")
    anim.save(output_path, writer='imagemagick', fps=1.5)
    plt.close(fig)
    print("Animation saved.")

if __name__ == "__main__":
    output_dir = 'images/10-Specialized-Models'
    output_path = os.path.join(output_dir, 'financial_contagion_animation.gif')

    if not os.path.exists(output_path):
        G_finance = setup_financial_network()
        # Shock the most interconnected node (highest weighted out-degree)
        central_node = max(dict(G_finance.out_degree(weight='weight')).items(), key=lambda x: x[1])[0]
        animate_and_save_contagion(G_finance, [central_node], output_path)
    else:
        print(f"Animation already exists at {output_path}.")
