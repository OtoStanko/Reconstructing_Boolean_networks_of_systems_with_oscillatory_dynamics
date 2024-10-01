import re
from parameters import *
from variable_handler import Variable_handler
from equations import edes
import pandas as pd
import matplotlib.pyplot as plt


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


def parameter_names():
    with open("parameter_names.txt", "r") as f:
        with open("parameter_names_python.txt", "w") as of:
            for line in f:
                if line != "":
                    new_name = variable_latex_to_python(line)
                    print(new_name, file=of)


def augusta_run():
    df = pd.read_csv('copasi_simulation_100d.csv', delimiter='\t')
    df = df.T
    print(df.index)
    import Augusta
    df = df.iloc[1:-1]
    rows_to_drop = ['Ant_c', 'Ago_R-i', 'Ago_R-a','Ant_p','Ant_d',
                    'Ago_d', 's113', 's114', 's115', 's116',
                    'Ago_c', 'Ant_R', ]
    for row_to_drop in rows_to_drop:
        df = df.drop(index=row_to_drop)
    df = df * 1000
    df.to_csv('output.csv', sep=';')
    Augusta.RNASeq_to_BN(count_table_input = 'output.csv')

def augusta_visualization():
    df = pd.read_csv('copasi_simulation_100d.csv', delimiter='\t')
    columns_to_drop = ['Ant_c', 'Ago_R-i', 'Ago_R-a','Ant_p','Ant_d',
                        'Ago_d', 's113', 's114', 's115', 's116',
                        'Ago_c', 'Ant_R', 'LH_Pit', 'FSH_pit']
    df = df.drop(columns=columns_to_drop)
    print(df)
    time_column = df.columns[0]

    for column in df.columns[1:]:
        #plt.figure(figsize=(10, 6))  # Create a new figure for each column
        plt.plot(df[time_column], df[column], label=column)
    #plt.title(f"Time Series Plot for {column}")
    plt.xlabel("Time")
    plt.ylabel('Hormone levels')
    plt.legend()
    plt.grid(True)
    plt.show()


#create_aeon_model()
#augusta_run()