import graphviz

def generate_emergence_diagram():
    """
    Generates a diagram illustrating the concept of emergence in ABMs.
    """
    dot = graphviz.Digraph('Emergence', comment='Emergence in Agent-Based Models')
    dot.attr(rankdir='TB', splines='spline')

    # --- Micro Level ---
    with dot.subgraph(name='cluster_micro') as c:
        c.attr(label='Micro Level: Agent Interactions', style='rounded', color='blue', fontname="Helvetica", fontsize="12")
        c.node_attr.update(style='filled', color='lightblue', shape='ellipse', fontname="Helvetica", fontsize="10")

        c.node('A1', 'Agent 1\n(Rules, State)')
        c.node('A2', 'Agent 2\n(Rules, State)')
        c.node('A3', 'Agent 3\n(Rules, State)')
        c.node('A_etc', '...')

        c.edge('A1', 'A2', label='Local Interaction')
        c.edge('A2', 'A3', label='Local Interaction')
        c.edge('A3', 'A1', label='Local Interaction')
        c.edge('A2', 'A_etc', label='Local Interaction')

    # --- Macro Level ---
    with dot.subgraph(name='cluster_macro') as c:
        c.attr(label='Macro Level: System-Wide Patterns', style='rounded', color='green', fontname="Helvetica", fontsize="12")
        c.node_attr.update(style='filled', color='lightgreen', shape='box', fontname="Helvetica", fontsize="10")

        c.node('P1', 'Bubbles & Crashes')
        c.node('P2', 'Segregation Patterns')
        c.node('P3', 'Business Cycles')
        c.node('P_etc', '...')

    # --- Emergence Arrow ---
    dot.edge('cluster_micro', 'cluster_macro', label=' Leads to (Emergence) ', style='dashed', arrowhead='normal', minlen='2', fontname="Helvetica", fontsize="12", color="purple", fontcolor="purple")

    # Render and save
    import os
    save_dir = 'images'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_path = os.path.join(save_dir, 'emergence_diagram')
    dot.render(save_path, format='png', view=False, cleanup=True)
    print(f"Diagram '{save_path}.png' created successfully.")

if __name__ == '__main__':
    generate_emergence_diagram()