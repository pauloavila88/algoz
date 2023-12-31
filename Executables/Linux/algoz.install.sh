#!/bin/sh
PROJ_DIR=~/Algoz

# Re-instalation Check
if ( test -d "$PROJ_DIR" ); then
    rm -r ${PROJ_DIR}
fi
# Create/Move to Project Folder
mkdir ${PROJ_DIR}
cd ${PROJ_DIR}

# Python Instalation Status
python3 --version
pythonstatus=$?
# Git Instalation Status
git --version
gitstatus=$?
# Miniconda Instalation Status
conda --version
condastatus=$?

# Install Python if Required - https://iohk.zendesk.com/hc/en-us/articles/16724475448473-Install-Python-3-11-on-ubuntu
if [ "$pythonstatus" -eq "0" ]; 
then
    echo "Python Installed"
else
    echo "Python Instalation Start"
    # Upgrade and update Ubuntu to the latest version 
    sudo apt update && sudo apt upgrade
    # Install the required packages
    sudo apt install wget build-essential libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev zlib1g-dev
    # Download python 3.11
    sudo add-apt-repository ppa:deadsnakes/ppa
    # Install it
    sudo apt install python3.11
    python3 --version
fi

# Install GIT if Required - https://www.digitalocean.com/community/tutorials/how-to-install-git-on-ubuntu-20-04
if [ "$gitstatus" -eq "0" ]; 
then
    echo "Git Installed"
else
    echo "Git Instalation Start"
    sudo apt update
    sudo apt install git
    git --version
fi

# Install Conda if Required - https://developers.google.com/earth-engine/guides/python_install-conda#linux
if [ "$condastatus" -eq "0" ]; 
then
    echo "Miniconda Installed"
else
    echo "Miniconda Instalation Start"
    # Download the Miniconda installer to your Home directory.
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh
    # Install Miniconda quietly, accepting defaults, to your Home directory.
    bash ~/miniconda.sh -b
    # Remove the Miniconda installer from your Home directory.
    rm ~/miniconda.sh
    source $HOME/miniconda3/bin/activate
    conda deactivate
    conda --version
fi

# Clone Repository
git clone --branch main https://github.com/pauloavila88/algoz.git .
# Systemctl Service file CHMOD edit (Execute Permission)
sudo chmod +x ~/Algoz/Executables/Linux/algoz.run.service.sh
# Create/Activate Conda Virtual Environment
echo Current DIR : "$PWD"
source $HOME/miniconda3/bin/activate
conda deactivate
conda create --prefix ./env python=3.11 -y
conda activate ./env
# Install required Libraries
pip install -r requirements.txt
# Get Google Cloud Credentials
bash ~/Algoz/Executables/Linux/algoz.gapi.install.sh

# Inform Instalation Completed
echo Algoz Instalation Completed!
printf 'press [ENTER] to exit ...'
read _
exit