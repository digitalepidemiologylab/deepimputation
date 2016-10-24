#! /usr/bin/sh


Proggress(){

	width=${9:-70}
	bar=$(( $width * $2 / $3 ))
	percent=$(( 100 * $2 / $3 ))
	printf "[$1] %s\t $percent%% %s\t["
	for i in $(seq 1 $bar); do printf "#" 1>&2; done
	for i in $(seq $bar $(( $width-1 ))); do printf " " 1>&2; done
	printf "]%s\tLast changes : $4 $5%s\tTime spent : $6%s\n%s\n"

	
}

PATHWRITTEN="/mount/SDF/1000genomeprocesseddata/floatfiles/*"
PATHORIGIN="/mount/SDF/1000genomeprocesseddata/"
#PATHWRITTEN="../fakedataset/floatfiles/*"
#PATHORIGIN="../fakedataset/"

for dirs in $PATHWRITTEN; do

	chrom=$(basename $dirs)
	written=$(ls $dirs | wc -l)
	totalfiles=$(ls "$PATHORIGIN/$chrom/" | wc -l)
	change_date=$(stat $dirs | grep Chang | awk '{print $2}')
	change_hour=$(stat $dirs | grep Chang | awk '{print $3}')
	if [ -f "/mount/SDF/deepimputation/log$chrom.log" ];then
		timespent=$(tail "/mount/SDF/deepimputation/log$chrom.log" | grep after | tail -n1 | awk '{print $5}')
	elif [ -f "/mount/SDF/deepimputation/LOGS/log$chrom.log" ]; then
		timespent=$(tail "/mount/SDF/deepimputation/LOGS/log$chrom.log" | grep after | tail -n1 | awk '{print $5}')
	else
		timespent="unknown"
	fi
	Proggress $chrom $written $totalfiles $change_date $change_hour $timespent

done
