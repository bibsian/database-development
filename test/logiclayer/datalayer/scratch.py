from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    select, update, MetaData, create_engine, Table, column)
from sqlalchemy.orm import sessionmaker, relationship
import pandas as pd
import pprint as pp

engine = create_engine(
    'postgresql+psycopg2://lter:bigdata@45.55.241.186/popler_3'
)
conn = engine.connect()

# Mapping metadata
metadata = MetaData(bind=engine)
# Creating base
base = declarative_base()

# creating classes for tables to query things
class lter_table(base):
    __table__ = Table('lter_table', metadata, autoload=True)
class study_site_table(base):
    __table__ = Table('study_site_table', metadata, autoload=True)
class project_table(base):
    __table__ = Table('project_table', metadata, autoload=True)
    taxa = relationship(
        'taxa_table', cascade="delete, delete-orphan")
    count = relationship(
        'count_table', cascade="delete, delete-orphan")
    density = relationship(
        'density_table', cascade="delete, delete-orphan")
    biomass = relationship(
        'biomass_table', cascade="delete, delete-orphan")
    percent_cover = relationship(
        'percent_cover_table', cascade="delete, delete-orphan")
    individual = relationship(
        'individual_table', cascade="delete, delete-orphan")
class site_in_project_table(base):
    __table__ = Table('site_in_project_table', metadata, autoload=True)
class taxa_table(base):
    __table__ = Table('taxa_table', metadata, autoload=True)
class taxa_accepted_table(base):
    __table__ = Table('taxa_accepted_table', metadata, autoload=True)
class count_table(base):
    __table__ = Table('count_table', metadata, autoload=True)
class biomass_table(base):
    __table__ = Table('biomass_table', metadata, autoload=True)
class density_table(base):
    __table__ = Table('density_table', metadata, autoload=True)
class percent_cover_table(base):
    __table__ = Table('percent_cover_table', metadata, autoload=True)
class individual_table(base):
    __table__ = Table('individual_table', metadata, autoload=True)


Session = sessionmaker(bind=engine, autoflush=False)

session = Session()
sitecheck = session.query(
    study_site_table.study_site_key).order_by(
        study_site_table.study_site_key).filter(
            study_site_table.lter_table_fkey == 'SBC'
            )
session.close()
sitecheckdf = pd.read_sql(
    sitecheck.statement, sitecheck.session.bind)

site_in_proj_subq_stmt = (
    select(
        [
            site_in_project_table,
            study_site_table,
            lter_table.lat_lter,
            lter_table.lng_lter,
            lter_table.lterid,
            project_table
        ]).
    select_from(
        site_in_project_table.__table__.
        join(study_site_table.__table__).
        join(lter_table.__table__).join(project_table)).alias()
)

pretty = pp.PrettyPrinter()

# pretty.pprint(site_in_proj_subq_stmt.compile().string)
Session = sessionmaker(bind=engine)
session = Session()
site_in_proj_subq_result = session.execute(site_in_proj_subq_stmt)
site_in_proj_subq_df = pd.DataFrame(site_in_proj_subq_result.fetchall())
site_in_proj_subq_df.columns = site_in_proj_subq_result.keys()
session.close()
