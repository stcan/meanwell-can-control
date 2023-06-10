#!/usr/bin/env python3

# bic2200.py
# Controlling the Mean Well BIC-2200-CAN
# tested only with the 24V Version BIC-2200-CAN-24
# Please note:  this software to control the BIC-2200 is not yet complete 
# and also not fully tested. The BIC-2200 should not be operated unattended. 
# There is no error handling yet !!!

# What is missing:
# - status queries
# - error handling
# - variables plausibility check
# - programming missing functions 
# - current and voltage maximum settings

# steve 08.06.2023  Version 0.2.1
# steve 10.06.2023  Version 0.2.2

import os
import can
import sys

error=1

can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')

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
    print("       can_up               -- start can bus")
    print("       can_down             -- shut can bus down")
    print("")
    print("       <value> = amps oder volts * 100 --> 25,66V = 2566")

def can_receive():
    msgr = str(can0.recv(0.5))
    msgr_split = msgr.split()
    hexval = (msgr_split[11]+ msgr_split[10])
    print (int(hexval,16))
    
    if msgr is None:
        print('Timeout occurred, no message.')

def can_up():
    os.system('sudo ip link set can0 up type can bitrate 250000')
    os.system('sudo ifconfig can0 txqueuelen 65536')

def can_down():
    os.system('sudo ip link set can0 down')

def output_on():
    print ("turn output on")
    # Command Code 0x0000
    commandhighbyte = 0x00
    commandlowbyte = 0x00
    val = 0x01
 
    msg = can.Message(arbitration_id=0x000C0300, data=[commandlowbyte, commandhighbyte,val], is_extended_id=True)
    can0.send(msg)

def output_off():
    print ("turn output off")
    # Command Code 0x0000
    commandhighbyte = 0x00
    commandlowbyte = 0x00
    val = 0x00
 
    msg = can.Message(arbitration_id=0x000C0300, data=[commandlowbyte, commandhighbyte,val], is_extended_id=True)
    can0.send(msg)

