# Throw away script
import pandas as pd
import numpy as np
from collections import namedtuple
from sys import platform as _platform
import re
import numbers
import decimal


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


test = namedtuple('commandobject', 'df commandliteral')

testinst = test(metadf, metadf['num_sites'])
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
