#!usr/bin/env python
import pandas as pd
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import re
from numpy import where
from collections import OrderedDict

def strip_time(data, col):
    strippedlist = []
    for i in list(set(col)):
        strippedlist.append([
            re.sub("/|,|-|;"," ", x) for x in list(
                data[i].astype(str))])
    return strippedlist

def year_strip(dateformat):
    '''
    Takes a string specifying a date format and then extracts the
    year format for help with processing.
    '''
    f = dateformat
    found = re.search('Y+', f)
    ylength = len(found.group(0))
    return ylength

def extract(d,keys):
    ''' return subset of dictionary based on list of keys'''
    return OrderedDict((k, d[k]) for k in d if k in keys)

def check_int(x):
    ''' function to check if text can be converted to integer'''
    try:
        int(x)
        return True
    except ValueError:
        return False


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

def check_registration(clss, inputname):
    '''
    Helper funciton to make sure the input handler was registered
    with the facade class before trying operations.

    ONLY FOR USE IN FACADE CLASS!!!!!!!
    '''
    try:
        assert clss._inputs[inputname].name == inputname
    except Exception as e:
        print(str(e))
        raise ValueError('Input Not Registered')


class UniqueReplace(object):
    ''' Class to perform the work of returning unique
    combinations of levels given 'n' number of columns
    '''
    def __init__(self, dataframe, clsinstance):
        self._data = pd.DataFrame(dataframe)
        self.userinput = clsinstance
        self.lookup = list(clsinstance.lnedentry.values())
        self.levels = None
        self.original = None
        self.modified = None

    def get_levels(self):
        '''
        Returns pandas dataframe with unique combination of
        levels
        '''
        try:
            self.levels = self._data[
                self.lookup].drop_duplicates().sort_values(
                    self.lookup).reset_index(drop=True)
            return self.levels
        except Exception as e:
            print(str(e))
            raise LookupError('Invalid column names')

    def replace_levels(self, usermodifiedlist):
        '''
        Takes a modified list of factor level labels and converts
        the original labels in the dataframe into
        the modified labels.
        '''
        try:
            assert len(self.lookup) == 1
        except Exception as e:
            print(str(e))
            raise AssertionError(
                'To replace values to must input only one column' +
                ' name.')

        if self.levels is not None:
            self.original = self.levels[self.lookup].values.tolist()
            self.modified = usermodifiedlist
            tochange = [
                [x, y] for x, y in zip(
                    self.original, self.modified) if x != y]
            fromlist = []
            tolist = []
            for i,item in enumerate(tochange):
                fromlist.append(item[0])
                tolist.append(item[1])
            return self._data.replace(fromlist, tolist)

        else:
            raise AssertionError(
                'Must use get_levels method before replacing' +
                ' values.')

    def replace_values(self):
        '''
        takes a list of values to change
        '''

        try:
            if check_int(
                    self.userinput.lnedentry['from']) is True:

                modified = self._data.replace(
                    int(self.userinput.lnedentry['from']),
                    self.userinput.lnedentry['to'])

                return modified

            else:
                pass

        except Exception as e:
            print(str(e))
            raise LookupError('InputHandler key error')

        finally:
            modified = self._data.replace(
                self.userinput.lnedentry['from'],
                self.userinput.lnedentry['to'])

            return modified

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

