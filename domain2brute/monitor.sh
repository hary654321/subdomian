#!/bin/bash

while true
do
	pid=`ps -ef | grep -v grep | grep 'dns2brute.py' | sed -n '1P' | awk '{print $2}'`
    if [ -z $pid ];then
		echo "start dns2brute.py"
    	cd /usr/local/domain2brute && python3 /usr/local/domain2brute/dns2brute.py >/dev/null 2>&1 &
    fi
	
	pid=`ps -ef | grep -v grep | grep 'dns_sniffer.py' | sed -n '1P' | awk '{print $2}'`
    if [ -z $pid ];then
		echo "start dns_sniffer.py"
    	cd /usr/local/domain2brute && python3 /usr/local/domain2brute/dns_sniffer.py >/dev/null 2>&1 &
    fi
	
	pid=`ps -ef | grep -v grep | grep 'dns_process.py' | sed -n '1P' | awk '{print $2}'`
    if [ -z $pid ];then
		echo "start dns_process.py"
    	cd /usr/local/domain2brute && python3 /usr/local/domain2brute/dns_process.py >/dev/null 2>&1 &
    fi

    sleep 3
    
done
