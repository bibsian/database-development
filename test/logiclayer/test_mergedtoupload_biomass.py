#! /usr/bin/env python
import pytest
from pandas import concat
import re
from collections import OrderedDict
import sys, os
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
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI import class_inputhandler as ini
from poplerGUI.logiclayer import class_timeparse as tparse
from poplerGUI.logiclayer.class_helpers import (
    string_to_list, extract, produce_null_df
    )
from poplerGUI.logiclayer import class_dictionarydataframe as ddf

def test_drop_records():

    table_dict = OrderedDict([
        ('biomass_table', orm.biomass_table),
        ('count_table', orm.count_table),
        ('density_table', orm.density_table),
        ('individual_table', orm.individual_table),
        ('percent_cover_table', orm.percent_cover_table),
        ('taxa_accepted_table', orm.taxa_accepted_table),
        ('site_in_project_table', orm.site_in_project_table),
        ('taxa_table', orm.taxa_table),
        ('project_table', orm.project_table),
        ('study_site_table', orm.study_site_table)]
    )

    for i, item in enumerate(table_dict):
        print(i)
        print('item', item)
        delete_statement = table_dict[item].__table__.delete()
        
        orm.conn.execute(delete_statement)

# ------------------------------------------------------ #
# ---------------- meta data handle --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def meta_handle():
    lentry = {
        'globalid': 3,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset.cgi?docid=knb-lter-sbc.19'),
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
def file_handle():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {'sheet': '', 'delim': '', 'tskip': '', 'bskip': ''}
    fileinput = ini.InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename=(
            rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
            'raw_data_test_3.csv'))

    return fileinput


# ------------------------------------------------------ #
# ---------------- Study site handle --------------- #
# ----------------------------------------------------- #
@pytest.fixture
def site_handle():
    lned = {'study_site_key': 'site'}
    sitehandle = ini.InputHandler(
        name='siteinfo', lnedentry=lned, tablename='study_site_table')
    return sitehandle

# ------------------------------------------------------ #
# ---------------- Project table handle --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def project_handle():
    main_input = ini.InputHandler(
        name='maininfo', tablename='project_table')
    return main_input

# ------------------------------------------------------ #
# ---------------- taxa table handle --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def taxa_handle():
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

# ------------------------------------------------------ #
# ---------------- time handle --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def time_handle():
    d = {
        'dayname': '',
        'dayform': 'NULL',
        'monthname': 'month',
        'monthform': 'mm',
        'yearname': 'year',
        'yearform': 'YYYY',
        'jd': False,
        'mspell': False
    }

    timeini = ini.InputHandler(
        name='timeinfo', tablename='timetable',
        lnedentry= d)
    return timeini

# ------------------------------------------------------ #
# ---------------- covar handle --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def covar_handle():
    covarlned = {'columns': None}
    
    covarlned['columns'] = string_to_list('temp')

    covarini = ini.InputHandler(
        name='covarinfo', tablename='covartable',
        lnedentry=covarlned)

    return covarini



# ------------------------------------------------------ #
# ---------------- obs table handle --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def count_handle():
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

def test_drop_records():

    table_dict = OrderedDict([
        ('biomass_table', orm.biomass_table),
        ('count_table', orm.count_table),
        ('density_table', orm.density_table),
        ('individual_table', orm.individual_table),
        ('percent_cover_table', orm.percent_cover_table),
        ('taxa_table', orm.taxa_table),
        ('site_in_project_table', orm.site_in_project_table),
        ('project_table', orm.project_table),
        ('study_site_table', orm.study_site_table)]
    )

    for i, item in enumerate(table_dict):
        print(i)
        print('item', item)
        delete_statement = table_dict[item].__table__.delete()
        
        orm.conn.execute(delete_statement)


