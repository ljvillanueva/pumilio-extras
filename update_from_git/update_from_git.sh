#!/bin/bash
# 17 Mar 2014

# update_from_git.sh

# For more details: http://ljvillanueva.github.io/pumilio/

#Script that downloads the last version of Pumilio from the git repo and updates the files in the local server.
# Please note that the git code may be broken or in the process of being changed. Always backup before an update.
# The script assumes it is in the parent directory of the git repo and that it exists already.
# If it is on:
#	/home/user/git/pumilio
# Place this script on
#	/home/user/git
# Then, set the path where Pumilio is installed inside /var/www/
# If "/var/www/pumilio", then set pumiliodir="pumilio"

pumiliodir="pumilio"

# Update the repo:
#	cd pumilio
#	git pull
#	cd ..

# Then, run as sudo:
#	sudo ./update_from_git.sh

#=================================================
# Script body
#=================================================

#check if can user is sudoer
if [ "$(whoami)" != "root" ]; then
	echo "Please run as root or using sudo."
	exit 1
fi

#Random dir
tmpdir=$RANDOM

mkdir /tmp/$tmpdir

cp -r pumilio/* /tmp/$tmpdir

rm -r /tmp/$tmpdir/tmp
rm -r /tmp/$tmpdir/sounds

sudo rsync -ruht /tmp/$tmpdir/ /var/www/$pumiliodir

sudo chown -R www-data:www-data $pumiliodir
sudo chmod -R 755 $pumiliodir

sudo chmod -R 777 /var/www/$pumiliodir/tmp
sudo chmod -R 777 /var/www/$pumiliodir/sounds

rm -r /tmp/$tmpdir

#Checks the database for updates on the structure
wget -O /dev/null http://localhost/$pumiliodir/upgrade

