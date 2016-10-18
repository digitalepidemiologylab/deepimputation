# -*- coding: utf-8 -*-
import os
import subprocess


if not os.path.isfile("./params.py") : #### If custom version of params doesn't exist, copy template
	subprocess.call("cp paramstemplate.py params.py", shell = True)
	from params import *
	from usefulfunctions import *
else:
	from params import *
	from usefulfunctions import *

if not os.path.isdir(PATHSUBSET+"/Subsets"):
	os.mkdir(PATHSUBSET+"/Subsets")
	os.mkdir(PATHSUBSET+"/Subsets/FULL")	
	os.mkdir(PATHSUBSET+"/Subsets/FULL/Train")
	os.mkdir(PATHSUBSET+"/Subsets/FULL/Test")
	os.mkdir(PATHSUBSET+"/Subsets/FULLValid")

	subprocess.call(cp PATHSUBSET+"/Subsets/FULL " PATHSUBSET+"/Subsets/FULL/10_PERCENT")
	subprocess.call(cp PATHSUBSET+"/Subsets/FULL " PATHSUBSET+"/Subsets/FULL/1_PERCENT")


listchroms = list_elements(PATHENCODED, _type = "dir")

for chroms in listchroms :

	listsamples = list_elements(chroms1+"/", extension=".txt.gz")