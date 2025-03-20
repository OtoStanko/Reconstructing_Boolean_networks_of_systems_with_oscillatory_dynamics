import os.path
import re
import scipy.signal

from Eulerlike_transformation.EulerlikeTransformer import EulerlikeTransformer
from Eulerlike_transformation.ODESystem import ODESystem
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


def ode_eulerlike_transform_to_aeon(equations_ode_file_path, output_eaon_file_path):
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


def gyn_cycle_augusta_run():
    df = pd.read_csv('model_3_gyn-cycle/copasi_sim_columns.csv', delimiter='\t')
    df = df.T
    import Augusta
    df = df.iloc[1:]
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
    df = pd.read_csv('model_1_predator-prey/predator_prey_ODE_sim_columns.csv', delimiter='\t')
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


def gyn_cycle_visualization():
    df = pd.read_csv('model_3_gyn-cycle/copasi_sim_columns.csv', delimiter='\t')
    columns_to_drop = ['Ant_c', 'Ago_R-i', 'Ago_R-a','Ant_p','Ant_d',
                        'Ago_d', 's113', 's114', 's115', 's116',
                        'Ago_c', 'Ant_R', 'LH_Pit', 'FSH_pit']
    #df = df.drop(columns=columns_to_drop)
    print(df.columns)
    print(df)
    time_column = df.columns[0]
    LH_P4_Lut = ["LH_bld", "P4",'Lut1', 'Lut2', 'Lut3', 'Lut4']
    LH_P4_Lut_colors = ["orange", "blue", "green", "green", "green", "green"]
    E2_Inh_foll = ["E2", "InhA", "InhA_delay", "AF1", "AF2", "AF3", "AF4", "PrF", "OvF"]
    E2_Inh_foll_colors = ["red", "darkblue", "blue", "gray", "gray", "gray", "gray", "yellow", "orange"]
    FSH_foll = ["FSH_bld", "AF1", "AF2", "AF3", "AF4", "PrF", "OvF"]
    GnRH_LH_FSH = ["GnRH", "LH_bld", "FSH_bld"]
    GnRH_LH_FSH = ["GnRH"]
    plots = [LH_P4_Lut, E2_Inh_foll, FSH_foll, GnRH_LH_FSH]
    plots_colors = [LH_P4_Lut_colors, E2_Inh_foll_colors, [], []]

    lh_peaks, _ = scipy.signal.find_peaks(df["LH_bld"], distance=10, height=0.5)
    if len(lh_peaks) >= 3:
        starttime = lh_peaks[0]-1
        endtime = lh_peaks[2]+1
        #ct = time_column - time_column[lh_peaks[1]]
    else:
        starttime = 0
        endtime = len(time_column)
        #ct = time_column

    for plot, colors in zip(plots, plots_colors):
        for i in range(len(plot)):
            column = plot[i]
            plt.plot(df[time_column][starttime:endtime], df[column][starttime:endtime], label=column)
        plt.grid()
        plt.legend(loc='upper right')
        plt.xlabel('time')
        plt.ylabel('relative units')
        plt.show()
    #plt.title(f"Time Series Plot for {column}")
    #plt.legend()
gyn_cycle_visualization()


def hormonal_cycle_euler_transform_to_aeon():
    create_aeon_model("model_3_gyn-cycle/hormonal_cycle_equations.txt", "model_3_gyn-cycle/boolean_functions_aeon.aeon")
    with open("boolean_functions_aeon", "a") as bool_funcs_aeon:
        print("$mass: true", file=bool_funcs_aeon, end='\n')
        print("$freq: !freq", file=bool_funcs_aeon, end='\n')
        print("freq -? freq", file=bool_funcs_aeon, end='\n')


def simplify_parameters_file(in_file, out_file):
    remove_left_brackets = '_lcb_'
    remove_right_brackets = '_rcb_'
    remove_power = '_pwr_'
    my_hyphen = '_hyp_'
    with open(in_file, 'r') as file:
        content = file.read()
    updated_content = content.replace(remove_left_brackets, '')
    updated_content = updated_content.replace(remove_right_brackets, '')
    updated_content = updated_content.replace(remove_power, '')
    updated_content = updated_content.replace(my_hyphen, 'mhyphen')
    with open(out_file, 'w') as file:
        file.write(updated_content)
#gc_param_file = os.path.join(os.getcwd(), "old_files", "parameters_gc.txt")
#gc_param_simplified = os.path.join(os.getcwd(), "old_files", "parameters_gc_simplified.txt")
#simplify_parameters_file(gc_param_file, gc_param_simplified)


def SAILoR_to_aeon(list_of_boolean_functions, aeon_file_path):
    """
    $LH_pit: !P4
    P4 -? LH_pit
    """
    with open(aeon_file_path, 'w') as file:
        for boolean_function in list_of_boolean_functions:
            variable, rhs = boolean_function.split(" = ")
            equation = re.sub(r'and', '&', rhs)
            equation = re.sub(r'or', '|', equation)
            equation = re.sub(r'not ', '!', equation)
            print("$" + variable + ":", equation, file=file)
            pattern = r'\b!?\w+\b'
            variables = re.findall(pattern, equation)
            unique_variables = sorted(set(variables))
            if unique_variables[0] == '0' or unique_variables[0] == '1':
                continue
            for input_variable in unique_variables:
                print(input_variable + " -? " + variable, file=file)


