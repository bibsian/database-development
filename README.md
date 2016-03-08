Population Dynamics Database
============================

The goal of this project is to develop an open source database that wil contain raw aggregated information from numerous ecological studies on population dynamics (plants, animals, algae, etc). This database will *not* be up to third normal form standards. This is because we wish to have a centralized data repositary where all temporal and spatial replication within the data is preserved; this will allow for more accurate modeling of population dyanimcs through state-space models.

# Project Components
## Identifying Data Sources
 This won't be public until end of project
## Database Schema
 Using PostgreSQL 9.4
## Populating the Database
 This entire project is centered around creating this
 GUI to populate the database we are creating. I believe we
 might be able to turn this into a tool to help other scientist
 create databases that sythensize various sources of informatoin
 ( i.e. any subdiscipline could use this if we make it flexible enough)
## Web Application to Access Database
  This may be a web application OR an R package--- to be determined 

#Folder Structure
GUI/*: Anything in this folder/subfolders will have classes related to managing the functionality of the GUI

classestested/*: Anything here will be related to model-viewer controller class in the GUI

data/*: Sample csv file to try testing the GUI with

db/*: Anything here will be related to creating the database design/keys/tables etc.
 
