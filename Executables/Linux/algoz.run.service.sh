#!/bin/sh
while true
do
    # Run Algoz.py
    sudo /home/ubuntu/Algoz/env/bin/python /home/ubuntu/Algoz/cli.py ui --host 0.0.0.0 --port 80
done
# Inform Crawl Finish
echo Algoz as Terminated !