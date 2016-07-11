#! /usr/bin/env python
import pandas as pd
from poplerGUI.logiclayer.datalayer import config as orm

__all__ = ['Flusher', 'flush']

def site_add(df, tablekey, ormreg, session):
    for i in range(len(df)):
        try:
            ormreg[i] = orm.Sitetable(
                siteid = df.loc[i, tablekey])
            session.add(ormreg[i])
        except Exception as e:
            session.rollback()
            print(str(e))
            raise ValueError('Could not map Site data')

def main_add(df, tablekey, ormreg, session):
    try:
        for i in range(len(df)):
            ormreg[i] = orm.Maintable(
                siteid = df.loc[i, tablekey])
            session.add(ormreg[i])
    except Exception as e:
        session.rollback()
        print(str(e))
        raise ValueError('Could not map Main data')

def taxa_add(df, tablekey, ormreg, session):
    try:
        for i in range(len(df)):
            ormreg[i] = orm.Taxatable(
                lter_proj_site = df.loc[i, tablekey])
            session.add(ormreg[i])
    except Exception as e:
        session.rollback()
        print(str(e))
        raise ValueError('Could not map Taxa data')

def raw_add(df, tablekey, ormreg, session):
    try:
        for i in range(len(df)):
            ormreg[i] = orm.Rawtable(
                taxaid = df.loc[i, tablekey])
            session.add(ormreg[i])
    except Exception as e:
        session.rollback()
        print(str(e))
        raise ValueError('Could not map Raw data')

class Flusher(object):

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

    def database_check(self, comparelist):
        print('in check block')
        comparelist = list(comparelist)
        session = orm.Session()
        if self.tablename == 'sitetable':
            maincheck = session.query(
                orm.Sitetable.siteid).order_by(
                    orm.Sitetable.siteid).filter(
                        orm.Sitetable.lterid == self.lterid)
        elif self.tablename == 'maintable':
            maincheck = session.query(
                orm.Maintable.metarecordid).order_by(
                    orm.Maintable.metarecordid)
        elif self.tablename == 'taxatable':
            maincheck = session.query(
                orm.Taxatable.lter_proj_site).order_by(
                    orm.Taxatable.lter_proj_site)
        elif self.tablename == 'rawtable':
            maincheck = session.query(
                orm.Rawtable.lter_proj_site).order_by(
                    orm.Rawtable.lter_proj_site)
        session.close()
        print('session closes in check')
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

    def go(self, session):
        '''
        method to a
        '''
        self.ormtable[self.tablename](
            self.df, self.pk, self.ormreg, session)

        try:
            for i in range(len(self.df)):
                dbupload = self.df.loc[
                    i, self.df.columns].to_dict()
                for key in dbupload.items():
                    setattr(
                        self.ormreg[i], key[0], key[1])
                    session.add(self.ormreg[i])
            session.flush()
            session.commit()
        except Exception as e:
            session.rollback()
            del session
            print(str(e))
            raise ValueError(
                'Could not update '+self.tablename+' values')

def flush(df,tablename,log,lter, sess):
    save_data = df

    if (tablename == 'sitetable' and
        save_data.loc[0, 'siteid'] in ['NULL', 'null'] and
        len(save_data) == 1 ):
        log.debug('Skipping database transaction')
    else:
        log.debug('Making database transaction')
        try:
            if tablename == 'sitetable':
                flush = Flusher(
                    save_data,
                    tablename,
                    'siteid',
                    lter)
                ck = flush.database_check(
                    save_data['siteid'].values.tolist())
            elif tablename == 'maintable':
                flush = Flusher(
                    save_data,
                    tablename,
                    'metarecordid',
                    lter)
                ck = flush.database_check(
                    save_data['metarecordid'].values.tolist())
            elif tablename == 'taxatable':
                flush = Flusher(
                    save_data,
                    tablename,
                    'lter_proj_site',
                    lter)
                ck = flush.database_check(
                    save_data['lter_proj_site'].values.tolist())
            elif tablename == 'rawtable':
                flush = Flusher(
                    save_data,
                    tablename,
                    'lter_proj_site',
                    lter)
                ck = flush.database_check(
                    save_data['lter_proj_site'].values.tolist())

            log.debug(
                'past database check: ' + tablename + str(ck))
            if ck is True:
                flush.go(sess)
            else:
                pass
        except Exception as e:
            print(str(e))
            log.debug(str(e))
            raise ValueError(str(e))
