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
filename = "37_BNZ_Defoliating_Insects_Werner_1975_2012.txt"

# Path to file
data <- read.table(paste0(getwd(),'/', filename), header=T, sep=',')

# Reshaping with tidyr's 
# gather_ function (data, new column for all wide columns , new data column name, 
# columns to turn long)

longdata <- gather_(
  data, "species_code", "count", colnames(data)[2:(length(colnames(data)))])

keys <- unique(longdata$species_code)
genus <- rep(NA,nrow(longdata))
species <- rep(NA,nrow(longdata))

write_genus <- c(
  'Choristoneura', 'Zeiraphera', 'Pristiphora', 'Rheumaptera',
  'Choristoneura', 'Chrysomela', 'Chryosemla; Phratora; Macrohalitca',
  'Phyllocnistis', 'Epinotia')

write_species <- c(
  'fumiferana', 'NA', 'erichsonii', 'hastata',
  'conflictana', 'NA', 'populiella',
  'solandriana')

for (i in 1:length(keys)){
  genus[c(which(longdata$species_code == keys[i]))] <- write_genus[i]
  species[c(which(longdata$species_code == keys[i]))] <- write_species[i]
}

# Adding columns to data
longdata['Taxa_genus'] <- genus
longdata['Taxa_species']<- species

unique(longdata['Taxa_genus'])
unique(longdata['Taxa_species'])

# Write long data to file
write.csv(
  longdata, 
  paste0(getwd(),'/reshaped_files','/',"reshaped_", filename),
  row.names = F)

