#!/usr/bin/env python

## run bbduk to clip off adaptor sequences from illumina RNA-seq data
# note threads requires setting
# note directory of adaptors requires setting

import shutil
import time
import os
import os.path
import sys
import gzip
import subprocess as sp

# directory for adaptor sequences

dirf = '~/bin/bbmap/resources/truseq_rna.fa'

# 

def bbduk():
	# loop over fastq files and remove adaptors
	print('running bbduk...')
	for root, dirs, files in os.walk("./"):
		for filex in files:  
			if filex.endswith('_R1_001.fastq.gz'):
				print(filex)
				# input files
				file_forward = filex # forward read
				file_reverse = filex.replace('_R1_001.fastq.gz','_R2_001.fastq.gz') # reverse read
				# output files
				outfile_forward = filex.replace('_R1_001.fastq.gz','trimmed_R1_001.fastq.gz') # forward read
				outfile_reverse = filex.replace('_R1_001.fastq.gz','trimmed_R2_001.fastq.gz') # reverse read
				# run trimmomatic
				proc = sp.Popen(['bbduk.sh', '-Xmx1g', 'ktrim=r', 'k=23', 'mink=11', 'hdist=1', 'threads=16', 'tpe', 'tbo', 'ref='+dirf, 'in1='+file_forward, 'in2='+file_reverse, 'out1='+outfile_forward, 'out2='+outfile_reverse])
				proc.wait()
				# move files to clipped directory
				#shutil.move(outfile_forward, "./ALL_CLIPPED/")
				#shutil.move(outfile_reverse, "./ALL_CLIPPED/")

# run code
bbduk()

# example code
#bbduk.sh -Xmx1g in1=SS001_R1_001.fastq.gz in2=SS001_R2_001.fastq.gz out1=clean1.fastq.gz out2=clean2.fastq.gz ref=~/bin/bbmap/resources/truseq_rna.fa ktrim=r k=23 mink=11 hdist=1 tpe tbo


