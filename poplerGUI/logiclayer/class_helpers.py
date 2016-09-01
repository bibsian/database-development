#! /usr/bin/env python
from pandas import  DataFrame, concat
import re
from numpy import where
from collections import OrderedDict
from itertools import chain

__all__ = [
    'string_to_list', 'strip_time', 'year_strip', 'extract',
    'check_int', 'produce_null_df', 'check_registration',
    'UniqueReplace', 'updated_df_values', 'write_column_to_log']

def string_to_list(userinput):
    '''
    Function to take a string with names separated by
    commas and turn that into a list of names
    '''
    strtolist = re.sub(
        ",\s", " ", userinput.rstrip()).split()
    return strtolist


def strip_time(data, col):
    '''
    Method to remove delimiter from date time data columns
    '''
    strippedlist = []
    for i in list(set(col)):
        strippedlist.append([
            re.sub("/|,|-|;"," ", x) for x in list(
                data[i].astype(str))])
    return strippedlist

def year_strip(dateformat):
    '''
    Takes a string specifying a date format and then extracts the
    year format for help with processing.----DELETE?
    '''
    f = dateformat
    found = re.search('Y+', f)
    ylength = len(found.group(0))
    return ylength

def extract(d,keys):
    ''' returns subset of dictionary based on list of keys'''
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

    allnulls = concat(
        [DataFrame(
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
    ''' 
    Class to perform the work of returning a dataframe with unique
    combinations of factors from 'x' number of columns
    '''
    def __init__(self, dataframe, clsinstance):
        self._data = dataframe.copy()
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

    def replace_levels(
            self, modifiedlevelname, allotherlevels=None):
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
                'To replace values input only one column' +
                ' name.')

        self.modified = modifiedlevelname
        self.original = self._data[self.lookup].drop_duplicates()
        og_list = self.original[self.lookup].values.tolist()
        if any(isinstance(i, list) for i in og_list):
            og_list = list(chain.from_iterable(og_list))
        else:
            pass

        level_name_changed_from = [
            x for x in og_list if x not in allotherlevels]
        print(level_name_changed_from, self.modified)

        try:
            assert (
                len(self.modified) == len(level_name_changed_from))

            self._data = self._data.replace(
                {self.lookup[0]: {
                    level_name_changed_from[0]: self.modified[0]}},
            )
            return self._data

        except Exception as e:
            print(str(e))
            raise AttributeError('Too many levels to replace')
        return self._data

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
    if (len(olddataframe) == 0 or
        olddataframe is None or
        len(olddataframe.columns) == 0):
        logger.info('{} "{}"'.format(
            name,
            'NULL'))
    else:

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

def write_column_to_log(dictionary, logger, tablename):
    '''
    Function to data a dictionary of column headers/entries,
    turn it into a dataframe, and log the entries as
    a function to the name.
    '''
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


