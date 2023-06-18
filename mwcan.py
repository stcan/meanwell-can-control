############################################################################
#    Copyright (C) 2023 by macGH                                           #
#                                                                          #
#    This lib is free software; you can redistribute it and/or modify      #
#    it under the terms of the GNU General Public License as published by  #
#    the Free Software Foundation; either version 2 of the License, or     #
#    (at your option) any later version.                                   #
#                                                                          #
#    This program is distributed in the hope that it will be useful,       #
#    but WITHOUT ANY WARRANTY; without even the implied warranty of        #
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         #
#    GNU General Public License for more details.                          #
#                                                                          #
#    You should have received a copy of the GNU General Public License     #
#    along with this program; if not, write to the                         #
#    Free Software Foundation, Inc.,                                       #
#    59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             #
############################################################################

# Controlling the Mean Well devices BIC-2200 and NPB-abc0
# Please note: this Lib is currently only wokring with these 2 devices 
# and also not fully tested.
# Use at your own risk !  

# Version history
# macGH 18.06.2023  Version 0.1.0

import os
import can

######################################################################################
# Explanations
######################################################################################

######################################################################################
# def __init__(self, usedmwdev, mwcanid, useRS232, devpath, loglevel):
#
# usedmwdev = Meanwell device
# 0 = BIC2200
# 1 = NPB-abc0 (NPB-0450 .. NPB-1700)
#
# mwcanid
# ID = Cortroller Message ID + Device ID [00-07] 
# Be sure you select the right Device-ID (Jumper block on device)
# BIC-2200 00 - 07  
# NPB-abc0 00 - 03  
#
# useRS232
# If you use a RS232 to CAN Adapter which is socketCAN compartible, switch to 1
# e.g. USBTin www.fischl.de
#
# devpath
# Add the right /dev/tty device here, mostly .../dev/ttyACM0
#
# loglevel
# Enter Loglevel 0..3 [not implementted yet ;-)]
######################################################################################

######################################################################################
# const values
#SYSTEM CONFIG BITS
SYSTEM_CONFIG_CAN_CTRL       = 0
SYSTEM_CONFIG_OPERATION_INIT = 1 #BIT1 + BIT2 --> 00 .. 11

#SYSTEM STATUS BITS
SYSTEM_STATUS_M_S           = 0
SYSTEM_STATUS_DC_OK         = 1
SYSTEM_STATUS_PFC_OK        = 2
SYSTEM_STATUS_ADL_ON        = 4
SYSTEM_STATUS_INITIAL_STATE = 5
SYSTEM_STATUS_EEPER         = 6

#NPB CURVE_CONFIG BITS
CURVE_CONFIG_CUVS  =  0 #Bit0 + Bit1 --> 00 .. 11
CURVE_CONFIG_TCS   =  2 #Bit2 + Bit3 --> 00 .. 11
CURVE_CONFIG_STGS  =  6
CURVE_CONFIG_CUVE  =  7
CURVE_CONFIG_CCTOE =  8
CURVE_CONFIG_CVTOE =  9
CURVE_CONFIG_FVTOE = 10

#NPB CHG STATUS
CHG_STATUS_FULLM       =  0
CHG_STATUS_CCM         =  1
CHG_STATUS_CVM         =  2
CHG_STATUS_FVM         =  3
CHG_STATUS_WAKEUP_STOP =  6
CHG_STATUS_NTCER       = 10
CHG_STATUS_BTNC        = 11
CHG_STATUS_CCTOF       = 13
CHG_STATUS_CVTOF       = 14
CHG_STATUS_FVTOF       = 15

#FAULT STATUS BITS
FAULT_FAN_FAIL = 0
FAULT_OTP      = 1
FAULT_OVP      = 2
FAULT_OLP      = 3
FAULT_SHORT    = 4
FAULT_AC_FAIL  = 5
FAULT_OP_OFF   = 6
FAULT_HI_TEMP  = 7
FAULT_HV_OVP   = 8


#########################################
# gereral function
def set_bit(value, bit):
    return value | (1<<bit)

def clear_bit(value, bit):
    return value & ~(1<<bit)

