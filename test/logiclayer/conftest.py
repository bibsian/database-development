import pytest
from pandas import (
    merge, concat, DataFrame, read_sql, read_csv, read_excel, read_table,
    to_numeric
)
from sqlalchemy import select, update, column
from collections import OrderedDict, namedtuple
import os, sys
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/")
    end = "/"

elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development")
    end = "\\"
os.chdir(rootpath)
from poplerGUI.logiclayer.datalayer import config as orm
from poplerGUI import class_inputhandler as ini
from poplerGUI.logiclayer.class_helpers import (
    string_to_list, extract
    )


# --- Fixtures to use across all test in this folder --- #
# ------------------------------------------------------ #
# ---------------- meta data handle --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def meta_handle_1_count():
    lentry = {
        'globalid': 1,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset.cgi?docid=knb-lter-sbc.18'),
        'lter': 'SBC'}
    ckentry = {}
    metainput = ini.InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput

@pytest.fixture
def meta_handle_2_density():
    lentry = {
        'globalid': 2,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset.cgi?docid=knb-lter-sbc.17'),
        'lter': 'SBC'}
    ckentry = {}
    metainput = ini.InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput

@pytest.fixture
def meta_handle_3_biomass():
    lentry = {
        'globalid': 3,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset.cgi?docid=knb-lter-sbc.19'),
        'lter': 'SBC'}
    ckentry = {}
    metainput = ini.InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput

@pytest.fixture
def meta_handle_4_percent_cover():
    lentry = {
        'globalid': 4,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset.cgi?docid=knb-lter-sbc.15'),
        'lter': 'SBC'}
    ckentry = {}
    metainput = ini.InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput

@pytest.fixture
def meta_handle5():
    lentry = {
        'globalid': 5,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset.cgi?docid=knb-lter-sbc.29'),
        'lter': 'SBC'}
    ckentry = {}
    metainput = ini.InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput

@pytest.fixture
def meta_handle7():
    lentry = {
        'globalid': 7,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset.cgi?docid=knb-lter-sbc.30'),
        'lter': 'SBC'}
    ckentry = {}
    metainput = ini.InputHandler(
        name='metacheck', tablename=None, lnedentry=lentry,
        checks=ckentry)
    return metainput

# ------------------------------------------------------ #
# ---------------- File loader handle --------------- #
# ------------------------------------------------------ #

@pytest.fixture
def file_handle_wide_to_long():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    Xlned = {
        'sheet': '', 'delim': '', 'tskip': '', 'bskip': '',
        'header': ''}
    fileinput = ini.InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename=(
            rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
            'long_data_test.csv'))
    return fileinput
    

@pytest.fixture
def file_handle_1_count():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {
        'sheet': '', 'delim': '', 'tskip': '', 'bskip': '',
        'header': ''}
    fileinput = ini.InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename=(
            rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
            'raw_data_test_1.csv'))
    return fileinput

@pytest.fixture
def file_handle_2_density():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {
        'sheet': '', 'delim': '', 'tskip': '', 'bskip': '',
        'header': ''}
    fileinput = ini.InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename=(
            rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
            'raw_data_test_2.csv'))
    return fileinput

@pytest.fixture
def file_handle_3_biomass():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {
        'sheet': '', 'delim': '', 'tskip': '', 'bskip': '',
        'header': ''}
    fileinput = ini.InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename=(
            rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
            'raw_data_test_3.csv'))
    return fileinput

@pytest.fixture
def file_handle_4_percent_cover():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {
        'sheet': '', 'delim': '', 'tskip': '', 'bskip': '',
        'header': ''}
    fileinput = ini.InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename=(
            rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
            'raw_data_test_4.csv'))
    return fileinput

@pytest.fixture
def file_handle5():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {
        'sheet': '', 'delim': '', 'tskip': '', 'bskip': '',
        'header': ''}
    fileinput = ini.InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename=(
            rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
            'raw_data_test_5.csv'))
    return fileinput

# ------------------------------------------------------ #
# ---------------- Study site handle --------------- #
# ----------------------------------------------------- #
@pytest.fixture
def site_handle_wide_to_long():
    lned = {'study_site_key': 'SITE'}
    sitehandle = ini.InputHandler(
        name='siteinfo', lnedentry=lned, tablename='study_site_table')
    return sitehandle
    

@pytest.fixture
def site_handle_1_count():
    lned = {'study_site_key': 'site'}
    sitehandle = ini.InputHandler(
        name='siteinfo', lnedentry=lned, tablename='study_site_table')
    return sitehandle

@pytest.fixture
def site_handle_2_density():
    lned = {'study_site_key': 'SITE'}
    sitehandle = ini.InputHandler(
        name='siteinfo', lnedentry=lned, tablename='study_site_table')
    return sitehandle

@pytest.fixture
def site_handle_3_biomass():
    lned = {'study_site_key': 'site'}
    sitehandle = ini.InputHandler(
        name='siteinfo', lnedentry=lned, tablename='study_site_table')
    return sitehandle

@pytest.fixture
def site_handle_4_percent_cover():
    lned = {'study_site_key': 'site'}
    sitehandle = ini.InputHandler(
        name='siteinfo', lnedentry=lned, tablename='study_site_table')
    return sitehandle

@pytest.fixture
def site_handle5():
    lned = {'study_site_key': 'SITE'}
    sitehandle = ini.InputHandler(
        name='siteinfo', lnedentry=lned, tablename='study_site_table')
    return sitehandle

