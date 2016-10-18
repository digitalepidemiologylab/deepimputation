# -*- coding: utf-8 -*-
import math
import random
import pandas as pd
import time
import datetime
import subprocess
import os

if not os.path.isfile("./params.py") : #### If custom version of params doesn't exist, copy template
	subprocess.call("cp paramstemplate.py params.py", shell = True)
	from params import *
	from usefulfunctions import *
else :
	from params import *
	from usefulfunctions import *

#####################################################################################################
CHROMTOBETESTED = str(2)#%%%%%SELECTYOURFAVORITECHROMOSOME%%%%% ####value replaced py the script generate scripts
#####################################################################################################

PATHENCODED = "../fakedataset/floatfiles/"
PATHORIGIN = "../fakedataset/"

if LOGGING==True :
	old_stdout = sys.stdout
	log_file = open("./logtestdecode{}.log".format(CHROMTOBETESTED),"w")
	sys.stdout = log_file

print("Program started at {}".format(str(datetime.datetime.now())))

errors = pd.DataFrame(columns = ["File", "Supposed_position", "Error_type", "Previous_positions", "Next_position"])

_meta = pd.read_csv(PATHORIGIN+"/"+CHROMTOBETESTED+"/_meta.txt.gz", sep = "\t", index_col=False).drop(["#CHROM","ID","QUAL", "FILTER", "INFO", "FORMAT"], 1)

files = list_elements(PATHENCODED + CHROMTOBETESTED + "/", extension = ".txt.gz")


for j in range(min(nbfilesmax, len(files))) :
	random.seed()
	testfile = random.choice(files)
	name = testfile.split("/")[-1].split(".")[0]


	_meta["originaldata"] = pd.read_csv(PATHORIGIN+"/"+CHROMTOBETESTED+"/"+name +"_"+ name + ".txt.gz", index_col=None, header=None)

	_meta["totest"] = pd.read_csv(testfile,  index_col = None, header = None)

	for i in range(nbtests):
		totest = random.choice(_meta.totest.tolist())
		A1, A2, position = decode_position(totest, LN)

		if position == -1 :
			index = error.loc[(error.totest == totest),:].index.tolist()
			errors.loc[errors.shape[0], :] = [testfile, position, "Impossible to decode", _meta.iloc[index-1, 0], _meta.iloc[index+1, 0]]

		originalalleles = _meta.loc[(_meta.totest == totest), :]["originaldata"].tolist()[0].split("/")
		originalpos = _meta.loc[(_meta.totest == totest), :]["POS"].tolist()[0]
		ref =  _meta.loc[(_meta.totest == totest), :]["REF"].tolist()[0]
		alt =  _meta.loc[(_meta.totest == totest), :]["ALT"].tolist()[0]

		if position != originalpos:
			index = error.loc[(error.totest == totest),:].index.tolist()[0]
			errors.loc[errors.shape[0], :] = [testfile, position, "Position", _meta.iloc[index-1, 0], _meta.iloc[index+1, 0]]

		if ((originalalleles[0] == 0) and (A1 != ref)) or ((originalalleles[0] == 1) and (A1 != alt)) :
			index = error.loc[(error.totest == totest),:].index.tolist()[0]
			errors.loc[errors.shape[0], :] = [testfile, position, "Allele 1", _meta.iloc[index-1, 0], _meta.iloc[index+1, 0]]

		if ((originalalleles[-1] == 0) and (A1 != alt)) or ((originalalleles[-1] == 1) and (A1 != alt)) :
			index = error.loc[(error.totest == totest),:].index.tolist()[0]
			errors.loc[errors.shape[0], :] = [testfile, position, "Allele 2", _meta.iloc[index-1, 0], _meta.iloc[index+1, 0]]

		if not LOGGING :
			printProgress(j*nbtests+i,nbtests*min(nbfilesmax, len(files))-1, decimals = 3)
		if VERBOSE == True :
			print("{0}/{1} files tested. Date : {2}".format(i, nbtests, str(datetime.datetime.now())))


errorsal1 = errors.loc[(errors.Error_type == "Allele 1"),:].shape[0]
errorsal2 = errors.loc[(errors.Error_type == "Allele 2"),:].shape[0]
errorspos = errors.loc[(errors.Error_type == "Position"),:].shape[0]
Impossibletodecode = errors.loc[(errors.Error_type == "Impossible to decode"),:].shape[0]
totalerror = errors.shape[0]

print("\nAllele 1 errors : {0}\nAllele 2 errors : {1}\nPosition errors : {2}\nImpossible to decode : {3}\nTotal errors : {4}".format(errorsal1, errorsal2, errorspos, Impossibletodecode, totalerror))
print("In total : {}% errors !\n".format(100*(totalerror)/(nbtests*min(nbfilesmax, len(files)))))
print("Date : {}".format(str(datetime.datetime.now())))

if not errors.empty :
	errors.to_csv("Errorsfound.csv", sep = "\t")

if LOGGING==True :
	sys.stdout = old_stdout
	log_file.close()

