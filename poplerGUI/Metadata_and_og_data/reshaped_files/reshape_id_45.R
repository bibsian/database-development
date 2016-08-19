# Script is to turn 
# sev023_rabbitpopns_20150310.txt format.
# http://sev.lternet.edu/data/sev-23

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
filename = "sev023_rabbitpopns_20150310.txt"
# Path to file
data <- read.table(paste0(getwd(),'/', filename), header=T, sep=',')

# Reshaping with tidyr's 
# gather_ function (data, new column for all wide columns , new data column name, 
# columns to turn long)


gen_spp <- do.call(
  rbind, str_split(c('Lepus californicus', 'Sylvilagus auduboni'), ' ' ))

keys <- unique(as.character(trimws(data$species)))[1:2]

genus <- vector()
species <- vector()
for (i in 1:length(keys)){
  genus[c(which(as.character(data$species) == keys[i]))] <- gen_spp[i,1]
  species[c(which(as.character(data$species) == keys[i]))] <- gen_spp[i,2]
}

# Adding columns to data
data['Taxa_genus'] <- genus
data['Taxa_species']<- species

unique(data['Taxa_genus'])
unique(data['Taxa_species'])

colnames(data)[8] <- 'Taxa_sppcode'

# Write long data to file
write.csv(
  data, 
  paste0(getwd(),'/reshaped_files','/',"reshaped_", filename),
  row.names = F)

