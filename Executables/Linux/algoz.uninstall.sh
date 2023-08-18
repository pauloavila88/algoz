#!/bin/sh
PROJ_DIR=~/Algoz

# Delete Project Folder
if ( test -d "$PROJ_DIR" ); then
    rm -r ${PROJ_DIR}
fi
# Inform Uninstall Completed
if !( test -d "$PROJ_DIR" ); then
    echo Algoz Uninstaled!
fi
printf 'press [ENTER] to exit ...'
read _
exit