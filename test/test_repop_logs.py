#!/usr/bin/env python
from collections import OrderedDict
from pandas import DataFrame, read_csv, Series, read_sql, concat, to_numeric
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
from poplerGUI import class_inputhandler as ini
from poplerGUI.logiclayer import class_helpers as hlp
from poplerGUI.logiclayer import class_timeparse as tparse
from poplerGUI.logiclayer import class_dictionarydataframe as ddf
from poplerGUI.logiclayer.datalayer import config as orm
from poplerGUI.logiclayer.datalayer import class_filehandles as fhdl



# ------------------------------------------
# Enging to connect to popler and get 'main_table' data
# which will become th 'project_table' data
# -----------------------------------------
from sqlalchemy import create_engine, MetaData, Table, column
from sqlalchemy.sql import select, and_, join, cast
from sqlalchemy.dialects.postgresql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = create_engine(
    'postgresql+psycopg2:///',
    echo=False)
conn = engine.connect()
# Mapping metadata
metadata = MetaData(bind=engine)
# Creating base
Base = declarative_base()

class Ltertable(Base):
    __table__ = Table('lter_table', metadata, autoload=True)


class Sitetable(Base):
    __table__ = Table('site_table', metadata, autoload=True)


class Maintable(Base):
    __table__ = Table('main_table', metadata, autoload=True)
    taxa = relationship(
        'Taxatable', cascade="delete, delete-orphan")
    raw = relationship('Rawtable', cascade="delete, delete-orphan")


class Taxatable(Base):
    __table__ = Table('taxa_table', metadata, autoload=True)


class Rawtable(Base):
    __table__ = Table('raw_table', metadata, autoload=True)



# --------------------------------
# Files neccessary to do a repopulation of popler_3
# metadata file & name changing file
# ----------------------------------
# Reading in metadata file
metadata_file = read_csv(
    filepath + 'poplerGUI' + end + 'Metadata_and_og_data' + end +
    'Cataloged_Data_Current_sorted.csv', encoding='iso-8859-11')

namechange_file = read_csv(
    rootpath + 'db' + end + 'popler2-migrate-to-popler3' +
    end + 'migration_changes.csv'
)

# -------------------------------
# Beinging to extract log data/query old popler
# to get information that will be used to repopulate popler3
# -------------------------------

# Gather log data to create tables
metadata_key = 3
meta = qaqc.QualityControl(metadata_key)
site_levels = meta.get_sitelevel_changes(meta.get_log_path('sitetable'))

# Creating dictionaries for data from different tables
site_dict = meta.table_data('sitetable').iloc[0]
obs_dict = meta.table_data('rawtable').iloc[0]
taxa_dict = meta.table_data('taxatable').iloc[0]
main_dict = meta.table_data('maintable').iloc[0] # Units and extent
main_dict_updated = meta.table_data('maintable').iloc[1] # Time & labels
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
facade.input_register(metainput)  # register metadata input
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

data_caretaker = fhdl.Caretaker()
data_originator = fhdl.DataOriginator(None, 'Initializing')

data_file_originator = fhdl.DataFileOriginator(fileinput)
caretaker = data_caretaker.save(
    data_file_originator.save_to_memento())

data_originator.restore_from_memento(
    data_caretaker.restore())

original_data = data_originator._data.copy()


# ------------------
# Create SITE HANDLE
# ------------------
sitecolumn = list(set(main_dict_updated['sp_rep1_label'][1]))[0]
facade._valueregister['study_site_key'] = sitecolumn  # register site column

lned = {'study_site_key': sitecolumn}
siteinput = ini.InputHandler(
    name='siteinfo', lnedentry=lned, tablename='study_site_table')
facade.input_register(siteinput)  # register site input


# Modify and store sitelevels
try:
    facade._data = facade._data.replace(to_replace={sitecolumn: site_levels})
except:
    print('No replacement needed')

facade.register_site_levels(
    facade._data[
        sitecolumn].drop_duplicates().values.tolist())  # register site levels


if 'siteid_levels' in site_dict.keys():
    study_site_key = site_dict['siteid_levels'][1]
else:
    study_site_key = site_dict['siteid'][1]

if 'lat' not in site_dict.keys() and 'lng' not in site_dict.keys():
    site_lat = ['NaN']
    site_lng = ['NaN']
else:
    site_lat = site_dict['lat'][1]
    site_lng = site_dict['lng'][1]
    
