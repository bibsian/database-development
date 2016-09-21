#! /usr/bin/env python
import pytest
from pandas import concat
import re
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
from collections import OrderedDict
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI.logiclayer.class_helpers import (
    string_to_list, extract, produce_null_df
    )
from poplerGUI.logiclayer.datalayer import config as orm
from poplerGUI.logiclayer import class_mergedtoupload as mrg
from poplerGUI import class_inputhandler as ini
from poplerGUI.logiclayer import class_timeparse as tparse
from poplerGUI.logiclayer import class_dictionarydataframe as ddf

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


# ------------------------------------------------------ #
# ---------------- meta data handle --------------- #
# ------------------------------------------------------ #
@pytest.fixture
def meta_handle():
    lentry = {
        'globalid': 1,
        'metaurl': ('http://sbc.lternet.edu/cgi-bin/showDataset.cgi?docid=knb-lter-sbc.18'),
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
            'raw_data_test_1.csv'))

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
def time_handle():
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

    countini = ini.InputHandler(
        name='rawinfo',
        tablename='count_table',
        lnedentry=extract(obslned, available),
        checks=obsckbox)

    return countini

@pytest.fixture
def Facade_push():
    class Facade_push(face.Facade):
        def __init__(self):
            face.Facade.__init__(self)


        def push_merged_data(self):
            '''
            Method in facade class to check if all data tables
            have been completed by the user (although
            site table can be empty if records are already in the 
            database).
            '''


            # Tables created from use input
            study_site_table_df = self.push_tables['study_site_table']
            #study_site_table_df[].fillna('NA', inplace=True)
            project_table_df = self.push_tables['project_table']
            taxa_table_df = self.push_tables['taxa_table']
            time_table_df = self.push_tables['timetable']
            observation_table_df = self.push_tables[
                self._inputs['rawinfo'].tablename]
            observation_table_name = self._inputs['rawinfo'].tablename
            covariate_table_df = self.push_tables['covariates']
            site_levels = self._valueregister['sitelevels']
            site_location = self._valueregister['siteid']
            lter = self._valueregister['lterid']
            # -------------------------------------- #
            # --- Pushing study site table data --- #
            # -------------------------------------- #

            if self.sitepushed is None:
                try:
                    study_site_table_df.to_sql(
                        'study_site_table',
                        orm.conn, if_exists='append', index=False)
                    self.sitepushed = True
                except Exception as e:
                    print(str(e))
                    self._tablelog['study_site_table'].debug(str(e))
                    raise ValueError(
                        'Could not push study site table data: ' + str(e)
                        )

            # -------------------------------------- #
            # --- Pushing project table data --- #
            # -------------------------------------- #
            if self.mainpushed is None:
                try:
                    project_table_df.to_sql(
                        'project_table', orm.conn,
                        if_exists='append', index=False
                    )
                    self.mainpushed = True
                except Exception as e:
                    print(str(e))
                    self._tablelog['project_table'].debug(str(e))
                    raise ValueError(
                        'Could not push project table data: ' + str(e)
                    )
            else:
                pass
            # -------------------------------------- #
            # --- Pushing site in project table data --- #
            # -------------------------------------- #
            if self.siteinproject is None:
                pass
            else:
                pass

            merge_object = mrg.MergeToUpload()
            site_in_project_key_df = merge_object.site_in_proj_key_df(
                studysitetabledf=study_site_table_df,
                projecttabledf=project_table_df,
                observationtabledf=time_table_df,
                lterlocation=lter,
                studysitelabel=site_location,
                studysitelevels=site_levels
            )

###
            merge_object.merge_for_taxa_table_upload(
                formated_taxa_table=taxa_table_df,
                siteinprojkeydf=site_in_project_key_df,
                sitelabel=site_location
            )
            
            taxa_column_in_data = [
                x[0] for x in 
                list(self._inputs['taxainfo'].lnedentry.items())
            ]

            taxa_column_in_push_table = [
                x[1] for x in 
                list(self._inputs['taxainfo'].lnedentry.items())
            ]
            print('past taxa')
            merge_object.merge_for_datatype_table_upload(
                raw_dataframe=time_table_df,
                formated_dataframe=observation_table_df,
                formated_dataframe_name=
                '{}'.format(
                            re.sub('_table', '', self._inputs['rawinfo'].tablename)),
                covariate_dataframe = covariate_table_df,
                siteinprojkeydf=site_in_project_key_df,
                raw_data_taxa_columns=taxa_column_in_data,
                uploaded_taxa_columns=taxa_column_in_push_table
            )

    return Facade_push

def test(
        Facade_push, site_handle, file_handle,
        meta_handle, project_handle, taxa_handle,
        time_handle, count_handle, covar_handle):
    facade = Facade_push()
    facade.input_register(meta_handle)
    facade.meta_verify()

    facade.input_register(file_handle)
    facade.load_data()

    facade.input_register(site_handle)
    sitedirector = facade.make_table('siteinfo')
    study_site_table = sitedirector._availdf


    study_site_table['lter_table_fkey'] = facade._valueregister[
        'globalid'] = meta_handle.lnedentry['lter']
    print(study_site_table)

    facade.push_tables['study_site_table'] = study_site_table

    siteid = site_handle.lnedentry['study_site_key']
    sitelevels = facade._data[
        siteid].drop_duplicates().values.tolist()
    facade.register_site_levels(sitelevels)

    
    facade.input_register(project_handle)
    maindirector = facade.make_table('maininfo')
    project_table = maindirector._availdf.copy().reset_index(drop=True)
    orm.convert_types(project_table, orm.project_types)
    facade.push_tables['project_table'] =  project_table
    print('project table: ', project_table)

    facade.input_register(taxa_handle)
    taxadirector = facade.make_table('taxainfo')
    facade.push_tables['taxa_table'] = taxadirector._availdf

    facade.input_register(time_handle)
    timetable = tparse.TimeParse(
        facade._data, time_handle.lnedentry).formater()
    timetable_og_cols = timetable.columns.values.tolist()
    timetable.columns = [x+'_derived' for x in timetable_og_cols]
    observationdf = facade._data
    observation_time_df = concat([timetable,observationdf], axis=1 )

    facade.push_tables['timetable'] = observation_time_df

    facade.input_register(count_handle)
    rawdirector = facade.make_table('rawinfo')
    facade.push_tables[facade._inputs[
        'rawinfo'].tablename] = rawdirector._availdf

    facade.input_register(covar_handle)
    covartable = ddf.DictionaryDataframe(
        facade._data,
        covar_handle.lnedentry['columns']).convert_records()
    facade.push_tables['covariates'] = covartable

    facade._valueregister['globalid'] = meta_handle.lnedentry['globalid']
    facade._valueregister['lter'] = meta_handle.lnedentry['lter']
    facade._valueregister['siteid'] = facade._inputs[
        'siteinfo'].lnedentry['study_site_key']

    facade.push_merged_data()
