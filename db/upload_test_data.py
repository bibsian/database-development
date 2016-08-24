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
Session = sessionmaker(bind=engine, autoflush=False)

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


# Reading in raw test datasets to perform necessary merges when
# uploading the test tables to the database
count = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'raw_data_test_1.csv')
density = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'raw_data_test_2.csv')
biomass = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'raw_data_test_3.csv')
percent = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'raw_data_test_4.csv')
individual = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'raw_data_test_5.csv')

# Reading in test study site table to upload to database
# Attempting to upload tables into the databaset
tbl_study_site = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'study_site_table_test.csv')
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

session = Session()
site_in_proj_key_query = select([
    site_in_project_table.__table__.c.site_in_project_key,     
    site_in_project_table.__table__.c.study_site_table_fkey,
    site_in_project_table.__table__.c.project_table_fkey
    ])
site_in_proj_key_statement = session.execute(site_in_proj_key_query)
site_in_proj_key_df = pd.DataFrame(site_in_proj_key_statement.fetchall())
site_in_proj_key_df.columns = site_in_proj_key_statement.keys()

# Reading in test taxa table to upload to databse
# Attempting to upload tables into the databasete
tbl_taxa = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'taxa_table_test.csv')

tbl_taxa_with_site_in_proj_key= pd.merge(
    tbl_taxa, site_in_proj_key_df,
    left_on=['study_site', 'metadata_key'],
    right_on=['study_site_table_fkey', 'project_table_fkey'],
    how='inner')

tbl_taxa_merged = tbl_taxa_with_site_in_proj_key.copy()
tbl_taxa_merged.drop([
    'metadata_key', 'study_site', 'study_site_table_fkey',
    'project_table_fkey'], inplace=True, axis=1)
tbl_taxa_merged.rename(
    columns= {
        'site_in_project_key': 'site_in_project_taxa_key'}, inplace=True)

tbl_taxa_merge.to_sql(
    'taxa_table', conn, if_exists='append', index=False)

# ------------- Merge 2 ---------------- #
# ------------ taxa_table ------ # taxa_table_key
# --------------- to ----------------- #
# ------------ count_table --------- # taxa_count_fkey
# --------- site_in_project_table ---- # site_in_project_count_fkey

# Reading in test observation tables to upload to database
tbl_count = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'count_table_test.csv')
taxa_key_query = select([taxa_table])
taxa_key_statement = session.execute(taxa_key_query)
taxa_key_df = pd.DataFrame(taxa_key_statement.fetchall())
taxa_key_df.columns = taxa_key_statement.keys()
taxa_key_df.replace({None: 'NA'}, inplace=True)

count_subset_taxa_key_df = taxa_key_df[
    taxa_key_df['site_in_project_taxa_key'].isin([1,2,3])]

# Merging taxa_table to site_in_project_key
count_merged_taxakey_siteinprojectkey = pd.merge(
    count_subset_taxa_key_df, site_in_proj_key_df,
    left_on='site_in_project_taxa_key',
    right_on='site_in_project_key', how='inner')

########### STOPPED HERE ##################
count_site_key = taxa_fk_df[
    taxa_fk_df['project_table_fkey'] ==  1]
count_site_key.columns


raw_count_merge = pd.merge(
    tbl_count, count_site_key,
    left_on= ['spatial_replication_level_1'],
    right_on=['study_site_table_fkey'], how='inner')
raw_count_merge.columns

raw_count_taxa_merge = pd.merge(
    raw_count_merge, count_taxa,
    left_on = [
        'site_in_project_key', 'genus', 'species', 'study_site_table_fkey'],
    right_on = [
        'site_in_project_key', 'genus', 'species', ''],
    how='left')

raw_count_taxa_merge.columns
raw_count_taxa_merge[['year', 'month', '

tbl_density = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'density_table_test.csv')
tbl_biomass = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'biomass_table_test.csv')
tbl_percent = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'percent_cover_table_test.csv')
tbl_individual = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test' +
    end + 'individual_table_test.csv')

