import graphviz

def generate_box_jenkins_flowchart():
    """
    Generates and saves a flowchart for the Box-Jenkins methodology.
    """
    dot = graphviz.Digraph('Box-Jenkins-Methodology', comment='The Box-Jenkins Methodology')
    dot.attr('node', shape='box', style='rounded', fontname='Helvetica', fontsize='10')
    dot.attr('edge', fontname='Helvetica', fontsize='10')

    # Define nodes
    dot.node('A', 'Start: Obtain Time Series Data')
    dot.node('B', '1. Identification/n- Plot data, check for stationarity (e.g., ADF test)./n- If non-stationary, apply transformations (e.g., differencing)./n- Examine ACF/PACF of stationary series to select candidate models (p, d, q).')
    dot.node('C', '2. Estimation\nEstimate parameters of candidate model(s) using Maximum Likelihood Estimation (MLE).')
    dot.node('D', '3. Diagnostic Checking\n- Analyze model residuals.\n- Are they white noise? (Check residual ACF/PACF, Ljung-Box test).')
    dot.node('E', 'Model is adequate.\nUse for forecasting or analysis.')
    dot.node('F', 'Model is inadequate.\nReturn to Identification stage.')

    # Define edges
    dot.edge('A', 'B')
    dot.edge('B', 'C')
    dot.edge('C', 'D')
    dot.edge('D', 'E', label='  Yes  ')
    dot.edge('D', 'F', label='  No  ')
    dot.edge('F', 'B')

    # Render and save
    # Ensure the images directory exists
    import os
    if not os.path.exists('images'):
        os.makedirs('images')

    dot.render('images/box_jenkins_methodology', format='png', view=False, cleanup=True)
    print("Flowchart 'images/png/box_jenkins_methodology.png' created successfully.")

if __name__ == '__main__':
    generate_box_jenkins_flowchart()