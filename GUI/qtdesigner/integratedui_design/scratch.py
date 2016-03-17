# This python script is going to be used catch the
# signals emitted on the Site Names and Coorinates Form
# and process the information
import copy
import itertools
import json
import sys
import re
from collections import defaultdict
from sys import platform as _platform
import decimal as dc
import numbers as nm
import pandas as pd
import numpy as np
import config as config
from sqlalchemy import create_engine

import class_columntodictframe as cdictframe
import class_database as uow
import importlib



df = None



if _platform == "darwin":
    metapath = (
        "/Users/bibsian/Dropbox/database-development/data/meta_file_test.csv")
    rawpath = (
        "/Users/bibsian/Dropbox/database-development/data/raw_table_test_mod.csv")
    timepath = (
        "/Users/bibsian/Dropbox/database-development/data/time_file_test.csv")

elif _platform == "win32":
    #=======================#
    # Paths to data and conversion of files to dataframe
    #=======================#
    metapath = ("C:\\Users\MillerLab\\Dropbox\\database-development"
                + "\\data\\meta_file_test.csv")
    rawpath = ("C:\\Users\MillerLab\\Dropbox\\database-development"
               + "\\data\\raw_table_test_mod.csv")
    timepath = ("C:\\Users\MillerLab\\Dropbox\\database-development"
                + "\\data\\time_file_test.csv")

metadf = pd.read_csv(metapath, encoding="iso-8859-11")
rawdf = pd.read_csv(rawpath)
timedf = pd.read_csv(timepath)


metadf['temp_int']

#==============#
# Class to convert covariates
# columns to json data types
#===============#


#del ColumnToJsonFrame

rawdfmod = rawdf.replace(-99999, 'NULL', inplace=True)

class ColumnToDictionaryFrame():
    '''
    This class will convert a dataframe (given a list of columns)
    into a dataframe of json types where each row is a json
    data type of all observations from the columns in that row
    '''
    def __init__(self, dataframe, columnlist):
        self.data = dataframe
        self.names = list(columnlist)
        self.ncols = np.shape(dataframe)[1]
        self.nrows = np.shape(dataframe)[0]

    # Method to return the json dataframe
    def dict_df(self):
        
        self.jsonlist = []
        try:
            self.dictstartseq = [
                {self.data[self.names].columns[i]:None
                 for i,item in enumerate(self.names)}]

        except:
            raise AttributeError

        self.dictlist = [
            (self.dictstartseq[0]).copy() for x in range(self.nrows)]

        for col in self.names:
            for i in range(self.nrows):
                self.dictlist[i][col] = str(self.data[col].iloc[i])

        self.dictdf = pd.DataFrame(
            {'covariate': self.dictlist})
        self.dictdf['covariate'] = self.dictdf['covariate'].astype(str)

        return self.dictdf



print(dictlistalltest)

#del dictlistalltest
dictlistalltest = ColumnToDictionaryFrame(
    rawdf,['VIS', 'OBS_CODE', 'AREA', 'Substrate_type']).dict_df()

len(dictlistalltest.iloc[0][0])

del testdictdf
testdictdf = cdictframe.ColumnToDictionaryFrame(
    rawdf, ['VIS', 'OBS_CODE', 'AREA', 'Substrate_type']).dict_df()
len(testdictdf.iloc[0][0])

print(testdictdf)

testdictdfall = pd.concat([rawdf['COUNT'], testdictdf],axis=1)
testdictdfall.columns = ['unitobs', 'covariate']
testdictdfall['unitobs']= pd.to_numeric(
    testdictdfall['unitobs'], errors='coerce')

#del engine
# Enging to connect to postgres database
engine = create_engine(
    'postgresql+psycopg2://postgres:demography@localhost/ArrayTest',
    echo=True)

testdictdfall.to_sql(
    'rawobs', con=engine, if_exists="append", index=False)

    
    
#del testlist
testlist = ['VIS', 'OBS_CODE']

