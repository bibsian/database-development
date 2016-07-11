#!/usr/bin/env python

import pandas as pd
import numpy
from sys import platform as _platfor
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, create_engine
from sqlalchemy import Table, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import *
from sqlalchemy.sql.expression import update
from psycopg2.extensions import register_adapter, AsIs
from collections import OrderedDict
import sys, os

if _platform == "darwin":
    path = (
        "/Users/bibsian/Dropbox/database-development/data/")
elif _platform == "win32":
    path = (
        "C:\\Users\MillerLab\\Dropbox\\database-development\\data\\")

# Test data files
sitedata = pd.read_csv(path+'site_table_test.csv')
maindata = pd.read_csv(path+'main_table_test.csv')
taxadata = pd.read_csv(path+'taxa_table_test.csv')
rawdata = pd.read_csv(path+'raw_table_test.csv')
raw = pd.read_csv(path+'raw_data_test.csv')
