from biodivine_aeon import *
import os


euler_like_pp_model_path = os.path.join(os.getcwd(), "predator-prey_model", "euler-like_transformation", "a_ge_b_d_l_g.aeon")
augusta_pp_model_path = os.path.join(os.getcwd(), "predator-prey_model", "augusta", "pp.sbml")
ideal_pp_model_path = os.path.join(os.getcwd(), "predator-prey_model", "ideal.aeon")
pp_model_paths = [euler_like_pp_model_path, augusta_pp_model_path, ideal_pp_model_path]

euler_like_be_model_path = os.path.join(os.getcwd(), "bovine-estrous_model", "euler-like_transformation", "first_model.aeon")
be_model_paths = [euler_like_be_model_path]

for model_path in pp_model_paths:
    model = BooleanNetwork.from_file(model_path)
    print(model_path)
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
    variables = model.variables()
    rabbits = HctlFormula(model.get_variable_name(variables[0]))
    foxes = HctlFormula(model.get_variable_name(variables[1]))
    both_zero = HctlFormula.mk_and(HctlFormula.mk_not(rabbits), HctlFormula.mk_not(foxes))
    rabbits_up = HctlFormula.mk_and(rabbits, HctlFormula.mk_not(foxes))
    both_up = HctlFormula.mk_and(rabbits, foxes)
    foxes_up = HctlFormula.mk_and(HctlFormula.mk_not(rabbits), foxes)
    # "(LH & EU(!P4, (E2 & EU(!LH, (P4 & EU(!E2, LH))))))"
    attractors_mc = ModelChecking.verify(stg, HctlFormula.mk_imp(both_zero, rabbits_up))
    print(attractors_mc)
    attractors_mc = ModelChecking.verify(stg, HctlFormula.mk_imp(rabbits_up, both_up))
    print(attractors_mc)
    attractors_mc = ModelChecking.verify(stg, HctlFormula.mk_imp(both_up, foxes_up))
    print(attractors_mc)
    attractors_mc = ModelChecking.verify(stg, HctlFormula.mk_imp(foxes_up, both_zero))
    print(attractors_mc)
    a1 = HctlFormula.mk_exist_until(HctlFormula.mk_not(rabbits_up), both_zero)
    a2 = HctlFormula.mk_and(both_up, a1)
    b1 = HctlFormula.mk_exist_until(HctlFormula.mk_not(both_zero), a2)
    b2 = HctlFormula.mk_and(rabbits_up, b1)
    c1 = HctlFormula.mk_exist_until(HctlFormula.mk_not(both_up), b2)
    c2 = HctlFormula.mk_and(both_zero, c1)
    print(c2)
    attractors_mc = ModelChecking.verify(stg, c2)
    print(attractors_mc)
    print()

for model_path in be_model_paths:
    model = BooleanNetwork.from_file(model_path)
    for v in model.variables():
        print(model.get_variable_name(v), "=", model.get_update_function(v))

    stg = AsynchronousGraph.mk_for_model_checking(model, 3)

    attractors = Attractors.attractors(stg)
    print(attractors)
    for attractor in attractors:
        classes = Classification.classify_long_term_behavior(stg, attractor)
        print(classes)
    lh = HctlFormula("LH")
    e2 = HctlFormula("E2")
    p4 = HctlFormula("P4")
    a1 = HctlFormula.mk_exist_until(HctlFormula.mk_not(e2), lh)
    a2 = HctlFormula.mk_and(p4, a1)
    b1 = HctlFormula.mk_exist_until(HctlFormula.mk_not(lh), a2)
    b2 = HctlFormula.mk_and(e2, b1)
    c1 = HctlFormula.mk_exist_until(HctlFormula.mk_not(p4), b2)
    c2 = HctlFormula.mk_and(lh, c1)
    print(c2)
    # "(LH & EU(!P4, (E2 & EU(!LH, (P4 & EU(!E2, LH))))))"
    attractors_mc = ModelChecking.verify(stg, c2)
    print(attractors_mc)