dictliststart = [
    {rawdf[testlist].columns[i]: None
     for i,item in enumerate(testlist)}]

#del dictlistall
#del dictlistalltest
dictlistall = [(dictliststart[0]).copy() for x in range(len(rawdf))]

#del jsonlist
jsonlist = []

for col in testlist:
    for i in range(len(rawdf)):
        dictlistall[i][col] = str(rawdf[col].iloc[i])

print(dictlistall[0:10])

type(jsonlist[0])

# del jsondf
# del testconcat
jsondf = pd.DataFrame(
    {'covariate':  dictlistall})

testconcat = pd.concat([rawdf['COUNT'],jsondf],axis=1)
testconcat['covariate']= testconcat['covariate'].astype(str)
testconcat.columns = ['unitobs', 'covariate']

type(testconcat.loc[0,'covariate'])

# Enging to connect to postgres database
engine = create_engine(
    'postgresql+psycopg2://postgres:demography@localhost/ArrayTest',
    echo=True)

testconcat.to_sql(
    'rawobs', con=engine, if_exists="append", index=False)

print(str(1))

#=======================#
# Test populate a database
# with queires from sql
#========================#
del sys.modules['class_database']
del sys.modules['config']
import class_database as uow
import config as config

session = config.Session()
q = uow.SiteTableQuery().go(session, config.sitetable)
type(q)
q[0]
len(q)
qdf = pd.DataFrame(q).iloc[:, 1:]
qdf.dtypes

qdf['lat'] = qdf['lat'].astype(float)
session.close()

session = config.Session()
q1 = uow.RawTableQuery().go(session, config.rawtable)
q1df = pd.DataFrame(q1).iloc[:,1:]

q1df.dtypes

q1df
    

#===============================#
# Test for turning numpy array into
# a dataframe
#==============================#
numpval = timedf.values
timedf == pd.DataFrame(numpval, columns=list(timedf.columns))

#==============================#
# Test Turning input into a string
#==============================#

# Getting list of users values
testname1 = 'ABUR, AHND, AQUE, BULL, CARP, GOLB, IVEE, MOHK, NAPL, SCDI, SCTW'
testnamelist = re.sub(",\s", " ", testname1.rstrip()).split()

#========================#
# Test matching list with different
# orders
#======================#
testname2 = 'AQUE, ABUR, AHND, CARP, BULL, GOLB, IVEE, MOHK, NAPL, SCDI, SCTW'
testname2list = re.sub(",\s", " ", testname2.rstrip()).split()


[x.lower() for x in testnamelist].sort() == [y.lower()
                                             for y in testname2list].sort()


#====================#
# Test for counting observations
# per site in data
#===================$
lengthlist = []
for i in testnamelist:
    subdf = rawdf[rawdf['site'] == i]
    lengthlist.append(len(subdf))

sum(lengthlist) == len(rawdf)

#===================#
# Test dataframe lookup methods
#====================#
# Subseting values from dataframe
globalid = 2
metaurl = 'http://sbc.lternet.edu/cgi-bin/showDataset.cgi?docid=knb-lter-sbc.17'
str(metadf.loc[metadf['global_id'] == globalid]
    ['site_metadata'].values[0]) == metaurl

#=====================#
# Test turning potentially NULL
# values into actual 'NULL'
#=====================#
# This can get a little tricky based on the data types of
# the data frame that is loaded.

# To handle this I'm giong to have the user separte
# their inputs into list of numeric and text values that
# represent 'NULL'

# All input that should be numeric will be converted but
# also treated as text.

# Example: Take an input of numerics that represent
# null_handle
testnulls = '-999, -9999, -99999, -999999'

# Convert them to a list
testnullslist = re.sub(",\s", " ", testnulls.rstrip()).split()

# Then convert to numeric
testnullsnumericlist = [int(x.strip(" ")) for x in testnullslist]

alltestlist = testnullslist

for i in testnullsnumericlist:
    alltestlist.append(i)

[type(x) for x in alltestlist]


