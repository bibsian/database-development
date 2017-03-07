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
import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/")
    end = "/"

elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development\\")
    end = "\\"

lterex = pd.read_csv(
	rootpath + 'db' + end + 'lter_table_test.csv')
ltertablename = 'lter_table'


# Here we are using the packageage sqlalchemy
# connecting to the lter databse
# by specifying the title of the database
# and the user name we will be working under.
# Note, postgres is the super user and can do
# everything possible (CREATE,INSERT, MANIPULATE, etc.)
#create_engine = create_engine(
#    'postgresql+psycopg2:///',
#    echo=True)
#conn = create_engine.connect()
#conn.execute("commit")
#conn.execute("CREATE DATABASE popler_3")
#conn.close()
#create_engine.dispose()

engine = create_engine(
    'postgresql+psycopg2://postgres:demography@localhost/popler_test',
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
    Column('lat_climate', NUMERIC),
    Column('lng_climate', NUMERIC),
    Column('descript', TEXT))


#lter_table will be the link from climate data to study data
lter_table = Table(
    'lter_table', metadata,
    Column('lterid', VARCHAR(10), primary_key=True),
    Column('lter_name', TEXT),
    Column('lat_lter', NUMERIC),
    Column('lng_lter', NUMERIC),
    Column('currently_funded', VARCHAR(50)),
    Column('current_principle_investigator', VARCHAR(200)),
    Column('current_contact_email', VARCHAR(200)),
    Column('alt_contact_email', VARCHAR(200)),
    Column('homepage', VARCHAR(200)))


# site_info: Table regarding site information for within each
# individual study. The table will be related to lter_info and
# the 'foreign key'= lterid/'lterid'
# (i.e. no entries are allowed in this table unless the site
# information originates at a given lter_id)
study_site_table = Table(
    'study_site_table', metadata,
    Column('study_site_key', VARCHAR(200), primary_key=True),
    Column('lter_table_fkey', VARCHAR(10),
           ForeignKey('lter_table.lterid')),
    Column('lat_study_site', NUMERIC),
    Column('lng_study_site', NUMERIC),
    Column('descript', TEXT))



project_table = Table(
    'project_table', metadata,
    # This column is the unique index that we created
    # in order to keep track of all the datasets that
    # will be uploaded
    Column('proj_metadata_key', INTEGER, primary_key=True),
    Column('lter_project_fkey', VARCHAR(10),
           ForeignKey('lter_table.lterid')),
    Column('title', TEXT),

    # META: This column specifies the type of information
    # about the sampling organisms life stage
    # ie. adult, juvenile, size, etc
    Column('samplingunits', VARCHAR(50)),

    # META: This column specifies the type of data that was
    # collected (i.e. count, biomass, percent cover, etc.)
    Column('datatype', VARCHAR(50)),

    # META: This column specifies the type of information
    # about the sampling organisms life stage
    # ie. size, age, life-stage 
    Column('structured_type_1',  VARCHAR(50)),
    Column('structured_type_1_units',  VARCHAR(50)),
    Column('structured_type_2',  VARCHAR(50)),
    Column('structured_type_2_units',  VARCHAR(50)),
    Column('structured_type_3',  VARCHAR(50)),
    Column('structured_type_3_units',  VARCHAR(50)),
    
    Column('studystartyr', NUMERIC),
    Column('studyendyr', NUMERIC),

    # META: This column relates to the frequency of sampling
    # i.e. seasonal, monthly, month:yr, season:yr, daily, etc.
    Column('samplefreq', TEXT),

    # META: This column list whether the study was observational
    # or experimental (which includes historic experiemental
    # events)
    Column('studytype', VARCHAR(50)),

    # META: This column indicates whether the study contained
    # community level data (i.e. data over multiple
    # taxonomic groups
    Column('community', VARCHAR(50)),

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
    
    Column('spatial_replication_level_1_extent', NUMERIC),
    Column('spatial_replication_level_1_extent_units', VARCHAR(200)),
    Column('spatial_replication_level_1_label', VARCHAR(200)),
    Column('spatial_replication_level_1_number_of_unique_reps', INTEGER),
    
    Column('spatial_replication_level_2_extent', NUMERIC),
    Column('spatial_replication_level_2_extent_units', VARCHAR(200)),
    Column('spatial_replication_level_2_label', VARCHAR(200)),
    Column('spatial_replication_level_2_number_of_unique_reps', INTEGER),
    
    Column('spatial_replication_level_3_extent', NUMERIC),
    Column('spatial_replication_level_3_extent_units', VARCHAR(200)),
    Column('spatial_replication_level_3_label', VARCHAR(200)),
    Column('spatial_replication_level_3_number_of_unique_reps', INTEGER),
    
    Column('spatial_replication_level_4_extent', NUMERIC),
    Column('spatial_replication_level_4_extent_units', VARCHAR(200)),
    Column('spatial_replication_level_4_label', VARCHAR(200)),
    Column('spatial_replication_level_4_number_of_unique_reps', INTEGER),

    Column('spatial_replication_level_5_extent', NUMERIC),
    Column('spatial_replication_level_5_extent_units', VARCHAR(200)),
    Column('spatial_replication_level_5_label', VARCHAR(200)),
    Column('spatial_replication_level_5_number_of_unique_reps', INTEGER),
    
    # Columns regarding treatments
    Column('treatment_type_1', VARCHAR(200)),
    Column('treatment_type_2', VARCHAR(200)),
    Column('treatment_type_3', VARCHAR(200)),
    Column('control_group', VARCHAR(200)),

    Column('derived', VARCHAR(200)),
    
    # Columns relating to author, metadata, other sources
    Column('authors', TEXT),
    Column('authors_contact', VARCHAR(200)),
    Column('metalink', VARCHAR(200)),
    Column('knbid', VARCHAR(200)))



