import graphviz

def generate_var_identification_diagram():
    """
    Generates and saves a diagram illustrating the VAR identification problem.
    """
    dot = graphviz.Digraph('VAR_Identification', comment='VAR Identification')
    dot.attr('node', shape='box', style='rounded', fontname='Helvetica', fontsize='10')
    dot.attr('graph', rankdir='LR', fontname='Helvetica', fontsize='10')

    # Nodes
    dot.node('U', 'Structural Shocks (u_t)\n- Uncorrelated\n- Economically meaningful\n(e.g., policy shock, demand shock)')
    dot.node('A', 'Contemporaneous Effects Matrix (A)\n- Contains identifying assumptions\n(e.g., Cholesky decomposition)')
    dot.node('E', 'Reduced-Form Residuals (ε_t)\n- Correlated\n- Directly estimated by VAR')

    # Edges
    dot.edge('U', 'A', label='Transformed by')
    dot.edge('A', 'E', label='To produce')

    # Grouping to show the equation
    with dot.subgraph(name='cluster_0') as c:
        c.attr(color='invis')
        c.node_attr.update(style='invis')
        c.edge_attr.update(style='invis')
        c.node('eq', 'A * ε_t = B * u_t', shape='plaintext', fontsize='14')


    # Render and save
    import os
    if not os.path.exists('images'):
        os.makedirs('images')

    dot.render('images/var_identification_diagram', format='png', view=False, cleanup=True)
    print("Diagram 'images\png\var_identification_diagram.png' created successfully.")

if __name__ == '__main__':
    generate_var_identification_diagram()