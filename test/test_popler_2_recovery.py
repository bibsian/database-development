from sqlalchemy import create_engine, MetaData, Table, column
from sqlalchemy.sql import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from pandas import DataFrame, read_csv, Series
import re
import pprint as pp
import ast
import shlex
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

# -----------------------------------
# Setting up connections to databases
# ----------------------------------

# ---------------
# Popler Version 2 tables & connection

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


column_name_list = [
    'year', 'day', 'month', 'kingdom', 'phylum', 'clss', 'ordr',
    'family', 'genus', 'species', 'spt_rep1', 'spt_rep2', 'spt_rep3',
    'spt_rep4', 'structure', 'individ', 'unitobs', 'samplingunits',
    'covariates'
]
column_objs = [column(x) for x in column_name_list]


# Creating a to do all comparisions

class QualityControl(object):    
    def __init__(self, recordID):
        self.recordID = int(recordID)

    @property
    def log_path(self):
        if sys.platform == "darwin":
            filepath = (
                self.root_path + 'poplerGUI/' +
                'Logs_UI/')
        elif sys.platform == "win32":
            filepath = (
                self.root_path + 'poplerGUI\\' +
                'Logs_UI\\')
        return filepath

    @property
    def root_path(self):
        if sys.platform == "darwin":
            rootpath = (
                "/Users/bibsian/Dropbox/database-development/" +
                "popler_version2/git-repo-revert/")
        elif sys.platform == "win32":
            rootpath = (
                "C:\\Users\MillerLab\\Dropbox\\database-development\\" +
                "popler_version2\\git-repo-revert\\")
            return rootpath
        
    @property
    def file_path(self):
        if sys.platform == "darwin":
            filepath = (
                self.root_path + 'poplerGUI/' +
                'Metadata_and_og_data/')
        elif sys.platform == "win32":
            filepath = (
                self.root_path + 'poplerGUI\\' +
                'Metadata_and_og_data\\')
        return filepath

    @property
    def rgx_pattern(self):
        s_number = str(self.recordID)
        if len(s_number) == 1:
            return '(^[{}]_)'.format(int(s_number))
        elif len(s_number) == 2:
            a = s_number[0]
            b = s_number[1]
            return '(^[{}][{}]_)'.format(a, b)
        elif len(s_number) == 3:
            a = s_number[0]
            b = s_number[1]
            c = s_number[2]
            return '(^[{}][{}][{}]_)'.format(a, b, c)

    @property
    def log_df(self):
        df = DataFrame({
            'logs':
            [
                
                file for file in os.listdir(
                    self.log_path) if os.path.isfile(
                        os.path.join(
                            self.log_path, file))
            ]
        })
        df = df[df['logs'].str.contains(self.rgx_pattern)].reset_index(True)
        # Subseting and creating a new dataframe
        # with all logs for the one metadata id (key)
        df = df[
            df['logs'].str.contains(self.rgx_pattern)].reset_index(True)
        # Extracting the original file name
        df[
            'original_file'] = df[
                'logs'].apply(
                    lambda x: x[
                        re.search('table_', x).
                        end():re.search('_[0-9]{4}_', x).start()])
        # Extracting the type of log it was/what infor is in it
        df['table'] = df['logs'].apply(
            lambda x: x[
                re.search(self.rgx_pattern, x).
                end():re.search('table', x).end()])
        df['file_path'] = df['logs'].apply(
            lambda z: os.path.join(self.log_path, z))
        df['parsed_data'] = df[
            'file_path'].apply(lambda z: self.parse_log(z))
        return df

    def table_data(self, tablename):
        return self.log_df[
            self.log_df['table'] == tablename]['parsed_data'].iloc[0]

    def parse_log(self, file_name):
        log_dict = {}
        with open(file_name) as f:
            for i, ln in enumerate(f.readlines()):
                obj_list = re.search('(\[.*\])', ln)
                if obj_list is not None:
                    try:
                        col_list = [
                            ast.literal_eval(
                                x.strip()) for x in obj_list.group().strip().split('to')
                        ]
                        obj_cols = shlex.split(re.search('(\".*\")', ln).group())[0]
                        log_dict[obj_cols+'_{}'.format(i)] = col_list
                    except Exception as e:
                        print(str(e))
                else:
                    pass
            f.close()
        return log_dict

    def get_file_path(self):
        return os.path.join(
            self.file_path,
            self.log_df['original_file'].drop_duplicates()[0])

    def get_log_path(self, tablename):
        return os.path.join(
            self.log_path, self.log_df[
                self.log_df['table'] == tablename]['logs'].iloc[0])



# ------------------------------
# Getting data from postgres db
# to compare against raw data
def get_data_with_metakey(id_number):
    stmt = conn.execute(
        select(column_objs).
        select_from(
            Rawtable.__table__.
            join(Taxatable.__table__).
            join(Maintable.__table__).
            join(Sitetable)).
        where(column('metarecordid') == id_number).
        order_by(column('sampleid'))
    )
    data = DataFrame(stmt.fetchall())
    data.columns = stmt.keys()
    return data


metadata_key = 14

meta
query_data = get_data_with_metakey(metadata_key)
# query_data.to_csv(
#    os.path.join(rootpath, 'query_meta'+'_{}.csv'.format(metadata_key)))

meta = QualityControl(metadata_key)
data = read_csv(meta.get_file_path())
# data.to_csv(
#    os.path.join(rootpath, 'data_meta'+'_{}.csv'.format(metadata_key)))

site_dict = meta.table_data('sitetable')
obs_dict = meta.table_data('rawtable')
taxa_dict = meta.table_data('taxatable')

pp.pprint(site_dict)
pp.pprint(obs_dict)
pp.pprint(taxa_dict)

site_booleans = query_data['spt_rep1'] == data[site_dict['siteid_6'][1][0]]
len(query_data[site_booleans == False])

obs_booleans = query_data['unitobs'] == data[obs_dict['unitobs_6'][1][0]]
len(query_data[obs_booleans == False])

taxa_booleans = query_data['species'] == data[taxa_dict['species_6'][1][0]]
taxa_mismatch = query_data[taxa_booleans == False]
# taxa_mismatch.to_csv(
#    os.path.join(rootpath, 'taxa_mismatch_meta'+'_{}.csv'.format(metadata_key)))




