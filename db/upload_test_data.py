#! /usr/bin/env python
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import *
from sqlalchemy.dialects.postgresql import *
import pandas as pd
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

# Reading in test datasets
count = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test'+
    end + 'raw_data_test_1.csv')

density = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test'+
    end + 'raw_data_test_2.csv')

biomass = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test'+
    end + 'raw_data_test_3.csv')

percent = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test'+
    end + 'raw_data_test_4.csv')

individual = pd.read_csv(
    rootpath + 'test' + end + 'Datasets_manual_test'+
    end + 'raw_data_test_5.csv')

