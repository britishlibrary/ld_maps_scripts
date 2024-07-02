# ld_maps_scripts
Set of scripts for working with digital maps

## Dependencies

Install the dependencies, GDAL can sometimes be difficult to install.

On mac:

`brew install gdal`

Followed by creating and activating a virtual env:

`python3 -m venv gdal_env`
`source gdal_env/bin/activate`

And then installing the dependencies inside the virtual env:

`pip install gdal`
`pip install osr`

Install gdal, note: python gdal must match system gdal

Check system version using `gdalinfo --version`
Match with pip eg `pip install gdal==2.4`

## Metadata

Python scripts to open a file system of vector and raster GIS data and create metadata in a spreadsheet in MARC formats.

### bounding_box.py
Place the bounding_box.py script in the same directory as the GIS data.

Replace the path variable on line 6 (`path = './test_data'`) to point to your GIS data (eg `path = './'` if in the same directory as the GIS data).

### dimensions.py
Open a directory of rasters, output pixels to spreadsheet in marc format.

### coords_marc.py
Take a spreadsheet of lat/lng and convert to MARC format.

## Extract attributes
Takes a set of geopackage or shp vector files, extracts attribute names and adds them to a spreadsheet to determine whether they should appear in viewer popups.

## Invalid UTF8
Takes a set of vector data encoded in utf-8 and corrects encoding errors replacing errors.
