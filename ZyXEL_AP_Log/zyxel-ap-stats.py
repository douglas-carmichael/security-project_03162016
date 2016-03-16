#!/usr/bin/python
#
# Process the ZyXEL AP log file data.

import re
import os
import SocketServer
import ap_log_modules
import ap_db_modules

ap_prod_message = 'Nov 24 00:31:21 192.168.1.2 CEF: 0|ZyXEL|NWA3560-N||0|wlan|5|src=0.0.0.0 dst=0.0.0.0 spt=0 dpt=0 msg=Station has disassoc. Interface:wlan-1-1 Station: ec:1f:72:94:e9:af'
ap_stat_message = 'Nov 24 00:31:06 192.168.1.2 CEF: 0|ZyXEL|NWA3560-N|2.23(UJC.8)|0|INTERFACE STATISTICS|5|src=0.0.0.0 dst=0.0.0.0 spt=0 dpt=0 msg=name=wlan-2-1,status=Up,TxPkts=7646619,RxPkts=3917124,Colli.=0,TxB/s=0,RxB/s=0'
ap_disconnect_message = 'Nov 23 23:26:50 192.168.1.2 CEF: 0|ZyXEL|NWA3560-N||0|wlan|5|src=0.0.0.0 dst=0.0.0.0 spt=0 dpt=0 msg=WPA authenticator requests disconnect: reason 2. Interface:wlan-2-1 Station: 12:34:56:78:90:dd'

# Hack to get the actual data out of the message.
		
def handle_msg(OurMessage, our_cursor):
	our_message_list = OurMessage.split("|")
	if(valueInList("INTERFACE STATISTICS", our_message_list)) == True:
		ap_db_modules.log_wlan_stat(our_cursor, ap_log_modules.stats_msg(OurMessage))
	elif(valueInList("Station has", our_message_list)) == True:
		ap_db_modules.log_wlan_auth(our_cursor, ap_log_modules.wlan_msg(OurMessage))
	else:
		print "Inappropriate message: " + OurMessage
		
def valueInList(value, list):
	return any(value in x for x in list)

# Class to handle the received messages

class MsgTCPHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		self.data = self.rfile.readline().strip()
		handle_msg(self.data, our_cursor)
		
### Main script

# Initialize the database connection
our_cursor = ap_db_modules.connect_db('wireless_db')

# Create our server
server = SocketServer.TCPServer(("localhost", 5030), MsgTCPHandler)

server.serve_forever()


