#! /usr/bin/sh

max=100
min=0

Proggress_bar(){
	echo $1
	
}

_PATH="/mount/SDF/1000genomeprocesseddata/floatfiles/*"
#_PATH="./floatfiles/*"

echo
for dirs in $_PATH; do
chrom=$(basename $dirs)
percdone=$(ls $dirs | wc -l | awk '{print $1*100/2504"%%"}')
printf "[$chrom] %s\t $percdone %s\n%s\n"

done
