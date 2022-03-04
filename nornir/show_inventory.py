#!/usr/bin/env python3 
# -*- coding=utf-8 -*-
# by EFLYTOP
# www.eflytop.com

from nornir import InitNornir
from nornir_netmiko import netmiko_send_command
from nornir_utils.plugins.functions import print_result
from nornir.core.task import Task, Result

nr = InitNornir(config_file="config.yaml")
def host_detail(task):
	return (task.host.name,
		task.host.hostname,
		task.host.username,
		task.host.password,
		task.host.platform,
		task.host.groups
		)

result = nr.run(task=host_detail)
print_result(result)