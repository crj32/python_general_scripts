#!/usr/bin/python

# usage: comparechecksums.py original_checksums new_checksums

import sys

file1 = sys.argv[1] # original checksums in column 1 of tsv
file2 = sys.argv[2] # new checksums in column 1 of tsv

print('infile1'+':'+file1)
print('infile2'+':'+file2)

# get the checksums

file1checksums = open(file1, 'r') # with open is a bit tidier?
file2checksums = open(file2, 'r')

file1_list = []
file2_list = []

# for file 1
for line in file1checksums:
	v1, v2 = line.split('\t')
	file1_list.append(v1) # add the ith row checksum

print(file1_list)

# for file 2
for line in file2checksums:
	v1, v2 = line.split('\t')
	file2_list.append(v1) # add the ith row checksum

print(file2_list)

# print lengths of lists

print('length infile1'+':',len(file1_list))
print('length infile1'+':',len(file2_list))

# test if equal and print results

if file1_list == file2_list:
	print('checksums identical')
else:
	print('checksums non-identical')
	for element in file1_list:
		if element not in file2_list:
			print('missing elements')
			print(element)


