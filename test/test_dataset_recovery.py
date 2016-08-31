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
def individual_table(base, metadata):
    class individual_table(base):
        __table__ = Table('individual_table', metadata, autoload=True)
    return individual_table

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
def site_in_proj_subq_stmt(
        engine, site_in_project_table, study_site_table,
        project_table, lter_table):
    '''
    Subquery 1 (used to perform union on all tables)
    This subquery perform the necessary joins to bring together
    four tables:
    1) site_in_project_table
    2) study_site_table
    3) lter_table
    4) project_table
    '''
    stmt = (
        select(
            [
                site_in_project_table,
                study_site_table,
                lter_table.lat_lter,
                lter_table.lng_lter,
                lter_table.lterid,
                project_table
            ]).
        select_from(
            site_in_project_table.__table__.
            join(study_site_table.__table__).
            join(lter_table.__table__).join(project_table)).alias()
    )
    return stmt

@pytest.fixture
def taxa_tbl_subq_stmt(
        site_in_proj_subq_stmt, engine,
        taxa_table):
    '''
    Subquery 2 (used to perform union on all tables)
    This subquery performs the join to bring together
    the four tables from subquery 1 and the taxa table.

    '''
    stmt = (
        select([site_in_proj_subq_stmt, taxa_table]).
        select_from(
            site_in_proj_subq_stmt.
            join(taxa_table)).alias()
    )
    return stmt

def test_recover_count_data(
        taxa_tbl_subq_stmt, engine, count_table, count):
    print('what')
    count_tbl_subq_stmt = (
        select([
            taxa_tbl_subq_stmt,
            count_table]).
        select_from(
            taxa_tbl_subq_stmt.
            join(
                count_table,
                onclause=and_(
                    taxa_tbl_subq_stmt.c.taxa_table_key ==
                    count_table.taxa_count_fkey,
                    taxa_tbl_subq_stmt.c.site_in_project_key ==
                    count_table.site_in_project_count_fkey
                )
            )
        ).alias('count join')
    )

    # pretty.pprint(count_tbl_subq_stmt.compile().string)
    Session = sessionmaker(bind=engine)
    session = Session()
    count_tbl_subq_result = session.execute(count_tbl_subq_stmt)
    count_tbl_subq_df = pd.DataFrame(count_tbl_subq_result.fetchall())
    count_tbl_subq_df.columns = count_tbl_subq_result.keys()
    count_tbl_subq_df.sort_values('count_table_key', inplace=True)
    session.close()
    print(count['site'].values.tolist())
    print(count_tbl_subq_df['spatial_replication_level_1'].values.tolist())

    assert (
        count['site'].values.tolist() ==
        count_tbl_subq_df['spatial_replication_level_1'].values.tolist()
    ) == True


    count_tbl_subq_df.to_csv('count_test_recover.csv')
    assert (
        count['count'].values.tolist() ==
        count_tbl_subq_df['count_observation'].values.tolist()
    ) == True

    assert (
        count['genus'].values.tolist() ==
        count_tbl_subq_df['genus'].values.tolist()
    ) == True

    assert (
        count['species'].values.tolist() ==
        count_tbl_subq_df['species'].values.tolist()
    ) == True


    count_tbl_subq_df['spatial_replication_level_2'] = pd.to_numeric(
        count_tbl_subq_df['spatial_replication_level_2'])
    
    assert (
        count['transect'].values.tolist() ==
        count_tbl_subq_df['spatial_replication_level_2'].values.tolist()
    ) == True

    count_tbl_subq_df['month'] = count_tbl_subq_df['month'].astype(int)
    
    assert (
        count['month'].values.tolist() ==
        count_tbl_subq_df['month'].values.tolist()
    ) == True

