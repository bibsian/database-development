#!/usr/bin/env python
import sys, os
from pandas import read_csv, read_sql
from poplerGUI.logiclayer.datalayer import config as orm

rootpath = os.path.dirname(os.path.dirname(os.path.dirname( __file__ )))
metapath = os.path.join(rootpath, 'Cataloged_Data_Current_sorted.csv')


__all__ = ['MetaVerifier']

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
        
    _meta = read_csv(metapath, encoding='iso-8859-11')

    def __init__(self,  inputclsinstance):
        self.idnumber = int(inputclsinstance.lnedentry['globalid'])
        self.lterloc = inputclsinstance.lnedentry['lter']
        self.metaurl = inputclsinstance.lnedentry['metaurl']


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
                session = orm.Session()
                global_check_q = session.query(
                    orm.project_table.proj_metadata_key).order_by(
                        orm.project_table.proj_metadata_key)
                session.close()
                global_check_df = read_sql(
                    global_check_q.statement,
                    global_check_q.session.bind)

                uploaded_globals = global_check_df[
                    'proj_metadata_key'].values.tolist()

                assert self.idnumber not in uploaded_globals
                
                assert (self._meta.loc[
                    self._meta['global_id']== self.idnumber][
                            'global_id'] == 
                        self.idnumber).bool() is True

                assert (self._meta.loc[
                    self._meta['global_id']== self.idnumber][
                        'lter'] ==
                        self.lterloc).bool() is True

                assert (self._meta.loc[
                    self._meta['global_id']== self.idnumber][
                            'site_metadata']
                        == self.metaurl).bool() is True

                return True
            except Exception as e:
                print(str(e))
                raise LookupError(
                    "The verification attributes have not been set" +
                    " correctly. Or global_id is already present: " +
                    str(e)
                )
