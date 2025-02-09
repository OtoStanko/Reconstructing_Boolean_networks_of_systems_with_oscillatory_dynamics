from biodivine_aeon import *
import os


be_model = os.path.join(os.getcwd(), "model_2_bovine-estrous")
boolnet_be_model_path = os.path.join(be_model, "BoolNet", "bovine-estrous_maxK4_colored_edges.aeon")
euler_like_be_model_path = os.path.join(be_model, "euler-like_transformation", "first_model.aeon")
euler_like_automated_be_model_path = os.path.join(be_model, "euler-like_transformation", "bovine-estrous-cycle_model.aeon")
sailor_be_model_path = os.path.join(be_model, "SAILoR", "bovine-estrous_model.aeon")
sketchBook_be_model_path = os.path.join(be_model, "SketchBook", "sat_networks_1", "candidate_1.aeon")
be_model_paths = [boolnet_be_model_path, euler_like_automated_be_model_path,
                  sailor_be_model_path, sketchBook_be_model_path]


for model_path in be_model_paths:
    print()
    print(len(model_path) * "*")
    print(model_path)
    print(len(model_path) * "*")
    model = BooleanNetwork.from_file(model_path, repair_graph=True)

    print("\nModel update functions")
    for v in model.variables():
        print(model.get_variable_name(v), "=", model.get_update_function(v))
    print("\nModel regulations")
    for regulation in model.regulations():
        print(regulation)

    stg = AsynchronousGraph.mk_for_model_checking(model, 6)
    attractors = Attractors.attractors(stg)
    print("\nModel attractors ({})".format(len(attractors)))
    print(attractors)
    for attractor in attractors:
        print(">")
        print("Attractor cardinality:", attractor.cardinality())
        print("Attractor vertices:", attractor.vertices())
        classes = Classification.classify_long_term_behavior(stg, attractor)
        print("class:", classes)

    print("\nPeriodic behaviour analysis:")
    print("Existence of a cycle that includes key ovulation hormonal pattern:")
    ovulation_behaviour = "3 {x}: (Foll & EF (E2 & Inh & Foll & EF (E2 & LH & ~P4 & Inh & ~CL & EF (~LH & ~P4 & CL & EF (~E2 & ~LH & P4 & ~Inh & ~Foll & CL & (EF {x}))))))"
    print(ovulation_behaviour)
    attractors_mc = ModelChecking.verify(stg, ovulation_behaviour)
    print(attractors_mc)
    print()