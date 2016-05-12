#!usr/bin/env python
import pytest
import pandas as pd
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))

class OneToMany(object):
    '''
    Class to split one column with words are records into multiple
    columns with each word being a unqiue column. This class
    also has methods to display any records which may raise
    errors in pandas. Can edit is observation view and 
    then retry the split.
    '''

    state = 'onetomany'

    def __init__(self, dataframe, colname, ncol, names):
        self.df = pd.DataFrame(dataframe.copy())
        self.colname = str(colname)
        self.ncol = int(ncol)
        self.names = list(names)
        self.lengthlist = None
        
    def do(self):
        '''
        Method to split the words in column records into
        multiple columns. 
        '''
        if self.colname in self.df.columns:
            pass
        else:
            raise KeyError('Column not located.')

        try:
            assert self.ncol == len(self.names)
        except:
            raise AssertionError(
                'Number to split by and column names to add ' +
                'do not match.')

        # Check for word length mismatches in records
        self.lengthlist = self.df['splitme'].str.split().apply(len)

        if all(self.lengthlist == self.ncol) is True:
            pass
        else:
            raise LookupError(
                'Words to split are not equal across records.')

        print(self.df[self.colname].str.len())
        splitdf = self.df[self.colname].str.split(expand=True)
        splitdf.columns = self.names
        print(pd.concat([self.df, splitdf], axis=1))

    def display_mod(self):
        '''
        Methods to return the records that are NOT consistent
        with how the one to many should split records. Also
        can return records that are consistent
        '''
        print(self.df.loc[
            self.lengthlist.loc[
                self.lengthlist==self.ncol].index, self.colname])

        print(self.df.loc[
            self.lengthlist.loc[
                self.lengthlist!=self.ncol].index, self.colname])


@pytest.fixture
def df():
    return pd.read_csv('DataRawTestFile.csv')

def test_onetomany_failures(df):
    # Wrong column location
    test = OneToMany(df, 'lsls', 2, ['genus', 'species'])
    with pytest.raises(KeyError):
        test.do()

    # Wrong column location
    test = OneToMany(df, 'splitme', 1, ['genus', 'species'])
    with pytest.raises(AssertionError):
        test.do()

    # Right column location records not equal across dataframe
    test = OneToMany(df, 'splitme', 2, ['genus', 'species'])
    with pytest.raises(LookupError):
        test.do()
    print(test.display_mod())

    