def simplify_TS(raw_ts, binarized_ts, simplified_raw, simplified_bin):
    binarized_data = pd.read_csv(binarized_ts, sep=",", index_col=0)

    simplified_ts_states = list()
    indexes = []
    for i in range(len(binarized_data.columns)):
        column = binarized_data.columns[i]
        state = list(binarized_data[column])
        if len(simplified_ts_states) == 0:
            simplified_ts_states.append(state)
            indexes.append(i)
            continue
        if simplified_ts_states[-1] != state:
            simplified_ts_states.append(state)
            indexes.append(i)
    print(simplified_ts_states)
    print(indexes)
    names = list(binarized_data.index)
    df = pd.DataFrame(simplified_ts_states).T
    df.index = names
    df.to_csv(simplified_bin)


def visualize_lynx_hare():
    df = pd.read_csv("model_1_predator-prey/Leigh1968_harelynx_columns.csv")

    # Assume the first column is the 'Year' and the rest are values for different labels
    years = df.iloc[:, 0]  # First column (Years)
    values = df.iloc[:, 1:]  # All other columns (Values)

    # Plot each value series against years
    plt.figure(figsize=(10, 6))
    for column in values.columns:
        plt.plot(years, values[column], label=column)

    # Add labels and title
    plt.xlabel('Year')
    plt.ylabel('# of furs sold to Hudson Bay company')
    plt.title('Hudson Bay company Lynx-Hare dataset (1847 - 1903)')

    # Optional: Add a legend to indicate what each line represents
    plt.legend(loc='upper left')

    # Show the plot
    plt.grid(True)  # Optional: Add grid for better readability
    plt.show()
#visualize_lynx_hare()


def visualize_lynx_hare_discrete():
    df = pd.read_csv("model_1_predator-prey/Leigh1968_harelynx_columns.csv")
    # Assume the first column is the 'Year' and the rest are values for different labels
    years = df.iloc[:, 0]  # First column (Years)
    values = df.iloc[:, 1:]  # All other columns (Values)

    df_disc = pd.read_csv("model_1_predator-prey/Leigh1968_harelynx_rows_binarized.csv",
                          header=0, index_col=0)
    df_disc = df_disc.T

    features = ["Hares", "Lynxes"]
    for feature in features:
        plt.figure(figsize=(10, 6))
        ts = values[feature]
        ts = ts / max(ts)
        plt.plot(years, ts, label="raw {}".format(feature))
        plt.plot(years, df_disc[feature], label="discretized {}".format(feature))

        # Add labels and title
        plt.xlabel('Year')
        plt.ylabel('# of furs sold to Hudson Bay company')
        plt.title('Hudson Bay company {} dataset (1847 - 1903) raw vs discretized values'.format(feature))

        # Optional: Add a legend to indicate what each line represents
        plt.legend(loc='upper left')

        # Show the plot
        plt.grid(True)  # Optional: Add grid for better readability
        plt.show()
#visualize_lynx_hare_discrete()


def find_first_cycle(ts_csv_file_path):
    df = pd.read_csv(ts_csv_file_path)
    df = df.drop(columns=df.columns[0])
    path = []
    cycles = []
    for _, row in df.iterrows():
        row_list = list(row)
        if row_list in path:
            # found a cycle
            start = path.index(row_list)
            cycles.append(path[start:])
            #print(cycles)
            path = list()
        path.append(row_list)
    return cycles, list(df.columns)


def csv_ts_to_states(ts_csv_file_path):
    df = pd.read_csv(ts_csv_file_path)
    df = df.drop(columns=df.columns[0])
    ts = []
    for _, row in df.iterrows():
        row_list = list(row)
        ts.append(row_list)
    return ts, list(df.columns)


def create_formula_for_path(ts, head, include_basic_transitions=True, ax=False, on_non_triv_att=False):
    # !{x}: (AG EF {X} & AX ~{x} & (... EF (... EF (...))))
    formula_base = "!{x}: "
    if on_non_triv_att:
        formula_base += "(AG EF {x} & AX ~{x}) & "
    states = []
    formula_builder = formula_base
    num_closing_brackets = 0
    formula = ""
    basic_transitions = []
    for i in range(len(ts)):
        state = ts[i]
        formula_terms = []
        for column, value in zip(head, state):
            if value == 1:
                formula_terms.append(column)
            elif value == 0:
                formula_terms.append(f"~{column}")
        state = ' & '.join(formula_terms)
        #formula_builder = formula_builder + "{}{} (".format(" & " if num_closing_brackets > 1 else "",
        #                                                    "" if num_closing_brackets == 1 else ("AX" if (ax and i!=0) else "EF")) + state
        formula_builder = formula_builder + "{}(".format("" if num_closing_brackets==0 else
                                                         " & AX " if ax else " & EF ") + state
        num_closing_brackets += 1
        states.append(state)
        formula = formula_builder + num_closing_brackets * ")"
    if include_basic_transitions:
        for i in range(len(states)-1):
            basic_transitions.append(formula_base + "(" + states[i] + " & {} (".format("AX" if ax else "EF")
                                     + states[i+1] + "))")
    return formula, basic_transitions


#print(create_formula_for_path(os.path.join(os.getcwd(), "model_1_predator-prey", "predator_prey_ODE_sim_columns_binarized_simplified.csv")))
#find_first_cycle(os.path.join(os.getcwd(), "model_2_bovine-estrous", "bov_cycle_ODE_sim_columns_binarized_simplified_auto.csv"))
#ts, head = csv_ts_to_states(os.path.join(os.getcwd(), "model_1_predator-prey", "predator_prey_ODE_sim_columns_binarized_simplified.csv"))
#create_formula_for_path(ts, head)