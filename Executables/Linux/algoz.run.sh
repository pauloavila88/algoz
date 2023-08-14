#!/bin/sh
PROJ_DIR=~/Algoz

# Go to Project Folder
cd ${PROJ_DIR}
# Activate Conda Virtual Environment
eval "$(conda shell.bash hook)" # https://stackoverflow.com/a/56155771
conda activate ./env
# Run ZapCrawler
python3 --version
if [ "$?" -eq "0" ]; 
then
    python3 cli.py ui --host 0.0.0.0 --port 80
else
    python --version
    if [ "$?" -eq "0" ]; 
    then
        python cli.py ui --host 0.0.0.0 --port 80
    fi
fi
# Inform Crawl Finish
echo Algoz as Terminated !