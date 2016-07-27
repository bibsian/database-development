#! /usr/bin/env python
import pytest
from pandas import read_sql, read_csv
from collections import namedtuple


import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/" +
        "test/")
    end = "/"

elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Dropbox\\database-development" +
        "\\test\\")
    end = "\\"
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath + 'logiclayer' + end)))
import datalayer.config as orm
os.chdir(rootpath)




@pytest.fixture
def Merger():
    class Merger(object):
        tabletuple = namedtuple(
            'TableData', 'orm pkey filterer identifier')
        
        def __init__(self, globalid):
            self.globalid = globalid
            self.tableq = {
                'maintable': self.tabletuple(
                    orm.Maintable,
                    orm.Maintable.lter_proj_site,
                    orm.Maintable.siteid,
                    orm.Maintable.metarecordid  
                ),
                'taxatable': self.tabletuple(
                    orm.Taxatable,
                    orm.Taxatable.taxaid,
                    orm.Taxatable.lter_proj_site,
                    None
                )
            }
            self.rawmain = None
            self.maintaxa = None

        def query_database(self, tablename, tablefilterlist):
            '''
            General method to query the database tables
            by indexing primary keys and filerting results
            with a instance specific list of filters (tablefilter)
            '''
            table = self.tableq[tablename]
            session = orm.Session()
            if tablename == 'maintable':
                query = (
                    session.query(table.orm).
                    order_by(table.pkey).
                    filter(table.filterer.in_(tablefilterlist)).
                    filter(table.identifier == self.globalid)
                )
            elif tablename == 'taxatable':
                query = (
                    session.query(table.orm).
                    order_by(table.pkey).
                    filter(table.filterer.in_(tablefilterlist))
                )
            session.close()
            querydf = read_sql(
                query.statement, query.session.bind)
            return querydf

        
    return Merger

@pytest.fixture
def df():
    return read_csv('Datasets_manual_test/raw_data_test.csv')

# This test will only work if the test data set is loaded into the
# database with metarecordid as '2'
# and the informaotin is at least filled out up to the taxatable
def test_query(Merger, df):
    merge1 = Merger(2)
    sitefilter = ['Site1', 'Site2', 'Site3']
    mainquery = merge1.query_database('maintable', sitefilter)
    print(mainquery)
    assert (
        (list(set(mainquery['siteid'].values.tolist())).sort() ==
         sitefilter.sort())
        is True)
    
    
    
