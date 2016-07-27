#! /usr/bin/env python
import pytest
import abc
import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/" +
        "test/")
    end = "/"
    
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Dropbox\\database-development" +
        "\\test\\")
    end = "\\"
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath + 'logiclayer' + end)))
from test.logiclayer.datalayer import class_filehandles as fhndl


# for all subclasses
@pytest.fixture
def abscommand():
    class DataCommand(object):
        '''
        Abstract class interface that
        will serve as the base when
        instantiating commands throughout
        the UI.
        '''

        __meta__ = abc.ABCMeta

        @abc.abstractmethod
        def execute(self):
            pass

        @abc.abstractmethod
        def undo(self):
            pass

    return DataCommand

@pytest.fixture
def caretakercommander(abscommand):
    class CareTakerCommand(abscommand):
        '''
        Commander object to make a call to generate a
        FileCaretaker instance
        '''
        def __init__(self, receiver):
            self.receiver = receiver
            self._caretaker = None
            
        def execute(self):
            self._caretaker = self.receiver.load_file_caretaker()

    return CareTakerCommand

@pytest.fixture
def caretakerreceiver():
    class CareTakerReceiver():
        '''
        Receiver object to istantiate an instance
        of the FileCaretaker
        '''
        def __init__(self):
            self.caretaker = None

        def load_file_caretaker(self):
            self.caretaker = fhndl.FileCaretaker()
            return self.caretaker

    return CareTakerReceiver


# SAME FIXTURE IN OTHER TEST FOR COMMANDER CLASSES
@pytest.fixture
def commandinvoker():
    class CommandInvoker(object):
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

    return CommandInvoker

def test_caretaker_command(
        caretakercommander, caretakerreceiver, commandinvoker):

    carecommand = caretakercommander(caretakerreceiver())

    careinvoker = commandinvoker(carecommand)

    careinvoker.load_file_caretaker()

    sessioncaretaker = carecommand._caretaker
    print(sessioncaretaker)
    assert isinstance(sessioncaretaker, fhndl.FileCaretaker)
