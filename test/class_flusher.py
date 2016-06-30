import pandas as pd
import config as orm

class Flusher(object):
    '''
    Class to flush database records
    '''
    def __init__(
            self, dataframe, tablename, tablekey, lterid):
        self.df = dataframe
        self.tablename = tablename
        self.pk = tablekey
        self.lterid = lterid
        self.ormreg = {}
        self.ormtable = {
            'sitetable': site_add,
            'maintable': main_add,
            'taxatable': taxa_add,
            'rawtable': raw_add
        }
        self.table_check = {
            'sitetable': orm.session.query(
                orm.Sitetable.siteid).order_by(
                    orm.Sitetable.siteid).filter(
                        orm.Sitetable.lterid == self.lterid),
            'maintable': orm.session.query(
                orm.Maintable.metarecordid).order_by(
                    orm.Maintable.metarecordid)
        }

    def database_check(self, comparelist):
        '''
        Comparing values from database table to those
        about to be flushed (avoiding redundant uploads)
        '''
        comparelist = list(comparelist)
        maincheck = self.table_check[self.tablename]
        maincheckdf = pd.read_sql(
            maincheck.statement, maincheck.session.bind)

        if maincheckdf is not None:
            if len(maincheckdf) == 0:
                return True
            else:
                records_entered = maincheckdf[
                    self.pk].values.tolist()
                check = [
                    x for x in list(
                        set(records_entered)) if x in comparelist]
                return len(check) == 0
        else:
            return True
            
    def go(self):
        '''
        Method to create indiviual orms and append records
        with information we have
        '''
        self.ormtable[self.tablename](
            self.df, self.pk, self.ormreg)

        for i in range(len(self.df)):
            dbupload = self.df.loc[
                i, self.df.columns].to_dict()
            for key in dbupload.items():
                setattr(
                    self.ormreg[i], key[0], key[1])
                orm.session.add(self.ormreg[i])
        orm.session.flush()


def site_add(df, tablekey, ormreg):
    for i in range(len(df)):
        ormreg[i] = orm.Sitetable(
            siteid = df.loc[i, tablekey])
        orm.session.add(ormreg[i])

def main_add(df, tablekey, ormreg):
    for i in range(len(df)):
        ormreg[i] = orm.Maintable(
            siteid = df.loc[i, tablekey])
        orm.session.add(ormreg[i])

def taxa_add(df, tablekey, ormreg):
    for i in range(len(df)):
        ormreg[i] = orm.Taxatable(
            projid = df.loc[i, tablekey])
        orm.session.add(ormreg[i])

def raw_add(df, tablekey, ormreg):
    for i in range(len(df)):
        ormreg[i] = orm.Rawtable(
            taxaid = df.loc[i, tablekey])
        orm.session.add(ormreg[i])
