from graphviz import Digraph
import os

def create_emergence_diagram():
    """
    Generates a diagram illustrating the concept of emergence using Graphviz.
    """
    dot = Digraph(comment='Emergence Concept')
    dot.attr('graph', rankdir='BT', bgcolor='transparent', label='The Concept of Emergence', fontname='Helvetica', fontsize='20')

    # Node attributes
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue', fontname='Helvetica')

    # Micro-level nodes
    with dot.subgraph(name='cluster_micro') as c:
        c.attr(label='Micro Level: Agent Rules & Local Interactions', style='rounded', color='grey')
        c.node('A1', 'Agent 1\\n(Simple Rules)')
        c.node('A2', 'Agent 2\\n(Simple Rules)')
        c.node('A3', 'Agent N\\n(Simple Rules)')
        c.edge('A1', 'A2', label='interacts', arrowhead='none')
        c.edge('A2', 'A3', label='interacts', arrowhead='none')

    # Macro-level node
    dot.attr('node', shape='ellipse', style='filled', fillcolor='lightgreen')
    dot.node('M1', 'Macro Level: Complex System-Wide Patterns\\n(e.g., Market Crashes, Segregation, Flocking)')

    # Emergence arrow
    dot.edge('A2', 'M1', label='Leads to (Emergence)', dir='back', constraint='false',
             fontsize='12', fontcolor='darkgreen', color='darkgreen', style='dashed', penwidth='2')

    # Save the file
    output_dir = 'images/10-Specialized-Models'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, 'emergence_diagram')

    # Using .render() will save the file as 'emergence_diagram.png'
    dot.render(output_path, format='png', view=False, cleanup=True)

    return f"{output_path}.png"

if __name__ == "__main__":
    generated_file = create_emergence_diagram()
    print(f"Diagram saved to: {generated_file}")
