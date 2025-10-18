import sys

def fix_latex_in_notebook(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # This is the specific string to be replaced
    # The user input shows "\\ " which in a python string is "\\\\ "
    # The correct replacement is "\\\\" which in a python string is "\\\\\\\\"
    # Let's be very specific to avoid unintended replacements
    erroneous_string = '"$$ \\\\nabla f(x) = \\\\begin{bmatrix} \\\\frac{\\partial f}{\\partial x_1} \\\\ \\\\vdots \\\\ \\\\frac{\\partial f}{\\partial x_n} \\\\end{bmatrix} $$\\n"'
    corrected_string = '"$$ \\\\nabla f(x) = \\\\begin{bmatrix} \\\\frac{\\partial f}{\\partial x_1} \\\\\\\\ \\\\vdots \\\\\\\\ \\\\frac{\\partial f}{\\partial x_n} \\\\end{bmatrix} $$\\n"'

    erroneous_string_2 = '"$$ J_F(x) = \\\\begin{bmatrix} \\\\frac{\\partial F_1}{\\partial x_1} & \\\\cdots & \\\\frac{\\partial F_1}{\\partial x_n} \\\\ \\\\vdots & \\\\ddots & \\\\vdots \\\\ \\\\frac{\\partial F_m}{\\partial x_1} & \\\\cdots & \\\\frac{\\partial F_m}{\\partial x_n} \\\\end{bmatrix} = \\\\begin{bmatrix} - & \\\\nabla F_1(x)^T & - \\\\ & \\\\vdots & \\\\ - & \\\\nabla F_m(x)^T & - \\\\end{bmatrix} $$"'
    corrected_string_2 = '"$$ J_F(x) = \\\\begin{bmatrix} \\\\frac{\\partial F_1}{\\partial x_1} & \\\\cdots & \\\\frac{\\partial F_1}{\\partial x_n} \\\\\\\\ \\\\vdots & \\\\ddots & \\\\vdots \\\\\\\\ \\\\frac{\\partial F_m}{\\partial x_1} & \\\\cdots & \\\\frac{\\partial F_m}{\\partial x_n} \\\\end{bmatrix} = \\\\begin{bmatrix} - & \\\\nabla F_1(x)^T & - \\\\\\\\ & \\\\vdots & \\\\\\\\ - & \\\\nabla F_m(x)^T & - \\\\end{bmatrix} $$"'

    erroneous_string_3 = '"$$ H_f(x) = \\\\begin{bmatrix} \\\\frac{\\partial^2 f}{\\partial x_1^2} & \\\\frac{\\partial^2 f}{\\partial x_1 \\\\partial x_2} & \\\\cdots & \\\\frac{\\partial^2 f}{\\partial x_1 \\\\partial x_n} \\\\ \\\\vdots & \\\\vdots & \\\\ddots & \\\\vdots \\\\ \\\\frac{\\partial^2 f}{\\partial x_n \\\\partial x_1} & \\\\frac{\\partial^2 f}{\\partial x_n \\\\partial x_2} & \\\\cdots & \\\\frac{\\partial^2 f}{\\partial x_n^2} \\\\end{bmatrix} $$"'
    corrected_string_3 = '"$$ H_f(x) = \\\\begin{bmatrix} \\\\frac{\\partial^2 f}{\\partial x_1^2} & \\\\frac{\\partial^2 f}{\\partial x_1 \\\\partial x_2} & \\\\cdots & \\\\frac{\\partial^2 f}{\\partial x_1 \\\\partial x_n} \\\\\\\\ \\\\vdots & \\\\vdots & \\\\ddots & \\\\vdots \\\\\\\\ \\\\frac{\\partial^2 f}{\\partial x_n \\\\partial x_1} & \\\\frac{\\partial^2 f}{\\partial x_n \\\\partial x_2} & \\\\cdots & \\\\frac{\\partial^2 f}{\\partial x_n^2} \\\\end{bmatrix} $$"'

    new_content = content.replace('\\\\ ', '\\\\\\\\')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python fix_latex.py <path_to_notebook>")
        sys.exit(1)

    notebook_path = sys.argv[1]
    fix_latex_in_notebook(notebook_path)
    print(f"Fixed LaTeX in {notebook_path}")