# Throw away script
import pandas as pd
from numpy import where
from collections import namedtuple, OrderedDict
import os, sys
from sys import platform as _platform
import re
if _platform == "darwin":
    metapath = (
    "/Users/bibsian/Dropbox/database-development/data" +
    "/meta_file_test.csv")
    testdatapath = (
    "/Users/bibsian/Dropbox/database-development/test" +
    "/DataRawTestFile.csv")
elif _platform == "win32":
    metapath = (
    "C:\\Users\MillerLab\\Dropbox\\database-development" +
    "\\data\\meta_file_test.csv")
    testdatapath = (
    "C:\\Users\MillerLab\\Dropbox\\database-development" +
    "\\test\\DataRawTestFile.csv")
metadf = pd.read_csv(metapath, encoding='iso-8859-11')
datadf = pd.read_csv(testdatapath)


tup = ('siteinfo', 'siteid')
tup[1]

f = 'dd - mm - YYYY (Any Order)'
f = 'YYYY'
f = 'mm - YYYY (Any Order)'
fnew = re.sub(
    'Any Order',"", f.strip("()")).strip("(").strip().split('-')
found = re.search('Y+', f)
ylength = len(found.group(0))

len(fnew[2].strip())


fnew = re.split('\s', f)

len(fnew[4])
d = 'NULL'
b = 'mm'

t =
['hello', 'hello', 'hello'].count('hello')
t.count(t[0]) == len(t)


check1 = [[1,1,1]]
pd.DataFrame(check1[0])


check = [[1,1,1], [2,2,2], [3,3,3]]
pd.DataFrame([list(x) for x in zip(*check1)])


if (d and b) is 'NULL'

'ULL' is 'NULL'
}
'NULL' in [None, None]

dset = ['month', 'day', 'year']

c = ['year']
[x for x in dset if x not in c]


os.path.split(metapath)[1]


taxalned = OrderedDict((
    ('sppcode', ''),
    ('kingdom', ''),
    ('phylum', 'TAXON_PHYLUM'),
    ('class', 'TAXON_CLASS'),
    ('order', 'TAXON_ORDER'),
    ('family', 'TAXON_FAMILY'),
    ('genus', 'TAXON_GENUS'),
    ('species', 'TAXON_SPECIES') 
))

list(taxalned.values())
taxackbox = OrderedDict((
    ('sppcode', False),
    ('kingdom', False),
    ('phylum', True),
    ('class', True),
    ('order', True),
    ('family', True),
    ('genus', True),
    ('species', True) 
))

available = [
    x for x,y in zip(
        list(taxalned.keys()), list(
            taxackbox.values()))
    if y is True
]


empty = pd.DataFrame()
not empty.values.tolist()
not datadf.values.tolist()

datadf['site'].values.tolist()
testcompdf = pd.DataFrame(
    ['ABUR', 'AHND', 'CULL ', 'SCDI', 'SCIdupe'], columns= ['site'])

testcompdf.values.tolist()


testdic = {
    'one': 1,
    'two': 2,
    'three': 3
}

testbool = {
    'one': True,
    'two':False,
    'three': True
}

avail = [x for x,y in zip(
    list(testdic.keys()), list(testbool.values()))
         if y is True]

def extract(d,keys):
    return dict((k, d[k]) for k in d if k in keys)

extract(testdic, avail)

datadf
datadfnew = datadf.copy()
datadfnew.loc[1, 'year'] = 1754


datadf.columns.values.tolist() == datadfnew.columns.values.tolist()


diffdf = (datadfnew != datadf)
any(diffdf['year'].values.tolist())
index = where(diffdf['year'].values)[0].tolist()
datadf.loc[index, 'year'].values.tolist()

for i,item in enumerate(diffdf.columns):
    if any(diffdf[item].values.tolist()):
        index = where(diffdf[item].values)[0].tolist()
        print('sitetable "{}" = {} to {}'.format(
            item,
            datadf.loc[index,item].values.tolist(),
            datadfnew.loc[index,item].values.tolist()))
    else:
        pass



test = {}
test['hello'] = 5
print(test)
test['hello'] = 10
print(test)
test['try'] = ''

'' not in test.values()

test1 = [1,2,3]
test2 = ['a', 'b', 'c']
test3 = zip(test1, test2)

for i,item in enumerate(test3):
    print(i)
    print(item[1])

lter = 'SBC'
idnumber = int('2')
metaurl = ('http://sbc.lternet.edu/cgi-bin/showDataset' +
           '.cgi?docid=knb-lter-sbc.17')
print(type(idnumber))
print(type(lter))
print(type(metaurl))

