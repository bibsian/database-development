#!/usr/bin/env python
import pytest
from pandas import read_csv
import sys
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development")
    end = "/"

elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development")
    end = "\\"

@pytest.fixture
def df():
    return read_csv(
        rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
        'raw_data_test_1.csv'
    )        

def test_replace(df):
    df.replace({None:'NULL'}, inplace = True)
    df.replace({'spelling': {'SPELLCHECK':'SpellCheck'}}, inplace=True)
    print(df)
    assert 0
