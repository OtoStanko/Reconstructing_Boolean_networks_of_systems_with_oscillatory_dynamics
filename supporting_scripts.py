import os
import re

from EulerlikeTransformer import EulerlikeTransformer
from ODESystem import ODESystem
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


def create_aeon_model(equations_ode_file_path, output_eaon_file_path):
    """
    Takes in file with each ODE on a separate line in a latex format names and discetized meaning that each continuous
    function is replaced by the variable itself, or 1-var.

    For now also expects \\ and a space before = (equals sign)
    :return: None
    """
    if equations_ode_file_path is None or output_eaon_file_path is None:
        print("File names not provided")
        return
    ode_system = ODESystem(equations_ode_file_path)
    bn = EulerlikeTransformer(ode_system)
    bn.save_bn_to_aeon(output_eaon_file_path)


def parameter_names():
    with open("parameter_names.txt", "r") as f:
        with open("parameter_names_python.txt", "w") as of:
            for line in f:
                if line != "":
                    new_name = variable_latex_to_python(line)
                    print(new_name, file=of)


def hormonal_cycle_augusta_run():
    df = pd.read_csv('copasi_simulation_100d.csv', delimiter='\t')
    df = df.T
    import Augusta
    df = df.iloc[1:-1]
    rows_to_drop = ['Ant_c', 'Ago_R-i', 'Ago_R-a','Ant_p','Ant_d',
                    'Ago_d', 's113', 's114', 's115', 's116',
                    'Ago_c', 'Ant_R', ]
    for row_to_drop in rows_to_drop:
        df = df.drop(index=row_to_drop)
    df = df * 1000
    print(df.index)
    print(df)
    df.to_csv('output.csv', sep=';')
    Augusta.RNASeq_to_BN(count_table_input = 'output.csv')
#hormonal_cycle_augusta_run()


def predator_prey_augusta_run():
    df = pd.read_csv('predator_prey_ODE_sim_results.csv', delimiter='\t')
    time_column = df.columns[0]
    df = df[df['Time'] >= 4]
    for column in df.columns[1:]:
        #plt.figure(figsize=(10, 6))  # Create a new figure for each column
        plt.plot(df[time_column], df[column], label=column)
    plt.legend()
    plt.grid(True)
    plt.show()
    df = df.T
    df = df.iloc[1:]
    import Augusta
    #df = (df * 100).astype(int)
    print(df.index)
    print(df)
    df.to_csv('predator_prey_ODE_sim_results_T.csv', sep=';')
    Augusta.RNASeq_to_BN(count_table_input = 'predator_prey_ODE_sim_results_T.csv')
#predator_prey_augusta_run()


def hormonal_cycle_augusta_visualization():
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


def hormonal_cycle_euler_transform_to_aeon():
    create_aeon_model("hormonal_cycle_equations.txt", "boolean_functions_aeon.aeon")
    with open("boolean_functions_aeon", "a") as bool_funcs_aeon:
        print("$mass: true", file=bool_funcs_aeon, end='\n')
        print("$freq: !freq", file=bool_funcs_aeon, end='\n')
        print("freq -? freq", file=bool_funcs_aeon, end='\n')


def predator_prey_euler_transform_to_aeon(ode_file, aeon_file):
    create_aeon_model(ode_file, aeon_file)


def bovine_estrous_euler_transform_to_aeon(ode_file, aeon_file):
    create_aeon_model(ode_file, aeon_file)