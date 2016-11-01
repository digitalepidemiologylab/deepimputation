# -*- coding: utf-8 -*-
import math
import os
import random
import subprocess
import time
import datetime

if not os.path.isfile("./params.py"): #### If custom version of params doesn't exist, copy template
	subprocess.call("cp paramstemplate.py params.py", shell=True)
	from params import *
	import usefulfunctions as uf
else:
	from params import *
	import usefulfunctions as uf
################################################################################################################

# ######################################################################################################
# PATHINPUT="../fakedataset/"
# PATHORIGIN = PATHINPUT
# PATHENCODED = PATHINPUT+"/encodeddata/"
# PATHSUBSET = PATHINPUT
# ######################################################################################################

listchromsdirs = uf.list_elements(PATHENCODED, _type = "dir")
listofchroms = [chroms.split("/")[-1] for chroms in listchromsdirs]


if not os.path.isdir(PATHSUBSET+"/Subsets"): ####Create the tree for the repartition of the dataset
	os.mkdir(PATHSUBSET+"/Subsets")
	os.mkdir(PATHSUBSET+"/Subsets/FULL")	
	uf.create_chrom_dirs(PATHSUBSET+"/Subsets/FULL",listofchroms)
	subprocess.call("cp -rf {0} {1}".format(PATHSUBSET+"/Subsets/FULL",
		PATHSUBSET+"/Subsets/10_PERCENT"), shell=True)
	subprocess.call("cp -rf {0} {1}".format(PATHSUBSET+"/Subsets/FULL ",
		PATHSUBSET+"/Subsets/1_PERCENT"), shell=True)
elif not os.path.isdir(PATHSUBSET+"/Subsets/FULL"):
	os.mkdir(PATHSUBSET+"/Subsets/FULL")	
	uf.create_chrom_dirs(PATHSUBSET+"/Subsets/FULL",listofchroms)
	subprocess.call("rm -r {0}/10_PERCENT {0}/1_PERCENT".format(PATHSUBSET+"/Subsets"), shell=True)
	subprocess.call("cp -rf {0} {1}".format(PATHSUBSET+"/Subsets/FULL",PATHSUBSET+"/Subsets/10_PERCENT"), shell=True)
	subprocess.call("cp -rf {0} {1}".format(PATHSUBSET+"/Subsets/FULL ",PATHSUBSET+"/Subsets/1_PERCENT"),shell=True)
else :
	subprocess.call("rm -r {0}/10_PERCENT {0}/1_PERCENT".format(PATHSUBSET+"/Subsets"), shell=True)
	os.mkdir(PATHSUBSET+"/Subsets/10_PERCENT")	
	uf.create_chrom_dirs(PATHSUBSET+"/Subsets/10_PERCENT",listofchroms)
	subprocess.call("cp -rf {0} {1}".format(PATHSUBSET+"/Subsets/10_PERCENT/ ",PATHSUBSET+"/Subsets/1_PERCENT"),shell=True)

#################Reorganise the files
for chroms in listchromsdirs :

	listsamples = uf.list_elements(chroms+"/", extension=".txt.gz")
	totalsamples = len(listsamples)

	for samples in range(int(math.floor(totalsamples*PROPTEST))) :
		pick = random.choice(listsamples)
		if not os.path.isdir(PATHSUBSET+"/Subsets/FULL/Test/"+chroms.split("/")[-1]) :
			os.mkdir(PATHSUBSET+"/Subsets/FULL/Test/"+chroms.split("/")[-1])
		subprocess.call("mv {0} {1}".format(pick, PATHSUBSET+"/Subsets/FULL/Test/"+chroms.split("/")[-1]), shell=True)
		listsamples.remove(pick)

	for samples in range(int(math.floor(totalsamples*PROPVALID))) :
		pick = random.choice(listsamples)
		if not os.path.isdir(PATHSUBSET+"/Subsets/FULL/Valid/"+chroms.split("/")[-1]) :
			os.mkdir(PATHSUBSET+"/Subsets/FULL/Valid/"+chroms.split("/")[-1])
		subprocess.call("mv {0} {1}".format(pick, PATHSUBSET+"/Subsets/FULL/Valid/"+chroms.split("/")[-1]), shell=True)
		listsamples.remove(pick)

	for samples in listsamples:
		if not os.path.isdir(PATHSUBSET+"/Subsets/FULL/Train/"+chroms.split("/")[-1]) :
			os.mkdir(PATHSUBSET+"/Subsets/FULL/Train/"+chroms.split("/")[-1])
		subprocess.call("mv {0} {1}".format(samples, PATHSUBSET+"/Subsets/FULL/Train/"+chroms.split("/")[-1]), shell=True)



#################Cut the files to get training examples of similar size
#################Filter 90% of the positions
subsets = uf.list_elements(PATHSUBSET + "/Subsets/FULL/", _type = "dir")
for sub in subsets :
	for chroms in listofchroms :
		uf.cut_files(uf.list_elements(sub +"/" + chroms + "/", extension=".txt.gz"), SIZEFRAGMENTS, sub +"/" + chroms, copy=False)
	uf.mask_data(sub + "/", 0.1, OUTPUTPATH=PATHSUBSET+"/Subsets/10_PERCENT/"+sub.split("/")[-1])

#################Filter 90% of the positions of the prefiltered dataset
subsets = uf.list_elements(PATHSUBSET + "/Subsets/10_PERCENT/", _type = "dir")
for sub in subsets :
	uf.mask_data(sub + "/", 0.1, OUTPUTPATH=PATHSUBSET+"/Subsets/1_PERCENT/"+sub.split("/")[-1], PREFIXSUB = "/1PER_")
