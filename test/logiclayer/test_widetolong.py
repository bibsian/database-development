#!/usr/bin/env python
import pytest
from pandas import melt, DataFrame, read_csv
import sys, os
from poplerGUI.logiclayer import class_helpers as hlp

rootpath = os.path.dirname(os.path.dirname(os.path.dirname( __file__ )))
end = os.path.sep

@pytest.fixture
def df_long():
    return read_csv(
        rootpath + end + 'test' + end + 'Datasets_manual_test' + end +
        'long_data_test.csv'
    )

@pytest.fixture
def wide_to_long():
    def wide_to_long(dataframe, value_columns, value_column_name):
        all_columns = dataframe.columns.values.tolist()
        id_columns = [x for x in all_columns if x not in value_columns]
        melted_df = melt(
            dataframe,
            value_vars=value_columns, var_name='species_column',
            id_vars=id_columns, value_name=str(value_column_name)
        )
        return melted_df
    return wide_to_long

def test_long(df_long, wide_to_long):
    melted = wide_to_long(
        dataframe=df_long,
        value_columns=hlp.string_to_list(
            'PHT, PF, KRF, RBF, SDUNK, SDP, SDKR, SDRD, SDAN'),
        value_column_name='cover'
    )

    assert (
        hlp.string_to_list(
            'PHT, PF, KRF, RBF, SDUNK, SDP, SDKR, SDRD, SDAN') ==
        melted['species_column'].drop_duplicates().values.tolist()
    ) is True
    
