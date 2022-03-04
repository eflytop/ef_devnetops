#!/usr/bin/env python3 
# -*- coding=utf-8 -*-
# by EFLYTOP
# www.eflytop.com

from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result

nr = InitNornir(config_file="config.yaml")
results = nr.run(netmiko_send_command, command_string='sh ip route') 

print_result(results)