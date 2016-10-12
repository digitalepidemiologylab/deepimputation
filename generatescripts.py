import subprocess
import os

if not os.path.isdir("Versions") :
	os.mkdir("Versions")

f = open("changetofloat.py", "r")
temp = f.read()
f.close()

for chrom in range(22) :
	f = open("./Versions/new-job-"+str(chrom)+".py", "w")
	f.write(temp.replace("%%%%%SELECTYOURFAVORITECHROMOSOME%%%%%", str(chrom+1)))
	f.close()
	print(chrom)

subprocess.call("cp params.py ./Versions", shell=True)
subprocess.call("cp usefulfunctions.py ./Versions", shell=True)
