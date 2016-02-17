# These are the classes that will use SQLalchemy to
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
import run_ui_mainwindow as mw



class LterTableQuery(object):
    ''' 
    This class will perform one unit of work and query the
    database so that it will return information about all
    LTER's that exist (probably overkill but why not)
    '''
    def go(self, session, configclass):
        ltertable = configclass
        return session.query(ltertable, ltertable.lterID).all()




class SiteTableQuery(object):
    '''
    This class will perform one unit of work and query the database
    so that it will return information about all the siteID's that
    have been entered into the site table of the database 

    Note: As the databse grows this query may return a huge list
    of items and the algorithm that uses this information to 
    screen data may take a very long time...may want to watch this
    '''
    def go(self, session, configclass):
        sitetable = configclass
        return session.query( sitetable, sitetable.siteID,
            sitetable.lterID).all()

class MainTableQuery(object):
    '''
    This class will perform one unit of work and query the database
    so that it will return information about all the siteID's that
    have been entered into the main table of database 

    Note: As the databse grows this query may return a huge list
    of items and the algorithm that uses this information to 
    screen data may take a very long time...may want to watch this
    '''
    def go(self, session, configclass):
        maintable = configclass
        return session.query( maintable, maintable.siteID,
            maintable.metalink).all()


class UploadToDatabase(object):
    '''
    This class will be used to upload data that was concatenated
    from user information to make tables, compare the data against 
    which is already in the database and then proceed to push it
    /append a table base on input data.

    The class takes multiple arguments:
    1) data: A DataFrame object
    2) config: The config objects derived from the configuration file
    i.e. see config.py
    3) table: A table name that will be appended i.e. 'sitetable'
    4) sitelist: a list of unique site abbreviations from user
    5) lter: an lter location supplied to the combobox from user
    '''
    def __init__(self, data, configclass, table, sitelist=None,
                 lter=None):
        self.data = data
        self.config = configclass
        self.table = table
        if sitelist is not None:
            self.sitelist = sitelist
        if lter is not None:
            self.lter = lter
        else:
            pass
        self.w = None

    # Creating a method that will take the arguments supplied to
    # the class, perform database queries in a unit of work
    # pattern to retrieve information, then compare
    # the information about to be loaded to a given table
    # and either return and error or pass the check and
    # get prepared to handle the database push
    def check_previous_sites(self):
        # Create session from factory
        session = self.config.Session()

        # Create a list of site abbreviates already
        # present in the database
        previousSitecheck = []
        # Create a list of all lters already present
        # in the database
        allLTERlocation = []

        # Fill list of LTER location
        for row in\
            LterTableQuery().go(session, self.config.ltertable):
            allLTERlocation.append(row.lterID)

        # The table argument supplies the table in the database
        # that information is attempting to be pushed to.
        if self.table == 'sitetable' :
            
            # Update the lists through two queries and
            # and the information retrieved
            for row in\
                SiteTableQuery().go(session, self.config.sitetable):
                previousSitecheck.append(row.siteID)

            # check the quieried information against that
            # supplied by the user (is this a unique
            # siteID about to be added)
            checkedSite = [
                i for i in previousSitecheck if i in self.sitelist]

        elif self.table == 'maintable':
            # Update the lists through two queries and
            # and the information retrieved
            for row in\
                MainTableQuery().go(session, self.config.maintable):
                previousSitecheck.append(row.siteID)

            # check the quieried information against that
            # supplied by the user (is this a unique
            # siteID about to be added)
            checkedSite = [
                i for i in previousSitecheck if i in self.sitelist]

        else:
            pass
        session.close()
        
        try:
            # check the quieried infomraotin against
            # that suppliued by the user (is this an established)
            # lter.
            checkedLTER = [i for i in allLTERlocation if i in self.lter]

            
        except Exception as e:
            print(str(e))


        finally:

            # Return a boolean to from this method
            # True: if no similar siteID abbreviations exits
            # and the lter specified is an established one.
            # False otherwise
            return len(checkedSite) == 0 and str(self.lter) in checkedLTER 

    def check_previous_taxa(self):
        if self.table == 'taxatable':
            pass
        elif self.table == 'rawtable':
            pass
        else:
            pass

    # Method to table the supplied dataframe from the user along
    # with the rest of the arguments and append the databse with
    # it. NOTE: THIS METHOD MUST BE PROCEEDED BY AN IF
    # STATEMENT TO CHECK THE PREVIOUS ENTRIES OF THE DATABASE
    # Otherwise reduant data can be added.
    def push_table_to_postgres(self):
        # Designating the table name to push to based on
        # arguments supplied to the class
        if self.table == 'sitetable':
            try:
                tabletopushto = str(
                    self.config.sitetable.__table__.name)
            except Error as e:
                print(str(e))
                
        elif self.table =='maintable':
            try:
                tabletopushto= str(
                    self.config.maintable.__table__.name)
            except Exception as e:
                print(str(e))

        elif self.table == 'taxatable':
            pass

        elif self.table == 'rawtable':
            pass

        else:
            pass

        # Trying to push the data to the database.
        try:
            self.data.to_sql(
                tabletopushto, con=self.config.engine,
                if_exists="append",index=False)
        except Exception as e:
            print(str(e))

