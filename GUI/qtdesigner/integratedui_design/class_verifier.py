#!/usr/bin/env python

# This class will be created to store the information unique
# to a dataset that is being cleaned/uploaded to the database.
import pandas as pd


class GlobalId(pd.DataFrame):
    """
    Gloabal Id is a pandas dataframe that
    contains all the metadata along with user
    supplied key word arguments.

    Keyword Arguments
    -----------------
    idnumber: integer
    lterloc: string
    metaurl: string
    """
    def __init__(self, *args, **kwargs):
        idnumber = kwargs.pop('idnumber', None)
        lterloc = kwargs.pop('lterloc', None)
        metaurl = kwargs.pop('metaurl', None)

        super(GlobalId, self).__init__(*args, **kwargs)
        # Giving our added attributes None type or assigning
        # them based on user input
        if idnumber is not None:
            self.idnumber = int(idnumber)
        else:
            self.idnumber = None

        if lterloc is not None:
            self.lterloc = str(lterloc)
        else:
            self.lterloc = None

        if metaurl is not None:
            self.metaurl = str(metaurl)
        else:
            self.metaurl = None
        self.records = None

    @property
    def _constructor(self):
        '''
        Defining the constructor to subclass a pandas
        dataframe.
        '''
        return GlobalId

    def get_records(self):
        '''
        This method is going to be used to verify
        the user input into the program. Ensuring that
        all the parameter supplied match a given record
        in the metadata dataframe.
        '''
        if None in (self.idnumber, self.lterloc, self.metaurl):
            return self.records
        else:
            try:
                self.records = self[self['global_id'] == self.idnumber]

                assert self.lterloc == list(self[
                    self['global_id'] == self.idnumber]['lter'])[0]

                assert self.metaurl == list(self[
                    self['global_id'] ==
                    self.idnumber]['site_metadata'])[0]

                return self.records

            except:
                raise LookupError(
                    "The global id attributes have not been set" +
                    " correctly. Please check the dataframe, " +
                    "global_id, LTER location, and metadata url.")
