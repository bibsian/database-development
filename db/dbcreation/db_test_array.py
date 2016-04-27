# This script is going to create the skelton of our LTER
# database and begin to populate it with raw data
# Note this is the newer version of the schema
# that was based on the meeting that tool place on
# December 21, 2015 with Aldo, Tom, and myself
# In addition rather than using psycopg2 as a module
# to populate the database, we are strictly using
# sqlalchemy with a psycog
# interpreter as our module for talking to postgresql
# THIS ASSUMES YOU HAVE THE DATABASE ALREADY CREATED
# IN POSTGRESQL
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import *
import pandas as pd
import sys

from sys import platform as _platform
if _platform == "darwin":
    sys.path.insert(
        0, "/Users/bibsian/Dropbox/database-development/data/")
    path = "/Users/bibsian/Dropbox/database-development/data/"
elif _platform == "win32":
    sys.path.insert(
        0, 'C:\\Users\\MillerLab\\Dropbox\\database-development\\data\\')
    path = 'C:\\Users\\MillerLab\\Dropbox\\database-development\\data\\'


lterex = pd.read_csv((path+'lter_table_test.csv'))
ltertablename = 'lter'
mainex = pd.read_csv((path+'main_table_test.csv'))
maintablename = 'main_data'
siteex = pd.read_csv((path+'siteID_table_test.csv'))
sitetablename = 'siteID'


# Here we are using the packageage sqlalchemy
# connecting to the lter databse
# by specifying the title of the database
# and the user name we will be working under.
# Note, postgres is the super user and can do
# everything possible (CREATE,INSERT, MANIPULATE, etc.)
engine = create_engine(
    'postgresql+psycopg2://postgres:demography@localhost/ArrayTest',
    echo=True)

# Note that the relationships in the database (i.e. entity-relation
#-ship diagram or  ED diagram) can be visualized after all the tables
# have been created. So, the first step to setting up the skeleton
# of out LTER database
# is going to be to create all tables, and attributes within each,
# and then use our open source database software manager (DBeaver)
# to visualize the layout

########################
# Table creation
#########################

# Now we're going to begin to create the tables and
# specify  their attributes/attribute classes

# The first step of this process is to create a database
# metadata catalog. With the object title 'metadata', we
# can create all the tables, their columns, primary, and foreign
# keys from the 'Table' command and use the 'metadata' object
# to compile all the information. Then it can be written
# to the postegresql database with a special method called
# 'create_all'
metadata = MetaData()



# count: Table containing the raw count data that is populating
# the database.
# 'foreign key' = 'siteID', 'projID', 'taxaID'
rawobs = Table('rawobs', metadata,
               Column('sampleID', Integer, primary_key=True),
               Column('unitobs', NUMERIC),
               Column('covariate', TEXT))

# This command takes all the information that was stored in the
# metadata catalog and uses it to populate the database that
# we connected to with our engine (user=postgres, databse=LTER)
metadata.create_all(engine)

