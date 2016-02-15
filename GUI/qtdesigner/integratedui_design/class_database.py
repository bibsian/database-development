# This is the class that will use SQLalchemy to
# push information to the database
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy.orm import sessionmaker, aliased
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from contextlib import contextmanager
import psycopg2
import logging as log
import datetime as TM


class LterTableQuery(object):
    def go(self, session, configclass):
        ltertable = configclass
        return session.query(ltertable, ltertable.lterID).all()
    

class SiteTableQuery(object):
    def go(self, session, configclass):
        sitetable = configclass
        return session.query( sitetable, sitetable.siteID,
            sitetable.lterID).all()