def is_bit(value, bit):
    return bool(value & (1<<bit))

#########################################
##class
class mwcan:
  
    def __init__(self, usedmwdev, mwcanid, useRS232, devpath, loglevel):
        self.CAN_DEVICE    = devpath
        self.USE_RS232_CAN = useRS232
        self.USEDMWHW = usedmwdev 
        if usedmwdev==0: 
            CAN_ADR_S   = "0x000C03" + mwcanid
            CAN_ADR_S_R = "000c02"   + mwcanid #return from CAN is lowercase
        else:
            CAN_ADR_S   = "0x000C01" + mwcanid
            CAN_ADR_S_R = "000c00"   + mwcanid #return from CAN is lowercase

        self.CAN_ADR   = int(CAN_ADR_S,16)
        self.CAN_ADR_R = CAN_ADR_S_R           #need string to compare of return of CAN
        self.loglevel = loglevel
        
        if self.loglevel > 0: 
            print(self.CAN_ADR)
            print(self.CAN_DEVICE)
            print(self.USE_RS232_CAN)


    #########################################
    # Decode Bitstring to text
    def decode_fault_status(self,val):
        print("BIT flags: " + format(val, '#016b'))
        if self.USEDMWHW in [0]:
            if not is_bit(val,0):     print("FAULT  BIT  0: FAN working normally")
            else:                     print("FAULT  BIT  0: FAN locked")
        if self.USEDMWHW in [1]:      print("FAULT  BIT  0: NOT USED")
 
        if self.USEDMWHW in [0,1]:
            if not is_bit(val,1):     print("FAULT  BIT  1: Internal temperature normal")
            else:                     print("FAULT  BIT  1: Internal temperature abnormal")

        if self.USEDMWHW in [0,1]:
            if not is_bit(val,2):     print("FAULT  BIT  2: DC voltage normal")
            else:                     print("FAULT  BIT  2: DC voltage protected")
        
        if self.USEDMWHW in [0,1]:
            if not is_bit(val,3):     print("FAULT  BIT  3: DC voltage normal")
            else:                     print("FAULT  BIT  3: DC voltage protected")

        if self.USEDMWHW in [0,1]:
            if not is_bit(val,4):     print("FAULT  BIT  4: Shorted circuit do not exist")
            else:                     print("FAULT  BIT  4: Output shorted circuit protected")
        
        if self.USEDMWHW in [0,1]:
            if not is_bit(val,5):     print("FAULT  BIT  5: AC main normal")
            else:                     print("FAULT  BIT  5: AC abnormal protection")
        
        if self.USEDMWHW in [0,1]:
            if not is_bit(val,6):     print("FAULT  BIT  6: Output/DC turned on")
            else:                     print("FAULT  BIT  6: Output/DC turned off")

        if self.USEDMWHW in [0,1]:
            if not is_bit(val,7):     print("FAULT  BIT  7: Internal temperature normal")
            else:                     print("FAULT  BIT  7: Internal temperature abnormal")

        if self.USEDMWHW in [0]:
            if not is_bit(val,8):     print("FAULT  BIT  8: HV voltage normal")
            else:                     print("FAULT  BIT  8: HV over voltage protected")

    def decode_system_status(self,val):
        print("BIT flags: " + format(val, '#016b'))
        if self.USEDMWHW in [0]:
            if not is_bit(val,0):     print("STATUS BIT  0: Current device is Slave")
            else:                     print("STATUS BIT  0: Current device is Master")
        if self.USEDMWHW in [1]:      print("STATUS BIT  0: NOT USED")
 
        if self.USEDMWHW in [0]:
            if not is_bit(val,1):     print("STATUS BIT  1: Secondary DD output voltage status TOO LOW")
            else:                     print("STATUS BIT  1: Secondary DD output voltage status NORMAL")
        if self.USEDMWHW in [1]:
            if not is_bit(val,1):     print("STATUS BIT  1: DC output at a normal range")
            else:                     print("STATUS BIT  1: DC output too low")

        if self.USEDMWHW in [0]:
            if not is_bit(val,2):     print("STATUS BIT  2: Primary PFC OFF or abnormal")
            else:                     print("STATUS BIT  2: Primary PFC ON normally")
        if self.USEDMWHW in [1]:      print("STATUS BIT  2: NOT USED")
        
        print("STATUS BIT  3: NOT USED")
        
        if self.USEDMWHW in [0]:
            if not is_bit(val,4):     print("STATUS BIT  4: Active dummy load off/function not supported")
            else:                     print("STATUS BIT  4: Active dummy load on")
        if self.USEDMWHW in [1]:      print("STATUS BIT  4: NOT USED")
        
        if self.USEDMWHW in [0]:
            if not is_bit(val,5):     print("STATUS BIT  5: In initialization status")
            else:                     print("STATUS BIT  5: NOT in initialization status")
        if self.USEDMWHW in [1]:
            if not is_bit(val,5):     print("STATUS BIT  5: NOT in initialization status")
            else:                     print("STATUS BIT  5: In initialization status")
        
        if not is_bit(val,6):         print("STATUS BIT  6: EEPROM data access normal")
        else:                         print("STATUS BIT  6: EEPROM data access error")
        print("STATUS BIT  7: NOT USED")

    def decode_system_config(self,val):
        print("BIT flags: " + format(val, '#016b'))
        if self.USEDMWHW in [0]:
            if not is_bit(val,0):     print("CONFIG BIT  0: The output voltage/current defined by control over SVR")
            else:                     print("CONFIG BIT  0: The output voltage, current, ON/OFF control defined by control")
        if self.USEDMWHW in [1]:        print("CONFIG BIT  0: NOT USED")
        
        c = val >> 1
        if c == 0:                    print("CONFIG BIT 21: Power OFF, pre-set 0x00(OFF)")    
        if c == 1:                    print("CONFIG BIT 21: Power ON, pre-set0x01(ON)")    
        if c == 2:                    print("CONFIG BIT 21: Pre-set is previous set value")    
        if c == 3:                    print("CONFIG BIT 21: not used, reserved")    
       
    def decode_chg_status(self,val):
        if self.USEDMWHW == 0: return
        print("BIT flags: " + format(val, '#016b'))
        if self.USEDMWHW in [1]:
            if not is_bit(val,0):     print("CHG    BIT  0: Not fully charged")
            else:                     print("CHG    BIT  0: Fully charged")
 
        if self.USEDMWHW in [1]:
            if not is_bit(val,1):     print("CHG    BIT  1: The charger NOT in constant current mode")
            else:                     print("CHG    BIT  1: The charger in constant current mode")

        if self.USEDMWHW in [1]:
            if not is_bit(val,2):     print("CHG    BIT  2: The charger NOT in constant voltage mode")
            else:                     print("CHG    BIT  2: The charger in constant voltage mode")
        
        if self.USEDMWHW in [1]:
            if not is_bit(val,3):     print("CHG    BIT  3: The charger NOT in float mode")
            else:                     print("CHG    BIT  3: The charger in float mode")

        print("CHG    BIT  4: NOT USED")
        print("CHG    BIT  5: NOT USED")
        
        if self.USEDMWHW in [1]:
            if not is_bit(val,6):     print("CHG    BIT  6: Wake up finished")
            else:                     print("CHG    BIT  6: Wake up not finished")

        print("CHG    BIT  7: NOT USED")
        print("CHG    BIT  8: NOT USED")
        print("CHG    BIT  9: NOT USED")

        if self.USEDMWHW in [1]:
            if not is_bit(val,10):     print("CHG    BIT 10: NO short-circuit in the circuitry of temperature compensation")
            else:                      print("CHG    BIT 10: The circuitry of temperature compensation has short-circuited")

        if self.USEDMWHW in [1]:
            if not is_bit(val,11):     print("CHG    BIT 11: Battery detected")
            else:                      print("CHG    BIT 11: Battery NOT detected")

        print("CHG    BIT 12: NOT USED")

        if self.USEDMWHW in [1]:
            if not is_bit(val,13):     print("CHG    BIT 13: NO time out in constant current mode")
            else:                      print("CHG    BIT 13: Constant current mode time out")

        if self.USEDMWHW in [1]:
            if not is_bit(val,14):     print("CHG    BIT 14: NO time out in constant voltage mode")
            else:                      print("CHG    BIT 14: Constant voltage mode time out")

        if self.USEDMWHW in [1]:
            if not is_bit(val,15):     print("CHG    BIT 15: NO time out in float mode")
            else:                      print("CHG    BIT 15: Float mode timed out")

    #########################################
    # CAN function
    def can_up(self):
        if self.USE_RS232_CAN == 0:
            os.system('sudo ip link set can0 up type can bitrate 250000')
            os.system('sudo ifconfig can0 txqueuelen 65536')
        else:
            os.system('sudo slcand -f -s5 -o ' + self.CAN_DEVICE)
            os.system('sudo ip link set up can0')
        
        self.can0 = can.interface.Bus(channel = 'can0', bustype = 'socketcan')
        
    def can_down(self):
        self.can0.shutdown()
        os.system('sudo ip link set can0 down')

    #########################################
    # receive function
    def can_receive(self):
        msgr = str(self.can0.recv(0.5))
        msgr_split = msgr.split()
        #Check if the CAN response is from our request
        if msgr_split[3] != self.CAN_ADR_R:
            return -1
        
        if msgr_split[7] == "3":
            hexval = (msgr_split[10])
            decval = int(hexval,8)
        
        if msgr_split[7] == "4":
            hexval = (msgr_split[11]+ msgr_split[10])
            decval = int(hexval,16)
        
        if self.loglevel > 0: 
            print ("HEX: " + hexval)
            print ("DEC: " + decval)
        
        if msgr is None:
            print('Timeout occurred, no message.')
        return decval
    
    def can_receive_char(self):
        msgr = str(self.can0.recv(0.5))
        msgr_split = msgr.split()
        #Check if the CAN response is from our request
        if msgr_split[3] != self.CAN_ADR_R:
            return ""
            
        s = bytearray.fromhex(msgr_split[10]+msgr_split[11]+msgr_split[12]+msgr_split[13]+msgr_split[14]+msgr_split[15]).decode()
        if self.loglevel > 0: 
            print(s)

        if msgr is None:
            print('Timeout occurred, no message.')
        return s

    #############################################################################
    # Read Write operation function
    def can_read_write(self,lobyte,hibyte,rw,val,count=2):
        if rw==0:
            msg = can.Message(arbitration_id=self.CAN_ADR, data=[lobyte,hibyte], is_extended_id=True)
            self.can0.send(msg)
            v = self.can_receive()
        else:
            valhighbyte = val >> 8
            vallowbyte  = val & 0xFF
            if count == 1: #1 byte to send
                msg = can.Message(arbitration_id=self.CAN_ADR, data=[lobyte,hibyte,vallowbyte], is_extended_id=True)
            if count == 2: #2 byte to send
                msg = can.Message(arbitration_id=self.CAN_ADR, data=[lobyte,hibyte,vallowbyte,valhighbyte], is_extended_id=True)
            self.can0.send(msg)
            v = val
            
        return v
    
    def can_read_string(self,lobyte,hibyte,lobyte2,hibyte2):

        msg = can.Message(arbitration_id=self.CAN_ADR, data=[lobyte,hibyte], is_extended_id=True)
        self.can0.send(msg)
        s1 = self.can_receive_char()
    
        s2 = ""
        if (lobyte2 > 0) or (hibyte2 > 0):
            msg = can.Message(arbitration_id=self.CAN_ADR, data=[lobyte2,hibyte2], is_extended_id=True)
            self.can0.send(msg)
            s2 = self.can_receive_char()
        
        s=s1+s2
        if self.loglevel > 0: 
            print(s)
        return s

    #############################################################################
    # Operation function
    
    def operation(self,rw,val):#0=off, 1=on
        # print ("turn output on")
        # Command Code 0x0000
        return self.can_read_write(0x00,0x00,rw,val,1)
    
    def v_out_set(self,rw,val): #0=read, 1=set
        # print ("read/write charge voltage setting")
        # Command Code 0x0020
        # Read Charge Voltage
        return self.can_read_write(0x20,0x00,rw,val)
   
    def i_out_set(self,rw,val): #0=read, 1=set
        # print ("read/write charge current setting")
        # Command Code 0x0030
        # Set Charge Current
        return self.can_read_write(0x30,0x00,rw,val)
    
    def fault_status_read(self): #0=read, 1=set
        # print ("read Fault Status")
        # Command Code 0x0040
        # Set Charge Current
        return self.can_read_write(0x40,0x00,0,0)

    def v_in_read(self):
        # print ("read ac voltage")
        # Command Code 0x0050
        # Read AC Voltage
        return self.can_read_write(0x50,0x00,0,0)

    def v_out_read(self):
        # print ("read dc voltage")
        # Command Code 0x0060
        # Read DC Voltage
        return self.can_read_write(0x60,0x00,0,0)

    def i_out_read(self):
        # print ("read dc current")
        # Command Code 0x0061
        # Read DC Current
        v = self.can_read_write(0x61,0x00,0,0)
        #BIC-2200 return negative current with 
        if self.USEDMWHW in [0]:
             if v > 20000: v = v - 65536
        return(v)
   
    def temp_read(self):
        # print ("read power supply temperature")
        # Command Code 0x0062
        # Read internal Temperature 
        return self.can_read_write(0x62,0x00,0,0)
    
    def manu_read(self):
        # print ("read power supply Manufacturer")
        # Command Code 0x0080
        # Command Code 0x0081
        # Read Type of PSU
        return self.can_read_string(0x80,0x00,0x81,0x00)

    def type_read(self):
        # print ("read power supply type")
        # Command Code 0x0082
        # Command Code 0x0083
        # Read Type of PSU
        return self.can_read_string(0x82,0x00,0x83,0x00)
    
    def firmware_read(self):
        # print ("read power supply type")
        # Command Code 0x0084
        # Read Type of PSU
        return self.can_read_string(0x84,0x00,0x00,0x00)

    def serial_read(self):
        # print ("read power supply serial")
        # Command Code 0x0087
        # Command Code 0x0088
        # Read Type of PSU
        return self.can_read_string(0x87,0x00,0x88,0x00)

    def system_status(self):
        # print ("read system status")
        # Command Code 0x00C1
        # Read system status 
        return self.can_read_write(0xC1,0x00,0,0)

    def system_config(self,rw,val):
        # print ("read/write system config")
        # Command Code 0x00C2
        # Read/Write system config 
        return self.can_read_write(0xC2,0x00,rw,val)

    #############################################################################
    ##NPB-abcd only: Charger functions
    #############################################################################
    def NPB_curve_config(self,rw,pos,val):
        # print ("Set Bits in CURVE CONFIG of NPB Device")
        # Command Code 0x00B4
        #first Read the current value

        v = self.can_read_write(0xB4,0x00,0,0)
        
        #modify bit at pos to val
        if rw==1: #0=read, 1=write
            if val==1:
              v = set_bit(v,pos)
            else:
              v = clear_bit(v,pos)
    
        #Write it back
            v = self.can_read_write(0xB4,0x00,1,v)
        #Read to check
            v = self.can_read_write(0xB4,0x00,0,0)
    
        return v

    def chg_status_read(self):
        # print ("read Charge status")
        # Command Code 0x00B8
        # Read/Write system config 
        return self.can_read_write(0xB8,0x00,0,0)

    #############################################################################
    ##BIC-2200 only - charge dischagre functions
    #############################################################################
    def BIC_chargemode(self,val): #0=charge, 1=discharge
        # print ("set direction charge")
        # Command Code 0x0100
        # Set Direction Charge
        return self.can_read_write(0x00,0x01,1,val,1)

    def BIC_discharge_v(self,rw,val):
        # print ("read/write discharge voltage setting")
        # Command Code 0x0120
        # Set Discharge Voltage
        return self.can_read_write(0x20,0x01,rw,val)
    
    def BIC_discharge_i(self,rw,val):
        # print ("read/write discharge current setting")
        # Command Code 0x0130
        # Read Discharge Current
        return self.can_read_write(0x30,0x01,rw,val)
