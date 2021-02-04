#!/bin/bash
#sh copy_files.sh 11
sh copy_files.sh 13
#sshpass -p '123456' ssh root@192.168.137.11 ifconfig wlan0 up
sshpass -p '123456' ssh root@192.168.137.13 ifconfig wlan0 up
#sshpass -p '123456' ssh root@192.168.137.11 python wil6210_server 8000 &
PID_1=$!
sshpass -p '123456' ssh root@192.168.137.13 python wil6210_server 8000 &
PID_2=$!
read
echo "killing ssh"
kill -9 $PID_1
kill -9 $PID_2
