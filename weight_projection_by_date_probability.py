#!/usr/bin/env python3

'''
File names are a bit hard-coded below where indicated.

***Projections should be in a folder called "projected".

Example:

./weight_projection_by_date_probability.py dating_histograms.csv

'''


import argparse
import numpy
import rasterio
import gdal
import subprocess
import pandas
import re
import sys
import os
import csv

parser = argparse.ArgumentParser(description='Script to weight projections by date probability.')
parser.add_argument('infile', action='store', help='Dating histogram table.')
args = parser.parse_args()

file = args.infile

df = pandas.read_csv(file, index_col=0)

dates = df.index.values
taxa = df.columns

taxa = [str(re.sub("t_n", "", x)) for x in taxa]

print(dates)
print(taxa)

os.system("mkdir projected_weighted")


# IN THIS BLOCK CUSTOMIZE FILENAMES
for date in dates:
	for taxon in taxa:
		#print(df["t_n{0}".format(taxon)][date])
		#print("{0}.bio1_{1}.asc.tifout_BIOCLIM_1.tif".format(taxon, date))
		cmd = 'gdal_calc.py -A projected/{0}.Bio1_{1}.tifout_table_BIOCLIM_1.tif --outfile=projected_weighted/{0}.bio1_{1}.tif --calc="A*{2}"'.format(taxon, date, df["t_n{0}".format(taxon)][date])
		print(cmd)
		os.system(cmd) # Run gdal_calc




