#! /usr/bin/env python
import pandas as pd
from sqlalchemy import (create_engine, MetaData, Table)
from sqlalchemy.orm import sessionmaker, relationship, load_only
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import select, update
from sqlalchemy.sql.expression import bindparam
from psycopg2.extensions import register_adapter, AsIs
import numpy as numpy
import sys
import os
import glob
import re
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Dropbox/database-development/" +
        "poplerGUI/")
    end = "/"

elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Dropbox\\database-development" +
        "\\poplerGUI\\")
    end = "\\"

# Adapter for numpy datatypes
def adapt_numpy_int64(numpy_int64):
    ''' Enable postgres to recognize numpy's int64 data type'''
    return AsIs(numpy_int64)
register_adapter(numpy.int64, adapt_numpy_int64)



# ---
# This script is for updating the database records for
# gloabid's 1 and 2. The database did not have
# all columns and required a modification (migration via alembic).
# After the modifactions were made to the database,
# (see below:
# main_table: treatment_type, num_treatments, exp_maintainence,
# and trt_label
#
# raw_table: trt_label)
#
# default values were inserted to new columns (as datasets did
# not contain pertinent information).
#
# main_table defaults:
# treatment_type = habitat
# num_treatments = NA
# exp_maintainence = NA
# trt_label = NA
#
# raw_table defaults:
# trt_label = NA
#
# ---

# Pulling up raw data files associated with
# gloabl id 1 and 2
os.chdir(rootpath + 'Logs_UI')
data_files = []
for i in glob.glob('*'):
    data_files.append(i.split('.csv')[0])

global_id = [re.split('table_|update_', x)[0][0] for x in data_files]
filename = [re.split('table_|update_', x)[1] for x in data_files]

combo = []
for i,item in enumerate(global_id):
    combo.append((item, filename[i]))

datafiles = [x for x in list(set(combo)) if x[1] is not '']

df1 = str(datafiles[0][1]) + '.csv'
global1 = str(datafiles[0][0]) + '.csv'

df2 = str(datafiles[1][1]) + '.csv'
global2 = str(datafiles[1][0])


rawdf_1 = pd.read_csv(
    rootpath + 'Metadata_and_og_data' + end + df1)
rawdf_2  = pd.read_csv(
    rootpath + 'Metadata_and_og_data' + end + df2)


# Creating database connection and orms
engine = create_engine(
    'postgresql+psycopg2://user:pswd@host/popler_',
    echo=False
)
metadata = MetaData(bind=engine)
base = declarative_base()

class lter_table(base):
    __table__ = Table('lter_table', metadata, autoload=True)

class site_table(base):
    __table__ = Table('site_table', metadata, autoload=True)

class main_table(base):
    __table__ = Table('main_table', metadata, autoload=True)
    taxa = relationship('taxa_table', cascade='all, delete-orphan')
    
class taxa_table(base):
    __table__ = Table('taxa_table', metadata, autoload=True)
    raw = relationship('raw_table', cascade='all, delete-orphan')    

class raw_table(base):
    __table__ = Table('raw_table', metadata, autoload=True)

# Creating database session    
Session = sessionmaker(bind=engine)
session = Session()

# For the main table i did a query of available data,
# set records for new columns, added changes to the session
# and commited the changes
main_query = (
    session.query(main_table).
    order_by(main_table.lter_proj_site))
maindf = pd.read_sql(main_query.statement, main_query.session.bind)

treatment_type = ('habitat '*len(maindf)).split()
num_treatments = ('NA '*len(maindf)).split()
exp_maintainence = ('NA '*len(maindf)).split()
trt_label = ('NA '*len(maindf)).split()

updatedf = maindf[['trt_label', 'num_treatments']]
updatedf.loc[:, 'treatment_type'] = treatment_type
updatedf.loc[:, 'exp_maintainence'] = exp_maintainence
updatedf.loc[:, 'num_treatments'] = num_treatments
updatedf.loc[:, 'trt_label'] = trt_label

updated_columns = updatedf.columns.values.tolist()

mainupdates = {}
for i in range(len(maindf)):
    mainupdates[i] = session.query(
        main_table).filter(
            main_table.lter_proj_site ==
            maindf['lter_proj_site'].iloc[i]).one()
    session.add(mainupdates[i])
    
for i in range(len(updatedf)):
    dbupload = updatedf[updated_columns].loc[
        i, updatedf[updated_columns].columns].to_dict()
    for key in dbupload.items():
        setattr(
            mainupdates[i], key[0], key[1])
        session.add(mainupdates[i])
session.flush()
session.commit()


# I found that the previous version of updating values
# is VERY inefficient. Here I made use of the update()
# sql feature and a raw database connection/transaction
# method

# Querying database for all primary_keys and new columns (trt_label)
raw_query = (
        session.query(raw_table).
        order_by(raw_table.sampleid).
        options(load_only('sampleid', 'trt_label')))
rawdf = pd.read_sql(raw_query.statement, raw_query.session.bind)
raw_trt_label = ('NA '*len(rawdf)).split()

# Creting connection and updating records
conn = engine.connect()
trans = conn.begin()
for i in range(len(rawdf)):
    stmt = (raw_table.__table__.update().values(
        {raw_table.trt_label: 'NA'})).where(
            raw_table.sampleid == i+1)
    conn.execute(stmt)
print('transaction complete')    
trans.commit()
conn.close()
engine.dispose()
# this method takes about 30s to update 30000 records.
# the previous method would take > 1 hr and still
# not be done/cause the machine to become extremely slow.
# Although this may have been related to not turning of the
# echo from sqlalchemy...


