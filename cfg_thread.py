#!/usr/bin/env python3 
# -*- coding=utf-8 -*-
# by EFLYTOP
# www.eflytop.com

from netmiko import ConnectHandler,NetmikoTimeoutException,NetmikoAuthenticationException 
import time
import getpass
import sys
import threading
from queue import Queue

username = input("请输入设备用户名：")
password = getpass.getpass(prompt='请输入密码:')
#enpass = getpass.getpass(prompt='请输入enable密码:')

failed_login_ip = []
threads = []

devices = open('device.txt','r')
ip_list = [x.strip() for x in devices.readlines()]
devices.close()

commands = open('cmd.txt','r')
cmd_list = [y.strip() for y in commands.readlines()]
commands.close()

#print输出到txt文件
class Logger(object):
	def __init__(self, filename="Default.log"):
		self.terminal = sys.stdout
		self.log = open(filename, "a")
	def write(self, message):
		self.terminal.write(message)
		self.log.write(message)
	def flush(self):
		pass
sys.stdout = Logger('log.txt')

def ssh_session(ip, output_q):
	device_info = {
    'device_type': 'cisco_ios',
    'ip': ipaddr,
    'username': username,
    'password': password,
    #'port': 22,
    #'secret': enpass,
	}
	ssh_session = ConnectHandler(**device_info)
	output = ssh_session.send_config_set(cmd_list)
	save_cfg = ssh_session.save_config()
	print(output)
	print(save_cfg)	

start_time = time.time()

for ipaddr in ip_list:
	t = threading.Thread(target=ssh_session,args=(ipaddr, Queue()))
	t.start()
	threads.append(t)

for i in threads:
	i.join()	
print('本次执行时长：%.2f'%(time.time()-start_time) + '秒')
print("命令执行完毕，结果请查看log.txt文件")