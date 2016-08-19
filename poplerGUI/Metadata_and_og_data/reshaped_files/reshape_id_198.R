# Script is to add a count column since it's trap data
# 55_Hare_Data_2012.txt 
# http://www.lter.uaf.edu/data/data-detail/id/55

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
filename = "55_Hare_Data_2012.txt"

# Path to file
data <- read.table(paste0(getwd(),'/', filename), header=T, sep=',')

data$count <- rep(1, nrow(data))

# Path to file
replace_values <- subset(data, select = -c(date))

inds <- which(replace_values == '-', arr.ind = T)
replace_values[inds]<- NA
replace_values$date <- data$date

# Write long data to file
write.csv(
  replace_values, 
  paste0(getwd(),'/reshaped_files','/',"reshaped_", filename),
  row.names = F)
