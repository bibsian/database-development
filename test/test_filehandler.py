#!usr/bin/env python
import pytest
import os
import pandas as pd
import collections
import gc

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
    
    def __init__(self, filetoload=None, **kwargs):
        self.filetoload = filetoload
        self.sheet = kwargs.pop('sheet', None)
        self.topskiplines = kwargs.pop('topskiplines', None)
        self.bottomskiplines = kwargs.pop('bottomskiplines', 0)
        self.delimitchar = kwargs.pop('delimitchar', None)
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
                'You have not specified a file to upload')

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
        self.__dfstate = pd.DataFrame(dfstate)
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

 
    
def test_initialization():
    # Simulate nothing returned from user
    testloadedfile = FileHandler()
    assert testloadedfile.file_id is None
    with pytest.raises(AttributeError):
        testloadedfile.create_memento()


    # Simulate only one parameter given (filetoload)
    # Bad entry (no extension to the file)
    testloadedfile = FileHandler(filetoload='nofilehere')
    assert testloadedfile.filetoload == 'nofilehere'
    with pytest.raises(OSError):
        testloadedfile.file_id.name

    with pytest.raises(OSError):
        testloadedfile.file_id.ext


    # Simulate only one parameter given (filetoload)
    # Good entry, file not there
    testfiletoload = FileHandler(
        filetoload='nofilehere.txt')
    testfiletoload.filetoload = 'test.txt'
    assert (testfiletoload.file_id.ext == '.txt') is True
    assert (testfiletoload.file_id.name == 'test') is True
    assert (testfiletoload.file_id.name == 'dkdkd') is False
    with pytest.raises(IOError):
        testfiletoload.create_memento()
    
    # Simulate one both parameters given
    # with a readable file
    testfiletoload = FileHandler(
        filetoload='DataRawTestFile.csv')
    testfiletoload.filetoload = 'DataRawTestFile.csv'
    assert (testfiletoload.file_id.name == 'DataRawTestFile') is True
    assert (testfiletoload.file_id.ext == '.txt') is False
    testcaretaker = FileCaretaker()
    testcaretaker.save_to_memento(testfiletoload.create_memento())
    print(testfiletoload.create_memento())
    print('-----')
    print('caretaker check')
    print(len(gc.get_referrers(testcaretaker)))
    print('-----')
    print('Fileload instance check')
    print(len(gc.get_referrers(testfiletoload)))

@pytest.fixture
def fhinstance():
    testfiletoload = FileHandler(
        filetoload='DataRawTestFile.csv')

    return testfiletoload
    
def test_modify_recover_memento(fhinstance):
    # Instatiated the FileCaretaker
    filecaretaker = FileCaretaker()

    # Registering the fixture instance of a FileHandler class
    # with the FileCaretaker
    filecaretaker.save_to_memento(fhinstance.create_memento())
    fhinstance.set_data(filecaretaker, 'original' )
  
    # Creating a proxy object from the FileHandler data
    fileproxy = DataProxy(fhinstance._data, 'proxy')

    # Registering proxy with memento class
    filecaretaker.save_to_memento(fileproxy.create_memento())

    # Printing data
    print("**-------------**")
    print(fileproxy._data)
    print(type(fileproxy._data))
    
    print("**-------------**")
    fileproxy._data = fileproxy._data['site']
    print(fileproxy._data)

    
    print("**-------------**")
    fileproxy._data = filecaretaker.restore_memento('proxy')
    print(fileproxy)
    assert isinstance(fileproxy._data, pd.DataFrame)

