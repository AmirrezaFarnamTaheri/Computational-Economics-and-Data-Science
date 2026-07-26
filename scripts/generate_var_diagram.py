import os

import graphviz


def generate_var_diagram():
    output_dir = "images/08-Time-Series"
    os.makedirs(output_dir, exist_ok=True)

    dot = graphviz.Digraph(comment="VAR Identification")
    dot.attr(rankdir="TB", dpi="300", bgcolor="white")
    dot.attr(
        "node",
        shape="box",
        style="filled",
        fillcolor="white",
        fontname="Helvetica",
        fontsize="12",
    )
    dot.attr("edge", fontname="Helvetica", fontsize="10")

    # Structural Shocks
    with dot.subgraph(name="cluster_shocks") as c:
        c.attr(label="Structural Shocks (Uncorrelated)", style="dashed", color="gray")
        c.node("u_gdp", "u_GDP\n(Supply/Demand)", shape="circle", fillcolor="#e6f3ff")
        c.node("u_inf", "u_Inflation\n(Cost Push)", shape="circle", fillcolor="#e6f3ff")
        c.node(
            "u_rate", "u_Rate\n(Monetary Policy)", shape="circle", fillcolor="#e6f3ff"
        )

    # Observed Variables
    with dot.subgraph(name="cluster_vars") as c:
        c.attr(label="Observed Variables (Time t)", style="solid", color="black")
        c.node("y_gdp", "GDP Growth", style="filled", fillcolor="#fff2cc")
        c.node("y_inf", "Inflation", style="filled", fillcolor="#fff2cc")
        c.node("y_rate", "Fed Funds Rate", style="filled", fillcolor="#fff2cc")

    # Edges (Cholesky Ordering: GDP -> Inflation -> Rate)

    # 1. GDP is affected by its own structural shock only (contemporaneously)
    dot.edge("u_gdp", "y_gdp")

    # 2. Inflation is affected by its own shock AND GDP shock
    dot.edge("u_inf", "y_inf")
    dot.edge("y_gdp", "y_inf", label="Contemporaneous")

    # 3. Rate is affected by its own shock AND GDP AND Inflation
    dot.edge("u_rate", "y_rate")
    dot.edge("y_gdp", "y_rate")
    dot.edge("y_inf", "y_rate", label="Contemporaneous")

    # Invisible edges to align shocks with vars
    dot.edge("u_gdp", "y_gdp", style="invis")
    dot.edge("u_inf", "y_inf", style="invis")
    dot.edge("u_rate", "y_rate", style="invis")

    output_path = os.path.join(output_dir, "var_identification_diagram")
    dot.render(output_path, format="png", cleanup=True)
    print(f"Generated {output_path}.png")


if __name__ == "__main__":
    generate_var_diagram()
