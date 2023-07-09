#!/usr/bin/env python3

# bic2200.py
# Controlling the Mean Well BIC-2200-CAN
# tested only with the 24V Version BIC-2200-CAN-24
# Please note:  this software to control the BIC-2200 is not yet complete 
# and also not fully tested. The BIC-2200 should not be operated unattended. 
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
# steve 19.06.2023  Version 0.2.4
#       - fault queries completed  

import os
import can
import sys
import time

error = 0

#########################
# MAIN CONFIG
#########################

#########################
#ID = Cortroller Message ID + Device ID [00-07]
#Be sure you select the right CAN_ADR and add your Device-ID (Jumper block)
#BIC-2200 00 - 07, NPB 00 - 03  
#
#BIC-2200
CAN_ADR = 0x000C0300
#
#NPB-1200
#CAN_ADR = 0x000C0103
#########################

#########################
#If you use a RS232 to CAN Adapter which ich socketCAN compartible, switch to 1
#e.g. USB-Tin www.fischl.de
#Add the rigth /dev/tty device here 
USE_RS232_CAN = 0
CAN_DEVICE = '/dev/ttyACM0'
#########################

def bic22_commands():
    print("")
    print(" " + sys.argv[0] + " - controlling the BIC-2200-CAN Bidirectional Power Supply")
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
    print("       init_mode            -- init BIC-2200 bi-directional battery mode")
    print("")
    print("       <value> = amps oder volts * 100 --> 25,66V = 2566")
    print("")
    print("       Version 0.2.4 ")

#########################################
# gereral function
def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)
    
#########################################
# receive function
def can_receive():
    msgr = str(can0.recv(0.5))
    msgr_split = msgr.split()
    hexval = (msgr_split[11]+ msgr_split[10])
    print (int(hexval,16))
    
    if msgr is None:
        print('Timeout occurred, no message.')
    return hexval

def can_receive_char():
    msgr = str(can0.recv(0.5))
    msgr_split = msgr.split()
    s = bytearray.fromhex(msgr_split[10]+msgr_split[11]+msgr_split[12]+msgr_split[13]+msgr_split[14]+msgr_split[15]).decode()
    #print(s)
    if msgr is None:
        print('Timeout occurred, no message.')
    return s

#########################################
# CAN function
def can_up():
    if USE_RS232_CAN == 0:
        os.system('sudo ip link set can0 up type can bitrate 250000')
        os.system('sudo ifconfig can0 txqueuelen 65536')
    else:
        os.system('sudo slcand -f -s5 -c -o ' + CAN_DEVICE)
        os.system('sudo ip link set up can0')
    
def can_down():
    os.system('sudo ip link set can0 down')

#########################################
# Operation function

def operation(val):#0=off, 1=on
    # print ("turn output on/off")
    # Command Code 0x0000
    commandhighbyte = 0x00
    commandlowbyte = 0x00
 
    msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte, commandhighbyte,val], is_extended_id=True)
    can0.send(msg)
    return val



def charge_voltage(rw,val=0xFFFF): #0=read, 1=set
    # print ("read/set charge voltage")
    # Command Code 0x0020
    # Read Charge Voltage
    commandhighbyte = 0x00
    commandlowbyte = 0x20
    
    if rw==0:
        msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
        can0.send(msg)
        v = can_receive()
    else:
        if val==0xFFFF: val=int(sys.argv[2])
        valhighbyte = val >> 8
        vallowbyte  = val & 0xFF
        v=val
        msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte,vallowbyte,valhighbyte], is_extended_id=True)
        can0.send(msg)
        
    return v

def charge_current(rw,val=0xFFFF): #0=read, 1=set
    # print ("read/set charge current")
    # Command Code 0x0030
    # Read Charge Voltage
    commandhighbyte = 0x00
    commandlowbyte = 0x30
    
    if rw==0:
        msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
        can0.send(msg)
        v = can_receive()
    else:
        if val==0xFFFF: val=int(sys.argv[2])
        valhighbyte = val >> 8
        vallowbyte  = val & 0xFF
        v=val
        msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte,vallowbyte,valhighbyte], is_extended_id=True)
        can0.send(msg)
        
    return v

def discharge_voltage(rw,val=0xFFFF): #0=read, 1=set
    # print ("read/set discharge voltage")
    # Command Code 0x0120
    # Read Charge Voltage
    commandhighbyte = 0x01
    commandlowbyte = 0x20
    
    if rw==0:
        msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
        can0.send(msg)
        v = can_receive()
    else:
        if val==0xFFFF: val=int(sys.argv[2])
        valhighbyte = val >> 8
        vallowbyte  = val & 0xFF
        v=val
        msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte,vallowbyte,valhighbyte], is_extended_id=True)
        can0.send(msg)
        
    return v

