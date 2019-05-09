#!/usr/bin/env python

import subprocess as sp
import os
from os import path
import optparse

# run fastqc on all reads

# combine the multiplexed .fasta.gz files using cat (need to check which ones are the same sample)

# gz_file_list = []
# for root, dirs, files in os.walk("./"):
# 	for filex in files:   
# 		if filex.endswith('fasta.gz'):
# 			fullpath = os.path.join(root, filex)
# 			gz_file_list.append(fullpath)

# print gz_file_list

def trim():
	print 'Cleaning reads using trimmomatic...'
	for root, dirs, files in os.walk("./"):
		for filex in files:  
			if filex.endswith('.fastq.unconc.gz'): # should be .fastq or .fq, but python seems buggy!
				print filex
				out_file = filex.replace('.fastq.unconc.gz', '_trimmed.fastq.gz')
				proc = sp.Popen(['java', '-jar', 'trimmomatic-0.33.jar', 'SE', '-threads', '15', '-phred33', filex, out_file, 'CROP:26'])
				proc.wait()

# original command
# java -jar trimmomatic-0.33.jar SE -threads 15 -phred33 QMUL2008-44_Lat_ACAGTG_L003_1_001_interleaved2.fastq.unconc.gz QMUL2008-44_Lat_ACAGTG_L003_1_001_interleaved2.fastq.clean.gz ILLUMINACLIP:adaptors:2:30:10 CROP:26

def align():
	print 'Aligning the reads to the genome using bowtie2...'
	for root, dirs, files in os.walk("./"):
		for filex in files:  
			if filex.endswith('_trimmed.fastq.gz'): # should be .fastq or .fq, but python seems buggy!
				print filex
				out_file = filex.replace('_trimmed.fastq.gz', '.sam')
				proc = sp.Popen(['bowtie2', '-p', '15', '--very-sensitive-local', '-x', 'hs_genome', '-U', filex, '-S', out_file])
				proc.wait()

# original command
# bowtie2 -p 15 --very-sensitive-local -x hs_genome -U testclean.fastq.gz -S result.sam &
# command with saving alignment rate
# bowtie2 -p 15 --very-sensitive-local -x hs_genome -U WTCHG_306408_201_1clean.fastq -S result.sam 2> XXXXXX.log &

# count alignments to miRNAs

def count():
	print('Counting alignmets to miRNAs using featurecounts...')
	for root, dirs, files in os.walk("./"):
		for filex in files:  
			if filex.endswith('.sam'): # should be .fastq or .fq, but python seems buggy!
				print filex
				out_file = filex.replace('.sam', '_counts.txt')
				proc = sp.Popen(['featureCounts', '-R', '-F', 'GFF', '-M', '-t', 'miRNA', '-g', 'Name', '-a', 'hsa.gff3', '-o', out_file, filex])
				proc.wait()

# concatonate count files

def concat():
	print('Merging files from counting...')
	# loop to make the file list
	filelist = []
	for root, dirs, files in os.walk("./"):
	    for filex in files:   
	        if filex.endswith('_counts.txt'):
	            #fullpath = os.path.join(root, filex)
	            filelist.append(filex)	            
	# loop to make a count dictionary
	mysamplenames = [] # this contains the column names
	mydict = {} # these contain the feature names and counts
	j = 0 # keep track of which file we are on
	for file in filelist:
	    if file[8]=='-':
	    	print(file)
	    	mysamplenames.append(file.split('_')[0])
	    elif file[8]=='_':
	    	tempsamplename = file
	    	tempsamplename = tempsamplename[:9].replace('_', '-')+tempsamplename[9:]
	    	print(tempsamplename)	    	
	    	mysamplenames.append(tempsamplename.split('_')[0]) 
	    j = j + 1
	    print(j)
	    with open(file) as infile:        
	        if j == 1: # for file 1 (we need to get out the IDs)            
	            i = 1
	            for line in infile:
	                if (i == 1) or (i ==2): # skip the header
	                    i = i + 1
	                    pass
	                else:
	                    tsplit = line.split("\t")            
	                    id = tsplit[0]
	                    mydict[id] = []
	                    mydict[id].append(tsplit[6].strip('\n'))         
	        if j >= 2: # for file 2 we do not need the IDs
	            i = 1
	            for line in infile:
	                if (i == 1) or (i ==2): # skip the header
	                    i = i + 1
	                    pass
	                else:
	                    tsplit = line.split("\t")            
	                    id = tsplit[0]
	                    mydict[id].append(tsplit[6].strip('\n'))
	print(mysamplenames)  	                    
	# loop to write the count file	                    
	outputname = 'miRNAseqcounts.tsv'
	with open(outputname, 'w') as out_file:
	    out_file.write('ID' + "\t" + "\t".join(mysamplenames) + "\n") 
	    for key in mydict:
	        towrite = (key + "\t" + "\t".join(mydict[key]) + "\n")
	        out_file.write(towrite) 

# execute functions here

print('Executing functions...')
#trim()
#align()
#count()
concat()
