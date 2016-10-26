#!/usr/bin/sh

_file="../1000genomeprocesseddata/2/_meta.txt.gz"
#_file="../fakedataset/2/_meta.txt.gz"
sizegrp=25000
#sizegrp=1100
onecentimorgan=1000000
#onecentimorgan=1000
startline=8
nboflines=$(($(zcat $_file | wc -l) -$startline))
nboftests=$(($nboflines/$sizegrp))
for ((i=$startline; i<$nboftests ; i++)); do
	begin=$i
	posbeg=$(zcat $_file | head -$begin | tail -n1 | awk '{print $2}')
	end=$(($begin+$sizegrp))
	posend=$(zcat $_file | head -$end | tail -n1 | awk '{print $2}')
	difference=$(($posend-$posbeg))

	if [ $difference -lt $onecentimorgan ]; then

		echo $difference
	fi
done
