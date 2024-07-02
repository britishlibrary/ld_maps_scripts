import geopandas as gpd
import fiona
import os
import csv
import pdb

path = './geopkgs'
# path = '/Volumes/VERBATIM HD/del Legal Deposit add to staging/'

def getGeopkgPaths (path):
    paths = []
    for (dirpath, subdirs, filenames) in os.walk(path):
        for file in filenames:
            if file.endswith('.gpkg'):
                paths.append(os.path.join(dirpath, file))
    return paths

paths = getGeopkgPaths(path)

attributes = []

for p in paths:
    # for i, df in enumerate(DBF(p, encoding='latin1')):
    for layername in fiona.listlayers(p):
        print(layername)
        geopkg = gpd.read_file(p, layer=layername)

        cols = list(geopkg.columns.drop('geometry'))
        cols.insert(0, p.replace('./geopkgs', 'FIELD_') + '/' + layername)
        attributes.append(cols)

        # for col in geopkg.columns.drop('geometry'):
        vals = [geopkg[c][0] for c in geopkg.columns.drop('geometry')]
        vals.insert(0, p.replace('./geopkgs', 'INCLUDE?_') + '/' + layername)
        attributes.append(vals)

with open('./attributes.csv', 'w', newline='') as myfile:
     wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
     for r in attributes:
         wr.writerow(r)
