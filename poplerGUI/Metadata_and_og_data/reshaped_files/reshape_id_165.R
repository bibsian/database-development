# Script is to turn 
# 504_BNZ_Beetles_Kruse_1975-2013.txt long format.


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
filename = "504_BNZ_Beetles_Kruse_1975-2013.txt"

# Path to file
data <- read.table(paste0(getwd(),'/', filename), header=T, sep=',')

# Reshaping with tidyr's 
# gather_ function (data, new column for all wide columns , new data column name, 
# columns to turn long)

longdata <- gather_(
  data, "species_code", "count", colnames(data)[4:(length(colnames(data))-3)])

# splitting genus speies column
genus <- do.call(
  rbind,lapply(str_split(longdata$species_code, "[.]"), function(x) x[1]))

species <- do.call(
  c,lapply(str_split(longdata$species_code, "[.]"), function(x) x[2]))

species[which(species=='Cerambicid')] <- 'NA'
species[which(species=='Buprestid')] <- 'NA'
unique(species)

# Adding columns to data
longdata['Taxa_genus'] <- genus
longdata['Taxa_species']<- species

unique(longdata['Taxa_genus'])
unique(longdata['Taxa_species'])


# Making family column based off metadata
family <- do.call(
  c,lapply(str_split(longdata$species_code, "[.]"), function(x) x[2]))

family[c(which(family=='Cerambicid'))] <- 'Cerambycidae'
family[c(which(family=='Buprestid'))] <- 'Buprestidae'

family[c(which(family!='Cerambicidae' & family!='Buprestidae'))] <- 'NA'
unique(family)

longdata['Taxa_family'] <- family
unique(longdata['Taxa_family'])

# Removing data points that are sums of records
longdata_subset <- longdata[-which(longdata$Location == 'All'), ]

# Write long data to file
write.csv(
  longdata_subset, 
  paste0(getwd(),'/reshaped_files','/',"reshaped_", filename),
  row.names = F)

