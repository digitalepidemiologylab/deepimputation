#! /usr/bin/sh

for dirs in /mount/SDF/1000genomeprocesseddata/floatfiles/*; do
echo $dirs
ls $dirs | wc -l | awk '{print $1*100/2504"%"}'
done
