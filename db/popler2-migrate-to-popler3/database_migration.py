#!/usr/bin/env python
from collections import OrderedDict
from sqlalchemy.sql import *
import datetime as dt
import pandas as pd
import sys,os
import re
import config_v3 as ormv3
import config_v2 as ormv2
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/")
    end = "/"
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development\\")
    end = "\\"
os.chdir(rootpath)

#startTime = dt.datetime.now()

# Excel file with all migration information (names, etc)
migration_changes = pd.read_csv(
    rootpath + 'db' + end + 'popler2-migrate-to-popler3'+
    end + 'migration_changes.csv'
)
# --------------------------------------- #
# ---- site_table to study_site_table ----#
# --------------------------------------- #

# Select all records from old site_table
site_table_statement = ormv2.conn.execute(
    select([ormv2.Sitetable.__table__]))
site_table_data = pd.DataFrame(site_table_statement.fetchall())
site_table_data.columns = site_table_statement.keys()


# Take proposed name changes data and make
# to a dictionary for chaning column names
study_site_table_name_changes = migration_changes[
    migration_changes['table_to'] == 'study_site_table'][
        ['column_from', 'column_to']]
study_site_table_dict_name_changes = dict(
    zip(
        study_site_table_name_changes['column_from'],
        study_site_table_name_changes['column_to']
    ))

# Copy records to new site table and change column names
study_site_table = site_table_data.copy()
study_site_table.rename(
    columns=study_site_table_dict_name_changes, inplace=True)

# Write old site_table records to new study_site_table
study_site_table.to_sql(
    'study_site_table', con=ormv3.engine,
    if_exists='append', index=False
)


# --------------------------------------- #
# ---- main_table to project_table ----#
# --------------------------------------- #
# Making list of columns that will go from the main
# table to the project_table
main_table_col_to_migrate_to_project_table = migration_changes[
    migration_changes['table_to'] == 'project_table'][
        'column_from'].values.tolist()
main_table_col_to_migrate_to_project_table.append('studytype')
main_table_col_to_migrate_to_project_table.append('studystartyr')
main_table_col_to_migrate_to_project_table.append('studyendyr')

# Modifying the list to contain sqlalchemy column objects
main_table_col_to_migrate_to_project_table_sqlobj = [
    column(x) for x in main_table_col_to_migrate_to_project_table
]

# Take proposed name changes data and make
# to a dictionary for chaning column names
project_table_name_changes = migration_changes[
    migration_changes['table_to'] == 'project_table'][
        ['column_from', 'column_to']]
project_table_dict_name_changes = dict(
    zip(
        project_table_name_changes['column_from'],
        project_table_name_changes['column_to']
    ))

# Statement to retrieve columns and make into dataframe
# and dropping duplicate records and push distinct data
# to the project table
main_table_statement = ormv2.conn.execute(
    select(from_obj = table('main_table'),
        columns=main_table_col_to_migrate_to_project_table_sqlobj
    ).
    order_by(ormv2.Maintable.metarecordid)
)
main_table_data = pd.DataFrame(
    main_table_statement.fetchall()
)

#print(main_table_data)
main_table_data.columns = main_table_statement.keys()
main_table_data_distinct = main_table_data.drop_duplicates(
    subset='metarecordid'
)


# join main_table to sites to get LTER id
main_fkey_join = study_site_table[['study_site_key', 'lter_table_fkey']]

main_table_data_merged = pd.merge(
    main_table_data_distinct, main_fkey_join, how='left',
    left_on = 'siteid', right_on='study_site_key')

main_table_data_merged.drop(['siteid', 'study_site_key'], axis=1, inplace=True)

main_table_data_merged.rename(
    columns=project_table_dict_name_changes, inplace=True)
main_table_data_merged.rename(
    columns={'lter_table_fkey': 'lter_project_fkey'}, inplace=True)



main_table_data_merged[['structured_type_1', 'structured_type_2']] = main_table_data_merged[
    'structured_type_1'].str.split(';', expand=True).fillna('NA')
main_table_data_merged['structured_type_1_units'] = main_table_data_merged[
    'structured_type_1'].str.extract('\((.*)\)').fillna('NA')
main_table_data_merged['structured_type_1'] = main_table_data_merged[
    'structured_type_1'].str.replace('\s\(.*\)', '')

