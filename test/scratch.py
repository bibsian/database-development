from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.orm import sessionmaker, load_only
import pandas as pd
import pprint as pp
import sys, os
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development/")
    end = "/"

elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development\\")
    end = "\\"

engine = create_engine(
    'postgresql+psycopg2:///',
    echo=True)
metadata = MetaData(bind=engine)
base = declarative_base()
conn = engine.connect()

# creating classes for tables to query things
class lter_table(base):
    __table__ = Table('lter_table', metadata, autoload=True)
class study_site_table(base):
    __table__ = Table('study_site_table', metadata, autoload=True)
class project_table(base):
    __table__ = Table('project_table', metadata, autoload=True)
class site_in_project_table(base):
    __table__ = Table('site_in_project_table', metadata, autoload=True)
class taxa_table(base):
    __table__ = Table('taxa_table', metadata, autoload=True)
class biomass_table(base):
    __table__ = Table('biomass_table', metadata, autoload=True)
class count_table(base):
    __table__ = Table('count_table', metadata, autoload=True)
class density_table(base):
    __table__ = Table('density_table', metadata, autoload=True)
class percent_cover_table(base):
    __table__ = Table('percent_cover_table', metadata, autoload=True)
class individual_table(base):
    __table__ = Table('individual_table', metadata, autoload=True)


# First subquery links the site_in_project_table
# to the study_site table and lter_table

site_in_proj_subq_stmt = (
    select(
        [
            site_in_project_table,
            study_site_table,
            lter_table.lat.label('lter_lat'),
            lter_table.lng.label('lter_lng'),
            lter_table.lterid,
            project_table
        ]).
    select_from(
        site_in_project_table.__table__.
        join(study_site_table.__table__).
        join(lter_table.__table__).join(project_table)).alias()
)

pretty = pp.PrettyPrinter()

pretty.pprint(site_in_proj_subq_stmt.compile().string)
Session = sessionmaker(bind=engine)
session = Session()
site_in_proj_subq_result = session.execute(site_in_proj_subq_stmt)
site_in_proj_subq_df = pd.DataFrame(site_in_proj_subq_result.fetchall())
site_in_proj_subq_df.columns = site_in_proj_subq_result.keys()
session.close()
site_in_proj_subq_df
site_in_proj_subq_df.columns


# Second subquery links the project_table to our
# first subquery
taxa_tbl_subq_stmt = (
    select([site_in_proj_subq_stmt, taxa_table]).
    select_from(
        site_in_proj_subq_stmt.
        join(taxa_table)).alias()
)


pretty.pprint(taxa_tbl_subq_stmt.compile().string)
Session = sessionmaker(bind=engine)
session = Session()
taxa_tbl_subq_result = session.execute(taxa_tbl_subq_stmt)
taxa_tbl_subq_df = pd.DataFrame(taxa_tbl_subq_result.fetchall())
taxa_tbl_subq_df.columns = taxa_tbl_subq_result.keys()
session.close()
taxa_tbl_subq_df.columns
taxa_tbl_subq_df



# Second subquery links the project_table to our
# first subquery
union_all_select_stmt = union(
    select([
        taxa_tbl_subq_stmt,
        count_table]).
    select_from(
        taxa_tbl_subq_stmt.
        join(
            count_table,
            onclause=and_(
                taxa_tbl_subq_stmt.c.taxa_table_key ==
                count_table.taxa_count_fkey,
                taxa_tbl_subq_stmt.c.site_in_project_key ==
                count_table.site_in_project_count_fkey
            )
        )
    ).alias('count join'),
    select([
        taxa_tbl_subq_stmt,
        biomass_table]).
    select_from(
        taxa_tbl_subq_stmt.
        join(
            biomass_table,
            onclause=and_(
                taxa_tbl_subq_stmt.c.taxa_table_key ==
                biomass_table.taxa_biomass_fkey,
                taxa_tbl_subq_stmt.c.site_in_project_key ==
                biomass_table.site_in_project_biomass_fkey
            )
        )
    ).alias('biomass join'),
    select([
        taxa_tbl_subq_stmt,
        density_table]).
    select_from(
        taxa_tbl_subq_stmt.
        join(
            density_table,
            onclause=and_(
                taxa_tbl_subq_stmt.c.taxa_table_key ==
                density_table.taxa_density_fkey,
                taxa_tbl_subq_stmt.c.site_in_project_key ==
                density_table.site_in_project_density_fkey
            )
        )
    ).alias('density join'),
    select([
        taxa_tbl_subq_stmt,
        percent_cover_table]).
    select_from(
        taxa_tbl_subq_stmt.
        join(
            percent_cover_table,
            onclause=and_(
                taxa_tbl_subq_stmt.c.taxa_table_key ==
                percent_cover_table.taxa_percent_cover_fkey,
                taxa_tbl_subq_stmt.c.site_in_project_key ==
                percent_cover_table.site_in_project_percent_cover_fkey
            )
        )
    ).alias('perecent cover join')
)


pretty.pprint(union_all_select_stmt.compile().string)
Session = sessionmaker(bind=engine)
session = Session()
union_all_select_result = session.execute(union_all_select_stmt)
union_all_select_df = pd.DataFrame(union_all_select_result.fetchall())
union_all_select_df.columns = union_all_select_result.keys()
session.close()
union_all_select_df
union_all_select_df.columns
union_all_select_df.to_csv('union_all_select.csv')
