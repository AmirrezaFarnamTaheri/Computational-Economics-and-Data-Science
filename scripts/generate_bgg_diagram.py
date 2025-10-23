from graphviz import Digraph

dot = Digraph(comment='BGG Financial Accelerator')

dot.attr('node', shape='box', style='rounded', fontname='Helvetica', fontsize='12')
dot.attr('edge', fontname='Helvetica', fontsize='10')

dot.node('A', 'Positive Shock (e.g., Technology)')
dot.node('B', 'Higher Firm Profits & Net Worth')
dot.node('C', 'Lower Leverage (K/N)')
dot.node('D', 'Lower External Finance Premium (EFP)')
dot.node('E', 'Increased Investment (I)')
dot.node('F', 'Higher Aggregate Demand & Output (Y)')

dot.edge('A', 'B')
dot.edge('B', 'C')
dot.edge('C', 'D')
dot.edge('D', 'E')
dot.edge('E', 'F')
dot.edge('F', 'B', label='Virtuous Cycle')

dot.render('images/09-Finance/bgg_accelerator_loop', format='png', view=False)
