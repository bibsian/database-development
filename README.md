Population Dynamics Database
============================

This project aims to create an open source database that wil contain raw aggregated information from numerous ecological studies on population dynamics (plants, animals, algae, etc). This database will *not* be up to third normal form standards. This is because we wish to have a centralized data repositary where all temporal and spatial replication within the data is preserved; this will allow for more accurate modeling of population dyanimcs through state-space models.

# Identifying Data Sources
 The data sources will come from LTER research station. Individual data entities are given a unique id by us for book keeping purposes. See the 'current' folder for a list of dataset that will be uploaded (sort by our created 'id' number) as of 07/11/16.
 
# Database Overview
The database will have seven tables.
1. raw_climate: Table of orginal (or aggregated) meteorlogical data from individual LTER stations 

2. climate_site: Table of meteorlogical sites wiht a given LTER station

3. lter_table: Table of all LTER stations and site abbreviations (w/ lat & long)

4. site_table: Table of designated sites within a study that gathered data at a LTER station (w/ lat & log if available)

5. main_table: Table of metadata that describes a study (includes temporal information, levels of spatial replication, PI's, contact emails, community data set indicator, etc). See the 'db' folder for a complete overview of fields.

6. taxa_table: Table of unique instances of a record regarding the taxonomy of study organisms

7. raw_table: Table of the orginal observations gathered from the study.

Note, in order to keep all spatial and temporal replication intact the main_table and taxa_table had to have the records on a per research site (with an LTER study) basis. Our R package will deal with this detail when summarizing database informatoin.

# Overview of Methods to Populate the Database
 Raw data gather from LTER research stations were formated and uploaded with a computer program written in python. This program has a graphical user interface (GUI) to enable various personal to upload data in a repeatable, recordable, and standarized way). I believe we might be able to turn this into a tool to help other scientist create databases that sythensize various independent if we make it flexible enough.

# Future goal
We would like to create a website and web application to access the database (this will only be done if we have enough time/manpower)

# Repo Folder Structure

UMLDiagrams/*: This folder contains '.dia' files with python class descriptions(an open source UML diagram creator; cross platform). 
The program architecture is also described within this folder. This has not been updated to reflect the current python classes (as of 7/11/16). Will update when I get a change.

current/*: Anything in this folder will be related to datasets we've catalogued and ID'ed. As well as some summary pdfs/word files (summaries were created for grant purposes).

db/*: All files related to the BETA version of the database (this is the current design that will likely be retained and unmodified)

db_alpha_deprecated/*: All files related to the ALPH version of the database that was created (we are currently using the beta version)

poplerGUI/*: All files are orginized into python packages. This is the source folder that contains all modules that make of the program (these files are copied over and updated from the test folder when neccessary).

poplerGUI_alpha_deprecated/*: All files related to the ALPHA version of the GUI that was created to populate the ALPHA version of the database. We are currently using the BETA version of the GUI (see 'poplerGUI' folder).

test/*: All unit test, python modules, and database scripts that were written for the BETA version of our GUI.
