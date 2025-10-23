from graphviz import Digraph

dot = Digraph(comment='Emergence')

dot.attr('node', shape='box', style='rounded', fontname='Helvetica', fontsize='12')
dot.attr('edge', fontname='Helvetica', fontsize='10')

with dot.subgraph(name='cluster_0') as c:
    c.attr(style='filled', color='lightgrey')
    c.node_attr.update(style='filled', color='white')
    c.edges([('A1', 'A2'), ('A2', 'A3'), ('A3', 'A1')])
    c.attr(label='Micro Level: Agent Interactions')
    c.node('A1', 'Agent 1')
    c.node('A2', 'Agent 2')
    c.node('A3', 'Agent 3')

dot.node('B', 'Macro Level: Emergent Pattern (e.g., Market Crash)')

dot.edge('A1', 'B', style='dashed')
dot.edge('A2', 'B', style='dashed')
dot.edge('A3', 'B', style='dashed')


dot.render('images/10-Specialized-Models/emergence_diagram', format='png', view=False)
