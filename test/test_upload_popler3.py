#! /usr/bin/env python
import pytest
from collections import OrderedDict
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

@pytest.fixture
def engine():
    ''' engine for creating connection and executing statements'''
    engine = create_engine(
        'postgresql+psycopg2:///',
        echo=True)
    return engine

@pytest.fixture
def metadata(engine):
    ''' metadata from database derived with db engine'''
    metadata = MetaData(bind=engine)
    return metadata

@pytest.fixture
def base():
    base = declarative_base()
    return base

@pytest.fixture
def conn(engine):
    '''connection to database'''
    conn = engine.connect()
    return conn

@pytest.fixture
def lter_table(base, metadata):
    class lter_table(base):
        __table__ = Table('lter_table', metadata, autoload=True)
    return lter_table

@pytest.fixture
def study_site_table(base, metadata):
    
    class study_site_table(base):
        __table__ = Table('study_site_table', metadata, autoload=True)
    return study_site_table

@pytest.fixture
def project_table(base, metadata):
    class project_table(base):
        __table__ = Table('project_table', metadata, autoload=True)
    return project_table

@pytest.fixture
def site_in_project_table(base, metadata):
    class site_in_project_table(base):
        __table__ = Table('site_in_project_table', metadata, autoload=True)
    return site_in_project_table

@pytest.fixture
def taxa_table(base, metadata):
    class taxa_table(base):
        __table__ = Table('taxa_table', metadata, autoload=True)

    return taxa_table

@pytest.fixture
def biomass_table(base, metadata):
    class biomass_table(base):
        __table__ = Table('biomass_table', metadata, autoload=True)
    return biomass_table

@pytest.fixture
def count_table(base, metadata):
    class count_table(base):
        __table__ = Table('count_table', metadata, autoload=True)
    return count_table

@pytest.fixture
def density_table(base, metadata):
    class density_table(base):
        __table__ = Table('density_table', metadata, autoload=True)
    return density_table

@pytest.fixture
def percent_cover_table(base, metadata):
    class percent_cover_table(base):
        __table__ = Table('percent_cover_table', metadata, autoload=True)
    return percent_cover_table

@pytest.fixture
def individual_table(base, metadata):
    class individual_table(base):
        __table__ = Table('individual_table', metadata, autoload=True)
    return individual_table

@pytest.fixture
def find_types():
    def find_types(tbl, name):
        ''' Method to get data types from Tbls'''
        dictname = {}
        for i,item in enumerate(tbl.__table__.c):
            name = (str(item).split('.')[1])
            print('col name in table: find_types ', name)
            dictname[name] = str(
                tbl.__table__.c[name].type)
        return dictname
    return find_types


@pytest.fixture
def convert_types():
    def convert_types(dataframe, types):
        ''' 
        Method to convert data types in dataframe to match 
        column types in database
        '''
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
    return convert_types

@pytest.fixture
def replace_numeric_null_with_string():
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
    return replace_numeric_null_with_string


@pytest.fixture
def count(replace_numeric_null_with_string):
    ''' Raw count data '''
    count = pd.read_csv(
        rootpath + 'test' + end + 'Datasets_manual_test' +
        end + 'raw_data_test_1.csv')
    replace_numeric_null_with_string(count)
    return count

@pytest.fixture
def density(replace_numeric_null_with_string):
    ''' Raw density data '''
    density = pd.read_csv(
        rootpath + 'test' + end + 'Datasets_manual_test' +
        end + 'raw_data_test_2.csv')
    replace_numeric_null_with_string(density)
    return density

@pytest.fixture
def biomass(replace_numeric_null_with_string):
    biomass = pd.read_csv(
        rootpath + 'test' + end + 'Datasets_manual_test' +
        end + 'raw_data_test_3.csv')
    replace_numeric_null_with_string(biomass)
    return biomass

@pytest.fixture
def percent(replace_numeric_null_with_string):
    percent = pd.read_csv(
        rootpath + 'test' + end + 'Datasets_manual_test' +
        end + 'raw_data_test_4.csv')
    replace_numeric_null_with_string(percent)
    return percent

@pytest.fixture
def individual(replace_numeric_null_with_string):
    individual = pd.read_csv(
        rootpath + 'test' + end + 'Datasets_manual_test' +
        end + 'raw_data_test_5.csv')
    replace_numeric_null_with_string(individual)
    return individual

