#!/usr/bin/env python3 
# -*- coding=utf-8 -*-
# by EFLYTOP
# www.eflytop.com

from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_get
from nornir_utils.plugins.functions import print_result
from nornir_utils.plugins.tasks.files import write_file
from datetime import date

nr = InitNornir(config_file="config.yaml")

def backup_cfg(task):
	r = task.run(task=napalm_get, getters=['config'])
	task.run(task=write_file, content=r.result['config']['running'], filename=str(task.host.name)+'-'+str(date.today())+'.cfg')

nr = InitNornir(config_file='config.yaml')
result = nr.run(name='正在备份设备配置...', task=backup_cfg)

print_result(result)