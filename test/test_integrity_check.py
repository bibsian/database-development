#!/usr/bin/env python
from collections import OrderedDict
from pandas import (
    DataFrame, read_csv, Series, read_sql, concat, to_numeric,
    to_datetime)
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
from poplerGUI.logiclayer import class_userfacade as face
from poplerGUI.logiclayer import class_helpers as hlp
from poplerGUI.logiclayer import class_timeparse as tparse
from poplerGUI.logiclayer import class_dictionarydataframe as ddf
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

###### @@@@@@@@@@@@@ KEY @@@@@@@@@@@@@@@ ##########
# Gather log data to create tables
metadata_key = 8
###### @@@@@@@@@@@@@ KEY @@@@@@@@@@@@@@@ ##########


engine = create_engine(
    'postgresql+psycopg2:///',
    echo=False)
#engine = create_engine(
#    'postgresql+psycopg2:///',
#    echo=False)

conn = engine.connect()
# Mapping metadata
metadata = MetaData(bind=engine)
# Creating base
Base = declarative_base()

class lter_table(Base):
    __table__ = Table('lter_table', metadata, autoload=True)
class study_site_table(Base):
    __table__ = Table('study_site_table', metadata, autoload=True)
class project_table(Base):
    __table__ = Table('project_table', metadata, autoload=True)
    taxa = relationship(
        'taxa_table', cascade="delete, delete-orphan")
    count = relationship(
        'count_table', cascade="delete, delete-orphan")
    density = relationship(
        'density_table', cascade="delete, delete-orphan")
    biomass = relationship(
        'biomass_table', cascade="delete, delete-orphan")
    percent_cover = relationship(
        'percent_cover_table', cascade="delete, delete-orphan")
    individual = relationship(
        'individual_table', cascade="delete, delete-orphan")
class site_in_project_table(Base):
    __table__ = Table('site_in_project_table', metadata, autoload=True)
class taxa_table(Base):
    __table__ = Table('taxa_table', metadata, autoload=True)
class taxa_accepted_table(Base):
    __table__ = Table('taxa_accepted_table', metadata, autoload=True)
class count_table(Base):
    __table__ = Table('count_table', metadata, autoload=True)
class biomass_table(Base):
    __table__ = Table('biomass_table', metadata, autoload=True)
class density_table(Base):
    __table__ = Table('density_table', metadata, autoload=True)
class percent_cover_table(Base):
    __table__ = Table('percent_cover_table', metadata, autoload=True)
class individual_table(Base):
    __table__ = Table('individual_table', metadata, autoload=True)


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


meta = qaqc.QualityControl(metadata_key)
site_levels = meta.get_sitelevel_changes(meta.get_log_path('sitetable'))


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
original_data.replace({'NaN':'NA'}, inplace=True)
original_data.replace({'-99999':'NA'}, inplace=True)
original_data.replace({'-9999':'NA'}, inplace=True)
original_data.replace({-99999:'NA'}, inplace=True)
original_data.replace({-9999:'NA'}, inplace=True)
original_data.fillna('NA', inplace=True)

# Creating dictionaries for data from different tables
site_dict = meta.table_data('sitetable').iloc[0]
obs_dict = meta.table_data('rawtable').iloc[0]
taxa_dict = meta.table_data('taxatable').iloc[0]
main_dict = meta.table_data('maintable').iloc[0] # Units and extent
main_dict_updated = meta.table_data('maintable').iloc[1] # Time & labels
time_dict = meta.table_data('timetable').iloc[0]
covar_dict = meta.table_data('covartable').iloc[0]

original_data = read_csv(filelocation, low_memory=False)
sitecolumn = list(set(main_dict_updated['sp_rep1_label'][1]))[0]

data_type = conn.execute(
    select([project_table.datatype]).
    where(project_table.proj_metadata_key == metadata_key)
).fetchone()[0]+'_table'

# Gathering date information
day_col = time_dict['dayname'][1][0]
month_col = time_dict['monthname'][1][0]
year_col = time_dict['yearname'][1][0]
date_col_list = [day_col, month_col, year_col]
date_index = ['day', 'month', 'year']
date_dict = dict(zip(date_index, date_col_list))
updated_date_dict = {}