assert print((metadf.loc[metadf['global_id']==idnumber]['global_id']
        == idnumber).values[0]) is True

assert (metadf.loc[metadf['global_id']==idnumber]['lter']
        == lter).bool() is True

metadf.loc[metadf['global_id']==idnumber]['site_metadata'] == metaurl


test = namedtuple('commandobject', 'df fk')
testdict = {
    'caller': test(metadf, 'globalid')
}




testinst.commandliteral


testinst.df.iloc[2]
testinst.commandliteral

lned = {'sheet': '2', 'delim': '', 'tskip': '', 'bskip': ''}
lned.values()
lned.keys()

list(lned.values())


print([x for x,y in zip(list(lned.keys()), list(lned.values())) if
 y != ''])


lorg = ['ABUR', 'AHND', 'CULL', 'SCDI', 'SCDIdupe']
luser = ['ABUR', 'AHND', 'CULL', 'VTA', 'LBC']
change = [[x,y] for x,y in zip(lorg, luser) if x != y]
fromlist = []
tolist = []

for i,item in enumerate(change):
    fromlist.append(item[0])
    tolist.append(item[1])

newdf = datadf.replace(fromlist, tolist)
newdf

val1 = 'NUll '
val2 = 'NULL'
p = re.compile('\w+\s')
matches1 = p.match(val1)
matches2 = p.match(val2)

print(matches2)
print(matches1)

if matches2 is None:
    newstr = (val2 +' ')

inputkey = {'siteid': 'SITE'}
sitetable = {
    'columns': ['siteid', 'lat', 'lng', 'descript'],
    'time': False,
    'cov': False
}

availcol = list(inputkey.keys())
allcol = sitetable['columns']
list(set(allcol).difference(availcol))

dataframe = metadf.iloc[1,:]
# Creating main data table
maindata = pd.DataFrame(
    {
        'metarecordid':dataframe['global_id'], 
        'title': dataframe['title'],
        'samplingunits': 'NULL',
        'samplingprotocol': dataframe['data_type'],
        'structured': 'NULL',
        'studystartyr': 'AutoUpdated',
        'studyendyr': 'AutoUpdated',
        'siteid': 'AutoUpdated',
        'sitestartyr': 'AutoUpdated',
        'siteendyr': 'AutoUpdated',
        'samplefreq': 'AutoUpdated',
        'totalobs': 'AutoUpdated',
        'studytype': dataframe['study_type'],
        'community': dataframe['comm_data'],
        'uniquetaxaunits': 'AutoUpdated',
        # Spatial repliaction attributes
        'sp_rep1_ext': 'NULL',
        'sp_rep1_ext_units': 'NULL',
        'sp_rep1_label': 'AutoUpdated',
        'sp_rep1_uniquelevels': 'AutoUpdated',
        'sp_rep2_ext': 'NULL,',
        'sp_rep2_ext_units': 'NULL',
        'sp_rep2_label': 'AutoUpdated',
        'sp_rep2_uniquelevels': 'AutoUpdated',
        'sp_rep3_ext': 'NULL',
        'sp_rep3_ext_units': 'NULL',
        'sp_rep3_label': 'AutoUpdated',
        'sp_rep3_uniquelevels': 'AutoUpdated',
        'sp_rep4_ext': 'NULL',
        'sp_rep4_ext_units': 'NULL',
        'sp_rep4_label': 'AutoUpdated',
        'sp_rep4_uniquelevels': 'AutoUpdated',
        'authors': 'NULL',
        'authors_contact': 'NULL',
        'metalink': dataframe['site_metadata'],
        'knbid': dataframe['portal_id']
    },
    columns = [
    'metarecordid', 'title', 'samplingunits',
    'samplingprotocol', 'structured', 'studystartyr',
    'studyendyr', 'siteid',
    'sitestartyr', 'siteendyr', 'samplefreq', 'totalobs',
    'studytype', 'community', 'uniquetaxaunits',
    # Spatial repliaction attributes
    'sp_rep1_ext', 'sp_rep1_ext_units', 'sp_rep1_label',
    'sp_rep1_uniquelevels',
    'sp_rep2_ext', 'sp_rep2_ext_units', 'sp_rep2_label',
    'sp_rep2_uniquelevels',
    'sp_rep3_ext', 'sp_rep3_ext_units', 'sp_rep3_label',
    'sp_rep3_uniquelevels',
    'sp_rep4_ext', 'sp_rep4_ext_units', 'sp_rep4_label',
    'sp_rep4_uniquelevels',
    'authors', 'authors_contact', 'metalink', 'knbid'], index=[0])

maindata



