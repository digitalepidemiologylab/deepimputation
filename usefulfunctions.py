# -*- coding: utf-8 -*-
import re
import pandas as pd
import sys
import subprocess
import os
import math
import glob
import threading
import time
from params import *

##########################################################################################################################
####////////////////////////////////////////////////////FUNCTIONS\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\####


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

def writeencodeoutput(PATH, chromosome, dataframe, SVE, listenames, namedir="/floatfiles/") :

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
	
	#### Wright files
	
	jobs = []
	for i in range(len(listenames)):
		thread = threading.Thread(target=savesamples(PATH, chromosome, dataframe, listenames, i, namedir="/floatfiles/"))
		jobs.append(thread)
	for j in jobs :
		j.start()
	for j in jobs :
		j.join()

def printProgress(iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
	"""
	Call in a loop to create terminal progress bar
	@params:
	    iteration   - Required  : current iteration (Int)
	    total       - Required  : total iterations (Int)
	    prefix      - Optional  : prefix string (Str)
	    suffix      - Optional  : suffix string (Str)
	    decimals    - Optional  : positive number of decimals in percent complete (Int)
	    barLength   - Optional  : character length of bar (Int)
	"""
	formatStr       = "{0:." + str(decimals) + "f}"
	percents        = formatStr.format(100 * (iteration / float(total)))
	filledLength    = int(round(barLength * iteration / float(total)))
	bar             = '█' * filledLength + '-' * (barLength - filledLength)
	sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
	if iteration == total:
	    sys.stdout.write('\n')
	sys.stdout.flush()



def  decode_position(totest, LN) :

	FBP = math.pow(2,28)
	encAL1 = FBP
	encAL2 = math.pow(2,31)
	position = 0
	_iter = 20
	AL1=AL2 = "N"


	while (totest - encAL2 -encAL1 -position != 0) and (encAL1 <= math.pow(2,33) and (encAL2 <= math.pow(2,37))) and (_iter > 0):

#		print(totest -encAL2 -encAL1 -position)
		if (encAL2*2 < totest) and (encAL1 == math.pow(2,28)) and (position == 0):
			encAL2 *= 2
			AL2 = LN[encAL2]
		elif (encAL1*2 + encAL2 < totest) and (position == 0):
			encAL1 *= 2
			AL1 = LN[encAL1]
		elif totest -encAL1 -encAL2 < FBP:
			position = int(totest - encAL1 -encAL2)
		_iter -=1

	if _iter <= 0 :
		position = -1
	return AL1[0], AL2[0], position

