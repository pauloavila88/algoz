#!/bin/sh
PROJ_DIR=~/Algoz
cd ${PROJ_DIR}

# Get Google Cloud Credentials
if ( -d "~/Algoz/crawler/confidential" ); 
then
    rm -r ~/Algoz/crawler/confidential
fi
mkdir ~/Algoz/crawler/confidential
echo [ WARNING ] - Before continuing insert the provided { client_secret.json } file in this folder: $HOME/Algoz/crawler/confidential
printf 'press [ENTER] to continue ...'
read _
if ( -f "~/Algoz/crawler/confidential/client_secret.json" ); 
then
    python3 ~/Algoz/crawler/authorize_pygsheets.py
    mv ./sheets.googleapis.com-python.json ~/Algoz/crawler/confidential
    printf 'Google Cloud Credentials Authorized !'
    sleep 5
else
    echo [ WARNING ] File { client_secret.json } not added into $HOME/Algoz/crawler/confidential!
    echo Retry running $HOME/Algoz/Executables/Linux/algoz.gapi.install.sh
    sleep 5
fi