#! /usr/bin/sh

_PATH="./Tests/"


scripts=$(printf %q $_PATH "new_")
for _file in `ls "$scripts"*`
do
	echo $_file
	nohup python -u $_file > /dev/null &
done
