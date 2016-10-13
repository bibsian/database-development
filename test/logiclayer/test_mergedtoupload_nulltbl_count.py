#! /usr/bin/env python
import pytest
from pandas import merge, concat, DataFrame, read_sql
from sqlalchemy import select
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


@pytest.fixture
def meta_handle2():
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
def file_handle2():
    ckentry = {}
    rbtn = {'.csv': True, '.txt': False,
            '.xlsx': False}
    lned = {'sheet': '', 'delim': '', 'tskip': '', 'bskip': ''}
    fileinput = ini.InputHandler(
        name='fileoptions',tablename=None, lnedentry=lned,
        rbtns=rbtn, checks=ckentry, session=True,
        filename=(
            rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
            'raw_data_test_1.csv'))

    return fileinput


# ------------------------------------------------------ #
# ---------------- Study site handle --------------- #
# ----------------------------------------------------- #
@pytest.fixture
def site_handle2():
    lned = {'study_site_key': 'site'}
    sitehandle = ini.InputHandler(
        name='siteinfo', lnedentry=lned, tablename='study_site_table')
    return sitehandle

# ------------------------------------------------------ #
# ---------------- Project table handle --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def project_handle2():
    main_input = ini.InputHandler(
        name='maininfo', tablename='project_table')
    return main_input

# ------------------------------------------------------ #
# ---------------- taxa table handle --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def taxa_handle2():
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

# ------------------------------------------------------ #
# ---------------- time handle --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def time_handle2():
    d = {
        'dayname': 'date',
        'dayform': 'dd-mm-YYYY (Any Order)',
        'monthname': 'date',
        'monthform': 'dd-mm-YYYY (Any Order)',
        'yearname': 'date',
        'yearform': 'dd-mm-YYYY (Any Order)',
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
def covar_handle2():
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
def count_handle2():
    obslned = OrderedDict((
        ('spatial_replication_level_2', 'transect'),
        ('spatial_replication_level_3', ''),
        ('spatial_replication_level_4', ''),
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

    
def test_site_in_project_key_number_two(
        MergeToUpload, site_handle2, file_handle2,
        meta_handle2, project_handle2, taxa_handle2,
        time_handle2, count_handle2, covar_handle2):
    facade = face.Facade()
    
    facade.input_register(meta_handle2)
    facade.meta_verify()

    facade.input_register(file_handle2)
    facade.load_data()

    facade.input_register(site_handle2)
    sitedirector = facade.make_table('siteinfo')
    study_site_table = sitedirector._availdf

    siteid = site_handle2.lnedentry['study_site_key']
    sitelevels = facade._data[
        siteid].drop_duplicates().values.tolist()
    facade.register_site_levels(sitelevels)
    print('test2 sitelevels: ', sitelevels)
    facade._valueregister['siteid'] = siteid

    print('study_site_table (test): ', study_site_table)

    facade.create_log_record('study_site_table')
    lter = meta_handle2.lnedentry['lter']
    ltercol = produce_null_df(1, [
        'lter_table_fkey'], len(study_site_table), lter)
    study_site_table = concat([study_site_table, ltercol], axis=1)
    study_site_table_og_col = study_site_table.columns.values.tolist()

    study_site_table_single = study_site_table.iloc[0, :]

    study_site_table_single_df = DataFrame([study_site_table_single])
    study_site_table_single_df.columns = study_site_table_og_col

    print('study site single: ', study_site_table_single)
    
    study_site_table_single_df.loc[0, 'study_site_key'] = 'NULL'

    print('study_site_table: ', study_site_table_single_df)

    facade.push_tables['study_site_table'] = study_site_table_single_df


    facade.input_register(project_handle2)
    maindirector = facade.make_table('maininfo')
    project_table = maindirector._availdf.copy().reset_index(drop=True)
    orm.convert_types(project_table, orm.project_types)
    
    facade.push_tables['project_table'] = project_table
    facade.create_log_record('project_table')


    facade.input_register(taxa_handle2)
    taxadirector = facade.make_table('taxainfo')
    
    taxa_table = taxadirector._availdf
    facade.push_tables['taxa_table'] = taxa_table
    print('taxa columns after make taxa table: ', taxa_table.columns)

    facade.create_log_record('taxa_table')
    
    print('taxa columns before time_table: ', taxa_table.columns)
    
    facade.input_register(time_handle2)
    timetable = tparse.TimeParse(
        facade._data, time_handle2.lnedentry).formater()
    facade.push_tables['timetable'] = timetable
    facade.create_log_record('timetable')

    print('taxa columns before count_table: ', taxa_table.columns)
    facade.input_register(count_handle2)
    rawdirector = facade.make_table('rawinfo')
    rawtable = rawdirector._availdf
    print(rawtable)
    facade.push_tables[count_handle2.tablename] = rawtable
    facade.create_log_record(count_handle2.tablename)

    print('taxa columns before covar_table: ', taxa_table.columns)
    facade.input_register(covar_handle2)
    covartable = ddf.DictionaryDataframe(
        facade._data,
        covar_handle2.lnedentry['columns']).convert_records()
    facade.push_tables['covariates'] = covartable
    facade.create_log_record('covartable')

    facade._valueregister['globalid'] = meta_handle2.lnedentry['globalid']
    facade._valueregister['lter'] = meta_handle2.lnedentry['lter']
    facade._valueregister['siteid'] = siteid

    timetable_og_cols = timetable.columns.values.tolist()
    timetable.columns = [x+'_derived' for x in timetable_og_cols]
    observationdf = facade._data
    observation_time_df = concat([timetable,observationdf], axis=1 )
    
    print('merge class obs_time columns: ', observation_time_df.columns)
    print('merge class project table: ', project_table)
    
    study_site_table.to_sql(
        'study_site_table',
        orm.conn, if_exists='append', index=False)

    project_table.to_sql(
        'project_table', orm.conn,
        if_exists='append', index=False
    )

    print('taxa columns before site_in_proj method: ', taxa_table.columns)
    
    merge_object = MergeToUpload()
    site_in_project_key_df = merge_object.site_in_proj_key_df(
        studysitetabledf=study_site_table,
        projecttabledf=project_table,
        observationtabledf=observation_time_df,
        lterlocation= facade._valueregister['lter'],
        studysitelabel=siteid,
        studysitelevels=sitelevels
    )

    print('taxa columns before user taxa merge method: ', taxa_table.columns)
    merge_object.merge_for_taxa_table_upload(
        formated_taxa_table=taxa_table,
        siteinprojkeydf=site_in_project_key_df,
        sitelabel=siteid
    )
    
    
    taxa_column_in_data = [
        x[0] for x in 
        list(facade._inputs['taxainfo'].lnedentry.items())
    ]

    taxa_column_in_push_table = [
        x[1] for x in 
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

