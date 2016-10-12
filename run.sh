#! /usr/bin/sh

ITER=0


for _file in `ls ./Versions/new-job*.py`
do
	echo $_file
	nohup python -u $_file &
	ITER=$((ITER+1))


done
