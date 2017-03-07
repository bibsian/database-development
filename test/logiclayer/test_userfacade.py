#!/usr/bin/env python
import pytest
from collections import namedtuple, OrderedDict
import datetime as tm
from pandas import DataFrame, read_csv
import sys, os
from poplerGUI.logiclayer.class_metaverify import MetaVerifier
from poplerGUI.logiclayer.class_helpers import (
    check_registration, extract)
from poplerGUI.logiclayer.class_tablebuilder import (
    Study_Site_Table_Builder, Table_Builder_Director,
    Project_Table_Builder, Taxa_Table_Builder,
    Observation_Table_Builder, UpdaterTableBuilder)
from poplerGUI.logiclayer import class_logconfig as log
from poplerGUI.class_inputhandler import InputHandler

rootpath = os.path.dirname(os.path.dirname(os.path.dirname( __file__ )))
end = os.path.sep
sys.path.append(os.path.realpath(os.path.dirname(
    rootpath + 'logiclayer' + end)))

@pytest.fixture
def Facade(Caretaker, DataFileOriginator, DataOriginator, Memento):
    class Facade:
        '''
        This is the facade class to handle the interaction
        between the user inputs and the data
        '''

        # Class attributes are related to managing
        # various commands from user
        data_caretaker = Caretaker()
        data_originator = DataOriginator(None, 'Initializing')

        def __init__(self):
            '''
            Initialize facade with a dictionary to track
            user inputs (for logging and session management).
            Class instances will be registered with the 
            input dictionary. 
            In addtion a filecaretaker will be instantiated
            when a raw data file is loaded. This will help track
            changes to data
            '''
            self.clsinstance = None
            self._inputs = {}
            self._valueregister = {
                'globalid': None,
                'lterid': None,
                'siteid': None,
                'sitelevels': None,
                'study_site_key': None
            }
            self._data = None
            self._dbtabledict = {
                'study_site_table': Study_Site_Table_Builder(),
                'project_table': Project_Table_Builder(),
                'taxa_table': Taxa_Table_Builder(),
                'timetable': None,
                'count_table': Observation_Table_Builder(),
                'biomass_table': Observation_Table_Builder(),
                'density_table': Observation_Table_Builder(),
                'percent_cover_table': Observation_Table_Builder(),
                'individual_table': Observation_Table_Builder(),
                'covartable': None,
                'updatetable': UpdaterTableBuilder()
            }

            self._datamerged = {
                'raw_main': None,
                'raw_main_taxa': None
            }
            
            self._tablelog = {
                'study_site_table': None,
                'project_table': None,
                'maintable': None,
                'maintable_update': None,
                'timetable': None,
                'taxa_table': None,
                'count_table': None,
                'bimoass_table': None,
                'density_table': None,
                'percent_cover_table': None,
                'individual_table': None,
                'covartable': None,
                'climatesite': None,
                'climateobs': None,
                'addsite': None,
                'widetolong': None,
                'changecolumn': None,
                'changecell': None
            }

            self._colinputlog = {
                'siteinfo': None,
                'maininfo': None,
                'taxainfo': None,
                'timeinfo': None,
                'rawinfo': None,
                'covarinfo': None
            }

            self.push_tables = {
                'study_site_table': None,
                'project_table': None,
                'taxa_table': None,
                'timetable': None,
                'count_table': None,
                'biomass_table': None,
                'density_table': None,
                'percent_cover_table': None,
                'individual_table': None,
                'covariates': None,
                'covartable': None
            }

            self.pushtables = None
            self.sitepushed = None
            self.mainpushed = None
            self.siteinproject = None
            self.taxapushed = None
            self.rawpushed = None
    
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

            if self._inputs['metacheck'].verify is None:
                pass
            else:
                verifier._meta = read_csv((
                    rootpath + end + 'data' + end +
                    'Identified_to_upload.csv'),
                    encoding='iso-8859-11')

            try:
                assert verifier.verify_entries()
            except Exception as e:
                raise AttributeError(str(e))

            self._valueregister['globalid'] = (
                self._inputs['metacheck'].lnedentry['globalid']
            )
            self._valueregister['lterid'] = (
                self._inputs['metacheck'].lnedentry['lter']
            )


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

            data_file_originator = DataFileOriginator(
                self._inputs['fileoptions']
            )
            self.data_caretaker.save(
                data_file_originator.save_to_memento()
            )
            self.data_originator.restore_from_memento(
                self.data_caretaker.restore()
            )
            self._data = self.data_originator._data

        def register_site_levels(self, sitelevels):
            '''
            Method to store the unique sitelevel in the
            facade class
            '''
            try:
                assert isinstance(sitelevels, list)
            except Exception as e:
                print(str(e))
                raise TypeError('Site levels input is not a list')

            sitelevels.sort()
            self._valueregister['sitelevels'] = sitelevels


        def create_log_record(self, tablename):
            '''
            Method to initialize a logger; appends the file the log
            saves to with relavent information regarding what table
            and type of information is being recorded
            '''
            try:
                globalid = self._inputs['metacheck'].lnedentry['globalid']
                filename = os.path.split(
                    self._inputs[
                        'fileoptions'].filename)[1]
                dt = (str(
                    tm.datetime.now()).split()[0]).replace("-", "_")
            except Exception as e:
                print(str(e))
                raise AttributeError(
                    'Global ID and data file not set')

            self._tablelog[tablename] =(
                log.configure_logger('tableformat',(
                    'logs/{}_{}_{}_{}.log'.format(
                        globalid, tablename,filename,dt))))
        
        def make_table(self, inputname):
            '''
            Method to take user inputs and create dataframes
            that contain informatoin that will be pushed into 
            the database. The formating of the tables is handled by
            class_tablebuilder.py module.
            Additionally logging of table specific informatoin
            is initiated here.
            '''
            uniqueinput = self._inputs[inputname]
            print('uqinput facade:', uniqueinput)
            tablename = self._inputs[inputname].tablename
            print('tbl name facade: ', tablename)
            globalid = self._inputs['metacheck'].lnedentry['globalid']
            print('globalid facade: ', globalid)
            sitecol = self._inputs['siteinfo'].lnedentry['study_site_key']
            uqsitelevels = self._valueregister['sitelevels']
            
            director = Table_Builder_Director()           
            builder = self._dbtabledict[tablename]
            director.set_user_input(uniqueinput)
            director.set_globalid(globalid)
            director.set_builder(builder)

            if tablename != 'project_table':
                director.set_data(self._data)
            else:
                metaverify = MetaVerifier(self._inputs['metacheck'])
                metadata = metaverify._meta
                director.set_data(metadata[metadata['global_id'] == globalid].copy())

            director.set_sitelevels(uqsitelevels)
            director.set_siteid(sitecol)
            return director.get_database_table()

    return Facade


