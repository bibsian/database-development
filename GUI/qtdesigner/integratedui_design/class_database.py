# G These are the classes that will use SQLalchemy to
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
        return session.query(sitetable, sitetable.siteID,
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
        return session.query(
            maintable, maintable.projID, maintable.siteID,
            maintable.metalink).all()


class TaxaTableQuery(object):
    '''
    This class will perform one unit of work and query the databse
    so that it will return informatoin about the projID's that
    have been entered and those sites that it corresponds too.
    '''

    def go(self, session, configclass):
        taxatable = configclass
        return session.query(
            taxatable, taxatable.taxaID, taxatable.projID,
            taxatable.sppcode, taxatable.kingdom,
            taxatable.phylum, taxatable.order).all()

class RawTableQuery(object):
    '''
    This class will perform one unit of work and query the databse
    so that it will return informatoin about the projID's that
    have been entered and those sites that it corresponds too.
    '''

    def go(self, session, configclass):
        rawtable = configclass
        return session.query(
            rawtable, rawtable.sampleID, rawtable.taxaID,
            rawtable.projID).all()

    
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
                 lter=None, meta=None, taxaprojIDlist=None,
                 rawprojID=None, rawtaxaID=None):
        self.data = data
        self.config = configclass
        self.table = table
        if sitelist is not None:
            self.sitelist = sitelist
        if lter is not None:
            self.lter = lter
        if meta is not None:
            self.meta = meta
        if taxaprojIDlist is not None:
            self.taxaprojID = taxaprojIDlist
        if rawprojID is not None:
            self.rawprojID = rawprojID
        if rawtaxaID is not None:
            self.rawtaxaID = rawtaxaID
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

        # Creat a list of metadata urls already present
        # in the database
        previousmetacheck = []

        # Create a list of all lters already present
        # in the database
        allLTERlocation = []

        # Fill list of LTER location
        for row in\
                LterTableQuery().go(session, self.config.ltertable):
            allLTERlocation.append(row.lterID)

        # The table argument supplies the table in the database
        # that information is attempting to be pushed to.
        if self.table == 'sitetable':

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
                previousmetacheck.append(row.metalink)

            # check the quieried information against that
            # supplied by the user (is this a unique
            # siteID about to be added)
            checkedSite = [
                i for i in set(previousSitecheck) if i in self.sitelist]
            checkedMeta = [
                i for i in set(previousmetacheck) if i in self.meta]

        else:
            pass

        # Closing session
        session.close()

        try:
            # check that the user is from an established lter.
            checkedLTER = [i for i in allLTERlocation if i in self.lter]

        except Exception as e:
            return print(str(e))

        finally:
            boolist = []

            if self.table == 'sitetable':
                # Retrun boolean list.
                # all(TRUE) means that:

                # 1) There are 0 similar site abbreviations in
                # the current database
                boolist.append(len(checkedSite) == 0)
                # 2) The LTER is a previously identified LTER location
                boolist.append(str(self.lter) in checkedLTER)

                return boolist

            elif self.table == 'maintable':
                # Return boolean list.
                # all(TRUE) means that:

                # 1) There are 0 or more site abbreviations
                # that match the records about to be pushed
                # THIS IS OKAY because studies can use
                # the same site locations at LTER's
                boolist.append(len(checkedSite) >= 0)

                # 2) The metadata url of the records about to
                # be pushed is unique. So if site abbreviations
                # are already present for this then
                # if the metadataurl is unique, the site was
                # used in a different project
                boolist.append(len(checkedMeta) == 0)
                return boolist

    # This needs to be created
    def check_previous_taxa(self):
        # Create session from factory
        session = self.config.Session()

        if self.table == 'taxatable':
            try:
                # Create a list that will have all the projID's that
                # are present in the taxa table
                taxaprojIDcurrent = []

                # Fill in the taxaprojIDcurrent list with queried
                # information (this performs a unit of work)
                for row in\
                        TaxaTableQuery().go(session, self.config.taxatable):
                    taxaprojIDcurrent.append(row.projID)

                taxaprojcheck = [
                    i for i in set(taxaprojIDcurrent) if i in self.taxaprojID]

                if taxaprojcheck == None:
                    boolist = [True]
                    return boolist
                else:
                    pass

                print(list(set(taxaprojcheck)))

                # Creating a boolean list to returnPressed
                boolist = []

                # Appending the boolean list with a our check
                # on the taxa/projID info
                boolist.append(len(list(taxaprojcheck)) == 0)

                return boolist
            except Exception as e:
                print(str(e))
            finally:
                session.close()
        else:
            pass

    def check_previous_rawobs(self):
        session = self.config.Session()
        
        # Creating a list that will have all the sampleID's
        # that are present in the rawobs table
        projIDcurrent = []
        taxaIDcurrent = []

        try:
            # Query to fill in list created above
            for row in RawTableQuery().go(session, self.config.rawtable):
                projIDcurrent.append(row.projID)
                taxaIDcurrent.append(row.taxaID)

            projIDcheck = [
                i for i in set(projIDcurrent) if i in self.rawprojID]

            taxaIDcheck =[
                i for i in set(taxaIDcurrent) if i in self.rawtaxaID]
        except Exception as e:
            print(str(e))

        finally:
            boolist = []
            boolist.append(len(list(projIDcheck))==0)
            boolist.append(len(list(taxaIDcheck))==0)
            session.close()
            return boolist
        


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

        elif self.table == 'maintable':
            try:
                tabletopushto = str(
                    self.config.maintable.__table__.name)
            except Exception as e:
                print(str(e))

        elif self.table == 'taxatable':
            try:
                tabletopushto = str(
                    self.config.taxatable.__table__.name)
            except Exception as e:
                print(str(e))

        elif self.table == 'rawtable':
            try:
                tabletopushto = str(
                    self.config.rawtable.__table__.name)
            except Exception as e:
                print(str(e))
        else:
            pass

        # Try command to push the
        # table created in the previous steps
        # to the database.
        try:
            self.data.to_sql(
                tabletopushto, con=self.config.engine,
                if_exists="append", index=False)
        except Exception as e:
            print(str(e))
