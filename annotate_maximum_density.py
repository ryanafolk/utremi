#! /usr/bin/env python3

'''

Usage:

for f in out_*.tre; do
g=`echo ${f} | sed 's/\.tre//g'`
./annotate_maximum_density.py ${f} ${g}.maxdensity.tre
done


'''

import dendropy
import argparse
import numpy
from pprint import pprint

def pick_label(tree):
	for node in tree.preorder_node_iter(): # Iterate over nodes
		node_annotations = node.annotations.values_as_dict() # Obtain node annotations as dictionary
		for key in node_annotations:
			node_annotations[key] = float(node_annotations[key]) # Important to get this to float -- imported as string
		max_key = max(node_annotations, key=lambda k: node_annotations[k]) # Obtain bin label (dictionary key) for highest probability density (dictionary value)
		pprint(node_annotations) # Nice dictionary printing
		print(max_key)
		node.annotations.drop()
		node.annotations.add_new('variable', max_key)
		print(node.annotations)
	return tree

parser = argparse.ArgumentParser(description='Script to annotate tree with maximum-density values from histograms.')
parser.add_argument('treefile', action='store', help='Tree in nexus format.')
parser.add_argument('outfile', action='store', help='Output tree in nexus format.')
args = parser.parse_args()

outfile = args.outfile
treefile = args.treefile


tree = dendropy.Tree.get(path = treefile, schema='nexus', extract_comment_metadata = True)
tree_maxdensity = pick_label(tree)

tree.write(path=outfile, schema="nexus", annotations_as_nhx = True)