# ------------------------------------------------------ #
# ---------------- Metadata verification test --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def badmetahandle():
    lentry = {
        'globalid': 1,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset' +
                    '.cgi?docid=knb-lter-sbc.17'),
        'lter': 'SBC'}
    ckentry = {}
    metainput = InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput


def test_incorrect_userinput(badmetahandle, Facade):
    '''
    Testing the input_register command with incorrect
    metadata inputs (should raise AttributeError)
    '''    
    face = Facade()
    face.input_register(badmetahandle)
    with pytest.raises(AttributeError):
        face.meta_verify()

@pytest.fixture
def metahandle():
    lentry = {
        'globalid': 3,
        'metaurl': (
            'http://sbc.lternet.edu/cgi-bin/showDataset.cgi?docid=knb-lter-sbc.19'),
        'lter': 'SBC'}
    ckentry = {}
    metainput = InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput


def test_meta_verify_method(metahandle, filehandle, Facade):
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

# ------------------------------------------------------ #
# ---------------- File loader test --------------- #
# ------------------------------------------------------ #

@pytest.fixture
def filehandle():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {'sheet': '', 'delim': '', 'tskip': '', 'bskip': ''}
    fileinput = InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename=(
            rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
            'raw_data_test_1.csv'))

    return fileinput

def test_file_loader(filehandle, Facade):
    '''
    Testing the file_load command of the facade class.
    NOTE ONLY TESTED FOR CSV FILES ****
    STILL NEED TO EXTEND BEHAVIOR FOR OTHER FILES***
    '''
    face = Facade()
    face.input_register(filehandle)
    face.load_data()
    assert isinstance(face._data, DataFrame)

# ------------------------------------------------------ #
# ---------------- Study site table build test --------------- #
# ------------------------------------------------------ #

@pytest.fixture
def sitehandle():
    lned = {'study_site_key': 'site'}
    sitehandle = InputHandler(
        name='siteinfo', lnedentry=lned, tablename='study_site_table')
    return sitehandle


