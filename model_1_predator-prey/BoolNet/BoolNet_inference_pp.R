library(BoolNet)

setwd("D:\\MUNI\\FI\\_mgr\\Diplomka\\boolean_gynCycle")

#
# PREDATOR-PREY MODEL
#

model_directory <- "model_1_predator-prey"


# BN inference using binarized Hudson's Bay dataset
binarized_data <- read.delim(file.path(getwd(), model_directory, "Leigh1968_harelynx_rows_binarized_simplified.csv"),
                             header = TRUE,
                             sep = ",",
                             row.names = 1,
                             stringsAsFactors = FALSE)
binarized_data

net <- reconstructNetwork(binarized_data,
                          method="bestfit",
                          maxK=2,
                          readableFunctions=TRUE,
                          requiredDependencies=list("Hares"=c("Lynxes", "Hares"), "Lynxes"=c("Hares", "Lynxes")))
net
plotNetworkWiring(net)

bn <- chooseNetwork(net, c(1, 1))
bn

toSBML(bn, file.path(getwd(), model_directory, "BoolNet", "predator-prey_hudsonBayDataset.sbml"))



# BN inference using binarized simulation data
binarized_data <- read.delim(file.path(getwd(), model_directory, "predator_prey_ODE_sim_binarized_k_means_simplified.csv"),
                             header = TRUE,
                             sep = ",",
                             row.names = 1,
                             stringsAsFactors = FALSE)
binarized_data
net <- reconstructNetwork(binarized_data,
                          method="bestfit",
                          maxK=2,
                          readableFunctions=TRUE,
                          requiredDependencies=list("Hares"=c("Lynxes", "Hares"), "Lynxes"=c("Hares", "Lynxes")))
net
plotNetworkWiring(net)

bn <- chooseNetwork(net, c(1, 1))
bn

toSBML(bn, file.path(getwd(), model_directory, "BoolNet", "predator-prey_simDataset.sbml"))
