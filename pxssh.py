#!/usr/bin/python
import pxssh
try:
        s=pxssh.pxssh()
        hostname='10.10.10.23'
        username='root'
        password='123123'
        s.login(hostname,username,password,original_prompt='[$#>]')
        s.sendline('ps aux')
        s.prompt()
        print s.before
        s.sendline('df -h')
        s.prompt()
        print s.before
        s.sendline('ifconfig')
        s.prompt()
        print s.before
        s.logout() 
        print '---------------------------'
except  pxssh.ExceptionPxssh,e:
        print "pxssh failed on login."
        print str(e)

