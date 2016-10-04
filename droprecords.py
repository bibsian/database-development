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
        echo=False)
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
def taxa_accepted_table(base, metadata):
    class taxa_accepted_table(base):
        __table__ = Table('taxa_accepted_table', metadata, autoload=True)

    return taxa_accepted_table

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


#
# ----- Not really a test, more just reseting the database
#
def test_drop_records(
        conn, biomass_table, count_table, density_table,
        individual_table, percent_cover_table, taxa_table,
        taxa_accepted_table,
        project_table, site_in_project_table, study_site_table):

    table_dict = OrderedDict([
        ('biomass_table', biomass_table),
        ('count_table', count_table),
        ('density_table', density_table),
        ('individual_table', individual_table),
        ('percent_cover_table', percent_cover_table),
        ('taxa_accepted_table', taxa_accepted_table),
        ('taxa_table', taxa_table),
        ('site_in_project_table', site_in_project_table),
        ('project_table', project_table),
        ('study_site_table', study_site_table)]
    )

    for i, item in enumerate(table_dict):
        delete_statement = table_dict[item].__table__.delete()
        conn.execute(delete_statement)
    conn.close()
