import re
from parameters import *
from variable_handler import Variable_handler
from equations import edes
from sympy import simplify_logic


def variable_latex_to_python(latex_string):
    latex_string = re.sub(r'\,', '_c_', latex_string)
    latex_string = re.sub(r'\{', '_lcb_', latex_string)
    latex_string = re.sub(r'\}', '_rcb_', latex_string)
    # Replace ^ with underscores
    latex_string = re.sub(r'\^', '_pwr_', latex_string)
    # Replace \mhyphen with underscores
    latex_string = re.sub(r'\\mhyphen ', '_hyp_', latex_string)
    print(latex_string)
    return latex_string



def reconstruct_latex(equation_string):
    # Replace underscores and symbols back to their LaTeX equivalents
    equation = re.sub(r'_lcb_', '{', equation_string)  # Replace custom _lcb_ with {
    equation = re.sub(r'_rcb_', '}', equation)         # Replace custom _rcb_ with }
    equation = re.sub(r'_pwr_', '^', equation)         # Replace custom _pwr_ with ^
    equation = re.sub(r'_hyp_', r'\\mhyphen ', equation)  # Replace custom _hyp_ with \mhyphen
    equation = re.sub(r'&', 'and', equation)           # Replace & with "and"
    equation = re.sub(r'\|', 'or', equation)           # Replace | with "or"
    equation = re.sub(r'!', 'not ', equation)          # Replace ! with "not"

    # Wrap the result back into LaTeX equation format
    latex_string = f"\\begin{{equation}}\n{equation}\n\\end{{equation}}"

    return latex_string




lh_pit = Variable_handler(edes[0])
lh_pit.infer_boolean_function()
print(simplify_logic(lh_pit.boolean_function))

lh_blood = Variable_handler(edes[1])
lh_blood.infer_boolean_function()
print(simplify_logic(lh_blood.boolean_function))
"""
# Example usage
num_vars = 3  # Number of input variables
output_column = [0, 1, 1, 0, 1, 0, 1, 0]  # Output column (example)
truth_table = generate_truth_table(num_vars, output_column)
boolean_function = infer_boolean_function(truth_table, num_vars)

print("Truth Table:")
for row in truth_table:
    print(row)

print("\nInferred Boolean Function (SOP):")
print(boolean_function)
"""

"""
with open("parameter_names.txt", "r") as f:
    with open("parameter_names_python.txt", "w") as of:
        for line in f:
            if line != "":
                new_name = variable_latex_to_python(line)
                print(new_name, file=of)
"""
