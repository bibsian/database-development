#!usr/bin/env python
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
from class_inputhandler import InputHandler
from collections import namedtuple
from class_commanders import LoadDataCommander, DataCommandReceiver
from class_commanders import CommandInvoker
from class_commanders import MakeProxyCommander, MakeProxyReceiver
from class_commanders import CareTakerCommand, CareTakerReceiver
from class_metaverify import MetaVerifier
from class_helpers import UniqueReplace, check_registration

class Facade:
    '''
    This is the facade class to handle the interaction
    between the user inputs.

    Names of user input instances should be one of the following.
    Note, each name corresponds to unique block in the 
    facade class.

    # ---Program start--- #
    'fileoptions' = Handle session creation and data verification
    'metacheck' = Handles metadata verification

    # ---Data Modifications--- #
    'replace'


    # ---Table Concatenation--- #
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
    'replace'


    Note:
    The class attribute 'input_manager' contains the 
    file caretaker (sessioncaretaker) and command 
    invoker (sessioninvoker). Everything preceeding
    it is setup requried to instantiate those classes
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
        self._rawcolumnregister = {
            'globalid': None,
            'lterid': None,
            'siteid': None,
            'metadataid': None,
            'sppcode': None,
            'kingdom': None,
            'phylum': None,
            'class': None,
            'order': None,
            'family': None,
            'genus': None,
            'species': None,
            'date': None,
            'year': None,
            'month': None,
            'day': None,
            'dateformat': None,
            'spt_rep1': None,
            'spt_rep2': None,
            'spt_rep3': None,
            'spt_rep4': None,
            'structure': None,
            'individ': None,
            'unitobs': None,
            'covariates': None
        }
        self._data = None

    def make_proxy_helper(self, data, label):
        proxycmd = MakeProxyCommander(
            MakeProxyReceiver(), data, label)            
        self.input_manager.invoker.perform_commands = proxycmd
        self.input_manager.invoker.make_proxy_data()
        self.input_manager.caretaker.save_to_memento(
            proxycmd._proxy.create_memento())
        self._data = (
            self.input_manager.caretaker.restore_memento(
                label))
        print('Proxy Created')

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
        check_registration(self, 'metacheck')

        verifier = MetaVerifier(self._inputs['metacheck'])
        try:
            assert verifier.verify_entries()
        except Exception as e:
            raise AttributeError(str(e))

        self._rawcolumnregister['globalid'] = (
            self._inputs['metacheck'].lnedentry['globalid'])
        self._rawcolumnregister['lterid'] = (
            self._inputs['metacheck'].lnedentry['lter'])

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

        self.make_proxy_helper(dfile._data, 'proxydf')

        return self._data


    def view_unique(self, inputname):

        check_registration(self, inputname)

        repinst = UniqueReplace(
            self._data, self._inputs[inputname])
        return repinst.get_levels()

    def replace_entry(self, inputname):
        ''' 
        Method to pass input to helper class and replace
        values in the dataframe.
        '''

        try:
            assert self._inputs[inputname].name == inputname
        except Exception as e:
            print(str(e))
            raise ValueError('Input Not Register')

        repinst = UniqueReplace(
            self._data, self._inputs[inputname])
        datamod = repinst.replace_values()

        self.make_proxy_helper(datamod, inputname)
        return self._data

    def replace_levels(self, inputname, modlist):
        '''
        Method to replace factor levels with a user
        modified list of levels
        '''
        check_registration(self, inputname)

        replaceinst = UniqueReplace(
            self._data, self._inputs[inputname])
        replaceinst.get_levels()
        datamod = replaceinst.replace_levels(modlist)

        self.make_proxy_helper(datamod, inputname)
        return self._data

    def display_table(self, tableinfo):
        try:
            assert self._inputs[tableinfo] is not None
        except Exception as e:
            print(str(e))
            raise AssertionError(
                'Table information not input')