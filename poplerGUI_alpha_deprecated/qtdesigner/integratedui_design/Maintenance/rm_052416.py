#!/usr/bin/env python
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine((
    'postgresql+psycopg2://postgres:beerbayes@localhost:63333/' +
    'LTER'), echo= True)
metadata = MetaData(bind=engine)
base = declarative_base()

class ltertable(base):
    __table__ = Table('lter', metadata, autoload=True)
    
class sitetable (base):
    __table__ = Table('siteID', metadata, autoload=True)
    
class maintable(base):
    __table__ = Table('main_data', metadata, autoload=True)
    taxa = relationship('taxatable', cascade='all, delete-orphan')

class taxatable(base):
    __table__ = Table('taxa', metadata, autoload=True)
    raw = relationship('rawtable', cascade='all, delete-orphan')

class rawtable(base):
    __table__ = Table('rawobs', metadata, autoload=True)

    

# Start sqlalchemy session
Session = sessionmaker(bind=engine)
session = Session()

# Step 1:
# Inspecting which sites must
# be removed based on maintable siteid
# and sitable siteid.
# i.e. if siteid is in sitetable but not maintable
# then the maintable data was not upload (liv hit a snag)
mainq = session.query(maintable).order_by(maintable.siteID)
mt = pd.read_sql(mainq.statement, mainq.session.bind)
sitekeep = mt['siteID'].drop_duplicates().values.tolist()

siteq = session.query(sitetable).order_by(sitetable.siteID)
sd = pd.read_sql(siteq.statement, siteq.session.bind)
siteall = sd['siteID'].drop_duplicates().values.tolist()

sitemr = [x for x in siteall if x not in sitekeep]

# Step 2: See maintenace directory 'progess' file in project folder
# List of knb's to identify
# data that must be removed.
# Data after maintable was NOT uploaded (liv hit a snag)
rmknb = [
    'knb-lter-sbc.17.28',
    'knb-lter-sbc.52.3'
]

# Using knbs above to get projID's to remove
# from the remaining database
rmproj = mt[mt['knbID'].isin(rmknb)].sort_values(
    by='projID')['projID'].drop_duplicates().values.tolist()

# Bulk delete commands based on projID's to be removed
session.query(rawtable).filter(
    rawtable.projID.in_(rmproj)).delete(synchronize_session='fetch')
session.commit()

session.query(taxatable).filter(
    taxatable.projID.in_(rmproj)).delete(synchronize_session='fetch')
session.commit()

session.query(maintable).filter(
    maintable.projID.in_(rmproj)).delete(synchronize_session='fetch')
session.commit()

# Double checking database for traces of
# projID's we just deleted
update_qmain = session.query(maintable)
up_m_df = pd.read_sql(update_qmain.statement, update_qmain.session.bind)
assert (not [x for x in
        up_m_df['projID'].drop_duplicates().values.tolist() if x
        in rmproj]) is True

update_qtaxa = session.query(taxatable)
up_t_df = pd.read_sql(update_qtaxa.statement, update_qtaxa.session.bind)
assert (not [x for x in
        up_t_df['projID'].drop_duplicates().values.tolist() if x
        in rmproj]) is True


update_raw = session.query(rawtable)
up_r_df = pd.read_sql(update_raw.statement, update_raw.session.bind)
assert (not [x for x in
        up_r_df['projID'].drop_duplicates().values.tolist() if x
        in rmproj]) is True

session.close()
# Fin.
