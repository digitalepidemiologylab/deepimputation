#! /usr/bin/sh

ITER=0


for _file in `ls ./Versions/new-job*`
do
	echo $_file
	nohup python -u $_file > "./Versions/log$ITER.out" &
	ITER=$((ITER+1))


done
