import graphviz

def generate_fama_macbeth_diagram():
    """
    Generates and saves a diagram illustrating the Fama-MacBeth two-pass procedure.
    """
    dot = graphviz.Digraph('Fama_MacBeth', comment='Fama-MacBeth Two-Pass Regression')
    dot.attr(rankdir='TB', splines='ortho', concentrate='true')

    with dot.subgraph(name='cluster_pass1') as c:
        c.attr(label='Pass 1: Time-Series Regressions (run for each asset N)', style='rounded', color='blue', fontname="Helvetica", fontsize="12")
        c.node_attr.update(style='filled', color='lightblue', shape='box', fontname="Helvetica", fontsize="10")

        c.node('TS_Input', 'Inputs:\n- Asset N Excess Returns (R_Nt)\n- Factor Returns (F_t)')
        c.node('TS_Reg', f'Regression (for each asset N):\nR_Nt = α_N + β_N1*F_1t + ... + β_NK*F_Kt + ε_Nt')
        c.node('TS_Output', 'Output:\nEstimated Betas (β_N1, ..., β_NK)\nfor each asset N')
        c.edge('TS_Input', 'TS_Reg')
        c.edge('TS_Reg', 'TS_Output')

    with dot.subgraph(name='cluster_pass2') as c:
        c.attr(label='Pass 2: Cross-Sectional Regressions (run for each time period T)', style='rounded', color='green', fontname="Helvetica", fontsize="12")
        c.node_attr.update(style='filled', color='lightgreen', shape='box', fontname="Helvetica", fontsize="10")

        c.node('CS_Input', 'Inputs (for time t):\n- All Asset Returns (R_1t, ..., R_Nt)\n- All Asset Betas (β_1, ..., β_N)')
        c.node('CS_Reg', f'Regression (for each time t):\nR_it = λ_0t + λ_1t*β_i1 + ... + λ_Kt*β_iK + u_it')
        c.node('CS_Output', 'Output:\nTime series of risk premia estimates\n(λ_1t, ..., λ_Kt)')
        c.edge('CS_Input', 'CS_Reg')
        c.edge('CS_Reg', 'CS_Output')

    with dot.subgraph(name='cluster_final') as c:
        c.attr(label='Final Step: Test Significance', style='rounded', color='purple', fontname="Helvetica", fontsize="12")
        c.node_attr.update(style='filled', color='lavender', shape='box', fontname="Helvetica", fontsize="10")
        c.node('Final_Test', 'Calculate time-series average of λ_kt.\nUse t-test (with Newey-West correction)\nto see if average premium is significantly different from zero.')

    dot.edge('TS_Output', 'CS_Input', lhead='cluster_pass2', ltail='cluster_pass1', style='dashed', arrowhead='normal', minlen='2')
    dot.edge('CS_Output', 'Final_Test', lhead='cluster_final', ltail='cluster_pass2', style='dashed', arrowhead='normal', minlen='2')

    # Render and save
    import os
    if not os.path.exists('images'):
        os.makedirs('images')

    dot.render('images/fama_macbeth_procedure', format='png', view=False, cleanup=True)
    print("Diagram 'images/png/fama_macbeth_procedure.png' created successfully.")

if __name__ == '__main__':
    generate_fama_macbeth_diagram()