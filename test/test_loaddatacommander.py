#!usr/bin/env python
import pytest
from .filehandles import FileCaretaker,FileHandler, DataProxy,\
    FileMemento
from .inputhandler import InputHandler
from .commanders import DataCommand, CareTakerCommand,\
    CareTakerReceiver, CommandInvoker
import pandas as pd

# Concrete Command classes
@pytest.fixture
def loaddatacommander():
    class LoadDataCommander(DataCommand):
        '''
        Commander class. Since the commander
        class is mostly for loading data
        it's going to have a data attribute
        that is populating via the data loader reciever.
        
        If anything goes wrong with loading the data
        its coming from the reiever class; not the commander.
        '''
        def __init__(self, receiver, userinput):
            self.receiver = receiver
            self.userinput = userinput
            self._loadfileinst = None
            
        def execute(self):
            self._loadfileinst = self.receiver.load_file_process(
                self.userinput)


    return LoadDataCommander


# Receiver class for loading data
@pytest.fixture
def datacommandreceiver():
    class DataCommandReceiver(object):
        '''
        In the command pattern the 'command' class
        is nothing but a sender of signals/commands.
        To send a command you need to instantiate it
        with a receiver. Reievers are what
        perform all the work. This receiver
        is specialized for loading data.
        '''
        
        def __init__(self):
            self.filehandlerinstance = None
            
        def load_file_process(self, userinput):
            # Loading file
            self.filehandlerinstance = FileHandler(
                filetoload= userinput.filename)

            return self.filehandlerinstance

    return DataCommandReceiver


# Invoker class to be used by UI Facade to track issued
# commands
@pytest.fixture
def commandinvoker():
    class CommandInvoker():
        '''
        The invoker is a class to keep track of the commands
        sent among all the receivers. Right now the
        only reciever is for file loading (but will incoroporate
        reicevers to interact with the database too)

        '''
        def __init__(self, commands):
            self.perform_commands = commands
            self.history = {}

        def load_file_caretaker(self):
            self.perform_commands.execute()
            self.history['caretaker'] = self.perform_commands

        # Invoker method for Loading the data file through
        # the datacommandreceiver
        def load_file_process(self):
            self.perform_commands.execute()
            self.history['fileloader'] = self.perform_commands
    return CommandInvoker


@pytest.fixture
def metahandle():
    lentry = {'globalid': 2, 'metaurl': 'https://test', 'lter': 'SBC'}
    metainput = InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry)
    return metainput


@pytest.fixture
def inputhandle():
    rbtn = {'.csv': True, '.txt': False, '.xlsx': False}
    fileinput = InputHandler(
        name='fileoptions', rbtns=rbtn,
        session=True, filename='DataRawTestFile.csv')
    return fileinput


def test_return_fileHandler(
        metahandle, inputhandle, loaddatacommander,
        datacommandreceiver, commandinvoker):

    # ----- Creating  CareTakerCommand instance
    print ('*-----Caretaker------*')
    carecommand = CareTakerCommand(CareTakerReceiver())

    # ----- Creating session Invoker instance
    sessioninvoker = commandinvoker(carecommand)

    # ----- Calling CareTakerCommand methods 
    sessioninvoker.load_file_caretaker()

    
    # ----  Setting CareTakerCommand to variable
    sessioncaretaker = carecommand._caretaker


    print('*----- LoadDataCommander------*')
    # --------Creating filehandler instance
    filehandlercommand = loaddatacommander(
        datacommandreceiver(), inputhandle)

    # ----- setting LoadDataCommander methods to Invoker methods
    # ----- (needed to properly call filehandler methods)
    sessioninvoker.perform_commands = filehandlercommand

    print('*---Should be FileHandler instance---')
    sessioninvoker.load_file_process()
    ogfile = filehandlercommand._loadfileinst
    assert isinstance(ogfile, FileHandler)

    print('*--- Should be a pandas dataframe instance')
    sessioncaretaker.save_to_memento(ogfile.create_memento())
    ogfile.set_data(sessioncaretaker, 'original')
    assert isinstance(ogfile._data, pd.DataFrame)
    
