
from graphviz import Digraph
import os

def create_fusion_diagram():
    """
    Creates a diagram illustrating early, late, and intermediate fusion strategies.
    """
    dot = Digraph(comment='Multi-modal Fusion Strategies')
    dot.attr(rankdir='TB', size='12,12', label='Multi-modal Fusion Strategies', fontsize='20')

    # --- Early Fusion ---
    with dot.subgraph(name='cluster_early') as c:
        c.attr(label='Early Fusion (Feature-level)', style='filled', color='lightgrey')
        c.node_attr.update(style='filled', color='white')
        c.node('early_in1', 'Modality 1 (e.g., Text)')
        c.node('early_in2', 'Modality 2 (e.g., Tabular)')
        c.node('early_concat', 'Concatenate Features')
        c.node('early_model', 'Unified Model')
        c.node('early_out', 'Prediction')
        c.edge('early_in1', 'early_concat')
        c.edge('early_in2', 'early_concat')
        c.edge('early_concat', 'early_model')
        c.edge('early_model', 'early_out')

    # --- Late Fusion ---
    with dot.subgraph(name='cluster_late') as c:
        c.attr(label='Late Fusion (Decision-level)', style='filled', color='lightgrey')
        c.node_attr.update(style='filled', color='white')
        c.node('late_in1', 'Modality 1 (e.g., Text)')
        c.node('late_in2', 'Modality 2 (e.g., Tabular)')
        c.node('late_model1', 'Model 1')
        c.node('late_model2', 'Model 2')
        c.node('late_combine', 'Combine Decisions')
        c.node('late_out', 'Prediction')
        c.edge('late_in1', 'late_model1')
        c.edge('late_in2', 'late_model2')
        c.edge('late_model1', 'late_combine')
        c.edge('late_model2', 'late_combine')
        c.edge('late_combine', 'late_out')

    # --- Intermediate Fusion ---
    with dot.subgraph(name='cluster_intermediate') as c:
        c.attr(label='Intermediate Fusion (Hybrid)', style='filled', color='lightgrey')
        c.node_attr.update(style='filled', color='white')
        c.node('inter_in1', 'Modality 1 (e.g., Text)')
        c.node('inter_in2', 'Modality 2 (e.g., Tabular)')
        c.node('inter_branch1', 'Branch 1')
        c.node('inter_branch2', 'Branch 2')
        c.node('inter_fuse', 'Fuse Intermediate Representations')
        c.node('inter_joint', 'Joint Model')
        c.node('inter_out', 'Prediction')
        c.edge('inter_in1', 'inter_branch1')
        c.edge('inter_in2', 'inter_branch2')
        c.edge('inter_branch1', 'inter_fuse')
        c.edge('inter_branch2', 'inter_fuse')
        c.edge('inter_fuse', 'inter_joint')
        c.edge('inter_joint', 'inter_out')

    # Save the diagram
    output_path = os.path.join('images', '07-Machine-Learning', 'multimodal_fusion_strategies')
    dot.render(output_path, format='png', view=False)
    print(f"Diagram saved to {output_path}.png")

if __name__ == '__main__':
    # Ensure the output directory exists
    os.makedirs(os.path.join('images', '07-Machine-Learning'), exist_ok=True)
    create_fusion_diagram()
