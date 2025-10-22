
import graphviz
import os

def create_ensemble_images():
    """Creates images illustrating ensemble methods."""
    output_dir = '07-Machine-Learning'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # --- Image 1: Bagging Process ---
    dot = graphviz.Digraph(comment='Bagging Process')
    dot.node('D', 'Original Data')
    dot.node('D1', 'Bootstrap Sample 1')
    dot.node('D2', 'Bootstrap Sample 2')
    dot.node('Dn', 'Bootstrap Sample n')
    dot.node('M1', 'Model 1')
    dot.node('M2', 'Model 2')
    dot.node('Mn', 'Model n')
    dot.node('A', 'Aggregate (Vote/Average)')
    dot.edge('D', 'D1')
    dot.edge('D', 'D2')
    dot.edge('D', 'Dn')
    dot.edge('D1', 'M1')
    dot.edge('D2', 'M2')
    dot.edge('Dn', 'Mn')
    dot.edge('M1', 'A')
    dot.edge('M2', 'A')
    dot.edge('Mn', 'A')
    dot.render(os.path.join(output_dir, 'bagging_process'), format='png', cleanup=True)

    # --- Image 2: Boosting Process ---
    dot = graphviz.Digraph(comment='Boosting Process')
    dot.node('D', 'Original Data')
    dot.node('M1', 'Model 1')
    dot.node('E1', 'Errors 1')
    dot.node('M2', 'Model 2')
    dot.node('E2', 'Errors 2')
    dot.node('Mn', 'Model n')
    dot.edge('D', 'M1')
    dot.edge('M1', 'E1')
    dot.edge('E1', 'M2')
    dot.edge('M2', 'E2')
    dot.edge('E2', 'Mn')
    dot.render(os.path.join(output_dir, 'boosting_process'), format='png', cleanup=True)

    # --- Image 3: Stacking Process ---
    dot = graphviz.Digraph(comment='Stacking Process')
    dot.node('D', 'Original Data')
    dot.node('M1', 'Model 1')
    dot.node('M2', 'Model 2')
    dot.node('Mn', 'Model n')
    dot.node('P', 'Predictions')
    dot.node('MM', 'Meta-Model')
    dot.edge('D', 'M1')
    dot.edge('D', 'M2')
    dot.edge('D', 'Mn')
    dot.edge('M1', 'P')
    dot.edge('M2', 'P')
    dot.edge('Mn', 'P')
    dot.edge('P', 'MM')
    dot.render(os.path.join(output_dir, 'stacking_process'), format='png', cleanup=True)

    print("Ensemble images created successfully.")

if __name__ == '__main__':
    create_ensemble_images()
