#!/usr/bin/env python  
# -*- coding: utf-8 -*-  
#python ssh.py  10.96.60.41 123123 ls;ifconfig;ls -l 
 
import pexpect
import sys
ip=sys.argv[1]
username=sys.argv[2]
passwd=sys.argv[3]
cmd=sys.argv[4]
#print ip,username,passwd,cmd
def ssh_cmd(ip,username , passwd, cmd):
    ret = -1
    ssh = pexpect.spawn('ssh %s@%s "%s"' % (username,ip, cmd))
    try:
        i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=5)
        if i == 0 :
            ssh.sendline(passwd)
        elif i == 1:
            ssh.sendline('yes\n')
            ssh.expect('password: ')
            ssh.sendline(passwd)
        ssh.sendline(cmd)
        r = ssh.read()
        print r
        ret = 0 
    except pexpect.EOF:
        print "EOF"
        ssh.close()
        ret = -1
    except pexpect.TIMEOUT:
        print "TIMEOUT"
        ssh.close()
        ret = -2
    return ret
#ssh_cmd('10.96.60.41','123123','ifconfig;ls;dir;df -hT')
ssh_cmd(ip,username,passwd,cmd)