def test_register_sitelevels(Facade):
    test = ['site1', 'site2']
    face = Facade()
    face.register_site_levels(test)
    assert (
        isinstance(face._valueregister['sitelevels'], list)) is True
    del face


def test_build_site(sitehandle, Facade, filehandle, metahandle):
    face = Facade()
    face.input_register(metahandle)
    face.meta_verify()
    face.input_register(filehandle)
    face.load_data()
    face.input_register(sitehandle)

    sitedirector = face.make_table('siteinfo')
    df = sitedirector._availdf
    assert (isinstance(df, DataFrame)) is True
    print(df)
    lat = df['lat_study_site'].drop_duplicates().values.tolist()
    lng = df['lng_study_site'].drop_duplicates().values.tolist()
    
    assert (lat == ['-99999']) is True
    assert (lng == ['-99999']) is True

    
# ------------------------------------------------------ #
# ---------------- Project table build test --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def project_table_input():
    main_input = InputHandler(
        name='maininfo', tablename='project_table')
    return main_input

def test_build_project_table(
        sitehandle, Facade, filehandle, metahandle, project_table_input,
        project_handle_1_count):
    face = Facade()
    face.input_register(metahandle)
    face.meta_verify()
    face.input_register(filehandle)
    face.load_data()
    face.input_register(sitehandle)
    face.input_register(project_handle_1_count)
    sitelevels = face._data['site'].drop_duplicates().values.tolist()
    sitelevels.sort()
    face.register_site_levels(sitelevels)
    
    maindirector = face.make_table('maininfo')
    df = maindirector._availdf
    print('test facade build: ',df)
    assert (isinstance(df, DataFrame)) is True
    assert (
        df['proj_metadata_key'].drop_duplicates().values.tolist() ==
        [3]) is True

# ------------------------------------------------------ #
# ---------------- Taxa table build test --------------- #
# --------------- Create taxa feature is OFF ----------- #
# ------------------------------------------------------ #
@pytest.fixture
def taxa_user_input():
    taxalned = OrderedDict((
        ('sppcode', ''),
        ('kingdom', ''),
        ('subkingdom', ''),
        ('infrakingdom', ''),
        ('superdivision', ''),
        ('divsion', ''),
        ('subdivision', ''),
        ('superphylum', ''),
        ('phylum', ''),
        ('subphylum', ''),
        ('clss', ''),
        ('subclass', ''),
        ('ordr', ''),
        ('family', ''),
        ('genus', 'genus'),
        ('species', 'species')
    ))

    taxackbox = OrderedDict((
        ('sppcode', False),
        ('kingdom', False),
        ('subkingdom', False),
        ('infrakingdom', False),
        ('superdivision', False),
        ('divsion', False),
        ('subdivision', False),
        ('superphylum', False),
        ('phylum', False),
        ('subphylum', False),
        ('clss', False),
        ('subclass', False),
        ('ordr', False),
        ('family', False),
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
        tablename='taxa_table',
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
    print(len(df['site'].name))
    print('test taxa build, userfacade: ', df)
    assert (isinstance(df, DataFrame)) is True

@pytest.fixture
def count_userinput():
    obslned = OrderedDict((
        ('spatial_replication_level_2', 'transect'),
        ('spatial_replication_level_3', ''),
        ('spatial_replication_level_4', ''),
        ('structure', ''),
        ('unitobs', 'count'),
        ('trt_label', '')
    ))
    
    obsckbox = OrderedDict((
        ('spatial_replication_level_2', False),
        ('spatial_replication_level_3', True),
        ('spatial_replication_level_4', True),
        ('structure', True),
        ('unitobs', False),
        ('trt_label', True)
    ))
    available = [
        x for x,y in zip(
            list(obslned.keys()), list(
                obsckbox.values()))
        if y is False
    ]

    countini = InputHandler(
        name='countinfo',
        tablename='count_table',
        lnedentry=extract(obslned, available),
        checks=obsckbox)

    return countini

def test_build_count(
        sitehandle, Facade, filehandle, metahandle,
        count_userinput):
    face = Facade()
    face.input_register(metahandle)
    face.meta_verify()
    face.input_register(filehandle)
    face.load_data()
    face.input_register(sitehandle)
    face.input_register(count_userinput)
    sitelevels = face._data['site'].drop_duplicates().values.tolist()
    sitelevels.sort()
    face.register_site_levels(sitelevels)
    
    countdirector = face.make_table('countinfo')
    df = countdirector._availdf
    print(df)
    assert (isinstance(df, DataFrame)) is True
