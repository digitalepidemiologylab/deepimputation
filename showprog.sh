#! /usr/bin/sh

max=100
min=0

Proggress_bar(){
	echo $1
	
}

#PATH="/mount/SDF/1000genomeprocesseddata/floatfiles/*"
_PATH="./floatfiles/*"

for dirs in $_PATH; do
chrom=$(basename $dirs)
echo $chrom
percdone=$(ls $dirs | wc -l | awk '{print $1*100/2504"%"}')
Proggress_bar $percdone

done
