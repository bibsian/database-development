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

@pytest.fixture
def MergeToUpload():

    class MergeToUpload(object):
        print('trying to initiate')
        def __init__(self):
            self.session = orm.Session()
            self.table_types = {
                'taxa': orm.taxa_types,
                'count': orm.count_types,
                'density': orm.density_types,
                'biomass': orm.biomass_types,
                'individual': orm.individual_types,
                'percent_cover': orm.percent_cover_types
            }

        def site_in_proj_key_df(
                self, studysitetabledf, projecttabledf, lterlocation,
                observationtabledf, studysitelabel, studysitelevels):
            '''
 
            Method to format the site_in_project_table with derived
            information.

            '''
            project_metadat_key = projecttabledf[
                'proj_metadata_key']
            sitecheck = (
                self.session.query(
                    orm.study_site_table.__table__).
                order_by(
                    orm.study_site_table.__table__.c.study_site_key).
                filter(
                    orm.study_site_table.__table__.c.lter_table_fkey ==
                    lterlocation)
            )
            sitecheckdf = read_sql(
                sitecheck.statement, sitecheck.session.bind)

            qsitelist = sitecheckdf['study_site_key'].values.tolist()
            nulltest = studysitetabledf['study_site_key'].drop_duplicates().values.tolist()
            if nulltest == ['NULL']:
                print('merged NA block')
                study_sites = DataFrame(
                    sitecheckdf['study_site_key']).drop_duplicates()
                study_sites = study_sites[study_sites.study_site_key != 'NULL']
                studysitelevels = study_sites['study_site_key'].values.tolist()
                print(study_sites)
            if len(qsitelist) >= 1 and nulltest != ['NULL']:
                print('merged qsitelist >=1 block')
                study_sites_stacked = concat(
                    [studysitetabledf, sitecheckdf], axis=0)
                study_sites = DataFrame(
                    study_sites_stacked['study_site_key']).drop_duplicates()
                study_sites = study_sites[study_sites.study_site_key != 'NULL']
                studysitelevels = study_sites['study_site_key'].values.tolist()
                print(study_sites)
            if len(qsitelist) == 0:
                print('merged qusitelist = 0')
                study_sites = DataFrame(
                    studysitetabledf['study_site_key']).drop_duplicates()
                study_sites = study_sites[study_sites.study_site_key != 'NULL']
                studysitelevels = study_sites['study_site_key'].values.tolist()
                print(study_sites)

            study_sites.columns = ['study_site_table_fkey']
            print('merge class site in proj col: ', study_sites.columns)
            study_sites['sitestartyr'] = 'NA'
            study_sites['siteendyr'] = 'NA'
            study_sites['totalobs'] = 'NA'
            study_sites['uniquetaxaunits'] = -99999
            study_sites['project_table_fkey'] = int(project_metadat_key)
            sites = study_sites['study_site_table_fkey'].values.tolist()
            sites = study_sites['study_site_table_fkey'].values.tolist()
            print('merge class past study site table')
            print(studysitelevels)
            print('obsdf', observationtabledf)

            yr_all = []
            for i, item in enumerate(studysitelevels):
                yr_list = observationtabledf[
                    observationtabledf[studysitelabel] == item][
                        'year_derived'].values.tolist()
                yr_list.sort()
                [yr_all.append(x) for x in yr_list]

                study_sites.loc[
                    study_sites.study_site_table_fkey == item,
                    'sitestartyr'
                ] = yr_list[0]

                study_sites.loc[
                    study_sites.study_site_table_fkey == item,
                    'siteendyr'
                ] = yr_list[-1]

                study_sites.loc[
                    study_sites.study_site_table_fkey == item,
                    'totalobs'
                ] = len(yr_list)


            print('past year info and total obs')
            print(study_sites)
            print(studysitelabel)

            print('merge class site in proj table: ', study_sites)
            study_sites.to_sql(
                'site_in_project_table', orm.conn,
                if_exists='append', index=False)

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
            print('taxa site in proj key df: ', siteinprojkeydf)
            print('taxa site formated taxa table: ', formated_taxa_table)
            # Step 2) Merge the formatted taxa_table with the quieried
            # site_in_project_key dataframe (to add foreign keys to
            # the taxa_table)
            print('starting taxa table upload')
            orm.replace_numeric_null_with_string(formated_taxa_table)
            print('past orm replace numeric')
            tbl_taxa_with_site_in_proj_key= merge(
                formated_taxa_table, siteinprojkeydf,
                left_on=[sitelabel],
                right_on=['study_site_table_fkey'],
                how='inner')
            print('past tbl_taxa site in proj key')
            # Step 3) Making a copy of the merged table
            tbl_taxa_merged = tbl_taxa_with_site_in_proj_key.copy()

            # Step 4) Dropping the unneccessary columns from the copy
            # of the merged taxa_table (that has foreign keys now)
            tbl_taxa_merged.drop([
                'study_site_table_fkey', sitelabel,
                'project_table_fkey'], inplace=True, axis=1)
            print('past tbl_taxa drop: ', tbl_taxa_merged)
            
            # Step 5) Renaming the foreign keys to match the column
            # label in the database
            tbl_taxa_merged.rename(
                columns= {
                    'site_in_project_key': 'site_in_project_taxa_key'}, inplace=True)
            print('merge class taxa merged: ', tbl_taxa_merged)

            # Step 6) Filling Null values (blank or NaN) with 'NA' strings
            # then converting each column into it's appropriate data type
            # for the database
            tbl_taxa_merged.fillna('NA', inplace=True)
            orm.convert_types(tbl_taxa_merged, orm.taxa_types)

            # Step 7) Upload table to datbase
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

            orm.replace_numeric_null_with_string(raw_dataframe)
            orm.replace_numeric_null_with_string(formated_dataframe)

            # Step 2) Query taxa_table to get the auto generated
            # primary keys returned. Turn query data into
            # dataframe.
            session = self.session
            taxa_key_query = select([orm.taxa_table])
            taxa_key_statement = session.execute(taxa_key_query)
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

            # Step 5) Merge the original dtype data with the
            # merged taxa_table query to have all foreign keys (taxa and site_project)
            # matched up with the original observations.
            dtype_merged_with_taxa_and_siteinproj_key = merge(
                raw_dataframe, tbl_dtype_merged_taxakey_siteinprojectkey,
                left_on = list(raw_data_taxa_columns),
                right_on = list(uploaded_taxa_columns),
                how='left')

            # Step 6) Take the merged original data with all foreign keys,
            # and merged that with the formatted dtype_table based on index
            # values (order or records should not changed from the original data
            # to the formatted data)
            tbl_dtype_merged_with_all_keys = merge(
                formated_dataframe,
                dtype_merged_with_taxa_and_siteinproj_key,
                left_index=True, right_index=True, how='inner',
                suffixes=('', '_y'))


            # Step 7) List the columns that will be needed to push the
            # dtype table to the database (including foreign keys)
            tbl_dtype_columns_to_upload = [
                'taxa_table_key', 'site_in_project_taxa_key', 'year_derived',
                'month_derived', 'day_derived', 'spatial_replication_level_1',
                'spatial_replication_level_2', 'spatial_replication_level_3',
                'spatial_replication_level_4', 'structure',
                'covariates', 'trt_label'
            ]

            time_cols_rename = {
                'year_derived': 'year',
                'month_derived': 'month',
                'day_derived': 'day'
            }
            
            tbl_dtype_columns_to_upload.append(
                '{}_observation'.format(str(formated_dataframe_name)))

            tbl_dtype_merged_with_all_keys = concat(
                [tbl_dtype_merged_with_all_keys, covariate_dataframe],
                axis=1)

            # Step 8) Subsetting the fully merged dtype table data
            tbl_dtype_to_upload = tbl_dtype_merged_with_all_keys[
                tbl_dtype_columns_to_upload]

            tbl_dtype_to_upload.rename(
                columns=time_cols_rename, inplace=True
            )

            # Step 9) Renaming columns to reflect that in database table
            # And converting data types
            tbl_dtype_to_upload.rename(columns={
                'taxa_table_key': 'taxa_{}_fkey'.format(str(formated_dataframe_name))}
                , inplace=True)
            
            datatype_key = 'site_in_project_{}_fkey'.format(str(formated_dataframe_name))
            tbl_dtype_to_upload.rename(columns={
                'site_in_project_taxa_key': datatype_key}, inplace=True)
            tbl_dtype_to_upload.fillna('NA', inplace=True)
            orm.convert_types(
                tbl_dtype_to_upload, self.table_types[str(formated_dataframe_name)])

            datatype_table = '{}_table'.format(str(formated_dataframe_name))
            # Step 10) Uploading to the database

            tbl_dtype_to_upload.to_sql(
                datatype_table,
                orm.conn, if_exists='append', index=False)

    return MergeToUpload


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
    
    study_site_table.to_sql(
        'study_site_table',
        orm.conn, if_exists='append', index=False)

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

    
def test_site_in_project_key_number_two(
        MergeToUpload, site_handle, file_handle,
        meta_handle2, project_handle, taxa_handle,
        time_handle, count_handle, covar_handle):
    facade = face.Facade()

    facade.input_register(meta_handle2)
    facade.meta_verify()

    facade.input_register(file_handle)
    facade.load_data()

    facade.input_register(site_handle)
    sitedirector = facade.make_table('siteinfo')
    study_site_table = sitedirector._availdf

    siteid = site_handle.lnedentry['study_site_key']
    sitelevels = facade._data[
        siteid].drop_duplicates().values.tolist()
    facade.register_site_levels(sitelevels)
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
    print(taxa_table)
    assert 0
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

    facade._valueregister['globalid'] = meta_handle2.lnedentry['globalid']
    facade._valueregister['lter'] = meta_handle2.lnedentry['lter']
    facade._valueregister['siteid'] = siteid

    timetable_og_cols = timetable.columns.values.tolist()
    timetable.columns = [x+'_derived' for x in timetable_og_cols]
    observationdf = facade._data
    observation_time_df = concat([timetable,observationdf], axis=1 )
    
    print('merge class obs_time columns: ', observation_time_df.columns)
    print('merge class project table: ', project_table)
    

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
