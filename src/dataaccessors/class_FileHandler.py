#!usr/bin/env python
import os
import pandas as pd
import collections

class FileHandler(object):
    """    
    FileHandler is a class that will take a user selected
    file, identify the extension, and load the data as an
    instance of a pandas dataframe.

    Keyword Arguments
    -----------------
    filetoload: string (file to be loaded)
    uniquefilekey: boolean
    sheet: integer
    topskiplines: integer or integer range (0- index)
    bottomskiplines:integer (0 default)
    delimitchar: characters or regular expression
    """
    
    ext_error = 'File to upload has no extension'
    file_error = 'Could not read file specified. Please recheck file.'
    get_info = collections.namedtuple('get_info', 'name ext uq')
    
    def __init__(self, filetoload=None, uniquefilekey=0, **kwargs):
        self.filetoload = filetoload
        self.uniquefilekey = uniquefilekey
        self.sheet = kwargs.pop('sheet', None)
        self.topskiplines = kwargs.pop('topskiplines', None)
        self.bottomskiplines = kwargs.pop('bottomskiplines', 0)
        self.delimitchar = kwargs.pop('delimitchar', None)
        self._datacontainer = {}

        self.readoptions = {
            '.csv': pd.read_csv,
            '.xlsx': pd.read_excel,
            '.xls': pd.read_excel,
            '.txt': pd.read_table
        }

        self.inputoptions = {
            '.csv': 'self.filetoload',
            '.xlsx': 'self.filetoload, sheet=self.sheet',
            '.xls': 'self.filetoload, sheet=self.sheet',
            '.txt': (
                'self.filetoload, skiprows=self.topskiplines' +
                ' skipfooter=self.bottomskiplines' +
                'delimiter=self.delimitchar, error_bad_lines=False')
        }

    @property
    def file_id(self):
        '''
        extension property based on the user inputs
        '''
        if self.filetoload is None:
            return None
        else:
            try:
                assert self.uniquefilekey > 0
            except:
                raise AssertionError('Please enter a unique data key')
            try:
                filename, ex = os.path.splitext(self.filetoload)
                if '.' in ex:
                    return self.get_info(
                        name=filename, ext=ex, uq=self.uniquefilekey)

                else:
                    raise IOError(self.ext_error)
            except:
                raise IOError(self.ext_error)

    def set_data(self):
        '''
        Adding a method to set the protected data
        attribute. Three criteria must be met for an attempted
        set method to proceed.
        '''

        if self.filetoload is None:
            raise AttributeError(
                'You have not specified a file to upload')

        elif self.file_id.ext not in ('.csv', '.txt', '.xlsx', '.xls'):
            raise IOError('Can not open file type')

        elif self.file_id.ext is not None:
            try:
                assert self.uniquefilekey > 0
            except:
                raise AssertionError(
                    'Please enter a unique data key.')
            try:
                self._datacontainer[
                    self.file_id] = self.readoptions[
                        self.file_id.ext](eval(
                            self.inputoptions[self.file_id.ext]))
            except:
                raise IOError(self.file_error)
