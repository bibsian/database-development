# Script is to turn 
# VCR09158.csv format.

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
filename = "VCR09158.csv"
# Path to file
data <- read.table(paste0(getwd(),'/', filename), header=T, sep=',')
# Removing the total column; no  need when converting data to long format
data <- data[, !(colnames(data) == 'Total')]

# Reshaping with tidyr's 
# gather_ function (data, new column for all wide columns , new data column name, 
# columns to turn long)
# ---------
longdata <- gather_(
  data, "species_code", "count", colnames(data)[3:(length(colnames(data))-3)])


# Adding taxa information
# ----------
spp_code <- unique(longdata$species_code)
family <- c(rep('Ardeidae', length(spp_code)-2), rep('Threskiornithidae', 2))
genus <- c(
  'Nycticorax', 'Ardea', 'Egretta', 'Bubulcus', 'Egretta', 'Egretta', 
  'Plegadis', 'Eudocimus')
species <- c(
  'nycticorax', 'alba', 'thula', 'ibis', 'tricolor', 'caerulea', 
  'falcinellus', 'albus')


longdata$Taxa_family <- rep(NA, nrow(longdata))
longdata$Taxa_genus <- rep(NA, nrow(longdata))
longdata$Taxa_species <- rep(NA, nrow(longdata))

for (i in 1:length(spp_code)){
  longdata$Taxa_family[c(which(as.character(
    longdata$species_code) == spp_code[i]))] <- family[i]
  longdata$Taxa_genus[c(which(as.character(
    longdata$species_code) == spp_code[i]))] <- genus[i]
  longdata$Taxa_species[c(which(as.character(
    longdata$species_code) == spp_code[i]))] <- species[i]
}
longdata$Colony[longdata$Colony==''] <- NA
longdata_colony_na_omit <- longdata[-c(which(is.na(longdata$Colony))),]

nrow(longdata)
nrow(longdata_colony_na_omit)

# Write long data to file
# --------
write.csv(
  longdata_colony_na_omit, 
  paste0(getwd(),'/reshaped_files','/',"reshaped_", filename),
  row.names = F)

