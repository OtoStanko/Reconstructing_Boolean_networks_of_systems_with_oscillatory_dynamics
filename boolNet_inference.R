library(BoolNet)

setwd("D:\\MUNI\\FI\\_mgr\\Diplomka\\boolean_gynCycle")


#
# PREDATOR-PREY MODEL
#

binarized_data <- read.delim(file.path(getwd(), "predator-prey_model/predator_prey_ODE_sim_binarized_k_means _simplified.csv"),
                             header = TRUE,
                             sep = ",",
                             row.names = 1,
                             stringsAsFactors = FALSE)
binarized_data

net <- reconstructNetwork(binarized_data,
                          method="bestfit",
                          maxK=2,
                          requiredDependencies=list("Rabbits"=c("Foxes"), "Foxes"=c("Rabbits")))
net
plotNetworkWiring(net)

bn <- chooseNetwork(net, c(1, 1))
bn

toSBML(bn, file.path(getwd(), "predator-prey_model", "BoolNet", "predator-prey.sbml"))


#
# GYNCYCLE MODEL
#

binarized_data <- read.delim(file.path(getwd(), "gyn-cycle_model/simulation_binarized_rows_simplified_auto.csv"),
                             header = TRUE,
                             sep = ",",
                             row.names = 1,
                             stringsAsFactors = FALSE)
binarized_data

net <- reconstructNetwork(binarized_data,
                          method="bestfit",
                          maxK=8,
                          )
net
plotNetworkWiring(net)

ones_vector <- rep(1, 38)
dontCareDefaults <- lapply(seq_along(net$interactions),
                          function(idx)
                          rep(F, sum(net$interactions[idx][[1]][[ones_vector[idx]]]$func == -1)))
names(dontCareDefaults) <- net$genes
bn <- chooseNetwork(net, ones_vector, dontCareValues=dontCareDefaults)
bn

toSBML(bn, file.path(getwd(), "gyn-cycle_model", "BoolNet", "predator-prey.sbml"))
