# Script is to turn 
# VCR97035.csv format.

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
filename = "VCR97035.csv"
# Path to file
data <- read.table(paste0(getwd(),'/', filename), header=T, sep=',')
# Removing the total column; no  need when converting data to long format
data <- data[, !(colnames(data) == 'Total')]

# Reshaping with tidyr's 
# gather_ function (data, new column for all wide columns , new data column name, 
# columns to turn long)
# ---------
longdata <- gather_(
  data, "plot", "cover", colnames(data)[3:(length(colnames(data)))])

# Separating plot/quadrat combo name 
head(longdata)
longdata$quadrats <- do.call(
  c, lapply(strsplit(longdata$plot, '[A-Z]{4,}[0-9]'), function(x) x[2]))
longdata$plot_id <- do.call(
  c, lapply( strsplit(longdata$plot, '[AB]{1}'), function(x) x[1]))


# Adding taxa information
# ----------
spp_code <- c(as.character(unique(longdata$Species)))
kingdom <- c('Plantae', 'NA', 'NA', rep('Plantae', 6))
order <- c(
  'Poales', 'NA', 'NA', rep('Poales', 3), 'Caryophyllales', 'Caryophyllales', 
  'Poales')
family <- c(
  'Juncaceae', 'NA', 'NA', 'Poaceae', 'Poaceae', 'Poaceae', 'Plumbaginaceae',
  'Amarathaceae', 'Poaceae')
genus <- c(
  'Juncus', 'NA', 'NA', 'Spartina', 'Spartina', 'Distichlis', 'Limonium', 
  'Salicornioideae', 'Spartina; Distichlis')
species <- c(
  'roemerianus', 'NA', 'NA', 'alterniflora', 'patens', 'spicata', 'NA',
  'NA', 'patens; spicata')
length(kingdom)
length(order)
length(family)
length(genus)
length(species)

longdata$Taxa_kingdom <- rep(NA, nrow(longdata))
longdata$Taxa_order <- rep(NA, nrow(longdata))
longdata$Taxa_family <- rep(NA, nrow(longdata))
longdata$Taxa_genus <- rep(NA, nrow(longdata))
longdata$Taxa_species <- rep(NA, nrow(longdata))

for (i in 1:length(spp_code)){
  longdata$Taxa_kingdom[c(which(as.character(
    longdata$Species) == spp_code[i]))] <- kingdom[i]
  longdata$Taxa_order[c(which(as.character(
    longdata$Species) == spp_code[i]))] <- order[i]
  longdata$Taxa_family[c(which(as.character(
    longdata$Species) == spp_code[i]))] <- family[i]
  longdata$Taxa_genus[c(which(as.character(
    longdata$Species) == spp_code[i]))] <- genus[i]
  longdata$Taxa_species[c(which(as.character(
    longdata$Species) == spp_code[i]))] <- species[i]
}

longdata$site <- 'UPC'

head(longdata)

# Write long data to file
# --------
write.csv(
  longdata, 
  paste0(getwd(),'/reshaped_files','/',"reshaped_", filename),
  row.names = F)

