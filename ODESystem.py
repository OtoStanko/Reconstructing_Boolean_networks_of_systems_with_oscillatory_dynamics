import os
import re

class ODE:
    def __init__(self, variable_name, rhs):
        self.variable_name = variable_name
        self.rhs = rhs
        self.input_variables = []
        self.num_input_variables = 0
        self.parameters = []

    def __str__(self):
        equation = "d"+self.variable_name + "/dt = " + self.rhs + "\n"
        input_info = "input variables: " + str(self.input_variables) + "\n"
        input_length = "num_input_variables: " + str(self.num_input_variables) + "\n"
        parameters = "parameters: " + str(self.parameters) + "\n"
        return equation + input_info + input_length + parameters


class ODESystem:
    def __init__(self, ode_file_path):
        """
        Takes in .ode file with ode model and parses it into list of differential equations, list of variables
        and dictionary of param:value pairs, where parameters are sorted by length in decreasing order
        and then alphabetically.
        :param ode_file_path: path to .ode file containing ODE model
        """
        odes = []
        parameters = {}
        all_variables = set()
        with open (ode_file_path, "r") as ode_file:
            pattern_ode = r'd([^/]+)/.*=(.*)'
            pattern_params = r'par\s(.*)'
            for line in ode_file:
                match = re.search(pattern_ode, line)
                if match:
                    variable = match.group(1)  # Substring between 'd' and '/'
                    rhs = match.group(2)  # Everything after '='
                    ode = ODE(variable, rhs)
                    odes.append(ode)
                    all_variables.add(variable)
                match =re.search(pattern_params, line)
                if match:
                    parameters_grouped = match.group(1)
                    parameters_split = parameters_grouped.split(",")
                    for parameter in parameters_split:
                        name, value = parameter.split("=")
                        parameters[name] = float(value)
        # At this point we have lhs rhs and parameters
        # Now we want for each ode a number of variables that it is dependent on
        sorted_parameters = dict(sorted(parameters.items(), key=lambda x: -len(x[0])))
        print(sorted_parameters)
        for ode in odes:
            for variable in all_variables:
                if variable in ode.rhs:
                    ode.input_variables.append(variable)
            ode.num_input_variables = len(ode.input_variables)
            for parameter_name in sorted_parameters.keys():
                if parameter_name in ode.rhs:
                    ode.parameters.append(parameter_name)
            print(ode)
        print(odes)
        print(all_variables)

ODESystem(os.path.join(os.getcwd(), "predator-prey_model", "predator-prey_ODE_model.ode"))

