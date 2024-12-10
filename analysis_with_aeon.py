from biodivine_aeon import *
import os


euler_like_pp_model_path = os.path.join(os.getcwd(), "predator-prey_model", "euler-like_transformation", "a_ge_b_d_l_g.aeon")
augusta_pp_model_path = os.path.join(os.getcwd(), "predator-prey_model", "augusta", "pp.sbml")
ideal_pp_model_path = os.path.join(os.getcwd(), "predator-prey_model", "ideal.aeon")
model_paths = [euler_like_pp_model_path, augusta_pp_model_path, ideal_pp_model_path]

for model_path in model_paths:
    model = BooleanNetwork.from_file(model_path)
    print(model.implicit_parameters())
    print(model.variables())
    for v in model.variables():
        print(model.get_variable_name(v), "=", model.get_update_function(v))

    stg = AsynchronousGraph(model)

    attractors = Attractors.attractors(stg)

    print(attractors)
    for attractor in attractors:
        classes = Classification.classify_long_term_behavior(stg, attractor)
        print(classes)
    print()