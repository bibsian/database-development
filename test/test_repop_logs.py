#!/usr/bin/env python
from collections import OrderedDict
from pandas import DataFrame, read_csv, Series, read_sql, concat, to_numeric, set_option
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

set_option('display.max_columns', None)

# Pop v2
engine = create_engine(
    'postgresql+psycopg2://--/popler_migrate_to_cloud',
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


metarecords_stmt = conn.execute(
    select([Maintable.lter_proj_site, Maintable.metarecordid]).
    order_by(Maintable.lter_proj_site)
)
metarecords_df = DataFrame(metarecords_stmt.fetchall())
metarecords_df.columns = metarecords_stmt.keys()
metarecords_list = metarecords_df['metarecordid'].drop_duplicates().values.tolist()

metadata_dict = {}
z=93

for z in metarecords_list:
    try:

        meta = qaqc.QualityControl(z)
        site_levels = meta.get_sitelevel_changes(meta.get_log_path('sitetable'))

        # Creating dictionaries for data from different tables
        site_dict = meta.table_data('sitetable').iloc[0]
        obs_dict = meta.table_data('rawtable').iloc[0]
        taxa_dict = meta.table_data('taxatable').iloc[0]
        main_dict = meta.table_data('maintable').iloc[0] # Units and extent
        main_dict_updated = meta.table_data('maintable').iloc[1] # Time & labels
        time_dict = meta.table_data('timetable').iloc[0]
        covar_dict = meta.table_data('covartable').iloc[0]

        sitecolumn = list(set(main_dict_updated['sp_rep1_label'][1]))[0]

        
        # -------------------------------------------------------------------
        # Begin concatenating data for reload to popler3
        # -------------------------------------------------------------------
        facade = face.Facade()

        # ---------------------
        # Create METADATA HANDLE
        # --------------------
        lentry = {
            'globalid': z,
            'metaurl': metadata_file[metadata_file['global_id'] == z]['site_metadata'].iloc[0],
            'lter': metadata_file[metadata_file['global_id'] == z]['lter'].iloc[0]}
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
        if ext == '.txt':
            possible_delims = ['\t','\s', ',']
            for i in possible_delims:
                print('trying delims: ', i)
                try:
                    lned = {
                        'sheet': '', 'delim': i, 'tskip': '', 'bskip': '',
                        'header': ''}
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
                    original_data[sitecolumn]
                    try:
                        original_data.replace(site_levels, inplace=True)
                        facade.input_register(fileinput)
                        facade.load_data()
                        print('loaded')
                        break
                    except Exception as e:
                        print(str(e))
                    
                except:
                    print('delim: ', i, 'not it')
        else:
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
            try:
                original_data.replace(site_levels, inplace=True)
                facade.input_register(fileinput)
                facade.load_data()

            except Exception as e:
                print(str(e))


        # ------------------
        # Create SITE HANDLE
        # ------------------
        sitecolumn = list(set(main_dict_updated['sp_rep1_label'][1]))[0]
        facade._valueregister['study_site_key'] = sitecolumn  # register site column

        lned = {'study_site_key': sitecolumn}
        siteinput = ini.InputHandler(
            name='siteinfo', lnedentry=lned, tablename='study_site_table')
        facade.input_register(siteinput)  # register site input


        sitecolumn_checklist = facade._data[sitecolumn].values.tolist()
        # Modify and store sitelevels
        try:
            facade._data[sitecolumn] = facade._data[sitecolumn].apply(str)
            for item, value in site_levels.items():
                if value not in sitecolumn_checklist:
                    facade._data[sitecolumn] = facade._data[
                        sitecolumn].replace(to_replace={item:value})
                else:
                    pass
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
            site_lat = [float(x) for x in site_dict['lat'][1]]
            site_lng = [float(x) for x in site_dict['lng'][1]]

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
            try:
                sitetable['descript'] = site_dict['descript'][1]
            except Exception as e:
                sitetable['descript'] = ['NA']*len(sitetable)
                print('descript not recorded')

        try:
            orm.convert_types(sitetable, orm.study_site_types)
        except Exception as e:
            print('converting issues: ', str(e))


        study_site_table_numeric_columns = [
            'lat_study_site', 'lng_study_site'
        ]
        # convert datatype to string/object
        sitetable[
            sitetable.columns.difference(study_site_table_numeric_columns)] = sitetable[
                sitetable.columns.difference(study_site_table_numeric_columns)].applymap(str)
        # Strip strings of leading and trailing whitespace
        sitetable[
            sitetable.columns.difference(study_site_table_numeric_columns)] = sitetable[
                sitetable.columns.difference(study_site_table_numeric_columns)].applymap(
                    lambda x: x.strip())

        sitetable[study_site_table_numeric_columns] = to_numeric(
            sitetable[study_site_table_numeric_columns], errors='coerce')

        
        facade.push_tables['study_site_table'] = sitetable  # register study site table

        #sess = orm.Session()
        #delstmt = sess.query(
        #    orm.study_site_table.__table__).filter(
        #        orm.study_site_table.__table__.c.study_site_key.in_(
        #            sitetable.study_site_key.values.tolist()
        #        )
        #    ).delete(synchronize_session=False)
        #sess.commit()
        #sess.close()

        # ---------------------
        # Create PROJECT TABLE (no need for handle just query original popler)
        # --------------------
        proj_stmt = conn.execute(
            select([Maintable]).where(column('metarecordid') == z)
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
                'lter_proj_site', 'lter_proj_fkey', 'sitestartyr', 'siteendyr',
                'totalobs', 'uniquetaxaunits', 'num_treatments',
                'exp_maintainence', 'trt_label'
            ], axis=1, inplace=True)


        try:
            proj_df.drop(
                ['samplingmethod'], axis=1, inplace=True)
        except Exception as e:
            print('no samplingmethod')

        try:
            proj_df[['treatment_type_1', 'treatment_type_2']] = proj_df[
                'treatment_type_1'].str.split(';', expand=True).fillna('NA')
        except Exception as e:
            print('Single treatment: ', str(e))
            
        
        try:
            proj_df[['structured_type_1', 'structured_type_2']] = proj_df[
                'structured_type_1'].str.split(';', expand=True).fillna('NA')
        except Exception as e:
            print('not multiple structured types: ', str(e))


        try:
            proj_df['structured_type_1_units'] = proj_df[
                'structured_type_1'].str.extract('\((.*)\)').fillna('NA')
        except Exception as e:
            print("can't format main table columns based on regex: ", str(e))

        try:
            proj_df['structured_type_1'] = proj_df[
                'structured_type_1'].str.replace('\s\(.*\)', '')
        except Exception as e:
            print("can't format main table columns based on regex: ", str(e))

        if 'structured_type_2' in proj_df.columns:
            char_cols_to_add = [
                'structured_type_2_units',
                'structured_type_3', 'structured_type_3_units',
                'spatial_replication_level_5_extent_units',
                'spatial_replication_level_5_label'
            ]
        else:
            char_cols_to_add = [
                'structured_type_2', 'structured_type_2_units',
                'structured_type_3', 'structured_type_3_units',
                'spatial_replication_level_5_extent_units',
                'spatial_replication_level_5_label'
            ]

        all_col = proj_df.columns.values.tolist()
        [all_col.append(x) for x in char_cols_to_add]
        proj_df = proj_df.reindex(columns=list(all_col), fill_value='NA')

        numeric_cols_to_add = [
            'spatial_replication_level_5_extent',
            'spatial_replication_level_5_number_of_unique_reps'
        ]
        all_col = proj_df.columns.values.tolist()
        [all_col.append(x) for x in numeric_cols_to_add]
        proj_df = proj_df.reindex(columns=list(all_col), fill_value=None)


        proj_df['datatype'] = proj_df[
            'datatype'].map(lambda x: 'individual' if 'mark' in x else x)
        proj_df['datatype'] = proj_df[
            'datatype'].map(lambda x: 'count' if 'dist' in x else x)
        proj_df['datatype'] = proj_df[
            'datatype'].map(lambda x: 'percent_cover' if 'per_cover' in x else x)
        proj_df['datatype'] = proj_df[
            'datatype'].map(lambda x: 'biomass' if 'biomass' in x else x)
        proj_df['datatype'] = proj_df[
            'datatype'].map(lambda x: 'density' if 'density' in x else x)


        project_table_numeric_columns = [
            'studystartyr', 'studyendyr',
            'spatial_replication_level_1_extent',
            'spatial_replication_level_1_number_of_unique_reps',
            'spatial_replication_level_2_extent',
            'spatial_replication_level_2_number_of_unique_reps',
            'spatial_replication_level_3_extent',
            'spatial_replication_level_3_number_of_unique_reps',
            'spatial_replication_level_4_extent',
            'spatial_replication_level_4_number_of_unique_reps',
            'spatial_replication_level_5_extent',
            'spatial_replication_level_5_number_of_unique_reps',
        ]
        # Converting data types

        proj_df.loc[
            :, proj_df.columns.difference(project_table_numeric_columns)] = proj_df.loc[
                :, proj_df.columns.difference(project_table_numeric_columns)].applymap(str).values
                # Striping strings
        proj_df.loc[
            :, proj_df.columns.difference(project_table_numeric_columns)] = proj_df.loc[
                :, proj_df.columns.difference(project_table_numeric_columns)].applymap(
                    lambda x: x.strip()).values
        proj_df.loc[:, project_table_numeric_columns] = proj_df.loc[:, project_table_numeric_columns].apply(
            to_numeric, errors='ignore'
        )

        facade.push_tables['project_table'] = proj_df

        # ------------------
        # Create TAXA HANDLE
        # -------------------
        taxalned = OrderedDict((
            ('sppcode', taxa_dict['sppcode'][1][0].strip()),
            ('kingdom', taxa_dict['kingdom'][1][0].strip()),
            ('subkingdom', ''),
            ('infrakingdom', ''),
            ('superdivision', ''),
            ('divsion', ''),
            ('subdivision', ''),
            ('superphylum', ''),
            ('phylum', taxa_dict['phylum'][1][0].strip()),
            ('subphylum', ''),
            ('clss', taxa_dict['clss'][1][0].strip()),
            ('subclass', ''),
            ('ordr', taxa_dict['ordr'][1][0].strip()),
            ('family', taxa_dict['family'][1][0].strip()),
            ('genus', taxa_dict['genus'][1][0].strip()),
            ('species', taxa_dict['species'][1][0].strip()),
            ('common_name', '')
        ))
        taxackbox = OrderedDict((
            ('sppcode', False if taxa_dict['sppcode'][1][0].strip() == '' else True),
            ('kingdom', False if taxa_dict['kingdom'][1][0].strip() == '' else True),
            ('subkingdom', False),
            ('infrakingdom', False),
            ('superdivision', False),
            ('divsion', False),
            ('subdivision', False),
            ('superphylum', False),
            ('phylum', False if taxa_dict['phylum'][1][0].strip() == '' else True),
            ('subphylum', False),
            ('clss', False if taxa_dict['clss'][1][0].strip() == '' else True),
            ('subclass', False),
            ('ordr', False if taxa_dict['ordr'][1][0].strip() == '' else True),
            ('family', False if taxa_dict['family'][1][0].strip() == '' else True),
            ('genus', False if taxa_dict['genus'][1][0].strip() == '' else True),
            ('species', False if taxa_dict['species'][1][0].strip() == '' else True),
            ('common_name', False)
        ))

        entered_taxacolumns = [x for x in taxalned.values() if x != '']
        data_columns = facade._data.columns.values.tolist()

        taxacreate = {
            'taxacreate': True if any(x in data_columns for x in entered_taxacolumns) == False else True
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

        taxatable = taxa_director._availdf
        taxatable.fillna('NA', inplace=True)
        taxatable = taxatable.applymap(str)
        taxatable = taxatable.applymap(lambda x: x.strip())
        facade.push_tables['taxa_table'] = taxatable

        # -------------------
        # Create TIME HANDLE
        # ------------------
        
        user_timeinputs = dict(
            zip(
                list(time_dict.keys()), [x[1][0] for x in time_dict.values()]
            )
        )

        if 'mspell' not in user_timeinputs.keys():
            user_timeinputs['hms'] = user_timeinputs.pop('mspell')
        else:
            pass

        if 'dayform' not in user_timeinputs.keys():
            user_timeinputs['dayform'] = 'NULL'
        if 'monthform' not in user_timeinputs.keys():
            user_timeinputs['monthform'] = 'NULL'
        if 'yearform' not in user_timeinputs.keys():
            user_timeinputs['yearform'] = 'NULL'

        
        for key, value in user_timeinputs.items():
            if 'name' in key and value == '':
                user_timeinputs[key.replace('name', 'form')] = 'NULL'

        missing_date_info = list(
            set(['hms', 'jd', 'dayname', 'monthname', 'yearname', 'dayform', 'monthform', 'yearform']) -
            set(user_timeinputs.keys())
        )
        for i in missing_date_info:
            if i in ['dayname', 'monthname', 'yearname']:
                user_timeinputs[i] = ''
            elif i in ['dayform', 'monthform', 'yearform']:
                user_timeinputs[i] = 'NULL'
            elif i in ['hms', 'jd']:
                user_timeinputs[i] = False


        timeinput = ini.InputHandler(
            name='timeinfo', tablename='timetable',
            lnedentry=user_timeinputs)
        facade.input_register(timeinput)

        timetable = tparse.TimeParse(
            facade._data, timeinput.lnedentry).formater()

        timetable = timetable.apply(to_numeric, errors='coerce')
        timetable_og_cols = timetable.columns.values.tolist()
        timetable.columns = [x+'_derived' for x in timetable_og_cols]
        observation_df = facade._data.copy()
        observation_time_df = concat([timetable, observation_df], axis=1)

        date_cols = ['year_derived', 'day_derived', 'month_derived']
        observation_time_df[date_cols] = to_numeric(
            observation_time_df[date_cols], errors='coerce')
        facade.push_tables['timetable'] = observation_time_df

        
        # -------------------
        # Create COVAR HANDLE
        # ------------------
        try:
            covarlned = {'columns': covar_dict['columns'][1][0]}
        except Exception as e:
            covarlned = {'columns': ['']}

        if covarlned['columns']:
            pass
        else:
            covarlned['columns'] = ['']

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
            ('spatial_replication_level_2', obs_dict['spt_rep2'][1][0].strip().strip()),
            ('spatial_replication_level_3', obs_dict['spt_rep3'][1][0].strip().strip()),
            ('spatial_replication_level_4', obs_dict['spt_rep4'][1][0].strip().strip()),
            ('spatial_replication_level_5', ''),
            ('structure_type_1', obs_dict['structure'][1][0].strip()),
            ('structure_type_2', ''),
            ('structure_type_3', ''),
            ('treatment_type_1', obs_dict['trt_label'][1][0].strip()),
            ('treatment_type_2', ''),
            ('treatment_type_3', ''),
            ('unitobs', obs_dict['unitobs'][1][0].strip())
        ))
        obsckbox = OrderedDict((
            ('spatial_replication_level_2', False if obs_dict['spt_rep2'][1][0].strip() == '' else True),
            ('spatial_replication_level_3', False if obs_dict['spt_rep3'][1][0].strip() == '' else True),
            ('spatial_replication_level_4', False if obs_dict['spt_rep4'][1][0].strip() == '' else True),
            ('spatial_replication_level_5', False),
            ('structure_type_1', False if obs_dict['structure'][1][0].strip() == '' else True),
            ('structure_type_2', False),
            ('structure_type_3', False),
            ('treatment_type_1', False if obs_dict['trt_label'][1][0].strip() == '' else True),
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
        elif 'indiv' in recorded_dtype:
            data_type = 'individual_table'


        countinput = ini.InputHandler(
            name='rawinfo',
            tablename=data_type,
            lnedentry=hlp.extract(obslned, available),
            checks=obsckbox)
        facade.input_register(countinput)
    
        rawdirector = facade.make_table('rawinfo')
        rawtable = rawdirector._availdf.copy()
        observation_type = data_type.replace('table', 'observation')

        changes = dict(
            zip(
                namechange_file[namechange_file[
                    'table_to'] == data_type]['column_from'].values.tolist(),
                namechange_file[namechange_file[
                    'table_to'] == data_type]['column_to'].values.tolist()
                )
            )
        rawtable.rename(columns=changes, inplace=True)
        rawtable.loc[:, rawtable.columns.difference(['level_0', 'index', observation_type])] = rawtable[rawtable.columns.difference(
            ['level_0', 'index', observation_type])].applymap(str)

        
        try:
            rawtable[observation_type].replace({'NA', -99999}, inplace=True)
        except Exception as e:
            print('No NAs to replace:', str(e))
        try:
            rawtable[observation_type].replace({'NaN' -99999}, inplace=True)
        except Exception as e:
            print('No NaN to replace:', str(e))
        try:
            rawtable[observation_type].replace({None, -99999}, inplace=True)
        except Exception as e:
            print('No None to replace:', str(e))
        rawtable[observation_type].fillna(-99999, inplace=True)
        rawtable.loc[:, observation_type] = rawtable.loc[:, observation_type].apply(
            to_numeric, errors='coerce')

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
        facade.push_merged_data()
        metadata_dict[z] = 'pass'
    except Exception as e:
        print(str(e))
        metadata_dict[z] = 'fail'
    try:
        del facade
    except Exception as e:
        print('facade not initiated: ', str(e))


with open((rootpath + 'repopulate_from_logs.txt'), "w") as text_file:
    for i, item in metadata_dict.items():
        if item == 'fail':
            print("repopulate fail: metarecord_id {}".format(i), file=text_file)
        else:
            print("repopulate pass: metarecord_id {}".format(i), file=text_file)