testdf = pd.DataFrame.copy(rawdf)
testdf.dtypes

type(testdf) == pd.DataFrame

for i in alltestlist:
    for j in testdf.columns:
        testdf[j].replace(i, 'NULL', inplace=True)

testdf['TAXON_FORMER_SPECIES']
rawdf['TAXON_FORMER_SPECIES']


#======================#
# Test converting factors/numerics
# into month for data with season
# information
#=====================#
seasondictionary = {
    "spring": None, "summer": None, "fall": None, "winter": None}

seasonnumdictionary = {
    "spring": int(0), "summer": int(0), "fall": int(0), "winter": int(0)}

seasonindex = ['spring', 'summer', 'fall', 'winter']


seasonnumcolumn = 'SEASONnumeric'
seasonnumcolumnlist = re.sub(",\s", " ", seasonnumcolumn.rstrip()).split()

fallnum = '2'
summernum = '1'
seasonnums = [fallnum, summernum]


# Running user inputs through a number of try blocks
# to convert the input to a list of integers or text
# because it could be either.xs
try:
    # Strips off any spaces that may have been added
    # to the end of the user input
    seasonnum_re = [
        re.sub("\s,", " ", x.strip()) for x in seasonnums]
    print(seasonnum_re)
except Exception as e:
    print(str(e))

try:
    # Converts the list of strings into a list of integers
    seasonnumlist = [int(x.strip(" ")) for x in seasonnum_re]
    print(seasonnumlist)
except Exception as e:
    print(str(e))

try:
    # Check if numeric list of seasons exist if not then the required
    # list is a list of strings
    required = seasonnumlist
except Exception as e:
    print(str(e))
    required = seasonnum_re

seasonnumlist
seasonnumdictionary['fall'] = seasonnumlist[0]
seasonnumdictionary['summer'] = seasonnumlist[1]

rawdf['SEASONtext']
rawdf[seasonnumcolumn].replace()

any([x > 0 for i, x in seasonnumdictionary.items()])


for i, item in seasonnumdictionary.items():
    if item > 0:
        testdf[seasonnumcolumn].replace(item, i)
testdf

#=====================#
# Test Turning input into a string then a decimal value
#=====================#
testnumber1 = '100.0, 100.0, 111.0, 101.0, 102.0, 103.0, 203.0, 465.0, 123.0, 789.0, 111.0'
testnumberlist = re.sub(",\s", " ", testnumber1.rstrip()).split()
testnumberdec = [dc.Decimal(x.strip(" ")) for x in testnumberlist]
print([isinstance(x, nm.Number) for x in testnumberdec])

xlen(testnumberdec)
100.0 in set(testnumberdec)


#=============================#
# Test turning inputs of words into
# list of words
#==============================#
testwords = 'NO FISH, WHATS UP, NO RECORD, how often does this work'
testwordslist = re.sub("^,\s$", " ", testwords.rstrip()).split(",")


testword = 'No Fish'
testwordlist = re.sub("^,\s$", " ", testword.rstrip()).split(",")

del testwordslist

# Test boolean
'AQUE' in testnamelist

#====================#
# Test repeating values
#====================#
ids = []
descript = []
for i in enumerate(testnamelist):
    ids.append("NWT")
    descript.append('NULL')

#====================#
# Test making dataframe from list
# and adjusting datatypes with numpy
#====================#
newdf = pd.DataFrame({
    'siteID': testnamelist,
    'lterID': ids,
    'lat': np.array(testnumberdec, dtype=np.int64),
    'long': np.array(testnumberdec, dtype=np.int64),
    'descript': descript},
    columns=[
    'siteID', 'lterID', 'lat', 'long', 'descript'])
newdf.dtypes
newdf.columns

#======================#
# Test returning a boolean list
#=======================#
a = 1
b = 1
c = 1
d = [2, 3, 4, 5]
boolist1 = []
boolist2 = []

boolist1.append(a == b)

boolist2.append(a == b)
boolist2.append(b == c)
boolist2.append(len(d) >= 0)

