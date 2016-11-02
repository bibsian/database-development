#!/usr/bin/env python
from pandas import DataFrame, read_csv, Series
import pprint as pp
import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/")
    filepath = (
        "/Users/bibsian/Dropbox/database-development/" +
        "popler_version2/git-repo-revert/"
    )
    end = "/"
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development\\")
    filepath = (
        "C:\\Users\MillerLab\\Dropbox\\database-development\\" +
        "popler_version2\\git-repo-revert\\"
    )
    end = "\\"
os.chdir(rootpath)
from test import class_qualitycontrol as qaqc
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI import class_inputhandler as ini

# Reading in metadata file
metadata_file = read_csv(
    filepath + 'poplerGUI' + end + 'Metadata_and_og_data' + end +
    'Cataloged_Data_Current_sorted.csv', encoding='iso-8859-11')

# Gather log data to create tables
metadata_key = 1
meta = qaqc.QualityControl(metadata_key)
site_levels = meta.get_sitelevel_changes(meta.get_log_path('sitetable'))

# Creating dictionaries for data from different tables
site_dict = meta.table_data('sitetable').iloc[0]
obs_dict = meta.table_data('rawtable').iloc[0]
taxa_dict = meta.table_data('taxatable').iloc[0]
main_dict = meta.table_data('maintable')
time_dict = meta.table_data('timetable').iloc[0]
covar_dict = meta.table_data('covartable').iloc[0]

# -------------------------------------------------------------------
# Begin concatenating data for reload to popler3
# -------------------------------------------------------------------
facade = face.Facade()

# ---------------------
# Create METADATA HANDLE
# --------------------
lentry = {
    'globalid': metadata_key,
    'metaurl': metadata_file[metadata_file['global_id'] == metadata_key]['site_metadata'].iloc[0],
    'lter': metadata_file[metadata_file['global_id'] == metadata_key]['lter'].iloc[0]}
ckentry = {}
metainput = ini.InputHandler(
    name='metacheck', tablename=None, lnedentry=lentry,
    checks=ckentry)
facade.input_register(metainput)
facade.meta_verify()

# ------------------
# Create FILE HANDLE
# -----------------
filename = meta.log_df['original_file'].drop_duplicates().iloc[0]
filelocation = os.path.join(meta.file_path, filename)
name, ext = os.path.splitext(filename)

ckentry = {}
rbtn = {'.csv': False, '.txt': False,
            '.xlsx': False}
lned = {
        'sheet': '', 'delim': '', 'tskip': '', 'bskip': '',
        'header': ''}

for key,value in rbtn.items():
    if ext == key:
        rbtn[key] = True
    else:
        pass
fileinput = ini.InputHandler(
    name='fileoptions',tablename=None, lnedentry=lned,
    rbtns=rbtn, checks=ckentry, session=True,
    filename=filelocation)
facade.input_register(fileinput)
facade.load_data()

# ------------------
# Create SITE HANDLE
# ------------------

# Create project handle

# Create taxa handle

# Create time handle

# Create covar handle

# Change sitelevels

# Push site table




facade.input_register(site_handle_1_count)
sitedirector = facade.make_table('siteinfo')
study_site_table = sitedirector._availdf

study_site_table['lter_table_fkey'] = facade._valueregister[
    'globalid'] = meta_handle_1_count.lnedentry['lter']
print(study_site_table)

facade.push_tables['study_site_table'] = study_site_table

siteid = site_handle_1_count.lnedentry['study_site_key']
sitelevels = facade._data[
    siteid].drop_duplicates().values.tolist()
facade.register_site_levels(sitelevels)

facade.input_register(project_handle_1_count)
maindirector = facade.make_table('maininfo')
project_table = maindirector._availdf.copy().reset_index(drop=True)
orm.convert_types(project_table, orm.project_types)
facade.push_tables['project_table'] = project_table
print('project table: ', project_table)

facade.input_register(taxa_handle_1_count)
taxadirector = facade.make_table('taxainfo')
facade.push_tables['taxa_table'] = taxadirector._availdf

facade.input_register(time_handle_1_count)
timetable = tparse.TimeParse(
    facade._data, time_handle_1_count.lnedentry).formater()
timetable_og_cols = timetable.columns.values.tolist()
timetable.columns = [x+'_derived' for x in timetable_og_cols]
observationdf = facade._data
observation_time_df = concat([timetable, observationdf], axis=1)

facade.push_tables['timetable'] = observation_time_df

facade.input_register(count_handle_1_count)
rawdirector = facade.make_table('rawinfo')
facade.push_tables[facade._inputs[
    'rawinfo'].tablename] = rawdirector._availdf

facade.input_register(covar_handle_1_count)
covartable = ddf.DictionaryDataframe(
    facade._data,
    covar_handle_1_count.lnedentry['columns']).convert_records()
facade.push_tables['covariates'] = covartable

facade._valueregister['globalid'] = meta_handle_1_count.lnedentry['globalid']
facade._valueregister['lter'] = meta_handle_1_count.lnedentry['lter']
facade._valueregister['siteid'] = facade._inputs[
    'siteinfo'].lnedentry['study_site_key']

facade.push_merged_data()
