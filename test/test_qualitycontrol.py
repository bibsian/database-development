from pandas import DataFrame
import pytest
import re
import difflib
import ast
import shlex
import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/")
    end = "/"
elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development\\")
    end = "\\"

@pytest.fixture 
def QualityControl():
    class QualityControl(object):
        
        root_path = rootpath
        log_path = rootpath + 'logs' + end
        file_path = rootpath + 'data'
        
        def __init__(self, recordID):
            self.recordID = int(recordID)
            self.log_dict = {}

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
            ''' Parses information regardign the log files available '''
            # Dataframe with list of log files in log directory
            df = DataFrame({
                'logs':
                [
                    file for file in os.listdir(
                        self.log_path) if os.path.isfile(
                            os.path.join(
                                self.log_path, file))
                ]
            })
            # Subset with specific metadata id
            df = df[df['logs'].str.contains(self.rgx_pattern)].reset_index(True)
            df['log_locaiton'] = df['logs'].apply(lambda x: os.path.join(self.log_path, x))
            
            # Extract file name for specific metadta id
            filename = (
                df['logs'].str.
                extract('.table_(.*)_[0-9]{4}_[0-9]{2}_[0-9]{2}.log').
                dropna().drop_duplicates().values.tolist())[0]
            print('FILENAME: ', filename)
            
            # Extract the different types of log files that exist for the metadata id
            df['log_types'] = df['logs'].str.extract('{}(?P<log_types>.*)_{}'.format(
                self.rgx_pattern ,filename))['log_types']

            # Find the location of the file in the data directory (recursive search)
            filelocation = []
            pattern   = filename
            for dirpaths, dirnames, filenames in os.walk(self.file_path):
                if pattern in filenames:        
                    filelocation.append(os.path.join(dirpaths, pattern))
            
            df['original_file'] = filelocation[0]

            return df

    return QualityControl

def test_clss(QualityControl):
    meta = QualityControl(314)
    print(meta.log_df)
    assert 0
    
#     # Creating dictionaries for data from different tables
#     site_dict = meta.table_data('sitetable').iloc[0]
#     obs_dict = meta.table_data('rawtable').iloc[0]
#     taxa_dict = meta.table_data('taxatable').iloc[0]
#     main_dict = meta.table_data('maintable').iloc[0] # Units and extent
#     main_dict_updated = meta.table_data('maintable').iloc[1] # Time & labels
#     time_dict = meta.table_data('timetable').iloc[0]
#     covar_dict = meta.table_data('covartable').iloc[0]
# 
