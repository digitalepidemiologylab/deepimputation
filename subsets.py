# -*- coding: utf-8 -*-
import os
import subprocess
import random
import math

if not os.path.isfile("./params.py") : #### If custom version of params doesn't exist, copy template
	subprocess.call("cp paramstemplate.py params.py", shell = True)
	from params import *
	from usefulfunctions import *
else:
	from params import *
	from usefulfunctions import *
################################################################################################################

######################################################################################################
PATHINPUT="../fakedataset/"
PATHORIGIN = PATHINPUT
PATHENCODED = PATHINPUT+"/encodeddata/"
PATHSUBSET = PATHINPUT
######################################################################################################

if not os.path.isdir(PATHSUBSET+"/Subsets"): ####Create the tree for the repartition of the dataset
	os.mkdir(PATHSUBSET+"/Subsets")
	os.mkdir(PATHSUBSET+"/Subsets/FULL")	
	os.mkdir(PATHSUBSET+"/Subsets/FULL/Train")
	os.mkdir(PATHSUBSET+"/Subsets/FULL/Test")
	os.mkdir(PATHSUBSET+"/Subsets/FULL/Valid")
	subprocess.call("cp -rf {0} {1}".format(PATHSUBSET+"/Subsets/FULL",PATHSUBSET+"/Subsets/10_PERCENT"), shell=True)
	subprocess.call("cp -rf {0} {1}".format(PATHSUBSET+"/Subsets/FULL ",PATHSUBSET+"/Subsets/1_PERCENT"), shell=True)
elif not os.path.isdir(PATHSUBSET+"/Subsets/FULL"):
	os.mkdir(PATHSUBSET+"/Subsets/FULL")	
	os.mkdir(PATHSUBSET+"/Subsets/FULL/Train")
	os.mkdir(PATHSUBSET+"/Subsets/FULL/Test")
	os.mkdir(PATHSUBSET+"/Subsets/FULL/Valid")
	subprocess.call("rm -r {0}/10_PERCENT {0}/1_PERCENT".format(PATHSUBSET+"/Subsets"), shell=True)
	subprocess.call("cp -rf {0} {1}".format(PATHSUBSET+"/Subsets/FULL",PATHSUBSET+"/Subsets/10_PERCENT"), shell=True)
	subprocess.call("cp -rf {0} {1}".format(PATHSUBSET+"/Subsets/FULL ",PATHSUBSET+"/Subsets/1_PERCENT"),shell=True)
else :
	subprocess.call("rm -r {0}/10_PERCENT {0}/1_PERCENT".format(PATHSUBSET+"/Subsets"), shell=True)
	os.mkdir(PATHSUBSET+"/Subsets/10_PERCENT")	
	os.mkdir(PATHSUBSET+"/Subsets/10_PERCENT/Train")
	os.mkdir(PATHSUBSET+"/Subsets/10_PERCENT/Test")
	os.mkdir(PATHSUBSET+"/Subsets/10_PERCENT/Valid")
	subprocess.call("cp -rf {0} {1}".format(PATHSUBSET+"/Subsets/10_PERCENT/ ",PATHSUBSET+"/Subsets/1_PERCENT"),shell=True)

#################Reorganise the files
listchroms = list_elements(PATHENCODED, _type = "dir")
for chroms in listchroms :

	listsamples = list_elements(chroms+"/", extension=".txt.gz")
	totalsamples = len(listsamples)

	for samples in range(math.floor(totalsamples*PROPTEST)) :
		pick = random.choice(listsamples)
		print("mv {0} {1}".format(pick, PATHSUBSET+"/Subsets/FULL/Test"+chroms.split("/")[-1]))
		if not os.path.isdir(PATHSUBSET+"/Subsets/FULL/Test/"+chroms.split("/")[-1]) :
			os.mkdir(PATHSUBSET+"/Subsets/FULL/Test/"+chroms.split("/")[-1])
		subprocess.call("mv {0} {1}".format(pick, PATHSUBSET+"/Subsets/FULL/Test/"+chroms.split("/")[-1]), shell=True)
		listsamples.remove(pick)

	for samples in range(math.floor(totalsamples*PROPVALID)) :
		pick = random.choice(listsamples)
		if not os.path.isdir(PATHSUBSET+"/Subsets/FULL/Valid/"+chroms.split("/")[-1]) :
			os.mkdir(PATHSUBSET+"/Subsets/FULL/Valid/"+chroms.split("/")[-1])
		subprocess.call("mv {0} {1}".format(pick, PATHSUBSET+"/Subsets/FULL/Valid/"+chroms.split("/")[-1]), shell=True)
		listsamples.remove(pick)

	for samples in range(len(listsamples)):
		if not os.path.isdir(PATHSUBSET+"/Subsets/FULL/Train/"+chroms.split("/")[-1]) :
			os.mkdir(PATHSUBSET+"/Subsets/FULL/Train/"+chroms.split("/")[-1])
		subprocess.call("mv {0} {1}".format(samples, PATHSUBSET+"/Subsets/FULL/Train/"+chroms.split("/")[-1]), shell=True)