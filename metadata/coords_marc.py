import gdal
import osr
import os
import pandas as pd
import pdb

path = './marc_data/OSD_coords.csv'
direction_cols = ['west', 'east', 'north', 'south']

# def getFiles (path):
#     paths = []
#     for (dirpath, dirnames, filenames) in os.walk(path):
#         clean_filenames = []
#         barred_file_exts = ['jpg', 'csv', 'xls', 'lsx', 'ovr', 'aux', 'asc']
#         for f in filenames:
#             if f[-3:] not in barred_file_exts:
#                 clean_filenames.append(f)
#
#         paths.append([dirpath, clean_filenames] )
#     return paths
#
# paths = getFiles(path)

df_coords = pd.read_csv(path)
df_coords = df_coords.reindex(columns=[*df_coords.columns.tolist(), *['034','255C']], fill_value=0)

# Convert to degrees, minutes, seconds
def decdeg2dms(dd):
    is_positive = dd >= 0
    dd = abs(dd)
    minutes, seconds = divmod(dd*3600,60)
    degrees, minutes = divmod(minutes,60)
    degrees = degrees if is_positive else -degrees
    return (int(degrees), int(minutes),int(round(seconds, 1)))

def decdeg2dmsTuples(df, i):
    decdegs = {}
    for c in direction_cols:
        decdegs[c] = decdeg2dms(df.loc[i, c])
    return decdegs

dmsBoundaries = [decdeg2dmsTuples(df_coords, i) for i in list(df_coords.index)]
# print(dmsBoundaries[0])

def formatCoord (bounds, direction):
    threeDigitBounds = '{:03}'.format(bounds[0]).replace('-', '0')

    if bounds[0] >= 0:
        if direction == 'WE':
            threeDigitBounds = 'E' + threeDigitBounds
        elif direction == 'NS':
            threeDigitBounds = 'N' + threeDigitBounds
    elif int(bounds[0]) < 0:
        if direction == 'WE':
            threeDigitBounds = 'W' + threeDigitBounds
        elif direction == 'NS':
            threeDigitBounds = 'S' + threeDigitBounds

    return threeDigitBounds + '{:02}'.format(bounds[1]) + '{:02}'.format(bounds[2])

def formatCoordDMS (boundary):
    # W0033343 to
    # (E010°48′40″--E010°48′54″/N063°32′40″--N063°32′34″) / W E N S
    return boundary[:4] + '°' + boundary[4:6] + '\'' + boundary[6:8] + '"'


for i, boundary in enumerate(dmsBoundaries):
    df_coords.loc[i, 'west_marc'] = formatCoord(boundary['west'], 'WE')
    df_coords.loc[i, 'east_marc'] = formatCoord(boundary['east'], 'WE')
    df_coords.loc[i, 'north_marc'] = formatCoord(boundary['north'], 'NS')
    df_coords.loc[i, 'south_marc'] = formatCoord(boundary['south'], 'NS')

    df_coords.loc[i, '255C'] = '(%s--%s/%s--%s)' % (formatCoordDMS(df_coords.loc[i, 'west_marc']), formatCoordDMS(df_coords.loc[i, 'east_marc']), formatCoordDMS(df_coords.loc[i, 'north_marc']), formatCoordDMS(df_coords.loc[i, 'south_marc']))
    # print(df_coords.loc[i, '255C'])

# $$dE0194678$$eE0356092$$f5127926$$gN5113133
# put all in one cell
# remove decimal from all
# first two coordinates: where there is a - swap it for W
# first two coordinates: where there is no - put E

for c in direction_cols:
    df_coords[c] = df_coords[c].astype(str)

df_coords['034'] = '$$d' + df_coords['west_marc'] + '$$e' + df_coords['east_marc'] + '$$f' + df_coords['north_marc'] + '$$g' + df_coords['south_marc']
print(df_coords.loc[0, '034'])

df_coords.to_csv('marc_boundaries.csv', sep=',', encoding='utf-8')
