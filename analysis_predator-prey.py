from biodivine_aeon import *
import os


pp_model = os.path.join(os.getcwd(), "model_1_predator-prey")
boolnet_pp_model_path = os.path.join(pp_model, "BoolNet", "predator-prey.sbml")
euler_like_pp_model_path = os.path.join(pp_model, "euler-like_transformation", "predator-prey_model.aeon")
sailor_pp_model_path = os.path.join(pp_model, "SAILoR", "predator-prey.aeon")
sketchBook_pp_model_path = os.path.join(pp_model, "SketchBook", "candidate_1.aeon")
ideal_pp_model_path = os.path.join(pp_model, "predator-prey_boolean_model_ideal.aeon")
pp_model_paths = [boolnet_pp_model_path,
                  euler_like_pp_model_path, sailor_pp_model_path,
                  sketchBook_pp_model_path, ideal_pp_model_path]


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
    for attractor in attractors:
        print(">")
        print("Attractor cardinality:", attractor.cardinality())
        print("Attractor vertices:", attractor.vertices())
        classes = Classification.classify_long_term_behavior(stg, attractor)
        print("class:", classes)

    print("\nPeriodic behaviour analysis:")
    print("Result of AX for a cycle representing predator-prey relationship:")
    cyclic_property_ax = "3 {x}: (EF (~Hares & ~Lynxes & AX (Hares & ~Lynxes & AX (Hares & Lynxes & AX (~Hares & Lynxes & AX (~Hares & ~Lynxes))))))"
    print(cyclic_property_ax)
    attractors_mc = ModelChecking.verify(stg, cyclic_property_ax)
    print(attractors_mc)

    print("Result of EF for a cycle representing predator-prey relationship:")
    cyclic_property_ef = "3 {x}: (EF (~Hares & ~Lynxes & EF (Hares & ~Lynxes & EF (Hares & Lynxes & EF (~Hares & Lynxes & EF (~Hares & ~Lynxes))))))"
    print(cyclic_property_ef)
    attractors_mc = ModelChecking.verify(stg, cyclic_property_ef)
    print(attractors_mc)
