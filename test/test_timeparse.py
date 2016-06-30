#!/usr/bin/env python
import pytest
import pandas as pd
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import class_helpers as hlp
from itertools import chain

# -----------
# Test data set
# -----------
@pytest.fixture
def df():
    return pd.read_csv('time_file_test.csv')

@pytest.fixture
def df2():
    return pd.read_csv('raw_data_test_dialogsite.csv')

# -----------
# 1 Column Input
# -----------
@pytest.fixture
def yearonly():
    d = {
        'dayname': '',
        'dayform': 'NULL',
        'monthname': '',
        'monthform': 'NULL',
        'yearname': 'y',
        'yearform': 'YYYY',
        'jd': False,
        'mspell': False
    }
    return d

@pytest.fixture
def monthonly():
    d = {
        'dayname': '',
        'dayform': 'NULL',
        'monthname': 'm',
        'monthform': 'mm',
        'yearname': '',
        'yearform': 'NULL',
        'jd': False,
        'mspell': False
    }
    return d

@pytest.fixture
def dayonly():
    d = {
        'dayname': 'd',
        'dayform': 'dd',
        'monthname': '',
        'monthform': 'NULL',
        'yearname': '',
        'yearform': 'NULL',
        'jd': False,
        'mspell': False
    }
    return d


# -----------
# 2 Column inputs
# -----------
@pytest.fixture
def monthyear4():
    d = {
        'dayname': '',
        'dayform': 'NULL',
        'monthname': 'm',
        'monthform': 'mm',
        'yearname': 'y',
        'yearform': 'YYYY',
        'jd': False,
        'mspell': False
    }
    return d

@pytest.fixture
def dayyear4():
    d = {
        'dayname': 'd',
        'dayform': 'dd',
        'monthname': '',
        'monthform': 'NULL',
        'yearname': 'y',
        'yearform': 'YYYY',
        'jd': False,
        'mspell': False
    }
    return d

@pytest.fixture
def daymonth():
    d = {
        'dayname': 'd',
        'dayform': 'dd',
        'monthname': 'm',
        'monthform': 'mm',
        'yearname': '',
        'yearform': 'NULL',
        'jd': False,
        'mspell': False
    }
    return d

@pytest.fixture
def monthyear4same():
    d = {
        'dayname': '',
        'dayform': 'NULL',
        'monthname': 'my',
        'monthform': 'mm-YY (Any Order) ',
        'yearname': 'my',
        'yearform': 'mm-YY (Any Order)',
        'jd': False,
        'mspell': False
    }
    return d

@pytest.fixture
def dayyear4same():
    d = {
        'dayname': 'd',
        'dayform': 'dd',
        'monthname': '',
        'monthform': 'NULL',
        'yearname': 'y',
        'yearform': 'YYYY',
        'jd': False,
        'mspell': False
    }
    return d

@pytest.fixture
def julianyear4():
    d = {
        'dayname': 'jd',
        'dayform': 'julian day',
        'monthname': '',
        'monthform': 'NULL',
        'yearname': 'y',
        'yearform': 'YYYY',
        'jd': True,
        'mspell': False
    }
    return d

# -----------
# All columns input
# -----------
@pytest.fixture
def monthdayyear4():
    d = {
        'dayname': 'mdy',
        'dayform': 'dd-mm-YYYY (Any Order)',
        'monthname': 'mdy',
        'monthform': 'dd-mm-YYYY (Any Order)',
        'yearname': 'mdy',
        'yearform': 'dd-mm-YYYY (Any Order)',
        'jd': False,
        'mspell': False
    }
    return d

@pytest.fixture
def daymonthyear4():
    d = {
        'dayname': 'dmy',
        'dayform': 'dd-mm-YYYY (Any Order)',
        'monthname': 'dmy',
        'monthform': 'dd-mm-YYYY (Any Order)',
        'yearname': 'dmy',
        'yearform': 'dd-mm-YYYY (Any Order)',
        'jd': False,
        'mspell': False
    }
    return d