# ------------------------------------------------------ #
# ---------------- Project table handle --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def project_handle_1_count():

    studytype = namedtuple('studytype', 'checked entry unit')
    # derived
    derived = namedtuple('derived', 'checked entry unit')
    # treatments
    treatments = namedtuple('treatments', 'checked entry unit')
    # Contacts: author, contact email
    contacts = namedtuple('contacts', 'checked entry unit')
    # Community
    community = namedtuple('community', 'checked entry unit')
    # SamplingFreq
    sampfreq = namedtuple('sampfreq', 'checked entry unit')
    # Datatype/units
    dtype = namedtuple('dtype', 'checked entry unit')
    # organism structure
    structure = namedtuple('structure', 'checked entry unit')
    # Spatial extent
    ext = namedtuple('spatial_ext', 'checked entry unit')

    form_dict = OrderedDict((
        ('samplingunits', dtype(False, '', None)),
        ('datatype', dtype(True, 'count', None)),
        ('structured_type_1', structure(True, 'size', 'cm')),
        ('structured_type_2', structure(False, '', '')),
        ('structured_type_3', structure(False, '', '')),
        ('samplefreq', sampfreq(True, 'month:yr', None)),
        ('studytype', studytype(True, 'obs', None)),
        ('community', community(True, True, None)),
        ('spatial_replication_level_1_extent', ext(True, '100', 'm2')),
        ('spatial_replication_level_2_extent', ext(True, '10', 'm2')),
        ('spatial_replication_level_3_extent', ext(False, '', '')),
        ('spatial_replication_level_4_extent', ext(False, '', '')),
        ('spatial_replication_level_5_extent', ext(False, '', '')),
        ('treatment_type_1', treatments(False, 'NULL', None)),
        ('treatment_type_2', treatments(False, 'NULL', None)),
        ('treatment_type_3', treatments(False, 'NULL', None)),
        ('control_group', treatments(False, '', None)),
        ('derived', derived(True, 'no', None)),
        ('authors', contacts(True, 'AJ Bibian, TEX Miller', None)),
        ('authors_contact', contacts(True, 'aj@hotmail.com, tex@hotmail.com', None))
    ))
    
    main_input = ini.InputHandler(
        name='maininfo', tablename='project_table',
        lnedentry=form_dict)
    return main_input

@pytest.fixture
def project_handle_2_density():
    main_input = ini.InputHandler(
        name='maininfo', tablename='project_table')
    return main_input

@pytest.fixture
def project_handle_3_biomass():
    main_input = ini.InputHandler(
        name='maininfo', tablename='project_table')
    return main_input

@pytest.fixture
def project_handle_4_percent_cover():
    main_input = ini.InputHandler(
        name='maininfo', tablename='project_table')
    return main_input

@pytest.fixture
def project_handle5():
    main_input = ini.InputHandler(
        name='maininfo', tablename='project_table')
    return main_input

# ------------------------------------------------------ #
# ---------------- taxa table handle --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def taxa_handle_1_count():
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
    taxaini = ini.InputHandler(
        name='taxainfo',
        tablename='taxa_table',
        lnedentry= extract(taxalned, available),
        checks=taxacreate)
    return taxaini

