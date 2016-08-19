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
filename = "sev13_rodentparasite_02182011.txt"
spp = "SEV_id_25_species_list.txt"
# Path to file
data <- read.table(paste0(getwd(),'/', filename), header=T, sep=',')
spplist <- read.table(paste0(getwd(),'/', spp), header=T, sep=',')

# Taking the codes from the species list
# and designating them as keys for the taxa table that will
# be made
keys <- as.character(spplist$spp_id)

# Taking the 'genus' column of the list and actually
# identify with classifcation the name represents
genus_unchanged <- as.character(spplist$gen)

true_taxa <- c(
  'Taxa_phylum', # acanthocephala (Acanthocephala)
  # (Kingdom:Animalia)
  
  'Taxa_genus', # Adelina
  # (Kingdom:Chromalveolata, Phylum:Apicomplexa, Class:Conoidasida, 
  # Order:Eucoccidiorida, Family:Eimeriidae)
  
  'Taxa_genus', # Catenotaenia
  #(Kingdom:Animalia, Phylum:Platyhelminthes, Class:Catenotaeniidae)
  
  rep('Taxa_genus', 3), # Cuterebra*3 
  # (Animalia, Phylum:Arthropoda, Class:Insecta, Order:Diptera, Family:Oestridae)
  
  'Taxa_class', # cestode
  # (Kingdom:Animalia, Phylum:Platyhelminthes)
  
  rep('Taxa_genus', 27), # Eimeria*27
  'Taxa_order', # Siphonaptera
  # (Animalia, Arthropoda, Insecta)
  
  rep('Taxa_genus', 4), # Heteromyoxyuris, Hymenolepis, Isospora*2
  # (K:Animalia, P:Nematoda, C:Secernentea, O:Ascaridida, F:Oxyuridae)
  # (K:Animalia, P:Platyhelminthes, C:Cestoda, O:Cyclophylidea, F:Hymenolepididae)
  
  'Taxa_suborder', # Mallophaga; Anoplura 
  # (Animalia, Phylum:Arthropoda, Class: Insect, Order:Phthriaptera);
  # (Animalia, Phylum:Arthropoda, Class: Insect, Order:Polotitas)
  
  rep('Taxa_genus', 2), # Mastophrus, Mathovetaenia
  # (K:Animalia, P:Nematoda, C:Secernentea, O:Spirurida, F:Spiruridae)
  # (K:Animalia, P:Platyhelminthes, C:Cestoda, O:Cyclophyllidea, F:Anoplocephalidae)
  
  'Taxa_subclass', # Acaria 
  # (Kingdom: Animalia, Phylum: Arthropoda, Class: Arachnida)
  
  'Taxa_genus', # Moniliformis
  # (K:Animalia, P:Acanthocephala, C:Archiacanthocephala, O:Moniliformida,
  # F:Moniliformidae)
  
  NA, # not available
  
  NA, # negative,
  
  'Taxa_phylum', # Nematode (Nematoda)
  # (K:Animalia)
  
  'Taxa_genus', #Oochoristica
  # (K:Animalia, P:Platyhelminthes, C:Cestoda, Order:Cyclophylidea, F:Listowiidae)
  
  NA, # positive
  
  rep('Taxa_genus', 5), 
  # Physalopter, Pterygodermatites, Raillietina, Schizorchodes, Syphacia
  # (K:Animalia, P:Nematoda, C:Secernentea, O:Spirurida, F:Physalopteridae)
  # (K:Animalia, P:Nematoda, C:Secernentea, O:Spirurida, F:Rictulariidae)
  # (K:Animalia, P:Platyhelminthes, C:Cestoda, O:Cyclophyllidae, F:Davaineidae)
  # (K:Animalia, P:Platyhelminthes, C:Cestoda, O:Cyclophyllidae, F:Anoplocephalidae)
  # (K:Animalia, P:Nematoda, C:Secernentea, O:Oxyurida, F:Oxyuridae)

  'Taxa_subclass', # Acaria 
  # (Kingdom: Animalia, Phylum: Arthropoda, Class: Arachnida)
  
  rep('Taxa_genus', 2), # Trichuris*2
  # (K:Animalia, P:Nematoda, C:Adenophorea, O:Trichurida, F:Trichuridae)
  
  'Taxa_class', #trematode (Trematoda)
  # (K:Animalia, P:Platyhelminthes)
  
  NA # unsporulated
)
length(genus_unchanged)

