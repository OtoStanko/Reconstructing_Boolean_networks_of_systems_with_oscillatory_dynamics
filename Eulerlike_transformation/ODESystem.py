import re


class ODE:
    def __init__(self, variable_name, rhs):
        self.variable_name = variable_name
        self.rhs = rhs
        self.input_variables = []
        self.num_vars = 0
        self.parameters = {}

    def replace_match(self, match):
        index = int(match.group(1))  # Extract the number 'i' from 'x<i>'
        if index < len(self.input_variables):
            return self.input_variables[index]

    def return_regulatory_network(self):
        rhs = self.rhs
        str_len = len(rhs)
        brackets_count = 0
        i = 0
        terms_pos = []
        terms_neg = []
        term_start = i
        while i < str_len:
            if rhs[i] == '(':
                brackets_count += 1
            elif rhs[i] == ')':
                brackets_count -= 1
            if (rhs[i] == "+" or rhs[i] == "-") and brackets_count == 0:
                # found end of term
                term = rhs[term_start:i]
                if term[0] != "-":
                    terms_pos.append(term)
                else:
                    terms_neg.append(term)
                term_start = i
            i += 1
        term = rhs[term_start:i]
        if term[0] != "-":
            terms_pos.append(term)
        else:
            terms_neg.append(term)
        green = set()
        red = set()
        for var in self.input_variables:
            #print(var)
            pattern = r'(^|[-+*/()=]+)' + re.escape(var) + r'($|[-+*/()=]|\s)'
            for term in terms_pos:
                r = re.findall(pattern, term)
                if len(r) > 0:
                    for match in r:
                        if "-" in match[0]:
                            red.add(var)
                        else:
                            green.add(var)
                #print(r)
            for term in terms_neg:
                r = re.findall(pattern, term)
                if len(r) > 0:
                    for match in r:
                        if "-" in match[0]:
                            green.add(var)
                        else:
                            red.add(var)
                #print(r)
        regulatory_network = ""
        dual_regulations = green.intersection(red)
        for var in dual_regulations:
            regulatory_network += var + " -? " + self.variable_name + "\n"
        for var in green.difference(dual_regulations):
            regulatory_network += var + " -> " + self.variable_name + "\n"
        for var in red.difference(dual_regulations):
            regulatory_network += var + " -| " + self.variable_name + "\n"
        #print("positive:", green)
        #print("negative:", red)
        return regulatory_network

    def __str__(self):
        equation = "d" + self.variable_name + "/dt = " + self.rhs + "\n"
        input_info = "input variables: " + str(self.input_variables) + "\n"
        input_length = "num_input_variables: " + str(self.num_vars) + "\n"
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
        self.odes = []
        self.parameters = {}
        self.all_variables = set()
        with open (ode_file_path, "r") as ode_file:
            pattern_ode = r'd([^/]+)/.*=(.*)'
            pattern_params = r'par\s(.*)'
            for line in ode_file:
                match = re.search(pattern_ode, line)
                if match:
                    variable = match.group(1)  # Substring between 'd' and '/'
                    rhs = match.group(2)  # Everything after '='
                    ode = ODE(variable, rhs)
                    self.odes.append(ode)
                    self.all_variables.add(variable)
                match =re.search(pattern_params, line)
                if match:
                    parameters_grouped = match.group(1)
                    parameters_split = parameters_grouped.split(",")
                    for parameter in parameters_split:
                        name, value = parameter.split("=")
                        self.parameters[name] = float(value)
        # At this point we have lhs rhs and parameters
        # Now we want for each ode a number of variables that it is dependent on
        sorted_parameters = dict(sorted(self.parameters.items(), key=lambda x: -len(x[0])))
        print(sorted_parameters)
        # We have variables from lhs
        # Variable lies between +-*/()= and start of the line
        for ode in self.odes:
            for variable in self.all_variables:
                pattern = r'(^|[-+*/()=])' + re.escape(variable) + r'($|[-+*/()=]|\s)'
                if re.search(pattern, ode.rhs):
                    ode.input_variables.append(variable)
            ode.input_variables = sorted(ode.input_variables, key=len, reverse=True)
            ode.num_vars = len(ode.input_variables)
            for parameter_name in sorted_parameters.keys():
                if parameter_name in ode.rhs:
                    ode.parameters[parameter_name] = sorted_parameters[parameter_name]
            print()
            print(ode)
        print(self.odes)
        print(self.all_variables)

    def to_network(self, network_file):
        with open(network_file, "w") as network_file:
            for ode in self.odes:
                for variable in ode.input_variables:
                    network_file.write(str(variable) + "\t" + str(ode.variable_name) + "\t" + "1" + "\n")

    def to_network_aeon_format(self, network_file):
        with open(network_file, "w") as network_file:
            for ode in self.odes:
                ode_interactions = ode.return_regulatory_network()
                network_file.write(ode_interactions)

    def get_requiredDependencies(self):
        max_input_vars = 0
        result = "list("
        for ode in self.odes:
            max_input_vars = max(max_input_vars, len(ode.input_variables))
            ode_dependency = "\"" + ode.variable_name + "\"=c("
            for variable in ode.input_variables:
                ode_dependency += "\"" + str(variable) + "\","
            ode_dependency = ode_dependency[:-1] + "),"
            result += ode_dependency
        result = result[:-1] + ")"
        return max_input_vars, result

#ode_file_pp = ODESystem(os.path.join(os.getcwd(), "model_1_predator-prey", "predator-prey_ODE_model.dode"))
#bn = EulerlikeTransformer(ode_file_pp)
#print(bn)

#bn.save_bn_to_aeon("predator_prey_euler-like.aeon")
#ode_file_be = os.path.join(os.getcwd(), "model_2_bovine-estrous", "bovine-estrous-cycle_ODE_model.dode")
#ode_system = ODESystem(ode_file_be)