all(boolist1)
all(boolist2)


#============================#
# Test methods to concatenate meta data information
#============================#
maincolumns = ['title', 'data_type', 'start_date', 'end_date',
               'temp_int', 'comm_data', 'study_type',
               'site_metadata', 'portal_id']

#============================#
# Test dataframe subseting
#============================#
subdf = metadf[globalid - 1:globalid][maincolumns]
subdf.dtypes

#========================#
# Test date parsing
#========================#
teststart = pd.to_datetime(subdf['start_date'], format="%m/%d/%Y").dt.year
testend = pd.to_datetime(subdf['end_date'], format="%m/%d/%Y").dt.year


#====================#
# Test created dataframe with one row
#=====================#
maindfpush = pd.DataFrame({
    'title': subdf['title'],
    'samplingunits': 'NULL',
    'samplingprotocol': subdf['data_type'],
    'startyr': teststart,
    'endyr': testend,
    'samplefreq': 'NULL',
    'totalobs': 'NULL',
    'studytype': subdf['study_type'],
    'community': subdf['comm_data'],
    'siteID': 'NULL',
    'sp_rep2_ext': 'NULL',
    'sp_rep3_ext': 'NULL',
    'sp_rep4_ext': 'NULL',
    'metalink': subdf['site_metadata'],
    'knbID': subdf['portal_id']},
    columns=[
    'title', 'samplingunits', 'samplingprotocol',
                              'startyr', 'endyr', 'samplefreq',
                              'totalobs', 'community', 'siteID',
                              'sp_rep2_ext', 'sp_rep3_ext', 'sp_rep4_ext',
                              'metalink', 'knbID'])


#====================#
# Test expanding the dataframe of 1 row to a given size
# ('len(testnamelist'))
#===================#
maindfconcat = pd.concat([maindfpush] * len(testnamelist), ignore_index=True)

#====================#
# Test appending entries of a dataframe with entries from a list
#====================#
for i in range(len(testnamelist)):
    maindfconcat.loc[i, 'siteID'] = testnamelist[i]


#================#
# Testing dictionary functionality
# and operations to put together the
# taxonomic tables
#================#
# Since the foreign key dependency is projID
# were going to have to break the taxonomic information
# by projID.

# This will require two steps, merging the raw dataframe with
# the correct project ID and then subseting the unique combinations
# of each taxonomic classifaction by projID

# Performing a unit of work to query the main database
# for the information we need to merge the data with
# projectID and siteID
mainq = uow.MainTableQuery().go(config.Session(), config.maintable)

projid = []
siteid = []

# Extracting the data into two list
for row in mainq:
    projid.append(row.projID)
    siteid.append(row.siteID)

# Combining two list into a dataframe
mergedatasql = pd.DataFrame(
    {'projID': projid, 'site': siteid})

# Adding a row of NULL values and changing the site location
# to have an ID to see how merge treats it
addrow = []
for i in range(len(rawdf.columns)):
    addrow.append("NULL")
addrow[3] = testnamelist[1]


# Attempting the merge
mergedataraw = rawdf[1:len(rawdf):300]
result = mergedataraw.append(
    pd.Series(addrow, index=list(rawdf.columns)), ignore_index=True)

# pd.merge worked!
merged = pd.merge(
    mergedatasql, result, left_on=['site'],
    right_on=['site'])


# Creat dictionary based on user input
testdict = {0: 'SP_CODE', 1: 'TAXON_KINGDOM', 7: 'TAXON_SPECIES'}

testdict[0]

# Seeing how we can use the dictionary object
for i in list(testdict.keys()):
    print(rawdf[testdict[i]])


mergedraw = pd.merge(
    mergedatasql, rawdf, left_on=['site'], right_on=['site'])


lookupcolumns = ['projID']
for i in testdict.values():
    lookupcolumns.append(i)
# Subseting the raw data frame with the column
# names that have been provided in the dictionary
testdf = mergedraw[lookupcolumns]


