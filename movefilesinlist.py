#!/usr/bin/python

import os
import shutil

# load ids to exchange with current ids

filelist = open('filelist.txt', 'r')

myfiles = []
for line in filelist:
	myfiles.append(line.strip('\n'))

cwd = os.getcwd()
destdir = cwd+'/mydir'

for filex in myfiles:
	pass
	filepath = cwd+'/'+filex
	shutil.move(filepath, destdir)
