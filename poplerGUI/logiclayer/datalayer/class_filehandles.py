#! /usr/bin/env python
import os
from pandas import read_csv, read_excel, read_table, DataFrame
from collections import namedtuple

__all__ = ['FileHandler', 'FileCaretaker', 'FileMemento', 'DataProxy']

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
    get_info = namedtuple(
        'get_info', 'name ext version')

    state = 'original'

    def __init__(self, inputclsinstance):
        self.filetoload = inputclsinstance.filename
        if inputclsinstance.lnedentry['sheet'] is not '':
            self.sheet = inputclsinstance.lnedentry['sheet']
        else:
            self.sheet = None
        if inputclsinstance.lnedentry['tskip'] is not '':
            self.topskiplines = int(inputclsinstance.lnedentry[
                'tskip'])
        else:
            self.topskiplines = None

        if inputclsinstance.lnedentry['bskip'] is not '':
            self.bottomskiplines = int(inputclsinstance.lnedentry[
                'bskip'])
        else:
            self.bottomskiplines = 0

        if inputclsinstance.lnedentry['delim'] is not '':
            self.delimitchar = inputclsinstance.lnedentry[
                'delim']
        else:
            self.delimitchar = '\t'

        if inputclsinstance.checks is True:
            self.header = -1
        else:
            self.header = 'infer'

        self._data = None
        self.inputoptions = {
            '.csv': {
                'filename':self.filetoload
            },
            '.xlsx': {
                'filename':self.filetoload,
                'sheet':self.sheet
            },
            '.txt': {
                'filename': self.filetoload,
                'skiprows': self.topskiplines,
                'skipfooter': self.bottomskiplines,
                'delimiter': self.delimitchar,
                'header': self.header
            }
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
                filename, ex = os.path.splitext(self.filetoload)
                if '.' in ex:
                    print('filename (class): ', filename, ex)
                    return self.get_info(
                        name=filename, ext=ex, version=self.state)

                else:
                    raise IOError(self.ext_error)
            except:
                raise IOError(self.ext_error)


    def create_memento(self):
        '''
        Adding a method to set the protected data
        attribute. Three criteria must be met for an attempted
        set method to proceed. Additionally strip trailing
        white space from all columns that could be strings
        '''

        if self.filetoload is None:
            raise AttributeError(
                'No file selected')
        elif self.file_id.ext not in ('.csv', '.txt', '.xlsx', '.xls'):
            raise IOError('Can not open file type')

        elif self.file_id.ext is not None:
            try:
                if self.file_id.ext == '.csv':
                    dfstate = read_csv(
                        self.inputoptions[
                            '.csv']['filename']
                        )
                elif (
                        self.file_id.ext == '.xls' or
                        self.file_id.ext == '.xlsx'):
                    dfstate = read_excel(
                        self.inputoptions[
                            'xlsx']['filename'],
                        sheetname=self.inputoptions[
                            'xlsx']['sheet']
                        )
                elif self.file_id.ext == '.txt':
                    dfstate = read_table(
                        self.inputoptions[
                            '.txt']['filename'],
                        delimiter=self.inputoptions[
                            '.txt']['delimiter'],
                        skiprows=self.inputoptions[
                            '.txt']['skiprows'],
                        header=self.inputoptions[
                            '.txt']['header'],
                        error_bad_lines=False,
                        engine='c'
                        )
                print('read with options')

                for i, item in enumerate(dfstate.columns):
                    if isinstance(
                            dfstate.dtypes.values.tolist()[i],
                            object):
                        try:
                            dfstate.loc[:, item] = dfstate.loc[
                                :,item].str.rstrip()
                            
                            na_vals = [
                                9999, 99999, 999999,
                                -9999, -99999, -999999,
                                -8888, -88888, -88888, -888
                            ]
                            na_vals_float = [
                                9999.0, 99999.0, 999999.0,
                                -9999.0, -99999.0, -999999.0
                                -8888.0, -88888.0, -888888.0,
                                -888.0
                            ]
                            na_text_vals = [
                                '9999', '99999', '999999',
                                '-9999', '-99999', '-999999',
                                '-8888', '-88888', '-888888',
                                '-888'
                            ]
                            for j,text_val in enumerate(
                                    na_text_vals):
                                if (
                                        (
                                            dfstate[item].dtypes
                                            == int)
                                        or
                                        (
                                            dfstate[item].dtypes
                                            == float)):
                                    dfstate[item].replace(
                                        {na_vals[j]: 'NA'},
                                        inplace=True)
                                    dfstate[item].replace(
                                        {na_vals_float[j]: 'NA'},
                                        inplace=True)
                                else:
                                    dfstate[item].replace(
                                        {text_val: 'NA'},
                                        inplace=True)
                        except:
                            pass
                    else:
                            pass
                dfstate.fillna('NA',inplace=True)
                memento = FileMemento(dfstate= dfstate,
                            state= self.state)
                return memento

            except Exception as e:
                print(str(e))
                raise IOError(self.file_error)

    def set_data(self, instFileCaretaker, state):
        self._data = instFileCaretaker.restore_memento(state)


class FileCaretaker(object):
    '''Caretaker for state of dataframe'''
    def __init__(self):
        self.__statelogbook = {}

    def save_to_memento(self, memento):
        ''' 
        Saves memento object with a dictionary
        recording the state name and the dataframe state
        '''
        self.__statelogbook[
            memento.get_state()] = memento.get_dfstate()

    def restore_memento(self, state):
        '''
        Restores a memento given a state_name
        '''
        try:
            return self.__statelogbook[state]
        except Exception as e:
            print(str(e))

class FileMemento(object):
    '''
    Memento Class. This simply records the
    state of the data and gives it to the 
    FileCaretaker
    '''

    def __init__(self, dfstate, state):
        self.__dfstate = DataFrame(dfstate)
        self.__state = str(state)

    def get_dfstate(self):
        return self.__dfstate

    def get_state(self):
        return self.__state


class DataProxy(FileHandler):
    def __init__(self, df, state):
        self._data = df
        self._state = state

    def create_memento(self):
        try:
            assert self._data is not None 
        except Exception as e:
            print(str(e))
            raise AttributeError('Data has not been set')
        memento = FileMemento(self._data, self._state)
        return memento