def test_site_in_project_key(
        MergeToUpload, site_handle, file_handle,
        meta_handle, project_handle, taxa_handle,
        time_handle, count_handle, covar_handle):
    facade = face.Facade()

    facade.input_register(meta_handle)
    facade.meta_verify()

    facade.input_register(file_handle)
    facade.load_data()

    facade.input_register(site_handle)
    sitedirector = facade.make_table('siteinfo')
    study_site_table = sitedirector._availdf

    print('study_site_table (test): ', study_site_table)

    facade.create_log_record('study_site_table')
    lter = meta_handle.lnedentry['lter']
    ltercol = produce_null_df(1, [
        'lter_table_fkey'], len(study_site_table), lter)
    study_site_table = concat([study_site_table, ltercol], axis=1)
    print('study_site_table: ', study_site_table)
    facade.push_tables['study_site_table'] = study_site_table
    
    siteid = site_handle.lnedentry['study_site_key']
    sitelevels = facade._data[
        siteid].drop_duplicates().values.tolist()
    facade.register_site_levels(sitelevels)
    facade._valueregister['siteid'] = siteid

    facade.input_register(project_handle)
    maindirector = facade.make_table('maininfo')
    project_table = maindirector._availdf.copy().reset_index(drop=True)
    orm.convert_types(project_table, orm.project_types)
    
    facade.push_tables['project_table'] = project_table
    facade.create_log_record('project_table')
    
    facade.input_register(taxa_handle)
    taxadirector = facade.make_table('taxainfo')
    taxa_table = taxadirector._availdf
    facade.push_tables['taxa_table'] = taxa_table
    facade.create_log_record('taxa_table')
    
    facade.input_register(time_handle)
    timetable = tparse.TimeParse(
        facade._data, time_handle.lnedentry).formater()
    facade.push_tables['timetable'] = timetable
    facade.create_log_record('timetable')

    facade.input_register(count_handle)
    rawdirector = facade.make_table('rawinfo')
    rawtable = rawdirector._availdf
    print(rawtable)
    facade.push_tables[count_handle.tablename] = rawtable
    facade.create_log_record(count_handle.tablename)

    facade.input_register(covar_handle)
    covartable = ddf.DictionaryDataframe(
        facade._data,
        covar_handle.lnedentry['columns']).convert_records()
    facade.push_tables['covariates'] = covartable
    facade.create_log_record('covartable')

    facade._valueregister['globalid'] = meta_handle.lnedentry['globalid']
    facade._valueregister['lter'] = meta_handle.lnedentry['lter']
    facade._valueregister['siteid'] = siteid

    timetable_og_cols = timetable.columns.values.tolist()
    timetable.columns = [x+'_derived' for x in timetable_og_cols]
    observationdf = facade._data
    observation_time_df = concat([timetable,observationdf], axis=1 )
    
    print('merge class obs_time columns: ', observation_time_df.columns)
    print('merge class project table: ', project_table)
    
    try:
        study_site_table.to_sql(
            'study_site_table',
            orm.conn, if_exists='append', index=False)
    except Exception as e:
        print(str(e))

    project_table.to_sql(
        'project_table', orm.conn,
        if_exists='append', index=False
    )

    merge_object = MergeToUpload()
    site_in_project_key_df = merge_object.site_in_proj_key_df(
        studysitetabledf=study_site_table,
        projecttabledf=project_table,
        observationtabledf=observation_time_df,
        lterlocation= facade._valueregister['lter'],
        studysitelabel=siteid,
        studysitelevels=sitelevels
    )

    merge_object.merge_for_taxa_table_upload(
        formated_taxa_table=taxa_table,
        siteinprojkeydf=site_in_project_key_df,
        sitelabel=siteid
    )

    taxa_column_in_data = [
        x[1] for x in 
        list(facade._inputs['taxainfo'].lnedentry.items())
    ]

    taxa_column_in_push_table = [
        x[0] for x in 
        list(facade._inputs['taxainfo'].lnedentry.items())
    ]

    merge_object.merge_for_datatype_table_upload(
        raw_dataframe=observation_time_df,
        formated_dataframe=rawtable,
        formated_dataframe_name=
        '{}'.format(
                    re.sub('_table', '', facade._inputs['rawinfo'].tablename)),
        covariate_dataframe = covartable,
        siteinprojkeydf=site_in_project_key_df,
        raw_data_taxa_columns=taxa_column_in_data,
        uploaded_taxa_columns=taxa_column_in_push_table
    )
