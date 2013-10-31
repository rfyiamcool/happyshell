#!/usr/bin/python
# -*- coding=utf-8 -*-
import json 
import urllib,urllib2
import sys,os


def send_mail(sub,to,content):
    task_info = {
            "key":"ece173174cb52dcac9120c2aa2d85fe6" , 
            "type":"email" ,
            "from":"domain" ,
            "to": "%s" % to ,
            "param":{} ,
#           "cc":"ops@dnspod.com"  ,
            "layout":"17687da88fced2c7442f18dc1a2a64de" ,
            "template":"" ,
            "subject":"%s" % sub ,
            "content":"%s" % content 
                }
    data = json.dumps(task_info)
    url = 'https://ec.dnspod.cn/apis/sends'
    domain_scan = urllib.urlopen(url, data)
    print domain_scan.read()
    domain_scan.close()

def send_weixin_table(content):
    task_info = {
            "key":"8b7210460396c35100e6677c94bd32b7" ,
            "type":"dweixin" ,
            "from":"dweixin" ,
            "to":"rfyiamcool" ,
            "content":content ,
            "content_type":"table"
    }
    data = json.dumps(task_info)
    url = 'https://ec.dnspod.cn/apis/events'
    domain_scan = urllib.urlopen(url, data)
    print domain_scan.read()
    domain_scan.close

def send_weixin(content):
    task_info = {
            "key":"8b7210460396c35100e6677c94bd32b7" ,
            "type":"dweixin" ,
            "from":"dweixin" ,
            "to":"p_owenrui" ,
            "content":content ,
    }
    data = json.dumps(task_info)
    url = 'https://ec.dnspod.cn/apis/sends'
    domain_scan = urllib.urlopen(url, data)
    print domain_scan.read()
    domain_scan.close


aa=sys.argv[1]

if __name__ == "__main__":
      print send_mail('邮件告警','owenrui@dnspod.com',aa)
#     aaa = {"header":["a","b","c","d"],"data1":["1","2","3","4"]}
#     aaa = {"header":["a","b","c","d"]}
#     bbb = json.string(aaa)
#      print send_weixin(aa)
