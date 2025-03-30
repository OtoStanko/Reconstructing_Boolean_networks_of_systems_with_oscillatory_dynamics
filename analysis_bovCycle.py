import os

from biodivine_aeon import *

from analysis import BNAnalysis
from supporting_scripts import create_formula_for_path, find_first_cycle

be_model = os.path.join(os.getcwd(), "model_2_bovine-estrous")
boolnet_be_model_path_full_const = os.path.join(be_model, "BoolNet", "bovine-estrous_full_constraints_colored_edges.aeon")
boolnet_be_model_path_maxK4 = os.path.join(be_model, "BoolNet", "bovine-estrous_maxK4_colored_edges.aeon")
euler_like_automated_be_model_path = os.path.join(be_model, "euler-like_transformation", "bovine-estrous-cycle_model_colored_edges.aeon")
sailor_be_model_path = os.path.join(be_model, "SAILoR", "colored_bovine-estrous_model_binarised.aeon")
sketchBook_be_model_path = os.path.join(be_model, "SketchBook", "candidate_1.aeon")
sketchBook_be_model_path_2 = os.path.join(be_model, "SketchBook", "candidate_2.aeon")
be_model_paths = [boolnet_be_model_path_full_const, boolnet_be_model_path_maxK4,
                  euler_like_automated_be_model_path,
                  sailor_be_model_path, sketchBook_be_model_path,
                  sketchBook_be_model_path_2]


cycles, head = find_first_cycle(os.path.join(be_model, "bov_cycle_ODE_sim_columns_binarized_simplified_auto.csv"))
print([len(cycle) for cycle in cycles])
cycles_intersect = cycles[0]
for i in range(1, len(cycles)):
    cycles_intersect = [val for val in cycles_intersect if val in cycles[i]]
cycles_intersect.append(cycles_intersect[0])
print(len(cycles_intersect))
path_formula_ef, basic_transitions_ef = create_formula_for_path(cycles_intersect, head, on_non_triv_att=False)
ovulation_behaviour = "!{x}: (Foll & EF (E2 & Inh & Foll & EF (E2 & LH & ~P4 & Inh & ~CL & EF (~LH & ~P4 & CL & EF (~E2 & ~LH & P4 & ~Inh & ~Foll & CL & (EF {x}))))))"

msg_ok = ">OK"
msg_nok = ">FAIL"

models_results = {}
for model_path in be_model_paths:
    bna = BNAnalysis(model_path)
    bna.print_basic_info()
    results_classes = bna.attractor_analysis()
    results = bna.analyze_periodic_behaviour(basic_transitions_ef, path_formula_ef, ovulation_behaviour)
    model_info = model_path.split(os.sep)
    method = model_info[-2]
    model = model_info[-1]
    models_results[(method, model)] = [results_classes, results]

for model_results in models_results.items():
    print(model_results)