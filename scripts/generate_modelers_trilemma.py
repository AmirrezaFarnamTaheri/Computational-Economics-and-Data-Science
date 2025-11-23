import matplotlib.pyplot as plt
import numpy as np

def create_trilemma_diagram():
    fig, ax = plt.subplots(figsize=(8, 8))

    # Triangle vertices
    # Top: Precision
    # Bottom Left: Realism
    # Bottom Right: Generality
    vertices = np.array([[0.5, 0.9], [0.1, 0.1], [0.9, 0.1]])
    labels = ["Precision", "Realism", "Generality"]

    # Draw the triangle
    triangle = plt.Polygon(vertices, fill=False, edgecolor='black', linewidth=2)
    ax.add_patch(triangle)

    # Add labels for vertices
    for i, (x, y) in enumerate(vertices):
        # Adjust text position slightly
        if i == 0: # Top
            xytext = (0, 15)
            va = 'bottom'
        elif i == 1: # Bottom Left
            xytext = (-15, -15)
            va = 'top'
        else: # Bottom Right
            xytext = (15, -15)
            va = 'top'

        ax.annotate(labels[i], (x, y), xytext=xytext, textcoords='offset points',
                    ha='center', va=va, fontsize=14, fontweight='bold')

    # Add labels for edges (The Trade-offs)
    # Edge 1: Precision - Realism (Left) -> Sacrifices Generality
    # Edge 2: Realism - Generality (Bottom) -> Sacrifices Precision
    # Edge 3: Generality - Precision (Right) -> Sacrifices Realism

    edge_centers = (vertices + np.roll(vertices, -1, axis=0)) / 2
    edge_labels = [
        "Sacrifices\nGenerality",
        "Sacrifices\nPrecision",
        "Sacrifices\nRealism"
    ]

    # Adjust positions manually for better fit
    # Left edge (Precision-Realism)
    ax.text(0.25, 0.5, "Analytical\nModels", ha='right', va='center', fontsize=12, color='blue')

    # Bottom edge (Realism-Generality)
    ax.text(0.5, 0.05, "Agent-Based\nModels", ha='center', va='top', fontsize=12, color='green')

    # Right edge (Generality-Precision)
    ax.text(0.75, 0.5, "General\nEquilibrium", ha='left', va='center', fontsize=12, color='red')

    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')

    plt.title("The Modeler's Trilemma", fontsize=16, y=0.95)

    # Save
    import os
    os.makedirs('images/png', exist_ok=True)
    plt.savefig('images/png/1.1-modelers-trilemma.png', dpi=300, bbox_inches='tight')
    print("Trilemma diagram created.")

if __name__ == "__main__":
    create_trilemma_diagram()
