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
filename = "sev228_dipodomys_07132009.txt"
# Path to file
data <- read.table(paste0(getwd(),'/', filename), header=T, sep=',')

data$Taxa_kingdom <- 'Animalia'
data$Taxa_phylum <- 'Chordata'
data$Taxa_class <- 'Mammalia'
data$Taxa_order <- 'Rodentia'
data$Taxa_family <- 'Heteromyidae'
data$Taxa_genus <- 'Dipodomys'
data$Taxa_species <- 'spectabilis'
data$site <- 'KR_mark_recap'
data$count <- 1

# Write long data to file
write.csv(
  data, 
  paste0(getwd(),'/reshaped_files','/',"reshaped_", filename),
  row.names = F)

