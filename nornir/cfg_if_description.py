#!/usr/bin/env python3 
# -*- coding=utf-8 -*-
# by EFLYTOP
# www.eflytop.com

import ipdb
from nornir import InitNornir
from nornir_netmiko import netmiko_send_command, netmiko_send_config
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
output = nr.run(netmiko_send_command, command_string='sh interface switchport', use_textfsm=True) 

for switch in output.keys():
	for i in range(6):
		trunk_description = ['interface ' + output[switch].result[i]['interface'],'description Trunk Port (via nornir)']
		access_description = ['interface ' + output[switch].result[i]['interface'],'description Access to VLAN '+output[switch].result[i]['access_vlan']+' (via nornir)']
		if 'trunk' in output[switch].result[i]['mode']:
			nr.run(netmiko_send_config, config_commands=trunk_description)
		elif 'static access' in output[switch].result[i]['mode']:
			nr.run(netmiko_send_config, config_commands=access_description)

results = nr.run(netmiko_send_command, command_string='show inter descrip')
print_result(results)
