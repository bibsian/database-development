import pytest
from pandas import read_csv, Series, concat
import sys
if sys.platform == "darwin":
    rootpath = (
        "/Users/bibsian/Desktop/git/database-development")
    end = "/"

elif sys.platform == "win32":
    rootpath = (
        "C:\\Users\MillerLab\\Desktop\\database-development")
    end = "\\"
from poplerGUI.logiclayer import class_helpers as hlp


@pytest.fixture
def df():
    return read_csv(
        rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
        'splitcolumn_data_test.csv'
    )

@pytest.fixture
def split_column():
    def split_column(dataframe, column, separator):
        splitdf = dataframe[
            column].apply(
                lambda x: Series([i for i in x.split(separator)]))
        
        return concat([dataframe, splitdf], axis=1)
    return split_column

@pytest.fixture
def cbind():
    def cbind(dataframe, column1, column2):
        try:
            column1 = int(column1)
            column2 = int(column2)
        except Exception as e:
            print(str(e))

        new_column = (
            dataframe[column1].astype(str) +
            ' ' +
            dataframe[column2].fillna('NULL').apply(
                lambda x: '' if x is 'NULL' else str(x))).apply(
                    lambda y: y.strip())
        return concat([dataframe, new_column], axis=1)
    return cbind


def test_space_split_then_cbind(df, split_column, cbind):
    test = split_column(df, 'space_sep', ' ')
    assert (0 in test.columns.tolist()) is True
    assert (1 in test.columns.tolist()) is True
    assert (2 in test.columns.tolist()) is True
    cbind_test = cbind(test, '0', '1')

    assert (df.loc[1,'species'] in cbind_test.iloc[1, 0]) is True
    assert (df.loc[2,'species'] in cbind_test.iloc[2, 0]) is True
    assert (df.loc[3,'species'] in cbind_test.iloc[3, 0]) is True
    assert (df.loc[4,'species'] in cbind_test.iloc[4, 0]) is True
    assert (df.loc[5,'species'] in cbind_test.iloc[5, 0]) is True


def test_dash_split(df, split_column):
    '''
    If -99999 are placeholders for NULL values and genus/spp names
    are separated by a dash (-), the negative gets dropped from -99999
    '''
    test = split_column(df, 'dash_sep', '-')
    assert (0 in test.columns.tolist()) is True




