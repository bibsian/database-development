# script just to try out
# python code, nothing will be commented of kept for
# use in the program
# used to talk to the postgresql database
from sqlalchemy import create_engine, exc, event, select
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.ext.automap import automap_base
from pprint import pprint
import pandas as pd
import dbmanager

# declare the automap base
base = automap_base()

# create the engine to connect to the
# database
engine = create_engine(
    'postgresql+psycopg2://postgres:demography@localhost/LTER',
            echo=True)

######################################
# Testing the automap function and
# creating our table classes with the built in method
#################################

# reflect tables in the database on our base map
base.prepare(engine, reflect=True)

# classes are created for each table in the database
# and we're assignig them to an object to print from
# and test
lter = base.classes.lter
site = base.classes.siteID
main = base.classes.main_data


winlter = 'C:\\Users\MillerLab\\Box Sync\\LTER\\Database\\\
GUIdevelopment\\QtDesigner\\lter_table_test.csv'
winsite = 'C:\\Users\\MillerLab\\Box Sync\\LTER\\Database\\\
GUIdevelopment\\QtDesigner\\SiteID_TestData.csv'
winmain = 'C:\\Users\\MillerLab\\Box Sync\\LTER\\Database\\\
GUIdevelopment\\QtDesigner\\main_data_test.csv'


import os

maclter = '~/Box Sync/LTER/Database/\
GUIdevelopment/QtDesigner/lter_table_test.csv'
macsite =  '~/Box Sync/LTER/Database/\
GUIdevelopment/QtDesigner/SiteID_TestData.csv'
macmain =  '~/Box Sync/LTER/Database/\
GUIdevelopment/QtDesigner/main_data_test.csv'


#####################
# Loading some data
# into the database with the connection
###################
lterdf = pd.read_csv(maclter)

# and dataset information
sitedf = pd.read_csv(macsite)

maindf = pd.read_csv(macmain)

lterdf.to_sql(lter.__table__.name, con=engine, if_exists="append",
              index=False)


sitedf.to_sql(
    str(site.__table__.name), con=engine, if_exists="append",
    index=False)

maindf.to_sql(str(main.__table__.name), con=engine, if_exists="append",
              index=False)


#########################
# Creating a session to query our database
###################
Session = sessionmaker(bind=engine)
session = Session()

# query the classes we created from
# the automap through our session connection
q1 = session.query(lter).all()

# printing the results using sqlalchemy syntax
# and python
for test in q1:
    pprint(test.lterID + " " + test.lter_name)

 session.query(site).filter(site.lterID.any(lter.lterID=='AND')).one().name
 
q2=select([site.lterID]).select_from(site.__table__.join(lter
)).where(lter.lterID == "AND")

print(q2)
for i in q2:
    print(i.name)
