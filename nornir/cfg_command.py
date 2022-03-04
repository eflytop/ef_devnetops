#!/usr/bin/env python3 
# -*- coding=utf-8 -*-
# by EFLYTOP
# www.eflytop.com

from nornir import InitNornir
from nornir_netmiko import netmiko_send_command, netmiko_send_config
from nornir_utils.plugins.functions import print_result, print_title

nr = InitNornir(config_file="config.yaml")

def config(cisco):
	cisco.run(task=netmiko_send_config, config_file='cmd.txt')
	cisco.run(task=netmiko_send_command, command_string='show vlan brief')

print_title('正在配置VLAN999...')
results = nr.run(task=config)

print_result(results)