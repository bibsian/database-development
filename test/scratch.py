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
        [study_site_table, site_in_project_table]).
    select_from(
        lter_table.__table__.
        join(study_site_table.__table__.join(site_in_project_table))
    ).alias('site_in_proj_join')
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
    select([site_in_proj_subq_stmt, project_table, taxa_table]).
    select_from(
        project_table.__table__.
        join(site_in_proj_subq_stmt.join(taxa_table)
        )
    ).alias('taxa join')
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
count_tbl_subq_stmt = (
    select([taxa_tbl_subq_stmt, count_table, biomass_table]).
    select_from(
        project_table.__table__.
        join(
            taxa_tbl_subq_stmt.join(
                count_table, onclause=and_(
                    taxa_tbl_subq_stmt.c.taxa_table_key ==
                    count_table.taxa_count_fkey,
                    taxa_tbl_subq_stmt.c.site_in_project_taxa_key ==
                    count_table.site_in_project_count_fkey
                )
            )
        ).join(
            biomass_table,
            onclause=and_(
                taxa_tbl_subq_stmt.c.taxa_table_key ==
                biomass_table.taxa_biomass_fkey,
                taxa_tbl_subq_stmt.c.site_in_project_taxa_key ==
                biomass_table.site_in_project_biomass_fkey
            )
        )
    ).alias('count join')
)


pretty.pprint(count_tbl_subq_stmt.compile().string)
Session = sessionmaker(bind=engine)
session = Session()
count_tbl_subq_result = session.execute(count_tbl_subq_stmt)
count_tbl_subq_df = pd.DataFrame(count_tbl_subq_result.fetchall())
count_tbl_subq_df.columns = count_tbl_subq_result.keys()
session.close()
count_tbl_subq_df
count_tbl_subq_df.columns
count_tbl_subq_df.to_csv('count_bio_outerjoin.csv')
