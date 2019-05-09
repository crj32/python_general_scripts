#!/usr/bin/python

import os

os.chdir("/home/christopher/Desktop/testtemp")
filelist = open('temp.txt', 'r')

# add file names to swap to a dictionary
myfiledict = {}
for line in filelist:
    original = line.split('\t')[0]
    print(original)
    replacement = line.split('\t')[1]
    print(replacement)
    myfiledict[original] = replacement

# get file names in current directory

x = []
for mydir, subdirs, files in os.walk("."):
    mydir = mydir.strip('./')
    if mydir in myfiledict.keys():
        print(mydir)
        print('we have a match')     
        # rename directory to new value from dictionary
        name = myfiledict[mydir].strip('\n')
        os.rename(mydir,name)
    

    