@pytest.fixture
def tbl_study_site():
    ''' formated study_site_table '''
    tbl_study_site = pd.read_csv(
        rootpath + 'test' + end + 'Datasets_manual_test' +
        end + 'study_site_table_test.csv')
    tbl_study_site.fillna('NA', inplace=True)
    return tbl_study_site

#
# ----- Not really a test, more just reseting the database
#
def test_drop_records(
        conn, biomass_table, count_table, density_table,
        individual_table, percent_cover_table, taxa_table,
        project_table, site_in_project_table, study_site_table):

    table_dict = OrderedDict([
        ('biomass_table', biomass_table),
        ('count_table', count_table),
        ('density_table', density_table),
        ('individual_table', individual_table),
        ('percent_cover_table', percent_cover_table),
        ('taxa_table', taxa_table),
        ('site_in_project_table', site_in_project_table),
        ('project_table', project_table),
        ('study_site_table', study_site_table)]
    )

    for i, item in enumerate(table_dict):
        print(i)
        print('item', item)
        delete_statement = table_dict[item].__table__.delete()
        conn.execute(delete_statement)
    conn.close()

#
# ----- Test 1: Study site table push ------
#
def test_push_study_site_table(
        tbl_study_site, study_site_table, engine, conn):
    tbl_study_site.to_sql(
        'study_site_table', conn, if_exists='append', index=False)
    conn.close()
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()
    tbl_study_site_query = select([study_site_table])
    study_site_query_stm = session.execute(tbl_study_site_query)
    study_site_query_df = pd.DataFrame(study_site_query_stm.fetchall())
    study_site_query_df.columns = study_site_query_stm.keys()
    session.close()
    engine.dispose()
    assert (
        tbl_study_site['descript'].values.tolist() ==
        study_site_query_df['descript'].values.tolist()) is True

@pytest.fixture
def tbl_project():
    ''' formated project table '''
    tbl_project = pd.read_csv(
        rootpath + 'test' + end + 'Datasets_manual_test' +
        end + 'project_table_test.csv')
    tbl_project.fillna('NA', inplace=True)
    return tbl_project

#
# ------ Test 2: Project table push -------
#
def test_push_project_table(
        tbl_project, project_table, engine, conn):
    tbl_project.to_sql(
        'project_table', conn, if_exists='append', index=False)
    conn.close()
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()
    tbl_project_query = select([project_table])
    project_query_stm = session.execute(tbl_project_query)
    project_query_df = pd.DataFrame(project_query_stm.fetchall())
    project_query_df.columns = project_query_stm.keys()
    session.close()
    engine.dispose()
    assert (
        tbl_project['title'].values.tolist() ==
        project_query_df['title'].values.tolist()) is True

    assert (
        tbl_project['samplefreq'].values.tolist() ==
        project_query_df['samplefreq'].values.tolist()) is True

@pytest.fixture
def tbl_site_in_proj():
    ''' formated site in project table '''
    tbl_site_in_proj = pd.read_csv(
        rootpath + 'test' + end + 'Datasets_manual_test' +
        end + 'site_in_project_table_test.csv')
    tbl_site_in_proj.fillna('NA', inplace=True)
    return tbl_site_in_proj

#
# ------ Test 3: Site in project table push
#
def test_push_site_in_project_table(
        tbl_site_in_proj, site_in_project_table, engine, conn):

    tbl_site_in_proj.to_sql(
        'site_in_project_table', conn, if_exists='append', index=False)
    conn.close()
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()
    tbl_site_in_project_query = select([site_in_project_table])
    site_in_project_query_stm = session.execute(tbl_site_in_project_query)
    site_in_project_query_df = pd.DataFrame(site_in_project_query_stm.fetchall())
    site_in_project_query_df.columns = site_in_project_query_stm.keys()
    session.close()
    engine.dispose()
    assert (
        tbl_site_in_proj['sitestartyr'].values.tolist() ==
        site_in_project_query_df['sitestartyr'].values.tolist()) is True

    assert (
        tbl_site_in_proj['totalobs'].values.tolist() ==
        site_in_project_query_df['totalobs'].values.tolist()) is True

