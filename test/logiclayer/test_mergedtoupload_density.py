#! /usr/bin/env python
from pandas import concat, DataFrame
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
from poplerGUI.logiclayer.datalayer import config as orm
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI.logiclayer import class_timeparse as tparse
from poplerGUI.logiclayer.class_helpers import produce_null_df
from poplerGUI.logiclayer import class_dictionarydataframe as ddf

def test_site_in_project_key_number_two(
        MergeToUpload, site_handle_2_density, file_handle_2_density,
        meta_handle_2_density, project_handle_2_density, taxa_handle_2_density,
        time_handle_2_density, count_handle_2_density, covar_handle_2_density):
    facade = face.Facade()
    
    facade.input_register(meta_handle_2_density)
    facade.meta_verify()

    facade.input_register(file_handle_2_density)
    facade.load_data()

    facade.input_register(site_handle_2_density)
    sitedirector = facade.make_table('siteinfo')
    study_site_table = sitedirector._availdf

    siteid = site_handle_2_density.lnedentry['study_site_key']
    sitelevels = facade._data[
        siteid].drop_duplicates().values.tolist()
    facade.register_site_levels(sitelevels)
    print('test2 sitelevels: ', sitelevels)
    facade._valueregister['siteid'] = siteid

    print('study_site_table (test): ', study_site_table)

    facade.create_log_record('study_site_table')
    lter = meta_handle_2_density.lnedentry['lter']
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


    facade.input_register(project_handle_2_density)
    maindirector = facade.make_table('maininfo')
    project_table = maindirector._availdf.copy().reset_index(drop=True)
    orm.convert_types(project_table, orm.project_types)
    
    facade.push_tables['project_table'] = project_table
    facade.create_log_record('project_table')


    facade.input_register(taxa_handle_2_density)
    taxadirector = facade.make_table('taxainfo')
    
    taxa_table = taxadirector._availdf
    facade.push_tables['taxa_table'] = taxa_table
    print('taxa columns after make taxa table: ', taxa_table.columns)

    facade.create_log_record('taxa_table')
    
    print('taxa columns before time_table: ', taxa_table.columns)
    
    facade.input_register(time_handle_2_density)
    timetable = tparse.TimeParse(
        facade._data, time_handle_2_density.lnedentry).formater()
    facade.push_tables['timetable'] = timetable
    facade.create_log_record('timetable')

    print('taxa columns before count_table: ', taxa_table.columns)
    facade.input_register(count_handle_2_density)
    rawdirector = facade.make_table('rawinfo')
    rawtable = rawdirector._availdf
    print(rawtable)
    facade.push_tables[count_handle_2_density.tablename] = rawtable
    facade.create_log_record(count_handle_2_density.tablename)

    print('taxa columns before covar_table: ', taxa_table.columns)
    facade.input_register(covar_handle_2_density)
    covartable = ddf.DictionaryDataframe(
        facade._data,
        covar_handle_2_density.lnedentry['columns']).convert_records()
    facade.push_tables['covariates'] = covartable
    facade.create_log_record('covartable')

    facade._valueregister['globalid'] = meta_handle_2_density.lnedentry['globalid']
    facade._valueregister['lter'] = meta_handle_2_density.lnedentry['lter']
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
        print('Sites in db: ', str(e))
    project_table['lter_project_fkey'] = facade._valueregister['lter']        
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
    
    taxa_column_in_push_table = [
        x[0] for x in 
        list(facade._inputs['taxainfo'].lnedentry.items())
    ]
    taxa_column_in_data = [
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
        spatial_rep_columns_from_formated_df=obs_columns_in_push_table)

