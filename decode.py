import math
import random
import pandas as pd

from usefulfunctions import *


_meta = pd.read_csv("./22/_meta.txt.gz", sep = "\t", index_col=False).drop(["#CHROM","ID","QUAL", "FILTER", "INFO", "FORMAT"], 1)
_meta["originaldata"] = pd.read_csv("./22/HG00096_HG00096.txt.gz", index_col=None, header=None)
_meta["totest"] = pd.read_csv("./floatfiles/22/HG00096.txt.gz",  index_col = None, header = None)


totest = random.choice(_meta.totest.tolist())

FBP = int(math.pow(2,28)) #FIRST_ALLELE_BIT_POS
NL = {"A":int(1), "T":int(2),"G":int(4), "C":int(8)} #NUCLEOTIDE_LABELS

LN = {int((NL["C"])*FBP*16):"C2",
 int((NL["G"])*FBP*16):"G2",
 int((NL["T"])*FBP*16):"T2",
 int((NL["A"])*FBP*16):"A2",
 int(NL["C"]*FBP):"C1",
 int(NL["G"]*FBP):"G1",
 int(NL["T"]*FBP):"T1",
 int(NL["A"]*FBP):"A1"}


errorsal1 = 0
errorsal2 = 0
listpbal1 = []
listpbal2 = []
nbtests = 1000

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

	printProgress(i,nbtests)


print("\nerrors for allele 1 : {0}\nerrors for allele 2 : {1}\ntotal errors : {2}\n".format(errorsal1, errorsal2, errorsal1+errorsal2))

print("\nIn total : {}% errors !".format(100*(errorsal1+errorsal2)/(2*nbtests)))