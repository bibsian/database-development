#! /usr/bin/env python
import sys, os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, create_engine, MetaData
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.sql.expression import update
from psycopg2.extensions import register_adapter, AsIs
import numpy
import datetime as dt
import logging
import pandas as pd

__all__ = [
    'Ltertable', 'Sitetable', 'Maintable', 'Taxatable', 'Rawtable',
    'Session', 'convert_types', 'sitetypes', 'maintypes', 'taxatypes',
    'rawtypes']

# Setup logging for program
date = (str(dt.datetime.now()).split()[0]).replace("-", "_")
logging.basicConfig(
    filename='db_transactions/database_log_{}.log'.format(date))
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


# Adapter for numpy datatypes
def adapt_numpy_int64(numpy_int64):
    ''' Enable postgres to recognize numpy's int64 data type'''
    return AsIs(numpy_int64)
register_adapter(numpy.int64, adapt_numpy_int64)

engine = create_engine(
    'postgresql+psycopg2://postgres:demography@localhost/popler_3',
    echo=True)
conn = engine.connect()

# Mapping metadata
metadata = MetaData(bind=engine)

# Creating base
base = declarative_base()

# creating classes for tables to query things
class lter_table(base):
    __table__ = Table('lter_table', metadata, autoload=True)


class study_site_table(base):
    __table__ = Table('study_site_table', metadata, autoload=True)


class project_table(base):
    __table__ = Table('project_table', metadata, autoload=True)
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


class site_in_project_table(base):
    __table__ = Table('site_in_project_table', metadata, autoload=True)


class taxa_table(base):
    __table__ = Table('taxa_table', metadata, autoload=True)


class taxa_accepted_table(base):
    __table__ = Table('taxa_accepted_table', metadata, autoload=True)


class count_table(base):
    __table__ = Table('count_table', metadata, autoload=True)


class biomass_table(base):
    __table__ = Table('biomass_table', metadata, autoload=True)


class density_table(base):
    __table__ = Table('density_table', metadata, autoload=True)


class percent_cover_table(base):
    __table__ = Table('percent_cover_table', metadata, autoload=True)


class individual_table(base):
    __table__ = Table('individual_table', metadata, autoload=True)


Session = sessionmaker(bind=engine, autoflush=False)


# Helper Functions
def find_types(tbl, name):
    ''' Method to get data types from Tbls'''
    dictname = {}
    for i, item in enumerate(tbl.__table__.c):
        name = (str(item).split('.')[1])
        print('col name in table: find_types ', name)
        dictname[name] = str(
            tbl.__table__.c[name].type)
    return dictname

study_site_types = find_types(study_site_table, 'study_site')
project_types = find_types(project_table, 'project')
taxa_types = find_types(taxa_table, 'taxa')
taxa_accepted_types = find_types(taxa_accepted_table, 'taxa_accepted')
count_types = find_types(count_table, 'count')
biomass_types = find_types(biomass_table, 'biomass')
density_types = find_types(density_table, 'density')
percent_cover_types = find_types(percent_cover_table, 'percent_cover')
individual_types = find_types(individual_table, 'individual')


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
