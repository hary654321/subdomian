#!/usr/bin/python
# coding=utf-8

import requests
import traceback
import logging
import signal
import time
import sys
import os
import json
import socket
import datetime
import logging
import geoip2.database
from dns.resolver import Resolver
from scapy.all import *

json_all_list = []
geo_reader = None
asn_reader = None
json_map   = {}
resolver   = None
iface_name = 'eth0'
iface_ip   = ""
dns_dict   = {}

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_dict():
    try:
        with open('/usr/local/domain2brute/top100.txt') as file:
            for line in file:
                line = line.strip()
                line = line.rstrip('\r')
                line = line.rstrip('\n')
                
                dns_dict[line] = line
    except:
        print(traceback.print_exc())

def do_with_file(path):
    try:
        with open(path) as file:
            for line in file:
                line = line.strip()
                line = line.rstrip('\r')
                line = line.rstrip('\n')
                                
                for key,value in dns_dict.items():
                    domain = key + '.' + line
                    json_map[domain] = 0
                
    except:
        print(traceback.print_exc())
            
if __name__ == '__main__':
    
    try:
        load_dict()
        iface_ip = get_if_addr(iface_name)
    except:
        pass
    
    while True:
        try:
            for root,dirs,files in os.walk('/u4/dns'):
                for file2 in files:
                    json_map.clear()
                    path = os.path.join(root, file2)                    
                    do_with_file(path)
                    
                    line_count = 0
                
                    logging.info('path: %s, start ...', path)
                
                    for domain,value in json_map.items():
                        #logging.info('domain = %s, line_count = %d, start ...', domain, line_count)
                        try:
                            line_count += 1
                            query = IP(src=iface_ip, dst='8.8.8.8')/UDP(sport=RandShort(), dport=53)/DNS(rd=1, qd=DNSQR(qname=domain))
                            try:
                                send(query, verbose=False, iface=iface_name)
                            except:
                                pass
                        except:
                            print(traceback.print_exc())
                
                        #logging.info('domain = %s, end ...', domain)
                    
                    logging.info('path: %s, end ...', path)
                    
                    try:
                        os.remove(path)
                    except:
                        pass
        except:
            print(traceback.print_exc())
        
        time.sleep(3)
    