@pytest.fixture
def daymonthyear4_df2():
    d = {
        'dayname': 'DATE',
        'dayform': 'dd-mm-YYYY (Any Order)',
        'monthname': 'DATE',
        'monthform': 'dd-mm-YYYY (Any Order)',
        'yearname': 'DATE',
        'yearform': 'dd-mm-YYYY (Any Order)',
        'jd': False,
        'mspell': False
    }
    return d


@pytest.fixture
def daymonthyear4_separate():
    d = {
        'dayname': 'd',
        'dayform': 'dd-mm-YYYY (Any Order)',
        'monthname': 'm',
        'monthform': 'dd-mm-YYYY (Any Order)',
        'yearname': 'y',
        'yearform': 'dd-mm-YYYY (Any Order)',
        'jd': False,
        'mspell': False
    }
    return d

@pytest.fixture
def daymonthyear4_same():
    d = {
        'dayname': 'dmy',
        'dayform': 'dd-mm-YYYY (Any Order)',
        'monthname': 'dmy',
        'monthform': 'dd-mm-YYYY (Any Order)',
        'yearname': 'dmy',
        'yearform': 'dd-mm-YYYY (Any Order)',
        'jd': False,
        'mspell': False
    }
    return d


@pytest.fixture
def dmy4_two_col_diff():
    d = {
        'dayname': 'dm',
        'dayform': 'dd-mm (Any Order)',
        'monthname': 'dm',
        'monthform': 'dd-mm (Any Order)',
        'yearname': 'y',
        'yearform': 'YYYY',
        'jd': False,
        'mspell': False
    }
    return d

