# Script is to turn 
# SBC_LTER_cross_shelf_study_2008_5m_phyto_counts.csv long format.
# Also to programtically add some taxaonimc classifcations from the
# key provided here:
# (http://sbc.lternet.edu/cgi-bin/showDataset.cgi?docid=knb-lter-sbc.45&displaymodule=entity&entitytype=dataTable&entityindex=3)

# Created by: Andrew Bibian
# Date: 08/3/16

setwd(paste0("/Users/bibsian/Desktop/git/database-development/poplerGUI/",
             "Metadata_and_og_data/"))
## Install any required packages that are not currently installed 
## -----------------------------------------
# List required packages
adm.req <-c("dplyr", "tidyr")
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
filename = "SBC_LTER_cross_shelf_study_2008_5m_phyto_counts.csv"

# Path to file
data <- read.csv(paste0(getwd(),'/', filename))

# Reshaping with tidyr's 
# gather_ function (data, new column for all wide columns , new data column name, 
# columns to turn long)

longdata <- gather_(
  data, "TAXON_GENUS", "count", colnames(data)[5:length(colnames(data))])

# TAXON_GENUS name that belong to the class Bacillariophyceae
TAXON_CLASS <- c(
  "Pseudo.nitzschia", "Leptocylindrus", "Thalassiosira", "Chaetoceros",
  "Eucampia", "Rhizosolenia", "Skeletonema", "Nitzschia", "Navicula",
  "Asterionellopsis", "Meuniera", "Thalassionema", "Guinardia", 
  "Hemiaulus", "Ditylum", "Coscinodiscus", "Cylindrotheca", "Bacteriastrum",
  "Heliotheca", "stephanopyxis", "Corethron", "Pleurosigma", "Thalassiothrix",
  "Asteromphalus", "Licomorpha", "Odontella", "Lithodesmium", "Melosira",
  "Fragilariopsis", "Diatom.unknown")

# TAXON_GENUS name that belong to the TAXON_PHYLUM Dinoflagellata
TAXON_PHYLUM <- c(
  "Proocentrum", "Ceratium", "Akashiwo", "Lingulodinium", "Dinophysis", 
  "Scrippsiella", "Protoperidinium", "Gonyaulax", "Alexandrinium", "Noctiluca",
  "Oxytoxum", "Amylax", "Pyrocystis", "Dinoflagellate.unknown")

# Creating empty recrods to fill
longdata['TAXON_PHYLUM'] <- 'NA'
longdata['TAXON_CLASS']<- 'NA'


# loop over TAXON_GENUS names, compare to class or TAXON_PHYLUM vectors
# and write appropiate classification
for (i in 1:nrow(longdata)){
  if (longdata[i,'TAXON_GENUS'] %in% TAXON_CLASS ){
    longdata[i,'TAXON_CLASS'] <- "Bacillariophyceae"
  } else if(longdata[i,'TAXON_GENUS'] %in% TAXON_PHYLUM ){
    longdata[i,'TAXON_PHYLUM'] <- "Dinoflagellata"
  }
}

# Write long data to file
write.csv(longdata, paste0(getwd(),'/reshaped_files','/',"reshaped_", filename))

