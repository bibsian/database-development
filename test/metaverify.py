#!usr/bin/env python
from sys import platform as _platform
import pandas as pd

class MetaVerifier(object):
    """
    This is going to be a Singleton pattern i.e. 
    only one instance of this class will be created 
    in the whole program.

    Keyword Arguments (Derived from InputHandler class)
    -----------------
    idnumber: integer
    lterloc: string
    metaurl: string
    """

    if _platform == "darwin":
        metapath = (
        "/Users/bibsian/Dropbox/database-development/data" +
        "/meta_file_test.csv")

    elif _platform == "win32":
        metapath = (
        "C:\\Users\MillerLab\\Dropbox\\database-development" +
        "\\data\\meta_file_test.csv")

    _meta = pd.read_csv(metapath, encoding='iso-8859-11')

    def __init__(self):
        self.idnumber = None
        self.lterloc = None
        self.metaurl = None

    def verify_entries(self, inputclsinstance):
        '''
        This method is going to be used to verify
        the user input into the program. Ensuring that
        all the parameter supplied match a given record
        in the metadata dataframe.
        '''
        idnumber = inputclsinstance.lnedentry['globalid']
        lterloc = inputclsinstance.lnedentry['lter']
        metaurl = inputclsinstance.lnedentry['metaurl']


        print(type(lterloc))
        print(metaurl)
        
        if None in (idnumber, lterloc, metaurl):
            raise AttributeError(
                'Not all attributes have been set. Please enter' +
                'the globalid, lter location, and metadata url.')
        else:
            try:
                assert idnumber > 0
            except:
                raise AttributeError(
                    'Plese enter the globalid number.')

            try:
                assert (self._meta.loc[
                        self._meta['global_id']== idnumber][
                            'global_id'].values[0] == idnumber) 
                

                assert (self._meta.loc[
                    self._meta['global_id']== idnumber][
                            'lter'].values[0] == lterloc) is True


                assert (self._meta.loc[
                    self._meta['global_id']== idnumber][
                            'site_metadata'].values[0] == metaurl) is True 
            except:
                raise AttributeError(
                    'Metadata values incorrect.')

            return True
