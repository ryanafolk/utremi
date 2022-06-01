#!/usr/bin/env python3

'''
Example:


mkdir combined_normalized
for i in `ls projected_weighted/*.tif | sed 's/.*_//g' | sed 's/\.tif//g' | sort | uniq`; do
./trim_sum_and_normalize_projections.py ./combined_normalized/${i}.combined.tif -178.2 6.6 -49.0 83.3 --rasters `ls projected_weighted/*_${i}.*tif`
done

'''


import argparse
import numpy
import rasterio
import gdal
import subprocess
import pandas
import re
import sys
import csv
import os

parser = argparse.ArgumentParser(description='Script to sum across species, crop, and normalize.')
parser.add_argument('outfile', action='store', help='Dating histogram table.')
parser.add_argument('x_upperleft', action='store', help='Degree coordinates of x upper left for trim.')
parser.add_argument('y_upperleft', action='store', help='Degree coordinates of x upper left for trim.')
parser.add_argument('x_lowerright', action='store', help='Degree coordinates of x upper left for trim.')
parser.add_argument('y_lowerright', action='store', help='Degree coordinates of x upper left for trim.')
parser.add_argument('-l','--rasters', nargs='+', help='List of rasters.', required=True)
args = parser.parse_args()

outfile = args.outfile
rasters = args.rasters
x_upperleft = args.x_upperleft
y_upperleft = args.y_upperleft
x_lowerright = args.x_lowerright
y_lowerright = args.y_lowerright

new_names = []
for raster in rasters:
	os.system("gdalwarp -of GTiff -overwrite -te {0} {1} {2} {3} {4} {4}.cropped".format(x_upperleft, y_upperleft, x_lowerright, y_lowerright, raster))
	new_names.append("{0}.cropped".format(raster))

with rasterio.open(raster, 'r') as ds:
	array = ds.read()  # read all raster values

rasters_new = [rasterio.open(x, 'r') for x in new_names]
print(rasters_new)
raster_arrays = [x.read() for x in rasters_new]
raster_arrays_missingfixed = []
for array in raster_arrays:
	array[array == 3.40282346600000016e+38] = 0
	
print(raster_arrays[0])
output_raster = numpy.nansum(raster_arrays, 0)


output_raster[output_raster == 0] = numpy.nan
output_raster[output_raster == numpy.inf] = numpy.nan

print(numpy.nansum(output_raster))
# Normalize to sum 1,000 (rather than one to keep pixel values reasonably large
normalized_output_raster = output_raster/numpy.nansum(output_raster)
normalized_output_raster = normalized_output_raster * 1000



print(normalized_output_raster)

metadata = rasters_new[0].profile

print(raster_arrays[0].shape)
print(normalized_output_raster.shape)

print(metadata)


with rasterio.open(outfile, 'w', **metadata) as dst:
			dst.write(normalized_output_raster)
			

