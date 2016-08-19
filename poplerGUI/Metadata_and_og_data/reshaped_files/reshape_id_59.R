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
filename = "sev081_waterbalance_03022011_0.txt"
spp = "SEV_species_list_master.txt"
# Path to files
data <- read.table(paste0(getwd(),'/', filename), header=T, sep=',')

spplist <- read.csv(paste0(getwd(),'/', spp), header=T, sep=',')
# Adding kingdom classification to species key file
spplist$Taxa_kingdom <- rep('Plantae', nrow(spplist))

# Taking the codes from the species list
# and designating them as keys for the taxa table that will
# be made
keys <- as.character(spplist$species_code)
key_translation<- c('Taxa_kingdom', 'family', 'genus', 'species')
taxa_headers <- c('Taxa_kingdom', 'Taxa_family', 'Taxa_genus', 'Taxa_species')
# Adding headers to 
for (i in taxa_headers){
  data[,i] = NA
}

for (i in 1:nrow(spplist)){
  for(j in 1:length(taxa_headers)){
    data[which(
      trimws(as.character(data$species_code)) == trimws(
        as.character(spplist$species_code))[i]), 
      taxa_headers[j]] <- as.character(spplist[i, key_translation[j]])
  }
}

data$updated_cover <- as.character(data$value)
data$updated_cover[which(as.character(data$updated_cover) == '+')] <- 0.5
data$updated_cover <- as.numeric(data$updated_cover)

data$date_updated <- ymd(data$date)

# Write long data to file
write.csv(
  data, 
  paste0(getwd(),'/reshaped_files','/',"reshaped_", filename),
  row.names = F)