def discharge_current(rw,val=0xFFFF): #0=read, 1=set
    # print ("read/set charge current")
    # Command Code 0x0130
    # Read Charge Voltage
    commandhighbyte = 0x01
    commandlowbyte = 0x30
    
    if rw==0:
        msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
        can0.send(msg)
        v = can_receive()
    else:
        if val==0xFFFF: val=int(sys.argv[2])
        valhighbyte = val >> 8
        vallowbyte  = val & 0xFF
        v=val
        msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte,vallowbyte,valhighbyte], is_extended_id=True)
        can0.send(msg)
        
    return v
  

def vread():
    # print ("read dc voltage")
    # Command Code 0x0060
    # Read DC Voltage

    commandhighbyte = 0x00
    commandlowbyte = 0x60

    msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
    
    v = can_receive()
    return v

def cread():
    # print ("read dc current")
    # Command Code 0x0061
    # Read DC Current

    commandhighbyte = 0x00
    commandlowbyte = 0x61

    msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
 
    msgr = str(can0.recv(0.5))
    msgr_split = msgr.split()
    hexval = (msgr_split[11]+ msgr_split[10])

    # quick and primitive solution to determine the 
    # negative charging current when discharging the battery
    
    cval = (int(hexval,16))
    if cval > 20000 :
        cval = cval - 65536
    
    print (cval)

    return cval
   

def acvread():
    # print ("read ac voltage")
    # Command Code 0x0050
    # Read AC Voltage

    commandhighbyte = 0x00
    commandlowbyte = 0x50

    msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
    v = can_receive()
    return v


def init_mode():

    # Check CANBus communication mode
    # Command Code 0x00C2
    commandhighbyte = 0x00
    commandlowbyte = 0xC2

    msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte, commandhighbyte], is_extended_id=True)
    can0.send(msg)
    cm = can_receive()

    # Check the battery mode
    # Command Code 0x0140
    # Check Battery mode
    commandhighbyte = 0x01
    commandlowbyte = 0x40

    msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte, commandhighbyte], is_extended_id=True)
    can0.send(msg)
    bm = can_receive()
    
    if ((bm == "0001") and (cm == "0003")):
        print ("The BIC-2200-xx-CAN is alread in the bi-directional battery mode with CANBus control. Nothing to do")
    
    else:
        
        print ("Set the Charge/Discharge Mode of the BIC-2200-xx-CAN.")
        print ("Only needed once to set up the Device and to configure the 'bi-directional battery mode'.")
        print ("It is recommended do disconnect the battery/load for this operation.")
        print ("Check manual if you are not shure what is the correct mode!")
        modein = input ("Do you want to change the mode? yes/no : ")
        
        if modein == "yes":
            # Command Code 0x00C2
            # Activate CANBus communication mode
            commandhighbyte = 0x00
            commandlowbyte = 0xC2
            val = 0x03
            msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte, commandhighbyte,val], is_extended_id=True)
            #can0.send(msg)
    
            time.sleep(1)

            # Command Code 0x0140
            # Set bi-directional battery mode
            commandhighbyte = 0x01
            commandlowbyte = 0x40
            val = 0x01

            msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte, commandhighbyte,val], is_extended_id=True)
            #can0.send(msg)

            print ("Repower the device to activate the new mode")



def BIC_chargemode(val): #0=charge, 1=discharge
    # print ("set direction charge")
    # Command Code 0x0100
    # Set Direction Charge

    commandhighbyte = 0x01
    commandlowbyte = 0x00
    #val = 0x00

    msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte, commandhighbyte,val], is_extended_id=True)
    can0.send(msg)


def NPB_chargemode(rw, val=0xFF):
    # print ("Set PSU or Charger Mode to NPB Device")
    # Command Code 0x00B4
    commandhighbyte = 0x00
    commandlowbyte = 0xB4

    #first Read the current value
    msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
    v = int(can_receive(),16)
    
    if rw==1: #0=read, 1=write
        #modify Bit 7 of Lowbyte
        if val==0xFF: val=int(sys.argv[3])
        if val==1:
          v = set_bit(v,7)
        else:
          v = clear_bit(v,7)

        valhighbyte = v >> 8
        vallowbyte = v & 0xFF

        #send to device
        msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte,vallowbyte,valhighbyte], is_extended_id=True)
        can0.send(msg)

        #check the current value
        msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
        can0.send(msg)
        v = int(can_receive(),16)

    return v

def typeread():
    # print ("read power supply type")
    # Command Code 0x0082
    # Command Code 0x0083
    # Read Type of PSU

    commandhighbyte = 0x00
    commandlowbyte = 0x82

    msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
    s1 = can_receive_char()

    commandlowbyte = 0x83
    msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
    s2 = can_receive_char()
    
    s=s1+s2
    print(s)
    return s

