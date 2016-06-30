#!/usr/bin/env python
import pandas as pd

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
        self.data = pd.DataFrame(dataframe)
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
        try:
            # Creating a separte dictionary for each column
            # and adding to list
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

        self.dictdf = pd.DataFrame(
            {'covariates': self.dictlist})
        self.dictdf['covariates'] = self.dictdf[
            'covariates'].astype(str)

        return self.dictdf
