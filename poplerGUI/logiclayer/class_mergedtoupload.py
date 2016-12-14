#!/usr/bin/env python
from pandas import merge, concat, DataFrame, read_sql, to_numeric
from sqlalchemy import select, update, column
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


class MergeToUpload(object):
    '''
    Class that encapsulated the processes of
    merging, pushing, and updating data for the database.
    All tabels past study_site_table  and part of the project_table
    are managed through this class.
    '''
    print('trying to initiate')
    def __init__(self):
        self.session = orm.Session()
        self.table_types = {
            'taxa_table': orm.taxa_types,
            'count_table': orm.count_types,
            'density_table': orm.density_types,
            'biomass_table': orm.biomass_types,
            'individual_table': orm.individual_types,
            'percent_cover_table': orm.percent_cover_types,
            'project_table': orm.project_types
        }
        self.rawdata = None
        self.metadata_key = None
        self.sitelabel = None
        self.formateddata = None

    def site_in_proj_key_df(
            self, studysitetabledf, projecttabledf, lterlocation,
            observationtabledf, studysitelabel, studysitelevels):
        '''

        Method to take the data stored in the user facade class
        and upload to the database
        REQUIRES: study_site_table, project_table, lter,
        observation_table, study_site_label, studysitelevels...
        to make the site_in_project_table (including the merge)
        as well as merge all other tables for keys and upload.
        To merge the site_in_project_table a series of steps
        must be performed

        1) Check to see if any of the original site levels
        are present in the database

        2) test whether the dataset site levels are contained
        within the raw data or database, or both, and
        make the site_in_project_table site labels based
        off of this test. (this is necessary because if sites are
        already in the database when we pull in the study_site
        table some will be missing since present ones aren't 
        pushed).

        3) Calculate all derived values for the 
        site_in_project_table (sitestartyr, siteendyr, uniquetaxa,
        totalobs).

        4) Push all data

        5) Query the pushed data to retrieve primary keys
        then merged primary keys to sitelevel data and
        return the dataframe (to be merged in another method)
        '''
        self.rawdata = observationtabledf
        self.sitelabel = studysitelabel
        # Types of outcomes to govern push behavior
        all_site_table_data_already_uploaded = False
        site_table_data_partially_uploaded = False
        all_site_table_data_not_yet_uploaded = False

        project_metadat_key = projecttabledf[
            'proj_metadata_key']
        self.metadata_key = int(project_metadat_key)

        study_site_table_query = (
            self.session.query(
                orm.study_site_table.__table__).
            order_by(
                orm.study_site_table.__table__.c.study_site_key).
            filter(
                orm.study_site_table.__table__.c.study_site_key.in_(
                    studysitelevels
                )
            )
        )
        study_site_table_query_df = read_sql(
            study_site_table_query.statement,
            study_site_table_query.session.bind)
        study_site_table_query_list = study_site_table_query_df[
            'study_site_key'].values.tolist()
        study_site_table_list_from_user = studysitetabledf[
            'study_site_key'].drop_duplicates().values.tolist()

        # ------------------------------------ #
        # ------- study_site_table ------ #
        # ------------------------------------ #
        print('empty', study_site_table_query_df.empty)
        print('query return', study_site_table_query_df)
        print('nulltest', study_site_table_list_from_user == ['NULL'])
        print('user table', study_site_table_list_from_user)
        # ------------------------------------ #
        # ---------- site_in_project_table --- #
        # ------------------------------------ #
        if (
                study_site_table_list_from_user == ['NULL']
                and
                study_site_table_query_df.empty == False
            ):
            print('ALL Study site data is already stored')
            site_in_proj_levels_to_push = DataFrame(
                study_site_table_query_df[
                    'study_site_key']).drop_duplicates()
            site_in_proj_levels_to_push = (
                site_in_proj_levels_to_push[
                    site_in_proj_levels_to_push[
                        'study_site_key'] != 'NULL']
            )
            study_site_levels_derived = (
                site_in_proj_levels_to_push[
                    'study_site_key'].values.tolist()
            )
            all_site_table_data_already_uploaded = True
            print(site_in_proj_levels_to_push)
            print('all_site_table_data_already_uploaded = True')
        elif (
                len(
                    [
                        i for i in
                        study_site_table_query_list
                        if i not in
                        study_site_table_list_from_user
                    ]
                ) > 0
                and
                (
                    len(study_site_table_query_list) != 0
                )
        ):
            print('Study site data is partially stored already')
            site_in_proj_levels_to_push = concat(
                [
                    studysitetabledf,
                    study_site_table_query_df
                ], axis=0).drop_duplicates(subset='study_site_key')
            print('site in proj to push: ', site_in_proj_levels_to_push)
            print(site_in_proj_levels_to_push.columns)

            site_in_proj_levels_to_push = (
                site_in_proj_levels_to_push.drop_duplicates(
                    subset='study_site_key')
            )
            site_in_proj_levels_to_push = (
                site_in_proj_levels_to_push[
                    site_in_proj_levels_to_push[
                        'study_site_key'] != 'NULL']
            )
            study_site_levels_derived = (
                site_in_proj_levels_to_push[
                    'study_site_key'].values.tolist()
            )
            site_table_data_partially_uploaded = True
            print(site_in_proj_levels_to_push)
            print('site_table_data_partially_uploaded = True')

        else:
            print('Study site data is not stored')
            site_in_proj_levels_to_push = DataFrame(
                studysitetabledf['study_site_key']).drop_duplicates()
            site_in_proj_levels_to_push = (
                site_in_proj_levels_to_push[
                    site_in_proj_levels_to_push[
                        'study_site_key'] != 'NULL']
            )
            study_site_levels_derived = (
                site_in_proj_levels_to_push[
                    'study_site_key'].values.tolist()
            )
            all_site_table_data_not_yet_uploaded = True
            print(site_in_proj_levels_to_push)
            print('all_site_table_data_not_yet_uploaded = True')

        # try:
        #    print('loaded site levels: ', studysitelevels)
        #    print('derived site levels: ', study_site_levels_derived)
        #    assert (studysitelevels == study_site_levels_derived)
        #except Exception as e:
        #    print(str(e))
        #    raise AttributeError(
        #        'Study site levels derived from query and user ' +
        #        'do not match the original site levels stored ' +
        #        'in the user facade class: ' + str(e))

        site_in_proj_table_to_push = DataFrame(site_in_proj_levels_to_push['study_site_key'])
        site_in_proj_table_to_push.columns = (
            ['study_site_table_fkey']
        )
        site_in_proj_table_to_push['sitestartyr'] = 'NA'
        site_in_proj_table_to_push['siteendyr'] = 'NA'
        site_in_proj_table_to_push['totalobs'] = 'NA'
        site_in_proj_table_to_push['uniquetaxaunits'] = -99999
        site_in_proj_table_to_push['project_table_fkey'] = int(
            project_metadat_key)
        
        yr_all = []
        for i, item in enumerate(study_site_levels_derived):
            yr_list = observationtabledf[
                observationtabledf[studysitelabel] == item][
                    'year_derived'].values.tolist()
            yr_list.sort()
            [yr_all.append(x) for x in yr_list]

            try:
                if len(yr_list) >= 2:
                    site_in_proj_table_to_push.loc[
                        site_in_proj_table_to_push.
                        study_site_table_fkey == item, 'sitestartyr'
                    ] = yr_list[0]
                    site_in_proj_table_to_push.loc[
                        site_in_proj_table_to_push.
                        study_site_table_fkey == item, 'siteendyr'
                    ] = yr_list[-1]
                    site_in_proj_table_to_push.loc[
                        site_in_proj_table_to_push.
                        study_site_table_fkey == item, 'totalobs'
                    ] = len(yr_list)
                else:
                    site_in_proj_table_to_push.loc[
                        site_in_proj_table_to_push.
                        study_site_table_fkey == item, 'sitestartyr'
                    ] = None
                    site_in_proj_table_to_push.loc[
                        site_in_proj_table_to_push.
                        study_site_table_fkey == item, 'siteendyr'
                    ] = None
                    site_in_proj_table_to_push.loc[
                        site_in_proj_table_to_push.
                        study_site_table_fkey == item, 'totalobs'
                    ] = None
            except Exception as e:
                print("couldn't update year records")

        session = self.session
        global_id_site_in_project_query = (
            select(
                [orm.site_in_project_table.__table__.c.project_table_fkey]
            ).distinct()
        )
        session.close()
        global_id_statement = session.execute(
            global_id_site_in_project_query)
        global_id_uploaded_list = [
            x[0] for x in global_id_statement.fetchall()]


        if self.metadata_key in global_id_uploaded_list:
            print('passing site in project table to upload')
            pass
        
        else:
            site_in_proj_table_to_push.to_sql(
                'site_in_project_table', orm.conn,
                if_exists='append', index=False)
            print('site_in_project_table table UPLOADED')

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
        '''
        Method to take the data stored in the user facade class
        and upload the database
        REQUIRES: formated taxa table (with database names),
        dataframe with site levels merged to site_in_project
        (formated_taxa_table)
        primary keys (created in method above...siteinprojkeydf)
        , and the name of the column with the site (sitelabel)
        to make the site_in_project_table (including the merge)
        as well as merge all other tables for keys and upload.
        To merge the site_in_project_table a series of steps
        must be performed

        1) Merged the formated taxa table with the site_in_project
        data that contains primary keys for site_in_project table
        and site levels (merge on site levels)

        2) Dropping columns not neccessary for the taxa_table
        push (metadata key: project_table_fkey,
        site label:study_site_table_fkey)

        3) Rename merged site_in_project_table primary key
        to match taxa table name

        4) Push taxa_table to database

        '''

        print('starting taxa table upload')
        orm.replace_numeric_null_with_string(formated_taxa_table)
        print('past orm replace numeric')
        print('siteingproj key df: ', siteinprojkeydf)
        print('siteingproj key df: ', siteinprojkeydf.columns)
        print('formatted taxa df: ', formated_taxa_table)
        print('formatted taxa df: ', formated_taxa_table.columns)

        tbl_taxa_with_site_in_proj_key = merge(
            formated_taxa_table, siteinprojkeydf,
            left_on=sitelabel,
            right_on='study_site_table_fkey',
            how='inner')
        print('past tbl_taxa site in proj key')
        tbl_taxa_merged = tbl_taxa_with_site_in_proj_key.copy()

        tbl_taxa_merged.drop([
            'study_site_table_fkey', sitelabel,
            'project_table_fkey'], inplace=True, axis=1)
        print('past tbl_taxa drop: ', tbl_taxa_merged)
        tbl_taxa_merged.rename(
            columns={
                'site_in_project_key': 'site_in_project_taxa_key'}, inplace=True)
        print('merge class taxa merged: ', tbl_taxa_merged)

        tbl_taxa_merged.fillna('NA', inplace=True)
        try:
            orm.convert_types(tbl_taxa_merged, orm.taxa_types)
        except Exception as e:
            print('converting issues: ', str(e))

        session = self.session
        site_in_proj_key_query = session.execute(
            select(
                [orm.taxa_table.__table__.c.site_in_project_taxa_key]
            ).
            distinct()
        )
        session.close()
        
        check_site_in_proj_keys = DataFrame(site_in_proj_key_query.fetchall())
        if check_site_in_proj_keys.empty:
            check_site_in_proj_keys = []
        else:
            check_site_in_proj_keys = check_site_in_proj_keys[0].values.tolist()
            
    
        if all(
                x in check_site_in_proj_keys
                for x in
                siteinprojkeydf['site_in_project_key'].values.tolist()):
            pass
        else:
            taxacolumns = [
                'site_in_project_taxa_key', 'sppcode', 'kingdom',
                'subkingdom', 'infrakingdom', 'superdivision', 'division',
                'subdivision', 'superphylum', 'phylum', 'subphylum',
                'clss', 'subclass', 'ordr', 'family', 'genus', 'species',
                'common_name', 'authority', 'metadata_taxa_key'
            ]
            tbl_taxa_merged['metadata_taxa_key'] = int(self.metadata_key)
            tbl_taxa_merged[taxacolumns].to_sql(
                'taxa_table', orm.conn, if_exists='append', index=False)

    def merge_for_datatype_table_upload(
            self, raw_dataframe,
            formated_dataframe,
            formated_dataframe_name,
            covariate_dataframe,
            siteinprojkeydf,
            raw_data_taxa_columns,
            uploaded_taxa_columns):

        print('start dtype upload')
        orm.replace_numeric_null_with_string(raw_dataframe)
        orm.replace_numeric_null_with_string(formated_dataframe)
        print('replacing nulls is a pain')

        # Step 2) Query taxa_table to get the auto generated
        # primary keys returned. Turn query data into
        # dataframe.
        session = self.session
        taxa_key_statement = session.execute(
            select([orm.taxa_table]).
            where(
                orm.taxa_table.__table__.c.site_in_project_taxa_key.in_
                (siteinprojkeydf['site_in_project_key'].values.tolist())
            )
        )
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

        raw_dataframe_siteinproj = merge(
            raw_dataframe, siteinprojkeydf,
            left_on=self.sitelabel, right_on='study_site_table_fkey',
            sort=False, how='left')

        raw_data_taxa_columns.append('site_in_project_key')
        uploaded_taxa_columns.append('site_in_project_taxa_key')

        raw_data_taxa_columns.append('site_in_project_key')
        uploaded_taxa_columns.append('site_in_project_taxa_key')

        print('updated raw data col list: ', raw_dataframe_siteinproj)
        print('update taxa data col list: ', uploaded_taxa_columns)
        # Step 5) Merge the original dtype data with the
        # merged taxa_table query to have all foreign keys...
        # taxa and site_project
        # matched up with the original observations.
        dtype_merged_with_taxa_and_siteinproj_key = merge(
            raw_dataframe_siteinproj,
            tbl_dtype_merged_taxakey_siteinprojectkey,
            left_on=list(raw_data_taxa_columns),
            right_on=list(uploaded_taxa_columns),
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
            'spatial_replication_level_4', 'spatial_replication_level_5',
            'structure_type_1', 'structure_type_2',
            'structure_type_3',
            'treatment_type_1', 'treatment_type_2',
            'treatment_type_3',
            'covariates'
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
        self.formateddata = tbl_dtype_to_upload
        # Step 10) Uploading to the database
        datatype_table = '{}_table'.format(str(formated_dataframe_name))
        datatype_obs = '{}_observation'.format(str(formated_dataframe_name))
        print('push raw_before', tbl_dtype_to_upload.columns)

        tbl_dtype_to_upload[datatype_obs] = to_numeric(
            tbl_dtype_to_upload[datatype_obs], errors='coerce'
        )
        
        text_cols = [
            'spatial_replication_level_1', 'spatial_replication_level_2',
            'spatial_replication_level_3', 'spatial_replication_level_4',
            'spatial_replication_level_5', 'treatment_type_1',
            'treatment_type_2', 'treatment_type_3',
            'structure_type_1', 'structure_type_2', 'structure_type_3'
        ]
        tbl_dtype_to_upload[text_cols] = tbl_dtype_to_upload[
            text_cols].applymap(str)
        tbl_dtype_to_upload[text_cols] = tbl_dtype_to_upload[
            text_cols].applymap(lambda x: x.strip())

        print(tbl_dtype_to_upload.dtypes)
        print(self.table_types[datatype_table])
        try:
            orm.convert_types(tbl_dtype_to_upload, self.table_types[datatype_table])
        except Exception as e:
            print('converting issues: ', str(e))


        print('push raw_after', tbl_dtype_to_upload.columns)
        print(tbl_dtype_to_upload.dtypes)
        print('this should have worked')


        other_numerics = [
            'year', 'month', 'day', datatype_key,
            'taxa_{}_fkey'.format(str(formated_dataframe_name))
        ]

        tbl_dtype_to_upload[datatype_obs] = to_numeric(
            tbl_dtype_to_upload[datatype_obs], errors='coerce'
        )

        try:
            tbl_dtype_to_upload[other_numerics].replace({'NA', -99999}, inplace=True)
        except Exception as e:
            print('No NAs to replace:', str(e))
        try:
            tbl_dtype_to_upload[other_numerics].replace({'NaN' -99999}, inplace=True)
        except Exception as e:
            print('No NaN to replace:', str(e))
        try:
            tbl_dtype_to_upload[other_numerics].replace({None, -99999}, inplace=True)
        except Exception as e:
            print('No None to replace:', str(e))
        tbl_dtype_to_upload[other_numerics].fillna(-99999, inplace=True)


        tbl_dtype_to_upload.loc[:, other_numerics] = tbl_dtype_to_upload.loc[
            :, other_numerics].apply(to_numeric, errors='coerce')

        metadata_key_column_name = 'metadata_{}_key'.format(
            formated_dataframe_name)
        tbl_dtype_to_upload[metadata_key_column_name] = int(self.metadata_key)
        tbl_dtype_to_upload.to_sql(
            datatype_table,
            orm.conn, if_exists='append', index=False)
        print('past datatype upload')

    def update_project_table(
            self,
            spatial_rep_columns_from_og_df,
            spatial_rep_columns_from_formated_df):
        '''
        Methods to update the projcet table with information
        that was gathered toward the end of a user session
        Arguments are the column names for 
        the different levels of spatial replication that
        are present (key/value pairs)
        '''
        ##
        # ADD STUDYSTARTYR, STUDYENDYR, SPAT_LEV_UNQ_REPS(1-5),
        # SPAT_LEV_LABELS(1-5)
        ##
        spatial_index = [
            i for i, item in enumerate(
                spatial_rep_columns_from_formated_df)
            if 'spatial' in item
        ]
        spatial_label_col = ['spatial_replication_level_1_label']
        spatial_label_val = [self.sitelabel]
        spatial_uq_num_of_rep_col = [
            'spatial_replication_level_1_number_of_unique_reps']
        spatial_uq_num_of_rep_val = [
            len(self.rawdata[self.sitelabel].unique())
            ]
        for i in range(len(spatial_index)):
            spatial_label_col.append(
                spatial_rep_columns_from_formated_df[i] + '_label')
            spatial_label_val.append(
                spatial_rep_columns_from_og_df[i])
            spatial_uq_num_of_rep_col.append(
                spatial_rep_columns_from_formated_df[i] +
                '_number_of_unique_reps')
            spatial_uq_num_of_rep_val.append(
                len(
                    self.rawdata[
                        spatial_rep_columns_from_og_df[i]].unique()
                )
            )
        print(self.formateddata.columns)
        print(self.formateddata)
        print('Populating update_dict')
        update_dict = {
            'studystartyr': self.formateddata.loc[:, 'year'].min(),
            'studyendyr': self.formateddata.loc[:, 'year'].max()
        }
        for i, item in enumerate(spatial_label_col):
            update_dict[item] = spatial_label_val[i]
            update_dict[spatial_uq_num_of_rep_col[i]] = spatial_uq_num_of_rep_val[i]
        print(self.metadata_key)
        print('startyear: ',update_dict['studystartyr'])
        print('endyear: ', update_dict['studyendyr'])
        orm.conn.execute(
            update(orm.project_table).
            where(
                column('proj_metadata_key') == self.metadata_key).
            values(update_dict)
        )
