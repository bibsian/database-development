# Created by: Andrew Bibian
# Date: 08/3/16

setwd(paste0("/Users/bibsian/Desktop/git/database-development/poplerGUI/",
             "Metadata_and_og_data/"))
## Install any required packages that are not currently installed 
## -----------------------------------------
# List required packages
adm.req <-c("dplyr", "tidyr", "stringr", "lubridate")
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
filename = "sev017_birdpop_09251997.txt"
spp = "SEV_id_32_species_list.txt"
# Path to files
data <- read.table(paste0(getwd(),'/', filename), header=T, sep=',')

spplist <- read.csv(paste0(getwd(),'/', spp), header=T, sep='\t')
# Adding kingdom classification to species key file
spplist$Taxa_kingdom <- rep('Plantae', nrow(spplist))

# Taking the codes from the species list
# and designating them as keys for the taxa table that will
# be made
keys <- as.character(spplist$Taxa_sppcode)
key_translation <- c(
  'Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 
  'Taxa_family', 'Taxa_genus', 'Taxa_species')
taxa_headers <- c(
  'Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 
  'Taxa_family', 'Taxa_genus', 'Taxa_species')

# Adding headers to 
for (i in taxa_headers){
  data[,i] = NA
}

for (i in 1:nrow(spplist)){
  for(j in 1:length(taxa_headers)){
    data[which(
      as.numeric(trimws(as.character(data$species_number))) == as.numeric(trimws(
        as.character(spplist$numer)))[i]), 
      taxa_headers[j]] <- as.character(spplist[i, key_translation[j]])
  }
}
data$presence <- rep(1, nrow(data))

#data_codes <- sort(unique(as.character(data$p_id)))
#taxa_key_codes <-sort(as.character(unique(spplist$spp_id)))
#code_matches <- which(data_codes %in% taxa_key_codes)

#taxa_key_codes_match <- data_codes[code_matches]
#taxa_key_codes_nomatch <-data_codes[-code_matches]
#spplist$spp_id

# Write long data to file
write.csv(
  data, 
  paste0(getwd(),'/reshaped_files','/',"reshaped_", filename),
  row.names = F)