new_project_table_columns = [
    'structured_type_2_units',
    'structured_type_3', 'structured_type_3_units',
    'spatial_replication_level_5_extent',
    'spatial_replication_level_5_extent_units',
    'spatial_replication_level_5_label',
    'spatial_replication_level_5_number_of_unique_reps',
    'treatment_type_2', 'treatment_type_3'
]

for i,value in enumerate(new_project_table_columns):
    if re.search('_extent$', value) is not None or 'reps' in value:
        main_table_data_merged[value] = -99999
    else:
        main_table_data_merged[value] = 'NA'

# Correcting labels for datatypes
main_table_data_merged['datatype'] = main_table_data_merged[
    'datatype'].map(lambda x: 'individual' if 'mark' in x else x)
main_table_data_merged['datatype'] = main_table_data_merged[
    'datatype'].map(lambda x: 'count' if 'dist' in x else x)
main_table_data_merged['datatype'] = main_table_data_merged[
    'datatype'].map(lambda x: 'percent_cover' if 'per_cover' in x else x)

main_table_data_merged.to_sql(
    'project_table',
    con=ormv3.engine, if_exists='append', index=False
)

# --------------------------------------- #
# ---- main_table to site_in_project_table ----#
# --------------------------------------- #
# Making list of columns that will go from the main
# table to the site_in_proj_table
main_table_col_to_migrate_to_site_in_project_table = migration_changes[
    migration_changes['table_to'] == 'site_in_project_table'][
        'column_from'].values.tolist()
# Modifying the list to contain sqlalchemy column objects
main_table_col_to_migrate_to_site_in_project_table_sqlobj = [
    column(x) for x in main_table_col_to_migrate_to_site_in_project_table
]

# Take proposed name changes data and make
# to a dictionary for chaning column names
site_in_project_table_name_changes = migration_changes[
    migration_changes['table_to'] == 'site_in_project_table'][
        ['column_from', 'column_to']]
site_in_project_table_dict_name_changes = dict(
    zip(
        site_in_project_table_name_changes['column_from'],
        site_in_project_table_name_changes['column_to']
    ))

# Statement to retrieve columns and make into dataframe,
# chane columns, and push to database (site_in_project_table)
main_table_statement = ormv2.conn.execute(
    select(from_obj = table('main_table'),
        columns=main_table_col_to_migrate_to_site_in_project_table_sqlobj
    ).
    order_by(ormv2.Maintable.lter_proj_site)
)
main_table_data = pd.DataFrame(
    main_table_statement.fetchall()
)
main_table_data.columns = main_table_statement.keys()

project_table_data = main_table_data.rename(
    columns=site_in_project_table_dict_name_changes
).copy()

project_table_data.to_sql(
    'site_in_project_table', con=ormv3.engine,
    if_exists='append', index=False
)

# --------------------------------------- #
# ---- taxa_table to taxa_table ----#
# --------------------------------------- #
# Select all records from old taxa_table
taxa_table_statement = ormv2.conn.execute(
    select([ormv2.Taxatable.__table__]).
    order_by('taxaid')
)
taxa_table_data = pd.DataFrame(taxa_table_statement.fetchall())
taxa_table_data.columns = taxa_table_statement.keys()


# Take proposed name changes data and make
# to a dictionary for chaning column names
taxa_table_name_changes = migration_changes[
    migration_changes['table_to'] == 'taxa_table'][
        ['column_from', 'column_to']]
taxa_table_dict_name_changes = dict(
    zip(
        taxa_table_name_changes['column_from'],
        taxa_table_name_changes['column_to']
    ))
taxa_table_db_columns = [
    column(x) for x in
    taxa_table_name_changes['column_to'].values.tolist()
]

# Copy records to new taxa table and change column names
taxa_table = taxa_table_data.copy()
taxa_table.rename(
    columns=taxa_table_dict_name_changes, inplace=True)

# Write old taxa_table records to new taxa_table
taxa_table.to_sql(
    'taxa_table', con=ormv3.engine,
    if_exists='append', index=False
)

# --------------------------------------- #
# ---- raw_table to count_table ----#
# --------------------------------------- #

# --------------------------------------------
# ----- creating COUNT table filter list -----
main_table_filer_statement = ormv2.conn.execute(
    select(
        from_obj=table(
            ormv2.Maintable.__tablename__),
        columns=[
            column('lter_proj_site'),
            column('samplingprotocol')
        ])
)
main_table_datatype_filter_data = pd.DataFrame(
    main_table_filer_statement.fetchall()
)
main_table_datatype_filter_data.columns = (
    main_table_filer_statement.keys())