og_day = None
og_month = None
og_year = None
if len(set(date_col_list)) == 1:
    original_data[day_col] = to_datetime(original_data[day_col])
    og_day = original_data[day_col].map(lambda x: x.day)
    og_month = original_data[day_col].map(lambda x: x.month)
    og_year = original_data[day_col].map(lambda x: x.year)
if len(set(date_col_list)) > 1:
    for i, val in date_dict.items():
        if val != '':
            updated_date_dict[i] = val
            original_data[val] = to_datetime(original_data[val])
            try:
                og_day = original_data[day_col].dt.day
            except:
                print('no day')
            try:
                og_month = original_data[day_col].dt.month
            except:
                print('no day')
            try:
                og_year = original_data[day_col].dt.day
            except:
                print('no day')
                
        else:
            pass
        


# --------------------
# Query to pull the pushed data
# from popler3
# -------------------
site_in_proj_keys_df = DataFrame(conn.execute(
    select([site_in_project_table.site_in_project_key]).
    where(site_in_project_table.project_table_fkey == metadata_key)
).fetchall())
site_in_proj_keys = site_in_proj_keys_df.loc[:, 0].values.tolist()


site_in_proj_subq_stmt = (
    select(
        [
            site_in_project_table,
            study_site_table,
            lter_table.lat_lter,
            lter_table.lng_lter,
            lter_table.lterid,
            project_table
        ]).
    where(site_in_project_table.project_table_fkey == metadata_key).
    select_from(
        site_in_project_table.__table__.
        join(study_site_table.__table__).
        join(lter_table.__table__).
        join(project_table)
    ).alias('site_in_proj_subq_stmt')
)


taxa_tbl_subq_stmt = (
    select([site_in_proj_subq_stmt, taxa_table]).
    select_from(
        site_in_proj_subq_stmt.join(
            taxa_table,
            onclause=(
                site_in_proj_subq_stmt.c.site_in_project_key ==
                taxa_table.site_in_project_taxa_key)
            )
        ).alias('taxa_tbl_subq_stmt')
)


if data_type == 'count_table':
    count_tbl_subq_stmt = (
        select([
            taxa_tbl_subq_stmt,
            count_table,
            cast(column('count_observation'), INTEGER).label('count_observation')]).
        select_from(
            taxa_tbl_subq_stmt.
            join(
                count_table,
                onclause=and_(
                    taxa_tbl_subq_stmt.c.taxa_table_key ==
                    count_table.taxa_count_fkey)
                )
            )
    )
if data_type == 'biomass_table':
    count_tbl_subq_stmt = (
        select([
            taxa_tbl_subq_stmt,
            biomass_table]).
        select_from(
            taxa_tbl_subq_stmt.
            join(
                biomass_table,
                onclause=and_(
                    taxa_tbl_subq_stmt.c.taxa_table_key ==
                    biomass_table.taxa_biomass_fkey)
                )
            )
    )
    
if data_type == 'density_table':
    count_tbl_subq_stmt = (
        select([
            taxa_tbl_subq_stmt,
            density_table]).
        select_from(
            taxa_tbl_subq_stmt.
            join(
                density_table,
                onclause=and_(
                    taxa_tbl_subq_stmt.c.taxa_table_key ==
                    density_table.taxa_density_fkey)
                )
            )
    )
if data_type == 'percent_cover_table' or data_type == 'per_cover_table':
    if 'per_cover' in data_type:
        data_type = 'percent_cover_table'
    count_tbl_subq_stmt = (
        select([
            taxa_tbl_subq_stmt,
            percent_cover_table]).
        select_from(
            taxa_tbl_subq_stmt.
            join(
                percent_cover_table,
                onclause=and_(
                    taxa_tbl_subq_stmt.c.taxa_table_key ==
                    percent_cover_table.taxa_percent_cover_fkey)
                )
            )
    )
