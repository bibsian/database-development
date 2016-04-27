# Verifying data integrity

setwd(
  paste0('/Users/bibsian/Dropbox/database-development/GUI',
         '/qtdesigner/integratedui_design/')
  )
# Install any required packages that are not currently installed 
#---------------------------------------------------------------
# List required packages
adm.req <-c('RPostgreSQL', 'dplyr')

# Load currently installed, required packages
tmp <- lapply(adm.req, require, character.only = T)

# Find the required packages that still need to be installed
adm.need <- adm.req[!(paste0("package:",adm.req) %in% search())]

# Install required packages that are not currently installed
if(length(adm.need)>0){ install.packages(adm.need,dependencies=T) }

# Now, make sure all packages are loaded
tmp <- lapply(adm.req, require, character.only = T)

tmp
#-----

# Creating driver to database and connecting to LTER
driver <- dbDriver("PostgreSQL")
con <- dbConnect(driver, dbname='LTER',host='localhost',port=5432,
                 user='postgres', password='demography')

# Query to pull current data
query_all<- dbGetQuery(
  con,
  'SELECT "siteID"."siteID", main_data."projID", taxa."taxaID", 
  rawobs."sampleID", title, lat, long, title, sppcode,
  kingdom, phylum, class, "order", family, genus, species,
  year, month, day, spt_rep1, spt_rep2, spt_rep3, spt_rep4,
  structure, "indivID", unitobs, covariate, "knbID", metalink
  FROM "siteID", main_data, taxa, rawobs
  WHERE "siteID"."siteID" = main_data."siteID"
  AND main_data."projID" = taxa."projID"
  AND taxa."taxaID" = rawobs."taxaID";'
)
write.csv(query_all, 'integrity_check_alldata.csv')

# NEED TO FIGURE OUT SUBSET QUERY
query_subset <- dbGetQuery(
  con,
  'SELECT "siteID"."siteID", main_data."projID", taxa."taxaID", 
  rawobs."sampleID", title, lat, long, title, sppcode,
  kingdom, phylum, class, "order", family, genus, species,
  year, month, day, spt_rep1, spt_rep2, spt_rep3, spt_rep4,
  structure, "indivID", unitobs, covariate, "knbID", metalink
  FROM "siteID", main_data, taxa, rawobs
  WHERE "siteID"."siteID" = main_data."siteID"
  AND main_data."projID" = taxa."projID"
  AND taxa."taxaID" = rawobs."taxaID";'
)
write.csv(query_subset, 'integrity_check_subset.csv')


