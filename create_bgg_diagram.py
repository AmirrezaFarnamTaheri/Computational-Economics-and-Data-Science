import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='BGG Financial Accelerator')
dot.attr(rankdir='TB', size='8,8')

# Define nodes
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue')
dot.node('A', 'Positive Shock (e.g., Technology)')
dot.node('B', 'Firm Profits & Net Worth Increase')
dot.node('C', 'Leverage (K/N) Decreases')
dot.node('D', 'External Finance Premium (EFP) Falls')
dot.node('E', 'Cost of Capital Decreases')
dot.node('F', 'Investment Increases')
dot.node('G', 'Aggregate Demand & Output Rise')

# Define edges
dot.edge('A', 'B')
dot.edge('B', 'C')
dot.edge('C', 'D')
dot.edge('D', 'E')
dot.edge('E', 'F')
dot.edge('F', 'G')
dot.edge('G', 'B', label='Amplification Loop', style='dashed', color='red', fontcolor='red')

# Render and save the graph
dot.render('bgg_accelerator_loop', format='png', cleanup=True)

print("Diagram 'bgg_accelerator_loop.png' created successfully.")
