import os

from supporting_scripts import *

wc = os.getcwd()


"""**********************************
    Predator-prey model abstractions
**********************************"""
pp_model = os.path.join(wc, "predator-prey_model")

"""
euler-like transformation from .ode file to .aeon file
"""
ode_file_pp = os.path.join(pp_model, "predator-prey_ODE_model.ode")
aeon_file_pp = os.path.join(pp_model, "euler-like_transformation", "predator-prey_model.aeon")
#ode_eulerlike_transform_to_aeon(ode_file_pp, aeon_file_pp)

#ode_system_pp = ODESystem(ode_file_pp)
#ode_system_pp.to_network(os.path.join(pp_model, "prior_network_pp.tsv"))

"""
SAILoR inference from time series and prior networks
"""
from SAILoR.SAILoR import ContextSpecificDecoder

time_series_data_predator_prey = os.path.join(pp_model, "predator_prey_ODE_sim_results.csv")
prior_network_predator_prey = os.path.join(pp_model, "prior_network_pp.tsv")

"""decoder = ContextSpecificDecoder(timeSeriesPath=time_series_data_predator_prey,
                                 referenceNetPaths=[prior_network_predator_prey])
print(decoder)
best = decoder.run()

boolean_expressions = []
for bfun in best:
    boolean_expressions.append(bfun[4])"""


"""**********************************
    Bovine-estrous cycle abstractions
**********************************"""
be_model = os.path.join(wc, "bovine-estrous_model")

"""
euler-like transformation from .ode file to .aeon file
"""
ode_file_be = os.path.join(be_model, "bovine-estrous-cycle_ODE_model.ode")
aeon_file_be = os.path.join(be_model, "euler-like_transformation", "bovine-estrous-cycle_model.aeon")
#ode_eulerlike_transform_to_aeon(ode_file_be, aeon_file_be)


"""**********************************
    Gyn cycle abstractions
**********************************"""
gc_model = os.path.join(wc, "gyn-cycle_model")

"""
euler-like transformation from .ode file to .aeon file
"""
ode_file_gc = os.path.join(gc_model, "gyn-cycle_ODE_model.ode")
aeon_file_gc = os.path.join(gc_model, "euler-like_transformation", "gyn-cycle_model.aeon")
#ode_eulerlike_transform_to_aeon(ode_file_gc, aeon_file_gc)

#ode_system_gc = ODESystem(ode_file_gc)
#ode_system_gc.to_network(os.path.join(gc_model, "prior_network_gc.tsv"))

"""
SAILoR inference from time series and prior networks
"""

"""time_series_data_gyn_cycle = os.path.join(wc, "gyn-cycle_model", "copasi_simulation_100d.csv")
prior_network_gyn_cycle = os.path.join(wc, "gyn-cycle_model", "prior_network_gc.csv")

decoder = ContextSpecificDecoder(timeSeriesPath=time_series_data_gyn_cycle,
                                 referenceNetPaths=[prior_network_gyn_cycle])
print(decoder)
best = decoder.run()

boolean_expressions = []
for bfun in best:
    boolean_expressions.append(bfun[4])"""