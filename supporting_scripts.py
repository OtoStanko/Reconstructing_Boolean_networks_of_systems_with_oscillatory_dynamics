import re
from parameters import *
from variable_handler import Variable_handler
from equations import edes


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


def infer_boolean_function():
    with open("boolean_functions_latex.txt", "w") as bool_funcs_latex:
        for eq in edes:
            vh = Variable_handler(eq)
            vh.infer_boolean_function_latex()
            print(vh.boolean_function_latex, file=bool_funcs_latex, end='\n\n')
            print(vh.name)


def create_aeon_model():
    with open("boolean_functions_aeon.aeon", "w") as bool_funcs_aeon:
        for eq in edes:
            vh = Variable_handler(eq)
            lines = vh.boolean_function_to_aeon()
            print(vh.name + " = " + vh.boolean_function)
            for line in lines:
                print(line, file=bool_funcs_aeon, end='\n')
            print(vh.name)
        print("$mass: true", file=bool_funcs_aeon, end='\n')
        print("$freq: !freq", file=bool_funcs_aeon, end='\n')
        print("freq -? freq", file=bool_funcs_aeon, end='\n')
create_aeon_model()


def parameter_names():
    with open("parameter_names.txt", "r") as f:
        with open("parameter_names_python.txt", "w") as of:
            for line in f:
                if line != "":
                    new_name = variable_latex_to_python(line)
                    print(new_name, file=of)
