from sqlalchemy import create_engine, MetaData, Table, column
from sqlalchemy.sql import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pandas import DataFrame, read_csv, Series
import re
import difflib
import pprint as pp
import ast
import shlex
import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/")
    filepath = (
        "/Users/bibsian/Dropbox/database-development/" +
        "popler_version2/git-repo-revert/"
    )
    end = "/"
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development\\")
    filepath = (
        "C:\\Users\MillerLab\\Dropbox\\database-development\\" +
        "popler_version2\\git-repo-revert\\"
    )
    end = "\\"
os.chdir(rootpath)
from test import class_qualitycontrol as qaqc

# -----------------------------------
# Setting up connections to databases
# ----------------------------------

# ---------------
# Popler Version 2 tables & connection

engine = create_engine(
    'postgresql+psycopg2:///',
    echo=False)
conn = engine.connect()
# Mapping metadata
metadata = MetaData(bind=engine)
# Creating base
Base = declarative_base()


class Ltertable(Base):
    __table__ = Table('lter_table', metadata, autoload=True)


class Sitetable(Base):
    __table__ = Table('site_table', metadata, autoload=True)


class Maintable(Base):
    __table__ = Table('main_table', metadata, autoload=True)
    taxa = relationship(
        'Taxatable', cascade="delete, delete-orphan")
    raw = relationship('Rawtable', cascade="delete, delete-orphan")


class Taxatable(Base):
    __table__ = Table('taxa_table', metadata, autoload=True)


class Rawtable(Base):
    __table__ = Table('raw_table', metadata, autoload=True)


column_name_list = [
    'year', 'day', 'month', 'kingdom', 'phylum', 'clss', 'ordr',
    'family', 'genus', 'species', 'spt_rep1', 'spt_rep2', 'spt_rep3',
    'spt_rep4', 'structure', 'individ', 'unitobs', 'samplingunits',
    'covariates'
]
column_objs = [column(x) for x in column_name_list]


# -----------------------------------
# Setting up connections to databases
# ----------------------------------

# ---------------
# Popler Version 2 tables & connection

engine = create_engine(
    'postgresql+psycopg2:///',
    echo=False)
conn = engine.connect()
# Mapping metadata
metadata = MetaData(bind=engine)
# Creating base
Base = declarative_base()


class Ltertable(Base):
    __table__ = Table('lter_table', metadata, autoload=True)


class Sitetable(Base):
    __table__ = Table('site_table', metadata, autoload=True)


class Maintable(Base):
    __table__ = Table('main_table', metadata, autoload=True)
    taxa = relationship(
        'Taxatable', cascade="delete, delete-orphan")
    raw = relationship('Rawtable', cascade="delete, delete-orphan")


class Taxatable(Base):
    __table__ = Table('taxa_table', metadata, autoload=True)


class Rawtable(Base):
    __table__ = Table('raw_table', metadata, autoload=True)


column_name_list = [
    'year', 'day', 'month', 'kingdom', 'phylum', 'clss', 'ordr',
    'family', 'genus', 'species', 'spt_rep1', 'spt_rep2', 'spt_rep3',
    'spt_rep4', 'structure', 'individ', 'unitobs', 'samplingunits',
    'covariates'
]
column_objs = [column(x) for x in column_name_list]
# ------------------------------
# Running query to get data
# and do qaqc
# ------------------------------
# Getting data from postgres db
# to compare against raw data
def get_data_with_metakey(id_number):
    stmt = conn.execute(
        select(column_objs).
        select_from(
            Rawtable.__table__.
            join(Taxatable.__table__).
            join(Maintable.__table__).
            join(Sitetable)).
        where(column('metarecordid') == id_number).
        order_by(column('sampleid'))
    )
    data = DataFrame(stmt.fetchall())
    data.columns = stmt.keys()
    return data


metadata_key = 12
meta = qaqc.QualityControl(metadata_key)
meta.log_df
site_levels = meta.get_sitelevel_changes(meta.get_log_path('sitetable'))
pp.pprint(site_levels)
data = read_csv(meta.get_file_path())
# data.to_csv(
#    os.path.join(rootpath, 'data_meta'+'_{}.csv'.format(metadata_key)))

site_dict = meta.table_data('sitetable').iloc[0]
obs_dict = meta.table_data('rawtable').iloc[0]
taxa_dict = meta.table_data('taxatable').iloc[0]
main_dict = meta.table_data('maintable')



# ------------------------------
# Running query to get data
# and do qaqc

query_data = get_data_with_metakey(metadata_key)
# query_data.to_csv(
#    os.path.join(rootpath, 'query_meta'+'_{}.csv'.format(metadata_key)))


site_booleans = Series(query_data['spt_rep1']) == Series(data[
    main_dict.iloc[1]['sp_rep1_label'][1][0]])
site_check = len(query_data[site_booleans == False])

obs_booleans = Series(query_data['unitobs']) == Series(data[obs_dict['unitobs'][1]])
obs_check = len(query_data[obs_booleans == False])

taxa_booleans = Series(query_data['species']) == Series(data[taxa_dict['species'][1]])
taxa_check = len(query_data[taxa_booleans == False])
# taxa_mismatch.to_csv(
#    os.path.join(rootpath, 'taxa_mismatch_meta'+'_{}.csv'.format(metadata_key)))
