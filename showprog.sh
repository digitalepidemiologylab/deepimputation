#! /usr/bin/sh


Proggress(){

	width=${4:-100}
	bar=$(( $width * $2 / $3 ))
	percent=$(( 100 * $2 / $3 ))
	printf "[$1] %s\t $percent%% %s\t["
	for i in $(seq 1 $bar); do printf "#" 1>&2; done
	for i in $(seq $bar $(( $width-1 ))); do printf " " 1>&2; done
	printf "]%s%s\n"

	
}

PATHWRITTEN="/mount/SDF/1000genomeprocesseddata/floatfiles/*"
PATHORIGIN="/mount/SDF/1000genomeprocesseddata/"
#PATHWRITTEN="../fakedataset/encodeddata/*"
#PATHORIGIN="../fakedataset/"

for dirs in $PATHWRITTEN; do

	chrom=$(basename $dirs)
	written=$(ls $dirs | wc -l)
	totalfiles=$(ls "$PATHORIGIN/$chrom/" | wc -l)
	Proggress $chrom $written $totalfiles

done
