#!/bin/sh
set -e

echo "IP address: `awk 'END{print $1}' /etc/hosts`"

### 1. Work Script ###
echo "### 1. Work Script ###"
su - appuser -c "/usr/local/bin/python /home/appuser/app.py &>> /home/appuser/application.log"


echo "### 2. Finish ###"
###### DONT CHANGE IT ######
echo "VM-WORKED-AND-SCRIPT-FINISHED.VM-WILL-BE-STOPED." 
