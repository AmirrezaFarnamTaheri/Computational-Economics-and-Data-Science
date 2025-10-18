import os
import graphviz

def generate_causal_tree_split_image():
    """
    Generates an image visualizing the splitting logic of a Causal Tree.
    """
    # Ensure the target directory exists
    output_dir = "images/causal_ml"
    os.makedirs(output_dir, exist_ok=True)

    # Define the graph
    dot = graphviz.Digraph('Causal Tree')
    dot.attr('node', shape='box', style='rounded', fontname='helvetica')
    dot.attr(label='Figure 2: Causal vs. Regression Tree Splitting Logic', fontsize='16', labelloc='t', fontname='helvetica')

    dot.node('root', 'Root Node\\n(Full Sample)\\nEst. Effect τ = 0.5')
    dot.node('left', 'Left Child\\nEst. Effect τ = -0.2')
    dot.node('right', 'Right Child\\nEst. Effect τ = 1.2')

    dot.edge('root', 'left', label='  Age < 40  ', fontname='helvetica')
    dot.edge('root', 'right', label='  Age >= 40  ', fontname='helvetica')

    # --- Render and Save ---
    output_path = os.path.join(output_dir, "figure2_causal_tree_split")
    dot.render(output_path, format='png', cleanup=True)
    print(f"Image saved to {output_path}.png")

if __name__ == "__main__":
    generate_causal_tree_split_image()