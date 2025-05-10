library(BoolNet)

setwd("D:\\MUNI\\FI\\_mgr\\Diplomka\\boolean_gynCycle")

#
# BOVINE ESTROUS CYCLE MODEL
#

model_directory <- "model_2_bovine-estrous"

binarized_data <- read.delim(file.path(getwd(), model_directory, "simulation_binarized_rows_simplified_auto.csv"),
                             header = TRUE,
                             sep = ",",
                             row.names = 1,
                             stringsAsFactors = FALSE)
binarized_data
one_cycle <- binarized_data[2:27]

#
# full constraints
#
net <- reconstructNetwork(one_cycle,
                          method="bestfit",
                          readableFunctions=TRUE,
                          requiredDependencies=list("GnRH"=c("P4","E2"),"FSH"=c("Inh"),"LH"=c("GnRH","P4"),"Foll"=c("FSH","LH","P4"),"CL"=c("Foll","IOF","LH"),"P4"=c("CL"),"E2"=c("Foll"),"Inh"=c("Foll"),"PGF"=c("P4","E2"),"IOF"=c("PGF","CL")))

net
plotNetworkWiring(net)

ones_vector <- rep(1, length(net$genes))
custom_vector <- c(1, 1, 1, 4, 2, 2, 2, 3, 2, 4)
dontCareDefaults <- lapply(seq_along(net$interactions),
                           function(idx)
                             rep(F, sum(net$interactions[idx][[1]][[ones_vector[idx]]]$func == -1)))
bn <- chooseNetwork(net, ones_vector, dontCareValues=dontCareDefaults)
bn

toSBML(bn, file.path(getwd(), model_directory, "BoolNet", "bovine-estrous_full_constraints.sbml"))


#
# maxK = 4
#
net <- reconstructNetwork(one_cycle,
                          method="bestfit",
                          readableFunctions=TRUE,
                          maxK=4)
net
plotNetworkWiring(net)

ones_vector <- rep(1, length(net$genes))
custom_vector <- c(1, 1, 1, 4, 2, 2, 2, 3, 2, 4)
dontCareDefaults <- lapply(seq_along(net$interactions),
                           function(idx)
                             rep(F, sum(net$interactions[idx][[1]][[ones_vector[idx]]]$func == -1)))
bn <- chooseNetwork(net, ones_vector, dontCareValues=dontCareDefaults)
bn

toSBML(bn, file.path(getwd(), model_directory, "BoolNet", "bovine-estrous_maxK4.sbml"))
