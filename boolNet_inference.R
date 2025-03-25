library(BoolNet)

setwd("D:\\MUNI\\FI\\_mgr\\Diplomka\\boolean_gynCycle")


#
# GYNCYCLE MODEL
#
model_directory <- "model_3_gyn-cycle"

binarized_data <- read.delim(file.path(getwd(), model_directory, "/gyn_cycle_sim_rows_binarized_simplified_auto.csv"),
                             header = TRUE,
                             sep = ",",
                             row.names = 1,
                             stringsAsFactors = FALSE)
binarized_data

#
# full constraints
#
net <- reconstructNetwork(binarized_data,
                          method="bestfit",
                          maxK=5,
                          readableFunctions=TRUE,
                          requiredDependencies=list("LH_Pit"=c("GnRH_R_a","LH_Pit","P4","E2"),"LH_bld"=c("GnRH_R_a","LH_bld","LH_Pit","R_LH"),"FSH_pit"=c("GnRH_R_a","FSH_pit","InhB","freq"),"FSH_bld"=c("GnRH_R_a","FSH_pit","FSH_bld","R_FSH"),"R_FSH"=c("R_FSH_des","FSH_bld","R_FSH"),"FSH_R"=c("FSH_bld","R_FSH","FSH_R"),"R_FSH_des"=c("R_FSH_des","FSH_R"),"R_LH"=c("R_LH_des","LH_bld","R_LH"),"LH_R"=c("LH_bld","R_LH","LH_R"),"R_LH_des"=c("R_LH_des","LH_R"),"R_Foll"=c("FSH_bld","R_Foll","P4"),"AF1"=c("FSH_R","AF1"),"AF2"=c("R_Foll","FSH_R","LH_R","AF2","AF1"),"AF3"=c("R_Foll","FSH_R","LH_R","AF2","AF3"),"AF4"=c("R_Foll","LH_R","AF4","AF3"),"PrF"=c("R_Foll","LH_R","AF4","PrF"),"OvF"=c("R_Foll","LH_R","PrF","OvF"),"Sc1"=c("Sc1","OvF"),"Sc2"=c("Sc1","Sc2"),"Lut1"=c("GnRH_R_a","Lut1","Sc2"),"Lut2"=c("GnRH_R_a","Lut1","Lut2"),"Lut3"=c("GnRH_R_a","Lut3","Lut2"),"Lut4"=c("GnRH_R_a","Lut3","Lut4"),"E2"=c("LH_bld","Lut1","Lut4","AF4","AF2","PrF","AF3","E2"),"P4"=c("Lut4","P4"),"InhA"=c("Lut1","Lut3","Lut4","Lut2","InhA","Sc1","PrF"),"InhB"=c("InhB","AF2","Sc2"),"InhA_delay"=c("InhA_delay","InhA"),"freq"=c("P4","E2"),"mass"=c("E2"),"GnRH"=c("GnRH_R_a","R_GnRH_a","GnRH","mass","freq"),"R_GnRH_a"=c("R_GnRH_i","GnRH_R_a","R_GnRH_a","GnRH"),"R_GnRH_i"=c("GnRH_R_i","R_GnRH_i","R_GnRH_a"),"GnRH_R_a"=c("GnRH_R_i","GnRH_R_a","R_GnRH_a","GnRH"),"GnRH_R_i"=c("GnRH_R_i","GnRH_R_a")))

net
plotNetworkWiring(net)

ones_vector <- rep(1, length(net$genes))
dontCareDefaults <- lapply(seq_along(net$interactions),
                          function(idx)
                          rep(F, sum(net$interactions[idx][[1]][[ones_vector[idx]]]$func == -1)))
names(dontCareDefaults) <- net$genes
bn <- chooseNetwork(net, ones_vector, dontCareValues=dontCareDefaults)
bn

toSBML(bn, file.path(getwd(), model_directory, "BoolNet", "gyn-cycle_full_constraints.sbml"))

#
# maxK = 4 only
#
net <- reconstructNetwork(binarized_data,
                          method="bestfit",
                          maxK=4,
                          readableFunctions=TRUE)
net
plotNetworkWiring(net)

ones_vector <- rep(1, length(net$genes))
dontCareDefaults <- lapply(seq_along(net$interactions),
                           function(idx)
                             rep(F, sum(net$interactions[idx][[1]][[ones_vector[idx]]]$func == -1)))
names(dontCareDefaults) <- net$genes
bn <- chooseNetwork(net, ones_vector, dontCareValues=dontCareDefaults)
bn

toSBML(bn, file.path(getwd(), model_directory, "BoolNet", "gyn-cycle_maxK4.sbml"))

#
# maxK = 8 only
#
net <- reconstructNetwork(binarized_data,
                          method="bestfit",
                          maxK=8,
                          readableFunctions=TRUE)
net
plotNetworkWiring(net)

ones_vector <- rep(1, length(net$genes))
dontCareDefaults <- lapply(seq_along(net$interactions),
                           function(idx)
                             rep(F, sum(net$interactions[idx][[1]][[ones_vector[idx]]]$func == -1)))
names(dontCareDefaults) <- net$genes
bn <- chooseNetwork(net, ones_vector, dontCareValues=dontCareDefaults)
bn

toSBML(bn, file.path(getwd(), model_directory, "BoolNet", "gyn-cycle_maxK8.sbml"))

