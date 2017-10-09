#!/usr/bin/env python
###########################

#Description.

#Import data (of contratos and socias over time) from csv and output json files grouped by municipalities.

###########################

#Define paths and inputs.

idir='../data/input/distribution-summaries/' #Name of input directory where all csv files are (and nothing else).
odir='../data/output/' #Name of output directory.
ofile_contratos='contratos.json' #Name of output file for contratos.
ofile_socias='socias.json' #Name of output file for socias.

###########################

#Import necessary modules.

import os,json
import pandas as pd

###########################

#Make a list of input files.

listfiles=os.listdir(idir)

###########################

#Make dictionaries of contratos and another for socias.

dict_contratos={}
dict_socias={}
for file_i in xrange(len(listfiles)):

	name_info=listfiles[file_i].split('-')
	file_class=name_info[1] #Either "contratos" or "socias".
	date=name_info[2]+'-'+name_info[3]+'-'+name_info[4] #Get the date of the data from the name of the file.

	#if int(name_info[2]+name_info[3]+name_info[4])>=20171101: #Since there seems to be csv files from the future!
	#	continue
	
	data=pd.read_csv(idir+listfiles[file_i],sep=None, header=0, usecols=['codi_ine','quants'], engine='python', dtype={'codi_ine':str,'quants':int})
	codi_ine=data.codi_ine.as_matrix()
	quants=data.quants.as_matrix()

	for i in xrange(len(codi_ine)):

		if codi_ine[i]=='None':

			continue
		
		if file_class=='contratos':
			
			#If an entry exists for that codi_ine, add data from new date, otherwise create key for this new code_ine.

			if codi_ine[i] in dict_contratos.keys():
				dict_contratos[codi_ine[i]][date]=quants[i]
			else:
                                dict_contratos['%s' %codi_ine[i]]={date:quants[i]}

		elif file_class=='socias':

			#Same procedure for socias.

                        if codi_ine[i] in dict_socias.keys():
                                dict_socias[codi_ine[i]][date]=quants[i]
                        else:
                                dict_socias['%s' %codi_ine[i]]={date:quants[i]}

###########################

#Dump data into json files.

with open(odir+ofile_contratos,'w') as f:
	f.write(json.dumps(dict_contratos))
f.close()

with open(odir+ofile_socias,'w') as f:
	f.write(json.dumps(dict_socias))
f.close()

###########################

'''
#Example of the output in json format.
{
  "08019": {
    "2015-01-01": 3295,
    "2015-02-01": 5555
  },
  "08015": {
    "2015-01-01": 164,
    "2015-02-01": 222
  }
}
'''

