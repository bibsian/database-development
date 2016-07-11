#!usr/bin/env python
import pytest
from pandas import read_csv
import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Dropbox/database-development/" +
        "test/")
    end = "/"

elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Dropbox\\database-development" +
        "\\test\\")
    end = "\\"
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath + 'logiclayer' + end)))
from test.logiclayer import class_commanders as cmd
from test.logiclayer.datalayer import class_filehandles as fhndl
os.chdir(rootpath)

@pytest.fixture
def makeproxycommander():
    class MakeProxyCommander(cmd.DataCommand):
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

    return MakeProxyCommander


@pytest.fixture
def makeproxyreceiver():
    class MakeProxyReceiver():
        '''
        Class to instatiate the proxy class
        '''
        def __init__(self):
            self.proxydata = None
            
        def make_proxy_data(self, dataframe, state):
            self.proxydata = fhndl.DataProxy(
                dataframe, state)
            
            return self.proxydata

    return MakeProxyReceiver

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


        def load_file_process(self):
            self.perform_commands.execute()
            self.history['fileloader'] = self.perform_commands

        def make_proxy_data(self):
            self.perform_commands.execute()
            self.history[
                self.perform_commands.state] = self.perform_commands
            
    return CommandInvoker

@pytest.fixture
def loadeddata():
    df = read_csv('Datasets_manual_test/DataRawTestFile.csv')
    return df


def test_making_proxies(
        makeproxycommander, makeproxyreceiver, loadeddata,
        commandinvoker):
    
    carecommand = cmd.CareTakerCommand(cmd.CareTakerReceiver())
    sessioninvoker = commandinvoker(carecommand)
    
    sessioninvoker.load_file_caretaker()
    sessioncaretaker = carecommand._caretaker
    print(sessioncaretaker)

    # ----Saving a whole data proxy--------------------------#
    # ----proxy command
    proxycommand = makeproxycommander(
        makeproxyreceiver(), loadeddata, 'proxy1')

    # ----session invoker
    sessioninvoker.perform_commands = proxycommand
    sessioninvoker.make_proxy_data()

    # ----session caretaker
    sessioncaretaker.save_to_memento(
        proxycommand._proxy.create_memento())

    # ---- Saving new dataframe wiht only 1 columns--------#
    proxycommandcolumn = makeproxycommander(
        makeproxyreceiver(), loadeddata['site'], 'proxycolumn')

    # ----session invoker
    sessioninvoker.perform_commands = proxycommandcolumn
    sessioninvoker.make_proxy_data()

    # ----session caretaker
    sessioncaretaker.save_to_memento(
        proxycommandcolumn._proxy.create_memento())

    # Asserting there are indeed differences in the proxies
    assert (len(sessioncaretaker.restore_memento('proxy1').columns)
           > 1) is True

    assert (len(sessioncaretaker.restore_memento('proxycolumn').columns)
            == 1) is True