# ------------
# TEST CLASS
# ------------
@pytest.fixture
def TimeParse():
    class TimeParse(object):
        def __init__(self, dataframe, datadict):
            self.data = dataframe
            self.dayname = datadict['dayname']
            self.dayform = datadict['dayform']
            self.monthname = datadict['monthname']
            self.monthform = datadict['monthform']
            self.yearname = datadict['yearname']
            self.yearform = datadict['yearform']
            self.jd = datadict['jd']
            self.mspell = datadict['mspell']
            self.mdyformat = [
                '%d %m %Y',  '%d %Y %m', '%m %d %Y', '%m %Y %d',
                '%Y %d %m', '%d %y %m','%d %m %y',
                '%m %d %y', '%m %y %d',
                '%Y %m %d', '%y %m %d', '%y %d %m',
                '%d %B %Y',  '%d %Y %B', '%B %d %Y', '%B %Y %d',
                '%Y %d %B', '%d %y %B','%d %B %y',
                '%B %d %y', '%B %y %d',
                '%Y %B %d', '%y %B %d', '%y %d %B',
                '%d %b %Y',  '%d %Y %b', '%b %d %Y', '%b %Y %d',
                '%Y %d %b', '%d %y %b','%d %b %y',
                '%b %d %y', '%b %y %d',
                '%Y %b %d', '%y %b %d', '%y %d %b',
            ]
            
            self.jdformat = [
                '%Y %j', '%j %Y', '%y %j', '%j %y'
            ]

            self.dyformat = ['%Y %d', '%y %d', '%d %Y', '%d %y']
            self.dmformat = [
                '%m %d', '%d %m', '%B %d', '%d %B', '%b %d', '%d %b']
            self.myformat = ['%Y %m', '%y %m', '%m %Y', '%m %y']

            self.yformat = ['%Y', '%y']
            self.mformat = ['%m', '%B', '%b']
            self.dformat = ['%d']

        @staticmethod
        def concatenator(
                data, name1_keep, name2_change, block, name3=None):
            '''
            Method to concatenate date informatoin that is separated
            into multiple columns (this makes it easier for formatting
            into the table into the database's structure)
            '''
            print('In '+block+' block')

            try:
                if name1_keep == name2_change:
                    concatname = name1_keep
                else:
                    data['concat1'] = data[
                        name1_keep].astype(str).str.cat(
                            data[name2_change].astype(
                                str), sep = '-')
                    concatname = 'concat1'
                    if name3 is not None:
                        data['concat2'] = data[
                            'concat1'].astype(str).str.cat(
                                data[name3].astype(str), sep = '-')
                        concatname = 'concat2'
                    else:
                        pass
                return concatname
                
            except Exception as e:
                print(str(e))


        @staticmethod
        def time_regex(data, col, form, nulls):
            '''
            Method to format the date columns in the raw data
            based on user input. Returns 3 formatted columns
            i.e. (year, month, day) including nulls
            '''
            fields = ['month', 'day', 'year']
            if any(isinstance(i, list) for i in col):
                col = list(chain.from_iterable(col))
            else:
                pass
                
            if len(nulls) > 0:
                nulldf = hlp.produce_null_df(
                    len(nulls), nulls, len(data), 'nan')

                
            else:
                nulldf = pd.DataFrame()            
            try:
                time_list_re = hlp.strip_time(data, col)
            except Exception as e:
                print(str(e))
                raise AttributeError('Could not strip time format')            
            notnull = [x for x in fields if x not in nulls]

            for i,item in enumerate(form):
                try:
                    time_form_list = []
                    for j in time_list_re:
                        time_form_list.append(
                            [
                                pd.to_datetime(
                                    x, format=form[i]) for x in
                                j
                            ]
                        )
                    if len(time_form_list) > 1:
                        timedf = pd.DataFrame(
                            [list(x) for x in zip(
                                *time_form_list)])

                    else:
                        timedf = pd.DataFrame(time_form_list[0])                    
                        if len(notnull) == 1:
                            timedf.columns = notnull
                        else:
                            pass
                    final = {'formatted': timedf, 'null': nulldf}
                    return final
                except Exception as e:
                    print(str(e))
                    print('Trying different format')

        @staticmethod
        def mapper(datedict, intervals):
            ''' 
            Function mapping time data that has been formated and
            time data the should have NULL values as entries.
            The parser above returns 'formated' data in a dictionary
            so it can be compiled here.
            '''
            print('In map block')
            try:
                interval_dict ={
                    'year': pd.DataFrame(
                        datedict['formatted'].iloc[:,0].dt.year,
                        columns=['year']),
                    'month': pd.DataFrame(
                        datedict['formatted'].iloc[:,0].dt.month,
                        columns=['month']),
                    'day': pd.DataFrame(
                        datedict['formatted'].iloc[:,0].dt.day,
                        columns=['day'])
                }
            
                interval_list = []
                for i,items in enumerate(intervals):
                    interval_list.append(
                        interval_dict[items]
                    )
                interval_list.append(datedict['null'])
                d1 = interval_list[0]
                for i,items in enumerate(interval_list):
                    if i > 0:
                        d1 = pd.concat([d1,items], axis=1)
                    else:
                        pass

                return d1
            except Exception as e:
                print(str(e))
                print('could not concatenate date-time data')


        def formater(self):
            '''
            Methods to specify to specify the parameters
            of the static methods above. Should handle all 
            potential use cases for the way date data will
            be formatted (i.e. raw data all in one column or
            spread across multiple columns)
            '''
            month = self.monthform
            day = self.dayform
            year = self.yearform
            count = [x for x in [month, day, year] if x is 'NULL']

            # 1 Column entry for date information
            if 'NULL' in [month,day,year] and len(count) > 1:

                # Year only data
                if day is 'NULL' and month is 'NULL':
                    print('In YEAR block')
                    yeardf = self.time_regex(
                        data=self.data, col=self.yearname,
                        form=self.yformat, nulls=['day', 'month'])
                    return  self.mapper(yeardf, ['year'])

                # Day only data
                elif month is 'NULL' and year is 'NULL':
                    print('In DAY block')
                    daydf = self.time_regex(
                        data=self.data, col=self.dayname,
                        form=self.dformat, nulls=['month', 'year'])
                    return self.mapper(daydf, ['day'])

                # Month only data
                elif day is 'NULL' and year is 'NULL':
                    print('In MONTH block')
                    monthdf = self.time_regex(
                        data=self.data, col=self.monthname,
                        form=self.mformat, nulls=['day', 'year'])
                    return self.mapper(monthdf, ['month'])

            # 2 Column entries for date information
            elif 'NULL' in [month,day,year] and len(count) == 1:

                # Day Column NULL
                if day is 'NULL':
                    catcol = self.concatenator(
                        data=self.data,
                        name1_keep=self.yearname,
                        name2_change=self.monthname,
                        block='MONTH_YEAR', name3=None)
                    monthyeardf = self.time_regex(
                        data=self.data, col=[catcol],
                        form=self.myformat, nulls=['day'])
                    return self.mapper(monthyeardf, ['month', 'year'])

                # Month is NULL (Not Julian Day Handler)
                if month is 'NULL' and self.jd is False:
                    catcol = self.concatenator(
                        data=self.data,
                        name1_keep=self.yearname,
                        name2_change=self.dayname,
                        block='DAY-YEAR', name3=None)
                    dayyeardf = self.time_regex(
                        data=self.data, col=[catcol],
                        form=self.dyformat, nulls=['month'])
                    return self.mapper(dayyeardf, ['day', 'year'])

                # MONTH is technically NULL
                # but Julian Day is account for here
                if month is 'NULL' and self.jd is True:
                    catcol = self.concatenator(
                        data=self.data,
                        name1_keep=self.yearname,
                        name2_change=self.dayname,
                        block='JD-YEAR', name3=None)
                    jdyeardf = self.time_regex(
                        data=self.data, col=[catcol],
                        form=self.jdformat, nulls=[])
                    return self.mapper(jdyeardf, [
                        'day','month', 'year'])

                # Year is NULL
                if year is 'NULL':
                    catcol = self.concatenator(
                        data=self.data,
                        name1_keep=self.monthname,
                        name2_change=self.dayname,
                        block='MONTH_DAY', name3=None)
                    daymonthdf = self.time_regex(
                        data=self.data, col=[catcol],
                        form=self.dmformat, nulls=['year'])
                    return self.mapper(daymonthdf, ['day', 'month'])

            # Three column entries for date information
            elif 'NULL' not in [month,day,year] and len(count) == 0:
                colnameslist = [
                    self.monthname, self.dayname, self.yearname]
                # 1 Column entry ALL data present
                if colnameslist.count(
                        colnameslist[0]) == len(colnameslist):
                    print('in all 1 column all data')
                    alldf = self.time_regex(
                        data=self.data, col=[self.yearname],
                        form=self.mdyformat, nulls=[])
                    return self.mapper(alldf, ['month', 'day', 'year'])
                
                # 2 Column entries ALL data present
                elif (month not in [day, year] and
                      [day, year].count(day) == 2):
                    catcol = self.concatenator(
                        data=self.data,
                        name1_keep=self.yearname,
                        name2_change=self.monthname,
                        block='MONTH_DAYYEAR', name3=None)
                    alldf = self.time_regex(
                        data=self.data, col=[catcol],
                        form=self.mdyformat, nulls=[])
                    return self.mapper(
                        alldf, ['month', 'day', 'year'])

                elif (day not in [month, year] and
                      [month,year].count(month) == 2):
                    catcol = self.concatenator(
                        data=self.data,
                        name1_keep=self.yearname,
                        name2_change=self.dayname,
                        block='DAY_MONTHYEAR', name3=None)
                    alldf = self.time_regex(
                        data=self.data, col=[catcol],
                        form=self.mdyformat, nulls=[])
                    return self.mapper(
                        alldf, ['month', 'day', 'year'])

                elif (year not in [day, month] and
                      [day, month].count(day) == 2):
                    catcol = self.concatenator(
                        data=self.data,
                        name1_keep=self.monthname,
                        name2_change=self.yearname,
                        block='YEAR_MONTHDAY', name3=None)
                    alldf = self.time_regex(
                        data=self.data, col=[catcol],
                        form=self.mdyformat, nulls=[])
                    return self.mapper(
                        alldf, ['month', 'day', 'year'])

                # 3 Column entries ALL data present
                else :
                    catcol = self.concatenator(
                        data=self.data,
                        name1_keep=self.monthname,
                        name2_change=self.yearname,
                        block='YEARMONTHDAY',
                        name3=self.dayname)
                    alldf = self.time_regex(
                        data=self.data, col=[catcol],
                        form=self.mdyformat, nulls=[])
                    return self.mapper(
                        alldf, ['month', 'day', 'year'])
    return TimeParse
