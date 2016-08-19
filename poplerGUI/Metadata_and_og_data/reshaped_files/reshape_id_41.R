# Script is to turn 
# 37_BNZ_Defoliating_Insects_Werner_1975_2012.txtlong format.
# http://www.lter.uaf.edu/data/data-detail/id/37

# Created by: Andrew Bibian
# Date: 08/3/16

setwd(paste0("/Users/bibsian/Desktop/git/database-development/poplerGUI/",
             "Metadata_and_og_data/"))
## Install any required packages that are not currently installed 
## -----------------------------------------
# List required packages
adm.req <-c("dplyr", "tidyr", "stringr")
# Load currently installed, required packages
tmp <- lapply(adm.req, require, character.only = T)
# Find the required packages that still need to be installed
adm.need <- adm.req[!(paste0("package:",adm.req) %in% search())]
# Install required packages that are not currently installed
if(length(adm.need)>0){ install.packages(adm.need,dependencies=T) }
# Now, make sure all packages are loaded
tmp <- lapply(adm.req, require, character.only = T)
tmp
# -------

# File to edit
filename = "sev198_pdoghoppermound_01142009.txt"
spp = "SEV_grasshopper_species_list.txt"
# Path to file
data <- read.table(paste0(getwd(),'/', filename), header=T, sep=',')
spplist <- read.table(paste0(getwd(),'/', spp), header=T, sep='\t')
# Reshaping with tidyr's 
# gather_ function (data, new column for all wide columns , new data column name, 
# columns to turn long)
data

keys <- as.character(spplist$CODE)

data$Taxa_genus <- NA
data$Taxa_species <- NA

for (i in 1:length(keys)){
  data$Taxa_genus[c(which(as.character(data$SPP) == keys[i]))] <- 
    as.character(spplist$Taxa_genus)[i]
  data$Taxa_species[c(which(as.character(data$SPP) == keys[i]))] <- 
    as.character(spplist$Taxa_species)[i]
  
}


# Write long data to file
write.csv(
  data, 
  paste0(getwd(),'/reshaped_files','/',"reshaped_", filename),
  row.names = F)

