#!/bin/bash
# 9 Jul 2014
#Script that installs the wac2wav converter from 
# Wildlife Acoustics.
# 

# Then, run as sudo:
#	sudo ./install_wac2wav.sh

#=================================================
# Script body
#=================================================

#check if can user is sudoer
if [ "$(whoami)" != "root" ]; then
	echo "Please run as root or using sudo."
	exit 1
fi

#check if gcc is installed
if ! type "__gcc" > /dev/null; then
	echo ""
	echo "gcc not found. Please install compiler using:"
	echo " sudo apt-get install build-essential"
	echo ""
	exit 1
fi

#Random dir
tmpdir=$RANDOM

mkdir /tmp/$tmpdir
cd /tmp/$tmpdir

echo " Downloading source..."
echo " "

#Get source
wget http://www.wildlifeacoustics.com/downloads/wac2wavcmd-1.0.zip
unzip wac2wavcmd-1.0.zip
cd wac2wavcmd-1.0

echo " Compiling..."
echo " "

#compile
make

echo " Installing to /usr/local/bin/"
echo " "

cp wac2wavcmd /usr/local/bin/

