import re
from itertools import product
from parameters import *
from predator_prey_parameters import *
from sympy import simplify_logic


def bp(orig, a):
        if a < 0:
            return 0
        if a > 0:
            return 1
        return orig

def remove_curlies_andX(string):
    string = re.sub(r'X_', r'', string)
    string = re.sub(r'_lcb_', r'', string)  # Replace custom _lcb_ with {
    string = re.sub(r'_rcb_', r'', string)
    return string

def variable_latex_to_python(latex_string):
    latex_string = re.sub(r'\,', '_c_', latex_string)
    latex_string = re.sub(r'\{', '_lcb_', latex_string)
    latex_string = re.sub(r'\}', '_rcb_', latex_string)
    # Replace ^ with underscores
    latex_string = re.sub(r'\^', '_pwr_', latex_string)
    # Replace \mhyphen with underscores
    latex_string = re.sub(r'\\mhyphen ', '_hyp_', latex_string)
    return latex_string


class VariableHandler():
    def __init__(self, equation_string):
        self.equation = None
        self.rhs = ''
        self.truth_table = []
        self.sgn_vector = []
        self.input_variables = []
        self.input_variables_reduced = []
        self.num_vars = 0
        self.name = ''
        self.update_values = []
        self.boolean_function = None
        self.boolean_function_latex = None


        maybe_equation = self.extract_equation(equation_string)
        if maybe_equation is not None:
            self.equation = maybe_equation
            variable_names_original = self.extract_variables()
            self.num_vars = len(variable_names_original)
            for i in range(self.num_vars):
                variable_names_original[i] = re.sub(r'\,', '_c_', variable_names_original[i])
            variable_names_extended = self.extend_variables_with_x(variable_names_original)
            self.input_variables = variable_names_extended
            
            rhs = self.equation.split("=")[1]
            self.rhs = re.sub(r',', '_c_', rhs)

            name_string = self.extract_name_string()
            name_string = re.sub(r'\,', '_c_', name_string)
            name_extended = self.extend_variables_with_x([name_string])
            self.name = name_extended[0]

    
    def extract_name_string(self):
        # Regular expression pattern to match h_{ and capture nested curly braces
        #pattern = r'h_\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}'
        
        # Search for the first occurrence of the pattern
        name_part = self.equation.split('(')[0]
        name = name_part[7:-5]
        return name


    def extract_equation(self, string, latex=False):
        # Define the regular expression pattern to match the equation
        if latex:
            pattern = r'\\begin{equation}\s*(.*?)\s*\\end{equation}'

            # Use re.DOTALL to match across multiple lines
            match = re.search(pattern, string, re.DOTALL)
            if match:
                equation = match.group(1)
            else:
                print("No match!", string)
                return
        else:
            equation = string

        def replace_frac(match):
            numerator = match.group(1)
            denominator = match.group(2)
            return f"(({numerator})/({denominator}))"

        # First, handle fractions
        #pattern = r'\\frac\{([^{}]+)\}\{([^{}]+)\}'
        pattern = r'\\frac\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}'
        equation = re.sub(pattern, replace_frac, equation)
        #equation = re.sub(pattern, r'((\1)/(\2))', equation)

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


    def extract_variables(self):
        # Find the content inside normal brackets ()
        match = re.search(r'\((.*?)\)', self.equation)
        
        if match:
            # Extract the content inside the brackets
            variables_str = match.group(1)
            # Split the string by commas and strip any extra spaces around the variable names
            variables_list = [var.strip() for var in variables_str.split(', ')]
            return variables_list
        else:
            return []


    def extend_variables_with_x(self, variables):
        extended = []
        for variable in variables:
            extended.append("X__lcb_" + variable + "_rcb_")
        return extended


    # Function to generate a truth table
    def generate_truth_table(self):
        truth_table = list(product([0, 1], repeat=self.num_vars))
        reversed_truth_table = [row[::-1] for row in truth_table]
        self.truth_table = truth_table
        return truth_table
        #truth_table = [list(row) for row in enumerate(input_combinations)]
        #return truth_table


    def evaluate_equation(self):
        self.generate_truth_table()
        results = list()
        for row in self.truth_table:
            #print()
            #print(rhs)
            #print()
            new_rhs = self.rhs
            #rhs_tmp = rhs.copy()
            for i in range(self.num_vars):
                new_rhs = new_rhs.replace(self.input_variables[i], str(row[i]))
            #print(new_rhs)
            lhs = eval(new_rhs)
            sgn_lhs = 0
            if lhs > 0:
                sgn_lhs = 1
            elif lhs < 0:
                sgn_lhs = -1
            results.append(sgn_lhs)
        whole_table = []
        for i in range(len(self.truth_table)):
            whole_table.append([x for x in self.truth_table[i]] + [results[i]])
        self.sgn_vector = results
        return whole_table
        #reconstructed = reconstruct_latex(extracted_equation)
        #print(reconstructed)
    

    def generate_update_values(self):
        x_k_1 = []
        variable_index = self.input_variables.index(self.name)
        for i in range(len(self.truth_table)):
            x_k_1.append(bp(self.truth_table[i][variable_index], self.sgn_vector[i]))
        self.update_values = x_k_1


    def replace_match(self, match):
        index = int(match.group(1))  # Extract the number 'i' from 'x<i>'
        if index < len(self.input_variables):
            return self.input_variables[index]


    # Function to infer the boolean function from the truth table (SOP form)
    def infer_boolean_function(self):
        self.evaluate_equation()
        self.generate_update_values()
        min_terms = []
        for j in range(len(self.truth_table)):
            row = self.truth_table[j]
            inputs = row[:self.num_vars]
            output = self.update_values[j]
            if output == 1:  # Only consider rows where output is 1
                term = []
                for i, val in enumerate(inputs):
                    if val == 1:
                        term.append(f"x{i}")
                    else:
                        term.append(f"~x{i}")
                min_terms.append(" & ".join(term))
        # Create the sum of products (OR of AND terms)
        if min_terms:
            boolean_function = " | ".join(min_terms)
        else:
            boolean_function = "0"  # If no min-terms, the function is always false
        simplified_boolean_function = str(simplify_logic(boolean_function))
        pattern = r'x(\d+)'
        sbf_input_var_names = re.sub(pattern, self.replace_match, simplified_boolean_function)
        self.boolean_function = sbf_input_var_names
        for var_name in self.input_variables:
            if var_name in sbf_input_var_names:
                self.input_variables_reduced.append(var_name)
        return simplified_boolean_function


    def infer_boolean_function_latex(self):
        if self.boolean_function_latex is None:
            self.infer_boolean_function()
        sbf_plus_name = self.name + " = " + self.boolean_function
        self.boolean_function_latex = self.reconstruct_latex(sbf_plus_name)



    def boolean_function_to_aeon(self):
        if self.boolean_function is None:
            self.infer_boolean_function()
        functions = []
        name = remove_curlies_andX(self.name)
        aeon_boolean_function = remove_curlies_andX(self.boolean_function.replace("~", "!"))
        functions.append("$" + name + ": " + aeon_boolean_function)
        for i in range(len(self.input_variables_reduced)):
            var_name = remove_curlies_andX(self.input_variables_reduced[i])
            functions.append(var_name + " -? " + name)
        return functions



    def reconstruct_latex(self, equation_string):
        # Replace underscores and symbols back to their LaTeX equivalents
        equation = re.sub(r'_c_', r',', equation_string)
        equation = re.sub(r'_lcb_', r'{', equation)  # Replace custom _lcb_ with {
        equation = re.sub(r'_rcb_', r'}', equation)         # Replace custom _rcb_ with }
        equation = re.sub(r'_pwr_', r'^', equation)         # Replace custom _pwr_ with ^
        equation = re.sub(r'_hyp_', r'\\mhyphen ', equation)  # Replace custom _hyp_ with \mhyphen
        equation = re.sub(r'&', r'\\land', equation)           # Replace & with "and"
        equation = re.sub(r'\|', r'\\lor', equation)           # Replace | with "or"
        equation = re.sub(r'~', r'\\neg ', equation)          # Replace ! with "not"

        # Wrap the result back into LaTeX equation format
        latex_string = f"""\\begin{{equation}} {equation} \\end{{equation}}"""
        print(latex_string)
        return latex_string
    
