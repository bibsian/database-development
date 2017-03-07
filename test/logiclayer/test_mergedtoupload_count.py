#! /usr/bin/env python
from pandas import concat
import re
import sys, os
from poplerGUI.logiclayer.datalayer import config as orm
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI.logiclayer import class_timeparse as tparse
from poplerGUI.logiclayer.class_helpers import produce_null_df
from poplerGUI.logiclayer import class_dictionarydataframe as ddf

def test_site_in_project_key(
        MergeToUpload, site_handle_corner_case, file_handle_corner_case,
        meta_handle_corner_case, project_handle_corner_case, taxa_handle_corner_case,
        time_handle_corner_case, count_handle_corner_case, covar_handle_corner_case):
    facade = face.Facade()

    facade.input_register(meta_handle_corner_case)
    facade.meta_verify()

    facade.input_register(file_handle_corner_case)
    facade.load_data()
    facade._data.replace({'-888': 'NA'}, inplace=True)

    
    facade.input_register(site_handle_corner_case)
    sitedirector = facade.make_table('siteinfo')
    study_site_table = sitedirector._availdf

    print('study_site_table (test): ', study_site_table)
    facade.create_log_record('study_site_table')
    lter = meta_handle_corner_case.lnedentry['lter']
    ltercol = produce_null_df(1, [
        'lter_table_fkey'], len(study_site_table), lter)
    study_site_table = concat([study_site_table, ltercol], axis=1)
    print('study_site_table: ', study_site_table)
    facade.push_tables['study_site_table'] = study_site_table
    
    siteid = site_handle_corner_case.lnedentry['study_site_key']
    sitelevels = facade._data[
        siteid].drop_duplicates().values.tolist()
    facade.register_site_levels(sitelevels)
    facade._valueregister['siteid'] = siteid

    facade.input_register(project_handle_corner_case)
    maindirector = facade.make_table('maininfo')
    project_table = maindirector._availdf.copy().reset_index(drop=True)
    orm.convert_types(project_table, orm.project_types)
    
    facade.push_tables['project_table'] = project_table
    facade.create_log_record('project_table')
    
    facade.input_register(taxa_handle_corner_case)
    taxadirector = facade.make_table('taxainfo')
    taxa_table = taxadirector._availdf
    facade.push_tables['taxa_table'] = taxa_table
    facade.create_log_record('taxa_table')
    
    facade.input_register(time_handle_corner_case)
    timetable = tparse.TimeParse(
        facade._data, time_handle_corner_case.lnedentry).formater()
    facade.push_tables['timetable'] = timetable
    facade.create_log_record('timetable')

    facade.input_register(count_handle_corner_case)
    rawdirector = facade.make_table('rawinfo')
    rawtable = rawdirector._availdf
    print(rawtable)
    facade.push_tables[count_handle_corner_case.tablename] = rawtable
    facade.create_log_record(count_handle_corner_case.tablename)

    facade.input_register(covar_handle_corner_case)
    covartable = ddf.DictionaryDataframe(
        facade._data,
        covar_handle_corner_case.lnedentry['columns']).convert_records()
    facade.push_tables['covariates'] = covartable
    facade.create_log_record('covartable')

    facade._valueregister['globalid'] = meta_handle_corner_case.lnedentry['globalid']
    facade._valueregister['lter'] = meta_handle_corner_case.lnedentry['lter']
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

    project_table['lter_project_fkey'] = facade._valueregister['lter']
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
    obs_columns_in_data = [
        x[1] for x in 
        list(facade._inputs['rawinfo'].lnedentry.items())
    ]
    obs_columns_in_push_table = [
        x[0] for x in 
        list(facade._inputs['rawinfo'].lnedentry.items())
    ]
    merge_object.update_project_table(
        spatial_rep_columns_from_og_df=obs_columns_in_data,
        spatial_rep_columns_from_formated_df=obs_columns_in_push_table
    )

