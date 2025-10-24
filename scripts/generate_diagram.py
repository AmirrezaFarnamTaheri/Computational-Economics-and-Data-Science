
import graphviz
import os

def generate_bgg_diagram():
    """Generates a flowchart for the BGG Financial Accelerator loop."""
    dot = graphviz.Digraph('BGG_Financial_Accelerator', comment='The BGG Financial Accelerator Loop')
    dot.attr('node', shape='box', style='rounded', fontname='Helvetica', fontsize='12')
    dot.attr('edge', fontname='Helvetica', fontsize='10')

    # Define nodes
    dot.node('A', 'Positive Shock (e.g., to technology)')
    dot.node('B', 'Higher Firm Profits & Net Worth')
    dot.node('C', 'Lower Firm Leverage (K/N)')
    dot.node('D', 'Lower External Finance Premium (EFP)')
    dot.node('E', 'Increased Investment & Aggregate Demand')

    # Define edges
    dot.edge('A', 'B')
    dot.edge('B', 'C', 'Improves Balance Sheet')
    dot.edge('C', 'D', 'Reduces Agency Costs')
    dot.edge('D', 'E', 'Lowers Cost of Capital')
    dot.edge('E', 'B', 'Amplifies Cycle', style='dashed')

    # Create the directory if it doesn't exist
    output_dir = 'images/09-Finance'
    os.makedirs(output_dir, exist_ok=True)

    # Render the graph
    output_path = os.path.join(output_dir, 'bgg_accelerator_loop.png')
    dot.render(os.path.join(output_dir, 'bgg_accelerator_loop'), format='png', cleanup=True)

    # Rename the output file to remove the .gv extension
    os.rename(os.path.join(output_dir, 'bgg_accelerator_loop.png'), output_path)

    print(f"Diagram saved to {output_path}")

if __name__ == "__main__":
    generate_bgg_diagram()
