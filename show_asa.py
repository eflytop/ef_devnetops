#!/usr/bin/python3.9
# -*- coding=utf-8 -*-
# by EFLAB
# www.eflytop.com

import sys
import time
import os
import cmd
import getpass
#引入netmiko连接模块、报错模块
from netmiko import ConnectHandler,NetmikoTimeoutException,NetmikoAuthenticationException 

def logininfo(ipaddr):
        return {
        'device_type': 'cisco_asa',
        'ip': ipaddr,
        'username': user,
        'password': passwd,
        'port': 22,
        'secret':enpass,
        }

#authentication
user = input("请输入设备用户名：")
passwd = getpass.getpass(prompt='请输入密码:')
enpass = getpass.getpass(prompt='请输入enable密码:')

date = time.strftime("%b %d %H:%M:%S", time.localtime())

devices = open('device_list.txt','r')
devicelist = [x.strip() for x in devices.readlines()]
devices.close()

commands = open('cmd_list.txt','r')
cmdlist = [y.strip() for y in commands.readlines()]
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
sys.stdout = Logger('result.log')

for ipaddr in devicelist:
	try:
		print('INFO: ',date,ipaddr,'正在连接...')
		hostconn = ConnectHandler(**logininfo(ipaddr))
		hostconn.enable()
		for cmd in cmdlist:
			print('INFO: ',date,'正在执行命令：',cmd)
			output = hostconn.send_command(cmd)
			print(output)
		print()	
		hostconn.disconnect()

	except NetmikoAuthenticationException : #认证失败报错记录
		print('INFO: ',date,ipaddr,'[Error 1] Authentication failed.\n')

	except NetmikoTimeoutException : #登录超时报错记录
		print('INFO: ',date,ipaddr,'[Error 2] Connection timed out.\n')

	except : #未知报错记录
		print('INFO: ',date,ipaddr,'[Error 3] Unknown error.\n')

print("命令执行完毕，结果请查看result.log文件")	




