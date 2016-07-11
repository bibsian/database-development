#! /usr/bin/env python
import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Dropbox/database-development/" +
        "test/")
    end = "/"
    
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Dropbox\\database-development" +
        "\\test\\")
    end = "\\"
os.chdir(rootpath)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, create_engine
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
    filename='Logs_DbTransactions/database_log_{}.log'.format(date))
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


# Adapter for numpy datatypes
def adapt_numpy_int64(numpy_int64):
    ''' Enable postgres to recognize numpy's int64 data type'''
    return AsIs(numpy_int64)
register_adapter(numpy.int64, adapt_numpy_int64)

engine = create_engine(
    'postgresql+psycopg2://username@host/LTERV2',
    echo=True)
conn = engine.connect()

# Creating base
Base = declarative_base()

# Instantiating the classes which represent our database
# tables and making their names available at the level
# of the whole UserInterface main window

class Ltertable(Base):
    __tablename__ = 'lter_table'

    lterid = Column(VARCHAR, primary_key=True)
    lter_name = Column(TEXT)
    currently_funded = Column(VARCHAR)
    pi = Column(VARCHAR)
    pi_contact_email = Column(VARCHAR)
    alt_contact_email = Column(VARCHAR)
    homepage = Column(VARCHAR)


class Sitetable(Base):
    __tablename__ = 'site_table'

    siteid = Column(VARCHAR, primary_key=True)
    lterid = Column(VARCHAR, ForeignKey('lter_table.lterid'))
    lat = Column(NUMERIC)
    lng = Column(NUMERIC)
    descript = Column(TEXT)


class Maintable(Base):
    __tablename__ = 'main_table'

    lter_proj_site = Column(Integer, primary_key=True)
    metarecordid = Column(INTEGER)
    title = Column(TEXT)
    samplingunits = Column(VARCHAR)
    samplingprotocol = Column(VARCHAR)
    structured = Column(VARCHAR)
    studystartyr = Column(NUMERIC)
    studyendyr = Column(NUMERIC)
    siteid = Column(VARCHAR, ForeignKey('site_table.siteid'))
    sitestartyr = Column(NUMERIC)
    siteendyr = Column(NUMERIC)
    samplefreq = Column(TEXT)
    totalobs = Column(NUMERIC)
    studytype = Column(VARCHAR)
    community = Column(BOOLEAN)
    uniquetaxaunits = Column(NUMERIC)
    sp_rep1_ext = Column(NUMERIC)
    sp_rep1_ext_units = Column(VARCHAR)
    sp_rep1_label = Column(VARCHAR)
    sp_rep1_uniquelevels = Column(NUMERIC)
    sp_rep2_ext = Column(NUMERIC)
    sp_rep2_ext_units = Column(VARCHAR)
    sp_rep2_label = Column(VARCHAR)
    sp_rep2_uniquelevels = Column(NUMERIC)
    sp_rep3_ext = Column(NUMERIC)
    sp_rep3_ext_units = Column(VARCHAR)
    sp_rep3_label = Column(VARCHAR)
    sp_rep3_uniquelevels = Column(NUMERIC)
    sp_rep4_ext = Column(NUMERIC)
    sp_rep4_ext_units = Column(VARCHAR)
    sp_rep4_label = Column(VARCHAR)
    sp_rep4_uniquelevels = Column(NUMERIC)
    authors = Column(TEXT)
    authors_contact = Column(VARCHAR)
    metalink = Column(VARCHAR)
    knbid = Column(VARCHAR)

    taxa = relationship(
        'Taxatable', cascade="delete, delete-orphan")

    raw = relationship('Rawtable', cascade="delete, delete-orphan")
    
class Taxatable(Base):
    __tablename__ = 'taxa_table'
    taxaid = Column(Integer, primary_key=True)
    lter_proj_site = Column(Integer, ForeignKey('main_table.lter_proj_site'))
    sppcode = Column(VARCHAR)
    kingdom = Column(VARCHAR)
    phylum = Column(VARCHAR)
    clss = Column(VARCHAR)
    order = Column(VARCHAR)
    family = Column(VARCHAR)
    genus = Column(VARCHAR)
    species = Column(VARCHAR)
    authority = Column(VARCHAR)

class Rawtable(Base):
    __tablename__ = 'raw_table'

    sampleid = Column(Integer, primary_key=True)
    taxaid = Column(Integer, ForeignKey('taxa_table.taxaid'))
    lter_proj_site = Column(Integer, ForeignKey('main_table.lter_proj_site'))
    year = Column(NUMERIC)
    month = Column(NUMERIC)
    day = Column(NUMERIC)
    spt_rep1 = Column(VARCHAR)
    spt_rep2 = Column(VARCHAR)
    spt_rep3 = Column(VARCHAR)
    spt_rep4 = Column(VARCHAR)
    structure = Column(VARCHAR)
    individ = Column(VARCHAR)
    unitobs = Column(NUMERIC)
    covariates = Column(TEXT)

Session = sessionmaker(bind=engine, autoflush=False)


# Helper Functions
def find_types(orm):
    ''' Method to get data types from Orms'''
    dictname = (orm.__tablename__.split("_")[0] + "types")
    dictname = {}
    for i,item in enumerate(orm.__table__.c):
        name = (str(item).split('.')[1])
        dictname[name] = str(
            orm.__table__.c[name].type)
    return dictname

sitetypes = find_types(Sitetable)
maintypes = find_types(Maintable)
taxatypes = find_types(Taxatable)
rawtypes = find_types(Rawtable)


def convert_types(dataframe, types):
    ''' Method to convert data types in dataframe to match Orm'''
    for i in dataframe.columns:
        if types[i] in ['NUMERIC', 'INTEGER']:
            dataframe[i] = pd.to_numeric(dataframe[i], errors='coerce')
        elif types[i] in ['VARCHAR', 'TEXT']:
            dataframe[i] = dataframe[i].astype(object)
