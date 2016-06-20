#!/usr/bin/env python
import pytest
import sys, os
import pandas as pd
import datetime as tm
from PyQt4 import QtCore
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
from class_inputhandler import InputHandler
from class_commanders import LoadDataCommander, DataCommandReceiver
from class_commanders import CommandInvoker
from class_commanders import MakeProxyCommander, MakeProxyReceiver
from class_commanders import CareTakerCommand, CareTakerReceiver
from class_metaverify import MetaVerifier
from class_helpers import UniqueReplace, check_registration, extract
from class_tablebuilder import (
    SiteTableBuilder, TableDirector, MainTableBuilder,
    TaxaTableBuilder)
from collections import namedtuple, OrderedDict
import class_logconfig as log

@pytest.fixture
def Facade():
    
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
        'timetable'
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
            self._valueregister = {
                'globalid': None,
                'lterid': None,
                'siteid':None,
                'sitelevels': None
            }
            self._data = None
            self._dbtabledict = {
                'sitetable': SiteTableBuilder(),
                'maintable': MainTableBuilder(),
                'taxatable': TaxaTableBuilder(),
                'timetable': None
            }

            self._datamerged = {
                'raw_main': None,
                'raw_main_taxa': None
            }
            
            self._tablelog = {
                'sitetable': None,
                'maintable': None,
                'taxatable': None
            }

            self._colinputlog = {
                'siteinfo': None,
                'maininfo': None,
                'taxainfo': None
            }

            
        def make_proxy_helper(self, data, label):
            proxycmd = MakeProxyCommander(
                MakeProxyReceiver(), data.reset_index(
                    drop=True), label)            
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

        def meta_verify(self):
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

            self._valueregister['globalid'] = (
                self._inputs['metacheck'].lnedentry['globalid'])
            self._valueregister['lterid'] = (
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

        def register_site_levels(self, sitelevels):
            try:
                assert isinstance(sitelevels, list)
            except Exception as e:
                print(str(e))
                raise TypeError('Site levels input is not a list')

            sitelevels.sort()
            self._valueregister['sitelevels'] = sitelevels
        
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

        def make_table(self, inputname):
            uniqueinput = self._inputs[inputname]
            tablename = self._inputs[inputname].tablename
            globalid = self._inputs['metacheck'].lnedentry['globalid']
            filename = os.path.split(
                                self._inputs[
                                    'fileoptions'].filename)[1]
            dt = (str(tm.datetime.now()).split()[0]).replace("-", "_")
            sitecol = self._inputs['siteinfo'].lnedentry['siteid']
            uqsitelevels = self._valueregister['sitelevels']
            
            if self._tablelog[tablename] is None:
                # Log to record input for different tables
                self._tablelog[tablename] =(
                    log.configure_logger('tableformat',(
                        'Logs_UI/{}_{}_{}_{}.log'.format(
                            globalid, tablename,filename,dt))))
            else:
                pass                

            director = TableDirector()           
            builder = self._dbtabledict[tablename]
            director.set_user_input(uniqueinput)
            director.set_builder(builder)

            if tablename != 'maintable':
                director.set_data(self._data)
            else:
                metaverify = MetaVerifier(self._inputs['metacheck'])
                metadata = metaverify._meta
                director.set_data(metadata.iloc[globalid,:])

            director.set_globalid(globalid)
            director.set_siteid(sitecol)
            director.set_sitelevels(uqsitelevels)

            return director.get_database_table()

        def merge_table(self, inputname):
            pass
        
    return Facade


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
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {'sheet': '', 'delim': '', 'tskip': '', 'bskip': ''}
    fileinput = InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename='DataRawTestFile.csv')

    return fileinput


@pytest.fixture
def replacehandle():
    lned = {'from': '-99999', 'to': 'NULL'}
    replaceinput = InputHandler(
        name='replace', lnedentry=lned)
    return replaceinput

@pytest.fixture
def sitehandle():
    lned = {'siteid': 'site'}
    sitehandle = InputHandler(
        name='siteinfo', lnedentry=lned, tablename='sitetable')
    return sitehandle
    
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
    face.meta_verify()
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
        face.meta_verify()

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

def test_register_sitelevels(Facade):
    test = ['site1', 'site2']
    face = Facade()
    face.register_site_levels(test)
    assert (
        isinstance(face._valueregister['sitelevels'], list)) is True
    
