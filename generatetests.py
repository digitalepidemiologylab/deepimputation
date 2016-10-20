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

numberofjobs = 22
tobetested = []

####Clean
if not os.path.isdir("Tests") :
	os.mkdir("Tests")
else :
	subprocess.call("rm ./Tests/*.py", shell = True)
subprocess.call("rm ./logtestdecode*.log", shell = True)
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

print("Encoded chromosomes to be tested : {}".format(ProcessedChrs))

####Copy template script
f = open("testdecoding.py", "r")
temp = f.read()
f.close()

i = 0
#### Pick a subset of remaining chromosomes and generate scripts for them
while i < min(numberofjobs,len(ProcessedChrs)) :
	pick = random.choice(ProcessedChrs)
	if pick not in tobetested :
		f = open("./Tests/new_test_"+str(pick)+".py", "w")
		f.write(temp.replace("%%%%%SELECTYOURFAVORITECHROMOSOME%%%%%", str(pick)))
		f.close()
		print(pick)
		tobetested.append(pick)
		i += 1


subprocess.call("cp params.py ./Tests", shell=True)
subprocess.call("cp usefulfunctions.py ./Tests", shell=True)
