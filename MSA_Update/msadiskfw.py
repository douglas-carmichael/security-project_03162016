#!/usr/bin/python
import os
import ftplib
import sys
#
#
from ftplib import FTP
#

# Define our variables
controller_ip = ""
msa_login = ""
msa_password = ""
#
# Define our directory and parameters
firmware_dir = ""
enclosure_id = "2"
enclosure_disks = "25"
#
#
#
# Log into the MSA controller
msa_ftp = FTP(controller_ip)
msa_ftp.login(msa_login, msa_password)
#
# Walk the directory for valid firmware files
#
# Create our working variables
#
for root, dirs, files in os.walk(firmware_dir, topdown=False):
	for name in files:
		if name != "null":
			our_path = os.path.join(root, name)
			slot_dir = root.split('/')[5]
			slot_number = slot_dir.split('_')[1]
			disk_id = "disk:" + enclosure_id + ":" + slot_number
			stor_command = "STOR " + disk_id
			print "Uploading " + name + " to " + disk_id
			print stor_command
			msa_ftp.storbinary(stor_command, open(our_path, "rb"), 1024)
#
#
# Close the connection to the server
msa_ftp.quit()