sitetable = DataFrame(
    {
        'study_site_key': study_site_key,
        'lter_table_fkey': site_dict['lterid'][1],
        'lat_study_site': site_lat,
        'lng_study_site': site_lng
    })
if 'descript' not in site_dict.keys():
    sitetable['descript'] = ['NA']*len(sitetable)
else:
    sitetable['descript'] = site_dict['descript'][1]

facade.push_tables['study_site_table'] = sitetable  # register study site table



# ---------------------
# Create PROJECT TABLE (no need for handle just query original popler)
# --------------------
proj_stmt = conn.execute(
    select([Maintable]).where(column('metarecordid') == metadata_key)
)
proj_df = DataFrame(list(proj_stmt.fetchone())).transpose()
proj_df.columns = proj_stmt.keys()
changes = dict(
    zip(
        namechange_file[namechange_file[
            'table_to'] == 'project_table']['column_from'].values.tolist(),
        namechange_file[namechange_file[
            'table_to'] == 'project_table']['column_to'].values.tolist()
        )
    )
proj_df = proj_df.rename(columns=changes)
proj_df.drop(
    [
        'lter_proj_site', 'siteid', 'sitestartyr', 'siteendyr',
        'totalobs', 'uniquetaxaunits', 'num_treatments',
        'exp_maintainence', 'trt_label'
    ], axis=1, inplace=True)

cols_to_add = [
    'structured_type_2', 'structured_type_2_units',
    'structured_type_3', 'structured_type_3_units',
    'spatial_replication_level_5_extent',
    'spatial_replication_level_5_extent_units',
    'spatial_replication_level_5_number_of_unique_reps',
    'spatial_replication_level_5_label'
]
all_col = proj_df.columns.values.tolist()
[all_col.append(x) for x in cols_to_add]

proj_df = proj_df.reindex(columns=list(all_col), fill_value='NA')

orm.convert_types(proj_df, orm.project_types)
facade.push_tables['project_table'] = proj_df

# ------------------
# Create TAXA HANDLE
# -------------------
taxalned = OrderedDict((
    ('sppcode', taxa_dict['sppcode'][1][0]),
    ('kingdom', taxa_dict['kingdom'][1][0]),
    ('subkingdom', ''),
    ('infrakingdom', ''),
    ('superdivision', ''),
    ('divsion', ''),
    ('subdivision', ''),
    ('superphylum', ''),
    ('phylum', taxa_dict['phylum'][1][0]),
    ('subphylum', ''),
    ('clss', taxa_dict['clss'][1][0]),
    ('subclass', ''),
    ('ordr', taxa_dict['ordr'][1][0]),
    ('family', taxa_dict['family'][1][0]),
    ('genus', taxa_dict['genus'][1][0]),
    ('species', taxa_dict['species'][1][0]),
    ('common_name', '')
))
taxackbox = OrderedDict((
    ('sppcode', False if taxa_dict['sppcode'][1][0] == '' else True),
    ('kingdom', False if taxa_dict['kingdom'][1][0] == '' else True),
    ('subkingdom', False),
    ('infrakingdom', False),
    ('superdivision', False),
    ('divsion', False),
    ('subdivision', False),
    ('superphylum', False),
    ('phylum', False if taxa_dict['phylum'][1][0] == '' else True),
    ('subphylum', False),
    ('clss', False if taxa_dict['clss'][1][0] == '' else True),
    ('subclass', False),
    ('ordr', False if taxa_dict['ordr'][1][0] == '' else True),
    ('family', False if taxa_dict['family'][1][0] == '' else True),
    ('genus', False if taxa_dict['genus'][1][0] == '' else True),
    ('species', False if taxa_dict['species'][1][0] == '' else True),
    ('common_name', False)
))

entered_taxacolumns = [x for x in taxalned.values() if x != '']
data_columns = facade._data.columns.values.tolist()

taxacreate = {
    'taxacreate': True if all(x in data_columns for x in entered_taxacolumns) == False else True
}    
available = [
    x for x,y in zip(
        list(taxalned.keys()), list(
            taxackbox.values()))
    if y is True
]
taxainput = ini.InputHandler(
    name='taxainfo',
    tablename='taxa_table',
    lnedentry= hlp.extract(taxalned, available),
    checks=taxacreate)
facade.input_register(taxainput)
taxa_director = facade.make_table('taxainfo')
facade.push_tables['taxa_table'] = taxa_director._availdf

