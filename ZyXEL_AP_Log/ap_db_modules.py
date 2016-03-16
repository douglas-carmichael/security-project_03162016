#!/usr/bin/python
#
# ap_db_modules.py: Database handling modules for processing log data
#

import psycopg2
import syslog
import sys

# define our variables
db_user = ""
db_pwd = ""

def connect_db(our_db):
	try:
		our_connection = psycopg2.connect(database=our_db, user=db_user, password=db_pwd)
	except psycopg2.OperationalError as e:
		print('Unable to connect!\n{0}').format(e)
		sys.exit(1)
	else:
		our_connection.autocommit = True
		our_cursor = our_connection.cursor()
		return our_cursor
		
def log_wlan_auth(our_cursor, auth_list):
	try:
		print auth_list
		our_cursor.execute("INSERT INTO wlan_auths (if_name, if_mac, if_msg) \
		VALUES(%s, %s, %s)", (auth_list[0], auth_list[1], auth_list[2]))
	except psycopg2.OperationalError as e:
		print('Unable to log auth msg: \n{0}').format(e)
	else:
		return 0
		
def log_wlan_stat(our_cursor, stat_list):
	try:
		print stat_list
		if "wlan" in stat_list[0]:
	 		our_cursor.execute("INSERT INTO wlan_statistics (if_name, if_status, \
			tx_packets, rx_packets) \
			VALUES(%s, %s, %s, %s)", (stat_list[0], stat_list[1], stat_list[2], 
			stat_list[3]))
		else:
		  	our_cursor.execute("INSERT INTO ether_statistics (if_name, if_status, \
			tx_packets, rx_packets, uptime) \
			VALUES(%s, %s, %s, %s)", (stat_list[0], stat_list[1], stat_list[2], 
			stat_list[3]))

	except psycopg2.OperationalError as e:
		print('Unable to log stat msg: \n{0}').format(e)
	else:
		return 0
