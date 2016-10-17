# -*- coding: utf-8 -*-
import math
import random
import pandas as pd
import time
import datetime

from usefulfunctions import *
from params import *

LOGGING = False
if LOGGING==True :
	old_stdout = sys.stdout
	log_file = open("./logtestdecode{}.log".format(21),"w")
	sys.stdout = log_file

errorsal1 = 0
errorsal2 = 0
listpbal1 = []
listpbal2 = []

_meta = pd.read_csv(PATHINPUT+"/21/_meta.txt.gz", sep = "\t", index_col=False).drop(["#CHROM","ID","QUAL", "FILTER", "INFO", "FORMAT"], 1)

files = list_elements(PATHINPUT+"/encodeddata/21/", extension = ".txt.gz")


for j in range(min(nbfilesmax, len(files))) :

	testfile = random.choice(files)
	name = testfile.split("/")[-1].split(".")[0]


	_meta["originaldata"] = pd.read_csv(PATHINPUT+"/21/"+name +"_"+ name + ".txt.gz", index_col=None, header=None)

	_meta["totest"] = pd.read_csv(testfile,  index_col = None, header = None)

	for i in range(nbtests):
		totest = random.choice(_meta.totest.tolist())
		A1, A2, position = decode_position(totest, LN)
		originalalleles = _meta.loc[(_meta.POS == position), :]["originaldata"].tolist()[0].split("/")
		ref =  _meta.loc[(_meta.POS == position), :]["REF"].tolist()[0]
		alt =  _meta.loc[(_meta.POS == position), :]["ALT"].tolist()[0]

		if (originalalleles[0] == 0) and (A1 != ref) :
			errorsal1 +=1
			listpbal1.append(position)
		if (originalalleles[0] == 1) and (A1 != alt) :
			errorsal1 += 1
			listpbal1.append(position)

		if (originalalleles[-1] == 0) and (A1 != alt) :
			errorsal2 +=1
			listpbal2.append(position)
		if (originalalleles[-1] == 1) and (A1 != alt) :
			errorsal2 +=1
			listpbal2.append(position)

		
		#printProgress(j*nbtests+i,nbtests*min(nbfilesmax, len(files))-1)
		if VERBOSE == True :
			print("{0}/{1} files tested. Date : {2}".format(i, nbtests, str(datetime.datetime.now())))


print("\nAllele 1 errors : {0}\nAllele 2 errors : {1}\ntotal errors : {2}".format(errorsal1, errorsal2, errorsal1+errorsal2))

print("In total : {}% errors !\n".format(100*(errorsal1+errorsal2)/(2*nbtests*min(nbfilesmax, len(files)))))

if LOGGING==True :
	sys.stdout = old_stdout
	log_file.close()

