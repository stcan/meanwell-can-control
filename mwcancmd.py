#!/usr/bin/env python3

# mwcancmd.py
# Controlling the MeanWell BIC-2200 and NPB-abc0
# tested only with the 24V Version BIC-2200 and NPB-1200
# Please note:  this software to control the Meanwell CAN devices is not yet complete 
# and also not fully tested. The device should not be operated unattended. 
# There is no error handling yet !!!

# What is missing:
# - code for programming BIC2200 mode settings
# - error handling
# - variables plausibility check
# - programming missing functions 
# - current and voltage maximum settings

# steve 08.06.2023  Version 0.2.1
# steve 10.06.2023  Version 0.2.2
# macGH 15.06.2023  Version 0.2.3
#       - support for Meanwell NPB-x Charger
#       - new config area   
# steve 16.06.2023  Version 0.2.4
#       - fault and status queries    
# macGH 18.06.2023  Changed to mwcan.py class

import os
import can
import sys
import signal
import atexit
from mwcan import *


def on_exit():
    print("CLEAN UP ...")
    candev.can_down()
    
def handle_exit(signum, frame):
    sys.exit(0)

def mwcan_commands():
    print("")
    print(" " + sys.argv[0] + " - controlling the Meanwell CAN devices BIC-2200 Power Supply and NPB-abc0 Charger")
    print("")
    print(" Usage:")
    print("        " + sys.argv[0] + " parameter and <value>")
    print("")
    print("       on                   -- output on")
    print("       off                  -- output off")
    print("")
    print("       cvread               -- read charge voltage setting")
    print("       cvset <value>        -- set charge voltage")
    print("       ccread               -- read charge current setting")
    print("       ccset <value>        -- set charge current")
    print("")
    print("       dvread               -- read discharge voltage setting")
    print("       dvset <value>        -- set discharge voltage")
    print("       dcread               -- read discharge current setting")
    print("       dcset <value>        -- set discharge current")
    print("")
    print("       vread                -- read DC voltage")
    print("       cread                -- read DC current")
    print("       acvread              -- read AC voltage")
    print("")
    print("       charge               -- set direction charge battery")
    print("       discharge            -- set direction discharge battery")
    print("")
    print("       tempread             -- read power supply temperature")
    print("       typeread             -- read power supply type")
    print("       statusread           -- read power supply status")
    print("       faultread            -- read power supply fault status")    
    print("       can_up               -- start can bus")
    print("       can_down             -- shut can bus down")
    print("")
    print("       <value> = amps oder volts * 100 --> 25,66V = 2566")
    print("")
    print("       Version 0.2.5 ")


#########################################
# Operation function

def operation(val):#0=off, 1=on
    print ("turn output on")
    v = candev.operation(1,val)
    print(v)
    return v

def charge_voltage(rw,val=0xFFFF): #0=read, 1=set
    # print ("read/set charge voltage")
    # Command Code 0x0020
    # Read Charge Voltage
    v = candev.v_out_set(rw,val)
    print(v)
    return v

def charge_current(rw,val=0xFFFF): #0=read, 1=set
    # print ("read/set charge current")
    # Command Code 0x0030
    # Read Charge Voltage
    v = candev.i_out_set(rw,val)
    print_(v)
    return v

def discharge_voltage(rw,val=0xFFFF): #0=read, 1=set
    # print ("read/set discharge voltage")
    # Command Code 0x0120
    # Read Charge Voltage
    v = candev.BIC_discharge_v(rw,val)
    print(v)
    return v

def discharge_current(rw,val=0xFFFF): #0=read, 1=set
    # print ("read/set charge current")
    # Command Code 0x0130
    # Read Charge Voltage
    v = candev.BIC_discharge_i(rw,val)
    print(v)
    return v

def vread():
    # print ("read dc voltage")
    # Command Code 0x0060
    # Read DC Voltage
    v = candev.v_out_read()
    print(v)
    return v

def cread():
    # print ("read dc current")
    # Command Code 0x0061
    # Read DC Current
    v = candev.i_out_read()
    print(v)
    return v

def acvread():
    # print ("read ac voltage")
    # Command Code 0x0050
    # Read AC Voltage
    v = candev.v_in_read()
    print(v)
    return v

def BIC_chargemode(val): #0=charge, 1=discharge
    # print ("set direction charge")
    # Command Code 0x0100
    # Set Direction Charge
    v = candev.BIC_chargemode()
    print(v)
    return v

def NPB_chargemode(rw, val=0xFF):
    # print ("Set PSU or Charger Mode to NPB Device")
    # Command Code 0x00B4
    v = candev.NPB_curve_config(1,CURVE_CONFIG_CUVE,val) #Bit 7 should be 0
    print(v)
    return v

def typeread():
    # print ("read power supply type")
    # Command Code 0x0082
    # Command Code 0x0083
    # Read Type of PSU
    v = candev.type_read()
    print(v)
    return v

def tempread():
    # print ("read power supply temperature")
    # Command Code 0x0062
    # Read AC Voltage
    v = candev.temp_read()
    print(v)
    return v

def statusread():
    # print ("Read System Status")
    # Command Code 0x00C1
    # Read System Status
    
    v = candev.system_status()
    candev.decode_system_status(v)
    return v
        
def faultread():
    # print ("Read System Fault Status")
    # Command Code 0x0040
    # Read System Fault Status
    
    v = candev.system_status() 
    candev.decode_system_status(v)
    return v

def command_line_argument():
    if len (sys.argv) == 1:
        print ("")
        print ("Error: First command line argument missing.")
        mwcan_commands()
        error = 1
        return
    
    if   sys.argv[1] in ['on']:        operation(1)
    elif sys.argv[1] in ['off']:       operation(2)
    elif sys.argv[1] in ['cvread']:    charge_voltage(0)
    elif sys.argv[1] in ['cvset']:     charge_voltage(1)
    elif sys.argv[1] in ['ccread']:    charge_current(0)
    elif sys.argv[1] in ['ccset']:     charge_current(1)
    elif sys.argv[1] in ['dvread']:    discharge_voltage(0)
    elif sys.argv[1] in ['dvset']:     discharge_voltage(1)
    elif sys.argv[1] in ['dcread']:    discharge_current(0)
    elif sys.argv[1] in ['dcset']:     discharge_current(1)
    elif sys.argv[1] in ['vread']:     vread()
    elif sys.argv[1] in ['cread']:     cread()
    elif sys.argv[1] in ['acvread']:   acvread()
    elif sys.argv[1] in ['charge']:    BIC_chargemode(0)
    elif sys.argv[1] in ['discharge']: BIC_chargemode(1)
    elif sys.argv[1] in ['tempread']:  tempread()
    elif sys.argv[1] in ['typeread']:  typeread()
    elif sys.argv[1] in ['statusread']:statusread()
    elif sys.argv[1] in ['faultread']: faultread()
    elif sys.argv[1] in ['NPB_chargemode']: NPB_chargemode(int(sys.argv[2]))
    else:
        print("")
        print("Unknown first argument '" + sys.argv[1] + "'")
        mwcan_commands()
        error = 1
        return

#### Main 
atexit.register(on_exit)
signal.signal(signal.SIGTERM, handle_exit)
signal.signal(signal.SIGINT, handle_exit)

#CAN INIT
#RS232 usage
candev = mwcan(1,"03",1,"/dev/ttyACM0",0)
#CAN0 usage
#candev = mwcan(0,"03",0,"",1)
candev.can_up()

command_line_argument()

sys.exit(0)
