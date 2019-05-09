#!/usr/bin/env python

import subprocess as sp
import os
from os import path
import optparse

mydict = {} # hold the mapping rate results

for root, dirs, files in os.walk("./"):
	for filex in files:   
		if filex.endswith('_quant.log'):
			fullpath = os.path.join(root, filex)
			#print fullpath
			SAMMID = fullpath.split('/')[1] # yields SAMID
			#print fullpath2
			# loop over each line and pull out mapping rate
			with open(fullpath,'r') as f:
				for line in f:
					if "Mapping rate" in line:
						rate = line.split(' ')[7]
						rate = rate.strip('\n')
						rate = rate[:-1]
						print(rate)
						mydict[SAMMID]=rate # append to mydict

print(mydict)

with open('mappingrates.tsv', 'w') as out_file:
	out_file.write('ID' + "\t" + "Rate"+ "\n") 
	for key in mydict:
		towrite = (key + "\t" + mydict[key] + "\n")
		out_file.write(towrite) 
			
