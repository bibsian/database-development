# Script is to turn 
# VCR97038.csv format.

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
filename = "VCR97038.txt"
# Path to file
data <- read.table(paste0(getwd(),'/', filename), header=T)
head(data)

# Replacing '.' with NA
# -------
ind <- which(data == '.', arr.ind = T)
data[cbind(ind[ ,1], ind[ ,2])] <- NA


# Adding taxa information
# ----------
spp_code <- c(1:8)

order <- c(
  'Euilpotyphla', rep('Rodentia', 6), 'Eulipotyphla' 
  )
family <- c(
  'Soricidae', 'Muridae', rep('Cricetidae', 3), 'Muridae', 'Dipodidae', 'Soricidae'
  )
genus <- c(
    'Cryptotis', 'Mus', 'Microtus', 'Oryzomys', 'Peromyscus', 'Rattus',
    'Zapus', 'Blarina'
  )
species <- c(
    'parva', 'musculus', 'pennsylvanicus', 'palustris', 'leucopus',
    'norvegicus', 'hudsonius', 'brevicauda'
  )
length(spp_code)
length(order)
length(family)
length(genus)
length(species)

data$Taxa_order <- rep(NA, nrow(data))
data$Taxa_family <- rep(NA, nrow(data))
data$Taxa_genus <- rep(NA, nrow(data))
data$Taxa_species <- rep(NA, nrow(data))

for (i in 1:length(spp_code)){
  data$Taxa_order[c(which(as.character(
    data$SPECIES) == spp_code[i]))] <- order[i]
  data$Taxa_family[c(which(as.character(
    data$SPECIES) == spp_code[i]))] <- family[i]
  data$Taxa_genus[c(which(as.character(
    data$SPECIES) == spp_code[i]))] <- genus[i]
  data$Taxa_species[c(which(as.character(
    data$SPECIES) == spp_code[i]))] <- species[i]
}

data$count <- rep(1, nrow(data))
# Write long data to file
# --------
write.csv(
  data, 
  paste0(getwd(),'/reshaped_files','/',"reshaped_", filename),
  row.names = F)

