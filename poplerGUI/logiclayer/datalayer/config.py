#!/usr/bin/env python
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
import re
rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname( __file__ ))))
end = os.path.sep

if getattr(sys, 'frozen', False):
	# we are running in a bundle
	transaction_path = os.path.join(os.path.dirname(sys.executable), 'db_transactions')
	logpath = os.path.join(os.path.dirname(sys.executable), 'logs')

else:
	# we are running in a normal Python environment
	transaction_path = os.path.join(rootpath, 'db_transactions')
	logpath = os.path.join(rootpath, 'logs')


if not os.path.exists(transaction_path):
    os.makedirs(transaction_path)
if not os.path.exists(logpath):
    os.makedirs(logpath)


# Setup logging for program
date = (str(dt.datetime.now()).split()[0]).replace("-", "_")
logging.basicConfig(filename= os.path.join(transaction_path, 'database_log_{}.log'.format(date)))
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Adapter for numpy datatypes
def adapt_numpy_int64(numpy_int64):
    ''' Enable postgres to recognize numpy's int64 data type'''
    return AsIs(numpy_int64)
register_adapter(numpy.int64, adapt_numpy_int64)

# Creating database engin
engine = create_engine(
    'postgresql+psycopg2://--/--',
    echo=False)
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
    site_in_proj = relationship(
        'site_in_project_table', cascade="delete, delete-orphan")
class site_in_project_table(base):
    __table__ = Table('site_in_project_table', metadata, autoload=True)
    taxa = relationship(
        'taxa_table', cascade="delete, delete-orphan")
class taxa_table(base):
    __table__ = Table('taxa_table', metadata, autoload=True)
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

# Session maker to perform transactions
Session = sessionmaker(bind=engine, autoflush=False)

# Helper Functions
def find_types(tbl, name):
    ''' Method to get data types from Tbls'''
    dictname = {}
    for i, item in enumerate(tbl.__table__.c):
        name = (str(item).split('.')[1])
        dictname[name] = str(
            tbl.__table__.c[name].type)
    return dictname

# Getting datatypes from database to perform checks prior to uploading
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

        if types[i] in [
                'VARCHAR', 'TEXT', 'VARCHAR(50)', 'VARCHAR(200)',
                'spatial_replication_level_1', 'spatial_replication_level_2',
                'spatial_replication_level_3', 'spatial_replication_level_4',
                'spatial_replication_level_5']:
            try:
                dataframe.loc[:, i] = dataframe.loc[:, i].apply(str).values
                print('In CONVERT: ', i ,dataframe.loc[:,i].dtypes)
            except Exception as e:
                print('string conversion did not work:', i, str(e))
            dataframe.loc[:, i] = dataframe.loc[:, i].astype(object).values

        if types[i] in ['NUMERIC', 'numeric', 'INTEGER', 'integer']:
            try:
                dataframe.loc[:, i] = pd.to_numeric(dataframe.loc[:, i].values, errors='coerce')
            except Exception as e:
                print('numeric conversion did not work:', i, str(e))

        if re.search('observation', i) is not None or re.search('_extent$', i) is not None or re.search('unique_reps', i) is not None:
            dataframe.loc[:, i] = pd.to_numeric(dataframe.loc[:, i].values, errors='coerce')


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
