#! /usr/bin/sh

for _file in `ls ./Versions/new-job*.py`
do
	echo $_file
	nohup python -u $_file > /dev/null &
done
