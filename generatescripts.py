import subprocess
import os

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
