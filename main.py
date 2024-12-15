from supporting_scripts import *

wc = os.getcwd()


"""
    Predator-prey model abstractions
"""

# euler-like transformation from .ode file to .aeon file
ode_file = os.path.join(wc, "predator-prey_model", "predator-prey_ODE_model.ode")
aeon_file = os.path.join(wc, "predator-prey_model", "euler-like_transformation", "predator-prey_model.aeon")
predator_prey_euler_transform_to_aeon(ode_file, aeon_file)



"""
    Bovine-estrous cycle abstractions
"""

# euler-like transformation from .ode file to .aeon file
ode_file = os.path.join(wc, "bovine-estrous_model", "bovine-estrous-cycle_ODE_model.ode")
aeon_file = os.path.join(wc, "bovine-estrous_model", "euler-like_transformation", "bovine-estrous-cycle_model.aeon")
bovine_estrous_euler_transform_to_aeon(ode_file, aeon_file)
