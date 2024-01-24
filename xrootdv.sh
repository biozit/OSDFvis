#!/bin/bash
filename='hosts.txt'

while read p; do 
    echo -n "$p "
    a=`curl -v --silent $p:1094 2>&1 | grep '< Server:' | awk {'print $3'}`
    echo $a
done < "$filename"
