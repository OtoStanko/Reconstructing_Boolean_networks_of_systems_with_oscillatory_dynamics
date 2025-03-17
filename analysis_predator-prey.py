import os

from biodivine_aeon import *

from supporting_scripts import create_formula_for_path, find_first_cycle

pp_model = os.path.join(os.getcwd(), "model_1_predator-prey")
boolnet_pp_model_hudsonBay_path = os.path.join(pp_model, "BoolNet", "predator-prey_hudsonBayDataset.sbml")
boolnet_pp_model_simData_path = os.path.join(pp_model, "BoolNet", "predator-prey_simDataset.sbml")
euler_like_pp_model_path_a_ge_b_d_ge_g = os.path.join(pp_model, "euler-like_transformation", "a_ge_b_d_ge_g.aeon")
euler_like_pp_model_path_a_ge_b_d_l_g = os.path.join(pp_model, "euler-like_transformation", "a_ge_b_d_l_g.aeon")
euler_like_pp_model_path_a_l_b_d_ge_g = os.path.join(pp_model, "euler-like_transformation", "a_l_b_d_ge_g.aeon")
euler_like_pp_model_path_a_l_b_d_l_g = os.path.join(pp_model, "euler-like_transformation", "a_l_b_d_l_g.aeon")
sailor_pp_model_path_hudson_raw = os.path.join(pp_model, "SAILoR", "coloured_predator-prey_hudsonBayDataset.aeon")
sailor_pp_model_path_hudson_bin = os.path.join(pp_model, "SAILoR", "coloured_predator-prey_hudsonBayDataset_binarised.aeon")
sailor_pp_model_path_sim_raw = os.path.join(pp_model, "SAILoR", "coloured_predator-prey_simDataset.aeon")
sailor_pp_model_path_sim_bin = os.path.join(pp_model, "SAILoR", "coloured_predator-prey_simDataset_binarised.aeon")
sketchBook_pp_model_path = os.path.join(pp_model, "SketchBook", "candidate_1.aeon")
ideal_pp_model_path = os.path.join(pp_model, "predator-prey_boolean_model_ideal.aeon")
pp_model_paths = [boolnet_pp_model_hudsonBay_path, boolnet_pp_model_simData_path,
                  euler_like_pp_model_path_a_ge_b_d_ge_g, euler_like_pp_model_path_a_ge_b_d_l_g,
                  euler_like_pp_model_path_a_l_b_d_ge_g, euler_like_pp_model_path_a_l_b_d_l_g,
                  sailor_pp_model_path_hudson_raw, sailor_pp_model_path_hudson_bin,
                  sailor_pp_model_path_sim_raw, sailor_pp_model_path_sim_bin,
                  sketchBook_pp_model_path, ideal_pp_model_path]


cycles, head = find_first_cycle(os.path.join(pp_model, "predator_prey_ODE_sim_columns_binarized_simplified.csv"))
cycles_intersect = cycles[0]
for i in range(1, len(cycles)):
    cycles_intersect = [val for val in cycles_intersect if val in cycles[i]]
cycles_intersect.append(cycles_intersect[0])
print(cycles_intersect)
path_formula_ax, basic_transitions_ax = create_formula_for_path(cycles_intersect, head, ax=True)
print(path_formula_ax)
print(basic_transitions_ax)
path_formula_ef, basic_transitions_ef = create_formula_for_path(cycles_intersect, head)
print(path_formula_ef)
print(basic_transitions_ef)

msg_ok = ">OK"
msg_nok = ">FAIL"


models_results = dict()
for model_path in pp_model_paths:
    print()
    print(len(model_path)*"*")
    print(model_path)
    print(len(model_path)*"*")
    model = BooleanNetwork.from_file(model_path, repair_graph=True)

    print("\nModel update functions")
    for v in model.variables():
        print(model.get_variable_name(v), "=", model.get_update_function(v))
    print("\nModel regulations")
    for regulation in model.regulations():
        print(regulation)

    stg = AsynchronousGraph.mk_for_model_checking(model, 2)
    attractors = Attractors.attractors(stg)
    print("\nModel attractors ({})".format(len(attractors)))
    print(attractors)
    results_classes = []
    for attractor in attractors:
        print(">")
        print("Attractor cardinality:", attractor.cardinality())
        print("Attractor vertices:", attractor.vertices())
        classes = Classification.classify_long_term_behavior(stg, attractor)
        results_classes.append(classes)
        print("class:", classes)

    print("\nPeriodic behaviour analysis:".upper())

    results_ax_ok = 0
    results_ax_nok = 0
    result_ax_whole = False
    print("\nResult of AX for a cycle representing predator-prey relationship:")
    for partial_transition in basic_transitions_ax:
        print()
        print(partial_transition)
        attractor_mc = ModelChecking.verify(stg, partial_transition)
        print(attractor_mc)
        if attractor_mc.cardinality() > 0:
            results_ax_ok += 1
            print(msg_ok)
        else:
            results_ax_nok += 1
            print(msg_nok)
    print(path_formula_ax)
    attractors_mc = ModelChecking.verify(stg, path_formula_ax)
    print(attractors_mc)
    if attractors_mc.cardinality() > 0:
        result_ax_whole = True
        print(msg_ok)
    else:
        print(msg_nok)

    results_ef_ok = 0
    results_ef_nok = 0
    result_ef_whole = False
    print("\nResult of EF for a cycle representing predator-prey relationship:")
    for partial_transition in basic_transitions_ef:
        print()
        print(partial_transition)
        attractor_mc = ModelChecking.verify(stg, partial_transition)
        print(attractor_mc)
        if attractor_mc.cardinality() > 0:
            results_ef_ok += 1
            print(msg_ok)
        else:
            results_ef_nok += 1
            print(msg_nok)
    print(path_formula_ef)
    attractors_mc = ModelChecking.verify(stg, path_formula_ef)
    print(attractors_mc)
    if attractors_mc.cardinality() > 0:
        result_ef_whole = True
        print(msg_ok)
    else:
        print(msg_nok)

    model_info = model_path.split(os.sep)
    method = model_info[-2]
    model = model_info[-1]
    models_results[(method, model)] = [results_classes, str(results_ax_ok)+"/"+str(results_ax_ok+results_ax_nok), result_ax_whole,
                                       str(results_ef_ok)+"/"+str(results_ef_ok+results_ef_nok), result_ef_whole]

for model_results in models_results.items():
    print(model_results)
