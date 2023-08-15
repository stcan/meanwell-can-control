#!/usr/bin/bash

timestamp1=$(date -r /home/pi/bin/battery.log)
sleep 15
timestamp2=$(date -r /home/pi/bin/battery.log)

if [ "$timestamp1" = "$timestamp2" ]; 
   then
   #echo "script steht"
   pid=$(ps -ax | grep charge_control.py | grep -v grep | awk '{print $1}')
   # echo $pid
   if [ -n "$pid" ] 
      then
      kill $pid
      sleep 5
      # echo "charge_control kill"
   fi
      
   cd /home/pi/bin
   ./charge_control.py 

   dati=$(date +%Y-%m-%d_%H:%M:%S) 
   echo $dati" charge_control neu gestartet" >> /home/pi/bin/process.log

fi
