# meanwell-can-control
Tool to control Power Supplys from Mean Well via CAN Bus

Tested with the 24V Version BIC-2200-24-CAN and NPB-abc0 Series Charger

Please note:  this tool is not yet complete and also not fully tested. Do not use without monitoring the devices. There is no error handling yet !!!

What is missing:
- variables plausibility check

       Usage: ./bic2200.py parameter value

       on                   -- output on
       off                  -- output off
       statusread           -- read output status 1:on 0:off 

       cvread               -- read charge voltage setting
       cvset <value>        -- set charge voltage
       ccread               -- read charge current setting
       ccset <value>        -- set charge current

       dvread               -- read discharge voltage setting
       dvset <value>        -- set discharge voltage
       dcread               -- read discharge current setting
       dcset <value>        -- set discharge current

       vread                -- read DC voltage
       cread                -- read DC current
       acvread              -- read AC voltage

       charge               -- set direction charge battery
       discharge            -- set direction discharge battery
       dirread              -- read direction 0:charge,1:discharge

       tempread             -- read power supply temperature
       fanread              -- read fan 1 and 2 revs.

       typeread             -- read type
       fwread               -- read firmware version
       statusread           -- read status
       faultread            -- read fault status
       configread           -- read control and eeprom mode
       configset            -- set control and eeprom mode
       batterymodeset       -- set battery mode

       can_up               -- start can bus
       can_down             -- shut can bus down

       <value> = amps oder volts * 100 --> 25,66V = 2566 


#  Steps to put a new BIC into operation

- Connect the BIC2200 CAN Bus to the Computer/Raspberry Pi/... 
- Do not connect the battery !!! That is very important, because the BIC is in SVR Mode and therefore it is impossible to cotrol it via CAN BUS.
- Connect 230V AC and switch the device on.
- Check if the communication is working. 
      ./bic2200.py configread
- Edit bic2200.py to set 
      CAN_control = 0x01
      Power_on_state = 0x04
      EEPROM_Storage = 0x00
      EEPROM_Config = 0x02
   The alternatives are described in the software and the manual
-  Activate the CAN communication and control EEPROM writing
      ./bic2200.py configset 
-  Activate the "Bidirectional Battery Mode" which we need to control the BIC2200 via CAN
      ./bic2200.py batterymodeset
- Power the device off an on, now the battery mode ist active. Check with "
      ./bic2200.py configread
- Set Values for Voltages an currents. For my 8s 24V System I start with
      ./bic2200.py cvset 2700
      ./bic2200.py dvset 2400
      ./bic2200.py ccset 0
      ./bic2200.py dcset 0

      ./bic2200.py dirset charge
      ./bic2200.py off

- Now switch the device off and connect the battery
- Switch AC Power on and you have full control with the bic2200.px software
 

# examples        
Example code to control battery charging and discharging depending on the electricity meter. 

All scripts are without any warranty. Use at your own risk
