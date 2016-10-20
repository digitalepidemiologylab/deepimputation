import subprocess
import os
import random
import time

if not os.path.isfile("./params.py") : #### If custom version of params doesn't exist, copy template
	subprocess.call("cp paramstemplate.py params.py", shell = True)
	from params import *
	from usefulfunctions import *
else:
	from params import *
	from usefulfunctions import *	

numberofjobs = 11
tobeprocessed = []

####Clean
if not os.path.isdir("Versions") :
	os.mkdir("Versions")
else :
	subprocess.call("rm ./Versions/*.py", shell = True)
subprocess.call("rm ./*log*.log", shell = True)
subprocess.call("rm ./nohup.out", shell = True)

#### Verify which chroms where not already processed
Filesinpath = list_elements(PATHINPUT, _type="dir", exception=[PATHINPUT+"encodeddata", PATHINPUT+"floatfiles"])
print(Filesinpath)
for i in range(len(Filesinpath)) :
	Filesinpath[i] = int(Filesinpath[i].replace(PATHINPUT, ""))

if not os.path.isdir(PATHINPUT+"/encodeddata/") :
	os.mkdir(PATHINPUT+"/encodeddata/")
	RemainingChrs = Filesinpath
else :
	ProcessedChrs = list_elements(PATHINPUT+"/encodeddata/",_type="dir")
	for i in range(len(ProcessedChrs)) :
		ProcessedChrs[i] = int(ProcessedChrs[i].replace(PATHINPUT+"/encodeddata/", ""))
	RemainingChrs  = [i for i in Filesinpath if i not in ProcessedChrs ]

print("Remaing chromosomes to be encoded : {}".format(RemainingChrs))

####Copy template script
f = open("changetofloat.py", "r")
temp = f.read()
f.close()

i = 0
#### Pick a subset of remaining chromosomes and generate scripts for them
while i < min(numberofjobs,len(RemainingChrs)) :
	pick = random.choice(RemainingChrs)
	if pick not in tobeprocessed :
		f = open("./Versions/new_job_"+str(pick)+".py", "w")
		f.write(temp.replace("%%%%%SELECTYOURFAVORITECHROMOSOME%%%%%", str(pick)))
		f.close()
		print(pick)
		tobeprocessed.append(pick)
		i += 1


subprocess.call("cp params.py ./Versions", shell=True)
subprocess.call("cp usefulfunctions.py ./Versions", shell=True)