genus_unchanged[
  which(trimws(genus_unchanged) == 'acanthocephala')] <-'Acanthocephala'

genus_unchanged[
  which(trimws(genus_unchanged) == 'trematode')] <-'Trematoda'

genus_unchanged[
  which(trimws(genus_unchanged) == 'Nematode')] <-'Nematoda'


# Creating species vector from our imported species list 
species <- as.character(spplist$spp)

# Creating the taxa table that will be filled out
taxa_headers <- c(
  'Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_subclass',
  'Taxa_order', 'Taxa_suborder', 'Taxa_family', 'Taxa_genus', 'Taxa_species')
taxa_table <- data.frame(
  matrix(NA, length(genus_unchanged), length(taxa_headers)))
colnames(taxa_table) <- taxa_headers
taxa_table$Taxa_species <- species
# Filling our table 
for (i in 1:length(genus_unchanged)){
  if(!is.na(true_taxa[i])){
    taxa_table[
      i, grep(true_taxa[i], taxa_headers)] <- genus_unchanged[i]  
  }
}


# Creating a table designating which levels of classification we know
higher_taxa_list <- list(
  'Taxa_kingdom', # acanthocephala (Acanthocephala)
  # (Kingdom:Animalia)
  
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'), # Adelina
  # (Kingdom:Chromalveolata, Phylum:Apicomplexa, Class:Conoidasida, 
  # Order:Eucoccidiorida, Family:Eimeriidae)
  
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'), 
  # Catenotaenia
  #(K:Animalia, P:Platyhelminthes, C:Catenotaeniidae, O:Cyclophyllidea, 
  # F:Catenotaeniidae)
  
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'), 
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  # Cuterebra*3 
  # (Animalia, Phylum:Arthropoda, Class:Insecta, Order:Diptera, Family:Oestridae)
  
  c('Taxa_kingdom', 'Taxa_phylum'), # cestode
  # (Kingdom:Animalia, Phylum:Platyhelminthes)
  
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  # Eimeria*27
  # (K:NA, P:Apicomplexa, C:Conoidasida, O:Eucoccidiorida, F:Eimeriidae) 
  
  
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class'), # Siphonaptera
  # (Animalia, Arthropoda, Insecta)
  
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  # Heteromyoxyuris, Hymenolepis, Isospora*2
  # (K:Animalia, P:Nematoda, C:Secernentea, O:Ascaridida, F:Oxyuridae)
  # (K:Animalia, P:Platyhelminthes, C:Cestoda, O:Cyclophylidea, F:Hymenolepididae)
  
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order'), 
  # Mallophaga; Anoplura 
  # (Animalia, Phylum:Arthropoda, Class: Insect, Order:Phthriaptera);
  # (Animalia, Phylum:Arthropoda, Class: Insect, Order:Polotitas)
  
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'), 
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  # Mastophrus, Mathovetaenia
  # (K:Animalia, P:Nematoda, C:Secernentea, O:Spirurida, F:Spiruridae)
  # (K:Animalia, P:Platyhelminthes, C:Cestoda, O:Cyclophyllidea, F:Anoplocephalidae)
  
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class'), # Acaria 
  # (Kingdom: Animalia, Phylum: Arthropoda, Class: Arachnida)
  
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'), 
  # Moniliformis
  # (K:Animalia, P:Acanthocephala, C:Archiacanthocephala, O:Moniliformida,
  # F:Moniliformidae)
  
  NA, # not available
  
  c('Taxa_kingdom', 'Taxa_phylum'), # negative,
  
  c('Taxa_kingdom'), 
  # Nematode (Nematoda)
  # (K:Animalia)
  
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'), 
  #Oochoristica
  # (K:Animalia, P:Platyhelminthes, C:Cestoda, Order:Cyclophylidea, F:Listowiidae)
  
  c('Taxa_kingdom', 'Taxa_phylum'), # positive
  
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  # Physalopter, Pterygodermatites, Raillietina, Schizorchodes, Syphacia
  # (K:Animalia, P:Nematoda, C:Secernentea, O:Spirurida, F:Physalopteridae)
  # (K:Animalia, P:Nematoda, C:Secernentea, O:Spirurida, F:Rictulariidae)
  # (K:Animalia, P:Platyhelminthes, C:Cestoda, O:Cyclophyllidae, F:Davaineidae)
  # (K:Animalia, P:Platyhelminthes, C:Cestoda, O:Cyclophyllidae, F:Anoplocephalidae)
  # (K:Animalia, P:Nematoda, C:Secernentea, O:Oxyurida, F:Oxyuridae)
  
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class'), # Acaria 
  # (Kingdom: Animalia, Phylum: Arthropoda, Class: Arachnida)
  
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'), 
  c('Taxa_kingdom', 'Taxa_phylum', 'Taxa_class', 'Taxa_order', 'Taxa_family'),
  # Trichuris*2
  # (K:Animalia, P:Nematoda, C:Adenophorea, O:Trichurida, F:Trichuridae)
  
  c('Taxa_kingdom', 'Taxa_phylum'), #trematode (Trematoda)
  # (K:Animalia, P:Platyhelminthes)
  
  NA # unsporulated
)
length(higher_taxa_list)

