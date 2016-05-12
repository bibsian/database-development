#!usr/bin/env python
import pytest
import os
import pandas as pd
import collections
import gc
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import class_inputhandler as ini


@pytest.fixture
def FileHandler(FileMemento):
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
        get_info = collections.namedtuple(
            'get_info', 'name ext version')

        state = 'original'

        def __init__(self, inputclsinstance):
            self.filetoload =  inputclsinstance.filename
            if 'sheet' in inputclsinstance.lnedentry.values():
                
                self.sheet =  inputclsinstance.lnedentry['sheet']
            else:
                self.sheet = None
            
            self.topskiplines =  inputclsinstance.lnedentry['tskip']
            self.bottomskiplines =  inputclsinstance.lnedentry['bskip']
            self.delimitchar =  inputclsinstance.lnedentry['delim']
            self._data = None
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
                    filename, ex = os.path.splitext(self.filetoload)
                    if '.' in ex:
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
            set method to proceed.
            '''

            if self.filetoload is None:
                raise AttributeError(
                    'No file selected')
            elif self.file_id.ext not in ('.csv', '.txt', '.xlsx', '.xls'):
                raise IOError('Can not open file type')

            elif self.file_id.ext is not None:
                try:
                    memento = FileMemento(dfstate= self.readoptions[
                        self.file_id.ext](eval(
                            self.inputoptions[self.file_id.ext])).copy(),
                                state= self.state)
                    return memento

                except Exception as e:
                    print(str(e))
                    raise IOError(self.file_error)

        def set_data(self, instFileCaretaker, state):
            self._data = instFileCaretaker.restore_memento(state)

    return FileHandler

@pytest.fixture
def FileCaretaker():
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

    return FileCaretaker

@pytest.fixture
def FileMemento():
    class FileMemento(object):
        '''
        Memento Class. This simply records the
        state of the data and gives it to the 
        FileCaretaker
        '''

        def __init__(self, dfstate, state):
            self.__dfstate = pd.DataFrame(dfstate)
            self.__state = str(state)

        def get_dfstate(self):
            return self.__dfstate

        def get_state(self):
            return self.__state
    return FileMemento

@pytest.fixture
def DataProxy(FileHandler):
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
    return DataProxy

@pytest.fixture
def user_input():
    rbtn = {'csv': True, 'xlsx': False, 'txt': False}
    lned = {'sheet': '', 'delim': '', 'tskip': '', 'bskip': ''}
    fname = 'DataRawTestFile.csv'

    user_input = ini.InputHandler(
        name='fileoptions', lnedentry=lned, rbtns=rbtn, filename=fname)

    return user_input


def test_csv_reader(
        user_input, DataProxy, FileCaretaker,
        FileHandler, FileMemento):
    filecaretaker = FileCaretaker()
    
    loaded = FileHandler(user_input)
    assert isinstance(loaded, FileHandler)

    
    # Register memento before loading data
    filecaretaker.save_to_memento(loaded.create_memento())
    loaded.set_data(filecaretaker, 'original')

    fileproxy = DataProxy(loaded._data, 'proxy')

    assert isinstance(fileproxy._data, pd.DataFrame)
    print(fileproxy._data)

