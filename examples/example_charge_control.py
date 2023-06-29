#!/usr/bin/env python3

# example for using bic2200.py
# Version 0.4
import sys
import time
import schedule
import json
import subprocess
import requests
import datetime
import configparser

from func_timeout import func_timeout, FunctionTimedOut

# Safe values for voltages and currents limiting to high oder low values in the config file
SafeChargeVoltage = 2790
SafeDischargeVoltage = 2520
SafeChargeCurrent = 2600
SafeDischargeCurrent = 2600

config = configparser.ConfigParser()

# First init Values from Config File
config.read('./charge_control.conf')
ChargeVoltage = int(config.get('Settings', 'ChargeVoltage'))
DischargeVoltage = int(config.get('Settings', 'DischargeVoltage'))
MaxChargeCurrent = int(config.get('Settings', 'MaxChargeCurrent'))
MaxDischargeCurrent = int(config.get('Settings', 'MaxDischargeCurrent'))



# Init CAN Bus
p = subprocess.run(["./bic2200.py" , "can_up"])

# Write Charge / Discharge Voltages
if ChargeVoltage > SafeChargeVoltage:
    ChargeVoltage = SafeChargeVoltage

if DischargeVoltage < SafeDischargeVoltage:
    DischargeVoltage = SafeDischargeVoltage
    
p = subprocess.run(["./bic2200.py", "cvset", str(ChargeVoltage)])
p = subprocess.run(["./bic2200.py", "dvset", str(DischargeVoltage)])

def control_power():

    #-------------------------------------------------------------- Read Config and Check Values
    config.read('./charge_control.conf')
    ChargeVoltage = int(config.get('Settings', 'ChargeVoltage'))
    DischargeVoltage = int(config.get('Settings', 'DischargeVoltage'))
    MaxChargeCurrent = int(config.get('Settings', 'MaxChargeCurrent'))
    MaxDischargeCurrent = int(config.get('Settings', 'MaxDischargeCurrent'))

    if MaxChargeCurrent > SafeChargeCurrent:
        MaxChargeCurrent = SafeChargeCurrent
        print ("Charge Current too big")

    if MaxDischargeCurrent > SafeDischargeCurrent:
        MaxDischargeCurrent = SafeDischargeCurrent
        print ("Discharge Current too big")            
    

    #-------------------------------------------------------------- Read Power Meter
    # print ("Control Charge/Discharge")

    stromzaehler = requests.get("http:// --your power meter IP-- /cm?cmnd=status%2010")
    stromz = stromzaehler.json()
    stromz1 = (stromz['StatusSNS'])
    # zeit = (stromz1['Time'])
    stromz2 = (stromz1['Haus'])
    Power = (stromz2['Power'])
    
    zeit = datetime.datetime.now()
    print (str(zeit) + ": Power: " + str(Power) + " W")

    if Power > 20000:
        Power = 20000

    #-------------------------------------------------------------- Read BIC-2200
    volt = subprocess.run(["./bic2200.py", "vread"], capture_output=True, text=True)
    volt_now = float(volt.stdout)
    amp = subprocess.run(["./bic2200.py", "cread"], capture_output=True, text=True)
    amp_now = float(amp.stdout)
    print ("BIC-2200 Volt: ", volt_now/100," Ampere: ", amp_now/100)
    
    #-------------------------------------------------------------- Charge / Discharge

    DiffCurrent = Power*10000/volt_now*(-1)
    Current = DiffCurrent + amp_now
    print ("Calc_Current: ", Current/100)

    if Current > 0:
        IntCurrent = int(Current)

        if IntCurrent >= MaxChargeCurrent:
            IntCurrent = MaxChargeCurrent
            

        p = subprocess.run(["./bic2200.py" , "charge"])
        c = subprocess.run(["./bic2200.py" , "ccset" ,  str(IntCurrent)]) 

    if Current < -10: 
        IntCurrent = int(Current*(-1)) 

        if IntCurrent >= MaxDischargeCurrent:
            IntCurrent = MaxDischargeCurrent  
        
        

        p = subprocess.run(["./bic2200.py" , "discharge"])
        c = subprocess.run(["./bic2200.py" , "dcset", str(IntCurrent)]) 

    

    # ---------------------------------------------------------------------------Logging 
    logfile = open('./battery.log','a')
    logfile.write(str(zeit) + ": PowerMeter:" + str(Power) + ":W: Battery_V:" + str(volt_now/100) + ":V: Battery_I:" + str(amp_now/100) + ":A: I Calc:" + str(Current/100)+":A \n")
    logfile.close()



schedule.every(3).seconds.do(control_power)      # Aufruf der Regelroutine ca alle 3s

while True:
     schedule.run_pending()
     #time.sleep(1)


