import os

from biodivine_aeon import *

from analysis import BNAnalysis
from supporting_scripts import create_formula_for_path, find_first_cycle

gc_model = os.path.join(os.getcwd(), "model_3_gyn-cycle")
boolnet_gc_model_path = os.path.join(gc_model, "BoolNet", "gyn-cycle.sbml")
boolnet_gc_model_path_full_consts = os.path.join(gc_model, "BoolNet", "gyn-cycle_full_constraints.sbml")
boolnet_gc_model_path_maxK4 = os.path.join(gc_model, "BoolNet", "gyn-cycle_maxK4.sbml")
boolnet_gc_model_path_maxK8 = os.path.join(gc_model, "BoolNet", "gyn-cycle_maxK8.sbml")
euler_like_gc_model_path = os.path.join(gc_model, "euler-like_transformation", "gyn-cycle_model_fixedNames.aeon")
sailor_gc_model_path = os.path.join(gc_model, "SAILoR", "gyn-cycle_model.aeon")
gc_model_paths = [boolnet_gc_model_path_full_consts,
                  boolnet_gc_model_path_maxK8,
                  euler_like_gc_model_path, sailor_gc_model_path]


cycles, head = find_first_cycle(os.path.join(gc_model, "gyn_cycle_sim_columns_binarized_simplified_auto.csv"))
cycles_intersect = cycles[0]
for i in range(1, len(cycles)):
    cycles_intersect = [val for val in cycles_intersect if val in cycles[i]]
cycles_intersect.append(cycles_intersect[0])
print(cycles_intersect)
path_formula_ef, basic_transitions_ef = create_formula_for_path(cycles_intersect, head, on_non_triv_att=False)
ovulation_behaviour = "!{x}: ((AF1 | AF2 | AF3 | AF4) & ~InhA & ~E2 & EF ((AF1 | AF2 | AF3 | AF4) & InhA & E2 & EF (PrF & EF (OvF & LH_bld & ~(Lut1 | Lut2 | Lut3 | Lut4) & ~P4 & EF (~LH_bld & (Lut1 | Lut2 | Lut3 | Lut4) & ~P4 & EF (~E2 & ~LH_bld & P4 & ~InhA & ~(AF1 | AF2 | AF3 | AF4) & (Lut1 | Lut2 | Lut3 | Lut4)))))))"

msg_ok = ">OK"
msg_nok = ">FAIL"


models_results = {}
for model_path in gc_model_paths:
    bna = BNAnalysis(model_path)
    bna.print_basic_info()
    results_classes = bna.attractor_analysis()
    results = bna.analyze_periodic_behaviour(basic_transitions_ef, path_formula_ef, ovulation_behaviour, False)
    model_info = model_path.split(os.sep)
    method = model_info[-2]
    model = model_info[-1]
    models_results[(method, model)] = [results_classes, results]

for model_results in models_results.items():
    print(model_results)