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
filename = "sev267_Konza-KrugersppcompKonza_03142012.txt"
spp = "SEV_species_list_master.txt"
# Path to files
data <- read.table(paste0(getwd(),'/', filename), header=T, sep=',')

spplist <- read.csv(paste0(getwd(),'/', spp), header=T, sep=',')

# Adding kingdom classification to species key file
spplist$Taxa_kingdom <- rep('Plantae', nrow(spplist))

# Taking the codes from the species list
# and designating them as keys for the taxa table that will
# be made
keys <- as.character(spplist$species)
key_translation<- c('Taxa_kingdom', 'family')
taxa_headers <- c('Taxa_kingdom', 'Taxa_family')
# Adding headers to 
for (i in taxa_headers){
  data[,i] = NA
}

# based on species
for (i in 1:nrow(spplist)){
  for(j in 1:length(taxa_headers)){
    data[which(
      trimws(as.character(data$species)) == trimws(
        as.character(spplist$species))[i]), 
      taxa_headers[j]] <- as.character(spplist[i, key_translation[j]])
  }
}

colnames(data)[which(colnames(data)=='genus')] <- 'Taxa_genus'
colnames(data)[which(colnames(data)=='species')] <- 'Taxa_species'
data$Taxa_kingdom <- 'Plantae'
# Write long data to file
write.csv(
  data, 
  paste0(getwd(),'/reshaped_files','/',"reshaped_", filename),
  row.names = F)

unique(data[which(as.character(data$ws) == 'n4d'), ]$year)
