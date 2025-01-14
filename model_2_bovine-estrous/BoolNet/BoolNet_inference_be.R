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

net <- reconstructNetwork(binarized_data,
                          method="bestfit",
                          maxK=4,
                          )
# full constraints lead to overfitting
net
plotNetworkWiring(net)

ones_vector <- rep(1, length(net$genes))
custom_vector <- c(1, 1, 1, 4, 2, 2, 2, 3, 2, 4)
dontCareDefaults <- lapply(seq_along(net$interactions),
                           function(idx)
                             rep(F, sum(net$interactions[idx][[1]][[ones_vector[idx]]]$func == -1)))
bn <- chooseNetwork(net, ones_vector, dontCareValues=dontCareDefaults)
bn

toSBML(bn, file.path(getwd(), model_directory, "BoolNet", "bovine-estrous.sbml"))
