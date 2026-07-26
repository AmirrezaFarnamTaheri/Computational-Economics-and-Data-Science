import os

import graphviz


def generate_diagram():
    dot = graphviz.Digraph(comment="RL Loop", format="png")
    dot.attr(dpi="300")
    dot.attr(bgcolor="transparent")

    dot.attr("node", shape="box", style="rounded", fontname="Helvetica", fontsize="14")
    dot.attr("edge", fontname="Helvetica", fontsize="12")
    dot.attr(rankdir="LR", size="8,5")

    dot.node("Agent", "Agent", height="1.2", width="2.2")
    dot.node("Env", "Environment", height="1.2", width="2.2")

    dot.edge("Agent", "Env", label=" Action (A_t) ")
    dot.edge("Env", "Agent", label=" State (S_{t+1})\nReward (R_{t+1}) ")

    # Label is handled in notebook caption usually, but let's keep it clean
    # dot.graph_attr['label'] = '\nFigure 1: The Agent-Environment Interaction Loop'
    # dot.graph_attr['labelloc'] = 't'
    # dot.graph_attr['fontsize'] = '18'

    output_dir = "images/07-Machine-Learning"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "rl_loop_diagram")
    dot.render(output_path, cleanup=True)
    print(f"Generated {output_path}.png")


if __name__ == "__main__":
    generate_diagram()
