import re
from itertools import product
from parameters import *


def bp(orig, a):
        if a < 0:
            return 0
        if a > 0:
            return 1
        return orig


class Variable_handler():
    def __init__(self, equation_string, name_string):
        self.equation = ''
        self.rhs = ''
        self.truth_table = []
        self.sgn_vector = []
        self.input_variables = []
        self.num_vars = 0
        self.name = ''
        self.update_values = []
        self.boolean_function = ''

        maybe_equation = self.extract_equation(equation_string)
        if maybe_equation is not None:
            self.equation = maybe_equation
            variable_names_original = self.extract_variables(self.equation)
            self.num_vars = len(variable_names_original)
            for i in range(self.num_vars):
                variable_names_original[i] = re.sub(r'\,', '_c_', variable_names_original[i])
            variable_names_extended = self.extend_variables_with_x(variable_names_original)
            self.input_variables = variable_names_extended
            rhs = self.equation.split("=")[1]
            self.rhs = re.sub(r',', '_c_', rhs)
        name_extended = self.extend_variables_with_x([name_string])
        self.name = name_extended[0]
        


    def extract_equation(self, latex_string):
        # Define the regular expression pattern to match the equation
        pattern = r'\\begin{equation}\s*(.*?)\s*\\end{equation}'

        # Use re.DOTALL to match across multiple lines
        match = re.search(pattern, latex_string, re.DOTALL)

        if match:
            # Extract the equation
            equation = match.group(1)
            def replace_frac(match):
                numerator = match.group(1)
                denominator = match.group(2)
                return f"(({numerator})/({denominator}))"

            # First, handle fractions
            #pattern = r'\\frac\{([^{}]+)\}\{([^{}]+)\}'
            pattern = r'\\frac\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}'
            equation = re.sub(pattern, replace_frac, equation)
            #equation = re.sub(pattern, r'((\1)/(\2))', equation)
            print(equation)
            
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


    def extract_variables(self, equation):
        # Find the content inside normal brackets ()
        match = re.search(r'\((.*?)\)', equation)
        
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
        for res in results:
            print(res)
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
        self.boolean_function = boolean_function
        return boolean_function
