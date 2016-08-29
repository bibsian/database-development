#! /usr/bin/env python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.orm import sessionmaker, load_only
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

engine = create_engine(
    'postgresql+psycopg2:///',
    echo=True)
metadata = MetaData(bind=engine)
base = declarative_base()
conn = engine.connect()

# creating classes for tables to query things
class lter_table(base):
    __table__ = Table('lter_table', metadata, autoload=True)
class study_site_table(base):
    __table__ = Table('study_site_table', metadata, autoload=True)
class project_table(base):
    __table__ = Table('project_table', metadata, autoload=True)
class site_in_project_table(base):
    __table__ = Table('site_in_project_table', metadata, autoload=True)
class taxa_table(base):
    __table__ = Table('taxa_table', metadata, autoload=True)
class biomass_table(base):
    __table__ = Table('biomass_table', metadata, autoload=True)
class count_table(base):
    __table__ = Table('count_table', metadata, autoload=True)
class density_table(base):
    __table__ = Table('density_table', metadata, autoload=True)
class percent_cover_table(base):
    __table__ = Table('percent_cover_table', metadata, autoload=True)
class individual_table(base):
    __table__ = Table('individual_table', metadata, autoload=True)

statement = (
    select([count_table]).
    select_from(
        count_table.__table__.join(taxa_table).
        join(
            alias(
                select([site_in_project_table]).

                select_from(
                    site_in_project_table.__table__.
                    join(project_table)
                )
            ))
    )
)

select_results = conn.execute(statement)
select_df = pd.DataFrame(select_results.fetchall())
select_df.columns = select_results.keys()
print(select_df)
print(select_df.columns)
    
# Helper Functions to coerce datatypes as necessary
# And replace likely values that indicate null (i.e. -99999)
def find_types(tbl, name):
    ''' Method to get data types from Tbls'''
    dictname = (name + "types")
    dictname = {}
    for i,item in enumerate(tbl.__table__.c):
        name = (str(item).split('.')[1])
        dictname[name] = str(
            tbl.__table__.c[name].type)
    return dictname


taxa_table_types = find_types(taxa_table, 'taxa')
count_table_types = find_types(count_table, 'count')
density_table_types = find_types(density_table, 'density')
biomass_table_types = find_types(biomass_table, 'biomass')
individual_table_types = find_types(individual_table, 'individual')
percent_cover_table_types = find_types(percent_cover_table, 'cover')


def convert_types(dataframe, types):
    ''' Method to convert data types in dataframe to match Orm'''
    for i in dataframe.columns:
        if types[i] in ['FLOAT', 'Float']:
            dataframe.loc[:, i] = pd.to_numeric(dataframe[i], errors='coerce')
        if types[i] in ['INTEGER', 'Integer']:
            dataframe.loc[:, i] = dataframe[i].astype(int)
        if types[i] in ['VARCHAR', 'TEXT']:
            try:
                dataframe.loc[:, i] = dataframe[i].astype(str)
            except:
                print('string conversion did not work')
            finally:
                dataframe.loc[:, i] = dataframe[i].astype(object)
        if i in ['year', 'month', 'day']:
            dataframe.loc[:, i] = pd.to_numeric(dataframe[i], errors='coerce')
            dataframe[i].fillna('NaN', inplace=True)

def replace_numeric_null_with_string(dataframe):
    ''' Function to take values such as -99999 and convert them 
    to NA's '''
    for i in dataframe.columns:
        try:
            dataframe[i].replace(
                {
                    '-999999': 'NA',
                    '-99999': 'NA',
                    '-9999': 'NA',
                    '-999': 'NA',
                    '-888': 'NA',
                    '-8888': 'NA',
                    '-88888': 'NA',
                    '-888888': 'NA'
                }, inplace=True)
        except:
            print(i + ' did not convert')


# Reading in raw test datasets to perform necessary merges when
# uploading the test tables to the database
count = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'raw_data_test_1.csv')
replace_numeric_null_with_string(count)
density = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'raw_data_test_2.csv')
replace_numeric_null_with_string(density)
biomass = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'raw_data_test_3.csv')
replace_numeric_null_with_string(biomass)
percent = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'raw_data_test_4.csv')
replace_numeric_null_with_string(percent)
individual = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'raw_data_test_5.csv')
replace_numeric_null_with_string(individual)

# Reading in test study site table to upload to database
# Attempting to upload tables into the databaset
tbl_study_site = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'study_site_table_test.csv')
tbl_study_site.fillna('NA')
tbl_study_site.to_sql(
    'study_site_table', conn, if_exists='append', index=False)

# Reading in test project table to upload to database
# Attempting to upload tables into the databaset
tbl_project = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'project_table_test.csv')
tbl_project.to_sql(
    'project_table', conn, if_exists='append', index=False)

