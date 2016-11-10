import pytest
from pandas import merge, concat, DataFrame, read_sql
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
        'globalid': 6,
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
def file_handle_split_columns():
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
            'splitcolumn_data_test.csv'))
    return fileinput

@pytest.fixture
def file_handle_wide_to_long():
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


