#!/usr/bin/env python
import pandas as pd
import numpy as np

class ColumnToDictionaryFrame():
    '''
    This class will convert a dataframe (given a list of columns)
    into a dataframe of json types where each row is a json
    data type of all observations from the columns in that row
    '''
    def __init__(self, dataframe, columnlist):
        self.data = dataframe
        self.names = list(columnlist)
        self.ncols = np.shape(dataframe)[1]
        self.nrows = np.shape(dataframe)[0]

    # Method to return the json dataframe
    def dict_df(self):
        self.jsonlist = []
        try:
            self.dictstartseq = [
                {self.data[self.names].columns[i]:None
                 for i,item in enumerate(self.names)}]

        except:
            raise AttributeError

        self.dictlist = [
            (self.dictstartseq[0]).copy() for x in range(self.nrows)]

        for col in self.names:
            for i in range(self.nrows):
                self.dictlist[i][col] = str(self.data[col].iloc[i])

        self.dictdf = pd.DataFrame(
            {'covariate': self.dictlist})
        self.dictdf['covariate'] = self.dictdf['covariate'].astype(str)

        return self.dictdf
