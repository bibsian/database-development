#!usr/bin/env python
import pytest
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
from .inputhandler import InputHandler
from .commanders import LoadDataCommander, DataCommandReceiver
from .commanders import CommandInvoker
from .commanders import MakeProxyCommander, MakeProxyReceiver
from .commanders import CareTakerCommand, CareTakerReceiver
from .metaverify import MetaVerifier
from collections import namedtuple
import pandas as pd

@pytest.fixture
def Facade():
    
    class TableFacade:
        '''
        This is the facade class to handle the interaction
        between the user inputs.
        
        Names of user input instances should be one of the following:
        'fileoptions' = Handle session creation and data verification
        'metacheck' = Handles metadata verification
        'sitetable'
        'taxatable'
        'rawtable'
        'climatesitetable'
        'climaterawtable'
        'timeparser'
        'editdata'
        'dbquery'
        'dbpush'
        'dataproxy'
        '''

        carecommand = CareTakerCommand(CareTakerReceiver())
        
        sessioninvoker = CommandInvoker(carecommand)
        sessioninvoker.load_file_caretaker()
        
        sessioncaretaker = carecommand._caretaker
        
        manager = namedtuple(
            'maanger', 'caretaker invoker')
        input_manager = manager(
            sessioncaretaker, sessioninvoker)


        
        def __init__(self):
            '''
            Initialize facade with a dictionary to track
            user inputs (for logging and session management).
            Class instances will be register with the 
            input dictionary. 

            A commandinvoker will be populating during
            the use of the program, tracking command histories
            
            In addtion a filecaretaker will be instantiated
            when a raw data file is loaded. This will help track
            changes to data
            '''
            self.clsinstance = None
            self._inputs = {}
            self._data = None

            '''

            This property goes through the sequence
            of creating an Caretaker command object and 
            Invoker command object.

            Caretaker will save mementos of altered
            dataframes.

            Invoker will record and implement all commander
            classes.
            '''
            
            
        def input_register(self, clsinstance):
            '''
            Sets user instantiated classes into the facade 
            _input dictionary. 
            
            All other operations performed
            by the program will take the _inputs dictionary 
            within methods to direct the behavior of the program
            '''
            self.clsinstance = clsinstance
            try:
                self._inputs[self.clsinstance.name] = self.clsinstance
            except:
                raise AttributeError(
                    'Wrong class input for program facade.')

        def meta_verity(self):
            '''
            Adapter method:
            Takes 'fileoption' input and MetaVerifier class
            for logic checks.
            '''
            try:
                assert self._inputs[
                    'metacheck'].name == 'metacheck'
            except:
                raise AttributeError(
                    'Not all metadata attributes were entered.')

            verifier = MetaVerifier()

            try:
                assert verifier.verify_entries(
                    self._inputs['metacheck'])

            except Exception as e:
                raise AttributeError(str(e))
                
                
            print('Input verified')
            
        def load_data(self):
            ''' Using commander classes to peform the following
            commands. Note All commands are executed by the
            self.input_manager attribute. This meas all
            commands are registered with the invoker and all
            loaded data is regeristered with the file caretaker


            1) Load Data via the LoadDataCommand (register with
            invoker and registed data loaded with file caretaker)

            2) Generate proxy data from MakeProxyCommander (
            register command with invoker and register proxy
            data with file caretaker)

            return a proxy of the original dataset loaded.
            
            '''
            try:
                assert self._inputs[
                    'fileoptions'].filename is not None
            except:
                raise AttributeError('No file selected to load.')

            
            filecmd = LoadDataCommander(
                DataCommandReceiver(), self._inputs['fileoptions'])

            
            self.input_manager.invoker.perform_commands = filecmd
            
            self.input_manager.invoker.load_file_process()

            dfile = filecmd._loadfileinst

            self.input_manager.caretaker.save_to_memento(
                dfile.create_memento())

            dfile.set_data(
                self.input_manager.caretaker, 'original')

            print(self.input_manager.invoker)
            
            proxycmd = MakeProxyCommander(
                MakeProxyReceiver(), dfile._data, 'proxydf')
            
            self.input_manager.invoker.perform_commands = proxycmd

            
            self.input_manager.invoker.make_proxy_data()

            
            self.input_manager.caretaker.save_to_memento(
                proxycmd._proxy.create_memento())

            self._data = (
                self.input_manager.caretaker.restore_memento(
                    'proxydf'))

            return self._data

                
    return TableFacade


@pytest.fixture
def metahandle():
    lentry = {
        'globalid': 2,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset' +
                    '.cgi?docid=knb-lter-sbc.17'),
        'lter': 'SBC'}
    ckentry = {}
    metainput = InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput

@pytest.fixture
def badmetahandle():
    lentry = {
        'globalid': 5,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset' +
                    '.cgi?docid=knb-lter-sbc.17'),
        'lter': 'SBC'}
    ckentry = {}
    metainput = InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput


@pytest.fixture
def filehandle():
    lentry = {}
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    fileinput = InputHandler(
        name='fileoptions',tablename=None, lnedentry=lentry,
        rbtns=rbtn, checks=ckentry, session=True,
        filename='DataRawTestFile.csv')

    return fileinput


def test_correct_userinput(metahandle, filehandle, Facade):
    '''
    Testing input_register command with a correctly enter
    metadata informatoin. Then trying to load a file
    without have given a fileopting input to the facade
    '''
    # Creating an instance of the facade class. This will
    # be instansiated within the User interface.
    face = Facade()

    # Registering input with the facade (metadata handler)
    face.input_register(metahandle)
    assert ('metacheck' in face._inputs.keys()) is True
    face.meta_verity()

    # Attempting to load data when there has been no
    # user inputs for loading a file
    with pytest.raises(AttributeError):
        face.load_data()


def test_incorrect_userinput(badmetahandle, Facade):
    '''
    Testing the input_register command with incorrect
    metadata inputs (should raise AttributeError)
    '''
    
    face = Facade()

    face.input_register(badmetahandle)

    with pytest.raises(AttributeError):
        face.meta_verity()

def test_file_loader(filehandle, Facade):
    '''
    Testing the file_load command of the facade class.

    NOTE ONLY TESTED FOR CSV FILES ****
    STILL NEED TO EXTEND BEHAVIOR FOR OTHER FILES***

    '''
    
    face = Facade()
    face.input_register(filehandle)

    face.load_data()
    
    assert isinstance(face._data, pd.DataFrame)

    
