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
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import *
import pandas as pd


lterex = pd.read_csv(('lter_table_test.csv'))
ltertablename = 'lter_table'


# Here we are using the packageage sqlalchemy
# connecting to the lter databse
# by specifying the title of the database
# and the user name we will be working under.
# Note, postgres is the super user and can do
# everything possible (CREATE,INSERT, MANIPULATE, etc.)
engine = create_engine(
    'postgresql+psycopg2://user:pswd@host/LTERV2',
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


# Raw climate station data
climate_raw_table = Table(
    'climate_raw_table', metadata,
    Column('metarecordid_', Integer, primary_key=True),
    Column('title', TEXT),
    Column('stationid', None, ForeignKey(
        'climate_station_table.stationid', ondelete="CASCADE")),
    Column('year', NUMERIC),
    Column('month', NUMERIC),
    Column('day', NUMERIC),
    # Terrestiral environmental variables
    Column('avetempobs', NUMERIC),
    Column('avetempmeasure', VARCHAR(50)),
    Column('mintempobs', NUMERIC),
    Column('mintempmeasure', VARCHAR(50)),
    Column('maxtempobs', NUMERIC),
    Column('maxtempmeasure', VARCHAR(50)),
    Column('aveprecipobs', NUMERIC),
    Column('aveprecipmeasure', VARCHAR(50)),
    Column('minprecipobs', NUMERIC),
    Column('minprecipmeasure', VARCHAR(50)),
    Column('maxprecipobs', NUMERIC),
    Column('maxprecipmeasure', NUMERIC),
    Column('avewindobs', NUMERIC),
    Column('avewindmeasure', VARCHAR(50)),
    Column('minwindobs', NUMERIC),
    Column('minwindmeasure', VARCHAR(50)),
    Column('maxwindobs', NUMERIC),
    Column('maxwindmeasure', NUMERIC),
    Column('avelightobs', NUMERIC),
    Column('avelightmeasure', VARCHAR(50)),
    Column('minlightobs', NUMERIC),
    Column('minlightmeasure', VARCHAR(50)),
    Column('maxlightobs', NUMERIC),
    Column('maxlightmeasure', NUMERIC),
    # Aquatic environmental vairables
    Column('avewatertempobs', NUMERIC),
    Column('avewatertempmeasure', VARCHAR(50)),
    Column('minwatertempobs', NUMERIC),
    Column('minwatertempmeasure', VARCHAR(50)),
    Column('maxwatertempobs', NUMERIC),
    Column('maxwatertempmeasure', VARCHAR(50)),
    Column('avephobs', NUMERIC),
    Column('avephmeasure', VARCHAR(50)),
    Column('minphobs', NUMERIC),
    Column('minphmeasure', VARCHAR(50)),
    Column('maxphobs', NUMERIC),
    Column('maxphmeasure', NUMERIC),
    Column('avecondobs', NUMERIC),
    Column('avecondmeasure', VARCHAR(50)),
    Column('mincondobs', NUMERIC),
    Column('mincondmeasure', VARCHAR(50)),
    Column('maxcondobs', NUMERIC),
    Column('maxcondmeasure', VARCHAR(50)),
    Column('aveturbidityobs', NUMERIC),
    Column('aveturbiditymeasure', VARCHAR(50)),
    Column('minturbidityobs', NUMERIC),
    Column('minturbiditymeasure', VARCHAR(50)),
    Column('maxturbidityobs', NUMERIC),
    Column('maxturbiditymeasure', VARCHAR(50)),
    Column('covariates', TEXT),
    Column('knbid_', VARCHAR(200)),
    Column('metalink_', VARCHAR(200)),
    Column('authors_', VARCHAR(200)),
    Column('authors_contact_', VARCHAR(200)))

# climate_site_table: This is the initial table
# that will contain information
# regarding the LTER sites themselves. Column names
# should be self explanatory.
climate_station_table = Table(
    'climate_station_table', metadata,
    Column('stationid', VARCHAR(200), primary_key=True),
    Column('lterid', None,
           ForeignKey('lter_table.lterid')),
    Column('lat', NUMERIC),
    Column('lng', NUMERIC),
    Column('descript', TEXT))


#lter_table will be the link from climate data to study data
lter_table = Table(
    'lter_table', metadata,
    Column('lterid', VARCHAR(10), primary_key=True),
    Column('lter_name', TEXT),
    Column('currently_funded', VARCHAR(50)),
    Column('pi', VARCHAR(200)),
    Column('pi_contact_email', VARCHAR(200)),
    Column('alt_contact_email', VARCHAR(200)),
    Column('homepage', VARCHAR(200)))


# site_info: Table regarding site information for within each
# individual study. The table will be related to lter_info and
# the 'foreign key'= lterid/'lterid'
# (i.e. no entries are allowed in this table unless the site
# information originates at a given lter_id)
site_table = Table(
    'site_table', metadata,
    Column('siteid', VARCHAR(200), primary_key=True),
    Column('lterid', VARCHAR(10),
           ForeignKey('lter_table.lterid')),
    Column('lat', NUMERIC),
    Column('lng', NUMERIC),
    Column('descript', TEXT))


# main: Table describing the raw data that was collected
# for each individual project
# 'foreign key' ='siteid'
# This is in case there is a project that does not give a specific
# 'siteid' that can be used in the schema and to ensure that
# any site data entered comes from
main_table = Table(
    'main_table', metadata,
    Column('lter_proj_site', Integer, primary_key=True),
    Column('metarecordid', INTEGER),
    Column('title', TEXT),
    # META: This column specifies the type of information
    # about the sampling organisms life stage
    # ie. adult, juvenile, size, etc
    Column('samplingunits', VARCHAR(50)),
    # META: This column specifies the type of data that was
    # collected (i.e. count, biomass, percent cover, etc.)
    Column('samplingprotocol', VARCHAR(50)),
    # META: This column specifies the type of information
    # about the sampling organisms life stage
    # ie. size, age, life-stage 
    Column('structured',  VARCHAR(50)),
    Column('studystartyr', NUMERIC),
    Column('studyendyr', NUMERIC),
    Column('siteid', VARCHAR(200),
           ForeignKey('site_table.siteid')),
    # DERIVED: start year of data collection for
    # a particular site
    Column('sitestartyr', NUMERIC),
    # DERIVED: end year of data collection for
    # a particular site
    Column('siteendyr', NUMERIC),
    # META: This column relates to the frequency of sampling
    # i.e. seasonal, monthly, month:yr, season:yr, daily, etc.
    Column('samplefreq', TEXT),
    # DERIVED: This will be the total observation
    # related to this project. THis includes
    # all temporal and spatial levels and
    # all taxa units
    Column('totalobs', NUMERIC),
    # META: This column list whether the study was observational
    # or experimental (which includes historic experiemental
    # events)
    Column('studytype', VARCHAR(50)),
    # META: This column indicates whether the study contained
    # community level data (i.e. data over multiple
    # taxonomic groups
    Column('community', VARCHAR(50)),
    # DERIVED: calculates the number of unique
    # taxonomic units from raw data
    Column('uniquetaxaunits', NUMERIC),

    # Spatial replicate informatoin
    # META:
    # sp_repX_ext: columns describes the
    # spatial extent sample at that level of spatial
    # replication

    # sp_repX_ext_units: column describes the unit
    # of measurement corresponding to that level of spatial
    # replication

    # sp_repX_label: describes the labeling scheme used
    # by the study

    #Derived:
    # sp_repX_uniquelevels: count of the number of unique
    # levels within that replicate level for a given site;
    # encompassed all time and taxa units.
    
    Column('sp_rep1_ext', NUMERIC),
    Column('sp_rep1_ext_units', VARCHAR(200)),
    Column('sp_rep1_label', VARCHAR(200)),
    Column('sp_rep1_uniquelevels', NUMERIC),
    
    Column('sp_rep2_ext', NUMERIC),
    Column('sp_rep2_ext_units', VARCHAR(200)),
    Column('sp_rep2_label', VARCHAR(200)),
    Column('sp_rep2_uniquelevels', NUMERIC),
    
    Column('sp_rep3_ext', NUMERIC),
    Column('sp_rep3_ext_units', VARCHAR(200)),
    Column('sp_rep3_label', VARCHAR(200)),
    Column('sp_rep3_uniquelevels', NUMERIC),
    
    Column('sp_rep4_ext', NUMERIC),
    Column('sp_rep4_ext_units', VARCHAR(200)),
    Column('sp_rep4_label', VARCHAR(200)),
    Column('sp_rep4_uniquelevels', NUMERIC),
    
    #Columns relating to author, metadata, other sources
    Column('authors', TEXT),
    Column('authors_contact', VARCHAR(200)),
    Column('metalink', VARCHAR(200)),
    Column('knbid', VARCHAR(200)),
    Column('treatment_type', VARCHAR(200)),
    Column('num_treatments', VARCHAR(200)),
    Column('exp_maintainence', VARCHAR(200)),
    Column('trt_label', VARCHAR(200)))

# taxa: Table regarding taxanomic information. Change from
# last time involves the forgein key and the addition of
# a column for species code (in case raw table information, does
# not contain a key for translation).
# 'foreign key' = site_info/'siteid'
taxa_table = Table(
    'taxa_table', metadata,
    Column('taxaid', Integer, primary_key=True),
    Column('lter_proj_site', Integer, ForeignKey(
        'main_table.lter_proj_site', ondelete="CASCADE")),
    Column('sppcode', VARCHAR(100)),
    Column('kingdom', VARCHAR(100)),
    Column('phylum', VARCHAR(100)),
    Column('clss', VARCHAR(100)),
    Column('ordr', VARCHAR(100)),
    Column('family', VARCHAR(100)),
    Column('genus', VARCHAR(100)),
    Column('species', VARCHAR(100)),
    Column('authority', VARCHAR(100)))


# count: Table containing the raw count data that is populating
# the database.
# 'foreign key' = 'siteid', 'lter_proj_site', 'taxaid'
raw_table = Table(
    'raw_table', metadata,
    Column('sampleid', Integer, primary_key=True),
    Column('taxaid', None, ForeignKey(
        'taxa_table.taxaid', ondelete="CASCADE")),
    Column('lter_proj_site', None, ForeignKey(
        'main_table.lter_proj_site', ondelete="CASCADE")),
    Column('year', NUMERIC),
    Column('month', NUMERIC),
    Column('day', NUMERIC),
    Column('spt_rep1', VARCHAR(50)),
    Column('spt_rep2', VARCHAR(50)),
    Column('spt_rep3', VARCHAR(50)),
    Column('spt_rep4', VARCHAR(50)),
    Column('structure', VARCHAR(50)),
    Column('individ', VARCHAR(50)),
    Column('unitobs', NUMERIC),
    Column('covariates', TEXT),
    Column('trt_label', VARCHAR(200)))


# This command takes all the information that was stored in the
# metadata catalog and uses it to populate the database that
# we connected to with our engine (user=postgres, databse=LTER)
metadata.create_all(engine)


lterex.to_sql(
    ltertablename, con=engine, if_exists="append", index=False)
