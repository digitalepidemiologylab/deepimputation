import os
import subprocess
import glob
import re
import pandas as pd

###########################################################################################
####useful functions
###########################################################################################

####List elements in path, _type can be "files", "dir", "all"
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
		print("In total {0} elements found in {1}".format(iteratordir+iteratorfiles,PATH))


	####Naturally sort the files so that the chromosomes are processed in the roght order
	if sort :
		filelist = natural_sort(filelist)

	return filelist

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)


###########################################################################################
####useful variables
###########################################################################################


PATHINPUT='./'
VERBOSE=False
listdir = []
listfiles = []

###########################################################################################
####It actually starts here
###########################################################################################

listdir = list_elements(PATHINPUT+"/", _type="dir", VERBOSE=True, exception=[PATHINPUT+"floatfiles", PATHINPUT+"/floatfiles"])

print(listdir)

if not os.path.isdir(PATHINPUT+"/floatfiles") :
	os.mkdir(PATHINPUT+"/floatfiles")


for dirs in listdir:


	print("Processing {}".format(dirs))
	_meta = pd.read_csv(dirs+"/_meta.txt.gz", sep ="\t")
	listfiles = list_elements(dirs+"/", extension=".txt.gz", exception=[dirs+"/_meta.txt.gz", dirs+"_meta.txt.gz", dirs+"/_comments.txt.gz", dirs+"_comments.txt.gz"])


