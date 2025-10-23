from graphviz import Digraph
import os

def create_aiyagari_loop_diagram():
    """
    Generates a diagram illustrating the Aiyagari model's general equilibrium solution loop.
    """
    dot = Digraph(comment='Aiyagari Equilibrium Loop')
    dot.attr('graph', rankdir='TB', bgcolor='transparent', label='Solving the Aiyagari Model', fontname='Helvetica', fontsize='20', labelloc='t')

    # Node attributes
    dot.attr('node', shape='box', style='rounded,filled', fontname='Helvetica')

    # Outer Loop
    with dot.subgraph(name='cluster_outer') as c:
        c.attr(label='Outer Loop: Find Equilibrium Interest Rate (r*)', style='rounded,dashed', color='firebrick')
        c.node('Guess_r', '1. Guess an Interest Rate, r', fillcolor='coral')
        c.node('Demand_K', '2. Firms: Calculate Capital Demand\\nKd = f(r)', fillcolor='skyblue')
        c.node('Supply_K', '3. Households: Calculate Capital Supply\\nKs(r) [Inner Loop]', shape='box3d', fillcolor='gold')
        c.node('Check', '4. Check Market Clearing\\nIs Kd ≈ Ks?', shape='diamond', fillcolor='lightgreen')
        c.node('Update_r', '5. Update r using Bisection', fillcolor='coral')

        c.edge('Guess_r', 'Demand_K')
        c.edge('Guess_r', 'Supply_K')
        c.edge('Demand_K', 'Check')
        c.edge('Supply_K', 'Check')
        c.edge('Check', 'Update_r', label='No (Kd != Ks)')
        c.edge('Update_r', 'Guess_r', label='Loop')

    # Inner Loop
    with dot.subgraph(name='cluster_inner') as c:
        c.attr(label='Inner Loop: Household Behavior for a given r', style='rounded,dashed', color='darkblue')
        c.node('VFI', '3a. Solve Bellman Equation via\\nValue Function Iteration (VFI)', fillcolor='goldenrod1')
        c.node('Policy', "3b. Find Optimal Savings Policy\\na' = g(a, y)", fillcolor='goldenrod1')
        c.node('Simulate', '3c. Simulate Many Households to find\\nStationary Distribution Φ(a, y)', fillcolor='goldenrod1')
        c.node('Aggregate', '3d. Aggregate to get Total Supply\\nKs = E[a] under Φ', fillcolor='goldenrod1')

        c.edge('VFI', 'Policy')
        c.edge('Policy', 'Simulate')
        c.edge('Simulate', 'Aggregate')

    # Connect Inner loop to Outer loop
    dot.edge('Aggregate', 'Supply_K', style='invis') # For layout
    dot.edge('Check', 'Equilibrium', label='Yes (Kd = Ks)', color='darkgreen', fontcolor='darkgreen')
    dot.node('Equilibrium', 'Equilibrium Found!\\nr* and Stationary Distribution Φ*(a,y)', shape='star', fillcolor='limegreen')

    # Save the file
    output_dir = 'images/10-Specialized-Models'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_path = os.path.join(output_dir, 'aiyagari_equilibrium_loop')

    dot.render(output_path, format='png', view=False, cleanup=True)

    return f"{output_path}.png"

if __name__ == "__main__":
    generated_file = create_aiyagari_loop_diagram()
    print(f"Diagram saved to: {generated_file}")
