#!/usr/bin/env python3 
# -*- coding=utf-8 -*-
# by EFLYTOP
# www.eflytop.com

from nornir import InitNornir
from nornir_utils.plugins.tasks.data import load_yaml
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.functions import print_result
from nornir.core.filter import F
from nornir_netmiko import netmiko_send_command, netmiko_send_config

def load_data(task):
	data = task.run(task=load_yaml, file=f'{task.host}.yaml')
	task.host['lo_num'] = data.result['lo_num']
	task.host['lo_ip'] = data.result['lo_ip']
	rendering = task.run(task=template_file, template='creat_loopbacl.j2', path='')
	task.run(task=netmiko_send_config, config_commands=rendering.result.split('\n'))

nr = InitNornir(config_file='config.yaml')
group1 = nr.filter(F(groups__contains='cisco_group1'))
r = group1.run(task=load_data)

print_result(r)