main_table_datatype_filter_data['samplingprotocol'] = main_table_datatype_filter_data[
    'samplingprotocol'].map(lambda x: 'individual' if 'mark' in x else x)
main_table_datatype_filter_data['samplingprotocol'] = main_table_datatype_filter_data[
    'samplingprotocol'].map(lambda x: 'count' if 'dist' in x else x)
main_table_datatype_filter_data['samplingprotocol'] = main_table_datatype_filter_data[
    'samplingprotocol'].map(lambda x: 'percent_cover' if 'per_cover' in x else x)


#print(main_table_filter_count_data)
count_filter = main_table_datatype_filter_data[
    main_table_datatype_filter_data['samplingprotocol'] == 'count'][
        'lter_proj_site'].values.tolist()

# ---------------------------------
# ----- querying COUNT table  -----
count_table_statement = ormv2.conn.execute(
    select([ormv2.Rawtable.__table__]).
    where(column('lter_proj_site').in_(count_filter)).
    order_by('sampleid')
)
count_table_data = pd.DataFrame(count_table_statement.fetchall())
count_table_data.columns = count_table_statement.keys()
count_table_data.drop('individ', axis=1, inplace=True)

# Take proposed name changes data and make
# to a dictionary for chaning column names

count_table_name_changes = migration_changes[
    migration_changes['table_to'] == 'count_table'][
        ['column_from', 'column_to']]
count_table_dict_name_changes = dict(
    zip(
        count_table_name_changes['column_from'],
        count_table_name_changes['column_to']
    ))
count_table_db_columns = [
    column(x) for x in
    count_table_name_changes['column_to'].values.tolist()
]

# Copy records to new taxa table and change column names
count_table = count_table_data.copy()
#print(count_table)
count_table.rename(
    columns=count_table_dict_name_changes, inplace=True)

# Write old count_table records to new count_table
count_table.to_sql(
    'count_table', con=ormv3.engine,
    if_exists='append', index=False
)


# --------------------------------------- #
# ---- raw_table to biomass_table ----#
# --------------------------------------- #
# --------------------------------------------
# ----- creating BIOMASS table filter list -----
biomass_filter = main_table_datatype_filter_data[
    main_table_datatype_filter_data['samplingprotocol'] == 'biomass'][
        'lter_proj_site'].values.tolist()

# ---------------------------------
# ----- querying BIOMASS table  -----
biomass_table_statement = ormv2.conn.execute(
    select([ormv2.Rawtable.__table__]).
    where(column('lter_proj_site').in_(biomass_filter)).
    order_by('sampleid')
)
biomass_table_data = pd.DataFrame(biomass_table_statement.fetchall())
biomass_table_data.columns = biomass_table_statement.keys()
biomass_table_data.drop('individ', axis=1, inplace=True)

# Take proposed name changes data and make
# to a dictionary for chaning column names
biomass_table_name_changes = migration_changes[
    migration_changes['table_to'] == 'biomass_table'][
        ['column_from', 'column_to']]
biomass_table_dict_name_changes = dict(
    zip(
        biomass_table_name_changes['column_from'],
        biomass_table_name_changes['column_to']
    ))
biomass_table_db_columns = [
    column(x) for x in
    biomass_table_name_changes['column_to'].values.tolist()
]

# Copy records to new taxa table and change column names
biomass_table = biomass_table_data.copy()
#print(biomass_table)
biomass_table.rename(
    columns=biomass_table_dict_name_changes, inplace=True)

# Write old biomass_table records to new biomass_table
biomass_table.to_sql(
    'biomass_table', con=ormv3.engine,
    if_exists='append', index=False
)



# --------------------------------------- #
# ---- raw_table to density_table ----#
# --------------------------------------- #
# --------------------------------------------
# ----- creating DENSITY table filter list -----
density_filter = main_table_datatype_filter_data[
    main_table_datatype_filter_data['samplingprotocol'] == 'density'][
        'lter_proj_site'].values.tolist()

# ---------------------------------
# ----- querying DENSITY table  -----
density_table_statement = ormv2.conn.execute(
    select([ormv2.Rawtable.__table__]).
    where(column('lter_proj_site').in_(density_filter)).
    order_by('sampleid')
)
density_table_data = pd.DataFrame(density_table_statement.fetchall())
density_table_data.columns = density_table_statement.keys()
density_table_data.drop('individ', axis=1, inplace=True)

