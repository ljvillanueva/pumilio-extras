#!/usr/bin/python
# For Pumilio 2.4.0 or recent

"""
v. 2.4.0a (28 Jul 2014)
Script to migrate sound files between Pumilio installations. 
 You can choose to either copy the files or move the files to save space.
 Edit the file configfile.py.dist with the appropiate values and save it as configfile.py

The script will migrate the sound files, sites, collections, sensors, kml, tags, and marks. It will not 
 migrate users, samples, or Pumilio settings. 

Whenever there is an error, the script will try to give information on what the problem was, 
 pay attention at these messages.
"""

"""
WORK IN PROGRESS. DO NOT USE!
"""
import sys
sys.exit (0)

#################################################
# HEADER DECLARATIONS							#
#################################################

# Import modules
import commands
import os
import wave
# import sys
# import datetime
# import time
import shutil


try:
	import MySQLdb
except:
	print "\n MySQLdb is not installed. To install in Ubuntu use: \n   sudo apt-get install python-mysqldb\n"
	sys.exit (1)


#################################################
# COMMAND LINE ARGUMENTS						#
#################################################


# Place "global" variables in the namespace
try:
	from configfile import *
except:
	print "\n The configuration file is missing.\n  Rename the file configfile.py.dist to configfile.py\n  and fill the values.\n"
	sys.exit (1)


#Check if there are at least two installations given
if len(pum_installations) < 2:
	print "\n Script needs at least 2 Pumilio installations."
	sys.exit (1)


#Check if there are at least two installations given
if len(pum_target) != 1:
	print "\n Script needs only 1 Pumilio target."
	sys.exit (1)


#check that can read folders
for db_database, server_dir in pum_installations.iteritems():
	print "\n Checking if directory %s exists..." % (server_dir),
	if os.access(server_dir, os.R_OK) == False:
		print "\n The script could not find the directory '" + server_dir + "' or you do not have read permissions."
		print "\n Exiting program.\n"
		sys.exit(1)
	#check db
	print "checking if we can connect to database %s..." % (db_database)
	try:
	        con = MySQLdb.connect(host=db_hostname, user=db_username, passwd=db_password, db=db_database)
	except MySQLdb.Error, e:
	        print "Error connecting to database %s. %d: %s" % (db_database, e.args[0], e.args[1])
	        sys.exit (1)


#################################################
# FUNCTION DECLARATIONS							#
#################################################


def fileExists(f):
	try:
		file = open(f)
	except IOError:
		exists = 0
	else:
		exists = 1
	return exists



def getsites():
        try:
                con = MySQLdb.connect(host=db_hostname, user=db_username, passwd=db_password, db=db_database)
        except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit (1)
        cursor = con.cursor()
        query = "SELECT SiteID, SiteName, SiteLat, SiteLon FROM Sites ORDER BY SiteName";
        cursor.execute (query)
        rows = cursor.fetchall ()
        print " Sites: "
        print " ID\tName of site and coordinates\n====================================\n"
        for row in rows:
                print " %s\t%s (%s,%s)" % (row[0], row[1], row[2], row[3])
        print " "
        cursor.close ()
        con.close ()




def getcollections():
        try:
                con = MySQLdb.connect(host=db_hostname, user=db_username, passwd=db_password, db=db_database)
        except MySQLdb.Error, e:
                print "Error %d: %s" % (e.args[0], e.args[1])
                sys.exit (1)
        cursor = con.cursor()
        query = "SELECT ColID, CollectionName FROM Collections ORDER BY CollectionName";
        cursor.execute (query)
        rows = cursor.fetchall ()
        print " Sites: "
        print " ID\tName of collection\n====================================\n"
        for row in rows:
                print " %s\t%s" % (row[0], row[1])
        print " "
        cursor.close ()
        con.close ()



        
#################################################
# EXECUTE THE SCRIPT							#
#################################################



while confirmid=="n":
	export_type = raw_input('\n\nSelect how to select files to export: [c]ollections or [s]ites: ')
	if export_type=='c' or export_type=='s': 
		confirmid="y"
		continue
	else:
		print "Error, please type the letter \"c\" for collection or \"s\" for sites\n"
		confirmid="n"
		continue

confirmid="n"
try:
	if export_type=='c':
		while confirmid=="n":
			getcollections()
			ColID = raw_input('\n\nEnter the ID of the collection to save the files into: ')
			confirmcollection(ColID)
			while confirmid!="y":
				confirmid = raw_input('\nIs this the correct collection? [y/n]: ')
				if confirmid == "y" or confirmid == "n":
					if confirmid=='y': continue
					if confirmid=='n': break
				else:
					print "Error, please type the letter \"y\" for yes or \"n\" for no\n"

		with Ticker("\n Exporting data..."):
			export_dir = exportcollection(str(ColID), export_dir)



	elif export_type=='s': 
		while confirmid=="n":
			getsites()
			SiteID = raw_input('\n\nEnter the ID of the site to save the files into: ')
			confirmsite(SiteID)
			while confirmid!="y":
				confirmid = raw_input('\nIs this the correct site? [y/n]: ')
				if confirmid == "y" or confirmid == "n":
					if confirmid=='y': continue
					if confirmid=='n': break
				else:
					print "Error, please type the letter \"y\" for yes or \"n\" for no\n"
		with Ticker("\n Exporting data..."):
			export_dir = exportsite(str(SiteID), export_dir)

	with Ticker("\n Creating archive file..."):
		cleanup(export_dir, export_format)


except (KeyboardInterrupt):
	print "\n\n Interrupt command received...\n  exiting..."
	when_stop=datetime.datetime.now().strftime("  Script keyboard-interrupted on %d/%b/%y %H:%M\n")
	print when_stop

	status, output = commands.getstatusoutput('rm *.pyc')
	sys.exit (0) #Exit normally

	
status, output = commands.getstatusoutput('rm *.pyc')

process_date = datetime.datetime.now().strftime("\n\n File export complete.\n")

print process_date
sys.exit (0)
