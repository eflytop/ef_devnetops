#!/usr/bin/env python3 
# -*- coding=utf-8 -*-
# by EFLYTOP
# www.eflytop.com

from netmiko import ConnectHandler,NetmikoTimeoutException,NetmikoAuthenticationException 
import time
import getpass
import sys

username = input("请输入设备用户名：")
password = getpass.getpass(prompt='请输入密码:')
#enpass = getpass.getpass(prompt='请输入enable密码:')

failed_login_ip = []

devices = open('device.txt','r')
ip_list = [x.strip() for x in devices.readlines()]
devices.close()

commands = open('cmd.txt','r')
cmd_list = [y.strip() for y in commands.readlines()]
commands.close()

start_time = time.time()

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


for ipaddr in ip_list:

	device_info = {
	    'device_type': 'cisco_ios',
	    'ip': ipaddr,
	    'username': username,
	    'password': password,
	    #'port': 22,
	    #'secret': enpass,
	}	

	try:
		host_conn = ConnectHandler(**device_info)
		print('INFO: ',time.strftime('%x %X'),ipaddr,'正在连接...')	
		output = host_conn.send_config_set(cmd_list)
		save_cfg = host_conn.save_config()
		print(output)
		print(save_cfg)

	except NetmikoAuthenticationException : #认证失败报错记录
		print('INFO: ',time.strftime('%x %X'),ipaddr,'[Error 1] Authentication failed.')
		failed_login_ip.append(ipaddr)

	except NetmikoTimeoutException : #登录超时报错记录
		print('INFO: ',time.strftime('%x %X'),ipaddr,'[Error 2] Connection timed out.')
		failed_login_ip.append(ipaddr)

	except : #未知报错记录
		print('INFO: ',time.strftime('%x %X'),ipaddr,'[Error 3] Unknown error.')
		failed_login_ip.append(ipaddr)

print('下列主机登录失败，请手动检查：')
for i in failed_login_ip:
	print(i)
print('本次执行时长：%.2f'%(time.time()-start_time) + '秒')
print("命令执行完毕，结果请查看log.txt文件")