if data_type == 'individual_table':
    count_tbl_subq_stmt = (
        select([
            taxa_tbl_subq_stmt,
            individual_table]).
        select_from(
            taxa_tbl_subq_stmt.
            join(
                individual_table,
                onclause=and_(
                    taxa_tbl_subq_stmt.c.taxa_table_key ==
                    count_table.taxa_individual_fkey)
                )
            )
    )


tbl_subq_result = conn.execute(count_tbl_subq_stmt)
tbl_subq_df = DataFrame(tbl_subq_result.fetchall())
tbl_subq_df.columns = tbl_subq_result.keys()
tbl_subq_df.sort_values(data_type + '_key', inplace=True)
print('done')

tbl_subq_df.replace({'NaN':'NA'}, inplace=True)
tbl_subq_df.replace({'-99999':'NA'}, inplace=True)
tbl_subq_df.replace({'-9999':'NA'}, inplace=True)
tbl_subq_df.replace({-99999:'NA'}, inplace=True)
tbl_subq_df.replace({-9999:'NA'}, inplace=True)
tbl_subq_df.fillna('NA', inplace=True)


# def test_repop():
assert (len(tbl_subq_df)==len(original_data)) is True

assert all(
    original_data[sitecolumn] == tbl_subq_df['spatial_replication_level_1']) is True


og_obs_data = Series(original_data[obs_dict['unitobs'][1][0]].copy())
if data_type == 'count_table':
    qu_obs_data = tbl_subq_df[data_type.replace('table', 'observation')].iloc[:,1].copy()
else:
    qu_obs_data = tbl_subq_df[data_type.replace('table', 'observation')].copy()

assert (og_obs_data.fillna('NaN', inplace=True) == qu_obs_data.fillna('NaN', inplace=True)) is True

taxa_info = dict(
    zip(list(taxa_dict.keys()),[x[1][0] for x in list(taxa_dict.values())]))

# One last go for replacing values that could be mismatches
original_data.replace({'NaN': 'NA'}, inplace=True)
original_data.replace({'-99999': 'NA'}, inplace=True)
original_data.replace({'-9999': 'NA'}, inplace=True)
original_data.replace({-99999: 'NA'}, inplace=True)
original_data.replace({-9999: 'NA'}, inplace=True)
original_data.fillna('NA', inplace=True)

tbl_subq_df.replace({'NaN': 'NA'}, inplace=True)
tbl_subq_df.replace({'-99999': 'NA'}, inplace=True)
tbl_subq_df.replace({'-9999': 'NA'}, inplace=True)
tbl_subq_df.replace({-99999: 'NA'}, inplace=True)
tbl_subq_df.replace({-9999: 'NA'}, inplace=True)
tbl_subq_df.fillna('NA', inplace=True)

taxa_check = {}
for dbcol, ogcol in taxa_info.items():
    test = all(original_data[ogcol] == tbl_subq_df[dbcol])
    if test is False:
        taxa_check[dbcol] = concat(
            [
                original_data[(original_data[ogcol] == tbl_subq_df[dbcol]) == False][ogcol],
                tbl_subq_df[(tbl_subq_df[dbcol] == original_data[ogcol]) == False][dbcol]],
            axis=1)

if taxa_check:
    print('mismataches')
else:
    print('Verified')

date_check = {}
# Check time
if og_day is not None:
    try:
        assert all(tbl_subq_df['day'] == og_day) is True
    except:
        date_check['day'] = tbl_subq_df[(tbl_subq_df['day'] == og_day) == False]
        print('day mismatch')
if og_month is not None:
    try:
        assert all(tbl_subq_df['month'] == og_month) is True
    except:
        date_check['month'] = tbl_subq_df[(tbl_subq_df['month'] == og_month) == False]
        print('month mismatch')
if og_year is not None:
    try:
        assert all(tbl_subq_df['year'] == og_year) is True
    except:
        date_check['year'] = tbl_subq_df[(tbl_subq_df['year'] == og_year) == False]
        print('year mismatch')

if date_check:
    print('date mismatches')
else:
    print('date data verified')

tbl_subq_df.covariates.map(lambda x: x[)
