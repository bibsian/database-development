#!usr/bin/env python
import abc
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
from filehandles import FileCaretaker,FileHandler, DataProxy
from filehandles import FileMemento
import pdb

# ------ Abstact class that all commands inherit from
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

# --------- Care Taker Pair----------#
class CareTakerCommand(DataCommand):
    '''
    Commander object to make a call to generate a
    FileCaretaker instance
    '''
    def __init__(self, receiver):
        self.receiver = receiver
        self._caretaker = None

    def execute(self):
        self._caretaker = self.receiver.load_file_caretaker()
        return self._caretaker


class CareTakerReceiver():
    '''
    Receiver object to istantiate an instance
    of the FileCaretaker
    '''
    def __init__(self):
        self.caretaker = None

    def load_file_caretaker(self):
        self.caretaker = FileCaretaker()
        return self.caretaker


# ----------- Make Proxy Pair ----------#
class MakeProxyCommander(DataCommand):
    '''
    Command to make a proxy for a given dataframe
    and state (this will help with undoing 
    things)
    '''

    def __init__(self, receiver, dataframe, state):
        self.receiver = receiver
        self.dataframe = dataframe
        self.state = state
        self._proxy = None

    def execute(self):
        self._proxy = self.receiver.make_proxy_data(
            self.dataframe, self.state)


class MakeProxyReceiver():
    '''
    Class to instatiate the proxy class
    '''
    def __init__(self):
        self.proxydata = None

    def make_proxy_data(self, dataframe, state):
        self.proxydata = DataProxy(
            dataframe, state)

        return self.proxydata

# ------------ Load Data Commander pair ----------------------#
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



# -------------Invoker: SHould have all command methods ------#
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


    def load_file_process(self):
        self.perform_commands.execute()
        self.history['fileloader'] = self.perform_commands

    def make_proxy_data(self):
        self.perform_commands.execute()
        self.history[
            self.perform_commands.state] = self.perform_commands