# main: Table describing the raw data that was collected
# for each individual project
# 'foreign key' ='siteid'
# This is in case there is a project that does not give a specific
# 'siteid' that can be used in the schema and to ensure that
# any site data entered comes from
site_in_project_table = Table(
    'site_in_project_table', metadata,
    Column(
        'site_in_project_key',
        Integer, primary_key=True),
    Column('study_site_table_fkey', None,
           ForeignKey(
               'study_site_table.study_site_key')),

    Column('project_table_fkey', None,
           ForeignKey('project_table.proj_metadata_key')),

    # DERIVED: start year of data collection for
    # a particular site
    Column('sitestartyr', NUMERIC),

    # DERIVED: end year of data collection for
    # a particular site
    Column('siteendyr', NUMERIC),

    # DERIVED: This will be the total observation
    # related to this project. THis includes
    # all temporal and spatial levels and
    # all taxa units
    Column('totalobs', NUMERIC),

    # DERIVED: calculates the number of unique
    # taxonomic units from raw data
    Column('uniquetaxaunits', NUMERIC))

# taxa: Table regarding taxanomic information. Change from
# last time involves the forgein key and the addition of
# a column for species code (in case raw table information, does
# not contain a key for translation).
# 'foreign key' = site_info/'siteid'
taxa_table = Table(
    'taxa_table', metadata,
    Column('taxa_table_key', Integer, primary_key=True),
    Column('site_in_project_taxa_key', None, ForeignKey(
        'site_in_project_table.site_in_project_key', ondelete="CASCADE")),
    Column('sppcode', VARCHAR(100)),
    Column('kingdom', VARCHAR(100)),
    Column('subkingdom', VARCHAR(100)),
    Column('infrakingdom', VARCHAR(100)),
    Column('superdivision', VARCHAR(100)),
    Column('division', VARCHAR(100)),
    Column('subdivision', VARCHAR(100)),
    Column('superphylum', VARCHAR(100)),
    Column('phylum', VARCHAR(100)),
    Column('subphylum', VARCHAR(100)),
    Column('clss', VARCHAR(100)),
    Column('subclass', VARCHAR(100)),
    Column('ordr', VARCHAR(100)),
    Column('family', VARCHAR(100)),
    Column('genus', VARCHAR(100)),
    Column('species', VARCHAR(100)),
    Column('common_name', VARCHAR(100)),
    Column('authority', VARCHAR(100)))

