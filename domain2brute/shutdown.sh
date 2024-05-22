#!/bin/sh

p1=`ps -ef | grep -v grep | grep 'monitor.sh' | sed -n '1P' | awk '{print $2}'`
if [ ! -z $p1 ];then
	kill -9 $p1
	echo "monitor.sh stopped"
fi

pid=`ps -ef | grep -v grep | grep 'dns2brute' | sed -n '1P' | awk '{print $2}'`
if [ ! -z $pid ];then
	kill -9 $pid
	echo "dns2brute stopped"
fi

pid=`ps -ef | grep -v grep | grep 'dns_process' | sed -n '1P' | awk '{print $2}'`
if [ ! -z $pid ];then
	kill -9 $pid
	echo "dns_process stopped"
fi

pid=`ps -ef | grep -v grep | grep 'dns_sniffer' | sed -n '1P' | awk '{print $2}'`
if [ ! -z $pid ];then
	kill -9 $pid
	echo "dns_sniffer stopped"
fi

exit 0