# ------
# Begin Testing
# Singles (y, m, d)
# ------
def test_single_columns(df, yearonly, monthonly, dayonly, TimeParse):
    # year test block
    assert isinstance(df, pd.DataFrame)
    assert isinstance(yearonly, dict)
    assert isinstance(monthonly, dict)
    assert isinstance(dayonly, dict)
    ytest = TimeParse(df, yearonly)
    yeardf = ytest.formater()
#    print(yeardf)
    ytestlist = yeardf['year'].values.tolist()
    ytruelist = df['y'].values.tolist()
    assert (ytestlist == ytruelist) is True

    # month test block
    mtest = TimeParse(df, monthonly)
    monthdf = mtest.formater()
#    print(monthdf)
    monthtestlist = monthdf['month'].values.tolist()
    monthtruelist = df['m'].values.tolist()
    assert (monthtestlist == monthtruelist) is True

    # day test block
    dtest = TimeParse(df, dayonly)
    daydf = dtest.formater()
#    print(daydf)
    daytestlist = daydf['day'].values.tolist()
    daytruelist = df['d'].values.tolist()
    assert (daytestlist == daytruelist) is True
    
def test_double_columns_different(
        df, dayyear4, monthyear4, TimeParse, daymonth,
        julianyear4):
    # Month-year 4
    mytest = TimeParse(df, monthyear4)
