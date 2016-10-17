import subprocess
import os
from usefulfunctions import *
import random

numberofjobs = 4
tobeprocessed = []


####Clean
if not os.path.isdir("Versions") :
	os.mkdir("Versions")
else :
	subprocess.call("rm ./Versions/*.py", shell = True)

#### Verify which chroms where not already processed and find a subset to work with
if not os.path.isdir("./LOGS") :
	os.mkdir("./LOGS")
	RemainingChrs = [i+ 1 for i in range(22)]
else :
	ProcessedChrs = list_elements("./LOGS/", extension=".log")
	for i in range(len(ProcessedChrs)) :
		ProcessedChrs[i] = int(ProcessedChrs[i].replace("./LOGS/log", "").replace(".log", ""))
	RemainingChrs  = [i for i in range(1,23) if i not in ProcessedChrs ]



for i in range(min(numberofjobs, len(RemainingChrs))) :
	
	pick = random.choice(RemainingChrs)
	if pick in tobeprocessed :
		i -= 1
	else :
		tobeprocessed.append(pick)

	
f = open("changetofloat.py", "r")
temp = f.read()
f.close()

for chrom in tobeprocessed :
	f = open("./Versions/new-job-"+str(chrom+1)+".py", "w")
	f.write(temp.replace("%%%%%SELECTYOURFAVORITECHROMOSOME%%%%%", str(chrom+1)))
	f.close()
	print(chrom+1)

subprocess.call("cp params.py ./Versions", shell=True)
subprocess.call("cp usefulfunctions.py ./Versions", shell=True)
