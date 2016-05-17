# THis file is going to be created to
# houst the constants of our program i.e.
# the databse engine and the database session factory maker
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
import psycopg2
import datetime as dt
import logging


# Creating a connection to the database specifying echo
# as false so we will not log information twice when
# writing SQL transactions. THis is at the global level
# so we can use sessions and unitofwork patterns
# with sqlalchemy
#global engine
engine = create_engine(
    'postgresql+psycopg2://username:password@localhost/LTER'\
    , echo= False)

# Set up the base
#global base
base = automap_base()

# And prepare the classes based on the reflection of the
# database structure
base.prepare(engine, reflect=True)

# Instantiating the classes which represent our database
# tables and making their names available at the level
# of the whole UserInterface main window

ltertable = base.classes.lter

sitetable = base.classes.siteID

maintable = base.classes.main_data

taxatable = base.classes.taxa

rawtable = base.classes.rawobs



# Creating a factory that can supply connection resources
# uses sessionmaker
Session = sessionmaker(bind=engine)



