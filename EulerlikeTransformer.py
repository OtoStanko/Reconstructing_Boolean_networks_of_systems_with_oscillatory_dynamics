import re
from itertools import product
from sympy import simplify_logic


def bp(orig, a):
    if a < 0:
        return 0
    if a > 0:
        return 1
    return orig

class BooleanEquation:
    def __init__(self, variable_name, rhs):
        self.variable_name = variable_name
        self.rhs = rhs

    def __str__(self):
        return self.variable_name + " = " + str(self.rhs)


class EulerlikeTransformer:
    def __init__(self, ode_system):
        self.ode_system = ode_system
        self.boolean_functions = []
        for ode in ode_system.odes:
            bf = self.infer_boolean_function(ode)
            self.boolean_functions.append(BooleanEquation(ode.variable_name, bf))

    def generate_truth_table(self, num_vars):
        truth_table = list(product([0, 1], repeat=num_vars))
        reversed_truth_table = [row[::-1] for row in truth_table]
        #self.truth_table = truth_table
        return truth_table

    def evaluate_equation(self, ode):
        truth_table = self.generate_truth_table(ode.num_vars)
        results = list()
        for row in truth_table:
            new_rhs = ode.rhs
            for i in range(ode.num_vars):
                new_rhs = new_rhs.replace(ode.input_variables[i], str(row[i]))
            for param in ode.parameters.keys():
                new_rhs = new_rhs.replace(param, str(ode.parameters[param]))
            lhs = eval(new_rhs)
            sgn_lhs = 0
            if lhs > 0:
                sgn_lhs = 1
            elif lhs < 0:
                sgn_lhs = -1
            results.append(sgn_lhs)
        whole_table = []
        for i in range(len(truth_table)):
            whole_table.append([x for x in truth_table[i]] + [results[i]])
        sgn_vector = results

        x_k_1 = []
        variable_index = ode.input_variables.index(ode.variable_name)
        for i in range(len(truth_table)):
            x_k_1.append(bp(truth_table[i][variable_index], sgn_vector[i]))
        update_values = x_k_1

        return truth_table, update_values

    def infer_boolean_function(self, ode):
        truth_table, update_values = self.evaluate_equation(ode)
        min_terms = []
        for j in range(len(truth_table)):
            row = truth_table[j]
            inputs = row[:ode.num_vars]
            output = update_values[j]
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
        boolean_function = re.sub(pattern, ode.replace_match, simplified_boolean_function)
        return boolean_function


    def __str__(self):
        result = ""
        for bf in self.boolean_functions:
            result += str(bf) + "\n"
        return result