#usr/bin/env python
import pytest
import pandas as pd
from numpy import where
import re
import decimal as dc
import config as cfig
import class_logconfig as log
from sys import platform as _platform
import config as orm

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
    ''' test integer checker'''
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
    '''test null df generator'''
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


@pytest.fixture
def decimal_df_col():
    def decimal_df_col(dataframe, colname):
        dataframe[colname].apply(dc.Decimal)
        return dataframe
    
    return decimal_df_col

@pytest.fixture
def df():
    return pd.read_csv('site_table_test.csv')

def test_decimal(decimal_df_col, df):
    print(df.dtypes)
    decimal_df_col(df, 'lat')
    decimal_df_col(df, 'lng')
    print(df)
    print(df.dtypes)
#    cfig.session.bulk_insert_mappings(
#    cfig.Sitetable,
#        [df.iloc[i,:].to_dict() for i in range(len(df))])
#    cfig.session.commit()

@pytest.fixture
def updated_df_values():
    def updated_df_values(olddataframe,newdataframe,logger, name):
        '''
        Helper function to aid in logging the difference between
        dataframes after user have modified the entries.
        For example, inputing latitude and longitude for the site
        table or the extent of spatial replication in the main table.
        
        Arguments:
        olddataframe = An unmodified dataframe
        newdataframe = A user modified dataframe
        logger = An instance of a logger handler
        table = A string with the name to append to log
        '''
        try:
            assert (
                olddataframe.columns.values.tolist() ==
                newdataframe.columns.values.tolist()) is True
        except Exception as e:
            print(str(e))
            raise AttributeError(
                'Dataframe columns are not equivalent')
        diffdf = (olddataframe != newdataframe)
            
        for i,item in enumerate(diffdf.columns):
            if any(diffdf[item].values.tolist()):
                index = where(diffdf[item].values)[0].tolist()
                logger.info('{} "{}" = {} to {}'.format(
                    name,
                    item,
                    olddataframe.loc[index,item].values.tolist(),
                    newdataframe.loc[index,item].values.tolist()))
            else:
                pass
    return updated_df_values

@pytest.fixture
def old():
    old = pd.read_csv('DataRawTestFile.csv')
    return old

@pytest.fixture
def new(old):
    new = old.copy()
    cols = list(new.columns)
    new.loc[1,cols[2]] = 'Change1'
    new.loc[2,cols[5]] = 'Change2'
    new.loc[3,cols[4]] = 'Change3'
    return new

@pytest.fixture
def mylog():
    mylog = log.configure_logger(
        'tableformat', 'Logs_UI/test_df_diff.log')
    return mylog

@pytest.fixture
def metadf_og():
    if _platform == "darwin":
        metapath = (
            "/Users/bibsian/Dropbox/database-development/data" +
            "/meta_file_test.csv")
            
    elif _platform == "win32":
        #=======================#
        # Paths to data and conversion of files to dataframe
        #=======================#
        metapath = (
            "C:\\Users\MillerLab\\Dropbox\\database-development" +
            "\\data\\meta_file_test.csv")

    metadf = pd.read_csv(metapath, encoding="iso-8859-11")
    return metadf

@pytest.fixture
def metadf_mod(metadf_og):
    new = metadf_og.copy()
    new.loc[3, 'treatment_type'] = 'maybe...'
    return new

def test_logger_and_df_diff(updated_df_values, mylog, old, new):
    updated_df_values(old, new, mylog, 'maintable')

def test_logger_and_metadf_diff(
        updated_df_values, mylog, metadf_og, metadf_mod):
    print(metadf_og.columns)
    print(metadf_og.dtypes)
    print('---------------')
    print(metadf_mod.columns)
    print(metadf_mod.dtypes)
    print('----------------')
    updated_df_values(metadf_og, metadf_mod, mylog, 'maintable')


@pytest.fixture
def maindf():
    df = pd.read_csv('DatabaseConfig/main_table_test.csv')
    return df

@pytest.fixture
def convert_typetest():
    def convert(dataframe, types):
        for i in dataframe.columns:
            if types[i] in ['NUMERIC', 'INTEGER', 'Integer']:
                dataframe[i] = pd.to_numeric(
                    dataframe[i], errors='coerce')
            elif types[i] in ['VARCHAR', 'TEXT']:
                dataframe[i] = dataframe[i].astype(object)
    return convert

def test_convert_types(maindf, convert_typetest):
    print(maindf.dtypes)
    convert_typetest(maindf, orm.maintypes)
    print(maindf.dtypes)