#    print(mytest)
    mydf = mytest.formater()
#    print(mydf)
    yeartestlist = mydf['year'].values.tolist()
    yeartruelist = df['y'].values.tolist() 
    assert (yeartestlist == yeartruelist) is True
    monthtestlist = mydf['month'].values.tolist()
    monthtruelist = df['m'].values.tolist()
    assert (monthtestlist == monthtruelist) is True

    #day-year
    dytest = TimeParse(df, dayyear4)
    dytest = dytest.formater()
#    print(dytest)
    daytestlist = dytest['day'].values.tolist()
    daytruelist = df['d'].values.tolist()
    assert (daytestlist == daytruelist) is True
    yeartestlist = dytest['year'].values.tolist()
    assert (yeartestlist == yeartruelist) is True
    
    dmtest = TimeParse(df, daymonth)
    dmdf = dmtest.formater()
#    print(dmdf)
    daytestlist = dmdf['day'].values.tolist()
    assert (daytestlist == daytruelist) is True
    monthtestlist = dmdf['month'].values.tolist()
    assert (monthtestlist == monthtruelist) is True

    #day-year
    jdytest = TimeParse(df, julianyear4)
    jdytest = jdytest.formater()
#    print(jdytest)
    daytestlist = jdytest['day'].values.tolist()
    daytruelist = df['d'].values.tolist()
    assert (daytestlist == daytruelist) is True
    yeartestlist = jdytest['year'].values.tolist()
    assert (yeartestlist == yeartruelist) is True
    
    
