import subprocess
import os
from usefulfunctions import *

if not os.path.isdir("./LOGS") :
	os.mkdir("./LOGS")
	RemainingChrs = [i+ 1 for i in range(22)]
else :
	ProcessedChrs = list_elements("./LOGS/", extension=".log")
	for i in range(len(ProcessedChrs)) :
		ProcessedChrs[i] = ProcessedChrs[i].split("/")[-1]
	RemainingChrs  = [i if i not in ProcessedChrs else None for i in range(1,23)]

print(ProcessedChrs)
print(RemainingChrs)

if not os.path.isdir("Versions") :
	os.mkdir("Versions")
	
f = open("changetofloat.py", "r")
temp = f.read()
f.close()

for chrom in range(10, 19) :
	f = open("./Versions/new-job-"+str(chrom+1)+".py", "w")
	f.write(temp.replace("%%%%%SELECTYOURFAVORITECHROMOSOME%%%%%", str(chrom+1)))
	f.close()
	print(chrom+1)

subprocess.call("cp params.py ./Versions", shell=True)
subprocess.call("cp usefulfunctions.py ./Versions", shell=True)
