import pandas as pd
import sys, os
sys.path.append(os.path.realpath(os.path.dirname(__file__)))
import class_helpers as hlp
from itertools import chain

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
        Method to determine whether the entries for date information
        are all from the same columns or different columns.
        If they are in different columns the method
        concatenates all columns so that it can be read as a 
        single date time column.
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

        # Nested loop to do actually parsing of date information
        # and format it into three different columns
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
        Function to map/format time data that has been parsed and
        including columns with NULL values as entries.
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