def cvread():
    # print ("read charge voltage setting")
    # Command Code 0x0020
    # Read Charge Voltage
    commandhighbyte = 0x00
    commandlowbyte = 0x20

    msg = can.Message(arbitration_id=0x000C0300, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
    can_receive()

def cvset():
    # print ("set the charge voltage")
    # Command Code 0x0020
    # Set Charge Voltage

    commandhighbyte = 0x00
    commandlowbyte = 0x20

    wert = int(sys.argv[2])
    valhighbyte = wert >> 8
    vallowbyte = wert & 0xFF

    msg = can.Message(arbitration_id=0x000C0300, data=[commandlowbyte,commandhighbyte,vallowbyte,valhighbyte], is_extended_id=True)

    can0.send(msg)
    wert = 0

def ccread():
    # print ("read charge current setting")
    # Command Code 0x0030
    # Set Charge Current
    commandhighbyte = 0x00
    commandlowbyte = 0x30

    msg = can.Message(arbitration_id=0x000C0300, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
    can_receive()

def ccset():
    # print ("set the charge current")
    # Command Code 0x0030
    # Set Charge Current

    commandhighbyte = 0x00
    commandlowbyte = 0x30

    wert = int(sys.argv[2])
    valhighbyte = wert >> 8
    vallowbyte = wert & 0xFF

    msg = can.Message(arbitration_id=0x000C0300, data=[commandlowbyte,commandhighbyte,vallowbyte,valhighbyte], is_extended_id=True)
    can0.send(msg)
    wert = 0

def dvread():
    # print ("read discharge voltage setting")
    # Command Code 0x0120
    # Set Discharge Voltage

    commandhighbyte = 0x01
    commandlowbyte = 0x20

    msg = can.Message(arbitration_id=0x000C0300, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
    can_receive()    

def dvset():
    # print ("set the discharge voltage")
    # Command Code 0x0120
    # Set Discharge Voltage

    commandhighbyte = 0x01
    commandlowbyte = 0x20

    wert = int(sys.argv[2])
    valhighbyte = wert >> 8
    vallowbyte = wert & 0xFF

    msg = can.Message(arbitration_id=0x000C0300, data=[commandlowbyte,commandhighbyte,vallowbyte,valhighbyte], is_extended_id=True)
    can0.send(msg)
    wert = 0

def dcread():
    # print ("read discharge current setting")
    # Command Code 0x0130
    # Read Discharge Current

    commandhighbyte = 0x01
    commandlowbyte = 0x30

    msg = can.Message(arbitration_id=0x000C0300, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
    can_receive()

def dcset():
    # print ("set the discharge current")
    # Command Code 0x0130
    # Set Discharge Current

    commandhighbyte = 0x01
    commandlowbyte = 0x30

    wert = int(sys.argv[2])
    valhighbyte = wert >> 8
    vallowbyte = wert & 0xFF

    msg = can.Message(arbitration_id=0x000C0300, data=[commandlowbyte,commandhighbyte,vallowbyte,valhighbyte], is_extended_id=True)
    can0.send(msg)
    wert = 0
    

def vread():
    # print ("read dc voltage")
    # Command Code 0x0060
    # Read DC Voltage

    commandhighbyte = 0x00
    commandlowbyte = 0x60

    msg = can.Message(arbitration_id=0x000C0300, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
    can_receive()

def cread():
    # print ("read dc current")
    # Command Code 0x0061
    # Read DC Current

    commandhighbyte = 0x00
    commandlowbyte = 0x61

    msg = can.Message(arbitration_id=0x000C0300, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
   
    msgr = str(can0.recv(0.5))
    msgr_split = msgr.split()
    hexval = (msgr_split[11]+ msgr_split[10])
    
    cval = (int(hexval,16))
    if cval > 20000 :
        cval = cval  -65536
    
    print (cval)
    

def acvread():
    # print ("read ac voltage")
    # Command Code 0x0050
    # Read AC Voltage

    commandhighbyte = 0x00
    commandlowbyte = 0x50

    msg = can.Message(arbitration_id=0x000C0300, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
    can_receive()

def charge():
    # print ("set direction charge")
    # Command Code 0x0100
    # Set Direction Charge

    commandhighbyte = 0x01
    commandlowbyte = 0x00
    val = 0x00

    msg = can.Message(arbitration_id=0x000C0300, data=[commandlowbyte, commandhighbyte,val], is_extended_id=True)
    can0.send(msg)

def discharge():
    # print ("set direction discharge")
    # Command Code 0x0100
    # Set Direction Discharge

    commandhighbyte = 0x01
    commandlowbyte = 0x00
    val = 0x01

    msg = can.Message(arbitration_id=0x000C0300, data=[commandlowbyte, commandhighbyte,val], is_extended_id=True)
    can0.send(msg)

def tempread():
    # print ("read power supply temperature")
    # Command Code 0x0050
    # Read AC Voltage

    commandhighbyte = 0x00
    commandlowbyte = 0x50

    msg = can.Message(arbitration_id=0x000C0300, data=[commandlowbyte,commandhighbyte], is_extended_id=True)
    can0.send(msg)
    can_receive()

def command_line_argument():
    if len (sys.argv) == 1:
        print ("")
        print ("Error: First command line argument missing.")
        bic22_commands()
        sys.exit(error)
    elif sys.argv[1] in ['on']: output_on()
    elif sys.argv[1] in ['off']: output_off()
    elif sys.argv[1] in ['cvread']: cvread()
    elif sys.argv[1] in ['cvset']: cvset()
    elif sys.argv[1] in ['ccread']: ccread()
    elif sys.argv[1] in ['ccset']: ccset()
    elif sys.argv[1] in ['dvread']: dvread()
    elif sys.argv[1] in ['dvset']: dvset()
    elif sys.argv[1] in ['dcread']: dcread()
    elif sys.argv[1] in ['dcset']: dcset()
    elif sys.argv[1] in ['vread']: vread()
    elif sys.argv[1] in ['cread']: cread()
    elif sys.argv[1] in ['acvread']: acvread()
    elif sys.argv[1] in ['charge']: charge()
    elif sys.argv[1] in ['discharge']: discharge()
    elif sys.argv[1] in ['tempread']: tempread()
    elif sys.argv[1] in ['can_up']: can_up()
    elif sys.argv[1] in ['can_down']: can_down()
    else:
        print("")
        print("Unknown first argument '" + sys.argv[1] + "'")
        bic22_commands()
        sys.exit(error)


#### Main 

command_line_argument()