def tempread():
    # print ("read power supply temperature")
    # Command Code 0x0062
    # Read AC Voltage

    commandhighbyte = 0x00
    commandlowbyte = 0x62

    msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
    v = can_receive()
    return v

def get_normalized_bit(value, bit_index):
    return (value >> bit_index) & 1

def statusread():
    # print ("Read System Status")
    # Command Code 0x00C1
    # Read System Status
    
    commandhighbyte = 0x00
    commandlowbyte = 0xC1

    msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
    sval = can_receive()
    
    # deconding 
    s = get_normalized_bit(int(sval), bit_index=0)
    if s == 0:
        print ("Current Device is Slave")
    else:
        print ("Current Device is Master")
    
    s = get_normalized_bit(int(sval), bit_index=1)
    if s == 0:
        print ("Secondary DD output Status TOO LOW")
    else:
        print ("Secondary DD output Status NORMAL")     
        
    s = get_normalized_bit(int(sval), bit_index=2)
    if s == 0:
        print ("Primary PFC OFF oder abnormal")
    else:
        print ("Primary PFC ON normally")  
        
    s = get_normalized_bit(int(sval), bit_index=3)
    if s == 0:
        print ("Active Dummy Load off / not_supported")
    else:
        print ("Active Dummy Load on")
    
    s = get_normalized_bit(int(sval), bit_index=4)
    if s == 0:
        print ("Device in initialization status")
    else:
        print ("NOT in initialization status")     
        
    s = get_normalized_bit(int(sval), bit_index=5)
    if s == 0:
        print ("EEPROM data access normal")
    else:
        print ("EEPROM data access error") 
    
        
def faultread():
    # print ("Read System Fault Status")
    # Command Code 0x0040
    # Read System Fault Status
    
    commandhighbyte = 0x00
    commandlowbyte = 0x40

    msg = can.Message(arbitration_id=CAN_ADR, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
    sval = can_receive()

    # deconding
    s = get_normalized_bit(int(sval), bit_index=0)
    if s == 0:
        print ("FAN_FAIL: Fan working normally")
    else:
        print ("FAN_FAIL: Fan locked")

    s = get_normalized_bit(int(sval), bit_index=1)
    if s == 0:
        print ("OTP: Internal temperature normal")
    else:
        print ("OTP: Internal temperature abnormal")

    s = get_normalized_bit(int(sval), bit_index=2)
    if s == 0:
        print ("OVP: DC voltage normal")
    else:
        print ("OVP: DC over voltage protected")

    s = get_normalized_bit(int(sval), bit_index=3)
    if s == 0:
        print ("OLP: DC current normal")
    else:
        print ("OLP: DC over current protected")

    s = get_normalized_bit(int(sval), bit_index=4)
    if s == 0:
        print ("SHORT: Short circuit do not exist")
    else:
        print ("SHORT: Short circuit protected")

    s = get_normalized_bit(int(sval), bit_index=5)
    if s == 0:
        print ("AC_FAIL: AC range normal")
    else:
        print ("AC_FAIL: AC range abnormal")

    s = get_normalized_bit(int(sval), bit_index=6)
    if s == 0:
        print ("OP_OFF: DC turned on")
    else:
        print ("OP_OFF: DC turned off")

    s = get_normalized_bit(int(sval), bit_index=7)
    if s == 0:
        print ("HI_TEMP: Internal temperature normal")
    else:
        print ("HI_TEMP: Internal temperature abnormal")
 
    s = get_normalized_bit(int(sval), bit_index=8)
    if s == 0:
        print ("HV_OVP: HV voltage normal")
    else:
        print ("HV_OVP: HV over voltage preotected")


 

def command_line_argument():
    if len (sys.argv) == 1:
        print ("")
        print ("Error: First command line argument missing.")
        bic22_commands()
        error = 1
        return
    
    if   sys.argv[1] in ['on']:        operation(1)
    elif sys.argv[1] in ['off']:       operation(0)
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
    elif sys.argv[1] in ['can_up']:    can_up()
    elif sys.argv[1] in ['can_down']:  can_down()
    elif sys.argv[1] in ['init_mode']: init_mode()
    elif sys.argv[1] in ['NPB_chargemode']: NPB_chargemode(int(sys.argv[2]))
    else:
        print("")
        print("Unknown first argument '" + sys.argv[1] + "'")
        bic22_commands()
        error = 1
        return

#### Main 
if USE_RS232_CAN == 1:
    if sys.argv[1] in ['can_up']: 
        can_up()
        sys.exit(0)
    
try:
    can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
except Exception as e:
    print(e)
    print("CAN INTERFACE NOT FOUND. TRY TO BRING UP CAN DEVICE FIRST WITH -> can_up")
    sys.exit(2)

command_line_argument()

if USE_RS232_CAN == 1:
    #shutdown CAN Bus
    can0.shutdown()

sys.exit(error)
