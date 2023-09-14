#!/bin/sh
PROJ_DIR=~/Algoz
cd ${PROJ_DIR}

# Get Google Cloud Credentials
if [ ! -d "$HOME/Algoz/crawler/confidential" ]; 
then
    echo Credentials Folder does not exist. Creating "$HOME/Algoz/crawler/confidential"...
    mkdir ~/Algoz/crawler/confidential
else
    echo Credentials Folder does exist!
fi

if [ -e "$HOME/Algoz/crawler/confidential/sheets.googleapis.com-python.json" ]; 
then
    echo Renew Google API credentials!
    rm ~/Algoz/crawler/confidential/sheets.googleapis.com-python.json
else
    echo Google API credentials does not exist!
fi

if [ ! -e "$HOME/Algoz/crawler/confidential/client_secret.json" ]; then
    echo [ WARNING ] - Before continuing insert the provided { client_secret.json } file in this folder: $HOME/Algoz/crawler/confidential
    printf 'press [ENTER] to continue ...'
    read _
fi

if [ -e "$HOME/Algoz/crawler/confidential/client_secret.json" ]; then
    ~/Algoz/env/bin/python ~/Algoz/crawler/authorize_pygsheets.py
    if [ -e "$HOME/Algoz/sheets.googleapis.com-python.json" ];
    then
        mv ./sheets.googleapis.com-python.json ~/Algoz/crawler/confidential
        printf 'Google Cloud Credentials Authorized !'
        printf 'press [ENTER] to continue ...'
        read _
    else
        echo [ WARNING ] - Something went wrong while Authorizing Google Cloud APIs!
        echo Retry running $HOME/Algoz/Executables/Linux/algoz.gapi.install.sh
        printf 'press [ENTER] to continue ...'
        read _
    fi
else
    echo [ WARNING ] - File { client_secret.json } not added into $HOME/Algoz/crawler/confidential!
    echo Retry running $HOME/Algoz/Executables/Linux/algoz.gapi.install.sh
    printf 'press [ENTER] to continue ...'
    read _
fi