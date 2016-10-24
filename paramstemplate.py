# -*- coding: utf-8 -*-
import math

##########################################################   TEMPLATE ---> DO NOT MODIFY ! MAKE YOUR CHANGES TO THE FILE PARAMS.PY
##########General
PATHINPUT = "/mount/SDF/1000genomeprocesseddata/"
VERBOSE = False
LOGGING = True

FBP = int(math.pow(2,28)) #FIRST_ALLELE_BIT_POS
NL = {"A":int(1), "T":int(2),"G":int(4), "C":int(8)} #NUCLEOTIDE_LABELS
SVE= [NL["A"]*FBP, NL["T"]*FBP, NL["G"]*FBP, NL["C"]*FBP, (NL["A"])*FBP*16, (NL["T"])*FBP*16, (NL["G"])*FBP*16, (NL["C"])*FBP*16] #SNPSVALUESENCODED --> A-C 1st allele and then A-C 2nd allele


LN = {int((NL["C"])*FBP*16):"C2", #Reverse dictionnary to decode information
 int((NL["G"])*FBP*16):"G2",
 int((NL["T"])*FBP*16):"T2",
 int((NL["A"])*FBP*16):"A2",
 int(NL["C"]*FBP):"C1",
 int(NL["G"]*FBP):"G1",
 int(NL["T"]*FBP):"T1",
 int(NL["A"]*FBP):"A1"}


#########Changetofloat.py
FILEBATCHSIZE=1

##########Testdecoding.py
PATHORIGIN = PATHINPUT
PATHENCODED = PATHINPUT+"/encodeddata/"
nbtests = 1000
nbfilesmax = 100

##########Subsets.py
PATHSUBSET = PATHINPUT
PROPTRAIN = 0.6
PROPTEST = 0.2
PROPVALID = 1-PROPTRAIN-PROPTEST
COPY=False
SIZEFRAGMENTS = 1000