taxa_accepted_table = Table(
    'taxa_accepted_table', metadata,
    Column('taxa_accepted_table_key', Integer, primary_key=True),
    Column('taxa_original_fkey', None, ForeignKey(
        'taxa_table.taxa_table_key', ondelete="CASCADE")),
    Column('sppcode', VARCHAR(100)),
    Column('kingdom_accepted', VARCHAR(100)),
    Column('subkingdom_accepted', VARCHAR(100)),
    Column('infrakingdom_accepted', VARCHAR(100)),
    Column('superdivision_accepted', VARCHAR(100)),
    Column('division_accepted', VARCHAR(100)),
    Column('superphylum_accepted', VARCHAR(100)),
    Column('phylum_accepted', VARCHAR(100)),
    Column('subphylum_accepted', VARCHAR(100)),
    Column('subdivision_accepted', VARCHAR(100)),
    Column('clss_accepted', VARCHAR(100)),
    Column('subclass_accepted', VARCHAR(100)),
    Column('ordr_accepted', VARCHAR(100)),
    Column('family_accepted', VARCHAR(100)),
    Column('genus_accepted', VARCHAR(100)),
    Column('species_accepted', VARCHAR(100)),
    Column('common_name_accepted', VARCHAR(100)),
    Column('authority', VARCHAR(100)))



# Count table
count_table = Table(
    'count_table', metadata,
    Column('count_table_key', Integer, primary_key=True),
    Column('taxa_count_fkey', None, ForeignKey(
        'taxa_table.taxa_table_key', ondelete="CASCADE")),
    Column('site_in_project_count_fkey', None, ForeignKey(
        'site_in_project_table.site_in_project_key', ondelete="CASCADE")),
    Column('year', NUMERIC),
    Column('month', NUMERIC),
    Column('day', NUMERIC),
    Column('spatial_replication_level_1', VARCHAR(50)),
    Column('spatial_replication_level_2', VARCHAR(50)),
    Column('spatial_replication_level_3', VARCHAR(50)),
    Column('spatial_replication_level_4', VARCHAR(50)),
    Column('spatial_replication_level_5', VARCHAR(50)),
    Column('treatment_type_1', VARCHAR(200)),
    Column('treatment_type_2', VARCHAR(200)),
    Column('treatment_type_3', VARCHAR(200)),
    Column('structure_type_1', VARCHAR(200)),
    Column('structure_type_2', VARCHAR(200)),
    Column('structure_type_3', VARCHAR(200)),
    Column('count_observation', NUMERIC),
    Column('covariates', TEXT))

# Biomass Table
biomass_table = Table(
    'biomass_table', metadata,
    Column('biomass_table_key', Integer, primary_key=True),
    Column('taxa_biomass_fkey', None, ForeignKey(
        'taxa_table.taxa_table_key', ondelete="CASCADE")),
    Column('site_in_project_biomass_fkey', None, ForeignKey(
        'site_in_project_table.site_in_project_key', ondelete="CASCADE")),
    Column('year', NUMERIC),
    Column('month', NUMERIC),
    Column('day', NUMERIC),
    Column('spatial_replication_level_1', VARCHAR(50)),
    Column('spatial_replication_level_2', VARCHAR(50)),
    Column('spatial_replication_level_3', VARCHAR(50)),
    Column('spatial_replication_level_4', VARCHAR(50)),
    Column('spatial_replication_level_5', VARCHAR(50)),
    Column('treatment_type_1', VARCHAR(200)),
    Column('treatment_type_2', VARCHAR(200)),
    Column('treatment_type_3', VARCHAR(200)),
    Column('structure_type_1', VARCHAR(200)),
    Column('structure_type_2', VARCHAR(200)),
    Column('structure_type_3', VARCHAR(200)),
    Column('biomass_observation', NUMERIC),
    Column('covariates', TEXT))

