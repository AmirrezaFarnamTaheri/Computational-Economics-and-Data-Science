import json
import sys

def add_granularity(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)

    for cell in notebook['cells']:
        if cell['cell_type'] == 'markdown':
            source = cell.get('source', [])
            new_source = []
            for line in source:
                if 'An AR model can be thought of as modeling a series that experiences random shocks' in line:
                    line += (
                        '\\n\\n'
                        '> 📖 **First Principles: The Lag Operator**\\n'
                        '> The lag operator, denoted by \\(L\\), is a mathematical tool used to represent the relationship between a value at time \\(t\\) and its value at a previous time. It simplifies the notation of time series models by transforming an equation into a more compact polynomial form. For example, \\(Ly_t = y_{t-1}\\) means that applying the lag operator to \\(y_t\\) gives its value in the previous period.'
                    )
                elif 'An **ARMA(p,q)** model combines the AR(p) and MA(q) components:' in line:
                    line += (
                        '\\n\\n'
                        '> 📖 **First Principles: Parsimony**\\n'
                        '> In the context of statistical modeling, parsimony refers to the principle of explaining a phenomenon with the simplest possible model. A parsimonious model has just enough parameters to represent the underlying data structure without overfitting to noise. This approach is favored because it often leads to better generalization and forecasting performance.'
                    )
                new_source.append(line)
            cell['source'] = new_source

    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        add_granularity(sys.argv[1])
