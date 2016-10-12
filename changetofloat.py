# -*- coding: utf-8 -*-
import os
import pandas as pd
import math
from joblib import Parallel, delayed
import time

from usefulfunctions import *
from params import *

###########################################################################################
####useful variables
###########################################################################################
listdir = []
listfiles = []
CHROMTOBEPROCESSED = %%%%%SELECTYOURFAVORITECHROMOSOME%%%%% ####value replaced py the script generate scripts
###########################################################################################
####It actually starts here
###########################################################################################

#if (PATHINPUT[0] == "/") and (len(PATHINPUT)<=1):
#	print("Wrong path to data, be careful...")
#	quit()
#else:
#	os.system("rm -rf {}/floatfiles/*".format(PATHINPUT))


listdir = [PATHINPUT+"/"+str(CHROMTOBEPROCESSED)] #list_elements(PATHINPUT+"/", _type="dir", VERBOSE=True, exception=[PATHINPUT+"floatfiles", PATHINPUT+"/floatfiles", PATHINPUT+"__pycache__", PATHINPUT+"ec2-user@ec2-54-93-98-88.eu-central-1.compute.amazonaws.com"])


if not os.path.isdir(PATHINPUT+"/floatfiles") :
	os.mkdir(PATHINPUT+"/floatfiles")

timepoints = [time.time()]

for dirs in listdir:

	print("Processing {}".format(dirs))	


	chromosome = dirs.split("/")[-1]

	if not os.path.isdir(PATHINPUT+"/floatfiles/"+chromosome) :
		os.mkdir(PATHINPUT+"/floatfiles/"+chromosome)


	####load the meta data in a pandas data frame
	_meta = pd.read_csv(dirs+"/_meta.txt.gz", sep ="\t",index_col=False)


	listfiles = list_elements(dirs+"/", extension=".txt.gz", exception=[dirs+"/_meta.txt.gz", dirs+"_meta.txt.gz", dirs+"/_comments.txt.gz", dirs+"_comments.txt.gz"])
	nbprocessedfiles = 0

	batchiter = 0
	liste=[]
	jobs=[]
	df = _meta.drop(["#CHROM","ID","QUAL", "FILTER", "INFO", "FORMAT"], 1)


	for files in listfiles :

		samplename = files.split("_")[0].split("/")[-1]
		liste.append(samplename)

		df[samplename] = pd.read_csv(files, index_col=None, header=None)



		if (batchiter < FILEBATCHSIZE-1) and (files is not listfiles[-1]):
			batchiter += 1
		else :
			####Reinitialize stuff
			wrightencodeoutput(PATHINPUT, chromosome , df, SVE, liste)
			batchiter = 0
			liste = []
			jobs=[]
			df = _meta.drop(["#CHROM","ID","QUAL", "FILTER", "INFO", "FORMAT"], 1)
			nbprocessedfiles += FILEBATCHSIZE

			m, s = divmod(time.time()-timepoints[-1], 60)
			h, m = divmod(m, 60)
			print("{0}/{1} files processed after {2}h{3}m{4}s".format(nbprocessedfiles, len(listfiles),math.floor(h),math.floor(m),math.floor(s)))

	timepoints.append(time.time())
	print("Processing {0} finished after {1} ".format(dirs, timepoints[-1]-timepoints[-2]))

