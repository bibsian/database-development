#!/usr/bin/env python
from pandas import DataFrame
import re
import difflib
import ast
import shlex
import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/")
    gitrepo = (
        "/Users/bibsian/Dropbox/database-development/" +
        "popler_version2/git-repo-revert/")
    end = "/"
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development\\")
    end = "\\"
    gitrepo = (
        "C:\\Users\MillerLab\\Dropbox\\database-development\\" +
        "popler_version2\\git-repo-revert\\")

class QualityControl(object):    

    root_path = gitrepo
    
    def __init__(self, recordID):
        self.recordID = int(recordID)
        self.log_dict = {}

#     @property
#     def root_path(self):
#         if sys.platform == "darwin":
#             rootpath = (
#                 "/Users/bibsian/Dropbox/database-development/" +
#                 "popler_version2/git-repo-revert/")
#         elif sys.platform == "win32":
#             rootpath = (
#                 "C:\\Users\MillerLab\\Dropbox\\database-development\\" +
#                 "popler_version2\\git-repo-revert\\")
#             return rootpath
 
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
                        end():re.search('_[0-9]{4}_[0-9]{2}_[0-9]{2}.log', x).start()])
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
            self.log_df['table'] == tablename]['parsed_data']

    def parse_log(self, file_name):
        local_log_dict = {}
        with open(file_name) as f:
            for i, ln in enumerate(f.readlines()):
                # INFO log data
                # (Contains data for making the sitetable to push,
                # and columns to make all other tables)
                obj_list = re.search('(\[.*\])', ln)
                if obj_list is not None:
                    try:
                        col_list = [
                            ast.literal_eval(
                                x.strip()) for x in obj_list.group().strip().split('to')
                        ]
                        obj_cols = shlex.split(re.search('(\".*\")', ln).group())[0]
                        if len(col_list) == 2:
                            self.log_dict[obj_cols] = col_list
                            local_log_dict[obj_cols] = col_list
                        else:
                            pass
                    except Exception as e:
                        print(str(e))
                        pass
                else:
                    pass
            f.close()
        return local_log_dict

    def get_sitelevel_changes(self, file_name):
        with open(file_name) as f:
            for i, ln in enumerate(f.readlines()):
                # DEBUG log data
                # (Contain data for site level names and/or data)
                site_level_obj = re.search('\s(\w*)list:\s(.*[^\s+])', ln)
                if site_level_obj is not None:
                    sitelevels = site_level_obj.group().strip().split(':')
                    if sitelevels[1].strip()[0:6] == 'siteid':
                        pass
                    else:
                        self.log_dict[
                            'sitelevels_{}'.format(sitelevels[0])] = sitelevels[1].strip()
                else:
                    pass
            f.close()

        site_to = self.log_dict['sitelevels_changed_site_list']
        site_to_list = site_to.split()
        site_from = self.log_dict['sitelevels_list']
        if ' or ' in site_from:
            site_from = site_from.replace(' or ', '_or_')
            site_from_list = site_from.split()
            site_from_list = [re.sub('_', ' ', x) for x in site_from_list]
        else:
            site_from_list = site_from.split()
        original_site_list = [None]*len(site_to_list)
        indexer = 0
        changed = list(difflib.restore(difflib.ndiff(site_to, site_from), 1))
        revert = list(difflib.restore(difflib.ndiff(site_to, site_from), 2))
        if len(changed) == len(revert) :
            for i, s in enumerate(changed):
                if i == 0 or s == ' ':
                    word = revert[i]
                    if i == 0:
                        original_site_list[indexer] = word
                if s == ' ':
                    indexer += 1
                elif i > 0:
                    word = word + revert[i]
                    original_site_list[indexer] = word
            original_site_list = [x.strip() for x in original_site_list]
            site_from_list = original_site_list
        elif len(site_to_list) == len(site_from_list):
            pass
        change_dict = {}
        for i, value in enumerate(site_from_list):
            change_dict[value] = site_to_list[i]
        return change_dict
        
    def get_file_path(self):
        return os.path.join(
            self.file_path,
            self.log_df['original_file'].drop_duplicates()[0])

    def get_log_path(self, tablename):
        try:
            return os.path.join(
                self.log_path, self.log_df[
                    self.log_df['table'] == tablename]['logs'].iloc[0])
        except Exception as e:
            print(str(e))
            raise IOError('Log file not present for ID: ' + self.recordID)

