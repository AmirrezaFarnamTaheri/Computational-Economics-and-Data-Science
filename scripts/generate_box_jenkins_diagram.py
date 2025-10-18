import graphviz

# Create a new directed graph
dot = graphviz.Digraph('BoxJenkins', comment='The Box-Jenkins Methodology')
dot.attr(rankdir='TB', size='8,5', label='The Box-Jenkins Methodology', fontsize='20')

# Define nodes
dot.attr('node', shape='box', style='rounded,filled', fillcolor='lightblue', fontname='Helvetica')
dot.node('A', '1. Identification\n- Check Stationarity (Difference if needed)\n- Plot ACF/PACF to find candidate (p,q) orders')
dot.node('B', '2. Estimation\n- Estimate parameters of candidate models\n(e.g., via Maximum Likelihood)')
dot.node('C', '3. Diagnostic Checking\n- Analyze model residuals (ACF, Ljung-Box test)\n- Are residuals white noise?')

dot.attr('node', shape='diamond', style='filled', fillcolor='lightyellow')
dot.node('D', 'Model Adequate?')

# Define edges
dot.edge('A', 'B', 'Select Candidate(s)')
dot.edge('B', 'C', 'Fit Model')
dot.edge('C', 'D')
dot.edge('D', 'A', 'No (Misspecified)')

# 'Yes' path
dot.attr('node', shape='ellipse', style='filled', fillcolor='lightgreen')
dot.node('E', 'Model is Ready for Forecasting')
dot.edge('D', 'E', 'Yes')

# Render the graph
output_path = 'images/box_jenkins_methodology'
dot.render(output_path, format='png', view=False, cleanup=True)

print(f"Diagram saved to {output_path}.png")