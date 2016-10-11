import os
import pandas as pd
import math
from joblib import Parallel, delayed
import time

from usefulfunctions import *

###########################################################################################
####useful variables and constants
###########################################################################################

####Constants
PATHINPUT='./'
VERBOSE=False
FILEBATCHSIZE=2
####Intermediate variables to make the encoding a bit more clear
FBP = int(math.pow(2,28)) #FIRST_ALLELE_BIT_POS
NL = {"A":int(1), "T":int(2),"G":int(4), "C":int(8)} #NUCLEOTIDE_LABELS
#SVE= SVE= [NL["A"]*FBP, NL["T"]*FBP, NL["G"]*FBP, NL["C"]*FBP, NL["A"]*FBP+SBP, NL["T"]*FBP+SBP, NL["G"]*FBP+SBP, NL["C"]*FBP+SBP] #SNPSVALUESENCODED --> A-C 1st allele and then A-C 2nd allele
SVE= [NL["A"]*FBP, NL["T"]*FBP, NL["G"]*FBP, NL["C"]*FBP, (NL["A"])*FBP*16, (NL["T"])*FBP*16, (NL["G"])*FBP*16, (NL["C"])*FBP*16] #SNPSVALUESENCODED --> A-C 1st allele and then A-C 2nd allele

####Variables
listdir = []
listfiles = []


###########################################################################################
####It actually starts here
###########################################################################################

if (PATHINPUT[0] == "/") and (len(PATHINPUT)<=1):
	print("Wrong path to data, be careful...")
	quit()
else:
	os.system("rm -rf {}/floatfiles/*".format(PATHINPUT))


listdir = list_elements(PATHINPUT+"/", _type="dir", VERBOSE=True, exception=[PATHINPUT+"floatfiles", PATHINPUT+"/floatfiles"])

print(listdir)

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

