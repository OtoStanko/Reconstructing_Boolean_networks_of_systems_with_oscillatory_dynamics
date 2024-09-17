import re
from itertools import product
from parameters import *



def extract_variables(string):
    # Find the content inside normal brackets ()
    match = re.search(r'\((.*?)\)', string)
    
    if match:
        # Extract the content inside the brackets
        variables_str = match.group(1)
        # Split the string by commas and strip any extra spaces around the variable names
        variables_list = [var.strip() for var in variables_str.split(',')]
        return variables_list
    else:
        return []


def extend_variables_with_x(variables):
    extended = []
    for variable in variables:
        extended.append("X__lcb_" + variable + "_rcb_")
    return extended


def variable_latex_to_python(latex_string):
    latex_string = re.sub(r'\{', '_lcb_', latex_string)
    latex_string = re.sub(r'\}', '_rcb_', latex_string)
    # Replace ^ with underscores
    latex_string = re.sub(r'\^', '_pwr_', latex_string)
    # Replace \mhyphen with underscores
    latex_string = re.sub(r'\\mhyphen ', '_hyp_', latex_string)
    print(latex_string)
    return latex_string



def extract_equation(latex_string):
    # Define the regular expression pattern to match the equation
    pattern = r'\\begin{equation}\s*(.*?)\s*\\end{equation}'

    # Use re.DOTALL to match across multiple lines
    match = re.search(pattern, latex_string, re.DOTALL)

    if match:
        # Extract the equation
        equation = match.group(1)

        # Remove curly brackets
        # find better solution, maybe more underscores
        equation = re.sub(r'\{', '_lcb_', equation)
        equation = re.sub(r'\}', '_rcb_', equation)
        # Remove the line cuts
        equation = re.sub(r'\\\\', '', equation)
        # Replace ^ with underscores
        equation = re.sub(r'\^', '_pwr_', equation)
        # Replace \mhyphen with underscores
        equation = re.sub(r'\\mhyphen ', '_hyp_', equation)
        # Replace ands, ors and negations
        equation = re.sub(r'and', '&', equation)
        equation = re.sub(r'or', '|', equation)
        equation = re.sub(r'not ', '!', equation)

        return equation
    else:
        return None


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


latex_string = r"""
\begin{equation}
    h_{LH_{pit}}(E2, P4, G\mhyphen R, LH_{pit}) = (b^{LH}_{syn}+k^{LH}_{E2} * X_{E2}) * (1-X_{P4}) \\ -(b^{LH}_{Rel}+k^{LH}_{G\mhyphen R} * X_{G\mhyphen R}) * X_{LH_{pit}}
\end{equation}
"""

# Function to generate a truth table
def generate_truth_table(num_vars):
    truth_table = list(product([0, 1], repeat=num_vars))
    reversed_truth_table = [row[::-1] for row in truth_table]
    return reversed_truth_table
    #truth_table = [list(row) for row in enumerate(input_combinations)]
    #return truth_table


# Function to infer the boolean function from the truth table (SOP form)
def infer_boolean_function(truth_table, num_vars):
    min_terms = []
    for row in truth_table:
        inputs = row[:num_vars]
        output = row[-1]
        if output == 1:  # Only consider rows where output is 1
            term = []
            for i, val in enumerate(inputs):
                if val == 1:
                    term.append(f"x{i+1}")
                else:
                    term.append(f"~x{i+1}")
            min_terms.append(" & ".join(term))
    # Create the sum of products (OR of AND terms)
    if min_terms:
        boolean_function = " | ".join(min_terms)
    else:
        boolean_function = "0"  # If no min-terms, the function is always false
    return boolean_function


def evaluate_equation(latex_string):
    extracted_equation = extract_equation(latex_string)
    print(extracted_equation)
    extracted_variables = extract_variables(extracted_equation)
    print(extracted_variables)
    extended_variables = extend_variables_with_x(extracted_variables)
    print(extended_variables)

    num_vars = len(extracted_variables)
    rhs = extracted_equation.split("=")[1]
    truth_table = generate_truth_table(num_vars)
    results = list()
    for row in truth_table:
        print()
        print(rhs)
        print()
        new_rhs = rhs
        #rhs_tmp = rhs.copy()
        for i in range(num_vars):
            new_rhs = new_rhs.replace(extended_variables[i], str(row[i]))
        print(new_rhs)
        lhs = eval(new_rhs)
        results.append(lhs)
    for res in results:
        print(res)
    #reconstructed = reconstruct_latex(extracted_equation)
    #print(reconstructed)


evaluate_equation(latex_string)

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
