#!/usr/bin/python

import sys

file2 = sys.argv[1]
file3 = sys.argv[2]

print('input:'+file2)
print('output'+file3)

with open(file2, "r") as infile:
        lines = infile.readlines()

out = []

for line in lines:
    if line.startswith('>'):
        modline = line.split('|', 1)[0]
        modline = modline+'\n'
        out.append(modline)
    else:
        out.append(line)

with open(file3, 'w') as file:
    for outline in out:        
        file.writelines(outline)
