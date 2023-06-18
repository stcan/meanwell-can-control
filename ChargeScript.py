#!/usr/bin/env python3

# Script for charging with Meanwell NPB-abc0 or BIC-2200
# Not suitable for productive use. 
# Use for demo purposes only!

import os
import sys
import time
from time import sleep
import json
import requests
import datetime
import paho.mqtt.client as mqtt
import signal
import atexit
import schedule
from mwcan import *

#Select Meanwell Device
# 0 = BIC2200
# 1 = NPB
Selected_Device = 1
#MaxID of MW Device supported !
MaxDevSupport = 1
#If you want to stop the charger is connection to meter is lost 
#to prevent overcharge or costs
StopOnConnectionLost = True

#select the charge option
# 0 = mqtt - get the WATT value from mqtt Server (e.g. iobroker)
# 1 = http - get WATT value from webserver (e.g. ESP32 with Tasmota)
GetPowerOption  = 0
#MaxID of posibilities to get used Power from meter
MaxGetPowerSupport = 1

#Select the method to control the charger / discharger
# see "def process_power(val)" --> below
# you can use the already implemneted or implement your own
PowerControlmethod = 1

#which http request should be used
# 0 = Tasmota Json
http_get_option = 0
http_ip_address = "192.168.2.20" #incl port :8080 if necessary

#http Request option
# after x seconds get new power value
http_schedule_time = 4

#mqtt settings
# 
mqttserver= "192.168.2.8"
mqttport  = 1883
mqttuser  = "mqtt"
mqttpass  = "mqtt"
#IMPORTANT
#The subscription topic must have the power in WATT (+ and -) 
#positiv = from Grid, negative = from Solar/Battery to Grid
mqttsubcribe ="smartmeter/0/1-0:16_7_0__255/value"

#mqttPublish charge voltage and current --> not implmented yet
mqttpublish        = 0
LastChargerCurrent = 0

#Support external discharger
# 0 = disabled
externel_discharger = 0

#Charge option
FixedChargeVoltage  = 2760  #Volt *100    --> 27,6V * 100 = 2760 (e.g. 24V with 8x3,45 = 27,6V 
MinDischargeVoltage = 2570  #Volt *100
MaxChargeCurrent    = 2500  #Current *100 --> 25,0A * 100 = 2500
MinChargeCurrent    =  760  #Current *100
MaxDischargeCurrent = 2500  #Current *100
LastChargerSet      = 0     #Check if we charge / discharge or do nothing
LastChargerCurrent  = 0     #Last Current set to charger to avoid change if not necessary
           

#    status = mqttclient.publish('kwb/temperture/outside', payload=mqttOutsidevalue, qos=1, retain=True)
#    if status.rc == 0:
#         print('Send via mqtt %i',mqttOutsidevalue)
#     else:
#         print('Error sending to mqtt Server')
#
#	except:
#          print('ERROR during mqtt send')
#

def on_exit():
    print("CLEAN UP ...")
    if GetPowerOption==0:
        mqttclient.unsubscribe(mqttsubcribe)
        mqttclient.loop_stop()
        mqttclient.disconnect()

    StartStopOperation(0)
    candev.can_down()
    
def handle_exit(signum, frame):
    sys.exit(0)


#####################################################################
#Setup Operation mode of charger
def StartStopOperation(startstop):
    global OperationStatus
    
    if startstop == 0:
        if OperationStatus != 0:
            candev.operation(1,0)
            OperationStatus = 0   
            print("Change operation mode to: OFF")
        else:
            print("Operation mode already OFF")
    else:
        if OperationStatus != 1:
            candev.operation(1,1)   
            OperationStatus = 1   
            print("Change operation mode to: ON")
        else:
            print("Operation mode already ON")
    return startstop


#####################################################################
#Setup Charge / Discharge here depending of Power
def process_power(val):
    global LastChargerSet
    global LastChargerCurrent
    print("Current Power usage: ", val)

    if PowerControlmethod == 0:
        #Method 0
        print("Method 0")
        StartStopOperation(1)
        zeit = datetime.datetime.now()
        print (str(zeit) + ": Power: " + str(val) + " W")
    
        #-------------------------------------------------------------- Read BIC-2200
    
        vout  = candev.v_out_read() #subprocess.run(["./bic2200.py", "vread"], capture_output=True, text=True)
        iout  = candev.i_out_read() #subprocess.run(["./bic2200.py", "cread"], capture_output=True, text=True)
        print ("BIC-2200 Volt: ", vout/100," Ampere: ", iout/100)
    
        #-------------------------------------------------------------- Charge / Discharge
    
        DiffCurrent = Power*10000/vout*(-1)
        Current = DiffCurrent + iout
        print ("Calc_Current: ", Current/100)
    
        if Current > 0:
            IntCurrent = int(Current)
    
            if IntCurrent >= MaxChargeCurrent:
                IntCurrent = MaxChargeCurrent 
    
            p = candev.BIC_chargemode(1)       # subprocess.run(["./bic2200.py" , "charge"])
            c = candev.i_out_set(1,IntCurrent) # subprocess.run(["./bic2200.py" , "ccset" ,  str(IntCurrent)])
    
        if Current < -10: 
            IntCurrent = int(Current*(-1)) 
    
            if IntCurrent >= MaxDischargeCurrent:
                IntCurrent = MaxDischargeCurrent  
    
            p = candev.BIC_chargemode(0)            #subprocess.run(["./bic2200.py" , "discharge"])
            c = candev.BIC_discharf_i(1,IntCurrent) # subprocess.run(["./bic2200.py" , "dcset", str(IntCurrent)]) 

        LastChargerCurrent = IntCurrent  
        print(str(zeit) + ": PowerMeter:" + str(val) + ":W: Battery_V:" + str(vout/100) + ":V: Battery_I:" + str(iout/100) + ":A: I Calc:" + str(Current/100)+":A \n")

    #Method 1
    if PowerControlmethod == 1:
        LastChargerCurrent = 0  
    #Method 2
    if PowerControlmethod == 2:
        LastChargerCurrent = 0  

