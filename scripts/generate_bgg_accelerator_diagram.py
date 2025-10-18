import graphviz

# Create a new directed graph
dot = graphviz.Digraph('BGG_Accelerator', comment='The BGG Financial Accelerator')
dot.attr(rankdir='TB', size='8,8', label='The Financial Accelerator Loop', fontsize='20')

# Define nodes with specific shapes and styles
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue', fontname='Helvetica')
dot.node('A', 'Positive Shock\n(e.g., Technology)')
dot.node('B', 'Firm Profits & Net Worth ↑')
dot.node('C', 'Leverage (K/N) ↓\n(Balance Sheet Improves)')
dot.node('D', 'External Finance Premium (EFP) ↓')
dot.node('E', 'Cost of Capital ↓')
dot.node('F', 'Investment & Aggregate Demand ↑')

# Define edges to create the loop
dot.edge('A', 'B')
dot.edge('B', 'C')
dot.edge('C', 'D')
dot.edge('D', 'E')
dot.edge('E', 'F')
dot.edge('F', 'B', style='dashed', constraint='false', label='Amplification Feedback')

# Render the graph
output_path = 'images/bgg_accelerator'
dot.render(output_path, format='png', view=False, cleanup=True)

print(f"Diagram saved to {output_path}.png")