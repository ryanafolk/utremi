#!/usr/bin/env python3

'''
Example:
./projections_binned_ancestralreconstruction.py ./ancestral_reconstruction_tables/out_table_BIOCLIM_1.txt ./BIOCLIM_1 -l ./ShellyFinal_NovemberLayers_2019/bio1_final/*.tif

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

parser = argparse.ArgumentParser(description='Script to project from binning ancestral reconstruction results.')
parser.add_argument('infile', action='store', help='Ancestral reconstruction table.')
parser.add_argument('outfile', action='store', help='Name of the outfile prefix.')
parser.add_argument('-l','--scenarios', nargs='+', help='List of scenarios.', required=True)
args = parser.parse_args()

file = args.infile
outfile = args.outfile
scenarios = args.scenarios

with open(file) as f:
	reader = csv.reader(f)
	bins = next(reader)
	
while("" in bins): 
	bins.remove("") 
bins = [float(x) for x in bins]
bins.append(bins[-1] + bins[1] - bins[0]) # Add a final bin to close the last interval
#print(bins)


df = pandas.read_csv(file, index_col=0)
df = df[df['Unnamed: 1'] == "maximum_likelihood"]
internal_nodes = [x for x in df.index.values if x.isnumeric()]
df = df.loc[internal_nodes]
#print(internal_nodes)
del df['Unnamed: 1'] # Remove second row with labels
#print(df)


for raster in scenarios:
	print("On scenario: {0}".format(raster))
	for species in internal_nodes:
		species_corrected = int(species) + 1 
		print("On species: {0}".format(species_corrected)) # Numbering is one off between MCMCtree and binning reconstruction
		with rasterio.open(raster, 'r') as ds:
			array = ds.read()  # read all raster values
			metadata = ds.profile
			#print(array.shape)  # this is a 3D numpy array, with dimensions [band, row, col]
			for first, second in zip(bins, bins[1:]):
				# If pixel is between the two bin boundaries, we substitute with bin height using a pandas lookup
				# Write as string to avoid overwriting on successive queries
				array[(array >= first) & (array < second)] = str(df[str(first)][str(species)]) 
			
			# Remove any pixels outside of the histogram bounds
			array[(array < bins[0]) | (array >= bins[-1])] = 0 
			
			# Back to float type
			array.astype(float)
		
		with rasterio.open('{0}.{1}{2}.tif'.format(species_corrected, re.sub(".*/", "", raster), re.sub("\..*", "", re.sub(".*/", "", file))), 'w', **metadata) as dst:
			dst.write(array)