# ------ MERGE/UPLOAD to database class
@pytest.fixture
def MergedataToUpload(
        find_types, conn, taxa_table, count_table, density_table,
        biomass_table, individual_table, percent_cover_table,
        site_in_project_table, replace_numeric_null_with_string,
        convert_types):

    taxa_table_types = find_types(taxa_table, 'taxa')
    density_table_types = find_types(density_table, 'density')
    biomass_table_types = find_types(biomass_table, 'biomass')
    individual_table_types = find_types(individual_table, 'individual')
    percent_cover_table_types = find_types(percent_cover_table, 'cover')
    print(percent_cover_table_types)

    class MergedataToUpload(object):
        print('trying to initiate')
        def __init__(self, sess):
            self.session = sess
            self.table_types = {
                'taxa': taxa_table_types,
                'count': count_table_types,
                'density': density_table_types,
                'biomass': biomass_table_types,
                'individual': individual_table_types,
                'percent_cover': percent_cover_table_types
            }

        @property
        def site_in_proj_key_df(self):
            ''' 
            Method to save the primary key from the 
            site_in_project_table:

            Query the site_in_project_table to retrieve
            the autogenerated primary keys from our previous upload
            of the site_in_project_table ('tbl_site_in_proj')
            '''
            # Step 1) Query taxa_table to get the auto generated
            # primary keys returned. Turn query data into
            # dataframe.
            print('in the site proj block of merge class')
            session = self.session()
            site_in_proj_key_query = select([
                site_in_project_table.__table__.c.site_in_project_key,     
                site_in_project_table.__table__.c.study_site_table_fkey,
                site_in_project_table.__table__.c.project_table_fkey
            ])

            site_in_proj_key_statement = session.execute(
                site_in_proj_key_query)
            session.close()
            site_in_proj_key_df = pd.DataFrame(
                site_in_proj_key_statement.fetchall())
            site_in_proj_key_df.columns = site_in_proj_key_statement.keys()
            return site_in_proj_key_df


        def merge_for_taxa_table_upload(self, formated_taxa_table):

            # Step 2) Merge the formatted taxa_table with the quieried
            # site_in_project_key dataframe (to add foreign keys to
            # the taxa_table)
            replace_numeric_null_with_string(formated_taxa_table)
            tbl_taxa_with_site_in_proj_key= pd.merge(
                formated_taxa_table, self.site_in_proj_key_df,
                left_on=['study_site', 'metadata_key'],
                right_on=['study_site_table_fkey', 'project_table_fkey'],
                how='inner')

            # Step 3) Making a copy of the merged table 
            tbl_taxa_merged = tbl_taxa_with_site_in_proj_key.copy()

            # Step 4) Dropping the unneccessary columns from the copy
            # of the merged taxa_table (that has foreign keys now)
            tbl_taxa_merged.drop([
                'metadata_key', 'study_site', 'study_site_table_fkey',
                'project_table_fkey'], inplace=True, axis=1)

            # Step 5) Renaming the foreign keys to match the column
            # label in the database
            tbl_taxa_merged.rename(
                columns= {
                    'site_in_project_key': 'site_in_project_taxa_key'}, inplace=True)

            # Step 6) Filling Null values (blank or NaN) with 'NA' strings
            # then converting each column into it's appropriate data type
            # for the database
            tbl_taxa_merged.fillna('NA', inplace=True)
            convert_types(tbl_taxa_merged, taxa_table_types)

            # Step 7) Upload table to datbase
            tbl_taxa_merged.to_sql(
                'taxa_table', conn, if_exists='append', index=False)

        def merge_for_datatype_table_upload(
                self, raw_dataframe,
                formated_dataframe,
                formated_dataframe_name,
                raw_data_taxa_columns, uploaded_taxa_columns):

            replace_numeric_null_with_string(raw_dataframe)
            replace_numeric_null_with_string(formated_dataframe)

            # Step 2) Query taxa_table to get the auto generated
            # primary keys returned. Turn query data into
            # dataframe.
            session = self.session()
            taxa_key_query = select([taxa_table])
            taxa_key_statement = session.execute(taxa_key_query)
            session.close()
            taxa_key_df = pd.DataFrame(taxa_key_statement.fetchall())
            taxa_key_df.columns = taxa_key_statement.keys()
            taxa_key_df.replace({None: 'NA'}, inplace=True)

            # Step 3) Subsetting the query tabled for record that only pertain
            # to the count data (because we will be subsetting from this
            # queried taxa table later)
            dtype_subset_taxa_key_df = taxa_key_df[
                taxa_key_df['site_in_project_taxa_key'].isin(
                    self.site_in_proj_key_df['site_in_project_key'])]

            # Step 4) Merge the taxa_table query results with
            # the site_in_project table query that was performed
            # to upload the taxa_table (see above). This gives
            # you a table with site names and taxonomic information
            # allowing for a merge with the original dtype data
            tbl_dtype_merged_taxakey_siteinprojectkey = pd.merge(
                dtype_subset_taxa_key_df, self.site_in_proj_key_df,
                left_on='site_in_project_taxa_key',
                right_on='site_in_project_key', how='inner')

            # Step 5) Merge the original dtype data with the
            # merged taxa_table query to have all foreign keys (taxa and site_project)
            # matched up with the original observations.
            dtype_merged_with_taxa_and_siteinproj_key = pd.merge(
                raw_dataframe, tbl_dtype_merged_taxakey_siteinprojectkey,
                left_on = list(raw_data_taxa_columns),
                right_on = list(uploaded_taxa_columns),
                how='left')

            # Step 6) Take the merged original data with all foreign keys,
            # and merged that with the formatted dtype_table based on index
            # values (order or records should not changed from the original data
            # to the formatted data)
            tbl_dtype_merged_with_all_keys = pd.merge(
                formated_dataframe,
                dtype_merged_with_taxa_and_siteinproj_key,
                left_index=True, right_index=True, how='inner',
                suffixes=('', '_y'))

            # Step 7) List the columns that will be needed to push the
            # dtype table to the database (including foreign keys)
            tbl_dtype_columns_to_upload = [
                'taxa_table_key', 'site_in_project_taxa_key', 'year',
                'month', 'day', 'spatial_replication_level_1',
                'spatial_replication_level_2', 'spatial_replication_level_3',
                'spatial_replication_level_4', 'structure',
                'covariates', 'trt_label'
            ]
            tbl_dtype_columns_to_upload.append(
                '{}_observation'.format(str(formated_dataframe_name)))

            # Step 8) Subsetting the fully merged dtype table data
            tbl_dtype_to_upload = tbl_dtype_merged_with_all_keys[
                tbl_dtype_columns_to_upload]

            # Step 9) Renaming columns to reflect that in database table
            # And converting data types
            tbl_dtype_to_upload.rename(columns={
                'taxa_table_key':
                'taxa_{}_fkey'.format(str(formated_dataframe_name))}, inplace=True)

            datatype_key = 'site_in_project_{}_fkey'.format(str(formated_dataframe_name))
            tbl_dtype_to_upload.rename(columns={
                'site_in_project_taxa_key': datatype_key}, inplace=True)
            tbl_dtype_to_upload.fillna('NA', inplace=True)
            convert_types(
                tbl_dtype_to_upload, self.table_types[str(formated_dataframe_name)])

            datatype_table = '{}_table'.format(str(formated_dataframe_name))
            # Step 10) Uploading to the database
            tbl_dtype_to_upload.to_sql(
                datatype_table,
                conn, if_exists='append', index=False)

    return MergedataToUpload

