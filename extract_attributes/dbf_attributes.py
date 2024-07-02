from simpledbf import Dbf5
import os
import csv
from dbfread import DBF

# path = './dbfs'

def getDbfFiles (path):
    paths = []
    for (dirpath, subdirs, filenames) in os.walk(path):
        for file in filenames:
            if file.endswith('.dbf'):
                paths.append(os.path.join(dirpath, file))
    return paths

paths = getDbfFiles(path)

attributes = []

for p in paths:
    for i, df in enumerate(DBF(p, encoding='latin1')):
        if i == 1:
            break
        dfkeys = list(df.keys())
        dfvals = [df[key] for key in dfkeys]
        dfkeys.insert(0, p.replace(path, 'FIELD_'))
        dfvals.insert(0, p.replace(path, 'INCLUDE?_'))
        attributes.append(dfkeys)
        attributes.append(dfvals)


with open('./attributes.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     for r in attributes:
         wr.writerow(r)
