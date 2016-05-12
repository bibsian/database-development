#usr/bin/env python
import pytest
import pandas as pd
import re

@pytest.fixture
def check_int():
    def check_int(x):
        ''' helper function to check if text can be converted to int'''
        try:
            int(x)
            return True
        except ValueError:
            return False

    return check_int

def test_int_check(check_int):
    assert check_int('4') is True
    assert check_int('word') is False

@pytest.fixture
def produce_null_df():
    def produce_null_df(ncols, colnames, dflength, nullvalue):
        ''' 
        Helper function to create a dataframe of null
        values for concatinating with formated data
        '''
        try:
            list(colnames)
            int(ncols)
            int(dflength)
            str(nullvalue)
        except Exception as e:
            print(str(e))
            ValueError('Invalid data types for arguments')

        p = re.compile('\w+\s')
        matches = p.match(nullvalue)
        if matches is None:
            nullvalue = (nullvalue + ' ')

        allnulls = pd.concat(
            [pd.DataFrame(
                re.sub(' ', ' ', (str(nullvalue)*dflength)).split())]*
            len(colnames), axis=1)
        allnulls.columns = colnames
        return allnulls

    return produce_null_df

def test_nulldf(produce_null_df):
    n = 2
    colnames = ['c1', 'c2']
    dflen = 5
    # Note null value MUST be folled by space
    null = 'NULL'

    testdf = produce_null_df(n, colnames, dflen, null)
    print(testdf)
    assert (list(testdf.columns) == colnames) is True
    assert ('NULL' in testdf.values) is True
    assert ('NULL' not in testdf.values) is False
    assert (1 not in testdf.values) is True
    assert ('x' not in testdf.values) is True
    assert (len(testdf) == dflen) is True