# Here were using the information we have regarding site names
# and the subsetting the original raw dataframe by siteID's and
# putting each subset into a list
dataframelist = []
for i in testnamelist:
    dataframelist.append(mergedraw[mergedraw['site'].isin([i])])


# Creaing a list of dataframe where there are unique combinations
# of dictionary values assigned above (unique combination of
# each column that will be specified by the user)
subdflist = []
for i in dataframelist:
    subdflist.append(i[lookupcolumns].drop_duplicates(lookupcolumns))

subdflist


# Collapsing the list of dataframes into one big
# dataframe that will be pushed to the database
subdfpush = subdflist[0]
subdfpush = subdfpush.append(subdflist[1::])
subdfpush

taxaprojtopush = list(set(subdfpush['projID']))

#======================#
# Testing converting taxa data columns
#=====================#
# Created a list of column names for the taxa table this
# is hard coded because it doesn't change
taxadfcol = ['projID', 'sppcode', 'kingdom', 'phylum', 'class',
             'order', 'family', 'genus', 'species', 'authority']

# Extracted the keys from the taxa dictionary
taxadictcolindex = list(testdict.keys())
# Added one to each index because
taxadictcolindex = [x + 1 for x in taxadictcolindex]


taxadictcol = list(testdict.values())
taxacurrentcol = list(subdfpush.columns)

for i in taxadictcolindex:
    print(taxadfcol[i])

taxacolumns = [taxadfcol[i] for i in taxadictcolindex]
taxacolumns.insert(0, 'projID')

subdfpush.columns = taxacolumns


#=============#
# Testing find the difference between two
# list and preserving the order of
#==============#
testset = set(taxacolumns)
missingcollist = [x for x in taxadfcol if x not in testset]


#=============#
# Test creating a dataframe of nulls for
# columns that are missing from the original
#=============#
taxanulldf = pd.DataFrame()
for i, item in enumerate(missingcollist):
    taxanulldf[missingcollist[i]] = item
    taxanulldf.loc[0] = 'NULL'

# Creating a dataframe of matching lengths
# that have nulls
taxanulldfconcat = pd.concat(
    [taxanulldf] * len(subdfpush), ignore_index=True)

taxafinal = pd.concat([subdfpush, taxanulldf], axis=1, ignore_index=True)
taxafinal.dtypes

uow.UploadToDatabase(
    taxafinal, config, 'taxatable',
    taxaprojIDlist=taxaprojtopush).push_table_to_postgres()


#==#
# Test unit of work query for
# taxatable information
#==#
test = ['sppcode']
test[0]
previoustaxaproj = []
for row in uow.TaxaTableQuery().go(config.Session(), config.taxatable):
    previoustaxaproj.append(row.projID)
    print(eval('row.' + test[0]))

print('row.' + test[0])

# List comprehension to compy project ID's if they are already
# present in the taxa table list
taxaprojcheck = [i for i in taxaprojtopush if i in previoustaxaproj]
len(taxaprojcheck)

dir(config.taxatable)

del taxacheck
taxacheck = uow.UploadToDatabase(
    subdfpush, config, 'taxatable',
    taxaprojIDlist=taxaprojtopush).check_previous_taxa()


print(taxacheck)

#-#
# Code chunck to re import class
#-#
del sys.modules['class_database']
import class_database as uow

#===================#
# Testing time parsing functions of
# pandas/ writing our own definitions
# just in case people are weird about things
#===================#
timedf.columns

timedf['mdy'][0]

col1names = list(timedf.columns)

# Creating a test function to parse columsn with
# multiple time components in them