# Take proposed name changes data and make
# to a dictionary for chaning column names
density_table_name_changes = migration_changes[
    migration_changes['table_to'] == 'density_table'][
        ['column_from', 'column_to']]
density_table_dict_name_changes = dict(
    zip(
        density_table_name_changes['column_from'],
        density_table_name_changes['column_to']
    ))
density_table_db_columns = [
    column(x) for x in
    density_table_name_changes['column_to'].values.tolist()
]

# Copy records to new taxa table and change column names
density_table = density_table_data.copy()
#print(density_table)
density_table.rename(
    columns=density_table_dict_name_changes, inplace=True)

# Write old density_table records to new density_table
density_table.to_sql(
    'density_table', con=ormv3.engine,
    if_exists='append', index=False
)


# --------------------------------------- #
# ---- raw_table to perecent_cover_table ----#
# --------------------------------------- #
# --------------------------------------------
# ----- creating PERCENT_COVER table filter list -----
percent_cover_filter = main_table_datatype_filter_data[
    main_table_datatype_filter_data['samplingprotocol'] == 'percent_cover'][
        'lter_proj_site'].values.tolist()

# ---------------------------------
# ----- querying PERCENT_COVER table  -----
percent_cover_table_statement = ormv2.conn.execute(
    select([ormv2.Rawtable.__table__]).
    where(column('lter_proj_site').in_(percent_cover_filter)).
    order_by('sampleid')
)
percent_cover_table_data = pd.DataFrame(percent_cover_table_statement.fetchall())
percent_cover_table_data.columns = percent_cover_table_statement.keys()
percent_cover_table_data.drop('individ', axis=1, inplace=True)

# Take proposed name changes data and make
# to a dictionary for chaning column names
percent_cover_table_name_changes = migration_changes[
    migration_changes['table_to'] == 'percent_cover_table'][
        ['column_from', 'column_to']]
percent_cover_table_dict_name_changes = dict(
    zip(
        percent_cover_table_name_changes['column_from'],
        percent_cover_table_name_changes['column_to']
    ))
percent_cover_table_db_columns = [
    column(x) for x in
    percent_cover_table_name_changes['column_to'].values.tolist()
]

# Copy records to new taxa table and change column names
percent_cover_table = percent_cover_table_data.copy()
#print(percent_cover_table)
percent_cover_table.rename(
    columns=percent_cover_table_dict_name_changes, inplace=True)

# Write old percent_cover_table records to new percent_cover_table
percent_cover_table.to_sql(
    'percent_cover_table', con=ormv3.engine,
    if_exists='append', index=False
)


# --------------------------------------- #
# ---- raw_table to perecent_cover_table ----#
# --------------------------------------- #
# --------------------------------------------
# ----- creating INDIVIDUAL table filter list -----
individual_filter = main_table_datatype_filter_data[
    main_table_datatype_filter_data['samplingprotocol'] == 'individual'][
        'lter_proj_site'].values.tolist()

# ---------------------------------
# ----- querying INDIVIDUAL table  -----
individual_table_statement = ormv2.conn.execute(
    select([ormv2.Rawtable.__table__]).
    where(column('lter_proj_site').in_(individual_filter)).
    order_by('sampleid')
)
individual_table_data = pd.DataFrame(individual_table_statement.fetchall())
individual_table_data.columns = individual_table_statement.keys()
individual_table_data.drop('individ', axis=1, inplace=True)

# Take proposed name changes data and make
# to a dictionary for chaning column names
individual_table_name_changes = migration_changes[
    migration_changes['table_to'] == 'individual_table'][
        ['column_from', 'column_to']]
individual_table_dict_name_changes = dict(
    zip(
        individual_table_name_changes['column_from'],
        individual_table_name_changes['column_to']
    ))
individual_table_db_columns = [
    column(x) for x in
    individual_table_name_changes['column_to'].values.tolist()
]

# Copy records to new taxa table and change column names
individual_table = individual_table_data.copy()
#print(individual_table)
individual_table.rename(
    columns=individual_table_dict_name_changes, inplace=True)

# Write old individual_table records to new individual_table
individual_table.to_sql(
    'individual_table', con=ormv3.engine,
    if_exists='append', index=False
)


#endTime = dt.datetime.now() - startTime
#print(endTime)


