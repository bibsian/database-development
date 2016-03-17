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
    'postgresql+psycopg2://postgres:demography@localhost/LTER',
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

# lter_info: This is the initial table that will contain information
# regarding the LTER sites themselves. Column names
# should be self explanatory.
lter = Table(ltertablename, metadata,
             Column('lterID', VARCHAR(5), primary_key=True),
             Column('lter_name', TEXT),
             Column('currently_funded', TEXT),
             Column('lat', NUMERIC),
             Column('long', NUMERIC))

# site_info: Table regarding site information for within each
# individual study. The table will be related to lter_info and
# the 'foreign key'= lterID/'lterID'
# (i.e. no entries are allowed in this table unless the site
# information originates at a given lter_id)
site_info = Table(sitetablename, metadata,
                  Column('siteID', VARCHAR(10), primary_key=True),
                  Column('lterID', None, ForeignKey('lter.lterID')),
                  Column('lat', NUMERIC),
                  Column('long', NUMERIC),
                  Column('descript', TEXT))


# taxa: Table regarding taxanomic information. Change from
# last time involves the forgein key and the addition of
# a column for species code (in case raw table information, does
# not contain a key for translation).
# 'foreign key' = site_info/'siteID'
taxa = Table('taxa', metadata,
             Column('taxaID', Integer, primary_key=True),
             Column('projID', None, ForeignKey('main_data.projID')),
             Column('sppcode', VARCHAR(20)),
             Column('kingdom', VARCHAR(20)),
             Column('phylum', VARCHAR(20)),
             Column('class', VARCHAR(20)),
             Column('order', VARCHAR(20)),
             Column('family', VARCHAR(20)),
             Column('genus', VARCHAR(20)),
             Column('species', VARCHAR(20)),
             Column('authority', VARCHAR(20)))


# main: Table describing the raw data that was collected
# for each individual project
# 'foreign key' ='siteID'
# This is in case there is a project that does not give a specific
# 'siteID' that can be used in the schema and to ensure that
# any site data entered comes from
maindata = Table(maintablename, metadata,
                 Column('projID', Integer, primary_key=True),
                 Column('title', TEXT),
                 # This column specifies the type of information
                 # about the sampling organisms life stage
                 # ie. adult, juvenile, size, etc
                 Column('samplingunits', VARCHAR(20)),
                 # This column specifies the type of data that was
                 # collected (i.e. count, biomass, percent cover, etc.)
                 Column('samplingprotocol', VARCHAR(20)),
                 # This column specifies the type of information
                 # about the sampling organisms life stage
                 # ie. adult, juvenile, size, etc
                 Column('structured',  VARCHAR(20)),
                 Column('startyr', INTEGER),
                 Column('endyr', INTEGER),
                 # This column relates to the frequency of sampling
                 # i.e. seasonal, monthly, month:yr, season:yr, daily, etc.
                 Column('samplefreq', TEXT),
                 # This will be the total observation
                 # related to this project. THis includes
                 # all temporal and spatial levels and
                 # all taxonomc groups
                 Column('totalobs', NUMERIC),
                 # This column list whether the study was observational
                 # or experimental (which includes historic experiemental
                 # events)
                 Column('studytype', VARCHAR(10)),
                 # This column indicates whether the study contained
                 # community level data (i.e. data over multiple
                 # taxonomic groups
                 Column('community', BOOLEAN),
                 # This will be the total observation
                 # related to this project. THis includes
                 # all temporal and spatial levels and
                 # all taxonomc groups
                 Column('totalobs', NUMERIC),
                 # sp_repX_ext columns descript the
                 # spatial extent at that level of spatial
                 # replication
                 Column('siteID', None, ForeignKey('siteID.siteID')),
                 Column('sp_rep1_ext', NUMERIC),
                 Column('sp_rep2_ext', NUMERIC),
                 Column('sp_rep3_ext', NUMERIC),
                 Column('sp_rep4_ext', NUMERIC),
                 Column('metalink', VARCHAR(80)),
                 Column('knbID', VARCHAR(20)))

# count: Table containing the raw count data that is populating
# the database.
# 'foreign key' = 'siteID', 'projID', 'taxaID'
rawobs = Table('rawobs', metadata,
               Column('sampleID', Integer, primary_key=True),
               Column('taxaID', None, ForeignKey('taxa.taxaID')),
               Column('projID', None, ForeignKey('main_data.projID')),
               Column('year', NUMERIC),
               Column('month', NUMERIC),
               Column('day', NUMERIC),
               Column('spt_rep1', VARCHAR(50)),
               Column('spt_rep2', VARCHAR(50)),
               Column('spt_rep3', VARCHAR(50)),
               Column('spt_rep4', VARCHAR(50)),
               Column('structure', VARCHAR(50)),
               Column('indivID', VARCHAR(50)),
               Column('unitobs', NUMERIC),
               Column('covariate', VARCHAR(200)))


# station_info: Table regarding climate station information within
# individual LTERs. The table will be related to lter_info and
# the 'foreign key'= 'lterID'
# (i.e. no entries are allowed in this table unless the site
# information originates at a given lter_id)
station_info = Table('station_data', metadata,
                     Column('stationID', VARCHAR(10), primary_key=True),
                     Column('lterID', None, ForeignKey('lter.lterID')),
                     Column('lat', NUMERIC),
                     Column('long', NUMERIC),
                     Column('descript', TEXT))


# climateobs: Table containing the raw climate  data that is
# populating the database.
# 'foreign key' = 'stationID'
climateobs = Table('climateobs', metadata,
                   Column('climate_obsID', Integer, primary_key=True),
                   Column('stationID', None, ForeignKey(
                       'station_data.stationID')),
                   Column('year', NUMERIC),
                   Column('month', NUMERIC),
                   Column('day', NUMERIC),
                   Column('hour', NUMERIC),
                   Column('unitobs', NUMERIC),
                   Column('unitmeasure', VARCHAR(10)))


# This command takes all the information that was stored in the
# metadata catalog and uses it to populate the database that
# we connected to with our engine (user=postgres, databse=LTER)
metadata.create_all(engine)


lterex.to_sql(ltertablename, con=engine, if_exists="append", index=False)
#
#siteex.to_sql(sitetablename, con=engine, if_exists="append", index=False)
#mainex.to_sql(maintablename, con=engine, if_exists="append", index=False)
