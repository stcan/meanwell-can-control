#!/usr/bin/env python3

# example for using bic2200.py

import time
import schedule
import json
import subprocess
import requests
import datetime

from func_timeout import func_timeout, FunctionTimedOut


ChargeVoltage = 2760
DischargeVoltage = 2570
MaxChargeCurrent = 2500
MaxDischargeCurrent = 2500

# Init CAN Bus
p = subprocess.run(["./bic2200.py" , "can_up"])

# Write Charge / Discharge Voltages
p = subprocess.run(["./bic2200.py", "cvset", str(ChargeVoltage)])
p = subprocess.run(["./bic2200.py", "dvset", str(DischargeVoltage)])

def control_power():

    #-------------------------------------------------------------- Read Power Meter
    # print ("Control Charge/Discharge")

    stromzaehler = requests.get("http://stromzaehler.fritz.box/cm?cmnd=status%2010")
    stromz = stromzaehler.json()
    stromz1 = (stromz['StatusSNS'])
    # zeit = (stromz1['Time'])
    stromz2 = (stromz1['Haus'])
    Power = (stromz2['Power'])
    
    zeit = datetime.datetime.now()
    print (str(zeit) + ": Power: " + str(Power) + " W")

    #-------------------------------------------------------------- Read BIC-2200
    
    v  = subprocess.run(["./bic2200.py", "vread"], capture_output=True, text=True)
    v_now = float(v.stdout)
    a  = subprocess.run(["./bic2200.py", "cread"], capture_output=True, text=True)
    a_now = float(a.stdout)
    print ("BIC-2200 Volt: ", v_now/100," Ampere: ", a_now/100)
    
    #-------------------------------------------------------------- Charge / Discharge

    DiffCurrent = Power*10000/v_now*(-1)
    Current = DiffCurrent + a_now
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
    logfile.write(str(zeit) + ": PowerMeter:" + str(Power) + ":W: Battery_V:" + str(v_now/100) + ":V: Battery_I:" + str(a_now/100) + ":A: I Calc:" + str(Current/100)+":A \n")
    logfile.close()





schedule.every(4).seconds.do(control_power)      # Start every 5s

while True:
     schedule.run_pending()

