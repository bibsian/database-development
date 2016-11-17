from sqlalchemy import create_engine, MetaData, Table, column
from sqlalchemy.sql import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pandas import DataFrame, read_csv
import sys
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/")
    end = "/"
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development")
    end = "\\"

# -----------------------------------
# Setting up connections to databases
# ----------------------------------

# ---------------
# Popler Version 2 tables & connection

engine_popler_2 = create_engine(
    'postgresql+psycopg2://postgres:demography@localhost/popler',
    echo=False)
conn_popler_2 = engine_popler_2.connect()
# Mapping metadata
metadata_popler_2 = MetaData(bind=engine_popler_2)
# Creating base
Base_popler_2 = declarative_base()


class Ltertable(Base_popler_2):
    __table__ = Table('lter_table', metadata_popler_2, autoload=True)


class Sitetable(Base_popler_2):
    __table__ = Table('site_table', metadata_popler_2, autoload=True)


class Maintable(Base_popler_2):
    __table__ = Table('main_table', metadata_popler_2, autoload=True)
    taxa = relationship(
        'Taxatable', cascade="delete, delete-orphan")
    raw = relationship('Rawtable', cascade="delete, delete-orphan")


class Taxatable(Base_popler_2):
    __table__ = Table('taxa_table', metadata_popler_2, autoload=True)


class Rawtable(Base_popler_2):
    __table__ = Table('raw_table', metadata_popler_2, autoload=True)



# ---------------
# Popler Version 3 tables & collections

engine_popler_3 = create_engine(
    'postgresql+psycopg2://postgres:demography@localhost/popler_3',
    echo=False)
conn_popler_3 = engine_popler_3.connect()
# Mapping metadata
metadata_popler_3 = MetaData(bind=engine_popler_3)
# Creating base
Base_popler_3 = declarative_base()


class lter_table(Base_popler_3):
    __table__ = Table('lter_table', metadata_popler_3, autoload=True)


class study_site_table(Base_popler_3):
    __table__ = Table('study_site_table', metadata_popler_3, autoload=True)


class project_table(Base_popler_3):
    __table__ = Table('project_table', metadata_popler_3, autoload=True)
    taxa = relationship(
        'taxa_table', cascade="delete, delete-orphan")
    count = relationship(
        'count_table', cascade="delete, delete-orphan")
    density = relationship(
        'density_table', cascade="delete, delete-orphan")
    biomass = relationship(
        'biomass_table', cascade="delete, delete-orphan")
    percent_cover = relationship(
        'percent_cover_table', cascade="delete, delete-orphan")
    individual = relationship(
        'individual_table', cascade="delete, delete-orphan")


class site_in_project_table(Base_popler_3):
    __table__ = Table('site_in_project_table', metadata_popler_3, autoload=True)


class taxa_table(Base_popler_3):
    __table__ = Table('taxa_table', metadata_popler_3, autoload=True)


class taxa_accepted_table(Base_popler_3):
    __table__ = Table('taxa_accepted_table', metadata_popler_3, autoload=True)


class count_table(Base_popler_3):
    __table__ = Table('count_table', metadata_popler_3, autoload=True)


class biomass_table(Base_popler_3):
    __table__ = Table('biomass_table', metadata_popler_3, autoload=True)


class density_table(Base_popler_3):
    __table__ = Table('density_table', metadata_popler_3, autoload=True)


class percent_cover_table(Base_popler_3):
    __table__ = Table('percent_cover_table', metadata_popler_3, autoload=True)


class individual_table(Base_popler_3):
    __table__ = Table('individual_table', metadata_popler_3, autoload=True)

# ---------------------------------------------------------------
# Data with all name changes that will take place during the migration
migration_changes_df = read_csv(
    rootpath + end + 'db' + end + 'popler2-migrate-to-popler3' + end +
    'migration_changes.csv'
)


# ------------------------------------------------------
# Function A: Returns a list of colnames to subset where
# selecting data from the database


def select_subset_of_columns_to_upload(tablename):
    subset = migration_changes_df[
        migration_changes_df['table_to'] == tablename][
            'column_from'].values.tolist()

    sql_column_list = [
        column(x) for x in subset
    ]
    return sql_column_list


# ------------------------------------------------------
# Function 1: Makes necessary name changes base on table