def time_pieces(
        dataframe, dfcolumn, dictionary, dictindex):

    # List of the possible date formats to parse when
    # there are 3 components of time.
    # these functions will be attached to checkboxes
    # combinations could have
    # http://www.tutorialspoint.com/python/time_strftime.htm
    # The above site list python formats
    if len(dictionary[dictindex]) == 3:
        dateformats = [
            '%d %m %Y', '%d %m %y', '%d %Y %m', '%d %y %m',
            '%m %d %Y', '%m %d %y', '%m %Y %d', '%m %y %d',
            '%Y %m %d', '%y %m %d', '%Y %d %m', '%y %d %m',
            '%Y %j', '%y %j', '%j %Y', '%j %y']

    # List of possible formats where dictionary contains
    # time information with 2 components (month and year)
    if len(dictionary[dictindex]) == 2 and \
       dictionary[dictindex] == 'my':
        dateformats = [
            '%Y %m', '%y %m', '%m %Y', '%m %y']

    try:
        print(dateformats)

    except Exception as e:
        print(str(e))

    # Iterating over the potential formats
    # to see if we can parse the column correctly and
    # made a data frame where data information is formated
    # to be pushed to the data base
    for i, item in enumerate(dateformats):
        try:
            testinput = [
                re.sub("/|,|-|;", " ", x)
                for x in list(dataframe[dfcolumn].astype(str))]
            print(testinput)
            print(dateformats[i])

            formatedtime = [pd.to_datetime(
                x, format=dateformats[i]) for x in testinput]
            print(formatedtime)

            if len(dictionary[dictindex]) == 3:
                tyear = [x.year for x in formatedtime]
                tmonth = [x.month for x in formatedtime]
                tday = [x.day for x in formatedtime]

                if tyear and tmonth and tday is not None:
                    timeformateddf = pd.DataFrame(
                        {'year': tyear, 'month': tmonth, 'day': tday})

                    return timeformateddf

                else:
                    pass

            elif len(dictionary[dictindex]) == 2 and\
                    dictionary[dictindex] is 'my':

                tyear = [x.year for x in formatedtime]
                tmonth = [x.month for x in formatedtime]

                if tmonth and tyear is not None:
                    timeformateddf = pd.DataFrame(
                        {'month': tmonth, 'year': tyear})

                    return timeformateddf
                    break

                else:
                    pass

            elif len(dictionary[dictindex]) == 2 and\
                    dictionary[dictindex] == 'dy':
                print("On Wrong Block")

        except:
            print("Trying different formating option")

# Test the function
time_pieces(timedf, 'ym', col1formatdict, 1)

[re.sub("/|,|-|;", " ", x) for x in list(timedf['dm'].astype(str))]

col1formatdict = {
    0: 'dmy', 1: 'my', 2: 'dy', 3: 'dm',
    4: 'y', 5: 'm', 6: 'j', 7: 'd'}


import class_timeparse as tp
#-#
del sys.modules['class_timeparse']
import class_timeparse as tp

t = tp.TimeParser(timedf, 'dmy', col1formatdict, 0).go()
print(t)
t.dtypes


t['day'] = t['day'].astype(str)
t.dtypes


#=============================================#
# Test for multiple data frames to check what
# type of data is within--- NESTED LIST
#=============================================#
timedatalist = []

dmdata = tp.TimeParser(timedf, 'dm', col1formatdict, 3).go()
timedatalist.append(dmdata)
ydata = tp.TimeParser(timedf, 'y', col1formatdict, 4).go()
timedatalist.append(ydata)

timedatalistcol1 = [list(x.columns) for x in timedatalist]
timedatalistnum1 = [len(x.columns) for x in timedatalist]


#========================================#
# Test for multiple data frames to check what
# type of data is within--- NON-NESTED LIST
#==========================================#
col1formatdict = {
    0: 'dmy', 1: 'my', 2: 'dy', 3: 'dm',
    4: 'y', 5: 'm', 6: 'j', 7: 'd'}


timedatalist2 = []


jdata = tp.TimeParser(timedf, 'jd', col1formatdict, 6).go()
timedatalist2.append(jdata)
ydata = tp.TimeParser(timedf, 'y', col1formatdict, 4).go()
timedatalist2.append(ydata)

timealldf2 = pd.DataFrame()
timealldf2 = timealldf2.append(timedatalist2[0])
timealldf2 = pd.concat([timealldf2, timedatalist2[1]], axis=1)

