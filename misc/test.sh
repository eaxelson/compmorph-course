#!/bin/sh

Lectures="Lecture*"
if [ "$1" != "" ]; then
    Lectures=$1;
fi

verbose="false"
if [ "$2" = "--verbose" ]; then
    verbose="true";
fi

for dir in $Lectures;
do
    cd $dir;
    # remove interactive and dummy commands
    cat src/Lecture.py | perl -pe 's/^from hfst_dev import start_xfst//; s/^start_xfst\(\)//; s/^help\(.*//; s/^.*some_text_file.*//; s/^.*some_analyzer.*//;' > tmp.py;
    if [ "$verbose" = "true" ]; then
	python3 tmp.py;
    else
	python3 tmp.py > /dev/null 2> /dev/null;
    fi
    if [ "$?" = "0" ]; then
	echo $dir": PASS";
    else
	echo $dir": FAIL";
    fi
    rm tmp.py;
    cd ..;
done
