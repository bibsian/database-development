#! /usr/bin/env python
from collections import OrderedDict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.orm import sessionmaker, load_only
import pandas as pd
from poplerGUI.logiclayer.datalayer import config as orm

def go():
    table_dict = OrderedDict([
        ('biomass_table', orm.biomass_table),
        ('count_table', orm.count_table),
        ('density_table', orm.density_table),
        ('individual_table', orm.individual_table),
        ('percent_cover_table', orm.percent_cover_table),
        ('taxa_accepted_table', orm.taxa_accepted_table),
        ('taxa_table', orm.taxa_table),
        ('site_in_project_table', orm.site_in_project_table),
        ('project_table', orm.project_table),
        ('study_site_table', orm.study_site_table)]
    )
    for i, item in enumerate(table_dict):
        delete_statement = table_dict[item].__table__.delete()
        orm.conn.execute(delete_statement)
    orm.conn.close()

if __name__ == "__main__":
    go()