def change_column_names_and_upload(
        tablename, dataframe, dropdupes=False):
    # Get name changes based on table
    subset = migration_changes_df[
        migration_changes_df['table_to'] == tablename][
            ['column_from', 'column_to']]

    # Make a dictionary of the name changes to take place
    dictionary_of_changes = dict(
        zip(
            subset['column_from'],
            subset['column_to']
        )
    )
    # Copy df and drop duplicates (if applicable) else rename
    # columns and upload to postgres
    df_copy = dataframe.copy()
    if dropdupes is True:
        df_copy.drop_duplicates(subset='metarecordid', inplace=True)
    else:
        pass
    df_copy.rename(columns=dictionary_of_changes, inplace=True)

    df_copy.to_sql(
        tablename, con=conn_popler_3, if_exists='append', index=False)


# ---------------------------------------------------
# Function 2: Extracts records based on string match for
# a specific datatype: Used to get lter_proj_site keys


def datatype_records_to_subset_and_migrate(likechars):
    stmt_for_pkeys = conn_popler_2.execute(
        select(
            from_obj=Maintable,
            columns=[
                column('lter_proj_site'),
                column('samplingprotocol')
            ]).
        where(
            column('samplingprotocol').like(
                '%{}%'.format(likechars))
        )
    )
    data = DataFrame(stmt_for_pkeys.fetchall())
    data.columns = stmt_for_pkeys.keys()

    records_to_get = data['lter_proj_site'].values.tolist()

    stmt_for_records = conn_popler_2.execute(
        select(
            from_table=Rawtable,
        ).
        where(column('lter_proj_site').in_(records_to_get)).
        order_by('sampleid')
    )
    data2 = DataFrame(stmt_for_records.fetchall())
    data2.columns = stmt_for_records.keys()
    data2.drop('individ', axis=1, inplace=True)
    
    ##### run through name change and upload ####




# ------------------------------------------------------
# Step 1: Migrate Sitetable records to study_site_table
site_table_stmt = conn_popler_2.execute(
    select([Sitetable])
)
site_table = DataFrame(site_table_stmt.fetchall())
site_table.columns = site_table_stmt.keys()
# Upload to postgres
change_column_names_and_upload(
    tablename='study_site_table', dataframe=site_table, dropdupes=False)

# ------------------------------------------------------
# Step 2: Migrate Maintable records (subset) to project_table
project_table_stmt = conn_popler_2.execute(
    select([Maintable])
)
project_table = DataFrame(project_table_stmt.fetchall())
project_table.columns = project_table_stmt.keys()
# Subset of columns
project_col_subset = [
    'metarecordid', 'title', 'samplingprotocol', 'structured',
    'studystartyr', 'studyendyr', 'samplefreq', 'studytype',
    'community',
    'sp_rep1_ext', 'sp_rep1_ext_units',
    'sp_rep1_label', 'sp_rep1_uniquelevels',
    'sp_rep2_ext', 'sp_rep2_ext_units',
    'sp_rep2_label', 'sp_rep2_uniquelevels',
    'sp_rep3_ext', 'sp_rep3_ext_units',
    'sp_rep3_label', 'sp_rep3_uniquelevels',
    'sp_rep4_ext', 'sp_rep4_ext_units',
    'sp_rep4_label', 'sp_rep4_uniquelevels',
    'treatment_type', 'derived', 'authors', 'authors_contact',
    'metalink', 'knbid'
]

project_table_to_upload = project_table[project_col_subset].drop_duplicates(
    subset='metarecordid').copy()


change_column_names_and_upload(
    tablename='project_table', dataframe=project_table_to_upload, dropdupes=False)

# ------------------------------------------------------
# Step 3: Migrate Maintable records (subset) to site_in_project_table




# Step 4: Extract lter_proj_site keys for fetching and uploading
# data to the correct datatype table
count_df_with_ind = select_datatype_records('cou')
count_df = count_df[
    ~count_df['samplingprotocol'].str.contains('mark')
]
change_column_names_and_upload(
    tablename='count_table', dataframe=count_df, dropdupes=True)

biomass_df = select_datatype_records('bio')
change_column_names_and_upload('biomass_table', biomass_df, True)

density_df = select_datatype_records('dens')
change_column_names_and_upload('density_table', density_df, True)

cover_df = select_datatype_records('cov')
change_column_names_and_upload('percent_cover_table', cover_df, True)

individual_df = count_df[
    count_df['samplingprotocol'].str.contains('mark')
]
change_column_names_and_upload('individual_table', individual_df, True)
