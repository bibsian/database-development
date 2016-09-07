#! /usr/bin/env python
from pandas import merge, concat, DataFrame, read_sql
from sqlalchemy import select
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
        # Step 1)
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


        # Step 2) Merge the formatted taxa_table with the quieried
        # site_in_project_key dataframe (to add foreign keys to
        # the taxa_table)
        orm.replace_numeric_null_with_string(formated_taxa_table)
        tbl_taxa_with_site_in_proj_key= merge(
            formated_taxa_table, siteinprojkeydf,
            left_on=[sitelabel],
            right_on=['study_site_table_fkey'],
            how='inner')

        # Step 3) Making a copy of the merged table
        tbl_taxa_merged = tbl_taxa_with_site_in_proj_key.copy()

        # Step 4) Dropping the unneccessary columns from the copy
        # of the merged taxa_table (that has foreign keys now)
        tbl_taxa_merged.drop([
            'study_site_table_fkey', sitelabel,
            'project_table_fkey'], inplace=True, axis=1)

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