def test_manipulate_data(filehandle, Facade, replacehandle):
    face = Facade()
    face.input_register(filehandle)
    face.load_data()

    face.input_register(replacehandle)
    face.replace_entry('replace')

    assert ('-99999' not in face._data.values) is True
    assert (int(-99999) not in face._data.values) is True

def test_view_unique(sitehandle, Facade, filehandle):
    face = Facade()
    face.input_register(filehandle)
    face.load_data()

    face.input_register(sitehandle)
    ulist = face.view_unique('siteinfo')

def test_replace_list(sitehandle, Facade, filehandle):
    sitehandle.name = 'replace_site_levels'
    face = Facade()
    face.input_register(filehandle)
    face.load_data()

    face.input_register(sitehandle)
    ulist = face.view_unique('replace_site_levels')
    print(ulist)
    print(type(ulist))
    modlist = ulist[sitehandle.lnedentry['siteid']].values.tolist()
    modlist[0] = 'changed'
    modlist[1] = 'whatwhat'
    face.replace_levels('replace_site_levels', modlist)
    print(face._data)
    assert (
        ulist.loc[0, sitehandle.lnedentry['siteid']]
        not in face._data.values) is True

    assert (
        ulist.loc[1, sitehandle.lnedentry['siteid']]
        not in face._data.values) is True

def test_build_site(sitehandle, Facade, filehandle, metahandle):
    face = Facade()
    face.input_register(metahandle)
    face.meta_verify()
    face.input_register(filehandle)
    face.load_data()
    face.input_register(sitehandle)

    sitedirector = face.make_table('siteinfo')
    df = sitedirector._availdf
    assert (isinstance(df, pd.DataFrame)) is True
    face._tablelog['sitetable'].info('is this logging?')

@pytest.fixture
def main_input():
    main_input = InputHandler(
        name='maininfo', tablename='maintable')
    return main_input

def test_build_main(
        sitehandle, Facade, filehandle, metahandle, main_input):
    face = Facade()
    face.input_register(metahandle)
    face.meta_verify()
    face.input_register(filehandle)
    face.load_data()
    face.input_register(sitehandle)
    face.input_register(main_input)
    sitelevels = face._data['site'].drop_duplicates().values.tolist()
    sitelevels.sort()
    face.register_site_levels(sitelevels)
    
    maindirector = face.make_table('maininfo')
    df = maindirector._availdf
    print(df)
    assert (isinstance(df, pd.DataFrame)) is True
    face._tablelog['maintable'].info('is this logging?')


@pytest.fixture
def taxa_user_input():
    taxalned = OrderedDict((
        ('sppcode', ''),
        ('kingdom', ''),
        ('phylum', 'TAXON_PHYLUM'),
        ('class', 'TAXON_CLASS'),
        ('order', 'TAXON_ORDER'),
        ('family', 'TAXON_FAMILY'),
        ('genus', 'TAXON_GENUS'),
        ('species', 'TAXON_SPECIES') 
    ))

    taxackbox = OrderedDict((
        ('sppcode', False),
        ('kingdom', False),
        ('phylum', True),
        ('class', True),
        ('order', True),
        ('family', True),
        ('genus', True),
        ('species', True) 
    ))

    taxacreate = {
        'taxacreate': False
    }
    
    available = [
        x for x,y in zip(
            list(taxalned.keys()), list(
                taxackbox.values()))
        if y is True
    ]
    
    taxaini = InputHandler(
        name='taxainfo',
        tablename='taxatable',
        lnedentry= extract(taxalned, available),
        checks=taxacreate)
    return taxaini
    
def test_build_taxa(
        sitehandle, Facade, filehandle, metahandle,
        taxa_user_input):
    face = Facade()
    face.input_register(metahandle)
    face.meta_verify()
    face.input_register(filehandle)
    face.load_data()
    face.input_register(sitehandle)
    face.input_register(taxa_user_input)
    sitelevels = face._data['site'].drop_duplicates().values.tolist()
    sitelevels.sort()
    face.register_site_levels(sitelevels)
    
    taxadirector = face.make_table('taxainfo')
    df = taxadirector._availdf
    print(df)
    assert (isinstance(df, pd.DataFrame)) is True

