import biodivine_aeon
from biodivine_aeon import *
import os


gc_model = os.path.join(os.getcwd(), "model_3_gyn-cycle")
boolnet_gc_model_path = os.path.join(gc_model, "BoolNet", "gyn-cycle.sbml")
euler_like_gc_model_path = os.path.join(gc_model, "euler-like_transformation", "gyn-cycle_model.aeon")
sailor_gc_model_path = os.path.join(gc_model, "SAILoR", "gyn-cycle_model.aeon")
gc_model_paths = [boolnet_gc_model_path,
                  euler_like_gc_model_path, sailor_gc_model_path]


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