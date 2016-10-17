import pytest
from pandas import read_csv, Series
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
    def split_column(
            dataframe, column, separator, firstcolname, secondcolname):
        all_columns = dataframe.columns.values.tolist()
        return all_columns
    return split_column


def test_long(df):
    test = df['space_sep'].apply(
        lambda x: Series([i for i in x.split(' ')]))
    print(test)

    assert 0
