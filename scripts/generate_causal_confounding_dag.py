import graphviz
import os

def generate_diagram():
    dot = graphviz.Digraph(format='png')
    dot.attr(dpi='300') # High quality
    dot.attr(bgcolor='transparent')

    dot.node('D', 'Treatment')
    dot.node('Y', 'Outcome')
    dot.node('Z', 'Confounder')

    dot.edge('Z', 'D')
    dot.edge('Z', 'Y')
    dot.edge('D', 'Y')

    # Save
    output_dir = 'images/06-Econometrics'
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, 'confounding_dag')
    dot.render(output_path, cleanup=True)
    print(f"Generated {output_path}.png")

if __name__ == "__main__":
    generate_diagram()
