#!usr/bin/env python
import pandas as pd
from sys import platform as _platform


class MetaVerifier(object):
    """
    This is going to be a Singleton pattern i.e. 
    only one instance of this class will be created 
    in the whole program.

    Keyword Arguments
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

    def __init__(self, *args, **kwargs):
        self.idnumber = kwargs.setdefault('idnumber', 0)
        self.lterloc = kwargs.setdefault('lterloc', None)
        self.metaurl = kwargs.setdefault('metaurl', None)


    def verify_entries(self):
        '''
        This method is going to be used to verify
        the user input into the program. Ensuring that
        all the parameter supplied match a given record
        in the metadata dataframe.
        '''
        if None in (self.idnumber, self.lterloc, self.metaurl):
            raise AttributeError(
                'Not all attributes have been set. Please enter' +
                'the globalid, lter location, and metadata url.')
        else:
            try:
                assert self.idnumber > 0
            except:
                raise AttributeError(
                    'Plese enter the globalid number.')

            try:

                assert self._meta.loc[
                    self._meta['global_id']== self.idnumber][
                            'global_id'] == self.idnumber

                assert self._meta.loc[
                    self._meta['lter']== self.lterloc][
                            'lter'] == self.lterloc

                assert self._meta.loc[
                    self._meta['site_metadata']== self.metaurl][
                            'site_metadata'] == self.metaurl

                return True

            except:
                raise LookupError(
                    "The verification attributes have not been set" +
                    " correctly. Please check values for the " +
                    "global_id, LTER location, and metadata url.")