# Reading in test site in project table to upload to database
# Attempting to upload tables into the databasete
tbl_site_in_proj = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'site_in_project_table_test.csv')
tbl_site_in_proj.to_sql(
    'site_in_project_table', conn, if_exists='append', index=False)

# ------------- Merge 1 ---------------- #
# --------- site_in_project_table ------ # site_in_project_key
# -----------------to------------------- #
# --------------taxa_table --------- # site_in_project_taxa_key

# Step 1) Bring in the formatted taxa table that does not
# have the foreign keys appended to it yet
tbl_taxa = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'taxa_table_test.csv')

# Using th MergedataToUpload class to push formated taxa table
# appended with all foeign keys

uploading = MergedataToUpload(sessionmaker(bind=engine, autoflush=False))
uploading.merge_for_taxa_table_upload(tbl_taxa)


# ------------- Merge 2 ---------------- #
# ------------ taxa_table ------ # taxa_table_key
# --------------- to ----------------- #
# ------------ count_table --------- # taxa_count_fkey
# --------- site_in_project_table ---- # site_in_project_count_fkey

# Using MergedataToUpload class to push
tbl_count = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'count_table_test.csv')

uploading.merge_for_datatype_table_upload(
    raw_dataframe=count, formated_dataframe=tbl_count,
    formated_dataframe_name='count',
    raw_data_taxa_columns=['site', 'genus', 'species'],
    uploaded_taxa_columns=['study_site_table_fkey', 'genus', 'species']
)

# ------------- Merge 3 ---------------- #
# ------------ taxa_table ------ # taxa_table_key
# --------------- to ----------------- #
# ------------ density_table --------- # taxa_count_fkey
# --------- site_in_project_table ---- # site_in_project_count_fkey
# Using the site_in_proj table query from above #

tbl_density = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'density_table_test.csv')
tbl_density.fillna('NA', inplace=True)

uploading.merge_for_datatype_table_upload(
    raw_dataframe=density, formated_dataframe=tbl_density,
    formated_dataframe_name='density',
    raw_data_taxa_columns=[
        'SITE', 'TAXON_KINGDOM', 'TAXON_PHYLUM', 'TAXON_CLASS',
        'TAXON_ORDER', 'TAXON_FAMILY', 'TAXON_GENUS', 'TAXON_SPECIES'],
    uploaded_taxa_columns= [
        'study_site_table_fkey', 'kingdom', 'phylum', 'clss',
        'ordr', 'family', 'genus', 'species']
)

# ------------- Merge 4 ---------------- #
# ------------ taxa_table ------ # taxa_table_key
# --------------- to ----------------- #
# ------------ biomass_table --------- # taxa_count_fkey
# --------- site_in_project_table ---- # site_in_project_count_fkey
# Using the site_in_proj table query from above #

tbl_biomass = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'biomass_table_test.csv')

uploading.merge_for_datatype_table_upload(
    raw_dataframe=biomass, formated_dataframe=tbl_biomass,
    formated_dataframe_name='biomass',
    raw_data_taxa_columns=[
        'site', 'phylum', 'clss',
        'ordr', 'family', 'genus', 'species'],
    uploaded_taxa_columns= [
        'study_site_table_fkey', 'phylum', 'clss',
        'ordr', 'family', 'genus', 'species']
)

# ------------- Merge 5 ---------------- #
# ------------ taxa_table ------ # taxa_table_key
# --------------- to ----------------- #
# ------------ percent_table --------- # taxa_count_fkey
# --------- site_in_project_table ---- # site_in_project_count_fkey
# Using the site_in_proj table query from above #

tbl_percent = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'percent_cover_table_test.csv')

uploading.merge_for_datatype_table_upload(
    raw_dataframe=percent, formated_dataframe=tbl_percent,
    formated_dataframe_name='percent_cover',
    raw_data_taxa_columns=[
        'site', 'code'],
    uploaded_taxa_columns= [
        'study_site_table_fkey', 'sppcode']
)

# ------------- Merge 6 ---------------- #
# ------------ taxa_table ------ # taxa_table_key
# --------------- to ----------------- #
# ------------ individual_table --------- # taxa_count_fkey
# --------- site_in_project_table ---- # site_in_project_count_fkey
# Using the site_in_proj table query from above #


tbl_individual = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'individual_table_test.csv')

uploading.merge_for_datatype_table_upload(
    raw_dataframe=individual, formated_dataframe=tbl_individual,
    formated_dataframe_name='individual',
    raw_data_taxa_columns=[
        'SITE', 'TAXON_GENUS', 'TAXON_SPECIES'],
    uploaded_taxa_columns= [
        'study_site_table_fkey', 'genus', 'species']
)