@pytest.fixture
def tbl_taxa():
    tbl_taxa = pd.read_csv(
        rootpath + 'test' + end + 'Datasets_manual_test' +
        end + 'taxa_table_test.csv')
    return tbl_taxa

#
# ------- Test 4: Merge site in project keys to taxa table and push
#
def test_merge_taxa_data_and_push(
        MergedataToUpload, engine, tbl_taxa, taxa_table):
    ta.fillna('NA', inplace=True)

    uploading = MergedataToUpload(sessionmaker(bind=engine, autoflush=False))
    print('made uploading object')
    uploading.merge_for_taxa_table_upload(tbl_taxa)
    Session = sessionmaker(bind=engine, autoflush=False)
    session = Session()
    tbl_taxa_query = select([taxa_table])
    taxa_query_stm = session.execute(tbl_taxa_query)
    taxa_query_df = pd.DataFrame(taxa_query_stm.fetchall())
    taxa_query_df.columns = taxa_query_stm.keys()
    session.close()
    engine.dispose()

    assert (
        tbl_taxa['kingdom'].values.tolist() ==
        taxa_query_df['kingdom'].values.tolist()) is True

    assert (
        tbl_taxa['phylum'].values.tolist() ==
        taxa_query_df['phylum'].values.tolist()) is True

