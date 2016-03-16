# ap_log_modules.py: modules to parse our log messages

import re

def wlan_msg(ap_wlan_message):
	raw_message_list = ap_wlan_message.split("|") 
	wlan_message_list = raw_message_list[7].split(" ")
	wlan_info_list = []
	for msg_ptr in range(4, len(wlan_message_list)):
		wlan_msg_info = wlan_message_list[msg_ptr]
		
		# Stop when we get to the "Interface" section
		if 'Interface:' in wlan_msg_info:
			station_if = wlan_msg_info.split(":")[1]
		elif 'Station:' in wlan_msg_info:
			# NOTE: This is a kludge
			wlan_msg_info = ""
		elif re.match("[0-9a-f]{2}([-:])[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", wlan_msg_info):
			station_mac = wlan_msg_info
		else:
			wlan_info_list.append(wlan_msg_info)
	
	wlan_message = wlan_info_list[0][4:] + ' ' + wlan_info_list[1] + ' ' + wlan_info_list[2]

	# NOTE: We've now got our WLAN message (assoc/disassoc/auth) and interface/MAC
	
	wlan_message_record = [station_if, station_mac, wlan_message]
	return wlan_message_record
		
def stats_msg(ap_wlan_message):
	wlan_message_list = ap_wlan_message.split("|")
	wlan_raw_list = wlan_message_list[7].split(" ")
	stats_raw_message = wlan_raw_list[4]
	stats_raw_list = stats_raw_message[4:].split(",")
	
	stats_list = []
	
	for stats_element in stats_raw_list:
		stats_list.append(stats_element.split("=")[1])

	return stats_list
	