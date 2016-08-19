# Script is to turn 
# sev008_rodentpopns_20160701.csv format.
# http://sev.lternet.edu/data/sev-008/4786

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
filename = "sev008_rodentpopns_20160701.csv"
spp = "SEV_id_58_species_list.txt"

# Path to file
data <- read.table(paste0(getwd(),'/', filename), header=T, sep=',')
spplist <- read.table(paste0(getwd(),'/', spp), header=T, sep=',')

# Turnig the species list dataframe into columns to append to 
# raw data
# ----------------
keys <- as.character(spplist$code)
genus <- as.character(spplist$gen)
species <- as.character(spplist$spp)
data$Taxa_genus <- rep(NA, nrow(data))
data$Taxa_species <- rep(NA, nrow(data))

# Making genus and species columns
# ---------
for (i in 1:length(keys)){
  data$Taxa_genus[c(which(as.character(data$species) == keys[i]))] <- genus[i]
  data$Taxa_species[c(which(as.character(data$species) == keys[i]))] <- species[i]
}

# Chanign 'species' column name to code (which it is)
# -----------

colnames(data)[8] <- 'Taxa_sppcode'
# Adding Count column
# -----------
data$count <- rep(1, nrow(data))

#Making family and order columns
# -------
unq_genus <- unique(genus) 
family <- c(
  'Sciuridae', 'Sciuridae', 'Sciuridae', 'Heteromyidae', 'Heteromyidae',
  'Heteromyidae', 'Cricetidae', 'Cricetidae', 'Cricetidae', 'Cricetidae',
  'Cricetidae', 'Leporidae', 'NA')
order <- c(
  rep('Rodentia', length(unq_genus)-2), 'Lagomorpha', 'NA' )
data$Taxa_family <- rep(NA, nrow(data))
data$Taxa_order <- rep(NA, nrow(data))

for (i in 1:length(unq_genus)){
  data$Taxa_family[c(which(as.character(data$Taxa_genus) == unq_genus[i]))] <- family[i]
  data$Taxa_order[c(which(as.character(data$Taxa_genus) == unq_genus[i]))] <- order[i]
}

# ---------

# Write long data to file
write.csv(
  data, 
  paste0(getwd(),'/reshaped_files','/',"reshaped_", filename),
  row.names = F)


