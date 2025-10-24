import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import networkx as nx
import os

# --- Model Setup ---
def setup_voter_model(n_agents=100, k=4, p=0.1):
    G = nx.watts_strogatz_graph(n_agents, k, p)
    opinions = np.random.randint(0, 2, n_agents)
    nx.set_node_attributes(G, {i: op for i, op in enumerate(opinions)}, 'opinion')
    return G

def voter_model_step(G):
    node = np.random.choice(G.nodes())
    neighbors = list(G.neighbors(node))
    if neighbors:
        neighbor = np.random.choice(neighbors)
        G.nodes[node]['opinion'] = G.nodes[neighbor]['opinion']

# --- Animation Setup ---
def create_animation(G, n_frames=100):
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)
    node_colors = ['royalblue' if G.nodes[i]['opinion'] == 0 else 'crimson' for i in G.nodes]
    nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, ax=ax)
    nx.draw_networkx_edges(G, pos, alpha=0.5, ax=ax)
    ax.set_title("Voter Model on a Small-World Network (Frame 0)")
    ax.axis('off')

    def update(frame):
        for _ in range(10):  # Run 10 steps per frame to speed up consensus
            voter_model_step(G)
        node_colors = ['royalblue' if G.nodes[i]['opinion'] == 0 else 'crimson' for i in G.nodes]
        nodes.set_color(node_colors)
        ax.set_title(f"Voter Model on a Small-World Network (Frame {frame + 1})")
        # Check for consensus to stop animation early
        if len(set(nx.get_node_attributes(G, 'opinion').values())) == 1:
            anim.event_source.stop()

    anim = FuncAnimation(fig, update, frames=n_frames, interval=100, repeat=False)
    return anim

# --- Main Execution ---
if __name__ == "__main__":
    output_dir = 'images/10-Specialized-Models'
    output_path = os.path.join(output_dir, 'voter_model_animation.gif')

    if not os.path.exists(output_path):
        print(f"Generating animation and saving to {output_path}...")
        graph = setup_voter_model()
        animation = create_animation(graph)
        animation.save(output_path, writer='imagemagick', fps=10)
        print("Animation saved successfully.")
    else:
        print(f"Animation already exists at {output_path}. Skipping generation.")

    plt.close() # Prevents the plot from displaying in the script output
