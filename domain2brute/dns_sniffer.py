#!/usr/bin/python
# coding=utf-8

import os
import datetime
import time
import random
import string
from scapy.all import *

# 定义空的 IP 地址列表
ip_list = {}
quiet = False

def random_string(length):
    # 生成可供选择的字符集合
    chars = string.ascii_letters + string.digits
    # 生成指定长度的随机字符串
    return ''.join(random.choice(chars) for _ in range(length))

# 定义 DNS 响应解析回调函数
def dns_callback(packet):
    if packet.haslayer(DNS) and packet.getlayer(DNS).qr == 1:
        # 只处理 DNS 响应数据包
        dns = packet.getlayer(DNS)
        #获取A、AAA、CNAME
        if dns.an and (dns.an.type == 1 or dns.an.type == 28 or dns.an.type == 5):
            try:
                pcap_file = '/u2/workdir/dnspkt/%s.pcap' % random_string(16)
                wrpcap(pcap_file, packet, append=True)
            except:
                print(traceback.print_exc())
            
if __name__ == "__main__":    
    try:
        os.mkdirs('/u2/workdir/dnspkt')
    except:
        pass
    
    # 在指定的网卡上监听 DNS 请求并解析响应
    sniff(filter="udp port 53", prn=dns_callback, iface='eth0')