# -------------------
# Create TIME HANDLE
# ------------------
user_timeinputs = dict(
    zip(
        list(time_dict.keys()), [x[1][0] for x in time_dict.values()]
    )
)
user_timeinputs['hms'] = user_timeinputs.pop('mspell')


timeinput = ini.InputHandler(
    name='timeinfo', tablename='timetable',
    lnedentry=user_timeinputs)
facade.input_register(timeinput)
timetable = tparse.TimeParse(
    facade._data, timeinput.lnedentry).formater()
timetable_og_cols = timetable.columns.values.tolist()
timetable.columns = [x+'_derived' for x in timetable_og_cols]
observation_df = facade._data.copy()
observation_time_df = concat([timetable, observation_df], axis=1)
facade.push_tables['timetable'] = observation_time_df

# -------------------
# Create COVAR HANDLE
# ------------------
covarlned = {'columns': covar_dict['columns'][1][0]}
covarinput = ini.InputHandler(
    name='covarinfo', tablename='covartable',
    lnedentry=covarlned
)
facade.input_register(covarinput)
covartable = ddf.DictionaryDataframe(
    facade._data,
    covarinput.lnedentry['columns']).convert_records()
facade.push_tables['covariates'] = covartable

# ------------------
# Create RAW DATA HANLDE
# ------------------
obslned = OrderedDict((
    ('spatial_replication_level_2', obs_dict['spt_rep2'][1][0]),
    ('spatial_replication_level_3', obs_dict['spt_rep3'][1][0]),
    ('spatial_replication_level_4', obs_dict['spt_rep4'][1][0]),
    ('spatial_replication_level_5', ''),
    ('structure_type_1', obs_dict['structure'][1][0]),
    ('structure_type_2', ''),
    ('structure_type_3', ''),
    ('treatment_type_1', obs_dict['trt_label'][1][0]),
    ('treatment_type_2', ''),
    ('treatment_type_3', ''),
    ('unitobs', obs_dict['unitobs'][1][0])
))
obsckbox = OrderedDict((
    ('spatial_replication_level_2', False if obs_dict['spt_rep2'][1][0] == '' else True),
    ('spatial_replication_level_3', False if obs_dict['spt_rep3'][1][0] == '' else True),
    ('spatial_replication_level_4', False if obs_dict['spt_rep4'][1][0] == '' else True),
    ('spatial_replication_level_5', False),
    ('structure_type_1', False if obs_dict['structure'][1][0] == '' else True),
    ('structure_type_2', False),
    ('structure_type_3', False),
    ('treatment_type_1', False if obs_dict['trt_label'][1][0] == '' else True),
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

# Get Table name
recorded_dtype = facade.push_tables['project_table']['datatype'].iloc[0]
if 'mark' in recorded_dtype:
    data_type = 'individual_table'
elif 'cou' in recorded_dtype :
    data_type = 'count_table'
elif 'dens' in recorded_dtype:
    data_type = 'density_table'
elif 'cover' in recorded_dtype:
    data_type = 'percent_cover_table'
elif 'bio' in recorded_dtype:
    data_type = 'biomass_table'

countinput = ini.InputHandler(
    name='rawinfo',
    tablename=data_type,
    lnedentry=hlp.extract(obslned, available),
    checks=obsckbox)

facade.input_register(countinput)
rawdirector = facade.make_table('rawinfo')

orm_dict = {
    'count_table': orm.count_types,
    'bimoass_table': orm.biomass_types,
    'density_table': orm.density_types,
    'percent_cover_table': orm.percent_cover_types,
    'individual_table': orm.individual_types
}

rawtable = rawdirector._availdf.copy()

changes = dict(
    zip(
        namechange_file[namechange_file[
            'table_to'] == data_type]['column_from'].values.tolist(),
        namechange_file[namechange_file[
            'table_to'] == data_type]['column_to'].values.tolist()
        )
    )

rawtable.rename(columns=changes, inplace=True)

facade.push_tables[facade._inputs[
    'rawinfo'].tablename] = rawtable


# ------------------------
# Making sure data values are set thata are needed
# ------------------------
facade._valueregister['globalid'] = metainput.lnedentry['globalid']
facade._valueregister['lter'] = metainput.lnedentry['lter']
facade._valueregister['siteid'] = facade._inputs['siteinfo'].lnedentry['study_site_key']

# ----------------------
# GO
# ----------------------

def test_push():
    facade.push_merged_data()

