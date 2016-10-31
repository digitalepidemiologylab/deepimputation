# -*- coding: utf-8 -*-
import os
import pandas as pd
import math
import time
import datetime

import usefulfunctions as uf
from params import *

if __name__ == "__main__" :

	###########################################################################################
	####useful variables
	###########################################################################################
	listdir = []
	listfiles = []
	CHROMTOBEPROCESSED = %%%%%SELECTYOURFAVORITECHROMOSOME%%%%% ####value replaced py the script generate scripts
	###########################################################################################
	####It actually starts here
	###########################################################################################


	#### Change output to log files
	if LOGGING == True:
		old_stdout = sys.stdout
		log_file = open("./log{}.log".format(CHROMTOBEPROCESSED),"w")
		sys.stdout = log_file
	
	timepoints = [time.time()]
	print("Program started at {}".format(str(datetime.datetime.now())))


	dirs = PATHINPUT+"/"+str(CHROMTOBEPROCESSED)
	if not os.path.isdir(PATHINPUT+"/floatfiles") :
		os.mkdir(PATHINPUT+"/floatfiles")
	print("Processing {}".format(dirs))	

	chromosome = str(CHROMTOBEPROCESSED)
	if not os.path.isdir(PATHINPUT+"/floatfiles/"+chromosome) :
		os.mkdir(PATHINPUT+"/floatfiles/"+chromosome)


	####load the meta data in a pandas data frame
	_meta = pd.read_csv(dirs+"/_meta.txt.gz", sep ="\t",index_col=False)

	listfiles = uf.list_elements(dirs+"/", extension=".txt.gz", exception=[dirs+"/_meta.txt.gz", dirs+"_meta.txt.gz", dirs+"/_comments.txt.gz", dirs+"_comments.txt.gz"])
	nbprocessedfiles = 0

	batchiter = 0
	liste=[]
	jobs=[]
	df = _meta.drop(["#CHROM","ID","QUAL", "FILTER", "INFO", "FORMAT"], 1)

	for files in listfiles :

		samplename = files.split("/")[-1].split(".")[0].split("_")[-1]
		liste.append(samplename)

		df[samplename] = pd.read_csv(files, index_col=None, header=None)


		if (batchiter < FILEBATCHSIZE-1) and (files is not listfiles[-1]):
			batchiter += 1
		else :
			####Reinitialize stuff
			uf.write_encoded_output(PATHINPUT, chromosome , df, SVE, liste)
			batchiter = 0
			liste = []
			jobs=[]
			df = _meta.drop(["#CHROM","ID","QUAL", "FILTER", "INFO", "FORMAT"], 1)
			nbprocessedfiles += FILEBATCHSIZE

			m, s = divmod(time.time()-timepoints[-1], 60)
			h, m = divmod(m, 60)
			print("{0}/{1} files processed after {2}h{3}m{4}s. Date : {5}".format(nbprocessedfiles, len(listfiles),math.floor(h),math.floor(m),math.floor(s),str(datetime.datetime.now())))

	timepoints.append(time.time())
	m, s = divmod(time.time()-timepoints[0], 60)
	h, m = divmod(m, 60)
	print("Processing {0} finished after {1}h{2}m{3}s. Date : {4}".format(dirs, math.floor(h),math.floor(m),math.floor(s), str(datetime.datetime.now())))

	if LOGGING == True:
		sys.stdout = old_stdout
		log_file.close()
		if not os.path.isdir("./LOGS"):
			subprocess.call("mkdir ./LOGS", shell = True)
			subprocess.call("mv ./log{}.log ./LOGS/".format(CHROMTOBEPROCESSED), shell = True)
