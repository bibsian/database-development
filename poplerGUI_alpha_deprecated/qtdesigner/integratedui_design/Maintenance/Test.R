# Andrew Bibian
# April 11, 2016
# This script is testing database queries based on what
# is currently uploaded (about 10 SBC sites)
setwd('C:/Users/MillerLab/Desktop/database-quieres')


# Install any required packages that are not currently installed 
#-----------------------------------------
# List required packages
adm.req <-c("ggplot2", "dplyr", "magrittr", "RPostgreSQL", 
            "compare", "lubridate" )

# Load currently installed, required packages
tmp <- lapply(adm.req, require, character.only = T)

# Find the required packages that still need to be installed
adm.need <- adm.req[!(paste0("package:",adm.req) %in% search())]

# Install required packages that are not currently installed
if(length(adm.need)>0){ install.packages(adm.need,dependencies=T) }

# Now, make sure all packages are loaded
tmp <- lapply(adm.req, require, character.only = T)

tmp


# Estiblish connection
#-------------------

# Choose driver
driver <- dbDriver("PostgreSQL") 

# Create connect to local database
con <- dbConnect(
  driver, dbname='LTER', host='localhost', port=5432, 
  user='postgres', password='demography')
#----

# Testing out package (RpostgeSQL) functions
# and simple quieres
#------------------------------------------

# Reference for Table names:
# c('climateobs', 'lter', 'main_data', 'rawobs', 
# 'siteID', 'siteID', 'station_data', 'taxa')

# Check table existence
dbExistsTable(con, c('siteID'))

# Read from lter table
lter <- dbGetQuery(con, 'SELECT * FROM lter')
site <- dbGetQuery(con, 'SELECT * FROM "siteID" ')
main <- dbGetQuery(con, 'SELECT * FROM main_data')
taxa <- dbGetQuery(con, 'SELECT * FROM taxa')
raw <- dbGetQuery(con, 'SELECT * FROM rawobs')
colnames(raw)

tlist <- dbListTables(con)

# Subset database with query across all tables
# Note: last line; only retrieving one dataframe
jointest <- dbGetQuery(
  con,
  'SELECT "lterID", year, month, day, lat, long, title, 
  studytype, species, spt_rep1, spt_rep2, spt_rep3, unitobs
  FROM "siteID", main_data, taxa, rawobs WHERE
  "siteID"."siteID" = main_data."siteID" 
  AND main_data."projID" = taxa."projID"
  AND taxa."taxaID" = rawobs."taxaID"
  AND main_data.metalink = $$http://sbc.lternet.edu/cgi-bin/showDataset.cgi?docid=knb-lter-sbc.19$$;')

# Writing the join to a file
write.csv(jointest, "test.csv")
#-----


# Raw data formating
#------------------------------------------
data <- read.csv("quad_swath_all_years_20140908 (1).csv")
data$DATE[1]

data$DATE <- ymd(data$DATE)
data$DAY <- day(data$DATE)

#----


# Subsetting data
#----------------
datasub <- data[c(
  'YEAR', 'MONTH', 'DAY', 'TAXON_SPECIES', 'SITE', 'TRANSECT', 
  'QUAD', 'COUNT')]
joinsub <- jointest[c(
  'year', 'month','day', 'species', 'spt_rep1', 'spt_rep2',
  'spt_rep3', 'unitobs')]

# View dataframe structure and coercing types from
# SQL query
str(datasub)
str(joinsub)

# joining data
joinsubmod<- joinsub %>% 
  mutate(
    TRANSECT = as.numeric(TRANSECT),
    QUAD = as.numeric(QUAD),
    TAXON_SPECIES = as.factor(TAXON_SPECIES),
    SITE = as.factor(SITE))

str(datasub)
str(joinsubmod)

keys = c(
  "YEAR", "MONTH", "DAY", "TAXON_SPECIES",
  "SITE", "TRANSECT", "QUAD", "COUNT")

datasub$key <- apply(
  datasub[ ,keys], 1,
  paste0, collapse='-')

joinsubmod$key <- apply(
  joinsubmod[, keys], 1,
  paste0, collapse='-'
)

# Merging the raw data with 
# the queried data
#--------------------------

# Ordering each dataframe by year, month, site, transect, species
# raw data
orderindex1 <- with(
  datasub, order(
    YEAR, MONTH, TAXON_SPECIES, SITE, TRANSECT,QUAD, COUNT))

# uploaded data
orderindex2 <- with(
  joinsubmod, order(
    YEAR, MONTH, TAXON_SPECIES, SITE, TRANSECT,QUAD, COUNT))

# looking at missing values
complength<- nrow(datasub) - nrow(joinsubmod)

compdf <- left_join(datasub, joinsubmod, )

nrow(datasub)
nrow(compdf)
nrow(joinsubmod)

# visual inspection
write.csv(compdf, "testcompare.csv")

#-----

# Comparison
#----------
comp <- compare(
  datasub, joinsubmod, allowAll = T, ignoreOrder = T)

comp$result
comp$transform
comp$detailedResult

# End script and close connection
dbDisconnect(con)

