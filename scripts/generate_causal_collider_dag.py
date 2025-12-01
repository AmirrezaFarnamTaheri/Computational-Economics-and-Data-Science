import graphviz
import os

def generate_diagram():
    dot = graphviz.Digraph(format='png')
    dot.attr(dpi='300')
    dot.attr(bgcolor='transparent')

    dot.node('T', 'Talent')
    dot.node('L', 'Luck')
    dot.node('A', 'Admission')

    dot.edge('T', 'A')
    dot.edge('L', 'A')

    output_dir = 'images/06-Econometrics'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'collider_bias_dag')
    dot.render(output_path, cleanup=True)
    print(f"Generated {output_path}.png")

if __name__ == "__main__":
    generate_diagram()
