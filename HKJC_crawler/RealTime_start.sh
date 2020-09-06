#!/bin/bash
source ~/anaconda3/bin/activate HKJC
while true
do
    python RealTime_crawler.py $1
    sleep $2
done
