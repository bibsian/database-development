# This script is going to have the code
# for the TimeParser class
import pandas as pd
import re


class TimeParser(object):
    '''
    This class will be used to parse date information
    based on what is available in the raw data table
    that is being teased apart.It's essentially
    a helper class.
    
    It has four inputs:
    1) The data frame with raw date infomration
    2) The data frame column indexing the date information
    3) A dictionary correpsonding to a set of check boxes
    in the user interface
    4) An index from the list of check boxes to indicate what
    kind of time informatoin is present.

    The function essentially takes the number of time components
    based on whether it's 3 or 2 pieces, formats it into datetime
    and return a formated data frame where the information is
    parsed into individual columns (This is what we need to populate
    the database). 
    
    '''
    def __init__(
            self, dataframe, dfcolumn,  dictionary, dictindex):
        self.dataframe = dataframe
        self.dfcolumn = dfcolumn
        self.dictionary = dictionary
        self.dictindex = dictindex
        self.datetypenum = len(self.dictionary[self.dictindex])
        self.datetypename = self.dictionary[self.dictindex]

    # Based on the dictionary supplied to the class as well as
    # dictionary index, the program will decide which
    # potential formats the column in the raw data could take.
    def go(self):
        if self.datetypenum == 3:
            # List of the possible date formats to parse when
            # there are 3 components of time.
            # these functions will be attached to checkboxes
            # combinations could have
            # http://www.tutorialspoint.com/python/time_strftime.htm
            # The above site list python formats
            dateformats = [
                '%d %m %Y', '%d %m %y', '%d %Y %m', '%d %y %m',
                '%m %d %Y', '%m %d %y','%m %Y %d', '%m %y %d',
                '%Y %m %d', '%y %m %d','%Y %d %m', '%y %d %m',
                '%Y %j', '%y %j', '%j %Y', '%j %y']

    
        elif self.datetypenum == 2 and self.datetypename == 'my':
            # List of the possible date formats to parse when
            # there are 2 components of time with only month
            # and year information
            dateformats = [
                '%Y %m', '%y %m', '%m %Y', '%m %y']

        elif self.datetypenum == 2 and self.datetypename == 'dy':
            # List of the possible date formats to parse when
            # there are 2 components of time with only day
            # and year information
            dateformats = [
                '%Y %d', '%y %d', '%d %Y', '%d %y']

        elif self.datetypenum == 2 and self.datetypename == 'dm':
            # List of the possible date formats to parse when
            # there are 2 components of time with only day
            # and year information
            dateformats = [
                '%m %d', '%d %m', '%B %d', '%d %B', '%b %d', '%d %b']

        # If the data column only contains year information
        # no parsing is needed except column name change
        elif self.datetypenum == 1 and self.datetypename == 'y':
            try:
                formatedtime = pd.DataFrame(
                    self.dataframe[self.dfcolumn])
                formatedtime.columns = ['year']
                return formatedtime                
            except Exception as e:
                print(str(e))
                return
        # If the data column only contains month information
        # no parsing is needed except column name change
        elif self.datetypenum == 1 and self.datetypename == 'm':
            try:
                formatedtime = pd.DataFrame(
                    self.dataframe[self.dfcolumn])
                formatedtime.columns = ['month']
                return formatedtime
            except Exception as e:
                print(str(e))
                return
        # If the data column only contains day information
        # no parsing is needed except column name change
        elif self.datetypenum == 1 and self.datetypename == 'd':
            try:
                formatedtime = pd.DataFrame(
                    self.dataframe[self.dfcolumn])
                formatedtime.columns = ['day']
                return formatedtime
            except Exception as e:
                print(str(e))
                return
        # If the data column only contains julian day information
        # no parsing is needed except column name change
        elif self.datetypenum == 1 and self.datetypename == 'j':
            try:
                formatedtime = pd.DataFrame(
                    self.dataframe[self.dfcolumn])
                formatedtime.columns = ['julianday']
                return formatedtime
            except Exception as e:
                print(str(e))
                return
    

        # Making sure there ius a dateformats variable created
        try:
            print(dateformats)

        except Exception as e:
            print(str(e))
        
            # Looping over the potential formats the date column could
            # be in and trying to extract the relevant iformation
        for i,item in enumerate(dateformats):
            try:
                # Striping the date format based on potential
                # character that could separate informatoin
                testinput_re = [
                    re.sub("/|,|-|;"," ", x) \
                    for x in list(self.dataframe[self.dfcolumn].astype(str))]


                # Attempting to format the columns based on one of
                # the date formats the column could be in (this is
                # why we're iterating over a list)
                formatedtime = [pd.to_datetime(
                    x, format=dateformats[i]) for x in testinput_re]


                # if the dictionary index indicates this column has
                # three time components (day,month, year and any
                # combination of) they extract that info
                if self.datetypenum == 3:
                    tyear = [x.year for x in formatedtime]
                    tmonth = [x.month for x in formatedtime]
                    tday = [x.day for x in formatedtime]

                    # Once all the informatoin has been extracted
                    # and their list are created, return a
                    # data frame with the right format
                    if tyear and tmonth and tday is not None:
                        timeformateddf = pd.DataFrame(
                            {'year':tyear, 'month':tmonth, 'day':tday})
                        
                        return timeformateddf
                    else:
                        pass

                    # If the dictionary index indicats the column has
                    # 2 time compents and they are month and year,
                    # extract that information specifically
                elif self.datetypenum ==2 and\
                     self.datetypename is 'my':

                    tyear = [x.year for x in formatedtime]
                    tmonth = [x.month for x in formatedtime]

                    # Once the information is extracted return
                    # a dataframe with the formated informatoin
                    if tmonth and tyear is not None:
                        timeformateddf = pd.DataFrame(
                            {'month':tmonth, 'year':tyear})

                        return timeformateddf
                    
                    else:
                        pass

                # If the dictionary index indicats the column has
                # 2 time compents and they are day and year,
                # extract that information specifically
                elif self.datetypenum == 2 and\
                     self.datetypename is 'dy':

                    tyear = [x.year for x in formatedtime]
                    tday = [x.day for x in formatedtime]

                    # Once the information is extracted return
                    # a dataframe with the formated informatoin
                    if tday and tyear is not None:
                        timeformateddf = pd.DataFrame(
                            {'day':tday, 'year':tyear})

                        return timeformateddf
                    
                    else:
                        pass
                
                    # If the dictionary index indicats the column has
                    # 2 time compents and they are month and year,
                    # extract that information specifically
                elif self.datetypenum ==2 and\
                     self.datetypename is 'dm':

                    tmonth = [x.month for x in formatedtime]
                    tday = [x.day for x in formatedtime]

                    # Once the information is extracted return
                    # a dataframe with the formated informatoin
                    if tday and tmonth is not None:
                        timeformateddf = pd.DataFrame(
                            {'day':tday, 'month':tmonth})

                        return timeformateddf
                    
                    else:
                        pass
            except:
                print("Trying different date format.")
