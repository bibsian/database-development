#! /usr/bin/env python
import pytest
from pandas import concat, DataFrame, read_csv, to_numeric, wide_to_long
from numpy import where
import re
import decimal as dc
import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/")
    end = "/"

elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development")
    end = "\\"
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath + 'logiclayer' + end)))
from poplerGUI.logiclayer import class_logconfig as log
from poplerGUI.logiclayer.datalayer import config as orm
os.chdir(rootpath)


def test_wide_to_long_(df_test_6):
    data = df_test_6
    data['id'] = data.index
    new = wide_to_long(
        data, ["trait", "growth"], i="id", j="year")
    print(new)
    assert ("growth" in new.columns.values.tolist()) is True
    assert ("trait" in new.columns.values.tolist()) is True


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

        allnulls = concat(
            [DataFrame(
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
    Note null value MUST be folled by space
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


def test_decimal(decimal_df_col, df_test_2):
    print(df.dtypes)
    decimal_df_col(df, 'DENSITY')
    print(df)
    print(df.dtypes)


@pytest.fixture
def updated_df_values():
    def updated_df_values(olddataframe, newdataframe, logger, name):
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
        if (
                len(olddataframe) == 0 or
                olddataframe is None or
                len(olddataframe.columns) == 0
        ):
            logger.info('{} "{}"'.format(
                name,
                'NULL'))
        else:
            diffdf = (olddataframe != newdataframe)
            for i, item in enumerate(diffdf.columns):
                if any(diffdf[item].values.tolist()):
                    index = where(diffdf[item].values)[0].tolist()
                    logger.info('{} "{}" = {} to {}'.format(
                        name,
                        item,
                        olddataframe.loc[index, item].values.tolist(),
                        newdataframe.loc[index, item].values.tolist()))
                else:
                    pass
    return updated_df_values


@pytest.fixture
def mylog():
    mylog = log.configure_logger(
        'tableformat',
        rootpath + end +' logs/test_df_diff.log'
    )
    return mylog

@pytest.fixture
def metadf_og():
    if sys.platform == "darwin":
        metapath = (
            rootpath + end + 'test' + end + 'Datasets_manual_test' +
            "/meta_file_test.csv")
    elif sys.platform == "win32":
        #=======================#
        #Paths to data and conversion of files to dataframe
        #=======================#
        metapath = (
            rootpath + end + 'test' + end + 'Datasets_manual_test' +
            "/meta_file_test.csv")

    metadf = read_csv(metapath, encoding="iso-8859-11")
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
    df = read_csv('DatabaseConfig/main_table_test.csv')
    return df

@pytest.fixture
def convert_typetest():
    def convert(dataframe, types):
        for i in dataframe.columns:
            if types[i] in ['NUMERIC', 'INTEGER', 'Integer']:
                dataframe[i] = to_numeric(
                    dataframe[i], errors='coerce')
            elif types[i] in ['VARCHAR', 'TEXT']:
                dataframe[i] = dataframe[i].astype(object)
    return convert

def test_convert_types(maindf, convert_typetest):
    print(maindf.dtypes)
    convert_typetest(maindf, orm.maintypes)
    print(maindf.dtypes)

@pytest.fixture
def year_strip():
    def year_strip(dateformat):
        f = dateformat
        found = re.search('Y+', f)
        ylength = len(found.group(0))
        return ylength
    return year_strip
    
def test_year_strip(year_strip):
    y2 = 'dd - mm - YY (Any Order)'
    y4 = 'dd - mm - YYYY (Any Order)'
    ym2 = 'mm - YY (Any Order)'
    ym4 = 'mm - YYYY (Any Order)'
    y = 'YYYY'
    assert (year_strip(y2) == 2) is True
    assert (year_strip(ym2) == 2) is True
    assert (year_strip(ym4) == 4) is True
    assert (year_strip(y4) == 4) is True
    assert (year_strip(y) == 4) is True

@pytest.fixture
def write_column_to_log(produce_null_df, updated_df_values):
    def write_column_to_log(dictionary, logger, tablename):
        coldf = DataFrame([dictionary])
        nulldf = produce_null_df(
            len(coldf.values.tolist()),
            coldf.columns.values.tolist(),
            len(coldf),
            'NULL'
        )
        
        updated_df_values(
            nulldf, coldf, logger, tablename
        )
    return write_column_to_log

def test_write_column(write_column_to_log, mylog):
    testdict = {'columnname':'uniquevalue'}
    write_column_to_log(testdict, mylog, 'testtable')

@pytest.fixture
def date_strip():
    return read_csv('Datasets_manual_test/raw_data_test_dialogsite.csv')

@pytest.fixture
def date_strip_test5():
    return read_csv('Datasets_manual_test/raw_data_test_5.csv')

@pytest.fixture
def strip_time():
    '''
    Function to strip a single date time column
    with all potential delimiters (leaving a space
    where the delimiter used to be). This is necessary
    to standardize the data enabling the effective use
    of the pandas as_datetime method.
    '''
    def strip_time(data, col):
        strippedlist = []
        for i in list(set(col)):
            print([
                re.sub("/|,|-|;"," ", x) for x in list(
                    data[i].astype(str))])
            strippedlist.append([
                re.sub("/|,|-|;"," ", x) for x in list(
                    data[i].astype(str))])

        return strippedlist

    return strip_time

def test_strip_time(date_strip, strip_time):
    test = strip_time(date_strip, ['DATE'])
    assert isinstance(test, list) is True

def test_strip_time_test5(date_strip_test5, strip_time):
    Single columns are going to give back nested list
    test = strip_time(date_strip_test5, ['YEAR'])
    print(test)
    assert isinstance(test, list) is True

@pytest.fixture
def string_to_list():
    def string_to_list(userinput):
        strtolist = re.sub(
            ",\s", " ", userinput.rstrip()).split()
        return strtolist

    return string_to_list

def test_string_to_list(string_to_list):
    teststring = 'DEPTH, REP, TEMP'
    test = string_to_list(teststring)
    print(test)
    assert isinstance(test, list) is True
