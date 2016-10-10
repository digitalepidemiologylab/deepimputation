import math

totest = 0

totest = input("Entrer la valeur à décoder :")
totest = float(totest)

FBP = int(math.pow(2,28)) #FIRST_ALLELE_BIT_POS
SBP = int(math.pow(2,30)) #SECOND_ALLELE_BIT_POS
NL = {"A":int(0), "T":int(1),"G":int(2), "C":int(3)} #NUCLEOTIDE_LABELS
LN = {int(0):"A", int(1):"T",int(2):"G", int(3):"C", int(4):"A", int(5):"T",int(6):"G", int(7):"C"}

encAL1 = 0
encAL2 = 0

SVE= [NL["A"]*FBP, NL["T"]*FBP, NL["G"]*FBP, NL["C"]*FBP, (NL["A"]+1)*FBP, (NL["T"]+1)*FBP, (NL["G"]+1)*FBP, (NL["C"]+1)*FBP] #SNPSVALUESENCODED --> A-C 1st allele and then A-C 2nd allele

valuesalleles = [SVE[j] for j in range(len(SVE))]


i = len(valuesalleles)-1
found = False


while (totest  <= valuesalleles[i] + NL["C"]*FBP + NL["A"]*FBP /2) and not found : #### Focus only on the part of the value to decode where the info on allele 2 was encoded

	if totest  >= valuesalleles[i-1] + NL["C"]*FBP + NL["A"]*FBP /2:
		encAL2 = valuesalleles[i]
		AL2 = LN[i]
		found = True
	else:
		i -= 1


print(AL2)
found = False
i = 4

print(valuesalleles[i] + encAL2 + NL["A"]*FBP/2)

while (totest  <= valuesalleles[i] + encAL2 + NL["A"]*FBP/2) and not found:
	

	print(i)
	print(totest -valuesalleles[i-1]-encAL2)

	if totest  >= valuesalleles[i-1] + encAL2 + NL["A"]*FBP/2 :
		encAL1 = valuesalleles[i]
		AL1 = LN[i]
		position = totest - encAL2 - encAL1
		print("Position : {0}; AL1 : {1}, REF : {2}".format(position, AL1, AL2))
		found = True
	else:
		print("#############")
		i -= 1
