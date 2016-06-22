#!/usr/bin/python
import sys
import re

file = '/etc/dhcp/dhcpd.conf.reserved'
reserve_template = 'host %(name)s {\r\n\
hardware ethernet %(mac)s;\r\n\
fixed-address %(ip)s;\r\n\
}\r\n'


def is_valid(ip, mac, name):
	ip_regex = '([0-9]{1,3}\.){3}[0-9]{1,3}'
	mac_regex = '(\w{2}:){5}\w{2}'
	name_regex = '\w+'

	ip_reg_search = re.search(ip_regex, ip)
	mac_reg_search = re.search(mac_regex, mac)
	name_reg_search = re.search(name_regex, name)

	if not ip_reg_search or ip_reg_search.group(0) != ip:
		raise Exception('ip is incorrect!')
	elif not mac_reg_search or mac_reg_search.group(0) != mac:
		raise Exception('mac is incorrect!')
	elif not name_reg_search or name_reg_search.group(0) != name:
		raise Exception('name is incorrect!')
	return True

def add_new_reserved_address(ip, mac, name):
	with open(file, 'a') as file_handler:
		file_handler.write(reserve_template % {'name': name, 'mac': mac, 'ip': ip})

if len(sys.argv) != 4:
	raise Exception('Incorrect arguments count!')

name = sys.argv[1]
ip = sys.argv[2]
mac = sys.argv[3]

if is_valid(ip, mac, name):
	add_new_reserved_address(ip, mac, name)
else:
	print('IP address or Name is incorrect!')