t = pd.concat([timedatalist2[0], timedatalist2[1]], axis=1)


t['c'] = t[list(t.columns)[0]].astype(str).map(str) + "-" +\
    t[list(t.columns)[1]].astype(str)


for i, item in enumerate(timedatalist2):
    if i > 0:
        pd.concat([timealldf2, item], axis=1)
    else:
        pass
    print(item)

timedatalistcol2 = [list(x.columns) for x in timedatalist2]
timedatalistnum2 = [len(x.columns) for x in timedatalist2]

allcolumns1 = []
for i, item in enumerate(timedatalistcol1):
    for j in range(timedatalistnum1[i]):
        allcolumns1.append(timedatalistcol1[i][j])


allcolumns2 = []
for i, item in enumerate(timedatalistcol2):
    for j in range(timedatalistnum2[i]):
        allcolumns2.append(timedatalistcol2[i][j])

'julianday' and 'year' in allcolumns1
'day' not in allcolumns

t1 = [0]
t2 = [0, 1, 2]

[x for x in t2 if x not in t1]


names = ['hello', 'goodbye']

allnulls = pd.concat(
    [pd.DataFrame(re.sub(" ", " ", ('NULL ' * 5)).split())] * len(names), axis=1)

allnulls.columns = names


#=============================#
# Test for regular expression
# formating date time
#=============================#
test_re = [re.sub(":|-|/", " ", x) for x in list(timedf['dmy'].astype(str))]
testtime = [pd.to_datetime(x, format=dateformats[0]) for x in test_re]
tyear = [x.year for x in testtime]
tmonth = [x.month for x in testtime]
tday = [x.day for x in testtime]

##==============##
# Test config file contents
##==============##
base = automap_base()

engine = create_engine(
    'postgresql+psycopg2://postgres:demography@localhost/LTER', echo=True)

base.prepare(engine, reflect=True)

lter = base.classes.lter
site = base.classes.siteID
main = base.classes.main_data

site.__table__.foreign_keys
site.__table__.columns

Session = sessionmaker(bind=engine)


testclass = push.PushToDatabase(newdf, 'siteID')
testclass.connect_and_make_base()


session1 = Session()


lookup = 'siteID'
siteidcheck = []
for row in session1.query(site, site.siteID).all():
    siteidcheck.append(row.siteID)

checked = [i for i in siteidcheck if i in testnamelist]
if len(checked) > 0:
    pass
else:
    newdf.to_sql(str(site.__table__.name), con=engine,
                 if_exists="append", index=False)


session1
session1.close()

#================#
# Test string to extract date for log files
#================#
(str(TM.datetime.now()).split()[0]).replace("-", "_")

#==================#
# Test defining my own
# signal
#==================#


class ResendSignal(QtCore.QObject):
    ''' 
    User defined signal to resend
    information when necessary
    '''
    signalsent = QtCore.pyqtSignal(str)

    def __init__(self, words, parent=None):
        super().__init__(parent)
        self.words = words

    def go(self):
        self.signalsent.emit(self.words)


@QtCore.pyqtSlot(str)
def catch_signal(x):
    print("Caught %s" % x)

test = ResendSignal('hello world')

test.signalsent.connect(catch_signal)

test.go()

################


def produce_null_df(ncols, names, length, input):

        # Test regarding input types
    try:
        if (type(names) is list) == True and\
                (type(ncols) is int) == True:
            pass
    except:
        raise TypeError
        return

    # Create a NULL dataframe based on the length provided
    # Make the number of columns necessary
    # piece together along axis 1
    allnulls = pd.concat(
        [
            pd.DataFrame(re.sub(" ", " ", (str(input) * length))
                         .split())] * len(names), axis=1)
    # Rename columns
    allnulls.columns = names

    # Return objects
    return allnulls

missing = ['one', 'two', 'three']

produce_null_df(len(missing), missing, len(timedf), 'NULL ')
