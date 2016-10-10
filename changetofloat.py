import os
import subprocess
import glob
import re
import pandas as pd
import math
from joblib import Parallel, delayed
import time
import subprocess

###########################################################################################
####useful functions
###########################################################################################

####List elements in path, _type can be "files", "dir", "all"; exception can be any file you don't want to add in the list
def list_elements(PATH, _type="files", extension='', VERBOSE=False, sort=True, exception=[]):
	filelist = []
	####List all files
	if _type=="files" or _type=="all" :
		iteratorfiles = 0
		for files in glob.glob(PATH+'*'+extension):
			if os.path.isfile(files) and (files not in exception) :
				iteratorfiles+=1
				filelist.append(files)
				if VERBOSE :
					print("File found at {0} : {1}".format(PATH,files))

		print("Number of{0} files found in {1} : {2}".format(extension, PATH, iteratorfiles))


	####List all directories
	if _type=="dir" or _type=="all" :
		iteratordir = 0
		for files in glob.glob(PATH+'*'+extension):
			if os.path.isdir(files) and (files not in exception) :
				iteratordir+=1
				filelist.append(files)
				if VERBOSE :
					print("File found at {0} : {1}".format(PATH,files))

		print("Number of{0} directories found in {1} : {2}".format(extension, PATH, iteratordir))

	if _type=="all" :
		print("In total {0} elements found in {1}".format(iteratordir+iteratorfiles,PATHINPUT))


	####Naturally sort the files so that the chromosomes are processed in the roght order
	if sort :
		filelist = natural_sort(filelist)

	return filelist

def natural_sort(l): 
	convert = lambda text: int(text) if text.isdigit() else text.lower() 
	alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
	return sorted(l, key = alphanum_key)

def savesamples(PATH, chromosome, dataframe, listenames,i, namedir="/floatfiles/") :

		#### Save 
		dataframe.loc[:, "output"+listenames[0]].to_csv(PATH+namedir+chromosome+"/"+listenames[i]+".txt", index = False, encoding = "utf8")

		####compressing file
		subprocess.call("gzip {}".format(PATH+namedir+chromosome+"/"+listenames[i]+".txt"),shell=True)


def wrightencodeoutput(PATH, chromosome, dataframe, SVE, listenames, namedir="/floatfiles/") :

	for i in range(len(listenames)) :

		#### First allele encoding
		dataframe.loc[((dataframe.REF == "A") & (dataframe.loc[:,listenames[i]].str[0] == "0" )), "output"+listenames[i]] = SVE[0]#### REF
		dataframe.loc[((dataframe.REF == "T") & (dataframe.loc[:,listenames[i]].str[0] == "0" )), "output"+listenames[i]] = SVE[1]
		dataframe.loc[((dataframe.REF == "G") & (dataframe.loc[:,listenames[i]].str[0] == "0" )), "output"+listenames[i]] = SVE[2]
		dataframe.loc[((dataframe.REF == "C") & (dataframe.loc[:,listenames[i]].str[0] == "0" )), "output"+listenames[i]] = SVE[3]
		dataframe.loc[((dataframe.ALT == "A") & (dataframe.loc[:,listenames[i]].str[0] == "1" )), "output"+listenames[i]] = SVE[0]#### ALT
		dataframe.loc[((dataframe.ALT == "T") & (dataframe.loc[:,listenames[i]].str[0] == "1" )), "output"+listenames[i]] = SVE[1]
		dataframe.loc[((dataframe.ALT == "G") & (dataframe.loc[:,listenames[i]].str[0] == "1" )), "output"+listenames[i]] = SVE[2]
		dataframe.loc[((dataframe.ALT == "C") & (dataframe.loc[:,listenames[i]].str[0] == "1" )), "output"+listenames[i]] = SVE[3]


		#### Second allele encoding
		dataframe.loc[((dataframe.REF == "A") & (dataframe.loc[:,listenames[i]].str[-1] == "0" )), "output"+listenames[i]] += SVE[4] #### REF
		dataframe.loc[((dataframe.REF == "T") & (dataframe.loc[:,listenames[i]].str[-1] == "0" )), "output"+listenames[i]] += SVE[5] 
		dataframe.loc[((dataframe.REF == "G") & (dataframe.loc[:,listenames[i]].str[-1] == "0" )), "output"+listenames[i]] += SVE[6] 
		dataframe.loc[((dataframe.REF == "C") & (dataframe.loc[:,listenames[i]].str[-1] == "0" )), "output"+listenames[i]] += SVE[7]
		dataframe.loc[((dataframe.ALT == "A") & (dataframe.loc[:,listenames[i]].str[-1] == "1" )), "output"+listenames[i]] += SVE[4] #### ALT
		dataframe.loc[((dataframe.ALT == "T") & (dataframe.loc[:,listenames[i]].str[-1] == "1" )), "output"+listenames[i]] += SVE[5]
		dataframe.loc[((dataframe.ALT == "G") & (dataframe.loc[:,listenames[i]].str[-1] == "1" )), "output"+listenames[i]] += SVE[6]
		dataframe.loc[((dataframe.ALT == "C") & (dataframe.loc[:,listenames[i]].str[-1] == "1" )), "output"+listenames[i]] += SVE[7]



		#### Add position
		dataframe.loc[:, "output"+listenames[0]] +=  dataframe.POS

	print(dataframe)

	
	Parallel(n_jobs=len(listenames))(delayed(savesamples)(PATH, chromosome, dataframe, listenames, i, namedir="/floatfiles/") for i in range(len(listenames)))




###########################################################################################
####useful variables and constants
###########################################################################################

####Constants
PATHINPUT='./'
VERBOSE=False
FILEBATCHSIZE=2
####Intermediate variables to make the encoding a bit more clear
FBP = int(math.pow(2,28)) #FIRST_ALLELE_BIT_POS
SBP = int(math.pow(2,30)) #SECOND_ALLELE_BIT_POS
NL = {"A":int(0), "T":int(1),"G":int(2), "C":int(3)} #NUCLEOTIDE_LABELS
#SVE= SVE= [NL["A"]*FBP, NL["T"]*FBP, NL["G"]*FBP, NL["C"]*FBP, NL["A"]*FBP+SBP, NL["T"]*FBP+SBP, NL["G"]*FBP+SBP, NL["C"]*FBP+SBP] #SNPSVALUESENCODED --> A-C 1st allele and then A-C 2nd allele
SVE= SVE= [NL["A"]*FBP, NL["T"]*FBP, NL["G"]*FBP, NL["C"]*FBP, (NL["A"]+1)*FBP, (NL["T"]+1)*FBP, (NL["G"]+1)*FBP, (NL["C"]+1)*FBP] #SNPSVALUESENCODED --> A-C 1st allele and then A-C 2nd allele

print(SVE[0])


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

		df[samplename] = pd.read_csv(files)



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