# Generating a table corresponding to the one above but with
# classifactions filled in
higher_taxa_names <- list(
  'Animalia', # acanthocephala (Acanthocephala)
  # (Kingdom:Animalia)
  
  c('Chromalveolata', 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'), # Adelina
  # (Kingdom:Chromalveolata, Phylum:Apicomplexa, Class:Conoidasida, 
  # Order:Eucoccidiorida, Family:Eimeriidae)
  
  c('Animalia', 'Platyhelminthes', 'Catenotaeniidae', 'Cyclophyllidea', 'Catenotaeniidae'), 
  # Catenotaenia
  #(K:Animalia, P:Platyhelminthes, C:Catenotaeniidae, O:Cyclophyllidea, 
  # F:Catenotaeniidae)
  
  c('Animalia', 'Arthropoda', 'Insecta', 'Diptera', 'Oestridae'),
  c('Animalia', 'Arthropoda', 'Insecta', 'Diptera', 'Oestridae'),
  c('Animalia', 'Arthropoda', 'Insecta', 'Diptera', 'Oestridae'),
  # Cuterebra*3 
  # (Animalia, Phylum:Arthropoda, Class:Insecta, Order:Diptera, Family:Oestridae)
  
  c('Animalia', 'Platyhelminthes'), # cestode
  # (Kingdom:Animalia, Phylum:Platyhelminthes)

  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Eimeriidae'),
  # Eimeria*27
  # (K:NA, P:Apicomplexa, C:Conoidasida, O:Eucoccidiorida, F:Eimeriidae) 
  
  
  c('Animalia', 'Arthropoda', 'Insecta'), # Siphonaptera
  # (Animalia, Arthropoda, Insecta)
  
  c('Animalia', 'Nematoda', 'Secernentea', 'Ascaridida', 'Oxyuridae'),
  c('Animalia', 'Platyhelminthes', 'Cestoda', 'Cyclophylidea', 'Hymenolepididae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Elimeriidae'),
  c(NA, 'Apicomplexa', 'Conoidasida', 'Eucoccidiorida', 'Elimeriidae'),
  # Heteromyoxyuris, Hymenolepis, Isospora*2
  # (K:Animalia, P:Nematoda, C:Secernentea, O:Ascaridida, F:Oxyuridae)
  # (K:Animalia, P:Platyhelminthes, C:Cestoda, O:Cyclophylidea, F:Hymenolepididae)
  # (K:NA, P:Apicomplexa, C:Conoidasida, O:Eucoccidiorida, F:Elimeriidae)
  
  c('Animalia', 'Arthropoda', 'Insect', 'Phthriaptera; Polotitas'), # Mallophaga; Anoplura 
  # (Animalia, Phylum:Arthropoda, Class: Insect, Order:Phthriaptera);
  # (Animalia, Phylum:Arthropoda, Class: Insect, Order:Polotitas)
  
  c('Animalia', 'Nematoda', 'Secernentea', 'Spirurida', 'Spiruridae'), 
  c('Animalia', 'Platyhelminthes', 'Cestoda', 'Cyclophyllidea', 'Anoplocephalidae'),
  # Mastophrus, Mathovetaenia
  # (K:Animalia, P:Nematoda, C:Secernentea, O:Spirurida, F:Spiruridae)
  # (K:Animalia, P:Platyhelminthes, C:Cestoda, O:Cyclophyllidea, F:Anoplocephalidae)
  
  c('Animalia', 'Arthropoda', 'Arachnida'), # Acaria 
  # (Kingdom: Animalia, Phylum: Arthropoda, Class: Arachnida)
  
  c('Animalia', 'Acanthocephala', 'Archiacanthocephala', 'Moniliformida', 'Moniliformidae'), 
  # Moniliformis
  # (K:Animalia, P:Acanthocephala, C:Archiacanthocephala, O:Moniliformida,
  # F:Moniliformidae)
  
  NA, # not available
  
  c('Animalia', 'Platyhelminthes (eggs negative)'), # negative,
  
  c('Animalia'), 
  # Nematode (Nematoda)
  # (K:Animalia)
  
  c('Animalia', 'Platyhelminthes', 'Cestoda', 'Cyclophylidea', 'Listowiidae'), 
  #Oochoristica
  # (K:Animalia, P:Platyhelminthes, C:Cestoda, Order:Cyclophylidea, F:Listowiidae)
  
  c('Animalia', 'Platyhelminthes (eggs positive)'), # positive
  
  c('Animalia', 'Nematoda', 'Secernentea', 'Spirurida', 'Physalopteridae'),
  c('Animalia', 'Nematoda', 'Secernentea', 'Spirurida', 'Rictulariidae'),
  c('Animalia', 'Platyhelminthes', 'Cestoda', 'Cyclophyllidae', 'Davaineidae'),
  c('Animalia', 'Platyhelminthes', 'Cestoda', 'Cyclophyllidae', 'Anoplocephalidae'),
  c('Animalia', 'Nematoda', 'Secernentea', 'Oxyurida', 'Oxyuridae'),
  # Physalopter, Pterygodermatites, Raillietina, Schizorchodes, Syphacia
  # (K:Animalia, P:Nematoda, C:Secernentea, O:Spirurida, F:Physalopteridae)
  # (K:Animalia, P:Nematoda, C:Secernentea, O:Spirurida, F:Rictulariidae)
  # (K:Animalia, P:Platyhelminthes, C:Cestoda, O:Cyclophyllidae, F:Davaineidae)
  # (K:Animalia, P:Platyhelminthes, C:Cestoda, O:Cyclophyllidae, F:Anoplocephalidae)
  # (K:Animalia, P:Nematoda, C:Secernentea, O:Oxyurida, F:Oxyuridae)
  
  c('Animalia', 'Arthropoda', 'Arachnida'), # Acaria 
  # (Kingdom: Animalia, Phylum: Arthropoda, Class: Arachnida)
  
  c('Animalia', 'Nematoda', 'Adenophorea', 'Trichurida', 'Trichuridae'),
  c('Animalia', 'Nematoda', 'Adenophorea', 'Trichurida', 'Trichuridae'),
  # Trichuris*2
  # (K:Animalia, P:Nematoda, C:Adenophorea, O:Trichurida, F:Trichuridae)
  
  c('Animalia', 'Platyhelminthes'), #trematode (Trematoda)
  # (K:Animalia, P:Platyhelminthes)
  
  'unsporulated' # unsporulated
)
length(higher_taxa_names)

# Adding headers to 
for (i in taxa_headers){
  data[,i] = NA
}

# populating the taxa table with linnean names
for (j in 1:length(higher_taxa_list)){
  for (i in 1:length(higher_taxa_list[[j]])){
    classification <- higher_taxa_list[[j]][i]
    if(!is.na(classification)){
      taxa_table[j, classification] <-higher_taxa_names[[j]][i]
     
    }   
  }
}

# Populating the dataframe with taxa names
for (i in 1:ncol(taxa_table)){
  for (j in 1:nrow(taxa_table)){
    classification <- colnames(taxa_table)[i]
    if(!is.na(classification)){
      data[which(
        trimws(as.character(data$p_id)) == trimws(as.character(spplist$spp_id))[j]), 
        classification] <- taxa_table[j, classification]   
    }
  }
}

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

