# -*- coding: utf-8 -*-

import numpy

## first read in file with gene symbols

ref_dict = {}

print('making dictionary from reference annotation...')
with open('gencode.v29.annotation.gtf') as ref_gtf:  
    for line in ref_gtf:
        if line.startswith('#'):
            pass
        else:
            temp = line.split('\t')
            ## if this is a gene, store name and co-ordinates in dictionary
            if temp[2] == 'gene':
                ## split the last entry by ; to get the gene_name
                last = temp[len(temp)-1]
                gene = last.split(';')[2]
                gene = gene.split('"')[1]
                ref_dict[gene] = [temp[0],temp[3],temp[4]]

## second read in file that requires gene symbols
                
f = open("mod.gtf","w+") # output file

print('opening new annotation and modifying...')
i = 1
with open('assembled_transcripts.gtf') as strawberry_gtf:  
    for line in strawberry_gtf:
        if line.startswith('#'):
            f.write(line)
            pass
        else:
            #print(i)
            temp = line.split('\t')
            ## remove extra stuff in each line            
            last = temp[len(temp)-1]
            last = last.split(';')
            last = last[:2]
            temp[len(temp)-1] = '; '.join(last)+';'          
            ## add gene_name to temp
            for key, value in ref_dict.items():
                # if the chromosome is a match
                if temp[0] == value[0]:
                    midpoint = numpy.mean([int(temp[3]),int(temp[4])])
                    # the chromosome matches
                    # check the co-ordinates for a match
                    if int(value[1]) <= midpoint <= int(value[2]):
                        # temp is our line of .gtf to be modified
                        # we have a chromosome match and a co-ordinate match
                        temp[8] = temp[8]+' gene_name '+'"'+key+'";' # add the gene name to the line
                        temp = '\t'.join(temp)+'\n' # remake a tab seperated line to write
                        f.write(temp)
f.close() 