@pytest.fixture
def taxa_handle_2_density():
    taxalned = OrderedDict((
        ('sppcode', ''),
        ('kingdom', 'TAXON_KINGDOM'),
        ('subkingdom', ''),
        ('infrakingdom', ''),
        ('superdivision', ''),
        ('divsion', ''),
        ('subdivision', ''),
        ('superphylum', ''),
        ('phylum', 'TAXON_PHYLUM'),
        ('subphylum', ''),
        ('clss', 'TAXON_CLASS'),
        ('subclass', ''),
        ('ordr', 'TAXON_ORDER'),
        ('family', 'TAXON_FAMILY'),
        ('genus', 'TAXON_GENUS'),
        ('species', 'TAXON_SPECIES')
    ))
    taxackbox = OrderedDict((
        ('sppcode', False),
        ('kingdom', True),
        ('subkingdom', False),
        ('infrakingdom', False),
        ('superdivision', False),
        ('divsion', False),
        ('subdivision', False),
        ('superphylum', False),
        ('phylum', True),
        ('subphylum', False),
        ('clss', True),
        ('subclass', False),
        ('ordr', True),
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
    taxaini = ini.InputHandler(
        name='taxainfo',
        tablename='taxa_table',
        lnedentry= extract(taxalned, available),
        checks=taxacreate)
    return taxaini

@pytest.fixture
def taxa_handle_3_biomass():
    taxalned = OrderedDict((
        ('sppcode', ''),
        ('kingdom', ''),
        ('subkingdom', ''),
        ('infrakingdom', ''),
        ('superdivision', ''),
        ('divsion', ''),
        ('subdivision', ''),
        ('superphylum', ''),
        ('phylum', 'phylum'),
        ('subphylum', ''),
        ('clss', 'clss'),
        ('subclass', ''),
        ('ordr', 'ordr'),
        ('family', 'family'),
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
        ('phylum', True),
        ('subphylum', False),
        ('clss', True),
        ('subclass', False),
        ('ordr', True),
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
    taxaini = ini.InputHandler(
        name='taxainfo',
        tablename='taxa_table',
        lnedentry= extract(taxalned, available),
        checks=taxacreate)
    return taxaini

@pytest.fixture
def taxa_handle_4_percent_cover():
    taxalned = OrderedDict((
        ('sppcode', 'code'),
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
        ('genus', ''),
        ('species', '')
    ))
    taxackbox = OrderedDict((
        ('sppcode', True),
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
        ('genus', False),
        ('species', False)
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
    taxaini = ini.InputHandler(
        name='taxainfo',
        tablename='taxa_table',
        lnedentry= extract(taxalned, available),
        checks=taxacreate)
    return taxaini


@pytest.fixture
def taxa_handle5():
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
        ('genus', 'TAXON_GENUS'),
        ('species', 'TAXON_SPECIES'),
        ('common_name', 'Common_Name')
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
        ('species', True),
        ('common_name', True)
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
    taxaini = ini.InputHandler(
        name='taxainfo',
        tablename='taxa_table',
        lnedentry= extract(taxalned, available),
        checks=taxacreate)
    return taxaini

# ------------------------------------------------------ #
# ---------------- time handle --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def time_handle_1_count():
    d = {
        'dayname': 'date',
        'dayform': 'dd-mm-YYYY (Any Order)',
        'monthname': 'date',
        'monthform': 'dd-mm-YYYY (Any Order)',
        'yearname': 'date',
        'yearform': 'dd-mm-YYYY (Any Order)',
        'jd': False,
        'hms': False
    }
    timeini = ini.InputHandler(
        name='timeinfo', tablename='timetable',
        lnedentry= d)
    return timeini

@pytest.fixture
def time_handle_2_density():
    d = {
        'dayname': '',
        'dayform': 'NULL',
        'monthname': 'MONTH',
        'monthform': 'mm',
        'yearname': 'YEAR',
        'yearform': 'YYYY',
        'jd': False,
        'hms': False
    }
    timeini = ini.InputHandler(
        name='timeinfo', tablename='timetable',
        lnedentry= d)
    return timeini

@pytest.fixture
def time_handle_3_biomass():
    d = {
        'dayname': '',
        'dayform': 'NULL',
        'monthname': 'month',
        'monthform': 'mm',
        'yearname': 'year',
        'yearform': 'YYYY',
        'jd': False,
        'hms': False
    }
    timeini = ini.InputHandler(
        name='timeinfo', tablename='timetable',
        lnedentry= d)
    return timeini

@pytest.fixture
def time_handle_4_percent_cover():
    d = {
        'dayname': '',
        'dayform': 'NULL',
        'monthname': 'month',
        'monthform': 'mm',
        'yearname': 'year',
        'yearform': 'YYYY',
        'jd': False,
        'hms': False
    }
    timeini = ini.InputHandler(
        name='timeinfo', tablename='timetable',
        lnedentry= d)
    return timeini

@pytest.fixture
def time_handle5():
    d = {
        'dayname': '',
        'dayform': 'NULL',
        'monthname': '',
        'monthform': 'NULL',
        'yearname': 'YEAR',
        'yearform': 'YYYY',
        'jd': False,
        'hms': False
    }
    timeini = ini.InputHandler(
        name='timeinfo', tablename='timetable',
        lnedentry= d)
    return timeini

# ------------------------------------------------------ #
# ---------------- covar handle --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def covar_handle_1_count():
    covarlned = {'columns': None}    
    covarlned['columns'] = string_to_list('temp')
    covarini = ini.InputHandler(
        name='covarinfo', tablename='covartable',
        lnedentry=covarlned)
    return covarini

@pytest.fixture
def covar_handle_2_density():
    covarlned = {'columns': None}    
    covarlned['columns'] = string_to_list('AREA, VIS, OBS_CODE')
    covarini = ini.InputHandler(
        name='covarinfo', tablename='covartable',
        lnedentry=covarlned)
    return covarini

@pytest.fixture
def covar_handle_3_biomass():
    covarlned = {'columns': None}    
    covarlned['columns'] = string_to_list('temp')
    covarini = ini.InputHandler(
        name='covarinfo', tablename='covartable',
        lnedentry=covarlned)
    return covarini

@pytest.fixture
def covar_handle_4_percent_cover():
    covarlned = {'columns': None}    
    covarlned['columns'] = string_to_list('Precip')
    covarini = ini.InputHandler(
        name='covarinfo', tablename='covartable',
        lnedentry=covarlned)
    return covarini


@pytest.fixture
def covar_handle5():
    covarlned = {'columns': None}    
    covarlned['columns'] = string_to_list('TEMP, TAG')
    covarini = ini.InputHandler(
        name='covarinfo', tablename='covartable',
        lnedentry=covarlned)
    return covarini

# ------------------------------------------------------ #
# ---------------- obs table handle --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def count_handle_1_count():
    obslned = OrderedDict((
        ('spatial_replication_level_2', 'transect'),
        ('spatial_replication_level_3', ''),
        ('spatial_replication_level_4', ''),
        ('spatial_replication_level_5', ''),
        ('structured_type_1', ''),
        ('structured_type_2', ''),
        ('structured_type_3', ''),
        ('treatment_type_1', ''),
        ('treatment_type_2', ''),
        ('treatment_type_3', ''),
        ('unitobs', 'count')
    ))    
    obsckbox = OrderedDict((
        ('spatial_replication_level_2', True),
        ('spatial_replication_level_3', False),
        ('spatial_replication_level_4', False),
        ('spatial_replication_level_5', False),
        ('structured_type_1', False),
        ('structured_type_2', False),
        ('structured_type_3', False),
        ('treatment_type_1', False),
        ('treatment_type_2', False),
        ('treatment_type_3', False),
        ('unitobs', True)
    ))
    available = [
        x for x,y in zip(
            list(obslned.keys()), list(
                obsckbox.values()))
        if y is True
    ]
    countini = ini.InputHandler(
        name='rawinfo',
        tablename='count_table',
        lnedentry=extract(obslned, available),
        checks=obsckbox)
    return countini


@pytest.fixture
def count_handle_2_density():
    obslned = OrderedDict((
        ('spatial_replication_level_2', 'TRANSECT'),
        ('spatial_replication_level_3', 'QUAD'),
        ('spatial_replication_level_4', 'SIDE'),
        ('spatial_replication_level_5', ''),
        ('structured_type_1', ''),
        ('structured_type_2', ''),
        ('structured_type_3', ''),
        ('treatment_type_1', ''),
        ('treatment_type_2', ''),
        ('treatment_type_3', ''),
        ('unitobs', 'DENSITY')
    ))    
    obsckbox = OrderedDict((
        ('spatial_replication_level_2', True),
        ('spatial_replication_level_3', True),
        ('spatial_replication_level_4', True),
        ('spatial_replication_level_5', False),
        ('structured_type_1', False),
        ('structured_type_2', False),
        ('structured_type_3', False),
        ('treatment_type_1', False),
        ('treatment_type_2', False),
        ('treatment_type_3', False),
        ('unitobs', True)
    ))
    available = [
        x for x,y in zip(
            list(obslned.keys()), list(
                obsckbox.values()))
        if y is True
    ]
    countini = ini.InputHandler(
        name='rawinfo',
        tablename='density_table',
        lnedentry=extract(obslned, available),
        checks=obsckbox)
    return countini

@pytest.fixture
def count_handle_3_biomass():
    obslned = OrderedDict((
        ('spatial_replication_level_2', 'plot'),
        ('spatial_replication_level_3', 'quadrat'),
        ('spatial_replication_level_4', ''),
        ('spatial_replication_level_5', ''),
        ('structured_type_1', ''),
        ('structured_type_2', ''),
        ('structured_type_3', ''),
        ('treatment_type_1', ''),
        ('treatment_type_2', ''),
        ('treatment_type_3', ''),
        ('unitobs', 'biomass')
    ))    
    obsckbox = OrderedDict((
        ('spatial_replication_level_2', True),
        ('spatial_replication_level_3', True),
        ('spatial_replication_level_4', False),
        ('spatial_replication_level_5', False),
        ('structured_type_1', False),
        ('structured_type_2', False),
        ('structured_type_3', False),
        ('treatment_type_1', False),
        ('treatment_type_2', False),
        ('treatment_type_3', False),
        ('unitobs', True)
    ))
    available = [
        x for x,y in zip(
            list(obslned.keys()), list(
                obsckbox.values()))
        if y is True
    ]
    countini = ini.InputHandler(
        name='rawinfo',
        tablename='biomass_table',
        lnedentry=extract(obslned, available),
        checks=obsckbox)
    return countini

@pytest.fixture
def biomass_handle_4_percent_cover():
    obslned = OrderedDict((
        ('spatial_replication_level_2', 'block'),
        ('spatial_replication_level_3', 'plot'),
        ('spatial_replication_level_4', ''),
        ('spatial_replication_level_5', ''),
        ('structured_type_1', ''),
        ('structured_type_2', ''),
        ('structured_type_3', ''),
        ('treatment_type_1', ''),
        ('treatment_type_2', ''),
        ('treatment_type_3', ''),
        ('unitobs', 'cover')
    ))    
    obsckbox = OrderedDict((
        ('spatial_replication_level_2', True),
        ('spatial_replication_level_3', True),
        ('spatial_replication_level_4', False),
        ('spatial_replication_level_5', False),
        ('structured_type_1', False),
        ('structured_type_2', False),
        ('structured_type_3', False),
        ('treatment_type_1', False),
        ('treatment_type_2', False),
        ('treatment_type_3', False),
        ('unitobs', True)
    ))
    available = [
        x for x,y in zip(
            list(obslned.keys()), list(
                obsckbox.values()))
        if y is True
    ]
    countini = ini.InputHandler(
        name='rawinfo',
        tablename='percent_cover_table',
        lnedentry=extract(obslned, available),
        checks=obsckbox)
    return countini


@pytest.fixture
def count_handle5():
    obslned = OrderedDict((
        ('spatial_replication_level_2', 'TRANSECT'),
        ('spatial_replication_level_3', ''),
        ('spatial_replication_level_4', ''),
        ('spatial_replication_level_5', ''),
        ('structured_type_1', ''),
        ('structured_type_2', ''),
        ('structured_type_3', ''),
        ('treatment_type_1', ''),
        ('treatment_type_2', ''),
        ('treatment_type_3', ''),
        ('unitobs', '')
    ))    
    obsckbox = OrderedDict((
        ('spatial_replication_level_2', True),
        ('spatial_replication_level_3', False),
        ('spatial_replication_level_4', False),
        ('spatial_replication_level_5', False),
        ('structured_type_1', False),
        ('structured_type_2', False),
        ('structured_type_3', False),
        ('treatment_type_1', False),
        ('treatment_type_2', False),
        ('treatment_type_3', False),
        ('unitobs', True)
    ))
    available = [
        x for x,y in zip(
            list(obslned.keys()), list(
                obsckbox.values()))
        if y is True
    ]
    countini = ini.InputHandler(
        name='rawinfo',
        tablename='individual_table',
        lnedentry=extract(obslned, available),
        checks=obsckbox)
    return countini

# ------------------------------------------------------ #
# ---------------- MergeToUpload Class --------------- #
# ------------------------------------------------------ #

@pytest.fixture
def MergeToUpload():
    class MergeToUpload(object):
        '''
        Class that encapsulated the processes of
        merging, pushing, and updating data for the database.
        All tabels past study_site_table  and part of the project_table
        are managed through this class.
        '''
        print('trying to initiate')
        def __init__(self):
            self.session = orm.Session()
            self.table_types = {
                'taxa_table': orm.taxa_types,
                'count_table': orm.count_types,
                'density_table': orm.density_types,
                'biomass_table': orm.biomass_types,
                'individual_table': orm.individual_types,
                'percent_cover_table': orm.percent_cover_types,
                'project_table': orm.project_types
            }
            self.rawdata = None
            self.metadata_key = None
            self.sitelabel = None
            self.formateddata = None

        def site_in_proj_key_df(
                self, studysitetabledf, projecttabledf, lterlocation,
                observationtabledf, studysitelabel, studysitelevels):
            '''

            Method to take the data stored in the user facade class
            and upload to the database
            REQUIRES: study_site_table, project_table, lter,
            observation_table, study_site_label, studysitelevels...
            to make the site_in_project_table (including the merge)
            as well as merge all other tables for keys and upload.
            To merge the site_in_project_table a series of steps
            must be performed

            1) Check to see if any of the original site levels
            are present in the database

            2) test whether the dataset site levels are contained
            within the raw data or database, or both, and
            make the site_in_project_table site labels based
            off of this test. (this is necessary because if sites are
            already in the database when we pull in the study_site
            table some will be missing since present ones aren't 
            pushed).

            3) Calculate all derived values for the 
            site_in_project_table (sitestartyr, siteendyr, uniquetaxa,
            totalobs).

            4) Push all data

            5) Query the pushed data to retrieve primary keys
            then merged primary keys to sitelevel data and
            return the dataframe (to be merged in another method)
            '''
            self.rawdata = observationtabledf
            self.sitelabel = studysitelabel
            # Types of outcomes to govern push behavior
            all_site_table_data_already_uploaded = False
            site_table_data_partially_uploaded = False
            all_site_table_data_not_yet_uploaded = False

            project_metadat_key = projecttabledf[
                'proj_metadata_key']
            self.metadata_key = int(project_metadat_key)

            study_site_table_query = (
                self.session.query(
                    orm.study_site_table.__table__).
                order_by(
                    orm.study_site_table.__table__.c.study_site_key).
                filter(
                    orm.study_site_table.__table__.c.study_site_key.in_(
                        studysitelevels
                    )
                )
            )
            study_site_table_query_df = read_sql(
                study_site_table_query.statement,
                study_site_table_query.session.bind)
            study_site_table_query_list = study_site_table_query_df[
                'study_site_key'].values.tolist()
            study_site_table_list_from_user = studysitetabledf[
                'study_site_key'].drop_duplicates().values.tolist()

            # ------------------------------------ #
            # ------- study_site_table ------ #
            # ------------------------------------ #
            print('empty', study_site_table_query_df.empty)
            print('nulltest', study_site_table_list_from_user == ['NULL'])
            print('user table', study_site_table_list_from_user)
            # ------------------------------------ #
            # ---------- site_in_project_table --- #
            # ------------------------------------ #
            if (
                    study_site_table_list_from_user == ['NULL']
                    and
                    study_site_table_query_df.empty == False
                ):
                print('ALL Study site data is already stored')
                site_in_proj_levels_to_push = DataFrame(
                    study_site_table_query_df[
                        'study_site_key']).drop_duplicates()
                site_in_proj_levels_to_push = (
                    site_in_proj_levels_to_push[
                        site_in_proj_levels_to_push.study_site_key != 'NULL']
                )
                study_site_levels_derived = (
                    site_in_proj_levels_to_push[
                        'study_site_key'].values.tolist()
                )
                all_site_table_data_already_uploaded = True
                print(site_in_proj_levels_to_push)
                print('all_site_table_data_already_uploaded = True')
            elif (
                    len(
                        [
                            i for i in
                            study_site_table_query_list
                            if i in
                            study_site_table_list_from_user
                        ]
                    ) > 0
                    and
                    (
                        len(study_site_table_query_list) <
                        len(study_site_table_list_from_user)
                    )
            ):
                print('Study site data is partially stored already')
                site_in_proj_levels_to_push = concat(
                    [
                        studysitetabledf,
                        study_site_table_query_df
                    ], axis=0).drop_duplicates()
                site_in_proj_levels_to_push = (
                    site_in_proj_levels_to_push[
                        'study_site_key'].drop_duplicates()
                )
                site_in_proj_levels_to_push = (
                    site_in_proj_levels_to_push[
                        site_in_proj_levels_to_push.
                        study_site_key != 'NULL']
                )
                study_site_levels_derived = (
                    site_in_proj_levels_to_push[
                        'study_site_key'].values.tolist()
                )
                site_table_data_partially_uploaded = True
                print(site_in_proj_levels_to_push)
                print('site_table_data_partially_uploaded = True')

            else:
                print('Study site data is not stored')
                site_in_proj_levels_to_push = DataFrame(
                    studysitetabledf['study_site_key']).drop_duplicates()
                site_in_proj_levels_to_push = (
                    site_in_proj_levels_to_push[
                        site_in_proj_levels_to_push.
                        study_site_key != 'NULL']
                )
                study_site_levels_derived = (
                    site_in_proj_levels_to_push[
                        'study_site_key'].values.tolist()
                )
                all_site_table_data_not_yet_uploaded = True
                print(site_in_proj_levels_to_push)
                print('all_site_table_data_not_yet_uploaded = True')
            try:
                print('loaded site levels: ', studysitelevels)
                print('derived site levels: ', study_site_levels_derived)
                assert (studysitelevels == study_site_levels_derived)
            except Exception as e:
                print(str(e))
                raise AttributeError(
                    'Study site levels derived from query and user ' +
                    'do not match the original site levels stored ' +
                    'in the user facade class: ' + str(e))
            site_in_proj_table_to_push = site_in_proj_levels_to_push
            site_in_proj_table_to_push.columns = (
                ['study_site_table_fkey']
            )
            site_in_proj_table_to_push['sitestartyr'] = 'NA'
            site_in_proj_table_to_push['siteendyr'] = 'NA'
            site_in_proj_table_to_push['totalobs'] = 'NA'
            site_in_proj_table_to_push['uniquetaxaunits'] = -99999
            site_in_proj_table_to_push['project_table_fkey'] = int(
                project_metadat_key)
            print(
                'before deriving records: ', site_in_proj_table_to_push)
            yr_all = []
            for i, item in enumerate(study_site_levels_derived):
                yr_list = observationtabledf[
                    observationtabledf[studysitelabel] == item][
                        'year_derived'].values.tolist()
                yr_list.sort()
                [yr_all.append(x) for x in yr_list]

                try:
                    if len(yr_list) >= 2:
                        site_in_proj_table_to_push.loc[
                            site_in_proj_table_to_push.
                            study_site_table_fkey == item, 'sitestartyr'
                        ] = yr_list[0]
                        site_in_proj_table_to_push.loc[
                            site_in_proj_table_to_push.
                            study_site_table_fkey == item, 'siteendyr'
                        ] = yr_list[-1]
                        site_in_proj_table_to_push.loc[
                            site_in_proj_table_to_push.
                            study_site_table_fkey == item, 'totalobs'
                        ] = len(yr_list)
                    else:
                        site_in_proj_table_to_push.loc[
                            site_in_proj_table_to_push.
                            study_site_table_fkey == item, 'sitestartyr'
                        ] = None
                        site_in_proj_table_to_push.loc[
                            site_in_proj_table_to_push.
                            study_site_table_fkey == item, 'siteendyr'
                        ] = None
                        site_in_proj_table_to_push.loc[
                            site_in_proj_table_to_push.
                            study_site_table_fkey == item, 'totalobs'
                        ] = None
                except Exception as e:
                    print("couldn't update year records")

            session = self.session
            global_id_site_in_project_query = (
                select(
                    [orm.site_in_project_table.__table__.c.project_table_fkey]
                ).distinct()
            )
            session.close()
            global_id_statement = session.execute(
                global_id_site_in_project_query)
            global_id_uploaded_list = [
                x[0] for x in global_id_statement.fetchall()]


            if self.metadata_key in global_id_uploaded_list:
                pass
            else:
                site_in_proj_table_to_push.to_sql(
                    'site_in_project_table', orm.conn,
                    if_exists='append', index=False)
                print('site_in_project_table table UPLOADED')

            session = self.session
            site_in_proj_key_query = select([
                orm.site_in_project_table.__table__.c.site_in_project_key,     
                orm.site_in_project_table.__table__.c.study_site_table_fkey,
                orm.site_in_project_table.__table__.c.project_table_fkey
            ]).where(
                orm.site_in_project_table.project_table_fkey ==
                int(project_metadat_key)
            )
            site_in_proj_key_statement = session.execute(
                site_in_proj_key_query)
            session.close()
            site_in_proj_key_df = DataFrame(
                site_in_proj_key_statement.fetchall())
            site_in_proj_key_df.columns = site_in_proj_key_statement.keys()
            return site_in_proj_key_df

        def merge_for_taxa_table_upload(
                self, formated_taxa_table, siteinprojkeydf,
                sitelabel
        ):
            '''
            Method to take the data stored in the user facade class
            and upload the database
            REQUIRES: formated taxa table (with database names),
            dataframe with site levels merged to site_in_project
            (formated_taxa_table)
            primary keys (created in method above...siteinprojkeydf)
            , and the name of the column with the site (sitelabel)
            to make the site_in_project_table (including the merge)
            as well as merge all other tables for keys and upload.
            To merge the site_in_project_table a series of steps
            must be performed

            1) Merged the formated taxa table with the site_in_project
            data that contains primary keys for site_in_project table
            and site levels (merge on site levels)

            2) Dropping columns not neccessary for the taxa_table
            push (metadata key: project_table_fkey,
            site label:study_site_table_fkey)

            3) Rename merged site_in_project_table primary key
            to match taxa table name

            4) Push taxa_table to database

            '''

            print('starting taxa table upload')
            orm.replace_numeric_null_with_string(formated_taxa_table)
            print('past orm replace numeric')
            print('siteingproj key df: ', siteinprojkeydf)
            print('siteingproj key df: ', siteinprojkeydf.columns)
            print('formatted taxa df: ', formated_taxa_table)
            print('formatted taxa df: ', formated_taxa_table.columns)

            tbl_taxa_with_site_in_proj_key = merge(
                formated_taxa_table, siteinprojkeydf,
                left_on=sitelabel,
                right_on='study_site_table_fkey',
                how='inner')
            print('past tbl_taxa site in proj key')
            tbl_taxa_merged = tbl_taxa_with_site_in_proj_key.copy()

            tbl_taxa_merged.drop([
                'study_site_table_fkey', sitelabel,
                'project_table_fkey'], inplace=True, axis=1)
            print('past tbl_taxa drop: ', tbl_taxa_merged)
            tbl_taxa_merged.rename(
                columns={
                    'site_in_project_key': 'site_in_project_taxa_key'}, inplace=True)
            print('merge class taxa merged: ', tbl_taxa_merged)

            tbl_taxa_merged.fillna('NA', inplace=True)
            orm.convert_types(tbl_taxa_merged, orm.taxa_types)

            session = self.session
            site_in_proj_key_query = session.execute(
                select(
                    [orm.taxa_table.__table__.c.site_in_project_taxa_key]
                ).
                distinct()
            )
            session.close()

            check_site_in_proj_keys = DataFrame(site_in_proj_key_query.fetchall())
            if check_site_in_proj_keys.empty:
                check_site_in_proj_keys = []
            else:
                check_site_in_proj_keys = check_site_in_proj_keys[0].values.tolist()


            if all(
                    x in check_site_in_proj_keys
                    for x in
                    siteinprojkeydf['site_in_project_key'].values.tolist()):
                pass
            else:
                tbl_taxa_merged.to_sql(
                    'taxa_table', orm.conn, if_exists='append', index=False)

        def merge_for_datatype_table_upload(
                self, raw_dataframe,
                formated_dataframe,
                formated_dataframe_name,
                covariate_dataframe,
                siteinprojkeydf,
                raw_data_taxa_columns,
                uploaded_taxa_columns):

            print('start dtype upload')
            orm.replace_numeric_null_with_string(raw_dataframe)
            orm.replace_numeric_null_with_string(formated_dataframe)
            print('replacing nulls is a pain')

            # Step 2) Query taxa_table to get the auto generated
            # primary keys returned. Turn query data into
            # dataframe.
            session = self.session
            taxa_key_statement = session.execute(
                select([orm.taxa_table]).
                where(
                    orm.taxa_table.__table__.c.site_in_project_taxa_key.in_
                    (siteinprojkeydf['site_in_project_key'].values.tolist())
                )
            )
            session.close()
            taxa_key_df = DataFrame(taxa_key_statement.fetchall())
            taxa_key_df.columns = taxa_key_statement.keys()
            taxa_key_df.replace({None: 'NA'}, inplace=True)

            # Step 3) Subsetting the query tabled for record that only pertain
            # to the count data (because we will be subsetting from this
            # queried taxa table later)
            dtype_subset_taxa_key_df = taxa_key_df[
                taxa_key_df['site_in_project_taxa_key'].isin(
                    siteinprojkeydf['site_in_project_key'])]

            # Step 4) Merge the taxa_table query results with
            # the site_in_project table query that was performed
            # to upload the taxa_table (see above). This gives
            # you a table with site names and taxonomic information
            # allowing for a merge with the original dtype data
            tbl_dtype_merged_taxakey_siteinprojectkey = merge(
                dtype_subset_taxa_key_df, siteinprojkeydf,
                left_on='site_in_project_taxa_key',
                right_on='site_in_project_key', how='inner')

            raw_dataframe_siteinproj = merge(
                raw_dataframe, siteinprojkeydf,
                left_on=self.sitelabel, right_on='study_site_table_fkey',
                sort=False, how='left')

            raw_data_taxa_columns.append('site_in_project_key')
            uploaded_taxa_columns.append('site_in_project_taxa_key')

            raw_data_taxa_columns.append('site_in_project_key')
            uploaded_taxa_columns.append('site_in_project_taxa_key')

            print('updated raw data col list: ', raw_dataframe_siteinproj)
            print('update taxa data col list: ', uploaded_taxa_columns)
            # Step 5) Merge the original dtype data with the
            # merged taxa_table query to have all foreign keys...
            # taxa and site_project
            # matched up with the original observations.
            dtype_merged_with_taxa_and_siteinproj_key = merge(
                raw_dataframe_siteinproj,
                tbl_dtype_merged_taxakey_siteinprojectkey,
                left_on=list(raw_data_taxa_columns),
                right_on=list(uploaded_taxa_columns),
                how='left')

            print("PAST MEGERED STEP 5")
            
            # Step 6) Take the merged original data with all foreign keys,
            # and merged that with the formatted dtype_table based on index
            # values (order or records should not changed from the original data
            # to the formatted data)
            tbl_dtype_merged_with_all_keys = merge(
                formated_dataframe,
                dtype_merged_with_taxa_and_siteinproj_key,
                left_index=True, right_index=True, how='inner',
                suffixes=('', '_y'))

            print("PAST MEGERED STEP 6")
            
            # Step 7) List the columns that will be needed to push the
            # dtype table to the database (including foreign keys)
            tbl_dtype_columns_to_upload = [
                'taxa_table_key', 'site_in_project_taxa_key', 'year_derived',
                'month_derived', 'day_derived', 'spatial_replication_level_1',
                'spatial_replication_level_2', 'spatial_replication_level_3',
                'spatial_replication_level_4', 'spatial_replication_level_5',
                'structure_type_1', 'structure_type_2',
                'structure_type_3',
                'treatment_type_1', 'treatment_type_2',
                'treatment_type_3',
                'covariates'
            ]
            time_cols_rename = {
                'year_derived': 'year',
                'month_derived': 'month',
                'day_derived': 'day'
            }
            print('BEFORE MERGE WITH COVARIATES')
            
            tbl_dtype_columns_to_upload.append(
                '{}_observation'.format(str(formated_dataframe_name)))
            tbl_dtype_merged_with_all_keys = concat(
                [tbl_dtype_merged_with_all_keys, covariate_dataframe],
                axis=1)
            print('ALL KEYS: ', tbl_dtype_merged_with_all_keys.columns)
            print('COVAR: ', covariate_dataframe.columns)
            print("PAST MEGERED STEP 7")
            
            # Step 8) Subsetting the fully merged dtype table data
            tbl_dtype_to_upload = tbl_dtype_merged_with_all_keys[
                tbl_dtype_columns_to_upload]
            tbl_dtype_to_upload.rename(
                columns=time_cols_rename, inplace=True
            )
            print('tbl dtype to upload: ', tbl_dtype_to_upload.columns)
            print("PAST MEGERED STEP 8")
            
            # Step 9) Renaming columns to reflect that in database table
            # And converting data types
            tbl_dtype_to_upload.rename(columns={
                'taxa_table_key': 'taxa_{}_fkey'.format(str(formated_dataframe_name))}
                , inplace=True)
            datatype_key = 'site_in_project_{}_fkey'.format(str(formated_dataframe_name))
            tbl_dtype_to_upload.rename(columns={
                'site_in_project_taxa_key': datatype_key}, inplace=True)
            tbl_dtype_to_upload.fillna('NA', inplace=True)
            self.formateddata = tbl_dtype_to_upload
            print("PAST MEGERED STEP 9")

            # Step 10) Uploading to the database
            datatype_table = '{}_table'.format(str(formated_dataframe_name))
            datatype_obs = '{}_observation'.format(str(formated_dataframe_name))
            print('push raw_before', tbl_dtype_to_upload.columns)

            tbl_dtype_to_upload[datatype_obs] = to_numeric(
                tbl_dtype_to_upload[datatype_obs], errors='coerce'
            )

            print("PAST MEGERED STEP 10")
            
            text_cols = [
                'spatial_replication_level_1', 'spatial_replication_level_2',
                'spatial_replication_level_3', 'spatial_replication_level_4',
                'spatial_replication_level_5', 'treatment_type_1',
                'treatment_type_2', 'treatment_type_3',
                'structure_type_1', 'structure_type_2', 'structure_type_3'
            ]
            tbl_dtype_to_upload[text_cols] = tbl_dtype_to_upload[
                text_cols].applymap(str)
            tbl_dtype_to_upload[text_cols] = tbl_dtype_to_upload[
                text_cols].applymap(lambda x: x.strip())

            print("PAST MEGERED STEP 8")
            try:
                orm.convert_types(tbl_dtype_to_upload, self.table_types[datatype_table])
            except Exception as e:
                print('converting issues: ', str(e))
            print("PAST MEGERED STEP CONVERT TYPES")
            print('this should have worked')


            other_numerics = [
                'year', 'month', 'day', datatype_key,
                'taxa_{}_fkey'.format(str(formated_dataframe_name))
            ]

            tbl_dtype_to_upload[datatype_obs] = to_numeric(
                tbl_dtype_to_upload[datatype_obs], errors='coerce'
            )

            try:
                tbl_dtype_to_upload[other_numerics].replace({'NA', -99999}, inplace=True)
            except Exception as e:
                print('No NAs to replace:', str(e))
            try:
                tbl_dtype_to_upload[other_numerics].replace({'NaN' -99999}, inplace=True)
            except Exception as e:
                print('No NaN to replace:', str(e))
            try:
                tbl_dtype_to_upload[other_numerics].replace({None, -99999}, inplace=True)
            except Exception as e:
                print('No None to replace:', str(e))
            tbl_dtype_to_upload[other_numerics].fillna(-99999, inplace=True)


            tbl_dtype_to_upload.loc[:, other_numerics] = tbl_dtype_to_upload.loc[
                :, other_numerics].apply(to_numeric, errors='coerce')

            tbl_dtype_to_upload.to_sql(
                datatype_table,
                orm.conn, if_exists='append', index=False)
            print('past datatype upload')

        def update_project_table(
                self,
                spatial_rep_columns_from_og_df,
                spatial_rep_columns_from_formated_df):
            '''
            Methods to update the projcet table with information
            that was gathered toward the end of a user session
            Arguments are the column names for 
            the different levels of spatial replication that
            are present (key/value pairs)
            '''
            ##
            # ADD STUDYSTARTYR, STUDYENDYR, SPAT_LEV_UNQ_REPS(1-5),
            # SPAT_LEV_LABELS(1-5)
            ##
            spatial_index = [
                i for i, item in enumerate(
                    spatial_rep_columns_from_formated_df)
                if 'spatial' in item
            ]
            spatial_label_col = ['spatial_replication_level_1_label']
            spatial_label_val = [self.sitelabel]
            spatial_uq_num_of_rep_col = [
                'spatial_replication_level_1_number_of_unique_reps']
            spatial_uq_num_of_rep_val = [
                len(self.rawdata[self.sitelabel].unique())
                ]
            for i in range(len(spatial_index)):
                spatial_label_col.append(
                    spatial_rep_columns_from_formated_df[i] + '_label')
                spatial_label_val.append(
                    spatial_rep_columns_from_og_df[i])
                spatial_uq_num_of_rep_col.append(
                    spatial_rep_columns_from_formated_df[i] +
                    '_number_of_unique_reps')
                spatial_uq_num_of_rep_val.append(
                    len(
                        self.rawdata[
                            spatial_rep_columns_from_og_df[i]].unique()
                    )
                )
            print(self.formateddata.columns)
            print(self.formateddata)
            print('Populating update_dict')
            update_dict = {
                'studystartyr': self.formateddata.loc[:, 'year'].min(),
                'studyendyr': self.formateddata.loc[:, 'year'].max()
            }
            for i, item in enumerate(spatial_label_col):
                update_dict[item] = spatial_label_val[i]
                update_dict[spatial_uq_num_of_rep_col[i]] = spatial_uq_num_of_rep_val[i]
            print(self.metadata_key)
            print('startyear: ',update_dict['studystartyr'])
            print('endyear: ', update_dict['studyendyr'])
            orm.conn.execute(
                update(orm.project_table).
                where(
                    column('proj_metadata_key') == self.metadata_key).
                values(update_dict)
            )
    return MergeToUpload


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
                    dfstate = read_csv(
                        self.inputoptions[
                            '.csv']['filename']
                        )
                elif (
                        self.file_id.ext == '.xls' or
                        self.file_id.ext == '.xlsx'):
                    dfstate = read_excel(
                        self.inputoptions[
                            'xlsx']['filename'],
                        sheetname=self.inputoptions[
                            'xlsx']['sheet']
                        )
                elif self.file_id.ext == '.txt':
                    dfstate = read_table(
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
                dfstate.fillna('NA',inplace=True)
                for i, item in enumerate(dfstate.columns):
                    if isinstance(
                            dfstate.dtypes.values.tolist()[i],
                            object):
                        try:
                            dfstate.loc[:, item] = dfstate.loc[
                                :,item].str.rstrip()
                            na_vals = [
                                9999, 99999, 999999,
                                -9999, -99999, -999999,
                                -8888, -88888, -88888, -888
                            ]
                            na_vals_float = [
                                9999.0, 99999.0, 999999.0,
                                -9999.0, -99999.0, -999999.0
                                -8888.0, -88888.0, -888888.0,
                                -888.0
                            ]
                            na_text_vals = [
                                '9999', '99999', '999999',
                                '-9999', '-99999', '-999999',
                                '-8888', '-88888', '-888888',
                                '-888'
                            ]
                            for j,text_val in enumerate(
                                    na_text_vals):
                                if (
                                        (
                                            dfstate[item].dtypes
                                            == int)
                                        or
                                        (
                                            dfstate[item].dtypes
                                            == float)):
                                    dfstate[item].replace(
                                        {na_vals[j]: 'NA'},
                                        inplace=True)
                                    dfstate[item].replace(
                                        {na_vals_float[j]: 'NA'},
                                        inplace=True)
                                else:
                                    dfstate[item].replace(
                                        {text_val: 'NA'},
                                        inplace=True)
                        except:
                            print('error trying to set predefined nulls')
                    else:
                            pass
                dfstate = dfstate[
                    dfstate.isnull().all(axis=1) != True]
                memento = Memento(dfstate= dfstate,
                            state= self.state)
                return memento
            except Exception as e:
                print(str(e))
                raise IOError('Cannot read in file: ' + str(e))

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
                return self._statelogbook[self._statelist.pop()]
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
            self._dfstate = DataFrame(dfstate).copy()
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
def df_test_1():
    return read_csv(
        rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
        'raw_data_test_1.csv'
    )

@pytest.fixture
def df_test_2():
    return read_csv(
        rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
        'raw_data_test_2.csv'
    )

@pytest.fixture
def df_test_3():
    return read_csv(
        rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
        'raw_data_test_3.csv'
    )

@pytest.fixture
def df_test_4():
    return read_csv(
        rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
        'raw_data_test_4.csv'
    )

@pytest.fixture
def df_test_5():
    return read_csv(
        rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
        'raw_data_test_5.csv'
    )
