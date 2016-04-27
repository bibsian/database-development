#!usr/bin/env python
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
from inputhandler import InputHandler
from commanders import DataCommand, LoadDataCommander
from commanders import CommandInvoker, DataCommandReceiver
from metaverify import MetaVerifier


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
            self.commandinvoker = None
            self._data = None
            self.filecaretaker = None
            
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
            ''' Using commander classes to upload data and save
            a proxy version of the data into the Facade class.
            This way the facade can perform some manipulations
            with user inputs and save versions of manipulated data
            to our FileCareTaker class'''
            try:
                assert self._inputs[
                    'fileoptions'].filename is not None
            except:
                raise AttributeError('No file selected to load.')

