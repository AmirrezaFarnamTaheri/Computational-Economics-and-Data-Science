import graphviz

def generate_bgg_accelerator_flowchart():
    """
    Generates and saves a flowchart for the BGG Financial Accelerator loop.
    """
    dot = graphviz.Digraph('BGG_Financial_Accelerator', comment='The BGG Financial Accelerator')
    dot.attr('node', shape='box', style='rounded', fontname='Helvetica', fontsize='10', width='2.5')
    dot.attr('edge', fontname='Helvetica', fontsize='10')
    dot.attr(rankdir='TB', splines='curved')

    # Nodes
    dot.node('A', 'Positive Economic Shock\n(e.g., Technology Improvement)')
    dot.node('B', 'Firm Profits & Asset Prices Increase')
    dot.node('C', 'Firm Net Worth Improves\n(Stronger Balance Sheets)')
    dot.node('D', 'Lower Leverage (K/N)\n("More skin in the game")')
    dot.node('E', 'External Finance Premium (EFP) Falls\n(Lower cost of borrowing)')
    dot.node('F', 'Investment Increases Sharply')
    dot.node('G', 'Higher Aggregate Demand & Output')

    # Edges
    dot.edge('A', 'B')
    dot.edge('B', 'C')
    dot.edge('C', 'D')
    dot.edge('D', 'E')
    dot.edge('E', 'F')
    dot.edge('F', 'G')
    dot.edge('G', 'B', label='Amplifying Feedback Loop')

    # Render and save
    import os
    if not os.path.exists('images'):
        os.makedirs('images')

    dot.render('images/bgg_accelerator', format='png', view=False, cleanup=True)
    print("Flowchart 'images\png\bgg_accelerator.png' created successfully.")

if __name__ == '__main__':
    generate_bgg_accelerator_flowchart()