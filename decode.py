import math
import random
import pandas as pd

from usefulfunctions import *

PATH = "./"
nbtests = 1000
nbfilesmax = 10


errorsal1 = 0
errorsal2 = 0
listpbal1 = []
listpbal2 = []

_meta = pd.read_csv(PATH+"22/_meta.txt.gz", sep = "\t", index_col=False).drop(["#CHROM","ID","QUAL", "FILTER", "INFO", "FORMAT"], 1)

files = list_elements(PATH+"floatfiles/22/", extension = ".txt.gz")


for testfile in range(min(nbfilesmax, len(files))) :

	testfile = random.choice(files)
	name = testfile.split("/")[-1].split(".")[0]


	_meta["originaldata"] = pd.read_csv(PATH+"/22/"+name +"_"+ name + ".txt.gz", index_col=None, header=None)

	_meta["totest"] = pd.read_csv(testfile,  index_col = None, header = None)

	for i in range(nbtests):
		totest = random.choice(_meta.totest.tolist())
		A1, A2, position = decode_position(totest, LN)

		originalalleles = _meta.loc[(_meta.POS == position), :]["originaldata"].tolist()[0].split("/")
		ref =  _meta.loc[(_meta.POS == position), :]["REF"].tolist()[0]
		alt =  _meta.loc[(_meta.POS == position), :]["ALT"].tolist()[0]

		if (originalalleles[0] == 0) and (A1 != ref) :
			errorsal1 +=1
			listpbal1.append(position)
		if (originalalleles[0] == 1) and (A1 != alt) :
			errorsal1 += 1
			listpbal1.append(position)

		if (originalalleles[-1] == 0) and (A1 != alt) :
			errorsal2 +=1
			listpbal2.append(position)
		if (originalalleles[-1] == 1) and (A1 != alt) :
			errorsal2 +=1
			listpbal2.append(position)


		printProgress(i,nbtests*min(nbfilesmax, len(files)))



print("\nerrors for allele 1 : {0}\nerrors for allele 2 : {1}\ntotal errors : {2}\n".format(errorsal1, errorsal2, errorsal1+errorsal2))

print("\nIn total : {}% errors !".format(100*(errorsal1+errorsal2)/(2*nbtests*min(nbfilesmax, len(files)))))