#        if LastChargerSet == 0:
#            LastChargerCurrent = 99
#            #enable charger
#    else:
#        if LastChargerCurrent > 0:
#            LastChargerCurrent = 100
#            #disable charger
    
    return val


#####################################################################
# http request
def http_request():
    #--------- Read Power Meter via http
    try:
        if http_get_option == 0:
            powermeter = requests.get("http://" + http_ip_address + "/cm?cmnd=status%2010")
            powerz     = powermeter.json()
            powerz1    = (powerz['StatusSNS'])
            powerz2    = (powerz1['Haus'])
            power      = (powerz2['Power'])
        if http_get_option == 1:
            print("option2")
        
    except Exception as e:
        print("HTTP CONNECTION ERROR")
        #Stop Operation if setting set
        if StopOnConnectionLost:
            StartStopOperation(0)
        return
            
    print (str(zeit) + ": Power: " + str(power) + " W")
    process_power(int(power))

#####################################################################
# mqtt
def mqtt_on_connect(client, userdata, flags, rc):
    print("Connected with mqttserver, Subscribe to topic")
    mqttclient.subscribe(mqttsubcribe,qos=1)

def mqtt_on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected disconnect with mqttserver")
        if StopOnConnectionLost:
            StartStopOperation(0)  

def mqtt_on_message(client, userdata, message):
    val = str(message.payload.decode("utf-8"))
    #print("message received ", val)
    #print("message topic=",message.topic)
    #print("message qos=",message.qos)
    #print("message retain flag=",message.retain)
    process_power(round(int(val)))

def mqtt_on_subscribe(client, userdata, mid, granted_qos):
    print("Qos granted: " + str(granted_qos))

#####################################################################
#                  *** Main ***
#####################################################################
atexit.register(on_exit)
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)
global OperationStatus

#CAN INIT

candev = mwcan(1,"03",1,"/dev/ttyACM0",0)
candev.can_up()

#Get Type of device
print(candev.manu_read())
print(candev.type_read())
#print(candev.serial_read())
print(str(candev.temp_read()/10) + " C")
print(str(candev.v_in_read()/10) + " V")

#Set main parameter and stop device
print("Operation STOP: " + str(candev.operation(1,0)))
OperationStatus = 0
print("SET CHARGE VOLTAGE: " + str(candev.v_out_set(1,FixedChargeVoltage)))

if Selected_Device > MaxDevSupport:
    print("DEVICE NOT SUPPORTED NOW")
    sys.exit(1)

if GetPowerOption > MaxGetPowerSupport:
    print("GET POWER OPTION NOT SUPPORTED NOW")
    sys.exit(1)

if Selected_Device==0:
    #setup Bic2200
    #set to charge mode first
    candev.BIC_chargemode(0)
    #set Min Discharge voltage
    candev.BIC_discharge_v(1,MinDischargeVoltage)

if Selected_Device==1:
    #setup NPB
    cuve = candev.NPB_curve_config(0,0,0) #Bit 7 should be 0
    if is_bit(cuve,CURVE_CONFIG_CUVE):    #Bit 7 is 1 --> Charger Mode
        print("NOT IN PSU MODE ! STOP ! PLEASE SET TO PSU MODE !!!")
        sys.exit(1) 
    candev.i_out_set(1,MinChargeCurrent)

if GetPowerOption==0:
    #init mqtt
    global mqttclient
    
    mqttclient = mqtt.Client()
    mqttclient.on_connect    = mqtt_on_connect
    mqttclient.on_disconnect = mqtt_on_disconnect
    mqttclient.on_message    = mqtt_on_message
    mqttclient.on_subscribe  = mqtt_on_subscribe

    mqttclient.username_pw_set(mqttuser, mqttpass)
    mqttclient.connect(mqttserver, mqttport, 20)
    mqttclient.loop_start()

    #mqttclient.publish('MWCharger/CurrentSettings/Chargecurrent', payload=0, qos=0, retain=false)
    #mqttclient.publish('MWCharger/CurrentSettings/Chargevoltage', payload=0, qos=0, retain=false)
    #mqttclient.publish('MWCharger/CurrentSettings/ChargeDirection', payload=1, qos=0, retain=false)

if GetPowerOption==1:
    schedule.every(http_schedule_time).seconds.do(http_request)      # Start every Xs

while True:
    if GetPowerOption==1:
        schedule.run_pending()
    pass
