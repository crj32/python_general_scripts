#!/usr/bin/env python

## usage: run in directory with your fastq.gz files, followed by 'multiqc .' in terminal to make report

import shutil
import time
import os
import os.path
import sys
import gzip
import subprocess as sp

# functions for running fastqc on everything

def make_list(ending): # make list of files to be run with fastqc
	fastqc_file_list = []
	for root, dirs, files in os.walk("./"):
		for filex in files:  
			if filex.endswith(ending): # should be .fastq or .fq, but python seems buggy!
				print(filex)
				fullpath = os.path.join(root, filex)
				fastqc_file_list.append(fullpath)
	print(fastqc_file_list)
	return fastqc_file_list

def fastqc(fastqc_file_list): # running fastqc on file list
	for filey in fastqc_file_list:
		print(filey)
		outdir = filey.split('_')[1] # this may change depending on the directory structure
		fastqc = 'fastqc'
		# use current directory
		print(outdir)
		proc = sp.Popen([fastqc, filey, '--extract']) # --extract '-o', outdir, 
		proc.wait()

## run

#list = make_list('.fastq.gz')
#fastqc(list)

