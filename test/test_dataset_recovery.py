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

def test_recover_count_data(count, count_table, conn):
    statement = (
        select([count_table]).
        select_from(
            count_table
        )
    )
    
