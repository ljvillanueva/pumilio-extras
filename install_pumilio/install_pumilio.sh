#!/bin/bash
# 17 Mar 2014
#Script that installs the required software for Pumilio (http://ljvillanueva.github.io/pumilio/)
# The script is for a current version of Ubuntu.

# Set the path where Pumilio will be installed inside /var/www/
# If "/var/www/pumilio", then set pumiliodir="pumilio" without trailing slash

pumiliodir="pumilio"

# Then, run as sudo:
#	sudo ./install_pumilio.sh

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
cd /tmp/$tmpdir

#update repos
apt-get update

#Install LAMP
apt-get install tasksel
tasksel install lamp-server

#Install SoX, LAME, flac, etc.
apt-get install python-dev python-setuptools python-numpy libsndfile1-dev libasound2-dev imagemagick sox libsox* python-imaging flac lame

#Install the audiolab Python module
wget https://pypi.python.org/packages/source/s/scikits.audiolab/scikits.audiolab-0.8.tar.gz
tar -xvzf scikits.audiolab-0.8.tar.gz 
cd scikits.audiolab-0.8/
python setup.py install
cd ..
rm -r scikits.audiolab-0.8
rm scikits.audiolab-0.8.tar.gz

#Get current version number
pum_version="`wget -qO- http://ljvillanueva.github.io/pumilio/cur_ver.txt`"

printf "\n Will install Pumilio version "
printf $pum_version
printf "\n"

#Download from Github
wget https://github.com/ljvillanueva/pumilio/archive/v$pum_version.tar.gz
tar -xvzf v$pum_version.tar.gz
cd pumilio-$pum_version

mkdir -p /var/www/$pumiliodir

rsync -ruth . /var/www/$pumiliodir/

sudo chown -R www-data:www-data /var/www/$pumiliodir
sudo chmod -R 755 /var/www/$pumiliodir/

sudo chmod -R 777 /var/www/$pumiliodir/tmp
sudo chmod -R 777 /var/www/$pumiliodir/sounds

#Cleanup
cd /tmp
rm -r /tmp/$tmpdir

printf "\n Rename the file /var/www/"
printf $pumiliodir
printf "/config.php.dist to config.php \n  and set the MySQL credentials\n"
printf "Visit the page\n   http://localhost/"
printf $pumiliodir
printf "/install \n"
printf " to run the system checks and to setup the administrative account.\n\n"