# Density Table
density_table = Table(
    'density_table', metadata,
    Column('density_table_key', Integer, primary_key=True),
    Column('taxa_density_fkey', None, ForeignKey(
        'taxa_table.taxa_table_key', ondelete="CASCADE")),
    Column('site_in_project_density_fkey', None, ForeignKey(
        'site_in_project_table.site_in_project_key', ondelete="CASCADE")),
    Column('year', NUMERIC),
    Column('month', NUMERIC),
    Column('day', NUMERIC),
    Column('spatial_replication_level_1', VARCHAR(50)),
    Column('spatial_replication_level_2', VARCHAR(50)),
    Column('spatial_replication_level_3', VARCHAR(50)),
    Column('spatial_replication_level_4', VARCHAR(50)),
    Column('spatial_replication_level_5', VARCHAR(50)),
    Column('treatment_type_1', VARCHAR(200)),
    Column('treatment_type_2', VARCHAR(200)),
    Column('treatment_type_3', VARCHAR(200)),
    Column('structure_type_1', VARCHAR(200)),
    Column('structure_type_2', VARCHAR(200)),
    Column('structure_type_3', VARCHAR(200)),
    Column('density_observation', NUMERIC),
    Column('covariates', TEXT))

# Percent Cover Table
percent_cover_table = Table(
    'percent_cover_table', metadata,
    Column('percent_cover_table_key', Integer, primary_key=True),
    Column('taxa_percent_cover_fkey', None, ForeignKey(
        'taxa_table.taxa_table_key', ondelete="CASCADE")),
    Column('site_in_project_percent_cover_fkey', None, ForeignKey(
        'site_in_project_table.site_in_project_key', ondelete="CASCADE")),
    Column('year', NUMERIC),
    Column('month', NUMERIC),
    Column('day', NUMERIC),
    Column('spatial_replication_level_1', VARCHAR(50)),
    Column('spatial_replication_level_2', VARCHAR(50)),
    Column('spatial_replication_level_3', VARCHAR(50)),
    Column('spatial_replication_level_4', VARCHAR(50)),
    Column('spatial_replication_level_5', VARCHAR(50)),
    Column('treatment_type_1', VARCHAR(200)),
    Column('treatment_type_2', VARCHAR(200)),
    Column('treatment_type_3', VARCHAR(200)),
    Column('structure_type_1', VARCHAR(200)),
    Column('structure_type_2', VARCHAR(200)),
    Column('structure_type_3', VARCHAR(200)),
    Column('percent_cover_observation', NUMERIC),
    Column('covariates', TEXT))


# Percent Cover Table
individual_table = Table(
    'individual_table', metadata,
    Column('individual_table_key', Integer, primary_key=True),
    Column('taxa_individual_fkey', None, ForeignKey(
        'taxa_table.taxa_table_key', ondelete="CASCADE")),
    Column('site_in_project_individual_fkey', None, ForeignKey(
        'site_in_project_table.site_in_project_key', ondelete="CASCADE")),
    Column('year', NUMERIC),
    Column('month', NUMERIC),
    Column('day', NUMERIC),
    Column('spatial_replication_level_1', VARCHAR(50)),
    Column('spatial_replication_level_2', VARCHAR(50)),
    Column('spatial_replication_level_3', VARCHAR(50)),
    Column('spatial_replication_level_4', VARCHAR(50)),
    Column('spatial_replication_level_5', VARCHAR(50)),
    Column('treatment_type_1', VARCHAR(200)),
    Column('treatment_type_2', VARCHAR(200)),
    Column('treatment_type_3', VARCHAR(200)),
    Column('structure_type_1', VARCHAR(200)),
    Column('structure_type_2', VARCHAR(200)),
    Column('structure_type_3', VARCHAR(200)),
    Column('individual_observation', NUMERIC),
    Column('covariates', TEXT))


# This command takes all the information that was stored in the
# metadata catalog and uses it to populate the database that
# we connected to with our engine (user=postgres, databse=LTER)
metadata.create_all(engine)


lterex.to_sql(
    ltertablename, con=engine, if_exists="append", index=False)
