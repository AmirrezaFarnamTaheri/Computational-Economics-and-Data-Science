import graphviz
import os

def generate_ordered_dict_diagram():
    """
    Generates a diagram illustrating the Python 3.7+ ordered dictionary implementation.
    """
    dot = graphviz.Digraph('Ordered_Dict_Structure', comment='Python 3.7+ Dict Implementation')
    dot.attr(rankdir='LR', splines='ortho')
    dot.attr('node', shape='record', fontname='Helvetica', fontsize='12')

    # Indices Array (Sparse)
    indices_label = "{ <h> Indices Array (Sparse) | " + \
                    "{ <0> 0 | <1> 1 | <2> 2 | <3> 3 | <4> 4 | <5> 5 | <6> 6 | <7> 7 } | " + \
                    "{ -1 | <e0> 0 | -1 | <e2> 2 | -1 | <e1> 1 | -1 | -1 } }"
    dot.node('Indices', indices_label, color='blue')

    # Entries Array (Dense)
    entries_label = "{ <h> Entries Array (Dense) | " + \
                    "{ Index | Hash | Key | Value } | " + \
                    "{ <r0> 0 | <h0> ... | 'apple' | 100 } | " + \
                    "{ <r1> 1 | <h1> ... | 'banana' | 200 } | " + \
                    "{ <r2> 2 | <h2> ... | 'cherry' | 300 } }"
    dot.node('Entries', entries_label, color='green')

    # Edges from indices to entries
    dot.edge('Indices:e0', 'Entries:r0', color='red', constraint='false')
    dot.edge('Indices:e1', 'Entries:r1', color='red', constraint='false')
    dot.edge('Indices:e2', 'Entries:r2', color='red', constraint='false')

    # Descriptions
    dot.node('Desc1', '1. Key hash determines index in Indices Array', shape='plaintext')
    dot.node('Desc2', '2. Value in Indices Array points to row in Entries Array', shape='plaintext')
    dot.node('Desc3', '3. Entries are stored densely, preserving insertion order', shape='plaintext')

    dot.edge('Desc1', 'Indices:h', style='dashed', color='gray')
    dot.edge('Desc2', 'Entries:h', style='dashed', color='gray')

    # Render
    save_dir = 'images/01-Foundations'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    save_path = os.path.join(save_dir, '1.7-ordered-dict')
    dot.render(save_path, format='png', view=False, cleanup=True)
    print(f"Diagram '{save_path}.png' created successfully.")

if __name__ == '__main__':
    generate_ordered_dict_diagram()
