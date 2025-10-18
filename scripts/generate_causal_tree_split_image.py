import graphviz
import os

def generate_causal_tree_image():
    """
    Generates a diagram illustrating the splitting logic of a Causal Tree.
    """
    dot = graphviz.Digraph(comment='Causal Tree Split')
    dot.attr('node', shape='box', style='rounded', fontname='Helvetica', fontsize='12')
    dot.attr('edge', fontname='Helvetica', fontsize='10')
    dot.attr(rankdir='TB', size='8,5')

    # Node styles
    parent_style = {'style': 'filled', 'fillcolor': 'lightblue'}
    child_style_high = {'style': 'filled', 'fillcolor': 'lightgreen'}
    child_style_low = {'style': 'filled', 'fillcolor': 'salmon'}

    # Create nodes
    dot.node('Root', 'Parent Node\\n(N=200)\\nτ = 0.5', **parent_style)
    dot.node('Child1', 'Child 1 (Age < 40)\\n(N=120)\\nτ = 1.2', **child_style_high)
    dot.node('Child2', 'Child 2 (Age >= 40)\\n(N=80)\\nτ = -0.3', **child_style_low)

    # Create edges
    dot.edge('Root', 'Child1', label='Age < 40')
    dot.edge('Root', 'Child2', label='Age >= 40')

    dot.attr(label='Causal Tree Splitting Logic\\nMaximizing Treatment Effect Heterogeneity', fontsize='16', labelloc='t')

    # Define the output path
    output_path = os.path.join(os.path.dirname(__file__), '..', 'images', '07-Machine-Learning', 'causal_ml', 'figure2_causal_tree_split')

    # Render the graph
    dot.render(output_path, format='png', cleanup=True)
    print(f"Image saved to {output_path}.png")

if __name__ == "__main__":
    # Ensure the target directory exists
    img_dir = os.path.join(os.path.dirname(__file__), '..', 'images', '07-Machine-Learning', 'causal_ml')
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    generate_causal_tree_image()