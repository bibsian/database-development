# Throw away script
import pandas as pd
import numpy as np
from collections import namedtuple

metapath = ('/Users/bibsian/Dropbox/database-development/data' +
            '/meta_file_test.csv')

metadf = pd.read_csv(metapath, encoding='iso-8859-11')


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
idnumber = 2
metaurl = ('http://sbc.lternet.edu/cgi-bin/showDataset' +
           '.cgi?docid=knb-lter-sbc.17')

np.int(2) == 2
metadf.loc[metadf['global_id']==idnumber]['global_id'] == idnumber
metadf.loc[metadf['global_id']==idnumber]['lter'] == lter
metadf.loc[metadf['global_id']==idnumber]['site_metadata'].values[0] == metaurl


test = namedtuple('commandobject', 'df commandliteral')

testinst = test(metadf, metadf['num_sites'])
testinst.df.iloc[2]
testinst.commandliteral
