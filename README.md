Population Dynamics Database
============================

The goal of this project is to develop an open source database that wil contain raw aggregated information from numerous ecological studies on population dynamics (plants, animals, algae, etc). This database will *not* be up to third normal form standards. This is because we wish to have a centralized data repositary where all temporal and spatial replication within the data is preserved; this will allow for more accurate modeling of population dyanimcs through state-space models.

# Project Components
## Identifying Data Sources
 See current folder
## Database Schema
 Using PostgreSQL 9.4
## Populating the Database
 This repo is mostly focused on code for the
 GUI to populate the database we are creating. I believe we
 might be able to turn this into a tool to help other scientist
 create databases that sythensize various independent data sources 
 ( i.e. any subdiscipline could use this if we make it flexible enough)
## Web Application and/or R package to Access Database
  This may be a web application OR an R package--- to be determined 

#Folder Structure
GUI/*: Anything in this folder/subfolders will have classes related to managing the functionality of the test version of the
GUI. We used this version to construct an alpha version of the database and assess what we needed to change

classestested/*: Anything here will be related to model-viewer class in the GUI

test/*: This folder and subfolders all have to do with python files for created the version 2.0 of the GUI
and database. The approach to creating this version was based on test driven development. You'll
find a number of unit test on classes that perform work in the program.

UMLDiagrams/*: This folder contains '.dia' files (an open source UML diagram creator; cross platform). 
There is a package diagram (showing the layered architecture of the new program) and class diagrams related to classes
in the various layers of the architecture. Note this is mostly current. Still in development/testing mode but
nearing a point where development should start moving a lot faster (I'm learning everything databases, GUIs, software development,
and best practices as we go; any helpful input is welcome.)

data/*: Sample csv file to try testing the GUI with

db/*: Anything here will be related to creating the database design/keys/tables etc.

current/*: Anythin in this folder will be related to datasets we've catalogued an ID'ed.
 
