#!/usr/bin/python
import paramiko

host = '192.168.88.1'
user = 'admin'
secret = ''
port = 22

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname=host, username=user, password=secret, port=port)

with open('/tmp/ip.txt') as file:
        for ip in file:
                ip = ip.strip()
                list = 'internet-servers' if ip.split('.')[2] == '2' else 'internet-users'
                print(list, ip)
                client.exec_command('/ip firewall address-list add list={0} address={1}'.format(list, ip))
client.close()
