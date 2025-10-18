import graphviz

def generate_aiyagari_loop_diagram():
    """
    Generates a diagram illustrating the nested loop algorithm for solving the Aiyagari model.
    """
    dot = graphviz.Digraph('Aiyagari_Equilibrium_Loop', comment='Aiyagari Model Solution Algorithm')
    dot.attr(rankdir='TB', splines='ortho')
    dot.attr('node', shape='box', style='rounded', fontname='Helvetica', fontsize='10')

    # --- Outer Loop ---
    with dot.subgraph(name='cluster_outer') as c:
        c.attr(label='Outer Loop: Find Equilibrium Interest Rate (r*)', style='rounded', color='blue', fontname="Helvetica", fontsize="12", penwidth='2')
        c.node('Guess_r', '1. Guess an interest rate (r)')
        c.node('Demand_K', '2. Calculate Firm Capital Demand:\nKd = f\'(r)')
        c.node('Supply_K', '3. Calculate Household Capital Supply (Ks)')
        c.node('Check', '4. Check for Market Clearing:\nIs Kd ≈ Ks?', shape='diamond', style='rounded,filled', color='lightyellow')
        c.node('Update_r', '5. Update guess for r\n(e.g., using bisection)')

        c.edge('Guess_r', 'Demand_K')
        c.edge('Demand_K', 'Supply_K')
        c.edge('Supply_K', 'Check')
        c.edge('Check', 'Update_r', label=' No ')
        c.edge('Update_r', 'Guess_r', style='dashed')

    # --- Inner Loop (within Supply_K) ---
    with dot.subgraph(name='cluster_inner') as c:
        c.attr(label='Inner Loop: Calculate Ks for a given r', style='rounded,dashed', color='green', fontname="Helvetica", fontsize="10")
        c.node_attr.update(style='filled', color='lightgreen')
        c.node('Solve_HH', '3a. Solve Household DP problem for policy function g(a,y)\n(Value Function Iteration)')
        c.node('Simulate', '3b. Find stationary distribution Φ(a,y)\n(Simulate many households using g(a,y))')
        c.node('Aggregate', '3c. Aggregate to find total savings:\nKs = E[a] under Φ(a,y)')

        c.edge('Solve_HH', 'Simulate', style='dashed')
        c.edge('Simulate', 'Aggregate', style='dashed')

    # --- Final Result ---
    dot.node('Equilibrium', 'Equilibrium Found!\n(r*, g*, Φ*)', shape='egg', style='filled', color='gold')
    dot.edge('Check', 'Equilibrium', label=' Yes ')

    # Connect outer loop to inner loop
    dot.edge('Demand_K', 'Solve_HH', lhead='cluster_inner', style='invis', minlen='0')
    dot.edge('Aggregate', 'Check', ltail='cluster_inner', style='invis', minlen='0')

    # Render and save
    import os
    save_dir = 'images'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_path = os.path.join(save_dir, 'aiyagari_equilibrium_loop')
    dot.render(save_path, format='png', view=False, cleanup=True)
    print(f"Diagram '{save_path}.png' created successfully.")

if __name__ == '__main__':
    generate_aiyagari_loop_diagram()