
import graphviz

def create_causal_tree_diagram():
    dot = graphviz.Digraph(comment='Causal Tree Split')
    dot.attr('node', shape='box', style='rounded')

    # Regression Tree Side
    dot.node('R_Root', 'Root Node\\nMSE = 10.5')
    dot.node('R_L1', 'Age < 40\\nMSE = 5.2')
    dot.node('R_R1', 'Age >= 40\\nMSE = 6.8')
    dot.edge('R_Root', 'R_L1', label='Split by Age')
    dot.edge('R_Root', 'R_R1', label='Split by Age')

    # Causal Tree Side
    dot.node('C_Root', 'Root Node\\nEst. Effect = +5%')
    dot.node('C_L1', 'Age < 40\\nEst. Effect = +12%')
    dot.node('C_R1', 'Age >= 40\\nEst. Effect = -2%')
    dot.edge('C_Root', 'C_L1', label='Split by Age')
    dot.edge('C_Root', 'C_R1', label='Split by Age')

    dot.render('images/07-Machine-Learning/causal_tree_split', format='png', cleanup=True)

if __name__ == '__main__':
    create_causal_tree_diagram()
