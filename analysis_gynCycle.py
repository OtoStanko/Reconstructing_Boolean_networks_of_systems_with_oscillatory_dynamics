import os

from biodivine_aeon import *

from supporting_scripts import create_formula_for_path, find_first_cycle

gc_model = os.path.join(os.getcwd(), "model_3_gyn-cycle")
boolnet_gc_model_path = os.path.join(gc_model, "BoolNet", "gyn-cycle.sbml")
euler_like_gc_model_path = os.path.join(gc_model, "euler-like_transformation", "gyn-cycle_model_fixedNames.aeon")
sailor_gc_model_path = os.path.join(gc_model, "SAILoR", "gyn-cycle_model.aeon")
gc_model_paths = [boolnet_gc_model_path,
                  euler_like_gc_model_path, sailor_gc_model_path]


cycles, head = find_first_cycle(os.path.join(gc_model, "gyn_cycle_sim_columns_binarized_simplified_auto.csv"))
cycles_intersect = cycles[0]
for i in range(1, len(cycles)):
    cycles_intersect = [val for val in cycles_intersect if val in cycles[i]]
cycles_intersect.append(cycles_intersect[0])
print(cycles_intersect)
path_formula_ef, basic_transitions_ef = create_formula_for_path(cycles_intersect, head, on_non_triv_att=False)
#print(path_formula_ef)
#print(basic_transitions_ef)

msg_ok = ">OK"
msg_nok = ">FAIL"


models_results = dict()
for model_path in gc_model_paths:
    print()
    print(len(model_path) * "*")
    print(model_path)
    print(len(model_path) * "*")
    model = BooleanNetwork.from_file(model_path, repair_graph=True)

    print("Model implicit params:", model.implicit_parameters())

    print("\nModel update functions")
    for v in model.variables():
        print(model.get_variable_name(v), "=", model.get_update_function(v))
    print("\nModel regulations")
    for regulation in model.regulations():
        print(regulation)

    stg = AsynchronousGraph.mk_for_model_checking(model, 35)
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
    print()

    print("\nPeriodic behaviour analysis:")
    results_ef_ok = 0
    results_ef_nok = 0
    result_ef_whole = False
    print("\nResult of EF path for gyn cycle:")
    for attractor in attractors:
        stg_att = stg.restrict(attractor)
        classes = Classification.classify_long_term_behavior(stg, attractor)
        print("\n***********")
        print("class:", classes)
        #print(list(classes.keys()))
        if Class(["disorder"]) not in list(classes.keys()):
            continue
        print(attractor.vertices())
        print_buffer = "\n"
        print_at_the_end = False
        for partial_transition in basic_transitions_ef:
            #print()
            #print(partial_transition)
            print_buffer += partial_transition + "\n"
            attractor_mc = ModelChecking.verify(stg_att, partial_transition)
            #print(attractor_mc)
            print_buffer += str(attractor_mc) + "\n"
            if attractor_mc.cardinality() > 0:
                results_ef_ok += 1
                print_at_the_end = True
                #print(msg_ok)
                print_buffer += msg_ok + "\n"
            else:
                results_ef_nok += 1
                #print(msg_nok)
                print_buffer += msg_nok + "\n"
        #print(path_formula_ef)
        print_buffer += path_formula_ef + "\n"
        attractors_mc = ModelChecking.verify(stg_att, path_formula_ef)
        #print(attractors_mc)
        print_buffer += str(attractors_mc) + "\n"
        if attractors_mc.cardinality() > 0:
            result_ef_whole = True
            print_at_the_end = True
            #print(msg_ok)
            print_buffer += msg_ok + "\n"
        else:
            #print(msg_nok)
            print_buffer += msg_nok + "\n"
        if print_at_the_end:
            print(print_buffer)

    model_info = model_path.split(os.sep)
    method = model_info[-2]
    model = model_info[-1]
    models_results[(method, model)] = [results_classes,
                                       str(results_ef_ok) + "/" + str(results_ef_ok + results_ef_nok),
                                       result_ef_whole]

for model_results in models_results.items():
    print(model_results)