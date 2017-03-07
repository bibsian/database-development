#!/usr/bin/env python
import pytest
from pandas import read_csv, DataFrame
import sys, os
rootpath = os.path.dirname(os.path.dirname(os.path.dirname( __file__ )))
end = os.path.sep

@pytest.fixture
def DictionaryDataframe():
    
    class DictionaryDataframe():
        '''
        Class that takes 'x' number of columns with covariate
        information, converts records in each column (x) 
        into a string with containing the records for all
        columns (x), in the row of the dataframe input. The string
        it makes has a python dictionary format. Class return a pandas
        dataframe with the coverted information. 

        This is the most elegant way I thought of to concatenate
        a lot of info (of varying sizes) into something that we 
        can unpack in the R package.
        '''
        def __init__(self, dataframe, columnlist):
            self.data = DataFrame(dataframe)
            self.names = list(columnlist)
            self.ncols = len(dataframe.columns.values.tolist())
            self.nrows = len(dataframe)
            self.dictstartseq = None
            self.dictlist = None
            self.dictdf = None
            
        def convert_records(self):
            '''
            actual method that converts column records into strings
            '''
            if self.names[0] != '':
                try:
                    # Creating a separte dictionary for each column
                    # and adding to list
                    try:
                        self.dictstartseq = [
                            {self.data[self.names].columns[i]:None
                             for i,item in enumerate(self.names)}]
                    except Exception as e:
                        self.names = [int(x) for x in self.names]
                        self.dictstartseq = [
                            {self.data[self.names].columns[i]:None
                             for i,item in enumerate(self.names)}]
                except:
                    raise AttributeError(
                        'Count not verify column names')

                self.dictlist = [
                    (self.dictstartseq[0]).copy()
                    for x in range(self.nrows)]

                for col in self.names:
                    for i in range(self.nrows):
                        self.dictlist[i][col] = str(self.data[col].iloc[i])

                self.dictdf = DataFrame(
                    {'covariates': self.dictlist})
                self.dictdf['covariates'] = self.dictdf[
                    'covariates'].astype(str)
            else:
                self.dictdf = DataFrame(
                    {'covariates': ['NA' for i in range(self.nrows)]})
                self.dictdf['covariates'] = self.dictdf[
                    'covariates'].astype(str)

            return self.dictdf

    return DictionaryDataframe


@pytest.fixture
def df():
    return read_csv(
        rootpath + end + "test" + end +
        'Datasets_manual_test/raw_data_test_1.csv'
    )

def test_dictionarydataframe(df, DictionaryDataframe):

    columnstocombine = ['temp', 'blank', 'spelling']
    test = DictionaryDataframe(df, columnstocombine)
    testdf = test.convert_records()
    print(testdf)
    assert (isinstance(testdf, DataFrame)) is True
    assert (isinstance(testdf.iloc[0], object)) is True
    testseries = testdf['covariates'].astype(str)
    assert (isinstance(testseries.iloc[0], str)) is True
    assert ('temp' in testseries.iloc[0]) is True
    assert ('blank' in testseries.iloc[0]) is True
    assert ('spelling' in testseries.iloc[0]) is True
    assert (len(df) == len(testseries)) is True
    assert (
        len(df.columns.values.tolist()) !=
        len(testseries.name)) is True
        

def test_dictionarydataframe_NA_values(df, DictionaryDataframe):

    columnstocombine = ['']
    test = DictionaryDataframe(df, columnstocombine)
    testdf = test.convert_records()
    print(testdf)
    assert (isinstance(testdf, DataFrame)) is True
    assert (isinstance(testdf.iloc[0], object)) is True
    testseries = testdf['covariates'].astype(str)
    assert (isinstance(testseries.iloc[0], str)) is True
    assert ('NA' in testseries.iloc[0]) is True
    assert (len(df) == len(testseries)) is True
    assert (
        len(df.columns.values.tolist()) !=
        len(testseries.name)) is True
        


