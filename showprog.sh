#! /usr/bin/sh


Proggress(){

	width=${9:-75}
	bar=$(( $width * $2 / $3 ))
	percent=$(( 100 * $2 / $3 ))
	printf "[$1] %s\t $percent%% %s\t["
	for i in $(seq 1 $bar); do printf "#" 1>&2; done
	for i in $(seq $bar $(( $width-1 ))); do printf " " 1>&2; done
	printf "]%s\tLast changes : $4 $5%s\n%s\n"

	
}

PATHWRITTEN="/mount/SDF/1000genomeprocesseddata/floatfiles/*"
PATHORIGIN="/mount/SDF/1000genomeprocesseddata/"
PATHWRITTEN="../fakedataset/encodeddata/*"
PATHORIGIN="../fakedataset/"

for dirs in $PATHWRITTEN; do

	chrom=$(basename $dirs)
	written=$(ls $dirs | wc -l)
	totalfiles=$(ls "$PATHORIGIN/$chrom/" | wc -l)
	change_date=$(stat $dirs | grep Chang | awk '{print $2}')
	change_hour=$(stat $dirs | grep Chang | awk '{print $3}')
	Proggress $chrom $written $totalfiles $change_date $change_hour

done