def test_three_columns_same(
        df, TimeParse, monthdayyear4, daymonthyear4):
    alltest = TimeParse(df, monthdayyear4)
    alldf = alltest.formater()
    daytestlist = alldf['day'].values.tolist()
    monthtestlist = alldf['month'].values.tolist()
    yeartestlist = alldf['year'].values.tolist()
    daytruelist = df['d'].values.tolist()
    monthtruelist = df['m'].values.tolist()
    yeartruelist = df['y'].values.tolist()
    assert (daytestlist == daytruelist) is True
    assert (monthtestlist == monthtruelist) is True
    assert (yeartestlist == yeartruelist) is True

    all2test = TimeParse(df, daymonthyear4)
    all2df = all2test.formater()
    daytestlist = all2df['day'].values.tolist()
    monthtestlist = all2df['month'].values.tolist()
    yeartestlist = all2df['year'].values.tolist()
    assert (daytestlist == daytruelist) is True
    assert (monthtestlist == monthtruelist) is True
    assert (yeartestlist == yeartruelist) is True


def test_three_column_entries_all_data_different_names(
        df, TimeParse, daymonthyear4_separate):
    alltest = TimeParse(df, daymonthyear4_separate)
    alldf = alltest.formater()
#    print(alldf)
    yeartestlist = alldf['year'].values.tolist()
    monthtestlist = alldf['month'].values.tolist()
    daytestlist = alldf['day'].values.tolist()
    daytruelist = df['d'].values.tolist()
    monthtruelist = df['m'].values.tolist()
    yeartruelist = df['y'].values.tolist()
    assert (daytestlist == daytruelist) is True
    assert (monthtestlist == monthtruelist) is True
    assert (yeartestlist == yeartruelist) is True
    
def test_two_column_entries_all_data_different_names(
        df, TimeParse, dmy4_two_col_diff):
    alltest = TimeParse(df, dmy4_two_col_diff)
    alldf = alltest.formater()
    print(alldf)
    yeartestlist = alldf['year'].values.tolist()
    monthtestlist = alldf['month'].values.tolist()
    daytestlist = alldf['day'].values.tolist()
    daytruelist = df['d'].values.tolist()
    monthtruelist = df['m'].values.tolist()
    yeartruelist = df['y'].values.tolist()
    assert (daytestlist == daytruelist) is True
    assert (monthtestlist == monthtruelist) is True
    assert (yeartestlist == yeartruelist) is True

def test_all_same_column_mdy(df, TimeParse, daymonthyear4_same):
    alltest = TimeParse(df, daymonthyear4_same)
    alldf = alltest.formater()
    print(alldf)
    yeartestlist = alldf['year'].values.tolist()
    monthtestlist = alldf['month'].values.tolist()
    daytestlist = alldf['day'].values.tolist()
    daytruelist = df['d'].values.tolist()
    monthtruelist = df['m'].values.tolist()
    yeartruelist = df['y'].values.tolist()
    assert (daytestlist == daytruelist) is True
    assert (monthtestlist == monthtruelist) is True
    assert (yeartestlist == yeartruelist) is True

def test_all_same_column_mdy_df2(df2, TimeParse, daymonthyear4_df2):

    alltest = TimeParse(df2, daymonthyear4_df2)
    alldf = alltest.formater()
    print(alldf)
    yeartestlist = alldf['year'].values.tolist()
    monthtestlist = alldf['month'].values.tolist()
    daytestlist = alldf['day'].values.tolist()
    datecol = pd.to_datetime(df2['DATE'])
    daytruelist = datecol.dt.day.values.tolist()
    monthtruelist = datecol.dt.month.values.tolist()
    yeartruelist = datecol.dt.year.values.tolist()
    assert (daytestlist == daytruelist) is True
    assert (monthtestlist == monthtruelist) is True
    assert (yeartestlist == yeartruelist) is True
    
