#!/usr/bin/python
# coding=utf-8

import os
import datetime
import time
import random
import string
import geoip2.database
from scapy.all import *
import json
import datetime
import pytz

# 定义空的 IP 地址列表
ip_list = {}
quiet = False
geo_reader = None
asn_reader = None

# 定义 DNS 响应解析回调函数
def dns_process(packet):
    if packet.haslayer(DNS) and packet.getlayer(DNS).qr == 1:
        # 只处理 DNS 响应数据包
        dns_layer = packet.getlayer(DNS)
        master_domain = ""
        cname = ""
        
        for i in range(dns_layer.ancount):
            json_dict = {}
        
            an = dns_layer.an[i]
        
            #CNAME
            if an and an.type == 5:
                master_domain = dns_layer.qd.qname.decode('utf-8')
                cname         = an.rdata.decode('utf-8')
                
                if master_domain.endswith('.'):
                    master_domain = master_domain.rstrip('.')
                    
                if cname.endswith('.'):
                    cname = cname.rstrip('.')
                
            #A、AAA
            if an and an.type == 1 or an and an.type == 28:
                # 获取解析后的 IP 地址
                response_asn = None
                response_geo = None
                response_asn = None
                response_geo = None
                asn_num = ""
                asn_organization = ""
                country_code = ""
                country_name = ""
                city_name = ""
                
                ip   = an.rdata
                name = dns_layer.qd.qname.decode('utf-8')
            
                if name.endswith('.'):
                    name = name.rstrip('.')
            
                try:
                    response_asn = asn_reader.asn(ip)
                    response_geo = geo_reader.city(ip)
                except:
                    pass
                
                try:
                    if response_asn != None and response_asn.autonomous_system_number != None:
                        asn_num = response_asn.autonomous_system_number
                    if response_asn != None and response_asn.autonomous_system_organization != None:
                        asn_organization = response_asn.autonomous_system_organization
                    if response_geo != None and response_geo.country.iso_code != None:
                        country_code = response_geo.country.iso_code
                    if country_code == 'TW' or country_code == 'HK':
                        country_code = 'CN'
                    if response_geo != None and response_geo.country.name != None:
                        country_name = response_geo.country.name
                    if response_geo != None and response_geo.city.name != None:
                        city_name = response_geo.city.name
                except:
                    pass
                
                if len(master_domain) > 0:
                    json_dict['domain'] = master_domain
                    json_dict['cname']  = cname
                else:
                    json_dict['domain'] = name
                    json_dict['cname']  = ""
                
                
                json_dict['address'] = ip
                json_dict['asn_num'] = asn_num
                json_dict['asn_organization'] = asn_organization
                json_dict['country_code'] = country_code
                json_dict['country_name'] = country_name
                json_dict['city_name'] = city_name
            
                # _index = "base_social_user_domain_addr"
                _json_str = json.dumps(json_dict)
                data      = "%s\n" % (_json_str)
            
                # 获取当前时间
                now = datetime.datetime.now()

                # 设置东八区时区
                tz = pytz.timezone('Asia/Shanghai')
                now = now.astimezone(tz)

                # 格式化时间
                hour = now.strftime("%Y-%m-%d-%H")
                json_path = '%s/subdomain%s.json' % ('/zrtx/log/cyberspace', hour)
                with open(json_path, 'a') as f:
                    f.write(data)
            
                print(f"{dns_layer.qd.qname.decode('utf-8')}: {ip}")


def decode_loop_pkt(file_dir):
    try:
        for root,dirs,files in os.walk(file_dir):
            for file2 in files:
                path = os.path.join(root, file2)
                
                try:
                    packets = rdpcap(path)
                    for packet in packets:
                        dns_process(packet)
                except:
                    print(path)
                    print(traceback.print_exc())
                
                try:
                    os.remove(path)
                except:
                    print(traceback.print_exc())
    except:
        print(traceback.print_exc())

if __name__ == "__main__":    
        
    file_dir = '/u2/workdir/dnspkt'

    try:
        geo_reader = geoip2.database.Reader('/u4/domain/GeoLite2-City.mmdb')
        asn_reader = geoip2.database.Reader('/u4/domain/GeoLite2-ASN.mmdb')
    except:
        print(traceback.print_exc())

    while True:
        decode_loop_pkt(file_dir)
        time.sleep(3)
    
