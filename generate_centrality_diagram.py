from graphviz import Digraph
import os

def create_centrality_diagram():
    """
    Generates a visual explanation of different network centrality measures.
    """
    dot = Digraph(comment='Centrality Measures')
    dot.attr('graph', rankdir='TB', bgcolor='transparent', label='Understanding Node Centrality', fontname='Helvetica', fontsize='20', labelloc='t')
    dot.attr('node', shape='circle', style='filled', fontname='Helvetica', width='1.2')
    dot.attr('edge', arrowhead='none', penwidth='2')

    # Common structure for all subgraphs
    common_edges = [('B', 'A'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('C', 'F'), ('F', 'G')]

    # 1. Degree Centrality
    with dot.subgraph(name='cluster_degree') as c:
        c.attr(label='Degree Centrality: Popularity', style='rounded', color='darkblue')
        c.node('A', 'A')
        c.node('B', 'B', fillcolor='gold')
        c.node('C', 'C', fillcolor='gold')
        c.node('D', 'D')
        c.node('E', 'E')
        c.node('F', 'F')
        c.node('G', 'G')
        c.edges(common_edges)
        c.attr(labeljust='l', labelloc='b', label='Node C has the highest degree (3 connections).\\nIt is a local hub.')

    # 2. Betweenness Centrality
    with dot.subgraph(name='cluster_betweenness') as c:
        c.attr(label='Betweenness Centrality: Bridge', style='rounded', color='firebrick')
        c.node('A2', 'A')
        c.node('B2', 'B')
        c.node('C2', 'C', fillcolor='coral')
        c.node('D2', 'D')
        c.node('E2', 'E')
        c.node('F2', 'F')
        c.node('G2', 'G')
        c.edges([('B2', 'A2'), ('B2', 'C2'), ('C2', 'D2'), ('D2', 'E2'), ('C2', 'F2'), ('F2', 'G2')])
        c.edge('A2', 'E2', style='dashed', color='firebrick', constraint='false', label='Path A->E')
        c.edge('B2', 'G2', style='dashed', color='firebrick', constraint='false', label='Path B->G')
        c.attr(labeljust='l', labelloc='b', label='Node C is on most shortest paths (e.g., A-E, B-G).\\nIt acts as a critical bridge or gatekeeper.')

    # 3. Eigenvector Centrality
    with dot.subgraph(name='cluster_eigenvector') as c:
        c.attr(label='Eigenvector Centrality: Influence', style='rounded', color='darkgreen')
        c.node('A3', 'A')
        c.node('B3', 'B', fillcolor='yellowgreen')
        c.node('C3', 'C', fillcolor='gold')
        c.node('D3', 'D')
        c.node('E3', 'E')
        c.node('F3', 'F')
        c.node('G3', 'G')
        c.edges(common_edges)
        c.attr(labeljust='l', labelloc='b', label='Node C is connected to B, which is also well-connected.\\nThis makes C more influential than F, even with equal degrees.')

    # Save the file
    output_dir = 'images/10-Specialized-Models'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'centrality_measures_diagram')

    dot.render(output_path, format='png', view=False, cleanup=True)
    return f"{output_path}.png"

if __name__ == "__main__":
    generated_file = create_centrality_diagram()
    print(f"Diagram saved to: {generated_file}")
