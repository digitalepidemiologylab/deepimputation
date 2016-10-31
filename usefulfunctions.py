# -*- coding: utf-8 -*-
import datetime
import glob
import gzip
import math
import os
import pandas as pd
import random
import re
import shutil
import subprocess
import sys
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

		if VERBOSE :
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

		if VERBOSE :
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
		dataframe.loc[:, "output"+listenames[i]] +=  dataframe.POS
	
	#### Wright files
	
	if len(listenames) > 1 :
		jobs = []
		for i in range(len(listenames)):
			thread = threading.Thread(target=savesamples(PATH, chromosome, dataframe, listenames, i, namedir="/floatfiles/"))
			jobs.append(thread)
		for j in jobs :
			j.start()
		for j in jobs :
			j.join()
	else:
		savesamples(PATH, chromosome, dataframe, listenames,0, namedir="/floatfiles/")

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

def decode_position(totest, LN) :

	FBP = math.pow(2,28)
	encAL1 = FBP
	encAL2 = math.pow(2,31)
	position = 0
	_iter = 20
	AL1=AL2 = "N"

	while (totest - encAL2 -encAL1 -position != 0) and (encAL1 <= math.pow(2,33) and (encAL2 <= math.pow(2,37))) and (_iter > 0):
		#print(totest -encAL2 -encAL1 -position)
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

def mask_data(_PATH, percentpass, OUTPUTPATH=None, PREFIXSUB = "/10PER_", VERBOSE=False) :
	### percentpass = nb between 0 and 1

	print("Starting to filter data from {0} at {1}. ({2} pass)".format(_PATH,datetime.datetime.now(),percentpass))

	if OUTPUTPATH==None :
		OUTPUTPATH = _PATH
	if not LOGGING:
		i = 0
	chromosomes = list_elements(_PATH, _type='dir', exception = [_PATH+"/floatfiles", _PATH + "floatfiles", _PATH + "/encodeddata", _PATH + "encodeddata", _PATH + "/Subsets", _PATH + "Subsets"])

	for chrom in chromosomes :

		chromname = chrom.split("/")[-1].split("_")[-1]
		files = list_elements(chrom +"/", extension='.txt.gz')

		for sample in files :
			
			namesample = sample.split("/")[-1].split(".")[0].split("_")[-1]
			nblines = getnblines(sample)
			subsetoflines = random.sample(range(nblines), math.floor(nblines*percentpass))

			with gzip.open(sample, "rt", encoding='utf-8') as infile, open(OUTPUTPATH+"/"+chromname+"/"+PREFIXSUB+namesample+".txt", "w") as outfile:
				lines = infile.readlines()

				for index in subsetoflines :
					outfile.write(lines[index])
			subprocess.call("gzip {}".format(OUTPUTPATH+"/"+chromname+"/"+PREFIXSUB+namesample+".txt"),shell=True)

			if not LOGGING :
				i +=1
				printProgress(i,len(chromosomes)*len(files)-1, decimals = 3)
			elif VERBOSE == True :
				print("{0}/{1} files tested. Date : {2}".format(i, len(chromosomes*len(files)), str(datetime.datetime.now())))
	print("\nData from {0} filtered at {1}. ({2} pass)".format(_PATH,datetime.datetime.now(),percentpass))

def getnblines(infile) :
	with gzip.open(infile, "rt") as f:
	    for i, l in enumerate(f):
	        pass
	return i+1

def createchromdeirs(_PATH, listofchroms):
	os.mkdir(_PATH+"/Train")
	os.mkdir(_PATH+"/Test")
	os.mkdir(_PATH+"/Valid")
	for chroms in listofchroms:
		os.mkdir(_PATH+"/Train/"+chroms)
		os.mkdir(_PATH+"/Test/"+chroms)
		os.mkdir(_PATH+"/Valid/"+chroms)

def cutfiles(filelist, sizeofoutputfiles, OUTPUTPATH, copy=True) :

	for file in filelist :
		filename = file.split("/")[-1].split(".")[0]
		nblines = getnblines(file)
		nboffiles = math.ceil(nblines/sizeofoutputfiles)
		overlapping = math.floor((sizeofoutputfiles-nblines%sizeofoutputfiles)/nboffiles)
		
		begin = 0
		for i in range(int(nboffiles)) :
			end = int(min(begin + sizeofoutputfiles, nblines))
			if end - begin < sizeofoutputfiles :
				begin = int(end - sizeofoutputfiles)
			subsetoflines= range(begin, end)
			begin += int(sizeofoutputfiles - overlapping)
				
			with open(OUTPUTPATH+"/"+filename+"-"+str(i+1)+".txt", "w") as outfile, gzip.open(file, "rt") as infile :
				lines = infile.readlines()
				for index in subsetoflines :
					outfile.write(lines[index])
			subprocess.call("gzip {}".format(OUTPUTPATH+"/"+filename+"-"+str(i+1)+".txt"),shell=True)

		if not copy :
			subprocess.call("rm {}".format(file), shell=True)
