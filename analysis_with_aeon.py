import biodivine_aeon
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

be_model = os.path.join(os.getcwd(), "model_2_bovine-estrous")
boolnet_be_model_path = os.path.join(be_model, "BoolNet", "bovine-estrous_maxK4_colored_edges.aeon")
euler_like_be_model_path = os.path.join(be_model, "euler-like_transformation", "first_model.aeon")
euler_like_automated_be_model_path = os.path.join(be_model, "euler-like_transformation", "bovine-estrous-cycle_model.aeon")
sailor_be_model_path = os.path.join(be_model, "SAILoR", "bovine-estrous_model.aeon")
sketchBook_be_model_path = os.path.join(be_model, "SketchBook", "sat_networks_1", "candidate_1.aeon")
be_model_paths = [boolnet_be_model_path, euler_like_automated_be_model_path,
                  sailor_be_model_path, sketchBook_be_model_path]


gc_model = os.path.join(os.getcwd(), "model_3_gyn-cycle")
boolnet_gc_model_path = os.path.join(gc_model, "BoolNet", "gyn-cycle.sbml")
euler_like_gc_model_path = os.path.join(gc_model, "euler-like_transformation", "gyn-cycle_model.aeon")
sailor_gc_model_path = os.path.join(gc_model, "SAILoR", "gyn-cycle_model.aeon")
gc_model_paths = [boolnet_gc_model_path,
                  euler_like_gc_model_path, sailor_gc_model_path]

for model_path in pp_model_paths:
    print()
    print("**********")
    print(model_path)
    print("**********")
    model = BooleanNetwork.from_file(model_path, repair_graph=True)
    biodivine_aeon.RegulatoryGraph
    print(model.implicit_parameters())
    print(model.variables())
    for v in model.variables():
        print(model.get_variable_name(v), "=", model.get_update_function(v))

    stg = AsynchronousGraph.mk_for_model_checking(model, 2)

    attractors = Attractors.attractors(stg)
    print(attractors)
    for attractor in attractors:
        classes = Classification.classify_long_term_behavior(stg, attractor)
        print(classes)
    print()
    cyclic_property_ax = "3 {x}: (EF (~Hares & ~Lynxes & AX (Hares & ~Lynxes & (AX (Hares & Lynxes & (AX (~Hares & Lynxes & (AX (~Hares & ~Lynxes)))))))))"
    attractors_mc = ModelChecking.verify(stg, cyclic_property_ax)
    print(attractors_mc)
    cyclic_property_ef = "3 {x}: (EF (~Hares & ~Lynxes & EF (Hares & ~Lynxes & EF (Hares & Lynxes & EF (~Hares & Lynxes & EF (~Hares & ~Lynxes))))))"
    attractors_mc = ModelChecking.verify(stg, cyclic_property_ef)
    print(attractors_mc)


for model_path in be_model_paths:
    print()
    print("**********")
    print(model_path)
    print("**********")
    model = BooleanNetwork.from_file(model_path)
    for v in model.variables():
        print(model.get_variable_name(v), "=", model.get_update_function(v))

    stg = AsynchronousGraph.mk_for_model_checking(model, 3)

    attractors = Attractors.attractors(stg)
    print(attractors)
    for attractor in attractors:
        classes = Classification.classify_long_term_behavior(stg, attractor)
        print(classes)
    # "(LH & EU(!P4, (E2 & EU(!LH, (P4 & EU(!E2, LH))))))"
    formula = "(LH & ((~P4) EU (E2 & ((~LH) EU (P4 & ((~E2) EU LH))))))"
    #ovulation_behaviour = "3 {x}: (EF((~Hares & ~Lynxes) & AX (Hares & ~Lynxes & (AX (Hares & Lynxes & (AX (~Hares & Lynxes & (AX (~Hares & ~Lynxes)))))))))"
    ovulation_behaviour = "3 {x}: (Foll & EF (E2 & Inh & Foll & EF (E2 & LH & ~P4 & Inh & ~CL & EF (~LH & ~P4 & CL & EF (~E2 & ~LH & P4 & ~Inh & ~Foll & CL & (EF {x}))))))"
    attractors_mc = ModelChecking.verify(stg, ovulation_behaviour)
    print(attractors_mc)
    print()


for model_path in gc_model_paths:
    print(model_path)
    model = BooleanNetwork.from_file(model_path, repair_graph=True)
    print(model.implicit_parameters())
    print(model.variables())
    for v in model.variables():
        print(model.get_variable_name(v), "=", model.get_update_function(v))

    stg = AsynchronousGraph.mk_for_model_checking(model, 2)

    attractors = Attractors.attractors(stg)

    print(attractors)
    for attractor in attractors:
        classes = Classification.classify_long_term_behavior(stg, attractor)
        print(classes)
    print()