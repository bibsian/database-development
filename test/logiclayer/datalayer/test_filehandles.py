#!/usr/bin/env python
import pytest
from pandas import read_csv, read_excel, read_table, DataFrame
from collections import namedtuple
import sys, os
import copy
from poplerGUI import class_inputhandler as ini

rootpath = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname( __file__ ))))
end = os.path.sep
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath + 'logiclayer' + end)))
os.chdir(rootpath)

@pytest.fixture
def DataFileOriginator(Memento):
    class DataFileOriginator(object):
        """
        FileHandler (i.e. the originator)
        is a class that will take a user selected
        file, identify the extension, and load the data as an
        instance of a pandas dataframe... This is all the
        handler does.

        Class has some properties for working with file extensions
        and pandas I/O methods

        This is the originator of the initial data
        """

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
            self.accepted_filetypes = [
                '.csv', '.txt', '.xlsx', 'xls'
            ]

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


        def save_to_memento(self):
            '''
            Adding a method to set the data
            attribute. File type must be able to be read in by
            pandas.
            '''

            if self.file_id.ext not in self.accepted_filetypes:
                raise IOError('Cannot open file type')
            try:
                if self.file_id.ext == '.csv':
                    self._data = read_csv(
                        self.inputoptions[
                            '.csv']['filename']
                        )
                elif (
                        self.file_id.ext == '.xls' or
                        self.file_id.ext == '.xlsx'):
                    self._data = read_excel(
                        self.inputoptions[
                            'xlsx']['filename'],
                        sheetname=self.inputoptions[
                            'xlsx']['sheet']
                        )
                elif self.file_id.ext == '.txt':
                    self._data = read_table(
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
            except Exception as e:
                print('Could not read in file: ', str(e))

            for i, item in enumerate(self._data.columns):
                na_vals = [
                    9999, 99999, 999999,
                    -9999, -99999, -999999,
                    -8888, -88888, -88888, -888,
                    9999.0, 99999.0, 999999.0,
                    -9999.0, -99999.0, -999999.0,
                    -8888.0, -88888.0, -888888.0,
                    -888.0
                ]
                self._data[item].replace(
                    dict(zip(na_vals, ['NaN']*len(na_vals))),
                    inplace=True)
            self._data.fillna('NA',inplace=True)

            self._data = self._data[
                self._data.isnull().all(axis=1) != True]
            memento = Memento(dfstate = self._data.copy(),state= self.state)
            return memento
    return DataFileOriginator

@pytest.fixture
def Caretaker():
    class Caretaker(object):
        '''Caretaker for state of dataframe'''
        def __init__(self):
            self._statelogbook = {}
            self._statelist = []
        def save(self, memento):
            ''' 
            Saves memento object with a dictionary
            recording the state name and the dataframe state
            '''
            self._statelogbook[
                memento.get_state()] = memento
            self._statelist.append(memento.get_state())
        def restore(self):
            '''
            Restores a memento given a state_name
            '''
            try:
                if self._statelist:
                    print('restore list:', self._statelist)
                    if len(self._statelist) == 1:
                        print('og restore')
                        return self._statelogbook[self._statelist[0]]
                    else:
                        self._statelist.pop()
                        return self._statelogbook[self._statelist[-1]]
                else:
                    raise AttributeError('Cannot undo further')
            except Exception as e:
                print(str(e))

    return Caretaker

@pytest.fixture
def Memento():
    class Memento(object):
        '''
        Memento Class. 
        This simply records the
        state of the data and gives it to the 
        FileCaretaker
        '''
        def __init__(self, dfstate, state):
            self._dfstate = dfstate.copy(deep=True)
            self._state = str(state)

        def get_dfstate(self):
            return self._dfstate

        def get_state(self):
            return self._state
    return Memento

@pytest.fixture
def DataOriginator():
    class DataOriginator(object):
        def __init__(self, df, state):
            self._data = df
            self._state = state
        def save_to_memento(self):
            memento = Memento(self._data, self._state)
            return memento
        def restore_from_memento(self, memento):
            self._data = memento.get_dfstate()
            self._state = memento.get_state()

    return DataOriginator


@pytest.fixture
def user_input():
    rbtn = {'csv': True, 'xlsx': False, 'txt': False}
    lned = {
        'sheet': '', 'delim': '', 'tskip': '', 'bskip': '',
        'header': ''
    }
    fname = (
        rootpath + end + 'Datasets_manual_test' + end +
        'raw_data_test_1.csv')
    user_input = ini.InputHandler(
        name='fileoptions',lnedentry=lned,
        rbtns=rbtn, filename=fname, checks=False)
    return user_input

@pytest.fixture
def real_data():
    rbtn = {'csv': False, 'xlsx': False, 'txt': True}
    lned = {
        'sheet': '', 'delim': '\t', 'tskip': '', 'bskip': '',
        'header': ''
    }
    fname = (rootpath + end +'data'+end + 'SGS_LTER_Humus_canopyCover.txt')
    user_input = ini.InputHandler(
        name='fileoptions',lnedentry=lned,
        rbtns=rbtn, filename=fname, checks=False)
    return user_input
    

# def test_csv_reader_method(
#         user_input, Caretaker,
#         DataFileOriginator, DataOriginator, Memento):
#     caretaker = Caretaker()
#     originator_from_file = DataFileOriginator(user_input)
#     originator = DataOriginator(None, 'Initialize')
#     assert (isinstance(originator, DataOriginator)) is True
#     caretaker.save(originator_from_file.save_to_memento())
#     originator.restore_from_memento(caretaker.restore())
#     assert (isinstance(originator._data, DataFrame)) is True

def test_txt_true(
        real_data, Caretaker,
        DataFileOriginator, DataOriginator, Memento):
    caretaker = Caretaker()
    originator_from_file = DataFileOriginator(real_data)
    originator = DataOriginator(None, 'Initialize')
    assert (isinstance(originator, DataOriginator)) is True
    caretaker.save(originator_from_file.save_to_memento())
    originator.restore_from_memento(caretaker.restore())
    assert (isinstance(originator._data, DataFrame)) is True
    print(originator._data)

# 
# @pytest.fixture
# def user_txt():
#     rbtn = {'csv': False, 'xlsx': False, 'txt': True}
#     lned = {
#         'sheet': '', 'delim': '', 'tskip': '', 'bskip': '',
#         'header': ''
#     }
#     fname = (
#         rootpath + end + 'Datasets_manual_test' + end +
#         'climate_precip.txt')
#     user_input = ini.InputHandler(
#         name='fileoptions', lnedentry=lned,
#         rbtns=rbtn, filename=fname, checks=True)
#     return user_input
# 
# def test_txt_reader_method(
#         user_txt, Caretaker,
#         DataFileOriginator, DataOriginator, Memento):
#     caretaker = Caretaker()
#     originator_from_file = DataFileOriginator(user_txt)
#     originator = DataOriginator(None, 'Initialize')
#     assert (isinstance(originator, DataOriginator)) is True
#     caretaker.save(originator_from_file.save_to_memento())
#     originator.restore_from_memento(caretaker.restore())
#     assert (isinstance(originator._data, DataFrame)) is True
# 
# 
# 
# @pytest.fixture
# def user_txt_delim():
#     rbtn = {'csv': False, 'xlsx': False, 'txt': True}
#     lned = {
#         'sheet': '', 'delim': ',', 'tskip': '', 'bskip': '',
#         'header': ''
#     }
#     fname = 'Datasets_manual_test/climate_temp_test.txt'
#     user_input = ini.InputHandler(
#         name='fileoptions', lnedentry=lned,
#         rbtns=rbtn, filename=fname, checks=False)
#     return user_input
#  
# def test_txt_comma_delim_reader_method(
#         user_txt_delim, Caretaker, user_txt,
#         DataFileOriginator, DataOriginator, Memento):
#     caretaker = Caretaker()
# 
#     originator_from_file = DataFileOriginator(user_txt_delim)
#     originator = DataOriginator(None, 'Initialize')
#     assert (isinstance(originator, DataOriginator)) is True
#     caretaker.save(originator_from_file.save_to_memento())
#     originator.restore_from_memento(caretaker.restore())
#     assert (isinstance(originator._data, DataFrame)) is True
#     originator_from_file = DataFileOriginator(user_txt)
#     originator = DataOriginator(None, 'Initialize')
#     assert (isinstance(originator, DataOriginator)) is True
#     caretaker.save(originator_from_file.save_to_memento())
#     originator.restore_from_memento(caretaker.restore())
#     assert (isinstance(originator._data, DataFrame)) is True
# 
# 
# 
# @pytest.fixture
# def user_txt_skiplines_no_header():
#     rbtn = {'csv': False, 'xlsx': False, 'txt': True}
#     lned = {
#         'sheet': '', 'delim': '\t', 'tskip': '8', 'bskip': '',
#         'header': '-1'
#     }
#     fname = (
#         rootpath + end + 'Datasets_manual_test' + end +
#         'skip_no_header_test.txt')
#     user_input = ini.InputHandler(
#         name='fileoptions', lnedentry=lned,
#         rbtns=rbtn, filename=fname, checks=True)
#     return user_input
# 
# def test_txt_skiplines_no_header(
#         user_txt_skiplines_no_header, Caretaker,
#         DataFileOriginator, DataOriginator, Memento):
#     caretaker = Caretaker()
#     originator_from_file = DataFileOriginator(
#         user_txt_skiplines_no_header)
#     originator = DataOriginator(None, 'Initialize')
#     assert (isinstance(originator, DataOriginator)) is True
#     caretaker.save(originator_from_file.save_to_memento())
#     originator.restore_from_memento(caretaker.restore())
#     data = originator._data
#     assert (isinstance(data, DataFrame)) is True
#     assert (len(data.columns) == 3) is True
#     print(data)
#     
# @pytest.fixture
# def user_txt_skiplines_header():
#     rbtn = {'csv': False, 'xlsx': False, 'txt': True}
#     lned = {
#         'sheet': '', 'delim': '\t', 'tskip': '10', 'bskip': '',
# ': ''
#     }
#     fname = (
#         rootpath + end + 'Datasets_manual_test' + end +
#         'skip_header_test.txt')
#     user_input = ini.InputHandler(
#         name='fileoptions', lnedentry=lned,
#         rbtns=rbtn, filename=fname, checks=False)
#     return user_input
# 
# def test_txt_skiplines_header(
#         user_txt_skiplines_header, Caretaker,
#         DataFileOriginator, DataOriginator, Memento):
#     caretaker = Caretaker()
#     originator_from_file = DataFileOriginator(
#         user_txt_skiplines_header)
#     originator = DataOriginator(None, 'Initialize')
#     assert (isinstance(originator, DataOriginator)) is True
#     caretaker.save(originator_from_file.save_to_memento())
#     originator.restore_from_memento(caretaker.restore())
#     data = originator._data
#     assert (isinstance(data, DataFrame)) is True
#     assert (len(data.columns) == 3) is True
#     print(data)
# 