def test_recover_biomass_data(
        taxa_tbl_subq_stmt, engine, biomass_table, biomass):
    print('what')
    biomass_tbl_subq_stmt = (
        select([
            taxa_tbl_subq_stmt,
            biomass_table]).
        select_from(
            taxa_tbl_subq_stmt.
            join(
                biomass_table,
                onclause=and_(
                    taxa_tbl_subq_stmt.c.taxa_table_key ==
                    biomass_table.taxa_biomass_fkey,
                    taxa_tbl_subq_stmt.c.site_in_project_key ==
                    biomass_table.site_in_project_biomass_fkey
                )
            )
        ).alias('biomass join')
    )

    # pretty.pprint(biomass_tbl_subq_stmt.compile().string)
    Session = sessionmaker(bind=engine)
    session = Session()
    biomass_tbl_subq_result = session.execute(biomass_tbl_subq_stmt)
    biomass_tbl_subq_df = pd.DataFrame(biomass_tbl_subq_result.fetchall())
    biomass_tbl_subq_df.columns = biomass_tbl_subq_result.keys()
    biomass_tbl_subq_df.sort_values('biomass_table_key', inplace=True)
    session.close()
    print(biomass['site'].values.tolist())
    print(biomass_tbl_subq_df['spatial_replication_level_1'].values.tolist())

    assert (
        biomass['site'].values.tolist() ==
        biomass_tbl_subq_df['spatial_replication_level_1'].values.tolist()
    ) == True


    biomass_tbl_subq_df.to_csv('biomass_test_recover.csv')
    assert (
        biomass['biomass'].values.tolist() ==
        biomass_tbl_subq_df['biomass_observation'].values.tolist()
    ) == True

    assert (
        biomass['genus'].values.tolist() ==
        biomass_tbl_subq_df['genus'].values.tolist()
    ) == True

    assert (
        biomass['species'].values.tolist() ==
        biomass_tbl_subq_df['species'].values.tolist()
    ) == True

    assert (
        biomass['plot'].values.tolist() ==
        biomass_tbl_subq_df['spatial_replication_level_2'].values.tolist()
    ) == True
    
    assert (
        biomass['month'].values.tolist() ==
        biomass_tbl_subq_df['month'].values.tolist()
    ) == True

def test_recover_density_data(
        taxa_tbl_subq_stmt, engine, density_table, density):
    print('what')
    density_tbl_subq_stmt = (
        select([
            taxa_tbl_subq_stmt,
            density_table]).
        select_from(
            taxa_tbl_subq_stmt.
            join(
                density_table,
                onclause=and_(
                    taxa_tbl_subq_stmt.c.taxa_table_key ==
                    density_table.taxa_density_fkey,
                    taxa_tbl_subq_stmt.c.site_in_project_key ==
                    density_table.site_in_project_density_fkey
                )
            )
        ).alias('density join')
    )

    # pretty.pprint(density_tbl_subq_stmt.compile().string)
    Session = sessionmaker(bind=engine)
    session = Session()
    density_tbl_subq_result = session.execute(density_tbl_subq_stmt)
    density_tbl_subq_df = pd.DataFrame(density_tbl_subq_result.fetchall())
    density_tbl_subq_df.columns = density_tbl_subq_result.keys()
    density_tbl_subq_df.sort_values('density_table_key', inplace=True)
    session.close()

    assert (
        density['SITE'].values.tolist() ==
        density_tbl_subq_df['spatial_replication_level_1'].values.tolist()
    ) == True

    density_tbl_subq_df.to_csv('density_test_recover.csv')
    assert (
        density['DENSITY'].values.tolist() ==
        density_tbl_subq_df['density_observation'].values.tolist()
    ) == True

    assert (
        density['TAXON_GENUS'].values.tolist() ==
        density_tbl_subq_df['genus'].values.tolist()
    ) == True

    assert (
        density['TAXON_SPECIES'].values.tolist() ==
        density_tbl_subq_df['species'].values.tolist()
    ) == True

    assert (
        density['TRANSECT'].values.tolist() ==
        density_tbl_subq_df['spatial_replication_level_2'].values.tolist()
    ) == True
    
    assert (
        density['MONTH'].values.tolist() ==
        density_tbl_subq_df['month'].values.tolist()
    ) == True
