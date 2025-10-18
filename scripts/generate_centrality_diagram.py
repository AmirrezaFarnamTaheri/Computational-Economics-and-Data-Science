import graphviz

def generate_centrality_diagram():
    """
    Generates a conceptual diagram explaining different centrality measures.
    """
    dot = graphviz.Digraph('Centrality_Measures', comment='Centrality Measures Explained')
    dot.attr(rankdir='TB', splines='spline', overlap='false', fontname="Helvetica", fontsize="12")

    # --- Degree Centrality ---
    with dot.subgraph(name='cluster_degree') as c:
        c.attr(label='Degree Centrality\n(Number of direct connections)', style='rounded', color='blue')
        c.node_attr.update(style='filled', color='lightblue', shape='circle')
        c.node('D_center', 'A', style='filled', color='gold', a_centrality='high')
        for i in range(1, 6):
            c.node(f'D{i}', f'N{i}')
            c.edge('D_center', f'D{i}')

    # --- Betweenness Centrality ---
    with dot.subgraph(name='cluster_betweenness') as c:
        c.attr(label='Betweenness Centrality\n(Bridge between groups)', style='rounded', color='green')
        c.node_attr.update(style='filled', color='lightgreen', shape='circle')
        c.node('B_center', 'B', style='filled', color='gold')
        with c.subgraph(name='cluster_b1') as c1:
            c1.attr(label='Group 1', style='dotted')
            for i in range(1, 4):
                c1.node(f'B1_{i}', '')
                c1.edge(f'B1_{i}', 'B_center')
        with c.subgraph(name='cluster_b2') as c2:
            c2.attr(label='Group 2', style='dotted')
            for i in range(1, 4):
                c2.node(f'B2_{i}', '')
                c2.edge(f'B2_{i}', 'B_center')

    # --- Eigenvector Centrality ---
    with dot.subgraph(name='cluster_eigen') as c:
        c.attr(label='Eigenvector Centrality\n(Connected to other important nodes)', style='rounded', color='purple')
        c.node_attr.update(style='filled', color='lavender', shape='circle')
        c.node('E_center', 'C', style='filled', color='gold')
        c.node('E_subcenter1', 'D', style='filled', color='orange')
        c.node('E_subcenter2', 'E', style='filled', color='orange')
        c.edge('E_center', 'E_subcenter1')
        c.edge('E_center', 'E_subcenter2')
        for i in range(1, 3):
            c.node(f'E_leaf{i}', '')
            c.edge('E_subcenter1', f'E_leaf{i}')
        for i in range(3, 5):
            c.node(f'E_leaf{i}', '')
            c.edge('E_subcenter2', f'E_leaf{i}')


    # Render and save
    import os
    save_dir = 'images'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_path = os.path.join(save_dir, 'centrality_measures_diagram')
    dot.render(save_path, format='png', view=False, cleanup=True)
    print(f"Diagram '{save_path}.png' created successfully.")


if __name__ == '__main__':
    generate_centrality_diagram()