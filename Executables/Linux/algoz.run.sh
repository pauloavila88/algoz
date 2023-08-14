#!/bin/sh
PROJ_DIR=~/Algoz

# Go to Project Folder
cd ${PROJ_DIR}
# Activate Conda Virtual Environment
# eval "$(conda shell.bash hook)" # https://stackoverflow.com/a/56155771
source $HOME/miniconda3/bin/activate
conda deactivate
conda activate ./env
# Run ZapCrawler
sudo ./env/bin/python cli.py ui --host 0.0.0.0 --port 80
# Inform Crawl Finish
echo Algoz as Terminated !