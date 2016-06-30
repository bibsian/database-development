import pytest
import pandas as pd
from collections import namedtuple
import config as orm

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
                    orm.Maintable.projid,
                    orm.Maintable.siteid,
                    orm.Maintable.metarecordid  
                ),
                'taxatable': self.tabletuple(
                    orm.Taxatable,
                    orm.Taxatable.taxaid,
                    orm.Taxatable.projid,
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
            if tablename == 'maintable':
                query = (
                    orm.session.query(table.orm).
                    order_by(table.pkey).
                    filter(table.filterer.in_(tablefilterlist)).
                    filter(table.identifier == self.globalid)
                )
            elif tablename == 'taxatable':
                query = (
                    orm.session.query(table.orm).
                    order_by(table.pkey).
                    filter(table.filterer.in_(tablefilterlist))
                )
            querydf = pd.read_sql(
                query.statement, query.session.bind)
            return querydf

        
    return Merger

@pytest.fixture
def df():
    return pd.read_csv('raw_data_test.csv')

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
    
    
    
